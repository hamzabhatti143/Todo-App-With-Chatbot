# Quick Start: MCP Task Server

**Feature**: 015-mcp-task-server
**Date**: 2026-01-17

## Overview

This guide provides step-by-step instructions for setting up, running, and testing the MCP Task Server. The server provides 5 tools for task management via the Model Context Protocol.

## Prerequisites

- Python 3.11+ installed
- PostgreSQL database (existing todo app database)
- Existing backend environment configured
- MCP client for testing (Claude Desktop, or HTTP client)

## Installation

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Activate Virtual Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

### 3. Install Dependencies

Update `requirements.txt` with MCP SDK:

```bash
# Add to requirements.txt
mcp[cli]==1.25.0
```

Install:

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import mcp; print(f'MCP SDK version: {mcp.__version__}')"
```

Expected output:
```
MCP SDK version: 1.25.0
```

## Configuration

### Environment Variables

The MCP server uses existing database configuration:

```bash
# .env (already configured)
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Optional: MCP server port (default: 8001)
MCP_PORT=8001

# Optional: MCP transport (default: streamable-http)
MCP_TRANSPORT=streamable-http
```

**No new environment variables required** - uses existing `DATABASE_URL`.

### Port Configuration

- **REST API**: Port 8000 (existing)
- **MCP Server**: Port 8001 (new, default)

Both services can run concurrently.

## Running the MCP Server

### Development Mode (stdio transport)

For local testing with Claude Desktop or stdio clients:

```bash
export MCP_TRANSPORT=stdio
python -m app.mcp_server.server
```

Server will communicate via stdin/stdout.

### Production Mode (HTTP transport)

For web clients and production deployment:

```bash
export MCP_TRANSPORT=streamable-http
export MCP_PORT=8001
python -m app.mcp_server.server
```

Server runs on `http://localhost:8001`.

### Concurrent with REST API

Run both FastAPI REST API and MCP server:

```bash
# Terminal 1: REST API
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: MCP Server
cd backend
python -m app.mcp_server.server --port 8001
```

## Testing the Server

### Method 1: Test Script

Run the included test script:

```bash
python -m app.mcp_server.test_tools
```

Expected output:
```
Testing add_task...
✓ Task created: Test Task (ID: 7c9e6679-...)

Testing list_tasks...
✓ Listed 1 tasks

Testing complete_task...
✓ Completed: Test Task

Testing delete_task...
✓ Deleted: Test Task

All tests passed!
```

### Method 2: Manual HTTP Testing

Using `curl` with HTTP transport:

**1. Create Task**:

```bash
curl -X POST http://localhost:8001/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "add_task",
    "arguments": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish quarterly report",
      "description": "Complete Q4 analysis"
    }
  }'
```

Response:
```json
{
  "content": [{
    "type": "text",
    "text": "Task created: Finish quarterly report (ID: 7c9e6679-...)"
  }]
}
```

**2. List Tasks**:

```bash
curl -X POST http://localhost:8001/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_tasks",
    "arguments": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "all"
    }
  }'
```

Response:
```json
{
  "content": [{
    "type": "text",
    "text": "Your tasks:\n◯ Finish quarterly report"
  }]
}
```

**3. Complete Task**:

```bash
curl -X POST http://localhost:8001/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "complete_task",
    "arguments": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
    }
  }'
```

Response:
```json
{
  "content": [{
    "type": "text",
    "text": "Completed: Finish quarterly report"
  }]
}
```

**4. Update Task**:

```bash
curl -X POST http://localhost:8001/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "update_task",
    "arguments": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "title": "Complete Q4 financial report",
      "description": "Include budget analysis"
    }
  }'
```

Response:
```json
{
  "content": [{
    "type": "text",
    "text": "Updated task: Complete Q4 financial report"
  }]
}
```

**5. Delete Task**:

```bash
curl -X POST http://localhost:8001/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "delete_task",
    "arguments": {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
    }
  }'
```

Response:
```json
{
  "content": [{
    "type": "text",
    "text": "Deleted: Complete Q4 financial report"
  }]
}
```

### Method 3: Claude Desktop Integration

