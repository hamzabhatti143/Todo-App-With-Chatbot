"""
Test suite for validating cascade deletion behavior.

Validates:
- FR-005: Cascade deletion when conversation is deleted
- SC-008: 100% success rate for cascade deletion
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel, select, func
from sqlmodel.pool import StaticPool

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


class TestCascadeDeletion:
    """Test cascade deletion behavior (FR-005, SC-008)."""

    def test_deleting_conversation_deletes_all_messages(self, session: Session):
        """Verify deleting conversation removes all associated messages (SC-008: 100% success)."""
        # Setup: Create user, conversation, and messages
        user = User(email="test1@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        conversation_id = conversation.id

        # Add 10 messages to the conversation
        messages = []
        for i in range(10):
            message = Message(
                conversation_id=conversation_id,
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}"
            )
            messages.append(message)

        session.add_all(messages)
        session.commit()

        # Verify messages exist
        count_before = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)
        ).one()
        assert count_before == 10, "Should have 10 messages before deletion"

        # Delete the conversation
        session.delete(conversation)
        session.commit()

        # Verify all messages are deleted (SC-008: 100% success rate)
        count_after = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)
        ).one()
        assert count_after == 0, "All messages should be deleted with conversation (SC-008)"

    def test_cascade_delete_with_multiple_conversations(self, session: Session):
        """Verify cascade delete only affects messages from deleted conversation."""
        user = User(email="test2@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        # Create two conversations
        conv1 = Conversation(user_id=user.id)
        conv2 = Conversation(user_id=user.id)
        session.add_all([conv1, conv2])
        session.commit()

        conv1_id = conv1.id
        conv2_id = conv2.id

        # Add messages to both conversations
        for i in range(5):
            msg1 = Message(conversation_id=conv1_id, role=MessageRole.USER, content=f"Conv1 {i}")
            msg2 = Message(conversation_id=conv2_id, role=MessageRole.USER, content=f"Conv2 {i}")
            session.add_all([msg1, msg2])
        session.commit()

        # Verify initial state
        conv1_count_before = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conv1_id)
        ).one()
        conv2_count_before = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conv2_id)
        ).one()

        assert conv1_count_before == 5
        assert conv2_count_before == 5

        # Delete only conversation 1
        session.delete(conv1)
        session.commit()

        # Verify only conv1 messages are deleted
        conv1_count_after = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conv1_id)
        ).one()
        conv2_count_after = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conv2_id)
        ).one()

        assert conv1_count_after == 0, "Conversation 1 messages should be deleted"
        assert conv2_count_after == 5, "Conversation 2 messages should remain intact"

    def test_cascade_delete_empty_conversation(self, session: Session):
        """Verify deleting conversation with no messages works correctly."""
        user = User(email="test3@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        # Create conversation with no messages
        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        conversation_id = conversation.id

        # Delete conversation
        session.delete(conversation)
        session.commit()

        # Verify conversation is deleted
        deleted_conv = session.get(Conversation, conversation_id)
        assert deleted_conv is None, "Conversation should be deleted"

    def test_cascade_delete_large_conversation(self, session: Session):
        """Verify cascade delete works with large number of messages (100+)."""
        user = User(email="test4@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        conversation_id = conversation.id

        # Add 100 messages
        messages = []
        for i in range(100):
            message = Message(
                conversation_id=conversation_id,
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}"
            )
            messages.append(message)

        session.add_all(messages)
        session.commit()

        # Verify 100 messages exist
        count_before = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)
        ).one()
        assert count_before == 100

        # Delete conversation
        session.delete(conversation)
        session.commit()

        # Verify all 100 messages deleted (SC-008: 100% success)
        count_after = session.exec(
            select(func.count()).select_from(Message).where(Message.conversation_id == conversation_id)
        ).one()
        assert count_after == 0, "All 100 messages should be cascade deleted"

    def test_cascade_delete_relationship_configured(self):
        """Verify cascade delete is configured in model relationship."""
        # Check that Conversation.messages relationship has cascade configured
        # This validates FR-005 at the model definition level
        conversation_relationships = Conversation.__sqlmodel_relationships__

        messages_relationship = conversation_relationships.get('messages')
        assert messages_relationship is not None, "messages relationship should exist"

        # Check cascade configuration in sa_relationship_kwargs
        cascade_config = messages_relationship.sa_relationship_kwargs.get('cascade')
        assert cascade_config == "all, delete-orphan", \
            "Cascade should be configured as 'all, delete-orphan' per FR-005"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
