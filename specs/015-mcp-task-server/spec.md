# Feature Specification: MCP Task Server

**Feature ID**: 015-mcp-task-server
**Status**: Draft
**Created**: 2026-01-17
**Last Updated**: 2026-01-17

## Overview

A stateless Model Context Protocol (MCP) server that provides 5 task management tools for creating, listing, updating, completing, and deleting tasks. The server integrates with the existing PostgreSQL database to persist all task operations, ensuring no in-memory state is maintained between requests.

## Problem Statement

The todo application needs an MCP-compliant interface to enable AI assistants and other MCP clients to perform task operations programmatically. Currently, task operations are only available through REST API endpoints, which limits integration with MCP-enabled tools and platforms. Users working with AI assistants should be able to manage their tasks through natural language commands that translate to MCP tool calls.

## User Scenarios & Testing

### Primary User Flow: AI Assistant Managing Tasks

**Actor**: User interacting with AI assistant (e.g., Claude Desktop, ChatGPT)

**Scenario 1: Creating a Task**

1. User says: "Add a task to finish the quarterly report"
2. AI assistant calls `add_task` tool with:
   - user_id: "current-user-uuid"
   - title: "Finish quarterly report"
3. MCP server creates task in database
4. Returns task_id, status ("pending"), and title to AI
5. AI confirms: "I've added 'Finish quarterly report' to your tasks"

**Expected Outcome**: Task appears in user's task list with "pending" status

**Scenario 2: Listing Tasks**

1. User asks: "What tasks do I have pending?"
2. AI calls `list_tasks` tool with:
   - user_id: "current-user-uuid"
   - status: "pending"
3. MCP server queries database for user's incomplete tasks
4. Returns array of task objects with id, title, description, status
5. AI presents formatted list to user

**Expected Outcome**: User sees all their incomplete tasks

**Scenario 3: Completing a Task**

1. User says: "Mark the quarterly report task as done"
2. AI identifies task_id from previous context
3. AI calls `complete_task` tool with:
   - user_id: "current-user-uuid"
   - task_id: "identified-task-uuid"
4. MCP server updates task.completed = True in database
5. Returns updated task status to AI
6. AI confirms: "Great! I've marked 'Finish quarterly report' as complete"

**Expected Outcome**: Task status changes from "pending" to "completed"

**Scenario 4: Updating a Task**

1. User says: "Change the report task description to include Q4 data"
2. AI calls `update_task` tool with:
   - user_id: "current-user-uuid"
   - task_id: "identified-task-uuid"
   - description: "Finish quarterly report including Q4 data"
3. MCP server updates task description in database
4. Returns updated task details
5. AI confirms the update

**Expected Outcome**: Task description is modified without changing other fields

**Scenario 5: Deleting a Task**

1. User says: "Remove the quarterly report task"
2. AI calls `delete_task` tool with:
   - user_id: "current-user-uuid"
   - task_id: "identified-task-uuid"
3. MCP server validates ownership and deletes task
4. Returns deletion confirmation
5. AI confirms: "I've removed 'Finish quarterly report' from your tasks"

**Expected Outcome**: Task is permanently removed from database

### Edge Cases & Error Handling

**Error Case 1: Task Not Found**

- User: "Complete task ABC"
- AI calls complete_task with invalid task_id
- Server returns error: "Task not found"
- AI informs user task doesn't exist

**Error Case 2: Permission Denied**

- AI attempts to access another user's task
- Server validates user_id doesn't match task owner
- Returns error: "Permission denied"
- AI informs user they can't access that task

**Error Case 3: Invalid Input**

- User: "Add a task" (no title provided)
- AI calls add_task without title parameter
- Server validates required fields
- Returns error: "Title is required"
- AI asks user for task title

**Error Case 4: Title Too Long**

- User provides 250-character title
- Server validates max length (200 chars)
- Returns error: "Title exceeds maximum length of 200 characters"
- AI asks user to shorten the title

## Functional Requirements

### FR-001: Add Task Tool

The MCP server shall provide an `add_task` tool that:

- Accepts required parameter: user_id (UUID string)
- Accepts required parameter: title (string, max 200 characters)
- Accepts optional parameter: description (string, max 1000 characters)
- Validates user_id is a valid UUID format
- Validates title is not empty and does not exceed 200 characters
- Validates description (if provided) does not exceed 1000 characters
- Inserts new task into tasks table with completed=False
- Auto-generates task_id (UUID) and timestamps
- Returns JSON object containing: task_id, status ("pending"), title
- Handles database connection errors gracefully
- Completes within 500ms for 95% of requests

