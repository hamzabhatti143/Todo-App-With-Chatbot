"""
Task Pydantic Schemas
"""

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: UUID
    completed: bool
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
