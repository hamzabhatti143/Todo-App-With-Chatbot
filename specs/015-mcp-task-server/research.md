# Research: MCP Task Server Implementation

**Feature**: 015-mcp-task-server
**Date**: 2026-01-17
**Status**: Complete

## Overview

This document consolidates research findings for implementing the MCP Task Server, specifically investigating the Model Context Protocol SDK, async/sync integration patterns, and deployment strategies.

## Decision 1: MCP SDK Package and Version

### Decision

Use **official MCP Python SDK** version **1.25.0** with **FastMCP** high-level API.

### Research Findings

**Package Details**:
- **Package Name**: `mcp` (on PyPI)
- **Current Version**: 1.25.0 (January 2026)
- **GitHub**: https://github.com/modelcontextprotocol/python-sdk
- **Installation**: `pip install "mcp[cli]"`

**Key Features**:
- Over 56 million downloads/month
- Two APIs: FastMCP (high-level, decorator-based) and Low-Level (fine-grained control)
- Automatic JSON Schema generation from type hints
- Built-in transport support (stdio, HTTP, SSE)
- Official protocol compliance

### Rationale

1. **Official SDK**: Authoritative implementation of MCP protocol
2. **Maturity**: v1.x is stable, production-ready (v2 in pre-alpha)
3. **Developer Experience**: FastMCP decorators simplify tool definition
4. **Type Safety**: Automatic schema from Python type hints
5. **Future-Proof**: Active development, broad adoption

### Implementation Pattern

```python
from mcp.server.fastmcp import FastMCP
import mcp.types as types

mcp = FastMCP("Todo Task Server")

@mcp.tool()
def add_task(user_id: str, title: str, description: str = None) -> types.CallToolResult:
    \"\"\"Create a new task for the user.\"\"\"
    try:
        # Implementation
        result = create_task_in_db(user_id, title, description)
        return types.CallToolResult(
            content=[types.TextContent(
                type="text",
                text=f"Task created: {result['task_id']}"
            )]
        )
    except Exception as e:
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        )

if __name__ == "__main__":
    mcp.run(transport="streamable-http", json_response=True)
```

### Alternatives Considered

**Option A: Custom MCP Implementation**
- **Pros**: Full control, no dependency
- **Cons**: Protocol complexity, maintenance burden, no interoperability
- **Rejected**: Official SDK provides better compliance and support

**Option B: Low-Level MCP SDK API**
- **Pros**: Fine-grained control over tool lifecycle
- **Cons**: More boilerplate, manual schema definition
- **Rejected**: FastMCP sufficient for our needs, simpler

**Option C: Older MCP SDK (1.0.0)**
- **Pros**: Already in requirements.txt
- **Cons**: Outdated (25 versions behind), missing features
- **Rejected**: Update to 1.25.0 for latest improvements

### Dependencies

Add to `backend/requirements.txt`:
```
mcp[cli]==1.25.0
```

Remove or update:
```
# Old: mcp==1.0.0
# New: mcp[cli]==1.25.0
```

## Decision 2: MCP Server Transport Protocol

### Decision

Use **Streamable HTTP** transport for production, with **stdio** for development/testing.

### Research Findings

**Transport Options**:

1. **stdio (Standard Input/Output)**:
   - Local process communication via stdin/stdout
   - Use case: Claude Desktop integration, local development
   - Format: JSON-RPC messages over pipes
   - Example: `python server.py` launches server process

2. **Streamable HTTP**:
   - HTTP-based request/response with streaming
   - Use case: Production deployments, web clients
   - Benefits: Stateless, horizontally scalable, load-balancer compatible
   - Example: Run on port with HTTP endpoint

3. **SSE (Server-Sent Events)**:
   - One-way streaming over HTTP
   - Use case: Web-based clients needing live updates
   - Less suitable for stateless request-response pattern

### Rationale

**Primary: Streamable HTTP**
1. **Stateless**: Aligns with specification requirement (no in-memory state)
2. **Scalable**: Multiple server instances can run concurrently
3. **Standard**: Uses familiar HTTP infrastructure
4. **Production-Ready**: Works with existing web infrastructure

**Secondary: stdio for Development**
1. **Simplicity**: Easy to test during development
2. **Claude Desktop**: Standard for local AI assistant integration
3. **Debugging**: Direct process I/O simplifies testing