**Acceptance Criteria**:

- Tool creates task with all provided fields
- Task is immediately queryable via list_tasks
- Returns valid UUID task_id
- Status is always "pending" for new tasks
- Timestamps (created_at, updated_at) are auto-populated

### FR-002: List Tasks Tool

The MCP server shall provide a `list_tasks` tool that:

- Accepts required parameter: user_id (UUID string)
- Accepts optional parameter: status (enum: "all", "pending", "completed", default: "all")
- Validates user_id is a valid UUID format
- Validates status is one of allowed values
- Queries tasks table filtering by user_id
- Filters by completion status based on status parameter:
  - "pending": WHERE completed = False
  - "completed": WHERE completed = True
  - "all": no completion filter
- Returns array of task objects, each containing:
  - task_id (UUID string)
  - title (string)
  - description (string or null)
  - status (string: "pending" or "completed")
  - created_at (ISO 8601 timestamp)
  - updated_at (ISO 8601 timestamp)
- Orders results by created_at descending (newest first)
- Returns empty array if no tasks match criteria
- Handles database connection errors gracefully
- Completes within 300ms for 95% of requests with up to 1000 tasks

**Acceptance Criteria**:

- Returns only tasks belonging to specified user_id
- Status filter correctly includes/excludes completed tasks
- Task objects contain all required fields
- Timestamps are in ISO 8601 format
- Results are ordered newest-first

### FR-003: Complete Task Tool

The MCP server shall provide a `complete_task` tool that:

- Accepts required parameter: user_id (UUID string)
- Accepts required parameter: task_id (UUID string)
- Validates both user_id and task_id are valid UUID format
- Queries database to verify task exists
- Validates task belongs to specified user_id
- Returns "Task not found" error if task doesn't exist
- Returns "Permission denied" error if user doesn't own task
- Updates tasks table: SET completed = True, updated_at = NOW()
- Returns JSON object containing: task_id, status ("completed"), title
- Uses database transactions to ensure atomicity
- Handles database connection errors gracefully
- Completes within 400ms for 95% of requests

**Acceptance Criteria**:

- Task completed flag changes from False to True
- updated_at timestamp is updated
- Returns error for non-existent tasks
- Returns error if user doesn't own task
- Change is immediately visible in list_tasks results

### FR-004: Delete Task Tool

The MCP server shall provide a `delete_task` tool that:

- Accepts required parameter: user_id (UUID string)
- Accepts required parameter: task_id (UUID string)
- Validates both user_id and task_id are valid UUID format
- Queries database to verify task exists
- Validates task belongs to specified user_id
- Returns "Task not found" error if task doesn't exist
- Returns "Permission denied" error if user doesn't own task
- Deletes task from tasks table (hard delete)
- Returns JSON object containing: task_id, status ("deleted"), title (from deleted task)
- Uses database transactions to ensure atomicity
- Handles database connection errors gracefully
- Completes within 400ms for 95% of requests

**Acceptance Criteria**:

- Task is permanently removed from database
- Returns error for non-existent tasks
- Returns error if user doesn't own task
- Deleted task no longer appears in list_tasks results
- Returns title of deleted task for confirmation

### FR-005: Update Task Tool

The MCP server shall provide an `update_task` tool that:

- Accepts required parameter: user_id (UUID string)
- Accepts required parameter: task_id (UUID string)
- Accepts optional parameter: title (string, max 200 characters)
- Accepts optional parameter: description (string, max 1000 characters)
- Validates user_id and task_id are valid UUID format
- Requires at least one of title or description to be provided
- Validates title (if provided) is not empty and ≤ 200 characters
- Validates description (if provided) ≤ 1000 characters
- Queries database to verify task exists
- Validates task belongs to specified user_id
- Returns "Task not found" error if task doesn't exist
- Returns "Permission denied" error if user doesn't own task
- Returns "At least one field required" if neither title nor description provided
- Updates only provided fields (partial update)
- Updates updated_at timestamp
- Returns JSON object containing: task_id, status (current completion status), title
- Uses database transactions to ensure atomicity
- Handles database connection errors gracefully
- Completes within 400ms for 95% of requests

**Acceptance Criteria**:

- Only provided fields are updated
- Unprovided fields retain original values
- updated_at timestamp is updated
- Returns error for non-existent tasks
- Returns error if user doesn't own task
- Returns error if no update fields provided
- Changes are immediately visible in list_tasks results

### FR-006: MCP Protocol Compliance

The MCP server shall:

