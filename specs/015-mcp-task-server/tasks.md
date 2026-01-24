# Tasks: MCP Task Server

**Feature**: 015-mcp-task-server
**Input**: Design documents from `/specs/015-mcp-task-server/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story (one per MCP tool) to enable independent implementation and testing.

**Tests**: Not explicitly requested in specification - tests are included as optional validation tasks in final phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Package Infrastructure)

**Purpose**: Initialize MCP server package structure and dependencies

- [ ] T001 Create backend/app/mcp_server/ directory structure
- [ ] T002 Create backend/app/mcp_server/__init__.py (empty, will populate in T021)
- [ ] T003 Add mcp[cli]==1.25.0 to backend/requirements.txt
- [ ] T004 Install dependencies with pip install -r backend/requirements.txt

**Checkpoint**: Package structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY tool can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create Pydantic input schemas in backend/app/mcp_server/schemas.py (AddTaskInput, ListTasksInput, TaskOperationInput, UpdateTaskInput)
- [ ] T006 [P] Create Pydantic output schemas in backend/app/mcp_server/schemas.py (TaskResponse, TaskDetail, TaskListResponse)
- [ ] T007 Create database utility functions in backend/app/mcp_server/db_utils.py (create_task, list_user_tasks, get_task, update_task_fields, delete_task)
- [ ] T008 Create MCP server initialization framework in backend/app/mcp_server/server.py (FastMCP instance, main block)

**Checkpoint**: Foundation ready - tool implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: AI assistant can create new tasks for users via natural language commands

**User Scenario**: User says "Add a task to finish the quarterly report" → AI calls add_task tool → Task created in database → AI confirms creation

**Independent Test**: Call add_task with user_id, title, and description → Verify task appears in database with completed=False → Verify task_id returned

### Implementation for User Story 1

- [ ] T009 [US1] Implement add_task tool in backend/app/mcp_server/tools.py using @mcp.tool() decorator
- [ ] T010 [US1] Add parameter validation using AddTaskInput schema
- [ ] T011 [US1] Implement database session management (create, commit, close)
- [ ] T012 [US1] Call create_task() utility from db_utils.py
- [ ] T013 [US1] Return ToolResult with task_id, status ("pending"), and title
- [ ] T014 [US1] Add error handling for validation errors, database errors

**Checkpoint**: add_task tool functional - can create tasks via MCP

---

## Phase 4: User Story 2 - List Tasks (Priority: P2)

**Goal**: AI assistant can retrieve user's tasks with optional status filtering

**User Scenario**: User asks "What tasks do I have pending?" → AI calls list_tasks with status="pending" → Returns array of incomplete tasks → AI presents formatted list

**Independent Test**: Create 3 tasks (2 pending, 1 completed) → Call list_tasks with status="pending" → Verify only 2 pending tasks returned → Call with status="all" → Verify all 3 returned

### Implementation for User Story 2

- [ ] T015 [US2] Implement list_tasks tool in backend/app/mcp_server/tools.py using @mcp.tool() decorator
- [ ] T016 [US2] Add parameter validation using ListTasksInput schema
- [ ] T017 [US2] Call list_user_tasks() utility with status filter
- [ ] T018 [US2] Map Task SQLModel objects to TaskDetail response models
- [ ] T019 [US2] Return ToolResult with TaskListResponse (array of tasks)
- [ ] T020 [US2] Add error handling for validation errors, empty results

**Checkpoint**: list_tasks tool functional - can query tasks with filtering

---

## Phase 5: User Story 3 - Complete Task (Priority: P3)

**Goal**: AI assistant can mark tasks as completed

**User Scenario**: User says "Mark the quarterly report task as done" → AI identifies task_id → Calls complete_task → Task.completed set to True → AI confirms completion

**Independent Test**: Create pending task → Call complete_task with task_id → Verify completed=True in database → Verify updated_at timestamp changed → Call list_tasks with status="completed" → Verify task appears

### Implementation for User Story 3

- [ ] T021 [US3] Implement complete_task tool in backend/app/mcp_server/tools.py using @mcp.tool() decorator
- [ ] T022 [US3] Add parameter validation using TaskOperationInput schema
- [ ] T023 [US3] Call get_task() utility to fetch and verify ownership
- [ ] T024 [US3] Set task.completed = True and update task.updated_at
- [ ] T025 [US3] Commit transaction and return ToolResult with status "completed"
- [ ] T026 [US3] Add error handling for task not found, permission denied, database errors

**Checkpoint**: complete_task tool functional - can toggle completion status

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: AI assistant can permanently remove tasks

**User Scenario**: User says "Remove the quarterly report task" → AI calls delete_task → Task deleted from database → AI confirms deletion with task title

**Independent Test**: Create task → Call delete_task with task_id → Verify task removed from database → Call list_tasks → Verify task not in results → Call delete_task again with same task_id → Verify "Task not found" error

### Implementation for User Story 4

- [ ] T027 [US4] Implement delete_task tool in backend/app/mcp_server/tools.py using @mcp.tool() decorator
- [ ] T028 [US4] Add parameter validation using TaskOperationInput schema
- [ ] T029 [US4] Call get_task() utility to fetch and verify ownership
- [ ] T030 [US4] Store task.title for response before deletion
- [ ] T031 [US4] Call delete_task() utility and commit transaction
- [ ] T032 [US4] Return ToolResult with status "deleted" and task title
- [ ] T033 [US4] Add error handling for task not found, permission denied, database errors

**Checkpoint**: delete_task tool functional - can remove tasks permanently

---

## Phase 7: User Story 5 - Update Task (Priority: P5)

**Goal**: AI assistant can modify task title and/or description

**User Scenario**: User says "Change the report task description to include Q4 data" → AI calls update_task with new description → Task updated in database → AI confirms update

**Independent Test**: Create task → Call update_task with new title only → Verify title changed, description unchanged → Call update_task with new description only → Verify description changed, title unchanged → Call update_task with both → Verify both changed

### Implementation for User Story 5

- [ ] T034 [US5] Implement update_task tool in backend/app/mcp_server/tools.py using @mcp.tool() decorator
- [ ] T035 [US5] Add parameter validation using UpdateTaskInput schema
- [ ] T036 [US5] Validate at least one field (title or description) provided
- [ ] T037 [US5] Call get_task() utility to fetch and verify ownership
- [ ] T038 [US5] Call update_task_fields() utility with provided fields only (partial update)
- [ ] T039 [US5] Commit transaction and return ToolResult with updated task info
- [ ] T040 [US5] Add error handling for no fields provided, task not found, permission denied, validation errors

**Checkpoint**: update_task tool functional - can modify task fields independently

---

## Phase 8: Integration & Polish

**Purpose**: Complete MCP server integration, validation, and documentation

- [ ] T041 Register all 5 tools with FastMCP instance in backend/app/mcp_server/server.py
- [ ] T042 Update backend/app/mcp_server/__init__.py with public exports (__all__ with tool names, schemas, initialize_mcp_server)
- [ ] T043 Create test script backend/app/mcp_server/test_tools.py with validation for all 5 tools
- [ ] T044 Add error scenario tests to test_tools.py (invalid UUID, task not found, permission denied, max length violations)
- [ ] T045 [P] Update specs/015-mcp-task-server/quickstart.md with actual server startup commands and test examples
- [ ] T046 [P] Create specs/015-mcp-task-server/tool-specifications.md documenting all 5 tools with parameters, responses, examples
- [ ] T047 Run test script and verify all tools pass (python -m app.mcp_server.test_tools)
- [ ] T048 Validate stateless design - restart server between operations and verify data persists

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T004) - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion (T005-T008)
  - User stories can proceed in parallel (if staffed for parallel work)
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5)
- **Integration & Polish (Phase 8)**: Depends on all user stories being complete (T009-T040)

### User Story Dependencies

- **User Story 1 (add_task)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (list_tasks)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (complete_task)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (delete_task)**: Can start after Foundational - No dependencies on other stories
- **User Story 5 (update_task)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- Tool implementation before error handling
- Database operations before response formatting
- All tasks within a story must complete before story checkpoint

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks can run sequentially (short, dependent)

**Phase 2 (Foundational)**:
- T005 and T006 (schemas) can run in parallel [P]
- T007 (db_utils) and T008 (server.py) can run in parallel [P] after schemas complete

**Phase 3-7 (User Stories)**:
- Once Foundational completes, ALL user stories (US1-US5) can start in parallel
- Different team members can work on different tools simultaneously
- Each tool is in a separate section of tools.py (no file conflicts)

**Phase 8 (Polish)**:
- T045 and T046 (documentation) can run in parallel [P]

---

## Parallel Example: After Foundational Phase

```bash
# If team has 5 developers, launch all user stories together:
Developer A: Tasks T009-T014 (User Story 1 - add_task)
Developer B: Tasks T015-T020 (User Story 2 - list_tasks)
Developer C: Tasks T021-T026 (User Story 3 - complete_task)
Developer D: Tasks T027-T033 (User Story 4 - delete_task)
Developer E: Tasks T034-T040 (User Story 5 - update_task)

