"""
Task Routes

Handles CRUD operations for tasks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List
from datetime import datetime

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Get all tasks for a user.

    Args:
        user_id: The user ID to get tasks for
        session: Database session
        current_user_id: The authenticated user's ID

    Returns:
        List[TaskResponse]: List of tasks

    Raises:
        HTTPException: If user is not authorized
    """
    # Verify user is accessing their own tasks
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Create a new task.

    Args:
        user_id: The user ID to create task for
        task_data: Task creation data
        session: Database session
        current_user_id: The authenticated user's ID

    Returns:
        TaskResponse: The created task

    Raises:
        HTTPException: If user is not authorized
    """
    # Verify user is creating their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    db_task = Task(**task_data.model_dump(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Get a specific task.

    Args:
        user_id: The user ID
        task_id: The task ID
        session: Database session
        current_user_id: The authenticated user's ID

    Returns:
        TaskResponse: The task

    Raises:
        HTTPException: If task not found or user not authorized
    """
    # Verify user is accessing their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Update a task.

    Args:
        user_id: The user ID
        task_id: The task ID
        task_data: Task update data
        session: Database session
        current_user_id: The authenticated user's ID

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: If task not found or user not authorized
    """
    # Verify user is updating their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    task_update_data = task_data.model_dump(exclude_unset=True)
    for key, value in task_update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Delete a task.

    Args:
        user_id: The user ID
        task_id: The task ID
        session: Database session
        current_user_id: The authenticated user's ID

    Raises:
        HTTPException: If task not found or user not authorized
    """
    # Verify user is deleting their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Toggle task completion status.

    Args:
        user_id: The user ID
        task_id: The task ID
        session: Database session
        current_user_id: The authenticated user's ID

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: If task not found or user not authorized
    """
    # Verify user is updating their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
