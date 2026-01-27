"""Pydantic schemas for chat and conversation API."""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any


class ChatMessageRequest(BaseModel):
    """Schema for incoming chat message requests."""

    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message content",
        examples=["Add a task to buy groceries tomorrow"],
    )
    conversation_id: Optional[UUID] = Field(
        None,
        description="Optional conversation ID to continue existing conversation. If null, creates new conversation.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "content": "Add a task to buy groceries tomorrow",
                    "conversation_id": None,
                },
                {
                    "content": "Mark that task as complete",
                    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                },
            ]
        }


class TaskData(BaseModel):
    """Schema for task data in chat response."""

    id: UUID
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    """Schema for chat message responses."""

    conversation_id: UUID = Field(
        ...,
        description="Conversation ID (new or existing)",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    message_id: UUID = Field(
        ...,
        description="ID of the assistant's response message",
        examples=["660e8400-e29b-41d4-a716-446655440001"],
    )
    role: str = Field(
        "assistant",
        description="Role of the message sender (always 'assistant' for responses)",
        examples=["assistant"],
    )
    content: str = Field(
        ...,
        description="AI agent's response message",
        examples=[
            "I've created a task titled 'Buy groceries' for tomorrow. Would you like me to add any specific items to the description?"
        ],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when message was created",
        examples=["2026-01-16T10:30:00Z"],
    )
    task_data: Optional[Dict[str, List[TaskData]]] = Field(
        None,
        description="Optional task data if the agent created/modified tasks",
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                    "message_id": "660e8400-e29b-41d4-a716-446655440001",
                    "role": "assistant",
                    "content": "I've created a task titled 'Buy groceries'. Would you like to add any specific items?",
                    "created_at": "2026-01-16T10:30:00Z",
                    "task_data": {
                        "tasks": [
                            {
                                "id": "880e8400-e29b-41d4-a716-446655440003",
                                "title": "Buy groceries",
                                "description": None,
                                "completed": False,
                                "user_id": "770e8400-e29b-41d4-a716-446655440002",
                                "created_at": "2026-01-16T10:30:00Z",
                                "updated_at": "2026-01-16T10:30:00Z",
                            }
                        ]
                    },
                }
            ]
        }


class MessageResponse(BaseModel):
    """Schema for message in conversation history."""

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Schema for conversation list item."""

    id: UUID
    user_id: UUID
    title: str = Field(
        ...,
        description="Title of the conversation (from first user message)",
    )
    last_message: str = Field(
        ...,
        description="Preview of the last message",
    )
    created_at: datetime
    updated_at: datetime
    message_count: int = Field(
        ...,
        description="Number of messages in this conversation",
    )

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    """Schema for detailed conversation with messages."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
