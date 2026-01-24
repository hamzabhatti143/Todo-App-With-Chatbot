"""
Test suite for validating database models against specification requirements.

Validates:
- FR-001: Task model fields, types, and constraints
- FR-002: Conversation model fields and structure
- FR-003: Message model fields and immutability design
- SC-007: Timestamp auto-population
"""

import pytest
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestTaskModel:
    """Test Task model validation (FR-001)."""

    def test_task_has_required_fields(self, session: Session):
        """Verify Task model has all required fields per FR-001."""
        # Create test user
        user = User(email="test@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create task with all required fields
        task = Task(
            user_id=user.id,
            title="Test Task",
            description="Test Description",
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        # Verify all required fields exist
        assert isinstance(task.id, UUID), "id should be UUID"
        assert isinstance(task.user_id, UUID), "user_id should be UUID"
        assert isinstance(task.title, str), "title should be string"
        assert isinstance(task.description, str) or task.description is None, "description should be optional string"
        assert isinstance(task.completed, bool), "completed should be boolean"
        assert isinstance(task.created_at, datetime), "created_at should be datetime"
        assert isinstance(task.updated_at, datetime), "updated_at should be datetime"

    def test_task_title_max_length(self, session: Session):
        """Verify Task.title has max length of 200 chars (FR-001)."""
        user = User(email="test2@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        # Title at exactly 200 characters should work
        title_200 = "A" * 200
        task = Task(user_id=user.id, title=title_200)
        session.add(task)
        session.commit()

        assert len(task.title) == 200, "Should accept 200 character title"

    def test_task_description_max_length(self, session: Session):
        """Verify Task.description has max length of 1000 chars (FR-001)."""
        user = User(email="test3@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        # Description at exactly 1000 characters should work
        desc_1000 = "B" * 1000
        task = Task(user_id=user.id, title="Test", description=desc_1000)
        session.add(task)
        session.commit()

        assert len(task.description) == 1000, "Should accept 1000 character description"

    def test_task_completed_defaults_to_false(self, session: Session):
        """Verify Task.completed defaults to False (FR-001)."""
        user = User(email="test4@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        task = Task(user_id=user.id, title="Test Task")
        session.add(task)
        session.commit()

        assert task.completed is False, "completed should default to False"

    def test_task_timestamps_auto_generated(self, session: Session):
        """Verify Task timestamps are auto-generated (SC-007)."""
        user = User(email="test5@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        before_creation = datetime.utcnow()
        task = Task(user_id=user.id, title="Test Task")
        session.add(task)
        session.commit()
        session.refresh(task)
        after_creation = datetime.utcnow()

        assert task.created_at is not None, "created_at should be auto-generated"
        assert task.updated_at is not None, "updated_at should be auto-generated"
        assert before_creation <= task.created_at <= after_creation, "created_at should be current time"
        assert before_creation <= task.updated_at <= after_creation, "updated_at should be current time"


class TestConversationModel:
    """Test Conversation model validation (FR-002)."""

    def test_conversation_has_required_fields(self, session: Session):
        """Verify Conversation model has all required fields per FR-002."""
        user = User(email="test6@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        assert isinstance(conversation.id, UUID), "id should be UUID"
        assert isinstance(conversation.user_id, UUID), "user_id should be UUID"
        assert isinstance(conversation.created_at, datetime), "created_at should be datetime"
        assert isinstance(conversation.updated_at, datetime), "updated_at should be datetime"

    def test_conversation_timestamps_auto_generated(self, session: Session):
        """Verify Conversation timestamps are auto-generated (SC-007)."""
        user = User(email="test7@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        before_creation = datetime.utcnow()
        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        after_creation = datetime.utcnow()

        assert conversation.created_at is not None, "created_at should be auto-generated"
        assert conversation.updated_at is not None, "updated_at should be auto-generated"
        assert before_creation <= conversation.created_at <= after_creation
        assert before_creation <= conversation.updated_at <= after_creation


class TestMessageModel:
    """Test Message model validation (FR-003)."""

    def test_message_has_required_fields(self, session: Session):
        """Verify Message model has all required fields per FR-003."""
        user = User(email="test8@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Test message content"
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        assert isinstance(message.id, UUID), "id should be UUID"
        assert isinstance(message.conversation_id, UUID), "conversation_id should be UUID"
        assert isinstance(message.role, MessageRole), "role should be MessageRole enum"
        assert isinstance(message.content, str), "content should be string"
        assert isinstance(message.created_at, datetime), "created_at should be datetime"

    def test_message_no_updated_at_field(self, session: Session):
        """Verify Message model has NO updated_at field (immutability design per FR-003)."""
        user = User(email="test9@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="Assistant response"
        )
        session.add(message)
        session.commit()

        # Verify updated_at does NOT exist (messages are immutable)
        assert not hasattr(message, 'updated_at'), "Message should NOT have updated_at (immutable design)"

    def test_message_role_enum_values(self, session: Session):
        """Verify MessageRole enum has correct values (FR-003)."""
        assert MessageRole.USER.value == "user", "USER role should be 'user'"
        assert MessageRole.ASSISTANT.value == "assistant", "ASSISTANT role should be 'assistant'"

        # Verify only two roles exist
        assert len(MessageRole) == 2, "Should have exactly 2 message roles"

    def test_message_content_max_length(self, session: Session):
        """Verify Message.content has max length of 5000 chars (FR-003)."""
        user = User(email="test10@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        # Content at exactly 5000 characters should work
        content_5000 = "X" * 5000
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=content_5000
        )
        session.add(message)
        session.commit()

        assert len(message.content) == 5000, "Should accept 5000 character content"

    def test_message_created_at_auto_generated(self, session: Session):
        """Verify Message.created_at is auto-generated (SC-007)."""
        user = User(email="test11@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        before_creation = datetime.utcnow()
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Test"
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        after_creation = datetime.utcnow()

        assert message.created_at is not None, "created_at should be auto-generated"
        assert before_creation <= message.created_at <= after_creation


class TestModelIndexes:
    """Test that required indexes are defined in models (FR-006, FR-007)."""

    def test_task_user_id_indexed(self):
        """Verify Task.user_id has index defined (FR-006)."""
        # Check SQLAlchemy table column has index
        table = Task.__table__
        user_id_column = table.columns['user_id']
        assert user_id_column.index is True, \
            "Task.user_id should be indexed"

    def test_task_title_indexed(self):
        """Verify Task.title has index defined (FR-006)."""
        table = Task.__table__
        title_column = table.columns['title']
        assert title_column.index is True, \
            "Task.title should be indexed"

    def test_conversation_user_id_indexed(self):
        """Verify Conversation.user_id has index defined (FR-006)."""
        table = Conversation.__table__
        user_id_column = table.columns['user_id']
        assert user_id_column.index is True, \
            "Conversation.user_id should be indexed"

    def test_message_conversation_id_indexed(self):
        """Verify Message.conversation_id has index defined (FR-007)."""
        table = Message.__table__
        conversation_id_column = table.columns['conversation_id']
        assert conversation_id_column.index is True, \
            "Message.conversation_id should be indexed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
