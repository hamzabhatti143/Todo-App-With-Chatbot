---
description: "Task breakdown for Todo AI Chatbot feature implementation"
---

# Tasks: Todo AI Chatbot (013-todo-ai-chatbot)

**Input**: Design documents from `/specs/013-todo-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/chat.openapi.yaml, contracts/mcp-tools.json, quickstart.md

**Tests**: Tests are OPTIONAL and not included in this task list per project standards.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/`, `backend/tests/`
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
- **Database**: `backend/alembic/versions/`
- **Documentation**: `specs/013-todo-ai-chatbot/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per quickstart.md

- [X] T001 Create feature branch `013-todo-ai-chatbot` from main
- [X] T002 Create backend MCP server directory structure: backend/app/mcp_server/
- [X] T003 [P] Update backend/requirements.txt to add google-generativeai==0.8.3, mcp==0.5.0, slowapi==0.1.9
- [X] T004 [P] Update frontend/package.json to add @openai/chatkit and axios if not present
- [X] T005 [P] Create backend/.env.example with GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_TOKENS, GEMINI_RATE_LIMIT, GEMINI_TIMEOUT, RATE_LIMIT_CHAT, RATE_LIMIT_AGENT placeholders
- [X] T006 [P] Create frontend/.env.local.example with NEXT_PUBLIC_CHATKIT_DOMAIN_KEY placeholder
- [X] T007 Update specs/013-todo-ai-chatbot/quickstart.md to verify all prerequisites listed
- [X] T008 Run `pip install -r backend/requirements.txt` to verify backend dependencies install successfully
- [X] T009 Run `npm install` in frontend/ to verify frontend dependencies install successfully

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Schema (Conversations & Messages)

- [X] T010 Create Alembic migration for conversations table in backend/alembic/versions/[timestamp]_add_conversations_table.py
- [X] T011 Create Alembic migration for messages table in backend/alembic/versions/[timestamp]_add_messages_table.py
- [X] T012 Create Conversation model in backend/app/models/conversation.py per data-model.md
- [X] T013 Create MessageRole enum and Message model in backend/app/models/message.py per data-model.md
- [ ] T014 Run `alembic upgrade head` to apply migrations and verify tables created

### Gemini AI Service Setup

- [X] T015 Create GeminiService class in backend/app/services/gemini_service.py with initialize_client(), generate_text(), and generate_chat_response() methods
- [X] T016 Create Gemini configuration dataclass in backend/app/config.py with GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_TOKENS, GEMINI_RATE_LIMIT, GEMINI_TIMEOUT
- [X] T017 Implement rate limiting for Gemini API calls using slowapi in backend/app/middleware/rate_limit.py
- [X] T018 Implement exponential backoff retry logic in backend/app/services/gemini_service.py for handling transient API failures

### MCP Tools Framework

- [X] T019 Create MCPToolRegistry class in backend/app/mcp_server/tool_registry.py with register_tool(), get_tool(), list_tools() methods
- [X] T020 [P] Create add_task MCP tool in backend/app/mcp_server/tools/add_task.py per contracts/mcp-tools.json schema
- [X] T021 [P] Create list_tasks MCP tool in backend/app/mcp_server/tools/list_tasks.py per contracts/mcp-tools.json schema
- [X] T022 [P] Create complete_task MCP tool in backend/app/mcp_server/tools/complete_task.py per contracts/mcp-tools.json schema
- [X] T023 [P] Create update_task MCP tool in backend/app/mcp_server/tools/update_task.py per contracts/mcp-tools.json schema
- [X] T024 [P] Create delete_task MCP tool in backend/app/mcp_server/tools/delete_task.py per contracts/mcp-tools.json schema
- [X] T025 Register all MCP tools with GeminiService in backend/app/main.py startup event

### API Infrastructure

- [X] T026 Create ChatMessageRequest schema in backend/app/schemas/chat.py with content and conversation_id fields per contracts/chat.openapi.yaml
- [X] T027 Create ChatMessageResponse schema in backend/app/schemas/chat.py with conversation_id, message_id, role, content, created_at, task_data fields
- [X] T028 Create ConversationResponse schema in backend/app/schemas/conversation.py per contracts/chat.openapi.yaml
- [X] T029 Create MessageResponse schema in backend/app/schemas/message.py per contracts/chat.openapi.yaml
- [X] T030 Update CORS middleware in backend/app/main.py to allow chat endpoints from frontend origin

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by describing them naturally in a chat interface

**Independent Test**: Send "Add a task to buy groceries tomorrow" via POST /api/chat and verify:
1. Gemini AI interprets the request
2. add_task MCP tool is called with title="Buy groceries"
3. Task is created in database with user_id from JWT
4. Response contains conversational confirmation
5. Task appears in GET /api/{user_id}/tasks

### Backend Implementation for User Story 1

- [ ] T031 [US1] Create ConversationService in backend/app/services/conversation_service.py with create_conversation(), get_conversation(), save_message() methods
- [ ] T032 [US1] Implement POST /api/chat endpoint in backend/app/routes/chat.py that accepts ChatMessageRequest per contracts/chat.openapi.yaml
- [ ] T033 [US1] Integrate JWT authentication dependency in chat route to extract user_id
- [ ] T034 [US1] Implement conversation creation logic: if conversation_id is null, create new conversation with user_id
- [ ] T035 [US1] Save user message to messages table with role="user" in chat endpoint
- [ ] T036 [US1] Call GeminiService.generate_chat_response() with user message and conversation history
- [ ] T037 [US1] Parse Gemini response for MCP tool calls and execute add_task tool when detected
- [ ] T038 [US1] Save assistant response to messages table with role="assistant"
- [ ] T039 [US1] Return ChatMessageResponse with conversation_id, message_id, content, and task_data
- [ ] T040 [US1] Add error handling for Gemini API failures, database errors, and invalid requests
- [ ] T041 [US1] Add rate limiting decorator to POST /api/chat endpoint (10 requests per minute per user)

### Frontend Implementation for User Story 1

- [ ] T042 [P] [US1] Create ChatInterface component in frontend/components/chat/ChatInterface.tsx using @openai/chatkit
- [ ] T043 [P] [US1] Create chat API client functions in frontend/lib/api/chat.ts for sendMessage(content, conversationId)
- [ ] T044 [P] [US1] Create chat page in frontend/app/chat/page.tsx that renders ChatInterface component
- [ ] T045 [US1] Implement message submission handler in ChatInterface that calls sendMessage API
- [ ] T046 [US1] Display user message immediately in chat UI after submission
- [ ] T047 [US1] Display assistant response when received from POST /api/chat
- [ ] T048 [US1] Handle loading state while waiting for AI response
- [ ] T049 [US1] Handle error state if API call fails with user-friendly error message
- [ ] T050 [US1] Add JWT token to Authorization header in all chat API requests via Axios interceptor
- [ ] T051 [US1] Store conversation_id in component state after first message and pass to subsequent messages

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via natural language chat

---

## Phase 4: User Story 2 - Task Status Management via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can view, complete, and modify tasks through natural language commands

**Independent Test**:
1. Create task via chat: "Add a task to finish report"
2. List tasks: "Show me all my tasks" - verify task appears
3. Complete task: "Mark finish report as done" - verify task marked completed
4. List completed: "Show my completed tasks" - verify task in completed list
5. Update task: "Change the report task to 'Submit Q4 report'" - verify title updated
6. Delete task: "Delete the report task" - verify task removed

### Backend Implementation for User Story 2

- [ ] T052 [US2] Extend GeminiService to recognize list_tasks intent from natural language queries
- [ ] T053 [US2] Extend GeminiService to recognize complete_task intent from phrases like "mark X as done", "complete X", "I finished X"
- [ ] T054 [US2] Extend GeminiService to recognize update_task intent from phrases like "change X to Y", "rename X", "update X"
- [ ] T055 [US2] Extend GeminiService to recognize delete_task intent from phrases like "delete X", "remove X", "cancel X"
- [ ] T056 [US2] Implement task matching logic in MCP tools to find task_id from task title mentioned in natural language
- [ ] T057 [US2] Handle ambiguous task references: if multiple tasks match, return list and ask user to clarify
- [ ] T058 [US2] Update list_tasks MCP tool to support completed filter when user asks for "completed tasks" or "incomplete tasks"
- [ ] T059 [US2] Format task list responses in conversational style (e.g., "Here are your tasks: 1. Buy groceries 2. Finish report")
- [ ] T060 [US2] Add confirmation messages after task operations (e.g., "I've marked 'Buy groceries' as completed")

### Frontend Implementation for User Story 2

- [ ] T061 [US2] Update ChatInterface to display task lists returned by AI in formatted style
- [ ] T062 [US2] Add visual indicators in chat for task operations (e.g., checkmark icon for completion)
- [ ] T063 [US2] Implement optimistic UI updates: show task status change immediately while API call is in progress
- [ ] T064 [US2] Sync task list in dashboard when tasks are modified via chat (use shared state or refetch)
- [ ] T065 [US2] Add loading spinner for multi-step operations (e.g., list tasks then complete task)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full task CRUD via chat

---

## Phase 5: User Story 3 - Conversation History & Context (Priority: P2)

**Goal**: System maintains conversation history for contextual responses

**Independent Test**:
1. Send message: "Add a task to buy groceries"
2. Send follow-up: "What was that task I just created?" - verify AI references previous message
3. Refresh page
4. Send message: "Show me my recent conversation" - verify conversation history is loaded
5. Continue conversation with context preserved

### Backend Implementation for User Story 3

- [ ] T066 [US3] Implement GET /api/conversations endpoint in backend/app/routes/conversations.py per contracts/chat.openapi.yaml
- [ ] T067 [US3] Add limit and offset query parameters for pagination (default limit=50, max=100)
- [ ] T068 [US3] Filter conversations by user_id from JWT token for user isolation
- [ ] T069 [US3] Order conversations by updated_at DESC (most recent first)
- [ ] T070 [US3] Include message_count in conversation response by counting related messages
- [ ] T071 [US3] Implement GET /api/conversations/{conversation_id} endpoint to retrieve specific conversation
- [ ] T072 [US3] Implement GET /api/conversations/{conversation_id}/messages endpoint to retrieve all messages
- [ ] T073 [US3] Verify conversation ownership: return 404 if conversation.user_id != JWT.user_id
- [ ] T074 [US3] Order messages by created_at ASC (chronological order)
- [ ] T075 [US3] Update POST /api/chat to load conversation history and pass to Gemini for context
- [ ] T076 [US3] Limit conversation history to last 20 messages to avoid token limit issues

### Frontend Implementation for User Story 3

- [ ] T077 [P] [US3] Create ConversationList component in frontend/components/chat/ConversationList.tsx
- [ ] T078 [P] [US3] Create conversation API client in frontend/lib/api/conversations.ts with listConversations(), getConversation(), getMessages()
- [ ] T079 [US3] Add conversation list sidebar to chat page showing recent conversations
- [ ] T080 [US3] Implement conversation selection: clicking a conversation loads its messages
- [ ] T081 [US3] Load conversation messages on page mount if conversation_id is in URL
- [ ] T082 [US3] Persist conversation_id in URL query parameter for bookmarkable conversations
- [ ] T083 [US3] Add "New Conversation" button to start fresh conversation
- [ ] T084 [US3] Display conversation timestamps and message count in sidebar
- [ ] T085 [US3] Implement auto-scroll to bottom when new messages arrive
- [ ] T086 [US3] Add visual indicator for active conversation in sidebar

**Checkpoint**: All P1 and P2 user stories are now complete - users have full conversational task management with history

---

## Phase 6: User Story 4 - Multi-User Support with Isolation (Priority: P2)

**Goal**: Each authenticated user has isolated task list and conversation history

**Independent Test**:
1. Register User A (usera@example.com) and create task via chat: "Add a task to prepare presentation"
2. Register User B (userb@example.com) and create task via chat: "Add a task to review code"
3. Login as User A - verify only "prepare presentation" task appears
4. Login as User B - verify only "review code" task appears
5. User A asks "Show my conversations" - verify only User A's conversations appear
6. User B asks "Show my conversations" - verify only User B's conversations appear
7. Attempt to access User A's conversation_id with User B's JWT - verify 404 returned

### Backend Implementation for User Story 4

- [ ] T087 [US4] Verify all MCP tools filter by user_id from JWT token (add_task, list_tasks, complete_task, update_task, delete_task)
- [ ] T088 [US4] Add user_id to all database queries: `WHERE user_id = ?` in tasks, conversations, messages
- [ ] T089 [US4] Verify GET /api/conversations filters by user_id from JWT
- [ ] T090 [US4] Verify GET /api/conversations/{conversation_id} checks conversation.user_id == JWT.user_id
- [ ] T091 [US4] Verify GET /api/conversations/{conversation_id}/messages checks ownership via conversation.user_id
- [ ] T092 [US4] Add database indexes: conversations.user_id, messages.conversation_id for performance
- [ ] T093 [US4] Test cross-user access attempts return 403 Forbidden or 404 Not Found
- [ ] T094 [US4] Update error messages to avoid leaking information about other users' data

### Frontend Implementation for User Story 4

- [ ] T095 [US4] Verify Axios interceptor includes JWT token in Authorization header for all requests
- [ ] T096 [US4] Clear conversation list and chat state on logout
- [ ] T097 [US4] Reload conversations on login to fetch current user's data
- [ ] T098 [US4] Handle 401 Unauthorized by redirecting to login page
- [ ] T099 [US4] Handle 403 Forbidden by showing "Access denied" message

**Checkpoint**: Multi-user support is complete - each user has fully isolated data

---

## Phase 7: User Story 5 - Intelligent Task Understanding (Priority: P3)

**Goal**: AI interprets complex, multi-part requests

**Independent Test**: Send "I need to finish the report by Friday, call the client on Monday, and schedule a meeting next week" and verify:
1. Three separate tasks are created
2. Task 1: "Finish the report" with description "Due Friday"
3. Task 2: "Call the client" with description "Due Monday"
4. Task 3: "Schedule a meeting" with description "Due next week"
5. AI response confirms all three tasks created

### Backend Implementation for User Story 5

- [ ] T100 [US5] Update Gemini prompt system instruction to detect multi-part requests
- [ ] T101 [US5] Implement multi-tool call logic: parse response for multiple add_task calls
- [ ] T102 [US5] Extract due date context from phrases like "by Friday", "on Monday", "next week" and add to description
- [ ] T103 [US5] Handle compound requests with mixed operations (e.g., "Add task X and mark task Y as done")
- [ ] T104 [US5] Improve task title extraction: handle complex sentences and extract concise titles
- [ ] T105 [US5] Add priority detection: if user says "urgent" or "important", add to description
- [ ] T106 [US5] Implement confirmation summary: list all tasks created in response (e.g., "I've created 3 tasks for you: 1. ... 2. ... 3. ...")

### Frontend Implementation for User Story 5

- [ ] T107 [US5] Update ChatInterface to handle multiple task creation responses with formatted lists
- [ ] T108 [US5] Add visual feedback when multiple tasks are created (e.g., "✓ Created 3 tasks")
- [ ] T109 [US5] Refresh task list in dashboard after multi-task creation

**Checkpoint**: All user stories (P1, P2, P3) are now complete - full feature implementation done

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T110 [P] Update specs/013-todo-ai-chatbot/quickstart.md with complete setup instructions
- [ ] T111 [P] Add logging for all chat operations in backend/app/routes/chat.py
- [ ] T112 [P] Add logging for all MCP tool executions in backend/app/mcp_server/tool_registry.py
- [ ] T113 [P] Implement request/response logging middleware in backend/app/middleware/logging.py
- [ ] T114 Add comprehensive error handling for network timeouts in frontend chat API
- [ ] T115 Implement retry logic for transient errors in frontend/lib/api/chat.ts
- [ ] T116 Add user-friendly error messages for common failures (rate limit, API down, network error)
- [ ] T117 [P] Add frontend loading skeleton for chat interface
- [ ] T118 [P] Add empty state UI for "No conversations yet"
- [ ] T119 Optimize database queries: add indexes for conversations.updated_at, messages.created_at
- [ ] T120 Implement database connection pooling in backend/app/core/database.py
- [ ] T121 Add Gemini API response caching for common queries (optional)
- [ ] T122 [P] Update CLAUDE.md to document new chat feature
- [ ] T123 [P] Update specs/overview.md to add Todo AI Chatbot to features list
- [ ] T124 Add security headers in backend/app/middleware/security.py (CSP, X-Content-Type-Options, etc.)
- [ ] T125 Validate all user inputs against schemas in both frontend and backend
- [ ] T126 Run `alembic upgrade head` to verify all migrations applied
- [ ] T127 Run quickstart.md validation: follow all steps and verify application works end-to-end
- [ ] T128 Create PHR (Prompt History Record) for feature implementation in specs/013-todo-ai-chatbot/phr/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US2 (Phase 4): Depends on US1 (needs task creation working)
  - US3 (Phase 5): Can start after Foundational - No dependencies on US1/US2
  - US4 (Phase 6): Verification phase - depends on US1, US2, US3 being implemented
  - US5 (Phase 7): Depends on US1 (enhances task creation)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ← BLOCKS EVERYTHING
    ↓
    ├── Phase 3 (US1: Task Creation) ← MVP starts here
    │       ↓
    │   Phase 4 (US2: Task Management) ← depends on US1
    │       ↓
    │   Phase 7 (US5: Intelligent Understanding) ← enhances US1
    │
    └── Phase 5 (US3: Conversation History) ← independent
            ↓
        Phase 6 (US4: Multi-User Isolation) ← verification phase
            ↓
        Phase 8 (Polish)
```

