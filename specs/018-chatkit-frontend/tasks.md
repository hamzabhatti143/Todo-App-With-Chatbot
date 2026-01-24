# Tasks: OpenAI ChatKit Frontend

**Input**: Design documents from `/specs/018-chatkit-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-client.md

**Tests**: Tests are not explicitly requested in the feature specification. Manual testing checklist provided in quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` (Next.js application)
- All paths relative to repository root: `/mnt/d/todo-fullstack-web/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and verification of existing structure

- [ ] T001 Verify Next.js 16.0.10 installed in frontend/package.json
- [ ] T002 [P] Verify Axios installed in frontend/package.json (from Feature 012)
- [ ] T003 [P] Verify TypeScript strict mode enabled in frontend/tsconfig.json
- [ ] T004 [P] Verify Tailwind CSS 4.x configured in frontend/tailwind.config.ts
- [ ] T005 Create frontend/.env.local with NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
- [ ] T006 Update frontend/.env.example to document NEXT_PUBLIC_BACKEND_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create frontend/types/chat.ts with Message, Conversation, ChatState, UIMessage interfaces
- [ ] T008 [P] Create frontend/lib/storage.ts with sessionStorage utilities (saveConversationId, getConversationId, saveUserId, getUserId)
- [ ] T009 [P] Create frontend/lib/error-handler.ts with getErrorMessage and isRetryable functions
- [ ] T010 Create frontend/lib/chat-api.ts with sendChatMessage function using Axios (POST /api/chat endpoint)
- [ ] T011 [P] Create frontend/components/chat/LoadingSpinner.tsx with Tailwind animated spinner
- [ ] T012 [P] Create frontend/components/chat/ErrorMessage.tsx with error display and retry button
- [ ] T013 Create frontend/contexts/ChatContext.tsx with ChatProvider, ChatContext, useChatContext hook, and chatReducer

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Enter Chat and Send First Message (Priority: P1) 🎯 MVP

**Goal**: Enable users to enter user ID, navigate to chat interface, send messages to AI assistant, and receive responses with conversation persistence.

**Independent Test**: Navigate to home page, enter user ID "test@example.com", click "Start Chat", send message "Add buy groceries", verify AI responds with task confirmation, send follow-up message "Show my tasks", verify conversation continues in same thread.

### Implementation for User Story 1

**Home Page (User ID Entry)**

- [ ] T014 [US1] Create frontend/app/page.tsx home page with gradient background and centered layout
- [ ] T015 [US1] Add user ID input form to frontend/app/page.tsx with Zod validation (alphanumeric, @, ., -, _)
- [ ] T016 [US1] Implement "Start Chat" button navigation to /chat?user_id=<encoded_id> in frontend/app/page.tsx
- [ ] T017 [US1] Style home page with Tailwind CSS (gradient background, card design, responsive layout)

**Chat Page Structure**

- [ ] T018 [US1] Create frontend/app/chat/page.tsx with layout (header, message area, input area)
- [ ] T019 [US1] Extract user_id from URL query parameter in frontend/app/chat/page.tsx
- [ ] T020 [US1] Save user_id to sessionStorage in frontend/app/chat/page.tsx on mount
- [ ] T021 [US1] Wrap chat page with ChatProvider from frontend/contexts/ChatContext.tsx
- [ ] T022 [US1] Add page header with user info display in frontend/app/chat/page.tsx

**Message Display Components**

- [ ] T023 [P] [US1] Create frontend/components/chat/Message.tsx to render single message with role-based styling (user vs assistant)
- [ ] T024 [P] [US1] Add timestamp display to frontend/components/chat/Message.tsx using created_at field
- [ ] T025 [US1] Create frontend/components/chat/MessageList.tsx to render array of messages with auto-scroll to bottom
- [ ] T026 [US1] Implement scroll behavior in frontend/components/chat/MessageList.tsx (auto-scroll on new message, maintain position on history load)

**Message Input Component**

- [ ] T027 [US1] Create frontend/components/chat/MessageInput.tsx with textarea, send button, and character counter
- [ ] T028 [US1] Implement Shift+Enter for line breaks, Enter for send in frontend/components/chat/MessageInput.tsx
- [ ] T029 [US1] Add input validation in frontend/components/chat/MessageInput.tsx (1-5000 chars, not empty/whitespace only)
- [ ] T030 [US1] Disable input and send button when loading state is true in frontend/components/chat/MessageInput.tsx
- [ ] T031 [US1] Show character counter when input length > 4500 in frontend/components/chat/MessageInput.tsx

**Chat Interface Integration**

- [ ] T032 [US1] Create frontend/components/chat/ChatInterface.tsx main component integrating MessageList, MessageInput, LoadingSpinner, ErrorMessage
- [ ] T033 [US1] Connect ChatInterface to ChatContext (useChatContext hook) for state access
- [ ] T034 [US1] Implement sendMessage handler in ChatInterface calling sendChatMessage from chat-api.ts
- [ ] T035 [US1] Add optimistic message rendering (add user message immediately before API call) in ChatInterface
- [ ] T036 [US1] Handle API response in ChatInterface: extract conversation_id, add assistant message, update state
- [ ] T037 [US1] Save conversation_id to sessionStorage on first message response in ChatInterface
- [ ] T038 [US1] Pass conversation_id to subsequent sendChatMessage calls in ChatInterface
- [ ] T039 [US1] Implement error handling in ChatInterface: display ErrorMessage component, show retry button for retryable errors
- [ ] T040 [US1] Show LoadingSpinner during API request in ChatInterface

**Styling and Responsive Design**

- [ ] T041 [US1] Style chat bubbles in frontend/components/chat/Message.tsx with Tailwind (different colors for user/assistant, rounded corners, padding)
- [ ] T042 [US1] Implement mobile-first responsive layout in frontend/app/chat/page.tsx (320px minimum width)
- [ ] T043 [US1] Test responsive design on mobile (375px), tablet (768px), desktop (1920px) and adjust Tailwind classes
- [ ] T044 [US1] Add smooth animations for message appearance in frontend/components/chat/MessageList.tsx (fade-in, slide-up)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. User can enter chat, send messages, receive AI responses, and conversation persists across messages.

---

## Phase 4: User Story 2 - View and Resume Conversation History (Priority: P2)

**Goal**: Enable returning users to see previous conversations, resume conversations with full context, and start new conversations.

**Independent Test**: Complete User Story 1 (create conversation), close browser, reopen application at /chat, verify conversation_id loaded from sessionStorage, send new message, verify AI responds with context. Click "New Conversation", verify new conversation starts.

### Implementation for User Story 2

**Conversation List API**

- [ ] T045 [P] [US2] Add getConversations function to frontend/lib/chat-api.ts (GET /api/conversations endpoint)
- [ ] T046 [P] [US2] Add getConversationDetail function to frontend/lib/chat-api.ts (GET /api/conversations/{id} endpoint)

**Conversation Sidebar Component**

- [ ] T047 [US2] Create frontend/components/chat/ConversationSidebar.tsx with conversation list display
- [ ] T048 [US2] Fetch conversation list on mount in ConversationSidebar using getConversations
- [ ] T049 [US2] Render conversation items with title, last_message preview, and updated_at timestamp
- [ ] T050 [US2] Implement conversation click handler to load conversation detail using getConversationDetail
- [ ] T051 [US2] Add "New Conversation" button to ConversationSidebar that clears conversation_id and messages
- [ ] T052 [US2] Style ConversationSidebar with Tailwind (sidebar layout, hover states, active conversation highlight)

**Conversation Persistence**

- [ ] T053 [US2] Add loadConversation action to chatReducer in frontend/contexts/ChatContext.tsx
- [ ] T054 [US2] Implement loadConversation function in ChatProvider to fetch and load conversation by ID
- [ ] T055 [US2] Load conversation_id from sessionStorage on chat page mount in frontend/app/chat/page.tsx
- [ ] T056 [US2] If conversation_id exists in sessionStorage, call loadConversation to restore messages
- [ ] T057 [US2] Implement startNewConversation function in ChatProvider to clear conversation state and sessionStorage

**Responsive Integration**

- [ ] T058 [US2] Add ConversationSidebar to frontend/app/chat/page.tsx layout
- [ ] T059 [US2] Hide ConversationSidebar on mobile (<768px) using Tailwind responsive classes
- [ ] T060 [US2] Show ConversationSidebar on tablet/desktop (≥768px) as persistent sidebar
- [ ] T061 [US2] Test conversation sidebar on multiple screen sizes and adjust layout

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can create conversations, resume them after page refresh, view conversation history, and start new conversations.

---

## Phase 5: User Story 3 - Receive Visual Feedback and Handle Errors Gracefully (Priority: P3)

**Goal**: Provide clear visual indicators for loading states, errors, offline detection, and enable error recovery with retry functionality.

**Independent Test**: Send message, verify loading spinner appears. Disconnect network, attempt to send message, verify "You're offline" error message displays with retry button. Reconnect network, click retry, verify message sends successfully.

### Implementation for User Story 3

**Enhanced Error Handling**

- [ ] T062 [US3] Add error type detection in frontend/lib/error-handler.ts (network, timeout, server, validation, unauthorized)
- [ ] T063 [US3] Map error types to user-friendly messages in getErrorMessage function
- [ ] T064 [US3] Implement offline detection in frontend/components/chat/ChatInterface.tsx using navigator.onLine
- [ ] T065 [US3] Show "You're offline" message without attempting API call when offline

**Retry Mechanism**

- [ ] T066 [US3] Add retryLastMessage action to chatReducer in frontend/contexts/ChatContext.tsx
- [ ] T067 [US3] Implement retryLastMessage function in ChatProvider to re-send last failed message
- [ ] T068 [US3] Connect retry button in ErrorMessage component to retryLastMessage function
- [ ] T069 [US3] Clear error state on successful retry in ChatInterface

**Enhanced Loading States**

- [ ] T070 [US3] Add loading indicator next to user message bubble while waiting for response in frontend/components/chat/Message.tsx
- [ ] T071 [US3] Implement typing indicator animation in LoadingSpinner for assistant response (3 animated dots)
- [ ] T072 [US3] Show loading state in MessageInput component (disabled state with visual feedback)

**Error Recovery UX**

- [ ] T073 [US3] Add dismiss button to ErrorMessage component to clear error without retrying
- [ ] T074 [US3] Implement timeout handling (30 second timeout) with specific error message
- [ ] T075 [US3] Add error boundary to frontend/app/chat/page.tsx to catch React errors gracefully
- [ ] T076 [US3] Style error states with Tailwind (red colors, warning icons, clear CTAs)

**Checkpoint**: All user stories should now be independently functional. Users have complete error handling, loading feedback, and recovery options.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and enhance overall user experience

**Animations and Interactions**

- [ ] T077 [P] Add smooth scroll animation to MessageList auto-scroll behavior in frontend/components/chat/MessageList.tsx
- [ ] T078 [P] Add fade-in animation for message appearance in frontend/components/chat/Message.tsx
- [ ] T079 [P] Add pulse animation for LoadingSpinner in frontend/components/chat/LoadingSpinner.tsx

**Keyboard Shortcuts**

- [ ] T080 [P] Create frontend/hooks/use-keyboard-shortcuts.ts hook with Escape and Ctrl+K handlers
- [ ] T081 Integrate keyboard shortcuts in frontend/app/chat/page.tsx (Escape to clear input, Ctrl+K for new conversation)

**Accessibility**

- [ ] T082 [P] Add ARIA labels to chat components (MessageList, MessageInput, send button)
- [ ] T083 [P] Ensure keyboard navigation works for all interactive elements
- [ ] T084 [P] Add focus styles for keyboard users in Tailwind

**Performance Optimization**

- [ ] T085 [P] Memoize Message component to prevent unnecessary re-renders
- [ ] T086 [P] Implement useCallback for message send handler to prevent re-creation
- [ ] T087 Add scroll performance optimization (consider virtual scrolling for 100+ messages as future enhancement)

**Documentation**

- [ ] T088 [P] Create frontend/README.md with setup instructions for Feature 018
- [ ] T089 [P] Document environment variables in frontend/.env.example
- [ ] T090 Update specs/018-chatkit-frontend/quickstart.md with actual file paths and verification steps

**Final Validation**

- [ ] T091 Run through quickstart.md verification checklist for User Story 1 (P1)
- [ ] T092 Run through quickstart.md verification checklist for User Story 2 (P2)
- [ ] T093 Run through quickstart.md verification checklist for User Story 3 (P3)
- [ ] T094 Test all edge cases from spec.md (invalid user ID, long messages, backend unavailable, rapid sending, etc.)
- [ ] T095 Test responsive design on physical mobile device (not just browser DevTools)
- [ ] T096 Run npm run build to verify production build succeeds
- [ ] T097 Run npm run lint to verify no ESLint errors
- [ ] T098 Run type-check (npx tsc --noEmit) to verify no TypeScript errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable (adds conversation list and resume functionality)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 with better error handling, independently testable

### Within Each User Story

- **US1**: Home page → Chat page structure → Components → Integration → Styling (sequential due to dependencies)
- **US2**: API functions → Sidebar component → Persistence logic → Responsive integration (mostly parallel)
- **US3**: Error handling → Retry mechanism → Loading states → Error recovery (mostly parallel)

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003, T004 can run in parallel (different files)

**Phase 2 (Foundational)**:
- T007, T008, T009, T011, T012 can run in parallel (different files, no dependencies)

**Phase 3 (User Story 1)**:
- T023 and T024 can run in parallel (Message.tsx development)
- T041, T042, T043, T044 can run in parallel after core components complete (styling tasks)

**Phase 4 (User Story 2)**:
- T045 and T046 can run in parallel (different API functions)

**Phase 5 (User Story 3)**:
- T070, T071, T072 can run in parallel (different loading state enhancements)

**Phase 6 (Polish)**:
- T077, T078, T079 can run in parallel (different animation tasks)
- T082, T083, T084 can run in parallel (different accessibility tasks)
- T085, T086, T087 can run in parallel (different performance optimizations)
- T088, T089, T090 can run in parallel (different documentation tasks)

---

## Parallel Example: User Story 1

```bash
# Foundation: Launch all foundational components together:
Task T007: "Create frontend/types/chat.ts with Message, Conversation, ChatState, UIMessage interfaces"
Task T008: "Create frontend/lib/storage.ts with sessionStorage utilities"
Task T009: "Create frontend/lib/error-handler.ts with getErrorMessage and isRetryable functions"
Task T011: "Create frontend/components/chat/LoadingSpinner.tsx with Tailwind animated spinner"
Task T012: "Create frontend/components/chat/ErrorMessage.tsx with error display and retry button"

