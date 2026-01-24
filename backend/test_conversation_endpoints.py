"""
Tests for conversation endpoints

These tests verify:
- GET /api/conversations endpoint (list conversations)
- GET /api/conversations/{conversation_id} endpoint (get specific conversation)
- GET /api/conversations/{conversation_id}/messages endpoint (get messages)
- JWT authentication and user isolation
- Pagination
- Ordering and filtering
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from datetime import datetime, timedelta
from uuid import uuid4

from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.auth import create_access_token, get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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
    """Create another test user"""
    user = User(
        email="other@example.com",
        hashed_password=get_password_hash("otherpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_conversation")
def test_conversation_fixture(session: Session, test_user: User):
    """Create a test conversation with messages"""
    conversation = Conversation(user_id=test_user.id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Add messages
    messages = [
        Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Hello"
        ),
        Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="Hi! How can I help?"
        ),
        Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Create a task"
        ),
        Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="I've created the task for you!"
        ),
    ]
    for msg in messages:
        session.add(msg)
    session.commit()

    return conversation


class TestListConversations:
    """Tests for GET /api/conversations endpoint"""

    def test_list_conversations_success(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test listing user's conversations"""
        # Create multiple conversations
        for i in range(3):
            conv = Conversation(user_id=test_user.id)
            session.add(conv)
        session.commit()

        response = client.get("/api/conversations", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 3
        for conv in data:
            assert "id" in conv
            assert "user_id" in conv
            assert conv["user_id"] == str(test_user.id)
            assert "created_at" in conv
            assert "updated_at" in conv

    def test_list_conversations_ordered_by_updated_at(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test that conversations are ordered by updated_at DESC"""
        # Create conversations with different timestamps
        old_conv = Conversation(
            user_id=test_user.id,
            updated_at=datetime.utcnow() - timedelta(days=2)
        )
        recent_conv = Conversation(
            user_id=test_user.id,
            updated_at=datetime.utcnow()
        )
        session.add_all([old_conv, recent_conv])
        session.commit()

        response = client.get("/api/conversations", headers=auth_headers)
        data = response.json()

        # Most recent should be first
        assert len(data) >= 2
        assert data[0]["id"] == str(recent_conv.id)

    def test_list_conversations_user_isolation(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        other_user: User,
        auth_headers: dict
    ):
        """Test that users only see their own conversations"""
        # Create conversations for both users
        test_conv = Conversation(user_id=test_user.id)
        other_conv = Conversation(user_id=other_user.id)
        session.add_all([test_conv, other_conv])
        session.commit()

        response = client.get("/api/conversations", headers=auth_headers)
        data = response.json()

        # Should only see test_user's conversation
        assert len(data) == 1
        assert data[0]["id"] == str(test_conv.id)

    def test_list_conversations_pagination(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test pagination with limit and offset"""
        # Create 10 conversations
        for i in range(10):
            conv = Conversation(user_id=test_user.id)
            session.add(conv)
        session.commit()

        # Test limit
        response = client.get(
            "/api/conversations?limit=5",
            headers=auth_headers
        )
        assert len(response.json()) == 5

        # Test offset
        response = client.get(
            "/api/conversations?offset=5&limit=5",
            headers=auth_headers
        )
        assert len(response.json()) == 5

    def test_list_conversations_requires_authentication(self, client: TestClient):
        """Test that endpoint requires authentication"""
        response = client.get("/api/conversations")
        assert response.status_code == 401

    def test_list_conversations_empty(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test listing conversations when user has none"""
        response = client.get("/api/conversations", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == []


class TestGetConversation:
    """Tests for GET /api/conversations/{conversation_id} endpoint"""

    def test_get_conversation_success(
        self,
        client: TestClient,
        test_conversation: Conversation,
        auth_headers: dict
    ):
        """Test getting a specific conversation"""
        response = client.get(
            f"/api/conversations/{test_conversation.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == str(test_conversation.id)
        assert "user_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_conversation_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting non-existent conversation"""
        fake_id = uuid4()
        response = client.get(
            f"/api/conversations/{fake_id}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_conversation_user_isolation(
        self,
        client: TestClient,
        session: Session,
        other_user: User,
        auth_headers: dict
    ):
        """Test that users cannot access other users' conversations"""
        # Create conversation for other user
        other_conv = Conversation(user_id=other_user.id)
        session.add(other_conv)
        session.commit()

        response = client.get(
            f"/api/conversations/{other_conv.id}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_conversation_requires_authentication(
        self,
        client: TestClient,
        test_conversation: Conversation
    ):
        """Test that endpoint requires authentication"""
        response = client.get(f"/api/conversations/{test_conversation.id}")
        assert response.status_code == 401


class TestGetConversationMessages:
    """Tests for GET /api/conversations/{conversation_id}/messages endpoint"""

    def test_get_messages_success(
        self,
        client: TestClient,
        test_conversation: Conversation,
        auth_headers: dict
    ):
        """Test getting messages from a conversation"""
        response = client.get(
            f"/api/conversations/{test_conversation.id}/messages",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 4  # From fixture
        for msg in data:
            assert "id" in msg
            assert "conversation_id" in msg
            assert msg["conversation_id"] == str(test_conversation.id)
            assert "role" in msg
            assert "content" in msg
            assert "created_at" in msg

    def test_get_messages_ordered_chronologically(
        self,
        client: TestClient,
        test_conversation: Conversation,
        auth_headers: dict
    ):
        """Test that messages are ordered by created_at ASC"""
        response = client.get(
            f"/api/conversations/{test_conversation.id}/messages",
            headers=auth_headers
        )
        data = response.json()

        # First message should be USER saying "Hello"
        assert data[0]["role"] == "USER"
        assert data[0]["content"] == "Hello"

        # Second should be ASSISTANT
        assert data[1]["role"] == "ASSISTANT"

    def test_get_messages_user_isolation(
        self,
        client: TestClient,
        session: Session,
        other_user: User,
        auth_headers: dict
    ):
        """Test that users cannot access other users' conversation messages"""
        # Create conversation and message for other user
        other_conv = Conversation(user_id=other_user.id)
        session.add(other_conv)
        session.commit()
        session.refresh(other_conv)

        msg = Message(
            conversation_id=other_conv.id,
            role=MessageRole.USER,
            content="Secret message"
        )
        session.add(msg)
        session.commit()

        response = client.get(
            f"/api/conversations/{other_conv.id}/messages",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_messages_empty_conversation(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test getting messages from empty conversation"""
        # Create conversation without messages
        empty_conv = Conversation(user_id=test_user.id)
        session.add(empty_conv)
        session.commit()
        session.refresh(empty_conv)

        response = client.get(
            f"/api/conversations/{empty_conv.id}/messages",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_get_messages_requires_authentication(
        self,
        client: TestClient,
        test_conversation: Conversation
    ):
        """Test that endpoint requires authentication"""
        response = client.get(
            f"/api/conversations/{test_conversation.id}/messages"
        )
        assert response.status_code == 401
