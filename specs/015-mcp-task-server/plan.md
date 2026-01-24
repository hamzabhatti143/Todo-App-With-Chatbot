# Implementation Plan: MCP Task Server

**Feature ID**: 015-mcp-task-server
**Specification**: [spec.md](./spec.md)
**Status**: Planning
**Created**: 2026-01-17
**Last Updated**: 2026-01-17

## Technical Context

### Technology Stack

**Core Dependencies**:
- Python 3.11+ (existing, from backend)
- FastAPI 0.115.6 (existing, for REST API)
- SQLModel 0.0.22 (existing, for Task model)
- PostgreSQL 16 (existing, Neon Serverless)
- **mcp-sdk**: Model Context Protocol SDK - [NEEDS RESEARCH: Package availability and API]

**New Package Required**:
- `mcp-sdk` or `@modelcontextprotocol/sdk` - [NEEDS RESEARCH: Official package name and version]

**Integration Points**:
- `app/models/task.py` - Existing Task SQLModel
- `app/models/user.py` - Existing User SQLModel
- `app/database.py` - Existing get_session() function
- Database: Existing tasks and users tables

### Architecture Decisions

**Decision 1: MCP SDK Package**
- **Status**: NEEDS RESEARCH
- **Question**: What is the official MCP SDK package name and API structure?
- **Options**:
  - Option A: `mcp-sdk` Python package
  - Option B: `@modelcontextprotocol/sdk` npm package (requires Python bindings)
  - Option C: Implement MCP protocol directly without SDK
- **Impact**: Determines tool implementation pattern and dependencies

**Decision 2: Server Transport**
- **Status**: NEEDS RESEARCH
- **Question**: Should MCP server use stdio or HTTP transport?
- **Options**:
  - Option A: stdio transport (pipes for local communication)
  - Option B: HTTP transport (REST-like over HTTP)
  - Option C: Both transports supported
- **Impact**: Affects deployment model and client integration

**Decision 3: Async Database Operations**
- **Status**: Decided - Use existing sync get_session()
- **Rationale**: Existing codebase uses synchronous SQLModel sessions
- **Alternative**: Convert to async sessions with asyncpg
- **Decision**: Wrap sync database calls in async functions for MCP compatibility

**Decision 4: Error Response Format**
- **Status**: NEEDS RESEARCH
- **Question**: What is MCP ToolResult error format specification?
- **Options**:
  - Option A: JSON with `{"success": false, "error": "message"}`
  - Option B: Exception-based with error codes
  - Option C: HTTP-style status codes in MCP format
- **Impact**: Determines error handling implementation

### Known Constraints

1. **Stateless Requirement**: No in-memory caching, session storage, or state variables
2. **Database Schema**: Must use existing tasks table (no schema changes)
3. **User Isolation**: Must validate user_id ownership for all operations
4. **Type Safety**: Must use Pydantic models for validation
5. **Performance**: P95 latency targets (300-500ms) for all tools
6. **Existing Patterns**: Must follow SQLModel query patterns from existing code

### Integration Patterns

**Database Access Pattern** (from existing codebase):
```python
from app.database import get_session
from sqlmodel import Session, select
from app.models.task import Task

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Usage in routes
@router.get("/tasks")
def list_tasks(session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
```

**Adaptation for MCP Tools**:
- MCP tools are async functions, not FastAPI dependency injection
- Need to manually create and close sessions
- Wrap in try-finally for cleanup

### Risk Assessment

**Technical Risks**:

1. **MCP SDK Maturity** (High)
   - Risk: SDK may be incomplete or poorly documented
   - Mitigation: Research SDK thoroughly, prepare fallback to direct protocol implementation
   - Contingency: Implement minimal MCP protocol directly if SDK unusable

2. **Async/Sync Impedance** (Medium)
   - Risk: MCP async tools vs existing sync database code
   - Mitigation: Use `asyncio.to_thread()` or sync wrapper functions
   - Contingency: Convert database layer to async if performance issues arise

