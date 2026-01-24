# MCP Tools Documentation

## Overview

The MCP Task Server provides 5 tools for managing tasks through natural language:

1. **add_task** - Create new task
2. **list_tasks** - Retrieve tasks with optional filtering
3. **complete_task** - Mark task as completed
4. **delete_task** - Remove task permanently
5. **update_task** - Modify task title and/or description

All tools are stateless and persist state to PostgreSQL database.

---

## Tool Specifications

### 1. add_task

**Purpose**: Create a new task for the user

**Parameters**:
- `user_id` (string, required) - UUID of the user creating the task
- `title` (string, required) - Task title (1-200 characters)
- `description` (string, optional) - Task description (max 1000 characters)

**Returns**:
```
Task created: {title} (ID: {task_id})
```

**Example Usage**:
```python
result = await add_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    title="Buy groceries",
    description="Milk, eggs, bread"
)
# Returns: "Task created: Buy groceries (ID: 7c9e6679-7425-40de-944b-e07fc1f90ae7)"
```

**Error Cases**:
- Empty title → "Title cannot be empty"
- Title > 200 chars → "Title must be 200 characters or less"
- Description > 1000 chars → "Description must be 1000 characters or less"
- Invalid UUID → "Invalid user_id format"

---

### 2. list_tasks

**Purpose**: Retrieve user's tasks with optional filtering

**Parameters**:
- `user_id` (string, required) - UUID of the user whose tasks to retrieve
- `status` (string, optional) - Filter: "all" (default), "pending", or "completed"

**Returns**:
```
Your tasks:
◯ Pending task 1
◯ Pending task 2
✓ Completed task 1
```

Or:
```
No tasks found
```

**Example Usage**:
```python
# Get all tasks
result = await list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    status="all"
)

# Get only pending tasks
result = await list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    status="pending"
)

# Get only completed tasks
result = await list_tasks(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    status="completed"
)
```

**Task Formatting**:
- `◯` = Pending task (completed=False)
- `✓` = Completed task (completed=True)
- Ordered by created_at descending (newest first)

**Error Cases**:
- Invalid UUID → "Invalid user_id format"
- Invalid status → "Status must be 'all', 'pending', or 'completed'"

---

### 3. complete_task

**Purpose**: Mark a task as completed

**Parameters**:
- `user_id` (string, required) - UUID of the user performing the operation
- `task_id` (string, required) - UUID of the task to complete

**Returns**:
```
Completed: {title}
```

**Example Usage**:
```python
result = await complete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="7c9e6679-7425-40de-944b-e07fc1f90ae7"
)
# Returns: "Completed: Buy groceries"
```

**Error Cases**:
- Invalid UUID → "Invalid UUID format"
- Task not found → "Task not found"
- Wrong user → "Permission denied - you can only modify your own tasks"

---

### 4. delete_task

**Purpose**: Remove a task permanently from the database

**Parameters**:
- `user_id` (string, required) - UUID of the user performing the operation
- `task_id` (string, required) - UUID of the task to delete

**Returns**:
```
Deleted: {title}
```

**Example Usage**:
```python
result = await delete_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="7c9e6679-7425-40de-944b-e07fc1f90ae7"
)
# Returns: "Deleted: Buy groceries"
```

**Error Cases**:
- Invalid UUID → "Invalid UUID format"
- Task not found → "Task not found"
- Wrong user → "Permission denied - you can only modify your own tasks"

---

### 5. update_task

**Purpose**: Modify task title and/or description

**Parameters**:
- `user_id` (string, required) - UUID of the user updating the task
- `task_id` (string, required) - UUID of the task to update
- `title` (string, optional) - New task title (1-200 characters)
- `description` (string, optional) - New task description (max 1000 characters)

**Note**: At least one of title or description must be provided

**Returns**:
```
Updated task: {new_title}
```

**Example Usage**:
```python
# Update title only
result = await update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
    title="Buy groceries and fruits"
)

# Update description only
result = await update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
    description="Milk, eggs, bread, apples, bananas"
)

# Update both
result = await update_task(
    user_id="550e8400-e29b-41d4-a716-446655440000",
    task_id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
    title="Shopping list",
    description="Full grocery shopping for the week"
)
```

**Error Cases**:
- No fields provided → "At least one of title or description must be provided"
- Empty title → "Title cannot be empty"
- Title > 200 chars → "Title must be 200 characters or less"
- Description > 1000 chars → "Description must be 1000 characters or less"
- Invalid UUID → "Invalid UUID format"
- Task not found → "Task not found"
- Wrong user → "Permission denied - you can only modify your own tasks"

---

## Natural Language Examples

