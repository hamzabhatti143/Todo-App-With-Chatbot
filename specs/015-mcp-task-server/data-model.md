# Data Model: MCP Task Server

**Feature**: 015-mcp-task-server
**Date**: 2026-01-17
**Status**: Design

## Overview

This document defines the data models for the MCP Task Server, including tool input/output schemas, database entities, and response formats. All models use Pydantic for validation and type safety.

## Tool Input Models

### AddTaskInput

Parameters for creating a new task.

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID

class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""

    user_id: str = Field(
        ...,
        description="UUID of the user creating the task",
        min_length=36,
        max_length=36
    )
    title: str = Field(
        ...,
        description="Task title (1-200 characters)",
        min_length=1,
        max_length=200
    )
    description: Optional[str] = Field(
        None,
        description="Optional task description (max 1000 characters)",
        max_length=1000
    )

    @validator('user_id')
    def validate_uuid_format(cls, v):
        """Ensure user_id is valid UUID format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError("Invalid UUID format for user_id")
```

**Validation Rules**:
- `user_id`: Required, valid UUID string (36 chars)
- `title`: Required, 1-200 characters, non-empty after strip
- `description`: Optional, max 1000 characters

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Finish quarterly report",
  "description": "Complete Q4 financial analysis"
}
```

### ListTasksInput

Parameters for listing user's tasks with optional filtering.

```python
from enum import Enum

class TaskStatusFilter(str, Enum):
    """Status filter options for list_tasks."""
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"

class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""

    user_id: str = Field(
        ...,
        description="UUID of the user whose tasks to retrieve",
        min_length=36,
        max_length=36
    )
    status: TaskStatusFilter = Field(
        TaskStatusFilter.ALL,
        description="Filter tasks by completion status"
    )

    @validator('user_id')
    def validate_uuid_format(cls, v):
        """Ensure user_id is valid UUID format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError("Invalid UUID format for user_id")
```

**Validation Rules**:
- `user_id`: Required, valid UUID string
- `status`: Optional, must be "all", "pending", or "completed" (default: "all")

**Examples**:
```json
// List all tasks
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "all"
}

// List only pending tasks
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

### TaskOperationInput

Parameters for complete_task and delete_task tools.

```python
class TaskOperationInput(BaseModel):
    """Input schema for task operations (complete, delete)."""

    user_id: str = Field(
        ...,
        description="UUID of the user performing the operation",
        min_length=36,
        max_length=36
    )
    task_id: str = Field(
        ...,
        description="UUID of the task to operate on",
        min_length=36,
        max_length=36
    )

    @validator('user_id', 'task_id')
    def validate_uuid_format(cls, v):
        """Ensure UUIDs are valid format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")
```

**Validation Rules**:
- `user_id`: Required, valid UUID string
- `task_id`: Required, valid UUID string
- Both UUIDs validated before database access

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

### UpdateTaskInput

Parameters for updating task title and/or description.

```python
class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""

    user_id: str = Field(
        ...,
        description="UUID of the user updating the task",
        min_length=36,
        max_length=36
    )
    task_id: str = Field(
        ...,
        description="UUID of the task to update",
        min_length=36,
        max_length=36
    )
    title: Optional[str] = Field(
        None,
        description="New task title (1-200 characters)",
        min_length=1,
        max_length=200
    )
    description: Optional[str] = Field(
        None,
        description="New task description (max 1000 characters)",
        max_length=1000
    )

    @validator('user_id', 'task_id')
    def validate_uuid_format(cls, v):
        """Ensure UUIDs are valid format."""
        try:
            UUID(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid UUID format: {v}")

    @validator('title', 'description')
    def at_least_one_field(cls, v, values):
        """Ensure at least one field is being updated."""
        if 'title' in values and 'description' in values:
            if not values.get('title') and not v:
                raise ValueError("At least one of title or description must be provided")
        return v
```

**Validation Rules**:
- `user_id`: Required, valid UUID string
- `task_id`: Required, valid UUID string
- `title`: Optional, 1-200 characters if provided
- `description`: Optional, max 1000 characters if provided
- **At least one of title or description must be provided**