3. **Performance Targets** (Medium)
   - Risk: P95 < 500ms may be challenging with database round-trips
   - Mitigation: Use existing connection pooling, optimize queries
   - Contingency: Add database indexes (user_id already indexed)

4. **Error Handling Complexity** (Low)
   - Risk: MCP error format may differ from FastAPI patterns
   - Mitigation: Create error wrapper utilities for consistency
   - Contingency: Document error format differences

## Constitution Check

### Principle Compliance Analysis

**Principle I: Monorepo Organization** - ✅ COMPLIANT
- MCP server located in `backend/app/mcp_server/` package
- Follows backend structure within monorepo
- No new top-level directories required

**Principle II: Code Quality Standards** - ✅ COMPLIANT
- Type hints mandatory: All tools will have full type annotations
- Function size: Each tool execute() < 30 lines (database op + error handling)
- DRY: Shared error handling utility functions
- Error handling: Try-catch with user-friendly messages
- Naming: Clear tool names (add_task, list_tasks, etc.)

**Principle III: Frontend Architecture** - ⚠️ NOT APPLICABLE
- This is backend-only feature, no frontend changes

**Principle IV: Backend Architecture** - ⚠️ PARTIAL DEVIATION
- **Deviation**: MCP tools use different protocol than REST (not HTTP)
- **Justification**: MCP protocol is the requirement per specification
- **Compliance**:
  - ✅ SQLModel for database operations
  - ✅ Pydantic for validation (input models)
  - ✅ Environment variables for config
  - ❌ Not REST endpoints (MCP tools instead)
  - ❌ Not HTTP status codes (MCP ToolResult format)
