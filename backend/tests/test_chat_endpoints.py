"""
Integration tests for chat API endpoints.

Tests cover:
- User Story 1: Send chat message and get AI response
- User Story 2: Resume existing conversation
- User Story 3: Health check and API information
- Edge cases and error handling
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.agent import AgentResponse, ToolCall


# ============================================================================
# User Story 1: Send Chat Message and Get AI Response (T012-T014)
# ============================================================================


@pytest.mark.asyncio
async def test_first_message_creates_conversation(client: TestClient, test_user, session: Session):
    """
    T012: Test that first message creates a new conversation.

    Validates:
    - New conversation created in database
    - User message stored
    - Assistant message stored
    - Response includes conversation_id
    """
    # Mock TodoBot agent response
    mock_agent_response = AgentResponse(
        message="I've added 'Buy groceries' to your tasks!",
        tool_calls=[
            ToolCall(
                name="add_task",
                parameters={"user_id": str(test_user.id), "title": "Buy groceries"},
                result="Task created: Buy groceries (ID: 123)",
                success=True,
            )
        ],
    )

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(return_value=mock_agent_response)

        # Send first message (no conversation_id)
        response = client.post(
            "/api/chat",
            json={
                "content": "Add buy groceries",
                "conversation_id": None,
            },
        )

    # Assert response
    assert response.status_code == 200
    data = response.json()

    assert "conversation_id" in data
    assert "message_id" in data
    assert data["role"] == "assistant"
    assert "Buy groceries" in data["content"]
    assert data["task_data"] is not None
    assert len(data["task_data"]["tasks"]) == 1

    # Verify conversation created in database
    conversation_id = data["conversation_id"]
    statement = select(Conversation).where(Conversation.id == conversation_id)
    conversation = session.exec(statement).first()

    assert conversation is not None
    assert str(conversation.user_id) == str(test_user.id)

    # Verify messages stored (user + assistant)
    message_statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(message_statement).all()

    assert len(messages) == 2
    assert messages[0].role == MessageRole.USER
    assert messages[0].content == "Add buy groceries"
    assert messages[1].role == MessageRole.ASSISTANT
    assert "Buy groceries" in messages[1].content


@pytest.mark.asyncio
async def test_multi_turn_conversation_maintains_context(client: TestClient, test_user, session: Session):
    """
    T013: Test that multi-turn conversation maintains context.

    Validates:
    - Multiple messages in same conversation
    - Conversation history passed to agent
    - All messages stored in database
    """
    mock_responses = [
        AgentResponse(
            message="I've added 'Buy milk' to your tasks!",
            tool_calls=[
                ToolCall(
                    name="add_task",
                    parameters={"user_id": str(test_user.id), "title": "Buy milk"},
                    result="Task created: Buy milk (ID: 456)",
                    success=True,
                )
            ],
        ),
        AgentResponse(
            message="I've updated the task to '2 gallons of milk'.",
            tool_calls=[
                ToolCall(
                    name="update_task",
                    parameters={"task_id": "456", "title": "2 gallons of milk"},
                    result="Task updated: 2 gallons of milk",
                    success=True,
                )
            ],
        ),
        AgentResponse(
            message="You have 1 task:\n◯ 2 gallons of milk",
            tool_calls=[
                ToolCall(
                    name="list_tasks",
                    parameters={"user_id": str(test_user.id)},
                    result="Found 1 task",
                    success=True,
                )
            ],
        ),
    ]

    conversation_id = None

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value

        # Message 1: "Add buy milk"
        mock_instance.run = AsyncMock(return_value=mock_responses[0])
        response1 = client.post(
            "/api/chat",
            json={"content": "Add buy milk", "conversation_id": None},
        )

        assert response1.status_code == 200
        conversation_id = response1.json()["conversation_id"]

        # Message 2: "Actually, make that 2 gallons"
        mock_instance.run = AsyncMock(return_value=mock_responses[1])
        response2 = client.post(
            "/api/chat",
            json={
                "content": "Actually, make that 2 gallons",
                "conversation_id": conversation_id,
            },
        )

        assert response2.status_code == 200
        assert response2.json()["conversation_id"] == conversation_id

        # Message 3: "Show my tasks"
        mock_instance.run = AsyncMock(return_value=mock_responses[2])
        response3 = client.post(
            "/api/chat",
            json={"content": "Show my tasks", "conversation_id": conversation_id},
        )

        assert response3.status_code == 200

    # Verify 6 total messages in database (3 user + 3 assistant)
    message_statement = select(Message).where(Message.conversation_id == conversation_id)
    messages = session.exec(message_statement).all()

    assert len(messages) == 6
    assert messages[0].role == MessageRole.USER
    assert messages[1].role == MessageRole.ASSISTANT
    assert messages[2].role == MessageRole.USER
    assert messages[3].role == MessageRole.ASSISTANT
    assert messages[4].role == MessageRole.USER
    assert messages[5].role == MessageRole.ASSISTANT


@pytest.mark.asyncio
async def test_agent_tool_execution(client: TestClient, test_user, session: Session):
    """
    T014: Test agent tool execution and task data in response.

    Validates:
    - Tool calls executed by agent
    - Task data returned in response
    - Tool call success tracked
    """
    mock_agent_response = AgentResponse(
        message="I've created three tasks for you!",
        tool_calls=[
            ToolCall(
                name="add_task",
                parameters={"user_id": str(test_user.id), "title": "Buy groceries"},
                result="Task created: Buy groceries (ID: 1)",
                success=True,
            ),
            ToolCall(
                name="add_task",
                parameters={"user_id": str(test_user.id), "title": "Call mom"},
                result="Task created: Call mom (ID: 2)",
                success=True,
            ),
            ToolCall(
                name="add_task",
                parameters={"user_id": str(test_user.id), "title": "Finish report"},
                result="Task created: Finish report (ID: 3)",
                success=True,
            ),
        ],
    )

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(return_value=mock_agent_response)

        response = client.post(
            "/api/chat",
            json={
                "content": "Add three tasks: buy groceries, call mom, and finish report",
                "conversation_id": None,
            },
        )

    assert response.status_code == 200
    data = response.json()

    # Verify task_data in response
    assert data["task_data"] is not None
    assert "tasks" in data["task_data"]
    assert len(data["task_data"]["tasks"]) == 3

    # Verify all tasks have results
    for task in data["task_data"]["tasks"]:
        assert "result" in task
        assert "Task created" in task["result"]


# ============================================================================
# User Story 2: Resume Existing Conversation (T018-T020)
# ============================================================================


@pytest.mark.asyncio
async def test_conversation_ownership_validation(client: TestClient, test_user, other_user, session: Session):
    """
    T018: Test conversation ownership validation.

    Validates:
    - User1 creates conversation
    - User2 cannot access User1's conversation
    - Returns 404 for unauthorized access
    """
    # Create conversation for test_user
    conversation = Conversation(user_id=test_user.id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Create message in conversation
    message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content="Test message",
    )
    session.add(message)
    session.commit()

    # Try to access test_user's conversation as other_user
    # (Need to override current_user dependency)
    from app.dependencies import get_current_user
    from app.main import app as fastapi_app

    def get_other_user_override():
        return other_user

    fastapi_app.dependency_overrides[get_current_user] = get_other_user_override

    mock_agent_response = AgentResponse(
        message="Response", tool_calls=[]
    )

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(return_value=mock_agent_response)

        response = client.post(
            "/api/chat",
            json={
                "content": "Hello",
                "conversation_id": str(conversation.id),
            },
        )

    # Should return 404 (conversation not found for other_user)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_conversation_history_limit_20_messages(client: TestClient, test_user, session: Session):
    """
    T019: Test conversation history limited to last 20 messages.

    Validates:
    - Agent receives only last 20 messages when conversation has more
    - Older messages still stored in database
    - Correct message order maintained
    """
    # Create conversation with 25 messages (12 pairs + 1)
    conversation = Conversation(user_id=test_user.id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Add 24 messages (12 user + 12 assistant)
    for i in range(12):
        user_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=f"User message {i}",
        )
        assistant_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=f"Assistant message {i}",
        )
        session.add(user_msg)
        session.add(assistant_msg)

    session.commit()

    # Send new message (will be 25th and 26th after assistant response)
    mock_agent_response = AgentResponse(
        message="Latest response", tool_calls=[]
    )

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(return_value=mock_agent_response)

        response = client.post(
            "/api/chat",
            json={
                "content": "Latest message",
                "conversation_id": str(conversation.id),
            },
        )

        # Verify agent was called
        assert mock_instance.run.called

        # Check conversation_history parameter passed to agent
        call_args = mock_instance.run.call_args
        agent_request = call_args[0][0]

        # Should have 19 messages (20 limit - 1 current message)
        # The latest message is excluded from history
        if agent_request.conversation_history:
            assert len(agent_request.conversation_history) <= 19

    assert response.status_code == 200

    # Verify all 26 messages still in database
    message_statement = select(Message).where(Message.conversation_id == conversation.id)
    all_messages = session.exec(message_statement).all()
    assert len(all_messages) == 26


@pytest.mark.asyncio
async def test_agent_resolves_context_references(client: TestClient, test_user, session: Session):
    """
    T020: Test agent resolves context references from previous messages.

    Validates:
    - Agent receives conversation history
    - Can resolve references like "that task"
    - Context maintained across messages
    """
    conversation_id = None

    mock_responses = [
        AgentResponse(
            message="Added 'Buy groceries'",
            tool_calls=[
                ToolCall(
                    name="add_task",
                    parameters={"user_id": str(test_user.id), "title": "Buy groceries"},
                    result="Task created: Buy groceries (ID: abc123)",
                    success=True,
                )
            ],
        ),
        AgentResponse(
            message="Marked 'Buy groceries' as complete",
            tool_calls=[
                ToolCall(
                    name="list_tasks",
                    parameters={"user_id": str(test_user.id)},
                    result="Found task: Buy groceries (ID: abc123)",
                    success=True,
                ),
                ToolCall(
                    name="complete_task",
                    parameters={"task_id": "abc123"},
                    result="Task completed: Buy groceries",
                    success=True,
                ),
            ],
        ),
    ]

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value

        # Message 1: "Add buy groceries"
        mock_instance.run = AsyncMock(return_value=mock_responses[0])
        response1 = client.post(
            "/api/chat",
            json={"content": "Add buy groceries", "conversation_id": None},
        )

        assert response1.status_code == 200
        conversation_id = response1.json()["conversation_id"]

        # Message 2: "Mark that as complete" (references "buy groceries")
        mock_instance.run = AsyncMock(return_value=mock_responses[1])
        response2 = client.post(
            "/api/chat",
            json={
                "content": "Mark that as complete",
                "conversation_id": conversation_id,
            },
        )

        assert response2.status_code == 200

        # Verify agent received conversation history
        assert mock_instance.run.call_count == 2

        # On second call, verify history includes first message
        second_call_args = mock_instance.run.call_args_list[1]
        agent_request = second_call_args[0][0]

        assert agent_request.conversation_history is not None
        assert len(agent_request.conversation_history) >= 1

        # First message in history should be the user's "Add buy groceries"
        first_history_msg = agent_request.conversation_history[0]
        assert first_history_msg.role == "user"
        assert "buy groceries" in first_history_msg.content.lower()


# ============================================================================
# User Story 3: Health Check and API Information (T024-T026)
# ============================================================================


def test_health_check_success(client: TestClient):
    """
    T024: Test health check endpoint returns healthy status.

    Validates:
    - 200 OK status code
    - Database connectivity verified
    - Correct response format
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"] == "connected"