### Implementation Pattern

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo Task Server")

# Define tools with @mcp.tool() decorators
# ... tool definitions ...

if __name__ == "__main__":
    import os

    # Use environment variable to select transport
    transport = os.getenv("MCP_TRANSPORT", "streamable-http")

    if transport == "stdio":
        # Development mode
        mcp.run(transport="stdio")
    else:
        # Production mode
        mcp.run(
            transport="streamable-http",
            json_response=True,      # Optimal for performance
            stateless_http=True,     # No session state
            host="0.0.0.0",
            port=int(os.getenv("MCP_PORT", "8001"))
        )
```

### Deployment Strategy

**Development**:
```bash
export MCP_TRANSPORT=stdio
python -m app.mcp_server.server
```

**Production**:
```bash
export MCP_TRANSPORT=http
export MCP_PORT=8001
python -m app.mcp_server.server
```

**Docker**:
```dockerfile
# Runs alongside FastAPI on different port
CMD ["python", "-m", "app.mcp_server.server"]
ENV MCP_TRANSPORT=http
ENV MCP_PORT=8001
```

### Alternatives Considered

**Option A: stdio Only**
- **Pros**: Simpler, standard for MCP
- **Cons**: Requires process management, not horizontally scalable
- **Rejected**: Doesn't meet stateless/scalability requirements

**Option B: SSE (Server-Sent Events)**
- **Pros**: Real-time streaming
- **Cons**: One-way communication, less suitable for request-response
- **Rejected**: Streamable HTTP better for our use case

**Option C: Custom HTTP Server**
- **Pros**: Full control
- **Cons**: Re-implements MCP transport layer
- **Rejected**: SDK provides production-ready HTTP transport

## Decision 3: MCP ToolResult Error Format

### Decision

Use **MCP ToolResult with `isError=True`** for tool-level errors, allowing LLMs to see and handle errors gracefully.

### Research Findings

**MCP Error Types**:

1. **Tool-Level Errors** (Recommended):
   - Errors returned in ToolResult with `isError=True`
   - LLM can see error messages and attempt recovery
   - Use for: Validation errors, not found, permission denied, business logic errors

2. **Protocol-Level Errors**:
   - Exceptions raised that halt tool execution
   - Use only for: Structural issues, invalid tool calls, server failures

**Error Response Structure**:

```python
# Success
types.CallToolResult(
    content=[
        types.TextContent(type="text", text="Operation successful: ...")
    ]
)

# Tool-level error (recommended for validation, not found, etc.)
types.CallToolResult(
    isError=True,
    content=[
        types.TextContent(type="text", text="Error: Task not found")
    ]
)

# Protocol-level error (only for critical failures)
raise ValueError("Invalid tool invocation")
```

### Rationale

1. **LLM Awareness**: Tool-level errors let AI assistants see what went wrong
2. **Recovery**: LLM can retry with corrected parameters or inform user
3. **User Experience**: Better than opaque "server error" messages
4. **Consistency**: All business logic errors use same format

### Error Categories and Messages

**Validation Errors** (400-equivalent):
```python
# Missing required field
"Error: Title is required"

# Max length exceeded
"Error: Title exceeds maximum length of 200 characters"

# Invalid UUID format
"Error: Invalid user_id format"
```

**Not Found Errors** (404-equivalent):
```python
# Task doesn't exist
"Error: Task not found"
```

**Permission Errors** (403-equivalent):
```python
# User doesn't own task
"Error: Permission denied - you can only modify your own tasks"
```

**Database Errors** (500-equivalent):
```python
# Connection failure
"Error: Database connection failed - please try again"

# Constraint violation
"Error: Database constraint violation"
```

### Implementation Pattern

```python
@mcp.tool()
def complete_task(user_id: str, task_id: str) -> types.CallToolResult:
    \"\"\"Mark a task as completed.\"\"\"
    try:
        # Input validation
        if not is_valid_uuid(user_id):
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(
                    type="text",
                    text="Error: Invalid user_id format"
                )]
            )

        # Business logic
        task = get_task(user_id, task_id)
        if not task:
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(
                    type="text",
                    text="Error: Task not found"
                )]
            )

        if task.user_id != user_id:
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(
                    type="text",
                    text="Error: Permission denied - you can only modify your own tasks"
                )]
            )

        # Update task
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.commit()

        # Success
        return types.CallToolResult(
            content=[types.TextContent(
                type="text",
                text=f"Task completed: {task.title}"
            )]
        )

    except DatabaseError as e:
        # Database-level error
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(
                type="text",
                text=f"Error: Database operation failed - {str(e)}"
            )]
        )
    except Exception as e:
        # Unexpected error - log and return generic message
        logger.error(f"Unexpected error in complete_task: {e}")
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(
                type="text",
                text="Error: An unexpected error occurred"
            )]
        )