# US1 Components: Launch Message component tasks together:
Task T023: "Create frontend/components/chat/Message.tsx to render single message with role-based styling"
Task T024: "Add timestamp display to frontend/components/chat/Message.tsx using created_at field"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify dependencies, env vars) - ~10 minutes
2. Complete Phase 2: Foundational (types, API client, context, base components) - ~2 hours
3. Complete Phase 3: User Story 1 (home page, chat page, components, integration) - ~4 hours
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md checklist
5. Deploy/demo if ready - MVP is complete!

**Total MVP Time**: ~6-7 hours

### Incremental Delivery

1. **Sprint 1**: Setup + Foundational → Foundation ready (~2 hours)
2. **Sprint 2**: User Story 1 → Test independently → Deploy/Demo (MVP!) (~4 hours)
3. **Sprint 3**: User Story 2 → Test independently → Deploy/Demo (Conversation history) (~3 hours)
4. **Sprint 4**: User Story 3 → Test independently → Deploy/Demo (Error handling polish) (~2 hours)
5. **Sprint 5**: Polish phase → Final testing → Production deploy (~2 hours)

Each sprint adds value without breaking previous functionality.

### Parallel Team Strategy

With 2-3 developers:

**Week 1**:
- Team completes Setup + Foundational together (Day 1)
- Once Foundational is done:
  - Developer A: User Story 1 (Days 2-3)
  - Developer B: User Story 2 (Days 2-3)
  - Developer C: User Story 3 (Days 2-3)