Add MCP server to Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "todo-tasks": {
      "command": "python",
      "args": ["-m", "app.mcp_server.server"],
      "cwd": "/path/to/todo-fullstack-web/backend",
      "env": {
        "MCP_TRANSPORT": "stdio",
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

Restart Claude Desktop. MCP tools will appear in tool menu.

## Tool Reference

### add_task

**Purpose**: Create a new task

**Parameters**:
- `user_id` (required): UUID string
- `title` (required): String, 1-200 characters
- `description` (optional): String, max 1000 characters

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Write blog post",
  "description": "Topic: MCP integration patterns"
}
```

### list_tasks

**Purpose**: Retrieve user's tasks with optional filtering

**Parameters**:
- `user_id` (required): UUID string
- `status` (optional): "all" | "pending" | "completed" (default: "all")

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

### complete_task

**Purpose**: Mark a task as completed

**Parameters**:
- `user_id` (required): UUID string
- `task_id` (required): UUID string

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

### delete_task

**Purpose**: Permanently remove a task

**Parameters**:
- `user_id` (required): UUID string
- `task_id` (required): UUID string

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

### update_task

**Purpose**: Update task title and/or description

**Parameters**:
- `user_id` (required): UUID string
- `task_id` (required): UUID string
- `title` (optional): String, 1-200 characters
- `description` (optional): String, max 1000 characters

**Note**: At least one of `title` or `description` must be provided

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Updated title",
  "description": "Updated description"
}
```

## Error Handling

### Common Errors

**Invalid UUID Format**:
```json
{
  "isError": true,
  "content": [{
    "type": "text",
    "text": "Error: Invalid user_id format"
  }]
}
```

**Task Not Found**:
```json
{
  "isError": true,
  "content": [{
    "type": "text",
    "text": "Error: Task not found"
  }]
}
```

**Permission Denied**:
```json
{
  "isError": true,
  "content": [{
    "type": "text",
    "text": "Error: Permission denied - you can only modify your own tasks"
  }]
}
```

**Validation Error**:
```json
{
  "isError": true,
  "content": [{
    "type": "text",
    "text": "Error: Title exceeds maximum length of 200 characters"
  }]
}
```

## Troubleshooting

### Server won't start

**Check Python version**:
```bash
python --version  # Should be 3.11+
```

**Check dependencies**:
```bash
pip list | grep mcp
```

**Check DATABASE_URL**:
```bash
echo $DATABASE_URL
```

### Database connection errors

**Verify PostgreSQL is running**:
```bash
psql $DATABASE_URL -c "SELECT 1"
```

**Check SSL mode** (for Neon):
```bash
# DATABASE_URL should include: ?sslmode=require
```

### Tools not responding

**Check server is running**:
```bash
curl http://localhost:8001/health
```

**Check logs for errors**:
```bash
# Server logs printed to stdout
```

**Verify task exists**:
```bash
# Query database directly
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE id='task-uuid'"
```

### Permission denied errors

**Verify user_id matches task owner**:
- Tool receives `user_id` parameter
- Task has `user_id` field in database
- These must match for complete/update/delete operations

**Check task ownership**:
```bash
psql $DATABASE_URL -c "SELECT id, user_id, title FROM tasks WHERE id='task-uuid'"
```

## Deployment

### Docker Deployment

Add MCP server to `docker-compose.yml`:

```yaml
services:
  backend-api:
    # Existing FastAPI service on port 8000
    ...

  mcp-server:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python -m app.mcp_server.server
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - MCP_TRANSPORT=streamable-http
      - MCP_PORT=8001
    ports:
      - "8001:8001"
    depends_on:
      - database
```

### Production Considerations

1. **Authentication**: MCP server assumes trusted user_id. Run behind authentication gateway in production.

2. **Rate Limiting**: Consider adding rate limiting at gateway level.

3. **Monitoring**: Add health check endpoint and logging.

4. **Scaling**: Streamable HTTP transport supports horizontal scaling.

5. **Security**: Restrict MCP server to internal network or trusted clients only.

## Next Steps

1. **Explore Tools**: Test all 5 tools with your task data
2. **Integration**: Connect MCP client (Claude Desktop, custom client)
3. **Monitoring**: Set up logging and error tracking
4. **Documentation**: Refer to tool-specifications.md for detailed API docs
5. **Development**: See data-model.md for schema details

## Support Resources

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Data Models**: [data-model.md](./data-model.md)
- **MCP SDK Docs**: https://modelcontextprotocol.github.io/python-sdk/
- **MCP Protocol**: https://modelcontextprotocol.io/

---

**Version**: 1.0.0
**Last Updated**: 2026-01-17
**Status**: Ready for Implementation
