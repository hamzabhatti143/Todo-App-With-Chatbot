"""
Test suite for validating model relationships.

Validates:
- FR-004: One-to-many relationship between Conversation and Message
- Relationship queries and bidirectional navigation
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel, select
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


class TestConversationMessageRelationship:
    """Test Conversation → Message one-to-many relationship (FR-004)."""

    def test_conversation_can_have_multiple_messages(self, session: Session):
        """Verify one conversation can have multiple messages."""
        # Create user and conversation
        user = User(email="test1@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Add multiple messages to conversation
        message1 = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="First message"
        )
        message2 = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="Second message"
        )
        message3 = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Third message"
        )

        session.add_all([message1, message2, message3])
        session.commit()

        # Query messages via relationship
        session.refresh(conversation)
        messages = conversation.messages

        assert len(messages) == 3, "Conversation should have 3 messages"
        assert messages[0].content == "First message"
        assert messages[1].content == "Second message"
        assert messages[2].content == "Third message"

    def test_message_belongs_to_conversation(self, session: Session):
        """Verify each message belongs to exactly one conversation."""
        user = User(email="test2@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Test message"
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        # Navigate from message back to conversation
        assert message.conversation.id == conversation.id, \
            "Message should reference its parent conversation"
        assert message.conversation.user_id == user.id, \
            "Should be able to navigate message → conversation → user"

    def test_query_messages_by_conversation(self, session: Session):
        """Verify can query all messages for a specific conversation."""
        user = User(email="test3@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        # Create two conversations
        conv1 = Conversation(user_id=user.id)
        conv2 = Conversation(user_id=user.id)
        session.add_all([conv1, conv2])
        session.commit()

        # Add messages to each conversation
        msg1_conv1 = Message(conversation_id=conv1.id, role=MessageRole.USER, content="Conv1 Msg1")
        msg2_conv1 = Message(conversation_id=conv1.id, role=MessageRole.ASSISTANT, content="Conv1 Msg2")
        msg1_conv2 = Message(conversation_id=conv2.id, role=MessageRole.USER, content="Conv2 Msg1")

        session.add_all([msg1_conv1, msg2_conv1, msg1_conv2])
        session.commit()

        # Query messages for conversation 1
        statement = select(Message).where(Message.conversation_id == conv1.id)
        conv1_messages = session.exec(statement).all()

        assert len(conv1_messages) == 2, "Conversation 1 should have 2 messages"
        assert all(msg.conversation_id == conv1.id for msg in conv1_messages), \
            "All messages should belong to conversation 1"

        # Query messages for conversation 2
        statement = select(Message).where(Message.conversation_id == conv2.id)
        conv2_messages = session.exec(statement).all()

        assert len(conv2_messages) == 1, "Conversation 2 should have 1 message"
        assert conv2_messages[0].conversation_id == conv2.id

    def test_conversation_messages_ordered_by_creation(self, session: Session):
        """Verify messages can be retrieved in chronological order."""
        user = User(email="test4@example.com", hashed_password="hashed")
        session.add(user)
        session.commit()

        conversation = Conversation(user_id=user.id)
        session.add(conversation)
        session.commit()

        # Add messages in specific order
        for i in range(5):
            message = Message(
                conversation_id=conversation.id,
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}"
            )
            session.add(message)
            session.commit()

        # Query messages ordered by created_at
        statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at)

        messages = session.exec(statement).all()

        assert len(messages) == 5
        # Verify order by checking content
        for i, message in enumerate(messages):
            assert message.content == f"Message {i}", \
                f"Messages should be in chronological order"


class TestForeignKeyConstraints:
    """Test foreign key constraints are defined (FR-005, FR-014)."""

    def test_message_has_conversation_foreign_key(self):
        """Verify Message.conversation_id has foreign key to conversations table."""
        # Check SQLAlchemy table column has foreign key
        table = Message.__table__
        conversation_id_column = table.columns['conversation_id']
        foreign_keys = list(conversation_id_column.foreign_keys)
        assert len(foreign_keys) > 0, \
            "Message.conversation_id should have a foreign key"
        assert str(foreign_keys[0].column) == "conversations.id", \
            "Message.conversation_id should reference conversations.id"

    def test_conversation_has_user_foreign_key(self):
        """Verify Conversation.user_id has foreign key to users table."""
        table = Conversation.__table__
        user_id_column = table.columns['user_id']
        foreign_keys = list(user_id_column.foreign_keys)
        assert len(foreign_keys) > 0, \
            "Conversation.user_id should have a foreign key"
        assert str(foreign_keys[0].column) == "users.id", \
            "Conversation.user_id should reference users.id"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