### Within Each User Story

- Backend implementation before frontend integration
- Database models before services
- Services before API endpoints
- API endpoints before frontend components
- Core functionality before error handling and polish

### Parallel Opportunities

#### Phase 1 (Setup)
- T003, T004, T005, T006, T007 can all run in parallel (different files)

#### Phase 2 (Foundational)
- T010, T011 migrations can run in parallel (different files)
- T020-T024 MCP tools can all run in parallel (different files)

#### Phase 3 (US1)
- T042, T043, T044 frontend components can run in parallel with backend T031-T041 if two developers available

#### Phase 5 (US3)
- T077, T078 frontend components can run in parallel (different files)

#### Phase 8 (Polish)
- T110, T111, T112, T113, T117, T118, T122, T123 can all run in parallel (different files)

---

## Parallel Example: User Story 1 (Natural Language Task Creation)

```bash
# Backend track (Developer A):
Task T031: Create ConversationService
Task T032: Implement POST /api/chat endpoint
Task T033: Integrate JWT authentication
# ... continue with T034-T041

# Frontend track (Developer B - can run in parallel after Phase 2):
Task T042: Create ChatInterface component
Task T043: Create chat API client functions
Task T044: Create chat page
# ... continue with T045-T051

# These tracks are independent until integration testing
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T030) - CRITICAL checkpoint
3. Complete Phase 3: User Story 1 (T031-T051) - Natural Language Task Creation
4. **STOP and VALIDATE**: Test US1 independently per test criteria
5. Complete Phase 4: User Story 2 (T052-T065) - Task Status Management
6. **STOP and VALIDATE**: Test US1 and US2 together
7. Deploy MVP with chat-based task management

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Database + Gemini + MCP → Backend ready
2. **MVP v1** (Phase 3): Add US1 → Test task creation via chat → Demo!
3. **MVP v2** (Phase 4): Add US2 → Test full CRUD via chat → Demo!
4. **Enhancement v1** (Phase 5): Add US3 → Test conversation history → Demo!
5. **Production Ready** (Phase 6): Add US4 → Test multi-user isolation → Deploy!
6. **Enhanced Intelligence** (Phase 7): Add US5 → Test complex requests → Deploy!
7. **Polish** (Phase 8): Add error handling, logging, docs → Production release!

### Parallel Team Strategy

With multiple developers after Phase 2 completion:

**Week 1: Foundation**
- Entire team: Phases 1-2 together (Setup + Foundational)

**Week 2-3: MVP**
- Developer A: Phase 3 (US1 backend)
- Developer B: Phase 3 (US1 frontend)
- Developer C: Phase 4 (US2 - waits for US1 backend)

**Week 4: Enhancement**
- Developer A: Phase 5 (US3 backend)
- Developer B: Phase 5 (US3 frontend)
- Developer C: Phase 6 (US4 verification)

**Week 5: Intelligence & Polish**
- Developer A: Phase 7 (US5)
- Developer B: Phase 8 (Polish - frontend)
- Developer C: Phase 8 (Polish - backend)

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- MVP = User Stories 1 & 2 (P1 priorities)
- User Story 3-5 are enhancements that can be added incrementally
- User Story 4 is verification - most code already implements isolation, this phase validates it
- Stop at any checkpoint to validate story independently before proceeding
- Commit after each task or logical group for clean git history
- Follow quickstart.md for environment setup and testing procedures
- All database queries MUST filter by user_id for security
- All API endpoints MUST require JWT authentication
- All Gemini API calls MUST have rate limiting and retry logic
