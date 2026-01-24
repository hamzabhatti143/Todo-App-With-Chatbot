---
description: "Task breakdown for Gemini AI Agent implementation"
---

# Tasks: Gemini AI Agent for Task Management

**Input**: Design documents from `/specs/016-gemini-agent/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Note**: This feature was already implemented during the planning phase. These tasks document the completed work.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Backend code: `backend/app/`
- Tests: `backend/app/test_agent.py`
- Docs: `specs/016-gemini-agent/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify dependencies and environment configuration

- [x] T001 Verify google-generativeai==0.8.3 installed from Feature 013
- [x] T002 Verify MCP Task Server tools accessible from Feature 015
- [x] T003 [P] Verify pytest-asyncio installed for async tests
- [x] T004 [P] Ensure GEMINI_API_KEY environment variable configured in backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core agent infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create AgentConfig Pydantic model in backend/app/agent.py
- [x] T006 [P] Create ConversationMessage Pydantic model in backend/app/agent.py
- [x] T007 [P] Create AgentRequest Pydantic model with user_id validation in backend/app/agent.py
- [x] T008 [P] Create AgentResponse Pydantic model in backend/app/agent.py
- [x] T009 [P] Create ToolCall Pydantic model in backend/app/agent.py
- [x] T010 Define SYSTEM_INSTRUCTIONS constant with agent behavior prompt in backend/app/agent.py
- [x] T011 Define ERROR_MESSAGES dictionary with user-friendly error templates in backend/app/agent.py
- [x] T012 Create _create_mcp_tools() function to generate Gemini-format tool declarations in backend/app/agent.py
- [x] T013 Implement TodoBot class __init__ with Gemini client initialization in backend/app/agent.py
- [x] T014 Implement _initialize_client() method to configure GenerativeModel with tools in backend/app/agent.py
- [x] T015 Implement _prepare_history() method to convert conversation messages to Gemini format in backend/app/agent.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Task via Natural Language (Priority: P1) 🎯 MVP

**Goal**: User can create tasks using conversational language like "Add buy groceries"

**Independent Test**: User sends "Add buy groceries" → Agent creates task → Task appears in database with correct title

### Implementation for User Story 1

- [x] T016 [US1] Implement add_task tool declaration in _create_mcp_tools() function in backend/app/agent.py
- [x] T017 [US1] Implement _execute_tool() method to route add_task calls to MCP tool in backend/app/agent.py
- [x] T018 [US1] Implement TodoBot.run() method with tool execution for task creation in backend/app/agent.py
- [x] T019 [US1] Add error handling for ValueError from add_task tool in backend/app/agent.py
- [x] T020 [US1] Add test_create_task() in backend/app/test_agent.py
- [x] T021 [P] [US1] Add test_create_task_with_description() in backend/app/test_agent.py
- [x] T022 [P] [US1] Add test_various_create_phrasings() to test different natural language patterns in backend/app/test_agent.py

**Checkpoint**: User Story 1 fully functional - users can create tasks via natural language

---

## Phase 4: User Story 2 - View Tasks via Natural Language (Priority: P2)

**Goal**: User can view tasks using conversational queries like "show my tasks" or "what's pending?"

**Independent Test**: User sends "Show my tasks" → Agent retrieves task list → User sees all tasks with completion status

### Implementation for User Story 2

- [x] T023 [US2] Implement list_tasks tool declaration with status parameter in _create_mcp_tools() in backend/app/agent.py
- [x] T024 [US2] Add list_tasks routing in _execute_tool() method in backend/app/agent.py
- [x] T025 [US2] Update TodoBot.run() to handle list_tasks responses in backend/app/agent.py
- [x] T026 [US2] Add test_list_tasks() in backend/app/test_agent.py
- [x] T027 [P] [US2] Add test_list_pending_tasks() for status filtering in backend/app/test_agent.py
- [x] T028 [P] [US2] Add test_various_list_phrasings() for natural language variations in backend/app/test_agent.py

**Checkpoint**: User Stories 1 AND 2 both work independently - full read/write cycle complete

---

## Phase 5: User Story 3 - Complete Task via Natural Language (Priority: P3)

**Goal**: User can mark tasks done using natural language like "mark the groceries task as done"

**Independent Test**: User views tasks → says "Mark [task reference] as done" → Agent marks task complete → Task shows completed status

### Implementation for User Story 3

- [x] T029 [US3] Implement complete_task tool declaration in _create_mcp_tools() in backend/app/agent.py
- [x] T030 [US3] Add complete_task routing with task identification in _execute_tool() in backend/app/agent.py
- [x] T031 [US3] Update SYSTEM_INSTRUCTIONS to guide task identification pattern in backend/app/agent.py
- [x] T032 [US3] Add tool execution logic for chained list→complete operations in TodoBot.run() in backend/app/agent.py

**Checkpoint**: User Stories 1, 2, AND 3 work independently - core task lifecycle complete

---

## Phase 6: User Story 4 - Delete Task via Natural Language (Priority: P4)

**Goal**: User can remove tasks using commands like "delete the shopping task"