```

### Alternatives Considered

**Option A: HTTP Status Code Model**
- **Pros**: Familiar pattern from REST APIs
- **Cons**: MCP protocol uses different error model
- **Rejected**: Doesn't align with MCP ToolResult format

**Option B: Exception-Based Errors**
- **Pros**: Python-native error handling
- **Cons**: LLM doesn't see error details, poor user experience
- **Rejected**: Tool-level errors provide better LLM integration

**Option C: Structured Error Objects**
- **Pros**: Machine-parseable error codes
- **Cons**: More complex, MCP uses text-based errors
- **Rejected**: Text errors sufficient for LLM understanding

## Decision 4: Async/Sync Database Integration

### Decision

**Wrap synchronous database operations** in async tool functions using existing `get_session()` pattern.

### Research Findings

**Current Database Pattern** (Synchronous):
```python
# From app/database.py
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Usage in FastAPI routes
@router.get("/tasks")
def list_tasks(session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()
```

**MCP Requirement**: Tools must be async functions

**Integration Options**:

1. **Keep Sync, Wrap in Async**:
   - Manually create and close sessions in tool functions
   - Use synchronous SQLModel operations
   - No changes to existing database layer

2. **Convert to Async Database**:
   - Use asyncpg driver
   - Update all database operations to async/await
   - Major refactoring of existing code

3. **Use asyncio.to_thread()**:
   - Run sync database code in thread pool
   - Minimal code changes
   - Potential performance overhead

### Rationale

**Chosen: Keep Sync, Wrap in Async**

1. **No Breaking Changes**: Existing REST API continues working
2. **Code Reuse**: Same database models and query patterns
3. **Simplicity**: No async database driver complexity
4. **Performance**: Database operations are I/O-bound, sync acceptable for MCP use case
5. **Isolation**: MCP server database code independent of REST API

### Implementation Pattern

```python
from app.database import engine
from sqlmodel import Session, select
from app.models.task import Task

@mcp.tool()
async def list_tasks(user_id: str, status: str = "all") -> types.CallToolResult:
    \"\"\"List user's tasks with optional status filter.\"\"\"
    try:
        # Create session manually (can't use FastAPI Depends)
        with Session(engine) as session:
            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

            # Execute query
            tasks = session.exec(statement).all()

            # Format response
            task_list = [
                f"- {task.title} ({'✓' if task.completed else '◯'})"
                for task in tasks
            ]

            return types.CallToolResult(
                content=[types.TextContent(
                    type="text",
                    text="\n".join(task_list) if task_list else "No tasks found"
                )]
            )
    except Exception as e:
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        )
```

### Transaction Pattern

```python
@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> types.CallToolResult:
    \"\"\"Delete a task permanently.\"\"\"
    with Session(engine) as session:
        try:
            # Fetch task
            task = session.get(Task, task_id)

            # Validation
            if not task:
                return error_response("Task not found")
            if task.user_id != user_id:
                return error_response("Permission denied")

            # Delete in transaction
            session.delete(task)
            session.commit()

            return success_response(f"Deleted task: {task.title}")

        except Exception as e:
            # Rollback on error
            session.rollback()
            return error_response(f"Database error: {str(e)}")