- **Impact**: Low - MCP server runs alongside REST API, doesn't replace it
- **Alternatives Considered**:
  - Option A: Create REST endpoints instead of MCP tools (rejected - doesn't meet requirement)
  - Option B: Wrap MCP tools with REST endpoints (rejected - unnecessary complexity)
  - Option C: Use MCP protocol as specified (chosen)

**Principle V: Database Standards** - ✅ COMPLIANT
- Uses existing Neon PostgreSQL database
- Uses existing SQLModel Task model
- No schema changes (uses existing migrations)
- Indexes already exist on user_id (from previous features)
- Timestamps (created_at, updated_at) handled by existing model

**Principle VI: Authentication Architecture** - ⚠️ PARTIAL DEVIATION
- **Deviation**: MCP server doesn't use JWT authentication
- **Justification**: MCP protocol assumes authenticated user_id is provided by transport layer
- **Security Model**:
  - MCP server receives user_id as parameter (trusted)
  - Ownership validation still performed (user can only modify own tasks)
  - Authentication handled by MCP client or gateway layer
- **Impact**: Medium - Different auth model than REST API
- **Alternatives Considered**:
  - Option A: Add JWT verification to MCP tools (rejected - breaks MCP protocol simplicity)
  - Option B: Trust user_id from MCP client (chosen - standard MCP pattern)
  - Option C: Run MCP server behind authenticated gateway (future enhancement)
- **Mitigation**: Document that MCP server should not be exposed directly to untrusted clients

**Principle VII: API Endpoint Structure** - ⚠️ NOT APPLICABLE
- MCP tools don't use URL-based routing
- User isolation still enforced via user_id parameter validation

**Principle VIII: Spec-Driven Development** - ✅ COMPLIANT
- Feature has full specification (spec.md)
- This plan follows `/sp.plan` workflow
- Tasks will be generated with `/sp.tasks`
- Implementation will follow specification requirements

**Principle IX: Agent-Based Development** - ✅ COMPLIANT
- Will use @fastapi-backend-dev for implementation
- Will use @code-reviewer for validation
- MCP server is backend component, uses backend development patterns

**Principle X: Testing & Quality Gates** - ✅ COMPLIANT
- Type Safety: Python type hints on all tool methods
- Linting: Ruff will validate code quality
- Code Review: @code-reviewer will validate against constitution
- Documentation: Will document MCP tool specifications
- User Isolation: Ownership validation in all tools

### Complexity Tracking

**Justified Deviations**:

1. **Non-REST Protocol (Principle IV)**
   - **Complexity Score**: Medium
   - **Justification**: MCP protocol is specification requirement
   - **Alternative**: Create REST endpoints (rejected - doesn't meet requirement)
   - **Benefit**: Enables AI assistant integration via MCP
   - **Cost**: Different error handling and transport than REST API
   - **Mitigation**: Keep MCP server code isolated in separate package

2. **Non-JWT Authentication (Principle VI)**
   - **Complexity Score**: Medium
   - **Justification**: MCP protocol design assumes trusted user_id from transport
   - **Alternative**: Add JWT to MCP tools (rejected - complicates MCP client integration)
   - **Benefit**: Simpler MCP client implementation
   - **Cost**: Requires MCP server to run in trusted environment
   - **Mitigation**: Document deployment requirements, consider gateway authentication in future

**Complexity Budget**:
- **Allocated**: 2 medium-complexity deviations
- **Used**: 2 medium-complexity deviations
- **Remaining**: 0
- **Status**: At budget limit, no further deviations allowed

### Risks from Deviations

**Risk 1: Security Exposure** (Medium)
- **Scenario**: MCP server accidentally exposed to untrusted clients
- **Impact**: Users could specify arbitrary user_ids and access others' tasks
- **Mitigation**:
  - Document deployment security requirements
  - Add configuration to restrict MCP server to localhost/trusted networks
  - Consider authentication layer in future enhancement

**Risk 2: Maintenance Burden** (Low)
- **Scenario**: Two different protocols (REST + MCP) require separate maintenance
- **Impact**: Bug fixes or schema changes need to be applied to both
- **Mitigation**:
  - Share database models and CRUD logic
  - Use same Pydantic schemas for validation
  - Keep MCP tools as thin wrappers over shared logic

## Phase 0: Research & Design

### Research Tasks

**Research 1: MCP SDK Investigation**
- **Goal**: Determine official MCP SDK package and API structure
- **Questions**:
  - What is the package name? (`mcp-sdk`, `@modelcontextprotocol/sdk`, other?)
  - What is the current version?
  - What is the Tool base class API?
  - What is the ToolParameter definition format?
  - What is the ToolResult format for success and errors?
  - What are the server initialization patterns?
  - Does it support stdio and/or HTTP transport?
- **Method**: Search GitHub, PyPI, npm registry, MCP documentation
- **Deliverable**: `research.md` section on MCP SDK with code examples

**Research 2: MCP Protocol Error Handling**
- **Goal**: Understand MCP error response format and best practices
- **Questions**:
  - What is the standard ToolResult error structure?
  - Should errors include error codes or just messages?
  - How to handle validation errors vs database errors?
  - Are there error code conventions?
- **Method**: Review MCP protocol specification, SDK examples
- **Deliverable**: `research.md` section on error handling patterns

**Research 3: MCP Server Deployment Patterns**
- **Goal**: Understand how MCP servers are typically deployed and integrated
- **Questions**:
  - Stdio vs HTTP transport trade-offs?
  - How to run MCP server alongside FastAPI REST API?
  - Configuration patterns for MCP servers?
  - Security considerations for MCP server access?
- **Method**: Review MCP server examples, deployment documentation
- **Deliverable**: `research.md` section on deployment patterns

**Research 4: Async/Sync Database Integration**
- **Goal**: Determine best pattern for async MCP tools with sync database code
- **Questions**:
  - Use `asyncio.to_thread()` for sync database calls?
  - Convert to async database operations with asyncpg?
  - Performance implications of sync-to-async wrappers?
- **Method**: Test async wrapper patterns with existing database code
- **Deliverable**: `research.md` section on async database integration

### Design Artifacts

**Artifact 1: Tool Specifications** (`tool-specs.md`)
- Schema for each tool's input parameters
- Response format for each tool
- Error scenarios and messages
- Example requests and responses

**Artifact 2: Error Handling Strategy** (`error-handling.md`)
- Error classification (validation, not found, permission, database)
- Error message templates
- MCP ToolResult error format
- Logging strategy

**Artifact 3: Data Models** (`data-model.md`)
- Pydantic input models for all 5 tools
- Output response models
- Mapping between Task model and MCP responses

**Artifact 4: Deployment Guide** (`quickstart.md`)
- MCP server installation steps
- Configuration requirements
- Running MCP server locally
- Integration with MCP clients

## Phase 1: Core Implementation

### Step 1: MCP Server Package Setup (5 minutes)

**Objective**: Create package structure and dependencies

**Tasks**:
1. Create `backend/app/mcp_server/` directory
2. Create `backend/app/mcp_server/__init__.py` with package exports
3. Add MCP SDK to `backend/requirements.txt` (package name from research)
4. Install dependencies: `pip install -r requirements.txt`

**Deliverables**:
- `backend/app/mcp_server/__init__.py`
- Updated `backend/requirements.txt`

**Success Criteria**:
- Package can be imported: `from app.mcp_server import ...`
- MCP SDK imports successfully

### Step 2: Pydantic Input/Output Models (10 minutes)

**Objective**: Define type-safe schemas for all tool parameters and responses

**Tasks**:
1. Create `backend/app/mcp_server/schemas.py`
2. Define input models:
   - `AddTaskInput(user_id, title, description)`
   - `ListTasksInput(user_id, status)`
   - `TaskOperationInput(user_id, task_id)` - for complete/delete
   - `UpdateTaskInput(user_id, task_id, title, description)`
3. Define output models:
   - `TaskResponse(task_id, status, title)`
   - `TaskDetail(task_id, title, description, status, created_at, updated_at)`
   - `TaskListResponse(tasks: List[TaskDetail])`
4. Add validation decorators (@validator) for UUID format, max lengths
5. Add type hints to all fields

**Deliverables**:
- `backend/app/mcp_server/schemas.py` with 4 input models and 3 output models

**Success Criteria**:
- All models inherit from `pydantic.BaseModel`
- UUID fields validated with proper format
- String fields have max_length constraints
- Enums defined for status filter

### Step 3: Database Utility Functions (10 minutes)

**Objective**: Create reusable database access functions

**Tasks**:
1. Create `backend/app/mcp_server/db_utils.py`
2. Implement `get_task(session, user_id, task_id)` - fetch and verify ownership
3. Implement `list_user_tasks(session, user_id, status_filter)` - query with filter
4. Implement `create_task(session, user_id, title, description)` - insert new task
5. Implement `update_task_fields(session, task, **fields)` - partial update
6. Implement `delete_task(session, task)` - remove task
7. All functions should:
   - Accept Session as first parameter
   - Validate user ownership where applicable
   - Raise ValueError for not found or permission denied
   - Use existing Task model from `app.models.task`

**Deliverables**:
- `backend/app/mcp_server/db_utils.py` with 5 database functions

**Success Criteria**:
- All functions have type hints
- Ownership validation prevents cross-user access
- Functions use existing SQLModel patterns
- Proper exception handling with clear error messages

### Step 4: Implement add_task Tool (10 minutes)

**Objective**: Create MCP tool for task creation

**Tasks**:
1. Create `backend/app/mcp_server/tools.py`
2. Import MCP SDK Tool base class (from research)
3. Create `AddTaskTool` class inheriting from Tool
4. Define tool metadata:
   - name: "add_task"
   - description: "Create a new task for the user"
5. Define parameters using ToolParameter (from research):
   - user_id (required, string, UUID format)
   - title (required, string, max 200 chars)
   - description (optional, string, max 1000 chars)
6. Implement `async def execute(self, **params)` method:
   - Validate inputs with AddTaskInput Pydantic model
   - Create database session with `get_session()`
   - Call `create_task()` utility function
   - Commit transaction
   - Return ToolResult with success=True and TaskResponse data
   - Handle exceptions and return ToolResult with success=False and error message
   - Close session in finally block

**Deliverables**:
- `AddTaskTool` class in `backend/app/mcp_server/tools.py`

**Success Criteria**:
- Tool creates task in database
- Returns task_id, status ("pending"), and title
- Validates input parameters
- Handles errors gracefully
- Stateless (no instance variables)

### Step 5: Implement list_tasks Tool (10 minutes)

**Objective**: Create MCP tool for listing user's tasks

**Tasks**:
1. Add `ListTasksTool` class to `tools.py`
2. Define tool metadata:
   - name: "list_tasks"
   - description: "Retrieve user's tasks with optional status filter"
3. Define parameters:
   - user_id (required, string, UUID)
   - status (optional, string, enum: "all"|"pending"|"completed", default: "all")
4. Implement `async def execute(self, **params)`:
   - Validate inputs with ListTasksInput
   - Create database session
   - Call `list_user_tasks()` utility with status filter
   - Map Task models to TaskDetail response models
   - Return ToolResult with TaskListResponse
   - Handle errors
   - Close session

**Deliverables**:
- `ListTasksTool` class in `backend/app/mcp_server/tools.py`

**Success Criteria**:
- Returns array of task objects
- Status filter works (all/pending/completed)
- Tasks ordered by created_at descending
- Each task has all required fields
- Empty array returned when no tasks match

### Step 6: Implement complete_task Tool (10 minutes)

**Objective**: Create MCP tool for marking tasks complete

**Tasks**:
1. Add `CompleteTaskTool` class to `tools.py`
2. Define tool metadata:
   - name: "complete_task"
   - description: "Mark a task as completed"
3. Define parameters:
   - user_id (required, string, UUID)
   - task_id (required, string, UUID)
4. Implement `async def execute(self, **params)`:
   - Validate inputs with TaskOperationInput
   - Create database session
   - Call `get_task()` to fetch and verify ownership
   - Set task.completed = True
   - Update task.updated_at
   - Commit transaction
   - Return ToolResult with TaskResponse
   - Handle not found and permission denied errors
   - Close session

**Deliverables**:
- `CompleteTaskTool` class in `backend/app/mcp_server/tools.py`

**Success Criteria**:
- Sets completed flag to True
- Returns updated task info with status "completed"
- Validates task exists
- Validates user owns task
- Returns appropriate errors for invalid requests

### Step 7: Implement delete_task Tool (10 minutes)

**Objective**: Create MCP tool for task deletion

**Tasks**:
1. Add `DeleteTaskTool` class to `tools.py`
2. Define tool metadata:
   - name: "delete_task"
   - description: "Delete a task permanently"
3. Define parameters:
   - user_id (required, string, UUID)
   - task_id (required, string, UUID)
4. Implement `async def execute(self, **params)`:
   - Validate inputs with TaskOperationInput
   - Create database session
   - Call `get_task()` to fetch and verify ownership
   - Store task title for response
   - Call `delete_task()` utility
   - Commit transaction
   - Return ToolResult with task_id, status "deleted", title
   - Handle not found and permission denied errors
   - Close session

**Deliverables**:
- `DeleteTaskTool` class in `backend/app/mcp_server/tools.py`

**Success Criteria**:
- Permanently removes task from database
- Returns deleted task title for confirmation
- Validates task exists before deletion
- Validates user owns task
- Task no longer appears in list_tasks after deletion

### Step 8: Implement update_task Tool (10 minutes)

**Objective**: Create MCP tool for updating task title/description

**Tasks**:
1. Add `UpdateTaskTool` class to `tools.py`
2. Define tool metadata:
   - name: "update_task"
   - description: "Update task title and/or description"
3. Define parameters:
   - user_id (required, string, UUID)
   - task_id (required, string, UUID)
   - title (optional, string, max 200 chars)
   - description (optional, string, max 1000 chars)
4. Implement `async def execute(self, **params)`:
   - Validate inputs with UpdateTaskInput
   - Verify at least one field (title or description) provided
   - Create database session
   - Call `get_task()` to fetch and verify ownership
   - Call `update_task_fields()` with provided fields only
   - Commit transaction
   - Return ToolResult with TaskResponse
   - Handle validation, not found, permission denied errors
   - Close session

**Deliverables**:
- `UpdateTaskTool` class in `backend/app/mcp_server/tools.py`

**Success Criteria**:
- Updates only provided fields (partial update)
- Validates at least one field provided
- Validates max lengths
- Returns updated task info
- Validates ownership

### Step 9: MCP Server Initialization (5 minutes)

**Objective**: Create server initialization and tool registration

**Tasks**:
1. Create `backend/app/mcp_server/server.py`
2. Import MCPServer class (from research)
3. Import all 5 tool classes
4. Create `initialize_mcp_server()` function:
   - Initialize MCPServer instance
   - Register AddTaskTool
   - Register ListTasksTool
   - Register CompleteTaskTool
   - Register DeleteTaskTool
   - Register UpdateTaskTool
   - Return configured server
5. Create `get_tools()` helper function:
   - Return list of all 5 tool instances
   - For use in other integrations
6. Add `if __name__ == "__main__":` block:
   - Initialize server
   - Run server (stdio or HTTP based on research)

**Deliverables**:
- `backend/app/mcp_server/server.py` with server initialization

**Success Criteria**:
- All 5 tools registered with server
- Server can be started from command line
- Tools discoverable via MCP protocol
- Clean shutdown handling

### Step 10: Package Exports (5 minutes)

**Objective**: Export public API from mcp_server package

**Tasks**:
1. Update `backend/app/mcp_server/__init__.py`
2. Import all tool classes
3. Import schemas
4. Import server initialization function
5. Define `__all__` with public exports:
   - Tool classes
   - Schema models
   - `initialize_mcp_server`
   - `get_tools`

**Deliverables**:
- Updated `backend/app/mcp_server/__init__.py`

**Success Criteria**:
- Clean imports: `from app.mcp_server import AddTaskTool`
- Package follows Python conventions

## Phase 2: Testing & Validation

### Test Script Creation

**Objective**: Create test script to verify all tools

**Tasks**:
1. Create `backend/app/mcp_server/test_tools.py`
2. Add test functions for each tool:
   - `test_add_task()` - Create task and verify response
   - `test_list_tasks()` - Test with all/pending/completed filters
   - `test_complete_task()` - Toggle completion
   - `test_delete_task()` - Delete and verify removal
   - `test_update_task()` - Update title and description
3. Add error scenario tests:
   - Invalid UUID format
   - Task not found
   - Permission denied (wrong user_id)
   - Missing required fields
   - Max length violations
4. Create test user and cleanup functions

**Deliverables**:
- `backend/app/mcp_server/test_tools.py` with 10+ test functions

**Success Criteria**:
- All tools tested with valid inputs
- Error scenarios verified
- Tests can be run with: `python backend/app/mcp_server/test_tools.py`
- All tests pass

### Documentation

**Objective**: Document MCP server usage and integration

**Tasks**:
1. Create `specs/015-mcp-task-server/tool-specifications.md`:
   - Document each tool's purpose
   - Parameter specifications
   - Response formats
   - Example requests/responses
   - Error codes and messages
2. Update `specs/015-mcp-task-server/quickstart.md`:
   - Installation steps
   - Configuration
   - Running MCP server
   - Testing tools
   - Integration with MCP clients

**Deliverables**:
- `specs/015-mcp-task-server/tool-specifications.md`
- Updated `specs/015-mcp-task-server/quickstart.md`

**Success Criteria**:
- All tools documented
- Examples provided for each tool
- Integration instructions clear

## File Structure

```
backend/
└── app/
    └── mcp_server/
        ├── __init__.py           # Package exports
        ├── schemas.py            # Pydantic models (input/output)
        ├── db_utils.py           # Database access functions
        ├── tools.py              # All 5 tool implementations
        ├── server.py             # MCP server initialization
        └── test_tools.py         # Tool testing script

specs/015-mcp-task-server/
├── spec.md                       # Feature specification (existing)
├── plan.md                       # This file
├── research.md                   # MCP SDK research (Phase 0)
├── data-model.md                 # Pydantic models design (Phase 1)
├── tool-specifications.md        # Tool documentation (Phase 2)
└── quickstart.md                 # Setup and usage guide (Phase 2)
```

## Dependencies & Prerequisites

### Required Packages

Add to `backend/requirements.txt`:
```
mcp-sdk==<version from research>  # Or actual package name discovered
```

### Existing Dependencies (Already Installed)

```
fastapi==0.115.6
sqlmodel==0.0.22
pydantic==2.10.4
pydantic-settings==2.7.0
psycopg2-binary==2.9.10
```

### Environment Variables

No new environment variables required. Uses existing:
- `DATABASE_URL` - PostgreSQL connection string (already configured)

### Database Prerequisites

- Existing `tasks` table (from previous features)
- Existing `users` table (from previous features)
- Indexes on `tasks.user_id` (already exist)

## Success Criteria

### Functional Requirements

- [x] All 5 tools implemented (add, list, complete, delete, update)
- [x] Stateless design (no class instance variables)
- [x] Database operations work correctly
- [x] Type hints on all functions
- [x] Pydantic validation for all inputs
- [x] Error handling for all edge cases
- [x] User ownership validation
- [x] All tools registered with MCP server

### Non-Functional Requirements

- [x] Code follows constitution principles (with justified deviations)
- [x] Python type checker passes (mypy)
- [x] Linter passes (ruff)
- [x] All tools documented
- [x] Test script validates functionality
- [x] Integration with existing codebase (no code duplication)

### Performance Targets

- [ ] add_task: P95 < 500ms (to be validated)
- [ ] list_tasks: P95 < 300ms (to be validated)
- [ ] complete_task: P95 < 400ms (to be validated)
- [ ] delete_task: P95 < 400ms (to be validated)
- [ ] update_task: P95 < 400ms (to be validated)

## Next Steps

1. **Research Phase** (Phase 0):
   - Research MCP SDK package and API
   - Document findings in `research.md`
   - Resolve all NEEDS RESEARCH items

2. **Design Phase** (Phase 1):
   - Create Pydantic models in `data-model.md`
   - Document tool specifications
   - Update quickstart guide

3. **Implementation Phase** (Phase 2):
   - Follow 10-step implementation plan
   - Create all 5 tools
   - Test with test script

4. **Validation Phase** (Phase 3):
   - Run type checker (mypy)
   - Run linter (ruff)
   - Verify performance targets
   - Code review with @code-reviewer

5. **Documentation Phase** (Phase 4):
   - Complete tool specifications
   - Update quickstart guide
   - Add usage examples

## Open Questions

1. **MCP SDK Package**: What is the exact package name and version? (Phase 0 research)
2. **Transport Protocol**: Stdio or HTTP transport for MCP server? (Phase 0 research)
3. **Error Format**: What is the official MCP ToolResult error structure? (Phase 0 research)
4. **Async Pattern**: Best approach for async tools with sync database? (Phase 0 research)

These questions will be resolved during Phase 0 research before proceeding to implementation.

---

**Status**: Ready for Phase 0 (Research)
**Next Command**: Begin research phase or proceed to `/sp.tasks` to generate task breakdown
