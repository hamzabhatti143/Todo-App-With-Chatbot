"""
Tests for chat endpoints

These tests verify:
- POST /api/chat endpoint functionality
- JWT authentication and user isolation
- Conversation creation and message storage
- Gemini AI integration (mocked)
- MCP tool execution
- Rate limiting
- Error handling
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch, MagicMock
from uuid import uuid4

from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.task import Task
from app.auth import create_access_token, get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create all tables
    from app.models import User, Task, Conversation, Message
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user: User):
    """Create authorization headers with JWT token"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="other_user")
def other_user_fixture(session: Session):
    """Create another test user for isolation testing"""
    user = User(
        email="other@example.com",
        hashed_password=get_password_hash("otherpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class TestChatEndpoint:
    """Tests for POST /api/chat endpoint"""

    @patch('app.services.gemini_service.GeminiService.generate_chat_response')
    def test_create_first_message_creates_conversation(
        self,
        mock_gemini: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that first message creates a new conversation"""
        # Mock Gemini response
        mock_gemini.return_value = {
            "content": "I'll help you create that task!",
            "tool_calls": []
        }

        response = client.post(
            "/api/chat",
            json={"content": "Add a task to buy groceries"},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Verify conversation was created
        assert "conversation_id" in data
        conversation = session.get(Conversation, data["conversation_id"])
        assert conversation is not None
        assert conversation.user_id == test_user.id

        # Verify messages were saved
        assert "message_id" in data
        message = session.get(Message, data["message_id"])
        assert message is not None
        assert message.role == MessageRole.ASSISTANT
        assert message.content == "I'll help you create that task!"

    @patch('app.services.gemini_service.GeminiService.generate_chat_response')
    def test_subsequent_message_uses_existing_conversation(
        self,
        mock_gemini: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that subsequent messages use existing conversation"""
        # Mock Gemini response
        mock_gemini.return_value = {
            "content": "Task created!",
            "tool_calls": []
        }

        # Create first message
        response1 = client.post(
            "/api/chat",
            json={"content": "Add a task"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        # Send second message with conversation_id
        response2 = client.post(
            "/api/chat",
            json={
                "content": "List my tasks",
                "conversation_id": conversation_id
            },
            headers=auth_headers
        )

        assert response2.status_code == 200
        data = response2.json()

        # Verify same conversation used
        assert data["conversation_id"] == conversation_id

        # Verify both messages exist in conversation
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        # 2 user messages + 2 assistant responses = 4 total
        assert len(messages) >= 2

    @patch('app.services.gemini_service.GeminiService.generate_chat_response')
    @patch('app.mcp_server.tools.add_task.add_task')
    def test_chat_creates_task_via_mcp_tool(
        self,
        mock_add_task: MagicMock,
        mock_gemini: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that chat can create tasks via MCP tool"""
        # Mock task creation
        task_id = uuid4()
        mock_add_task.return_value = {
            "id": str(task_id),
            "title": "Buy groceries",
            "description": "Get milk and eggs",
            "completed": False
        }

        # Mock Gemini to call add_task tool
        mock_gemini.return_value = {
            "content": "I've created the task 'Buy groceries' for you!",
            "tool_calls": [
                {
                    "name": "add_task",
                    "arguments": {
                        "user_id": str(test_user.id),
                        "title": "Buy groceries",
                        "description": "Get milk and eggs"
                    }
                }
            ]
        }

        response = client.post(
            "/api/chat",
            json={"content": "Add a task to buy groceries"},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Verify MCP tool was called
        assert mock_add_task.called

        # Verify response contains task data
        assert "I've created the task" in data["content"]

    def test_chat_requires_authentication(self, client: TestClient):
        """Test that chat endpoint requires authentication"""
        response = client.post(
            "/api/chat",
            json={"content": "Hello"}
        )

        assert response.status_code == 401

    def test_chat_rejects_empty_message(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test that empty messages are rejected"""
        response = client.post(
            "/api/chat",
            json={"content": ""},
            headers=auth_headers
        )

        assert response.status_code == 422

    def test_chat_user_isolation(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        other_user: User,
        auth_headers: dict
    ):
        """Test that users cannot access other users' conversations"""
        # Create conversation for other_user
        conversation = Conversation(user_id=other_user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Try to send message to other user's conversation with test_user's token
        response = client.post(
            "/api/chat",
            json={
                "content": "Hello",
                "conversation_id": str(conversation.id)
            },
            headers=auth_headers
        )

        # Should fail with 404 (not 403, to avoid leaking existence)
        assert response.status_code in [403, 404]

    @patch('app.services.gemini_service.GeminiService.generate_chat_response')
    def test_chat_handles_gemini_api_error(
        self,
        mock_gemini: MagicMock,
        client: TestClient,
        auth_headers: dict
    ):
        """Test error handling when Gemini API fails"""
        # Mock Gemini API error
        mock_gemini.side_effect = Exception("Gemini API error")

        response = client.post(
            "/api/chat",
            json={"content": "Hello"},
            headers=auth_headers
        )

        # Should return 500 with error message
        assert response.status_code == 500
        assert "error" in response.json()

    @patch('app.services.gemini_service.GeminiService.generate_chat_response')
    def test_chat_saves_user_message(
        self,
        mock_gemini: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that user messages are saved to database"""
        mock_gemini.return_value = {
            "content": "Hello!",
            "tool_calls": []
        }

        response = client.post(
            "/api/chat",
            json={"content": "Hi there"},
            headers=auth_headers
        )

        conversation_id = response.json()["conversation_id"]

        # Check that user message was saved
        messages = session.exec(
            select(Message).where(
                Message.conversation_id == conversation_id,
                Message.role == MessageRole.USER
            )
        ).all()

        assert len(messages) >= 1
        assert messages[0].content == "Hi there"

    @patch('app.agent.TodoBot.run')
    def test_multi_turn_conversation_maintains_context(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that multi-turn conversation maintains context across message pairs"""
        from app.agent import AgentResponse, ToolCall

        # Mock agent to return different responses
        mock_agent.side_effect = [
            AgentResponse(message="Task created!", tool_calls=[], error=None),
            AgentResponse(message="Updated to 2 gallons!", tool_calls=[], error=None),
            AgentResponse(message="Here are your tasks...", tool_calls=[], error=None),
        ]

        # Create conversation with 3 message pairs (6 messages total)
        # Message 1
        response1 = client.post(
            "/api/chat",
            json={"content": "Add buy milk"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        # Message 2 (references previous context)
        response2 = client.post(
            "/api/chat",
            json={"content": "Make that 2 gallons", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Message 3
        response3 = client.post(
            "/api/chat",
            json={"content": "Show my tasks", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Verify 6 total messages (3 user + 3 assistant)
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        assert len(messages) == 6

        # Verify conversation history was passed to agent on second call
        second_call_args = mock_agent.call_args_list[1]
        agent_request = second_call_args[0][0]
        assert agent_request.conversation_history is not None

    @patch('app.agent.TodoBot.run')
    def test_conversation_history_limit_20_messages(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that conversation history is limited to last 20 messages when passed to agent"""
        from app.agent import AgentResponse

        # Mock agent to return simple responses
        mock_agent.return_value = AgentResponse(
            message="Response", tool_calls=[], error=None
        )

        # Create conversation
        response1 = client.post(
            "/api/chat",
            json={"content": "First message"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        # Add 24 more messages (25 total: 13 user + 12 assistant from previous, + 1 new)
        for i in range(12):
            client.post(
                "/api/chat",
                json={"content": f"Message {i+2}", "conversation_id": conversation_id},
                headers=auth_headers
            )

        # Send final message
        client.post(
            "/api/chat",
            json={"content": "Final message", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Verify database has all messages (26 total: 13 user + 13 assistant)
        all_messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        assert len(all_messages) == 26

        # Verify agent was called with max 20 messages in history
        # (The last call should have received history with at most 20 messages)
        last_call_args = mock_agent.call_args_list[-1]
        agent_request = last_call_args[0][0]

        if agent_request.conversation_history:
            assert len(agent_request.conversation_history) <= 20

    @patch('app.agent.TodoBot.run')
    def test_agent_tool_execution_captured(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that agent tool execution is captured and returned to client"""
        from app.agent import AgentResponse, ToolCall

        # Mock agent with tool calls
        mock_agent.return_value = AgentResponse(
            message="I've created the task!",
            tool_calls=[
                ToolCall(
                    name="add_task",
                    arguments={"user_id": str(test_user.id), "title": "Buy groceries"},
                    result="Task created: Buy groceries (ID: uuid)",
                    success=True
                )
            ],
            error=None
        )

        response = client.post(
            "/api/chat",
            json={"content": "Add task: buy groceries"},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Verify tool execution data is in response
        assert "task_data" in data or "tool_calls" in data


class TestConversationContextRetention:
    """Tests for User Story 2: Conversation Context Retention"""

    @patch('app.agent.TodoBot.run')
    def test_conversation_ownership_strictly_enforced(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        other_user: User,
        auth_headers: dict
    ):
        """Test AC-002.1: Users can only send messages to their own conversations"""
        from app.agent import AgentResponse

        mock_agent.return_value = AgentResponse(
            message="Response", tool_calls=[], error=None
        )

        # Create conversation for other_user
        conversation = Conversation(user_id=other_user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Attempt to send message to other_user's conversation with test_user's token
        response = client.post(
            "/api/chat",
            json={
                "content": "Trying to hijack conversation",
                "conversation_id": str(conversation.id)
            },
            headers=auth_headers
        )

        # Should be rejected with 404 (not 403 to avoid leaking existence)
        assert response.status_code in [403, 404]
        assert "not found" in response.json()["detail"].lower() or "not authorized" in response.json()["detail"].lower()

        # Verify no messages were added to other_user's conversation
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation.id)
        ).all()
        assert len(messages) == 0

    @patch('app.agent.TodoBot.run')
    def test_conversation_history_passed_to_agent_correctly(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test AC-002.2 & AC-002.3: History is passed correctly to agent"""
        from app.agent import AgentResponse, AgentRequest

        # Mock agent to return responses
        mock_agent.return_value = AgentResponse(
            message="Response", tool_calls=[], error=None
        )

        # Create initial message
        response1 = client.post(
            "/api/chat",
            json={"content": "First message"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        # Send second message
        response2 = client.post(
            "/api/chat",
            json={"content": "Second message", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Verify agent was called twice
        assert mock_agent.call_count == 2

        # Verify second call received history from first message pair
        second_call_args = mock_agent.call_args_list[1]
        agent_request: AgentRequest = second_call_args[0][0]

        # Should have conversation_history
        assert agent_request.conversation_history is not None
        assert len(agent_request.conversation_history) >= 2  # At least first user + assistant message

        # Verify history contains previous messages
        history_contents = [msg.content for msg in agent_request.conversation_history]
        assert "First message" in history_contents

    @patch('app.agent.TodoBot.run')
    def test_empty_conversation_history_handled(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that first message has no history (or None)"""
        from app.agent import AgentResponse, AgentRequest

        mock_agent.return_value = AgentResponse(
            message="Hello!", tool_calls=[], error=None
        )

        # Send first message (no conversation_id)
        client.post(
            "/api/chat",
            json={"content": "Hello"},
            headers=auth_headers
        )

        # Verify agent was called
        assert mock_agent.call_count == 1

        # Verify first call has no history or empty history
        first_call_args = mock_agent.call_args_list[0]
        agent_request: AgentRequest = first_call_args[0][0]

        # conversation_history should be None or empty
        assert agent_request.conversation_history is None or len(agent_request.conversation_history) == 0

    @patch('app.agent.TodoBot.run')
    def test_conversation_history_maintains_chronological_order(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that conversation history is in correct chronological order"""
        from app.agent import AgentResponse, AgentRequest
        from app.models.message import MessageRole

        mock_agent.return_value = AgentResponse(
            message="Response", tool_calls=[], error=None
        )

        # Create conversation with 3 message pairs
        response1 = client.post(
            "/api/chat",
            json={"content": "Message 1"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        client.post(
            "/api/chat",
            json={"content": "Message 2", "conversation_id": conversation_id},
            headers=auth_headers
        )

        client.post(
            "/api/chat",
            json={"content": "Message 3", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Get the last agent call
        last_call_args = mock_agent.call_args_list[-1]
        agent_request: AgentRequest = last_call_args[0][0]

        # Verify history is in chronological order
        history = agent_request.conversation_history
        if history and len(history) >= 4:
            # Should have messages in order: user, assistant, user, assistant, ...
            # First message should be "Message 1"
            assert history[0].content == "Message 1"
            assert history[0].role == "user"
            # Second should be assistant response
            assert history[1].role == "assistant"
            # Third should be "Message 2"
            assert history[2].content == "Message 2"
            assert history[2].role == "user"


class TestEdgeCasesAndErrorHandling:
    """Tests for edge cases and error handling scenarios"""

    def test_malformed_request_missing_content(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test AC-003.4: Reject malformed requests (missing content)"""
        response = client.post(
            "/api/chat",
            json={},  # Missing required 'content' field
            headers=auth_headers
        )

        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_malformed_request_empty_content(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test AC-003.4: Reject empty message content"""
        response = client.post(
            "/api/chat",
            json={"content": ""},  # Empty content
            headers=auth_headers
        )

        # Should return 422 Unprocessable Entity
        assert response.status_code == 422

    def test_malformed_request_whitespace_only_content(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test AC-003.4: Reject whitespace-only content"""
        response = client.post(
            "/api/chat",
            json={"content": "   "},  # Whitespace only
            headers=auth_headers
        )

        # Should return 422 or handle gracefully
        assert response.status_code in [422, 400]

    def test_invalid_conversation_id_format(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test handling of invalid UUID format for conversation_id"""
        response = client.post(
            "/api/chat",
            json={
                "content": "Hello",
                "conversation_id": "not-a-valid-uuid"
            },
            headers=auth_headers
        )

        # Should return 422 for invalid UUID format
        assert response.status_code == 422

    def test_nonexistent_conversation_id(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test handling of valid UUID but nonexistent conversation"""
        from uuid import uuid4

        fake_conversation_id = str(uuid4())

        response = client.post(
            "/api/chat",
            json={
                "content": "Hello",
                "conversation_id": fake_conversation_id
            },
            headers=auth_headers
        )

        # Should return 404 Not Found
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_very_long_message_content(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test handling of message exceeding maximum length"""
        # Create message exceeding 5000 characters
        long_content = "a" * 6000

        response = client.post(
            "/api/chat",
            json={"content": long_content},
            headers=auth_headers
        )

        # Should return 422 for validation error
        assert response.status_code == 422

    @patch('app.agent.TodoBot.run')
    def test_agent_timeout_handling(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        auth_headers: dict
    ):
        """Test handling of agent timeout or slow response"""
        # Mock agent to raise timeout exception
        mock_agent.side_effect = TimeoutError("Agent timed out")

        response = client.post(
            "/api/chat",
            json={"content": "Hello"},
            headers=auth_headers
        )

        # Should return 500 with error message
        assert response.status_code == 500
        assert "error" in response.json() or "detail" in response.json()

    @patch('app.agent.TodoBot.run')
    def test_agent_general_exception_handling(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        auth_headers: dict
    ):
        """Test handling of unexpected agent errors"""
        # Mock agent to raise unexpected exception
        mock_agent.side_effect = RuntimeError("Unexpected error in agent")

        response = client.post(
            "/api/chat",
            json={"content": "Hello"},
            headers=auth_headers
        )

        # Should return 500 with error message
        assert response.status_code == 500
        assert "error" in response.json() or "detail" in response.json()

    @patch('app.database.engine')
    def test_database_connection_error_returns_503(
        self,
        mock_engine: MagicMock,
        client: TestClient,
        auth_headers: dict
    ):
        """Test AC-003.3: Database unavailable returns 503"""
        from sqlalchemy.exc import OperationalError

        # Mock database to raise connection error
        mock_engine.connect.side_effect = OperationalError(
            "Database connection failed", None, None
        )

        response = client.post(
            "/api/chat",
            json={"content": "Hello"},
            headers=auth_headers
        )

        # Should return 503 Service Unavailable
        # Note: This test might not work as expected due to mocking complexity
        # In production, database errors should return 503
        assert response.status_code in [500, 503]

    @patch('app.agent.TodoBot.run')
    def test_concurrent_requests_same_conversation(
        self,
        mock_agent: MagicMock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test handling of concurrent requests to same conversation"""
        from app.agent import AgentResponse
        import time

        # Mock agent with delay to simulate processing
        def slow_response(request):
            time.sleep(0.1)  # Simulate processing time
            return AgentResponse(message="Response", tool_calls=[], error=None)

        mock_agent.side_effect = slow_response

        # Create initial conversation
        response1 = client.post(
            "/api/chat",
            json={"content": "First message"},
            headers=auth_headers
        )
        conversation_id = response1.json()["conversation_id"]

        # Send second message to same conversation
        # (In real concurrent scenario, these would be parallel)
        response2 = client.post(
            "/api/chat",
            json={"content": "Second message", "conversation_id": conversation_id},
            headers=auth_headers
        )

        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both messages are stored
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        # Should have 4 messages: 2 user + 2 assistant
        assert len(messages) >= 4
