"""
MCP Tools for Task Management

This module implements 5 MCP tools for managing tasks:
- add_task: Create new task
- list_tasks: Retrieve tasks with optional filtering
- complete_task: Mark task as completed
- delete_task: Remove task permanently
- update_task: Modify task title and/or description

All tools are stateless and persist state to PostgreSQL database.
"""

from typing import Optional
from datetime import datetime
from uuid import UUID

from mcp.server.fastmcp import FastMCP
import mcp.types as types
from sqlmodel import Session, select

from app.database import engine
from app.models.task import Task


# Initialize FastMCP server
mcp = FastMCP("Todo Task Server")


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> str:
    """
    Create a new task for the user.

    Args:
        user_id: UUID of the user creating the task
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Success message with task ID and title
    """
    # Validate inputs
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    if description and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user_id format")

    # Create database session and insert task
    with Session(engine) as session:
        try:
            task = Task(
                user_id=user_uuid,
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(task)
            session.commit()
            session.refresh(task)

            return f"Task created: {task.title} (ID: {task.id})"

        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to create task: {str(e)}")


@mcp.tool()
async def list_tasks(
    user_id: str,
    status: str = "all"
) -> str:
    """
    List user's tasks with optional status filter.

    Args:
        user_id: UUID of the user whose tasks to retrieve
        status: Filter by status - "all", "pending", or "completed" (default: "all")

    Returns:
        Formatted list of tasks with completion status
    """
    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user_id format")

    # Validate status filter
    if status not in ["all", "pending", "completed"]:
        raise ValueError("Status must be 'all', 'pending', or 'completed'")

    # Query database
    with Session(engine) as session:
        try:
            # Build query
            statement = select(Task).where(Task.user_id == user_uuid)

            # Apply status filter
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

            # Order by newest first
            statement = statement.order_by(Task.created_at.desc())

            # Execute query
            tasks = session.exec(statement).all()

            # Format response
            if not tasks:
                return "No tasks found"

            task_list = "\n".join([
                f"{'✓' if task.completed else '◯'} {task.title} (ID: {task.id})"
                for task in tasks
            ])

            return f"Your tasks:\n{task_list}"

        except Exception as e:
            raise ValueError(f"Failed to list tasks: {str(e)}")


@mcp.tool()
async def complete_task(
    user_id: str,
    task_id: str
) -> str:
    """
    Mark a task as completed.

    Args:
        user_id: UUID of the user performing the operation
        task_id: UUID of the task to complete

    Returns:
        Success message with completed task title
    """
    # Validate UUID formats
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise ValueError("Invalid UUID format")

    # Update task
    with Session(engine) as session:
        try:
            # Fetch task
            task = session.get(Task, task_uuid)

            # Verify exists
            if not task:
                raise ValueError("Task not found")

            # Verify ownership
            if task.user_id != user_uuid:
                raise ValueError("Permission denied - you can only modify your own tasks")

            # Update completion status
            task.completed = True
            task.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(task)

            return f"Completed: {task.title}"

        except ValueError:
            raise
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to complete task: {str(e)}")


@mcp.tool()
async def delete_task(
    user_id: str,
    task_id: str
) -> str:
    """
    Delete a task permanently.

    Args:
        user_id: UUID of the user performing the operation
        task_id: UUID of the task to delete

    Returns:
        Success message with deleted task title
    """
    # Validate UUID formats
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise ValueError("Invalid UUID format")

    # Delete task
    with Session(engine) as session:
        try:
            # Fetch task
            task = session.get(Task, task_uuid)

            # Verify exists
            if not task:
                raise ValueError("Task not found")

            # Verify ownership
            if task.user_id != user_uuid:
                raise ValueError("Permission denied - you can only modify your own tasks")

            # Store title for response
            task_title = task.title

            # Delete
            session.delete(task)
            session.commit()

            return f"Deleted: {task_title}"

        except ValueError:
            raise
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to delete task: {str(e)}")


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """
    Update task title and/or description.

    Args:
        user_id: UUID of the user updating the task
        task_id: UUID of the task to update
        title: New task title (1-200 characters, optional)
        description: New task description (max 1000 characters, optional)

    Returns:
        Success message with updated task title
    """
    # Validate at least one field provided
    if title is None and description is None:
        raise ValueError("At least one of title or description must be provided")

    # Validate field lengths
    if title is not None:
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

    if description is not None and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")

    # Validate UUID formats
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise ValueError("Invalid UUID format")

    # Update task
    with Session(engine) as session:
        try:
            # Fetch task
            task = session.get(Task, task_uuid)

            # Verify exists
            if not task:
                raise ValueError("Task not found")

            # Verify ownership
            if task.user_id != user_uuid:
                raise ValueError("Permission denied - you can only modify your own tasks")

            # Update fields (partial update)
            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description.strip() else None

            # Update timestamp
            task.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(task)

            return f"Updated task: {task.title}"

        except ValueError:
            raise
        except Exception as e:
            session.rollback()
            raise ValueError(f"Failed to update task: {str(e)}")