**Examples**:
```json
// Update title only
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Updated task title"
}

// Update both fields
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Complete Q4 report",
  "description": "Include budget analysis and projections"
}
```

## Database Entity

### Task Model

The MCP server uses the existing `Task` model from `app/models/task.py`:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
```

**Fields**:
- `id`: UUID primary key, auto-generated
- `title`: String (max 200 chars), indexed for search
- `description`: Optional string (max 1000 chars)
- `completed`: Boolean flag (default False)
- `user_id`: UUID foreign key to users table, indexed
- `created_at`: Timestamp, auto-set on creation
- `updated_at`: Timestamp, updated on modification

**Indexes**:
- Primary key on `id`
- Index on `user_id` (for user-filtered queries)
- Index on `title` (for future search functionality)

**Constraints**:
- Foreign key: `user_id` → `users.id`
- Not null: `title`, `completed`, `user_id`

## Tool Response Formats

### Success Response: add_task

**MCP ToolResult**:
```python
types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text="Task created: {title} (ID: {task_id})"
    )]
)
```

**Example**:
```
Task created: Finish quarterly report (ID: 7c9e6679-7425-40de-944b-e07fc1f90ae7)
```

### Success Response: list_tasks

**MCP ToolResult**:
```python
types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text="Your tasks:\n{task_list}"
    )]
)
```

**Example (with tasks)**:
```
Your tasks:
◯ Finish quarterly report
◯ Review budget proposal
✓ Submit expense report
✓ Team meeting notes
```

**Example (empty)**:
```
No tasks found
```

**Formatting**:
- `◯` for pending tasks (`completed=False`)
- `✓` for completed tasks (`completed=True`)
- Ordered by `created_at` descending (newest first)

### Success Response: complete_task

**MCP ToolResult**:
```python
types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text="Completed: {title}"
    )]
)
```

**Example**:
```
Completed: Finish quarterly report
```

### Success Response: update_task

**MCP ToolResult**:
```python
types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text="Updated task: {title}"
    )]
)
```

**Example**:
```
Updated task: Complete Q4 financial report
```

### Success Response: delete_task

**MCP ToolResult**:
```python
types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text="Deleted: {title}"
    )]
)
```

**Example**:
```
Deleted: Finish quarterly report
```

### Error Response Format

All errors use consistent ToolResult format:

```python
types.CallToolResult(
    isError=True,
    content=[types.TextContent(
        type="text",
        text="Error: {error_message}"
    )]
)
```

**Error Categories**:

1. **Validation Errors** (400-equivalent):
   ```
   Error: Title is required
   Error: Title exceeds maximum length of 200 characters
   Error: Invalid user_id format
   Error: At least one field (title or description) must be provided
   ```

2. **Not Found Errors** (404-equivalent):
   ```
   Error: Task not found
   ```

3. **Permission Errors** (403-equivalent):
   ```
   Error: Permission denied - you can only modify your own tasks
   ```

4. **Database Errors** (500-equivalent):
   ```
   Error: Database operation failed - please try again
   ```

## State Transitions

### Task Status

Tasks have a simple completed/pending state:

```
┌─────────┐
│ Created │ (completed=False)
│ Pending │
└────┬────┘
     │
     │ complete_task()
     ▼
┌───────────┐
│ Completed │ (completed=True)
└───────────┘
```

**Operations**:
- `add_task`: Creates task with `completed=False`
- `complete_task`: Sets `completed=True`
- `update_task`: Does not change `completed` status
- `delete_task`: Removes task entirely

**Note**: There is no "uncomplete" operation. Once marked complete, task stays complete unless updated via REST API.

## Data Flow Diagrams

### add_task Flow

```
User Request → MCP Tool → Validate Input → Create Session
                              │               │
                              ▼               ▼
                        Pydantic Model   Database Engine
                              │               │
                              ▼               ▼
                         UUID Check      Insert Task
                              │               │
                              ▼               ▼
                         Max Length      Auto-generate ID
                              │               │
                              ▼               ▼
                        Success/Error    Commit Transaction
                              │               │
                              └───────┬───────┘
                                      ▼
                              Return ToolResult