```

### Alternatives Considered

**Option A: Async Database (asyncpg + SQLAlchemy async)**
- **Pros**: True async I/O, better concurrency
- **Cons**: Requires refactoring existing code, more complex
- **Rejected**: Not needed for MCP server scale, breaks existing REST API

**Option B: asyncio.to_thread() Wrapper**
- **Pros**: Automatic sync-to-async conversion
- **Cons**: Thread pool overhead, harder to debug
- **Rejected**: Manual session management cleaner and more explicit

**Option C: FastAPI Dependency Injection in MCP**
- **Pros**: Reuses existing patterns
- **Cons**: MCP tools aren't FastAPI routes, incompatible
- **Rejected**: Can't use FastAPI Depends() in MCP tool functions

### Performance Considerations

**Database Connection Pooling**:
- Existing configuration: `pool_size=5, max_overflow=10`
- MCP server shares same engine/pool as REST API
- No changes needed

**Concurrency**:
- MCP HTTP transport handles concurrent requests
- Each tool invocation gets its own session
- No session state carried between requests

**Benchmarking**:
- Target: P95 latency < 500ms
- Typical database query: 10-50ms
- Session creation overhead: ~1-5ms
- Expected total: 20-100ms per tool call (well within target)

## Decision 5: Tool Response Format

### Decision

Return **text-based task summaries** in ToolResult content, optimized for LLM comprehension.

### Research Findings

**MCP Content Types**:
- `TextContent`: Plain text or formatted text
- `ImageContent`: Base64-encoded images
- `EmbeddedResource`: Structured resources

**Text Format Options**:
1. **JSON strings**: `"{\"task_id\": \"123\", \"title\": \"...\"}"string in content
2. **Formatted text**: `"Task created: Finish report (ID: 123)"`
3. **Markdown**: `"**Task Created**\n- Title: Finish report\n- ID: 123"`

### Rationale

**Chosen: Formatted Text (Human-Readable)**

1. **LLM Optimization**: AI assistants parse natural language better than JSON strings
2. **User-Facing**: LLM presents directly to user without additional formatting
3. **Readability**: Clear, concise summaries
4. **Flexibility**: LLM can rephrase for user

### Implementation Examples

**Success Responses**:

```python
# add_task
return types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text=f"Task created: {title} (ID: {task.id})"
    )]
)

# list_tasks
task_list = "\n".join([
    f"{'✓' if t.completed else '◯'} {t.title}"
    for t in tasks
])
return types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text=f"Your tasks:\n{task_list}" if task_list else "No tasks found"
    )]
)

# complete_task
return types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text=f"Completed: {task.title}"
    )]
)

# update_task
return types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text=f"Updated task: {task.title}"
    )]
)

# delete_task
return types.CallToolResult(
    content=[types.TextContent(
        type="text",
        text=f"Deleted: {task.title}"
    )]
)
```

### Alternatives Considered

**Option A: JSON Strings**
- **Pros**: Structured, machine-parseable
- **Cons**: LLM must parse JSON, less natural for conversation
- **Rejected**: Formatted text better for LLM-to-user flow

**Option B: Markdown Formatting**
- **Pros**: Rich formatting, lists, emphasis
- **Cons**: Overkill for simple responses, inconsistent rendering
- **Rejected**: Plain text sufficient for task descriptions

**Option C: Multiple Content Items**
- **Pros**: Separate text, structured data, metadata
- **Cons**: More complex, single text item sufficient
- **Rejected**: Single TextContent item simpler and adequate

## Summary of Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **MCP SDK** | `mcp==1.25.0` with FastMCP | Official SDK, decorator-based simplicity, type safety |
| **Transport** | Streamable HTTP (primary), stdio (dev) | Stateless, scalable, standard HTTP infrastructure |
| **Error Format** | ToolResult with `isError=True` | LLM-visible errors, better recovery, user experience |
| **Database** | Sync SQLModel with manual sessions | No breaking changes, code reuse, simplicity |
| **Response Format** | Formatted text (human-readable) | LLM-optimized, natural language, user-facing |

## Implementation Readiness

All research questions resolved. Ready to proceed with implementation:

1. **Dependencies**: `mcp[cli]==1.25.0`
2. **Tool Definition**: FastMCP `@mcp.tool()` decorators
3. **Error Handling**: ToolResult `isError=True` pattern
4. **Database**: Manual `Session(engine)` in tool functions
5. **Transport**: Streamable HTTP on port 8001
6. **Response**: Text-based task summaries

## References

- [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Python SDK PyPI](https://pypi.org/project/mcp/)
- [MCP Python SDK Documentation](https://modelcontextprotocol.github.io/python-sdk/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/docs/develop/build-server)
- [FastMCP Documentation](https://gofastmcp.com/servers/tools)
- [MCP Error Handling Guide](https://mcpcat.io/guides/error-handling-custom-mcp-servers/)

---

**Status**: Complete
**Next Phase**: Phase 1 - Create data models and implementation plan