- Implement MCP protocol specification version 1.0 or later
- Use Official MCP SDK (mcp-sdk Python package)
- Define each tool using MCP Tool base class
- Specify ToolParameter for each parameter with:
  - name (parameter name)
  - type (string, boolean, etc.)
  - required (true/false)
  - description (human-readable explanation)
- Return ToolResult for each tool invocation containing:
  - success: boolean
  - data: result object (on success)
  - error: error message (on failure)
- Register all 5 tools with MCPServer instance
- Support both stdio and HTTP transport protocols
- Handle concurrent requests without state conflicts

**Acceptance Criteria**:

- Server passes MCP protocol conformance tests
- Tools are discoverable via MCP tool listing
- Parameters are properly validated before execution
- Errors are returned in MCP-compliant format
- Multiple concurrent requests don't interfere

### FR-007: Stateless Design

The MCP server shall:

- Maintain zero in-memory state between requests
- Store all task data in PostgreSQL database
- Use database transactions for all data modifications
- Not cache user data, task data, or session information
- Support horizontal scaling across multiple server instances
- Use app/database.py get_session() for all database access
- Close database sessions after each request
- Handle database connection pooling through existing infrastructure

**Acceptance Criteria**:

- Server can be restarted without data loss
- Multiple server instances can run concurrently
- Each request is independent (no session state)
- Database is single source of truth
- Connection pooling prevents resource exhaustion

### FR-008: Error Handling & Validation

The MCP server shall:

- Validate all input parameters before database operations
- Return descriptive error messages for validation failures
- Use HTTP status code equivalents in MCP error responses:
  - 400 (Bad Request) for validation errors
  - 404 (Not Found) for missing resources
  - 403 (Forbidden) for permission errors
  - 500 (Internal Server Error) for unexpected errors
- Log errors with sufficient context for debugging
- Never expose internal error details (stack traces, SQL) to clients
- Handle database connection failures gracefully
- Retry database operations once on transient failures
- Validate UUID format using standard UUID validation
- Validate string lengths before database insertion

**Acceptance Criteria**:

- Invalid UUIDs return clear error messages
- Missing required parameters return validation errors
- Ownership violations return permission errors
- Database errors don't crash the server
- Error messages are user-friendly and actionable
- Internal details are not leaked to clients

### FR-009: Type Safety & Async Support

The MCP server shall:

- Use Pydantic models for all input validation
- Define Pydantic BaseModel subclasses for:
  - AddTaskInput (user_id, title, description)
  - ListTasksInput (user_id, status)
  - CompleteTaskInput (user_id, task_id)
  - DeleteTaskInput (user_id, task_id)
  - UpdateTaskInput (user_id, task_id, title, description)
- Define Pydantic models for outputs:
  - TaskResponse (task_id, status, title)
  - TaskListResponse (tasks: List[TaskDetail])
- Use Python type hints for all function signatures
- Implement all tools as async functions (async def)
- Use asyncio-compatible database drivers
- Support concurrent tool invocations
- Handle async exceptions properly

**Acceptance Criteria**:

- All inputs validated against Pydantic schemas
- Invalid data types trigger validation errors
- Type hints enable IDE autocomplete and type checking
- Tools can be invoked concurrently
- Async exceptions are caught and handled

### FR-010: Integration with Existing Codebase

The MCP server shall:

- Import Task model from app/models/task.py
- Import User model from app/models/user.py (for validation)
- Use app/database.py get_session() for database sessions
- Use SQLModel query patterns consistent with existing code
- Not duplicate CRUD logic (use existing patterns)
- Follow existing error handling conventions
- Use same database connection pool configuration
- Import UUID utilities from existing codebase
- Maintain consistency with existing timestamp handling

**Acceptance Criteria**:

- No code duplication with existing CRUD operations
- Database queries use same SQLModel patterns
- Error handling matches existing REST API conventions
- Timestamps use same datetime.utcnow() pattern
- Code passes existing linter/type checker rules

## Success Criteria

### SC-001: Tool Functionality

All 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) successfully create, retrieve, modify, and delete tasks in the database with 100% success rate for valid inputs.

**Measurement**: Automated test suite with 50+ test cases covering all tools and edge cases, achieving 100% pass rate.

### SC-002: Performance

- add_task completes within 500ms for 95% of requests
- list_tasks completes within 300ms for 95% of requests (up to 1000 tasks)
- complete_task completes within 400ms for 95% of requests
- delete_task completes within 400ms for 95% of requests
- update_task completes within 400ms for 95% of requests

**Measurement**: Performance test suite recording P95 latency for each tool under normal load.