**Week 2**:
- Team completes Polish phase together (Day 4)
- Final testing and validation (Day 5)

Stories complete and integrate independently.

---

## Notes

- **[P]** tasks = different files, no dependencies - can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable per acceptance scenarios in spec.md
- Stop at any checkpoint to validate story independently using quickstart.md checklist
- Commit after each task or logical group for rollback safety
- All file paths are relative to repository root: `/mnt/d/todo-fullstack-web/`
- No new npm dependencies required - Axios already installed from Feature 012
- Custom chat UI components instead of OpenAI ChatKit (not publicly available per research.md)
- Mobile-first responsive design: 320px (mobile), 768px (tablet), 1024px (desktop)
- Backend Feature 017 already complete - frontend consumes `/api/chat` endpoint

---

## Success Criteria Validation

**From spec.md - verify these after implementation**:

- **SC-001**: Users complete full task workflow (create, list, complete) through chat in <2 minutes ✓ (test with US1)
- **SC-002**: Chat interface loads in <2 seconds on 3G ✓ (test with npm run build + network throttling)
- **SC-003**: 99% message delivery reliability when backend available ✓ (test with US1 + error handling)
- **SC-004**: 95% of users successfully send first message without errors ✓ (UX test with US1)
- **SC-005**: Conversation history persists across browser sessions without data loss ✓ (test with US2)
- **SC-006**: Chat renders correctly on mobile (320px width) ✓ (test responsive design)
- **SC-007**: 90% of users resolve errors independently with clear messages ✓ (test with US3)
- **SC-009**: Smooth 60fps scrolling with 100+ messages ✓ (test performance with DevTools)
- **SC-010**: Handles network interruptions with zero data loss and clear recovery ✓ (test with US3)

---

**Total Tasks**: 98
**Estimated Time**: 13-15 hours for complete implementation (all 3 user stories + polish)
**MVP Time**: 6-7 hours (Setup + Foundational + User Story 1 only)