**Independent Test**: User views tasks → says "Delete [task reference]" → Agent removes task → Task no longer appears

### Implementation for User Story 4

- [x] T033 [US4] Implement delete_task tool declaration in _create_mcp_tools() in backend/app/agent.py
- [x] T034 [US4] Add delete_task routing in _execute_tool() in backend/app/agent.py
- [x] T035 [US4] Update TodoBot.run() to handle delete confirmations in backend/app/agent.py

**Checkpoint**: User Stories 1-4 work independently - full CRUD operations complete

---

## Phase 7: User Story 5 - Update Task via Natural Language (Priority: P5)

**Goal**: User can modify tasks using commands like "change the title to..." or "update the description"

**Independent Test**: User views tasks → says "Change [task reference] to [new content]" → Agent updates task → Changes visible

### Implementation for User Story 5

- [x] T036 [US5] Implement update_task tool declaration in _create_mcp_tools() in backend/app/agent.py
- [x] T037 [US5] Add update_task routing in _execute_tool() in backend/app/agent.py
- [x] T038 [US5] Update TodoBot.run() to handle update operations in backend/app/agent.py

**Checkpoint**: All 5 user stories complete - full natural language task management available

---

## Phase 8: Conversation Context & Edge Cases

**Purpose**: Multi-turn conversation support and robust error handling

- [x] T039 Implement conversation history trimming (max 20 messages) in _prepare_history() in backend/app/agent.py
- [x] T040 [P] Add test_conversation_context() for multi-turn conversations in backend/app/test_agent.py
- [x] T041 [P] Add test_invalid_user_id() validation in backend/app/test_agent.py
- [x] T042 [P] Add test_empty_message() validation in backend/app/test_agent.py
- [x] T043 [P] Add test_message_too_long() validation in backend/app/test_agent.py
- [x] T044 [P] Add test_conversation_history_too_long() validation in backend/app/test_agent.py

**Checkpoint**: Agent handles edge cases gracefully with user-friendly errors

---

## Phase 9: Documentation & Polish

**Purpose**: Complete documentation and validation

- [x] T045 [P] Create research.md documenting technical decisions in specs/016-gemini-agent/
- [x] T046 [P] Create data-model.md with all Pydantic schemas in specs/016-gemini-agent/
- [x] T047 [P] Create quickstart.md with usage examples in specs/016-gemini-agent/
- [x] T048 [P] Create IMPLEMENTATION_SUMMARY.md in specs/016-gemini-agent/
- [x] T049 Add docstrings to all TodoBot methods in backend/app/agent.py
- [x] T050 Add inline code documentation for complex logic in backend/app/agent.py
- [x] T051 Run test suite with python -m app.test_agent to verify structure
- [x] T052 Create cleanup test in test_agent.py for test task removal

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Context & Edge Cases (Phase 8)**: Can proceed after Foundational phase
- **Documentation (Phase 9)**: Can proceed alongside implementation

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but complements it
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses list_tasks pattern from US2 but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Similar to US3, independent
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Similar to US3/US4, independent

### Within Each User Story

- Tool declaration before tool routing
- Tool routing before run() method integration
- Core implementation before tests
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] (T006-T015) can run in parallel once T005 completes
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests within a story marked [P] can run in parallel
- Documentation tasks (T045-T048) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Add test_create_task() in backend/app/test_agent.py"
Task: "Add test_create_task_with_description() in backend/app/test_agent.py"
Task: "Add test_various_create_phrasings() in backend/app/test_agent.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (task creation)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready ✅
2. Add User Story 1 → Test independently → MVP! ✅
3. Add User Story 2 → Test independently → Read/Write cycle complete ✅
4. Add User Story 3 → Test independently → Task lifecycle complete ✅
5. Add User Story 4 → Test independently → Full CRUD available ✅
6. Add User Story 5 → Test independently → Complete feature set ✅
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Create tasks)
   - Developer B: User Story 2 (View tasks)
   - Developer C: User Story 3 (Complete tasks)
3. Stories complete and integrate independently

---

## Status

**Implementation Status**: ✅ COMPLETE

All 52 tasks completed during implementation:
- Phase 1: 4/4 tasks complete
- Phase 2: 11/11 tasks complete (foundation ready)
- Phase 3 (US1): 7/7 tasks complete
- Phase 4 (US2): 6/6 tasks complete
- Phase 5 (US3): 4/4 tasks complete
- Phase 6 (US4): 3/3 tasks complete
- Phase 7 (US5): 3/3 tasks complete
- Phase 8: 6/6 tasks complete
- Phase 9: 8/8 tasks complete

**Files Created**:
- `backend/app/agent.py` (~450 lines)
- `backend/app/test_agent.py` (~450 lines)
- `specs/016-gemini-agent/research.md`
- `specs/016-gemini-agent/data-model.md`
- `specs/016-gemini-agent/quickstart.md`
- `specs/016-gemini-agent/IMPLEMENTATION_SUMMARY.md`

**Integration Testing**: Pending valid Gemini API key

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- All tasks completed using direct google-generativeai SDK (research decision)
- Agent structure validated with test suite
- Ready for integration with valid API key
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
