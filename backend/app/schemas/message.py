"""Pydantic schemas for message API."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from app.models.message import MessageRole


class MessageResponse(BaseModel):
    """Schema for message responses."""

    id: UUID = Field(
        ...,
        description="Unique message identifier",
        examples=["660e8400-e29b-41d4-a716-446655440001"],
    )
    conversation_id: UUID = Field(
        ...,
        description="ID of the conversation this message belongs to",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    role: MessageRole = Field(
        ...,
        description="Role of the message sender (user or assistant)",
        examples=["user"],
    )
    content: str = Field(
        ...,
        description="Message content",
        examples=["Show me all my incomplete tasks"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when message was created",
        examples=["2026-01-16T10:25:00Z"],
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                    "role": "user",
                    "content": "Add a task to buy groceries",
                    "created_at": "2026-01-16T10:25:00Z",
                },
                {
                    "id": "661e8400-e29b-41d4-a716-446655440002",
                    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                    "role": "assistant",
                    "content": "I've created a task titled 'Buy groceries'. Would you like to add any specific items?",
                    "created_at": "2026-01-16T10:25:30Z",
                },
            ]
        }