### SC-003: Error Handling

All error scenarios return appropriate MCP error responses with descriptive messages, achieving zero server crashes during error conditions.

**Measurement**: Error scenario test suite covering 20+ error cases (invalid UUIDs, missing tasks, permission errors, database failures) with 100% proper error response rate.

### SC-004: MCP Protocol Compliance

Server passes official MCP conformance test suite with 100% test pass rate.

**Measurement**: Run MCP conformance tests and verify all protocol requirements are met.

### SC-005: Statelessness

Server can be restarted or replaced without any data loss or state corruption. Multiple server instances can run concurrently without conflicts.

**Measurement**: Restart test that verifies all data persists across server restarts. Concurrency test running 3 server instances simultaneously with 100% data consistency.

### SC-006: Type Safety

All code passes Python type checker (mypy) with zero type errors in strict mode.

**Measurement**: Run `mypy --strict` on MCP server codebase with 100% success.

### SC-007: Integration Quality

MCP server integrates with existing codebase without code duplication, using existing models, database sessions, and patterns.

**Measurement**: Code review checklist verifying imports from existing modules, no duplicated CRUD logic, and consistent patterns across codebase.

## Key Entities

### TaskDetail (Output Model)

Represents a complete task object returned by list_tasks:

- **task_id**: UUID - Unique identifier
- **title**: String - Task title (max 200 chars)
- **description**: String or null - Optional description (max 1000 chars)
- **status**: String - Either "pending" or "completed"
- **created_at**: ISO 8601 timestamp - When task was created
- **updated_at**: ISO 8601 timestamp - When task was last modified

### TaskResponse (Output Model)

Represents a brief task response returned by add_task, complete_task, delete_task, update_task:

- **task_id**: UUID - Unique identifier
- **status**: String - Current task status ("pending", "completed", or "deleted")
- **title**: String - Task title

### AddTaskInput (Input Model)

Parameters for creating a new task:

- **user_id**: UUID - Owner of the task (required)
- **title**: String - Task title, 1-200 characters (required)
- **description**: String - Task description, max 1000 characters (optional)

### ListTasksInput (Input Model)

Parameters for listing tasks:

- **user_id**: UUID - Owner whose tasks to retrieve (required)
- **status**: String - Filter: "all", "pending", or "completed" (optional, default: "all")

### TaskOperationInput (Input Model)

Parameters for complete_task, delete_task:

- **user_id**: UUID - Owner of the task (required)
- **task_id**: UUID - Task to operate on (required)

### UpdateTaskInput (Input Model)

Parameters for updating a task:

- **user_id**: UUID - Owner of the task (required)
- **task_id**: UUID - Task to update (required)
- **title**: String - New title, 1-200 characters (optional)
- **description**: String - New description, max 1000 characters (optional)

Note: At least one of title or description must be provided.

## Assumptions

1. **MCP SDK Availability**: The official MCP SDK (mcp-sdk) is available as a Python package and provides the necessary base classes (Tool, ToolParameter, ToolResult, MCPServer).

2. **Database Schema**: The existing tasks table schema (from models/task.py) includes:
   - id (UUID primary key)
   - user_id (UUID foreign key)
   - title (string, max 200)
   - description (string, max 1000, nullable)
   - completed (boolean, default False)
   - created_at (timestamp)
   - updated_at (timestamp)

3. **Authentication**: User authentication is handled externally (by the client or transport layer). The MCP server receives authenticated user_id values and trusts them. The server validates ownership but does not perform authentication.

4. **Transport Protocol**: The MCP server will support stdio transport initially. HTTP transport support is optional and can be added later if needed.

5. **Concurrency**: The server will handle concurrent requests using async/await, relying on database connection pooling to manage concurrent database access.

6. **Error Recovery**: Database transient errors (connection timeouts, deadlocks) will trigger one automatic retry. Persistent failures will return errors to the client.

7. **Status Values**: Task status is derived from the completed boolean field:
   - completed = False → status = "pending"
   - completed = True → status = "completed"
   - deleted task → status = "deleted" (only in deletion response)

8. **Timestamp Format**: All timestamps will be returned in ISO 8601 format (e.g., "2026-01-17T14:30:00Z") for maximum compatibility with MCP clients.

9. **UUID Format**: All UUIDs will be validated using standard UUID format (8-4-4-4-12 hexadecimal with hyphens). Both uppercase and lowercase are accepted.

10. **Deployment**: The MCP server will run as a separate process/service from the FastAPI REST API, potentially using a different port or stdio-based communication.

## Dependencies

