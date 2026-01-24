"""Conversation model for chat history."""

from datetime import datetime
from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between user and AI agent.

    Attributes:
        id: Unique identifier for the conversation
        user_id: Foreign key to the user who owns this conversation
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
    """

    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