```

### list_tasks Flow

```
User Request → MCP Tool → Validate Input → Create Session
                              │               │
                              ▼               ▼
                        UUID Check      Query Builder
                              │               │
                              ▼               ▼
                       Status Filter    WHERE user_id=?
                              │               │
                              ▼               ▼
                        all/pending/    Filter completed
                          completed         │
                              │               ▼
                              │          Execute Query
                              │               │
                              └───────┬───────┘
                                      ▼
                              Format Task List
                                      │
                                      ▼
                              Return ToolResult
```

### complete_task Flow

```
User Request → MCP Tool → Validate Input → Create Session
                              │               │
                              ▼               ▼
                        UUID Checks      Fetch Task
                              │               │
                              ▼               ▼
                        Ownership Check   Verify Exists
                              │               │
                              ▼               ▼
                       Permission OK?    Verify user_id
                          Yes │ No           │
                              │  └─→ Error   │
                              ▼               ▼
                        Set completed=True   │
                              │               │
                              └───────┬───────┘
                                      ▼
                              Commit Transaction
                                      │
                                      ▼
                              Return ToolResult
```

## Database Query Patterns

### Create Task

```python
from sqlmodel import Session
from app.models.task import Task
from uuid import UUID
from datetime import datetime

# Pattern used in add_task
task = Task(
    user_id=UUID(user_id),
    title=title,
    description=description,
    completed=False,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
session.add(task)
session.commit()
session.refresh(task)  # Get auto-generated ID
```

### List Tasks (with filter)

```python
from sqlmodel import select

# Base query
statement = select(Task).where(Task.user_id == UUID(user_id))

# Apply status filter
if status == "pending":
    statement = statement.where(Task.completed == False)
elif status == "completed":
    statement = statement.where(Task.completed == True)
# "all" - no additional filter

# Order by newest first
statement = statement.order_by(Task.created_at.desc())

# Execute
tasks = session.exec(statement).all()
```

### Get Single Task (with ownership check)

```python
# Fetch task
task = session.get(Task, UUID(task_id))

# Verify exists
if not task:
    raise ValueError("Task not found")

# Verify ownership
if task.user_id != UUID(user_id):
    raise ValueError("Permission denied")
```

### Update Task

```python
# Fetch and verify (same as above)
task = session.get(Task, UUID(task_id))
# ... ownership checks ...

# Update fields (partial update)
if title is not None:
    task.title = title
if description is not None:
    task.description = description

# Update timestamp
task.updated_at = datetime.utcnow()

# Commit
session.commit()
session.refresh(task)
```

### Delete Task

```python
# Fetch and verify
task = session.get(Task, UUID(task_id))
# ... ownership checks ...

# Store title for response
task_title = task.title

# Delete
session.delete(task)
session.commit()

# Return title in response
```

## Schema Files

### JSON Schema (for MCP Protocol)

Generated automatically by FastMCP from type hints:

```json
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "inputSchema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "UUID of the user creating the task"
      },
      "title": {
        "type": "string",
        "description": "Task title (1-200 characters)"
      },
      "description": {
        "type": "string",
        "description": "Optional task description (max 1000 characters)"
      }
    },
    "required": ["user_id", "title"]
  }
}
```

## Integration Points

### Existing Models

The MCP server **reuses** existing database models:
- `app/models/task.py` - Task model (no changes)
- `app/models/user.py` - User model (for reference only, no direct queries)
- `app/database.py` - Database engine and session creation

### No Schema Changes

- No database migrations required
- Uses existing `tasks` table
- Uses existing indexes on `user_id` and `title`
- Compatible with existing REST API

### Shared Database Access

- MCP server shares database engine with FastAPI
- Uses same connection pool (pool_size=5, max_overflow=10)
- No conflicts - each request gets its own session
- Stateless design - no session caching

---

**Status**: Design Complete
**Next Phase**: Implementation
**Dependencies**: No schema changes, existing models reused