| User Says | AI Calls |
|-----------|----------|
| "Add buy groceries" | `add_task(title="Buy groceries")` |
| "Create a task to call mom tomorrow" | `add_task(title="Call mom", description="Tomorrow")` |
| "Show my tasks" | `list_tasks(status="all")` |
| "What's pending?" | `list_tasks(status="pending")` |
| "Show completed tasks" | `list_tasks(status="completed")` |
| "Mark task 3 done" | `complete_task(task_id="...")` |
| "Delete task 2" | `delete_task(task_id="...")` |
| "Change task 1 title to Call mom" | `update_task(task_id="...", title="Call mom")` |
| "Update task description" | `update_task(task_id="...", description="...")` |

---

## Server Configuration

### Starting the MCP Server

#### Development Mode (stdio):
```bash
cd backend
export MCP_TRANSPORT=stdio
python -m app.mcp_server.server
```

#### Production Mode (HTTP):
```bash
cd backend
export MCP_TRANSPORT=http
export MCP_PORT=8001
python -m app.mcp_server.server
```

### Environment Variables

- `MCP_TRANSPORT`: Transport type - "stdio" or "http" (default: "http")
- `MCP_PORT`: Port for HTTP transport (default: 8001)
- `MCP_HOST`: Host for HTTP transport (default: "0.0.0.0")
- `DATABASE_URL`: PostgreSQL connection string (required)

### Testing the Tools

Run the test script to verify all tools work correctly:

```bash
cd backend
python -m app.mcp_server.test_tools
```

Expected output:
```
Testing MCP Tools
============================================================
Test User ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

1️⃣  Testing add_task...
✅ Task created: Test MCP Task (ID: ...)
...
All MCP tool tests completed!
```

---

## Integration with AI Assistants

### Using with Gemini

The MCP server integrates seamlessly with Google Gemini or other AI assistants that support the MCP protocol:

```python
from app.mcp_server import mcp

# The FastMCP instance exposes tools automatically
# AI assistants can discover and call them through the MCP protocol
```

### Tool Discovery

When connected via MCP, AI assistants can:
1. List all available tools (5 tools)
2. Get parameter schemas for each tool (auto-generated from type hints)
3. Call tools with validated parameters
4. Receive formatted text responses

---

## Security & User Isolation

### User Ownership Validation

All tools that access or modify tasks verify user ownership:

```python
# Task must belong to the user_id provided
if task.user_id != UUID(user_id):
    raise ValueError("Permission denied - you can only modify your own tasks")
```

### Stateless Design

- No in-memory session state
- Each tool call is independent
- Database is single source of truth
- Server restarts don't affect data

---

## Performance Characteristics

### Target Latencies (P95)

- add_task: < 500ms
- list_tasks: < 300ms (up to 1000 tasks)
- complete_task: < 400ms
- delete_task: < 400ms
- update_task: < 400ms

### Database Queries

- All queries use existing indexes on `user_id`
- Queries are parameterized (SQL injection safe)
- Connection pooling handles concurrent requests
- Automatic transaction management

---

## Error Handling

All errors are returned as `ValueError` exceptions with descriptive messages that AI assistants can understand and communicate to users:

**Validation Errors**:
```python
ValueError("Title cannot be empty")
ValueError("Invalid user_id format")
```

**Authorization Errors**:
```python
ValueError("Permission denied - you can only modify your own tasks")
```

**Not Found Errors**:
```python
ValueError("Task not found")
```

**Database Errors**:
```python
ValueError("Failed to create task: ...")
```

---

## Implementation Details

### Technology Stack

- **MCP SDK**: mcp[cli]==1.25.0
- **FastMCP**: High-level decorator-based API
- **Database**: PostgreSQL via SQLModel (sync operations)
- **Validation**: Python type hints (auto-schema generation)
- **Transport**: Streamable HTTP (production), stdio (development)

### Database Schema

Uses existing `tasks` table:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### File Structure

```
backend/app/mcp_server/
├── __init__.py        # Package exports
├── tools.py           # All 5 MCP tools
├── server.py          # Server initialization
└── test_tools.py      # Test script
```

---

## Troubleshooting

### Common Issues

**Import Error**: "cannot import name 'mcp'"
- Solution: Ensure `mcp[cli]==1.25.0` is installed
- Run: `pip install "mcp[cli]==1.25.0"`

**Database Connection Error**
- Solution: Verify `DATABASE_URL` environment variable is set
- Check PostgreSQL is running and accessible

**Permission Denied Errors**
- Solution: Verify `user_id` matches task ownership
- Each user can only access their own tasks

**Tool Not Found**
- Solution: Ensure MCP server is running
- Check transport configuration (stdio vs HTTP)

---

## Further Reading

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