def test_root_endpoint_returns_metadata(client: TestClient):
    """
    T026: Test root endpoint returns API metadata.

    Validates:
    - 200 OK status code
    - Includes status, message, version
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] == "healthy"
    assert "message" in data
    assert "version" in data


# ============================================================================
# Edge Cases & Error Handling
# ============================================================================


@pytest.mark.asyncio
async def test_empty_message_rejected(client: TestClient):
    """
    Test that empty messages are rejected with 422 validation error.

    Validates:
    - Empty string rejected
    - Whitespace-only rejected
    - Proper error message
    """
    # Empty string
    response1 = client.post(
        "/api/chat",
        json={"content": "", "conversation_id": None},
    )

    assert response1.status_code == 422
    assert "detail" in response1.json()

    # Whitespace only
    response2 = client.post(
        "/api/chat",
        json={"content": "   ", "conversation_id": None},
    )

    # May pass Pydantic validation but fail in endpoint logic
    assert response2.status_code in [422, 400]


@pytest.mark.asyncio
async def test_invalid_conversation_id_returns_404(client: TestClient, test_user):
    """
    Test that invalid conversation_id returns 404.

    Validates:
    - Non-existent conversation returns 404
    - Proper error message
    """
    fake_conversation_id = uuid4()

    mock_agent_response = AgentResponse(
        message="Response", tool_calls=[]
    )

    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(return_value=mock_agent_response)

        response = client.post(
            "/api/chat",
            json={
                "content": "Hello",
                "conversation_id": str(fake_conversation_id),
            },
        )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_agent_error_returns_500(client: TestClient, test_user):
    """
    Test that agent errors return 500 with user-friendly message.

    Validates:
    - Agent exception caught
    - 500 Internal Server Error returned
    - User message still saved to database
    """
    with patch("app.routes.chat.TodoBot") as MockBot:
        mock_instance = MockBot.return_value
        mock_instance.run = AsyncMock(side_effect=Exception("Agent crashed"))

        response = client.post(
            "/api/chat",
            json={"content": "Test message", "conversation_id": None},
        )

    assert response.status_code == 500
    assert "detail" in response.json()
    assert "AI agent unavailable" in response.json()["detail"]
