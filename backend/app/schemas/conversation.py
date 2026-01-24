"""Pydantic schemas for conversation API."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class ConversationResponse(BaseModel):
    """Schema for conversation responses."""

    id: UUID = Field(
        ...,
        description="Unique conversation identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    user_id: UUID = Field(
        ...,
        description="ID of the user who owns this conversation",
        examples=["770e8400-e29b-41d4-a716-446655440002"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when conversation was created",
        examples=["2026-01-16T10:00:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when conversation was last updated",
        examples=["2026-01-16T10:30:00Z"],
    )
    message_count: Optional[int] = Field(
        None,
        description="Number of messages in the conversation",
        examples=[12],
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "user_id": "770e8400-e29b-41d4-a716-446655440002",
                    "created_at": "2026-01-16T10:00:00Z",
                    "updated_at": "2026-01-16T10:30:00Z",
                    "message_count": 12,
                }
            ]
        }
