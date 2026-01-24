"""Message model for conversation history."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum as SQLAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class MessageRole(str, Enum):
    """Enumeration of message roles in a conversation."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Message model representing a single message in a conversation.

    Attributes:
        id: Unique identifier for the message
        conversation_id: Foreign key to the conversation this message belongs to
        role: Role of the message sender (user or assistant)
        content: Text content of the message (max 5000 characters)
        created_at: Timestamp when message was created
    """

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(SQLAEnum(MessageRole)))
    content: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