### Internal Dependencies

- **app/models/task.py**: Task SQLModel definition
- **app/models/user.py**: User SQLModel definition (for validation)
- **app/database.py**: Database connection and session management (get_session function)
- **Existing database**: PostgreSQL with tasks and users tables

### External Dependencies

- **mcp-sdk**: Official Model Context Protocol SDK for Python
- **pydantic**: Data validation and settings management (already in project)
- **sqlmodel**: Database ORM (already in project)
- **asyncio**: Async/await support (Python standard library)
- **uuid**: UUID validation (Python standard library)

## Out of Scope

The following are explicitly excluded from this feature:

1. **User Authentication**: The MCP server does not implement authentication. It assumes user_id values are provided by an authenticated source.

2. **REST API Endpoints**: This feature only implements MCP tools. The existing REST API endpoints remain separate.

3. **Task Sharing**: Multi-user task sharing or collaboration features are not included.

4. **Task Categories/Tags**: Task categorization, tagging, or folder organization is not part of this feature.

5. **Due Dates/Reminders**: Task scheduling, due dates, or reminder functionality is excluded.

6. **Bulk Operations**: Batch operations (e.g., complete multiple tasks at once) are not included.

7. **Search Functionality**: Full-text search or advanced filtering beyond status is out of scope.

8. **Task History/Audit**: Tracking task change history or audit logs is not included.

9. **WebSocket/Real-time**: Real-time task updates or WebSocket support is not part of this feature.

10. **UI Components**: No user interface changes or components are included. This is a backend-only feature.

11. **Rate Limiting**: Request rate limiting or throttling is not implemented in the MCP server (assumed to be handled at transport/gateway level).

12. **Caching**: No caching layer is implemented. All requests query the database directly.

## Risks & Mitigation

### Risk 1: MCP SDK Maturity

**Risk**: The official MCP SDK may be in early stages or have limited documentation.

**Impact**: Development delays, unexpected API changes, or missing features.

**Mitigation**:

- Research MCP SDK thoroughly before implementation
- Have fallback plan to implement MCP protocol directly if SDK is insufficient
- Start with minimal SDK usage and expand incrementally
- Monitor SDK repository for updates and breaking changes

### Risk 2: Performance Under Load

**Risk**: Database queries for each tool call may cause performance bottlenecks under high concurrency.

**Impact**: Slow response times, timeout errors, poor user experience.

**Mitigation**:

- Use database connection pooling (already configured)
- Implement async/await to prevent blocking
- Add database indexes on user_id and task_id (already exist)
- Monitor query performance and optimize if needed
- Consider read replicas for list_tasks if needed

### Risk 3: State Management Confusion

**Risk**: Developers may accidentally introduce stateful behavior (caching, session storage) that breaks stateless design.

**Impact**: Bugs with multiple server instances, data inconsistency.

**Mitigation**:

- Clear documentation emphasizing stateless requirement
- Code review checklist to verify no in-memory state
- Integration tests running multiple server instances
- Automated tests verifying data persists across restarts

### Risk 4: Error Handling Gaps

**Risk**: Unforeseen edge cases may cause unhandled exceptions or cryptic error messages.

**Impact**: Server crashes, poor debugging experience, user frustration.

**Mitigation**:

- Comprehensive error scenario testing
- Global exception handler to catch unexpected errors
- Detailed logging for all error paths
- User-friendly error messages with actionable guidance

### Risk 5: Breaking Changes to Database Schema

**Risk**: Future changes to Task model or database schema may break MCP server.

**Impact**: MCP tools stop working, data corruption.

**Mitigation**:

- Use existing Task model (don't create parallel schema)
- Add integration tests that verify model compatibility
- Document dependency on Task model schema
- Version MCP server alongside database migrations

## Future Enhancements

Potential improvements for future iterations (not part of this feature):

1. **Batch Operations**: Tools for bulk task creation, completion, or deletion
2. **Advanced Filtering**: Search by title, filter by date range, sort options
3. **Task Statistics**: Tool to retrieve task counts, completion rates, productivity metrics
4. **Recurring Tasks**: Support for tasks that repeat on a schedule
5. **Task Priorities**: Add priority levels (high, medium, low) to tasks
6. **Task Labels/Tags**: Categorization and organization features
7. **Task Subtasks**: Hierarchical task structures with parent-child relationships
8. **Task Sharing**: Multi-user collaboration and task delegation
9. **Webhook Support**: Notifications when tasks are created, completed, or deleted
10. **GraphQL Interface**: Alternative to MCP for more flexible querying
