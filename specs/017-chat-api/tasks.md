# Tasks: Stateless Chat API Backend

**Input**: Design documents from `/specs/017-chat-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.yaml, quickstart.md

**Implementation Status**: ✅ **Backend already implemented in Feature 013** (Todo AI Chatbot)

**Task Focus**: This task list focuses on:
1. **Validation**: Verify existing implementation meets Feature 017 requirements
2. **Gap Remediation**: Fix identified gaps from research.md analysis
3. **Documentation**: Ensure comprehensive documentation
4. **Testing**: Add missing test coverage

**Organization**: Tasks are grouped by user story to enable independent testing and validation of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This project uses **Web app (monorepo)** structure:
- Backend: `backend/app/`
- Frontend: `frontend/` (separate feature)
- Specs: `specs/017-chat-api/`

---

## Phase 1: Setup & Validation

**Purpose**: Verify existing implementation and setup validation infrastructure

- [X] T001 Verify backend server starts without errors (run `uvicorn app.main:app --reload` from backend/)
- [X] T002 [P] Verify all dependencies installed (check `backend/requirements.txt` includes fastapi, sqlmodel, google-generativeai, uvicorn)
- [X] T003 [P] Verify environment variables configured (check `.env` has DATABASE_URL, GEMINI_API_KEY, JWT_SECRET_KEY, CORS_ORIGINS)
- [X] T004 Verify database migrations applied (run `alembic current` from backend/, should show conversations and messages tables)
- [X] T005 [P] Review existing implementation files match spec (backend/app/routes/chat.py, backend/app/agent.py, backend/app/schemas/chat.py, backend/app/services/conversation_service.py)

---

## Phase 2: Foundational (Gap Remediation)

**Purpose**: Fix identified gaps from research.md analysis

**⚠️ CRITICAL**: These gaps must be fixed before user story validation

### Health Check Enhancement (from research.md gap analysis)

- [X] T006 Enhance health check endpoint to verify database connectivity in backend/app/main.py
  - Import database session
  - Try simple query (SELECT 1)
  - Return 503 Service Unavailable if database unreachable
  - Return {"status": "healthy", "database": "connected"} if successful

### Rate Limiting Enhancement (from research.md gap analysis)

- [X] T007 [P] Update rate limiting to use user-based key in backend/app/middleware/rate_limit.py
  - Change key_func from get_remote_address to extract user_id from JWT token
  - Fallback to IP address if unauthenticated
  - Add Redis configuration for distributed rate limiting (optional)

### Error Handling Enhancement

- [X] T008 [P] Add database-specific error handling in backend/app/routes/chat.py
  - Catch database connection errors separately
  - Return 503 instead of 500 for database unavailability
  - Log database errors with full context

**Checkpoint**: Foundation gaps remediated - ready for user story validation

---

## Phase 3: User Story 1 - Send Chat Message and Get AI Response (Priority: P1) 🎯 MVP

**Goal**: Validate core chat functionality - users can send messages and receive AI responses with task operations

**Independent Test**: Send POST request to `/api/chat` with message → Receive response with conversation_id and AI message → Verify messages stored in database

**Implementation Status**: ✅ Already implemented in backend/app/routes/chat.py

### Validation for User Story 1

- [X] T009 [P] [US1] Test creating first message creates new conversation using curl or Postman
  - POST /api/chat with {"content": "Add buy groceries", "conversation_id": null}
  - Verify response includes conversation_id, message_id, role="assistant", content
  - Check database: SELECT * FROM conversations WHERE user_id = '...'
  - Check database: SELECT * FROM messages WHERE conversation_id = '...'

- [X] T010 [P] [US1] Test follow-up message uses existing conversation using curl or Postman
  - POST /api/chat with {"content": "Show my tasks", "conversation_id": "uuid-from-T009"}
  - Verify response references previous conversation
  - Check database for 4 total messages (2 user + 2 assistant)

- [X] T011 [P] [US1] Test agent tool execution returns tool_calls array using curl or Postman
  - POST /api/chat with {"content": "Add task: call mom"}
  - Verify response.task_data includes tasks array
  - Verify tool_calls in response (if exposed)

### Additional Test Coverage for User Story 1

- [X] T012 [P] [US1] Add integration test for first message flow in backend/tests/test_chat_endpoints.py
  - Test function: test_first_message_creates_conversation()
  - Mock TodoBot agent response
  - Assert conversation created in database
  - Assert user message and assistant message stored

- [X] T013 [P] [US1] Add integration test for multi-turn conversation in backend/tests/test_chat_endpoints.py
  - Test function: test_multi_turn_conversation_maintains_context()
  - Create conversation with 3 message pairs
  - Verify 6 total messages in database
  - Verify conversation history passed to agent

- [X] T014 [P] [US1] Add integration test for tool execution in backend/tests/test_chat_endpoints.py
  - Test function: test_agent_tool_execution()
  - Send message that triggers add_task
  - Verify task created in database
  - Verify task_data in response

**Checkpoint**: User Story 1 fully validated and tested - MVP is functional

---

## Phase 4: User Story 2 - Resume Existing Conversation (Priority: P2)

**Goal**: Validate conversation context retention across sessions

**Independent Test**: Create conversation → Close client → Reopen and send message with conversation_id → Verify AI response uses previous context

**Implementation Status**: ✅ Already implemented via conversation history retrieval (last 20 messages)

### Validation for User Story 2

- [X] T015 [P] [US2] Test conversation context maintained across requests using curl or Postman
  - Create conversation: "Add buy milk"
  - Wait 5 seconds (simulate session gap)
  - Send follow-up: "Make that 2 gallons" with conversation_id
  - Verify AI response references "milk" from previous message

- [X] T016 [P] [US2] Test unauthorized access to conversation returns 404 using curl or Postman
  - User A creates conversation (save conversation_id)
  - User B tries to access with User A's conversation_id
  - Verify 404 Not Found response (ownership validation)

- [X] T017 [P] [US2] Test invalid conversation_id returns 404 using curl or Postman
  - POST /api/chat with {"content": "Hello", "conversation_id": "00000000-0000-0000-0000-000000000000"}
  - Verify 404 Not Found response

### Additional Test Coverage for User Story 2

- [X] T018 [P] [US2] Add integration test for conversation ownership validation in backend/tests/test_chat_endpoints.py
  - Test function: test_conversation_ownership_validation()
  - Create conversation for user1
  - Attempt access with user2's token
  - Assert 404 response

- [X] T019 [P] [US2] Add integration test for conversation history limit in backend/tests/test_chat_endpoints.py
  - Test function: test_conversation_history_limit_20_messages()
  - Create conversation with 25 messages
  - Send new message
  - Verify agent receives only last 20 messages (check logs or mock)

- [X] T020 [P] [US2] Add integration test for context reference resolution in backend/tests/test_chat_endpoints.py
  - Test function: test_agent_resolves_context_references()
  - Message 1: "Add buy groceries"
  - Message 2: "Mark that as complete"
  - Verify agent calls list_tasks then complete_task with correct task_id

**Checkpoint**: User Story 2 fully validated - conversation context works across sessions

---

## Phase 5: User Story 3 - Health Check and API Information (Priority: P3)

**Goal**: Validate operational endpoints for monitoring and API discovery

**Independent Test**: Send GET to `/health` → Verify 200 OK with database status → Send GET to `/` → Verify API metadata returned

**Implementation Status**: ⚠️ Partially implemented - health check needs database verification (Gap T006)

### Validation for User Story 3

- [X] T021 [P] [US3] Test health check returns healthy status using curl
  - GET /health
  - Verify 200 OK response
  - Verify {"status": "healthy", "database": "connected"} (after T006)

- [X] T022 [P] [US3] Test health check returns 503 when database unavailable using curl
  - Stop database or break DATABASE_URL
  - GET /health
  - Verify 503 Service Unavailable response
  - Restore database

- [X] T023 [P] [US3] Test root endpoint returns API metadata using curl
  - GET /
  - Verify response includes {"status": "healthy", "message": "Todo API is running", "version": "1.0.0"}

### Additional Test Coverage for User Story 3

- [X] T024 [P] [US3] Add integration test for health check endpoint in backend/tests/test_health_endpoints.py
  - Test function: test_health_check_success()
  - Assert 200 status
  - Assert database connectivity verified

- [X] T025 [P] [US3] Add integration test for health check database failure in backend/tests/test_health_endpoints.py
  - Test function: test_health_check_database_unavailable()
  - Mock database connection failure
  - Assert 503 status

- [X] T026 [P] [US3] Add integration test for root endpoint in backend/tests/test_health_endpoints.py
  - Test function: test_root_endpoint_returns_metadata()
  - Assert response includes name, version, message

**Checkpoint**: User Story 3 fully validated - operational endpoints working

---

## Phase 6: Edge Cases & Error Handling

**Purpose**: Validate error scenarios and edge cases from spec.md

### Error Scenario Tests

- [X] T027 [P] Test agent timeout handling using mock or delay
  - Mock TodoBot.run() to raise timeout exception
  - Verify 500 error with user-friendly message
  - Verify user message still saved to database

- [X] T028 [P] Test malformed request payload validation using curl
  - POST /api/chat with {"content": ""} (empty message)
  - Verify 422 Unprocessable Entity with validation error
  - POST /api/chat with {"content": "x" * 6000} (too long)
  - Verify 422 error

- [X] T029 [P] Test conversation with hundreds of messages using script
  - Create conversation with 100 messages
  - Send new message
  - Verify only last 20 passed to agent
  - Verify performance acceptable (<5 seconds)

- [X] T030 [P] Test concurrent requests to same conversation using parallel curl
  - Launch 5 simultaneous requests to same conversation_id
  - Verify all complete successfully
  - Verify messages interleaved in database (expected behavior)

- [X] T031 [P] Test empty message rejected using curl
  - POST /api/chat with {"content": ""}
  - Verify 422 error

- [X] T032 [P] Test missing authentication token using curl
  - POST /api/chat without Authorization header
  - Verify 401 Unauthorized response

- [X] T033 [P] Test CORS preflight request using browser or curl
  - OPTIONS /api/chat with Origin header
  - Verify CORS headers in response (Access-Control-Allow-Origin, etc.)

**Checkpoint**: All edge cases handled correctly

---

## Phase 7: Documentation & Polish

**Purpose**: Ensure comprehensive documentation and code quality

### Documentation Tasks

- [X] T034 [P] Verify OpenAPI docs auto-generated at /docs
  - Navigate to http://localhost:8000/docs
  - Test chat endpoint through Swagger UI
  - Verify all request/response schemas documented

- [X] T035 [P] Verify quickstart.md instructions work end-to-end in specs/017-chat-api/quickstart.md
  - Follow setup steps from scratch
  - Test all curl examples
  - Fix any incorrect commands or responses

- [X] T036 [P] Update backend/README.md with Feature 017 information
  - Add section: "Chat API Endpoints"
  - Document POST /api/chat endpoint
  - Link to specs/017-chat-api/quickstart.md

- [X] T037 [P] Update CLAUDE.md Recent Changes section
  - Add: "017-chat-api: Stateless chat API backend with Gemini agent integration"
  - Update Active Technologies if needed

### Code Quality Tasks

- [X] T038 [P] Run type checker on backend code
  - Run: `mypy backend/app/` (if mypy configured)
  - Fix any type errors found

- [X] T039 [P] Run linter on backend code
  - Run: `ruff check backend/app/` (if ruff configured)
  - Fix any linting errors

- [X] T040 [P] Review code for constitution compliance in backend/app/routes/chat.py
  - Verify functions <30 lines (✅ already compliant)
  - Verify type hints on all functions (✅ already compliant)
  - Verify DRY principle (✅ ConversationService used)

### Performance & Monitoring

- [X] T041 [P] Add request duration logging in backend/app/routes/chat.py
  - Import time module
  - Capture start_time before agent invocation
  - Log duration after completion: `logger.info(f"Chat request completed in {duration:.2f}s")`
  - Verify <5 seconds p95 latency (SC-001 requirement)

- [X] T042 [P] Add performance test for concurrent requests in backend/tests/test_performance.py
  - Test function: test_100_concurrent_requests()
  - Use asyncio to launch 100 requests simultaneously
  - Verify all complete without errors (SC-002 requirement)

**Checkpoint**: Documentation complete, code quality verified, performance validated

---

## Phase 8: Final Validation

**Purpose**: End-to-end validation using quickstart.md scenarios

### Quickstart Validation

- [X] T043 Execute Scenario 1 from quickstart.md: User creates multiple tasks in one message
  - Send: "Add three tasks: buy groceries, call mom, and finish report by Friday"
  - Verify 3 tasks created
  - Verify conversational response confirms all tasks

- [X] T044 Execute Scenario 2 from quickstart.md: User asks to complete a task
  - Send: "Mark 'buy groceries' as complete"
  - Verify agent calls list_tasks then complete_task
  - Verify task marked complete in database

- [X] T045 Execute Scenario 3 from quickstart.md: Conversation context maintained
  - Message 1: "Add buy milk"
  - Message 2: "Actually, make that 2 gallons"
  - Verify agent understands "that" refers to milk task
  - Verify task updated with "2 gallons of milk"

### Final Checklist

- [X] T046 Run all backend tests with coverage
  - Run: `pytest --cov=app --cov-report=html backend/tests/`
  - Verify >80% coverage for chat endpoints
  - Review coverage report in htmlcov/index.html

- [X] T047 Verify all functional requirements met (FR-001 through FR-020)
  - Review spec.md requirements section
  - Check each requirement against implementation
  - Document any deviations in plan.md

- [X] T048 Verify all success criteria met (SC-001 through SC-010)
  - Review spec.md success criteria section
  - Test each criterion
  - Document results

**Checkpoint**: Feature 017 complete and validated ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup validation (Phase 1)
- **User Story 1 (Phase 3)**: Depends on Foundational gap fixes (Phase 2) - MVP story
- **User Story 2 (Phase 4)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (Phase 5)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **Edge Cases (Phase 6)**: Depends on all user stories validated
- **Documentation (Phase 7)**: Can start anytime after Phase 2
- **Final Validation (Phase 8)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories - can validate after Phase 2
- **User Story 2 (P2)**: Builds on US1 concepts but independently testable - can validate in parallel with US1
- **User Story 3 (P3)**: Completely independent - can validate in parallel with US1/US2

### Within Each User Story

- Validation tests (T009-T011) should run before adding integration tests (T012-T014)
- Integration tests can run in parallel (all marked [P])
- Each story phase is independently completable

### Parallel Opportunities

- **Phase 1 (Setup)**: All tasks (T001-T005) can run in parallel
- **Phase 2 (Foundational)**: T007 and T008 can run in parallel (different files)
- **User Story 1**: All validation tasks (T009-T011) and all test tasks (T012-T014) can run in parallel
- **User Story 2**: All validation tasks (T015-T017) and all test tasks (T018-T020) can run in parallel
- **User Story 3**: All validation tasks (T021-T023) and all test tasks (T024-T026) can run in parallel
- **Edge Cases**: All tasks (T027-T033) can run in parallel
- **Documentation**: All tasks (T034-T042) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all validation tests for User Story 1 together:
Task T009: "Test creating first message creates new conversation using curl or Postman"
Task T010: "Test follow-up message uses existing conversation using curl or Postman"
Task T011: "Test agent tool execution returns tool_calls array using curl or Postman"

# Launch all integration tests for User Story 1 together:
Task T012: "Add integration test for first message flow in backend/tests/test_chat_endpoints.py"
Task T013: "Add integration test for multi-turn conversation in backend/tests/test_chat_endpoints.py"
Task T014: "Add integration test for tool execution in backend/tests/test_chat_endpoints.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup & Validation (T001-T005)
2. Complete Phase 2: Foundational Gap Remediation (T006-T008) - CRITICAL
3. Complete Phase 3: User Story 1 Validation (T009-T014)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md
5. MVP is ready for deployment

### Incremental Delivery

1. Complete Setup + Foundational → Gaps fixed
2. Add User Story 1 → Test independently → **MVP validated**
3. Add User Story 2 → Test independently → Context retention verified
4. Add User Story 3 → Test independently → Operational endpoints ready
5. Add Edge Cases → All error scenarios handled
6. Add Documentation → Feature complete and documented

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (Phase 1) together
2. Team completes Foundational (Phase 2) together - MUST be sequential
3. Once Foundational is done:
   - Developer A: User Story 1 validation and tests
   - Developer B: User Story 2 validation and tests
   - Developer C: User Story 3 validation and tests
4. Developer D: Documentation tasks (can start after Phase 2)
5. All converge for Edge Cases and Final Validation

---

## Notes

### Key Insights from Research

- **Implementation already complete**: Backend was implemented in Feature 013
- **Focus on validation**: Tasks verify existing implementation meets requirements
- **Identified gaps**: Health check, rate limiting, documentation need enhancement
- **API pattern deviation**: `/api/chat` instead of `/api/{user_id}/chat` is documented and justified

### Task Organization

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently validatable and testable
- Validation tasks (manual testing) before integration tests (automated)
- Stop at any checkpoint to validate story independently

### Success Criteria Mapping

- **SC-001** (< 5s p95 latency): Validated in T041
- **SC-002** (100 concurrent requests): Validated in T042
- **SC-003** (99.9% database reliability): Validated in T008, T024, T025
- **SC-004** (zero data loss): Validated in T009, T012, T027
- **SC-005** (appropriate HTTP status codes): Validated throughout user stories
- **SC-006** (CORS configuration): Validated in T033
- **SC-007** (health check <100ms): Validated in T024
- **SC-008** (stateless verification): Validated in T001, T015
- **SC-009** (context maintained): Validated in T015, T019, T020, T045
- **SC-010** (tool execution capture): Validated in T011, T014

### Avoid

- Vague tasks without specific file paths
- Tasks that modify multiple files (breaks parallelization)
- Cross-story dependencies that prevent independent testing
- Skipping validation before adding new tests
- Changing implemented API patterns without reviewing research.md rationale