# All tools can be developed independently and merged without conflicts
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T008) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 1 (T009-T014) - add_task tool
4. **STOP and VALIDATE**: Test add_task independently with quickstart examples
5. Minimal viable MCP server with single tool ready for demo

### Incremental Delivery (Recommended)

1. Setup + Foundational → Foundation ready (T001-T008)
2. Add User Story 1 (add_task) → Test independently → Can create tasks! (T009-T014)
3. Add User Story 2 (list_tasks) → Test independently → Can view tasks! (T015-T020)
4. Add User Story 3 (complete_task) → Test independently → Can mark done! (T021-T026)
5. Add User Story 4 (delete_task) → Test independently → Can remove tasks! (T027-T033)
6. Add User Story 5 (update_task) → Test independently → Full CRUD complete! (T034-T040)
7. Polish & Documentation → Production ready (T041-T048)

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T008)
2. Once T008 completes, split into parallel tracks:
   - Track 1: US1 + US2 (Task creation and listing)
   - Track 2: US3 + US4 (Task completion and deletion)
   - Track 3: US5 (Task updates)
3. Merge and integrate in Phase 8

---

## Notes

- **[P] markers**: Tasks marked [P] can run in parallel (different files or independent work)
- **[Story] labels**: Maps each task to specific user story for traceability
- **Independent stories**: Each user story can be completed and tested without others
- **File organization**: All 5 tools in same file (backend/app/mcp_server/tools.py) but separate @mcp.tool() decorators - no conflicts
- **Commit strategy**: Commit after each user story phase completion (T014, T020, T026, T033, T040)
- **Validation**: Each story checkpoint includes independent test criteria
- **Constitution compliance**: Deviations documented in plan.md (non-REST protocol, non-JWT auth)
- **MCP SDK**: Using FastMCP high-level API with decorators (decision from research.md)
- **Transport**: Streamable HTTP on port 8001 for production (stdio for dev/testing)
- **Database**: Reuses existing Task model, no schema changes required
- **Stateless**: All tools query database directly, no in-memory caching

---

## Success Criteria

### Functional Requirements (from spec.md)

- ✅ All 5 tools implemented (add_task, list_tasks, complete_task, delete_task, update_task)
- ✅ Stateless design (database is single source of truth)
- ✅ Database operations use existing Task model and patterns
- ✅ Type hints on all functions
- ✅ Pydantic validation for all inputs
- ✅ Error handling for all edge cases (validation, not found, permission denied, database errors)
- ✅ User ownership validation in all tools
- ✅ All tools registered with MCP server

### Performance Targets (from spec.md)

- add_task: P95 < 500ms
- list_tasks: P95 < 300ms (up to 1000 tasks)
- complete_task: P95 < 400ms
- delete_task: P95 < 400ms
- update_task: P95 < 400ms

### Quality Gates

- Python type checker passes: `mypy backend/app/mcp_server/`
- Linter passes: `ruff check backend/app/mcp_server/`
- Test script validates all tools: `python -m app.mcp_server.test_tools`
- Statelessness verified: Server restart doesn't lose data
- Documentation complete: tool-specifications.md + updated quickstart.md
- Constitution compliance: Code review confirms adherence with documented deviations

---

**Total Tasks**: 48
**User Stories**: 5 (one per MCP tool)
**Parallel Opportunities**: Foundational schemas (2 tasks), All 5 user stories after foundation, Documentation (2 tasks)
**Suggested MVP Scope**: Phase 1-3 (Setup + Foundational + User Story 1) = 14 tasks for minimal viable MCP server
**Independent Test Criteria**: Each user story phase includes checkpoint validation

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, labels, file paths)
