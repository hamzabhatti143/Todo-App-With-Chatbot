# Tasks: Task Management User Interface

**Input**: Design documents from `/specs/005-task-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Focus is on implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` for Next.js frontend
- Frontend structure: `app/`, `components/`, `lib/`, `types/`, `hooks/`, `validation/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Frontend project initialization and foundational dependencies

**Note**: Project setup (001), Database (002), Auth (003), and Backend API (004) are already implemented in previous features. This feature focuses solely on the frontend UI.

- [ ] T001 Verify frontend project exists and Next.js 16+ dependencies installed in frontend/package.json
- [ ] T002 [P] Verify Tailwind CSS 4.x configuration exists in frontend/tailwind.config.js
- [ ] T003 [P] Verify TypeScript strict mode enabled in frontend/tsconfig.json
- [ ] T004 [P] Create frontend/types/task.ts with Task, TaskCreate, TaskUpdate, TaskFilter interfaces
- [ ] T005 [P] Create frontend/validation/task.ts with Zod schemas for task validation
- [ ] T006 [P] Create frontend/lib/utils.ts with date formatting and helper functions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create frontend/lib/api.ts with centralized Axios client and JWT interceptor
- [ ] T008 Implement Better Auth session integration in frontend/lib/auth.ts
- [ ] T009 Create frontend/components/ui/Button.tsx with variants (primary, secondary, danger)
- [ ] T010 [P] Create frontend/components/ui/Input.tsx with label, error state, validation feedback
- [ ] T011 [P] Create frontend/components/ui/LoadingSpinner.tsx for async operation indicators
- [ ] T012 Add taskApi methods to frontend/lib/api.ts (list, create, get, update, delete, toggleComplete)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Interact with Task List (Priority: P1) 🎯 MVP

**Goal**: Display all user's tasks in an organized list view with title, description, completion status, and creation date

**Independent Test**: Authenticate, navigate to dashboard, verify all task information displays correctly with proper ordering (newest first) and empty state handling

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create frontend/components/features/TaskItem.tsx to display individual task with all fields
- [ ] T014 [P] [US1] Create frontend/hooks/useTasks.ts for task data fetching with loading and error states
- [ ] T015 [US1] Create frontend/app/(dashboard)/dashboard/page.tsx with task list display and empty state message
- [ ] T016 [US1] Implement task list rendering with TaskItem components in dashboard page
- [ ] T017 [US1] Add task ordering by created_at DESC (newest first) in useTasks hook
- [ ] T018 [US1] Add date formatting for task creation date display using lib/utils.ts
- [ ] T019 [US1] Style task list for responsive layout (320px minimum width) with Tailwind CSS

**Checkpoint**: At this point, User Story 1 should be fully functional - users can view their task list with proper display and ordering

---

## Phase 4: User Story 2 - Create New Tasks (Priority: P1)

**Goal**: Enable task creation through form interface with title (required) and description (optional)

**Independent Test**: Open creation form, submit valid task data, verify task appears immediately in list with form reset

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create frontend/components/features/TaskForm.tsx with title and description fields
- [ ] T021 [P] [US2] Create frontend/hooks/useTaskMutations.ts with create, update, delete, toggleComplete methods
- [ ] T022 [US2] Implement Zod validation in TaskForm (title required, max 200 chars, description max 2000 chars)
- [ ] T023 [US2] Add task creation form state management (title, description, errors, submitting) in TaskForm
- [ ] T024 [US2] Integrate TaskForm with dashboard page - add "+ New Task" button and form toggle
- [ ] T025 [US2] Implement form submission handler calling useTaskMutations.create
- [ ] T026 [US2] Add immediate task list refresh after successful creation
- [ ] T027 [US2] Implement form reset after successful submission
- [ ] T028 [US2] Add field-level error display for validation failures

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can view tasks and create new tasks

---

## Phase 5: User Story 3 - Toggle Task Completion Status (Priority: P1)

**Goal**: Mark tasks as complete/incomplete with immediate visual feedback and persistence

**Independent Test**: Click task checkbox, verify status updates immediately, refresh page, verify change persists

### Implementation for User Story 3

- [ ] T029 [US3] Add checkbox control to TaskItem component for completion toggle
- [ ] T030 [US3] Implement onToggleComplete handler in TaskItem calling useTaskMutations.toggleComplete
- [ ] T031 [US3] Add optimistic UI update for completion status change
- [ ] T032 [US3] Add error handling with status revert on failure
- [ ] T033 [US3] Update visual styling for completed tasks (strikethrough, opacity change)
- [ ] T034 [US3] Add loading state during toggle operation
- [ ] T035 [US3] Wire toggleComplete handler from dashboard page through to TaskItem

**Checkpoint**: All P1 user stories (1, 2, 3) now functional - core MVP features complete

---

## Phase 6: User Story 4 - Filter Tasks by Completion Status (Priority: P2)

**Goal**: Filter task list to show all tasks, completed only, or incomplete only

**Independent Test**: Apply different filters, verify correct task subset displays, verify filter persists during task operations

### Implementation for User Story 4

- [ ] T036 [P] [US4] Create frontend/components/features/FilterBar.tsx with three filter buttons (All, Pending, Completed)
- [ ] T037 [US4] Add filter state management to dashboard page (all, completed, incomplete)
- [ ] T038 [US4] Update useTasks hook to accept completed filter parameter (true, false, undefined)
- [ ] T039 [US4] Integrate FilterBar with dashboard page above task list
- [ ] T040 [US4] Implement filter change handler updating dashboard filter state
- [ ] T041 [US4] Add visual indicator for active filter (highlight selected button)
- [ ] T042 [US4] Ensure filter persists when tasks are created, edited, or deleted
- [ ] T043 [US4] Add smooth transition animation when filter changes

**Checkpoint**: User Stories 1-4 now complete - users can view, create, toggle completion, and filter tasks

---

## Phase 7: User Story 5 - Edit Existing Tasks (Priority: P2)

**Goal**: Modify task title and description with pre-populated form and validation

**Independent Test**: Click edit on task, verify form pre-populates, modify data, save, verify changes appear in list

### Implementation for User Story 5

- [ ] T044 [US5] Add "Edit" button to TaskItem component
- [ ] T045 [US5] Add editing state management to dashboard page (editingTask: Task | null)
- [ ] T046 [US5] Update TaskForm to accept initialData prop for edit mode
- [ ] T047 [US5] Update TaskForm title to show "Create New Task" vs "Edit Task" based on initialData
- [ ] T048 [US5] Implement onEdit handler in TaskItem passing task to dashboard edit state
- [ ] T049 [US5] Render TaskForm in edit mode when editingTask is set
- [ ] T050 [US5] Implement update submission handler calling useTaskMutations.update
- [ ] T051 [US5] Add cancel button to TaskForm clearing editingTask state
- [ ] T052 [US5] Ensure validation applies equally to edit mode (title required, length limits)
- [ ] T053 [US5] Add immediate task list refresh after successful edit

**Checkpoint**: User Stories 1-5 complete - full CRUD operations (create, read, update) plus completion toggle and filtering

---

## Phase 8: User Story 6 - Delete Unwanted Tasks (Priority: P3)

**Goal**: Permanently delete tasks with confirmation prompt to prevent accidents

**Independent Test**: Click delete, verify confirmation shows, confirm deletion, verify task removed from list

### Implementation for User Story 6

- [ ] T054 [US6] Add "Delete" button to TaskItem component
- [ ] T055 [US6] Implement onDelete handler in TaskItem with window.confirm() confirmation prompt
- [ ] T056 [US6] Implement delete submission calling useTaskMutations.delete
- [ ] T057 [US6] Add immediate task list removal on successful deletion
- [ ] T058 [US6] Add error handling displaying error message if deletion fails
- [ ] T059 [US6] Wire delete handler from dashboard page through to TaskItem
- [ ] T060 [US6] Add loading state during delete operation
- [ ] T061 [US6] Style delete button with danger variant (red color)

**Checkpoint**: Full CRUD operations complete - users can create, read, update, delete, toggle completion, and filter tasks

---

## Phase 9: User Story 7 - Responsive Mobile Experience (Priority: P2)

**Goal**: Ensure all features work on mobile devices (320px minimum width, 44x44px touch targets)

**Independent Test**: Access dashboard on mobile device, verify layout adapts, all interactions work with touch

### Implementation for User Story 7

- [ ] T062 [P] [US7] Add responsive breakpoints to Tailwind config for mobile (320px), tablet (768px), desktop (1024px)
- [ ] T063 [P] [US7] Update Button component with minimum 44x44px touch target size on mobile
- [ ] T064 [P] [US7] Update Input component with mobile-friendly text size and padding
- [ ] T065 [US7] Update dashboard page layout to stack vertically on mobile (no horizontal scroll)
- [ ] T066 [US7] Update TaskItem component for mobile layout (stack buttons below task content)
- [ ] T067 [US7] Update TaskForm for mobile (full-width inputs, larger touch targets)
- [ ] T068 [US7] Update FilterBar for mobile (full-width buttons or horizontal scroll)
- [ ] T069 [US7] Add viewport meta tag to app layout for proper mobile scaling
- [ ] T070 [US7] Test and adjust spacing for mobile touch interaction (minimum 8px between targets)

**Checkpoint**: Application now mobile-responsive - all features accessible on phones, tablets, and desktops

---

## Phase 10: User Story 8 - Clear Error Communication (Priority: P3)

**Goal**: Display clear, actionable error messages and loading indicators for all operations

**Independent Test**: Trigger error conditions (network failure, validation failure), verify messages are clear and user can retry

### Implementation for User Story 8

- [ ] T071 [P] [US8] Create frontend/components/ui/ErrorMessage.tsx for consistent error display
- [ ] T072 [P] [US8] Create frontend/components/ui/SuccessMessage.tsx for success feedback
- [ ] T073 [US8] Add loading spinner to dashboard page while tasks are fetching
- [ ] T074 [US8] Add loading state to Button component (disabled + spinner when loading prop true)
- [ ] T075 [US8] Update TaskForm to show field-level error messages below each input
- [ ] T076 [US8] Add network error handling to api.ts with user-friendly messages
- [ ] T077 [US8] Update dashboard error state to display ErrorMessage component
- [ ] T078 [US8] Add success feedback after task creation, edit, delete (optional toast or message)
- [ ] T079 [US8] Add retry capability for failed operations (retry button in error message)
- [ ] T080 [US8] Ensure loading indicators prevent duplicate submissions

**Checkpoint**: All user stories complete with enhanced error handling and user feedback

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [ ] T081 [P] Add JSDoc comments to all components (Button, Input, TaskItem, TaskForm, FilterBar)
- [ ] T082 [P] Add JSDoc comments to all hooks (useTasks, useTaskMutations)
- [ ] T083 [P] Add JSDoc comments to api.ts client methods
- [ ] T084 [P] Verify TypeScript strict mode compliance (no `any` types, proper typing)
- [ ] T085 [P] Run ESLint and fix all warnings in frontend/
- [ ] T086 [P] Run Prettier and format all frontend code
- [ ] T087 Add accessibility attributes (ARIA labels, roles, keyboard navigation)
- [ ] T088 Add focus management for form fields and buttons
- [ ] T089 Verify 401 handling redirects to sign-in page
- [ ] T090 [P] Create frontend/README.md with component catalog and usage examples
- [ ] T091 [P] Update root README.md with Task UI setup and usage instructions
- [ ] T092 Verify all FR-001 through FR-025 functional requirements are met
- [ ] T093 Verify all SC-001 through SC-010 success criteria are met (performance, usability)
- [ ] T094 Run manual testing checklist from spec.md acceptance scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verify existing infrastructure
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-10)**: All depend on Foundational phase completion
  - P1 stories (US1, US2, US3) - Core MVP features
  - P2 stories (US4, US5, US7) - Enhanced functionality
  - P3 stories (US6, US8) - Nice-to-have features
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

**Independent Stories** (can implement in any order after Foundational):
- **User Story 1 (P1)**: View Task List - Foundation for all other features
- **User Story 2 (P1)**: Create Tasks - Independent, uses US1 for display
- **User Story 3 (P1)**: Toggle Completion - Builds on US1 (modifies TaskItem)
- **User Story 4 (P2)**: Filter Tasks - Builds on US1 (filters task list)
- **User Story 5 (P2)**: Edit Tasks - Uses TaskForm from US2, displays in US1
- **User Story 6 (P3)**: Delete Tasks - Builds on US1 (modifies TaskItem)
- **User Story 7 (P2)**: Mobile Responsive - Applies to all components
- **User Story 8 (P3)**: Error Communication - Applies to all components

**Suggested Sequential Order** (priority-based):
1. US1 (View) → US2 (Create) → US3 (Toggle) = Core MVP
2. US4 (Filter) → US5 (Edit) = Enhanced CRUD
3. US7 (Mobile) = Responsive UX
4. US6 (Delete) → US8 (Errors) = Polish

### Within Each User Story

- Foundation tasks (types, validation, utils) before component tasks
- Base components (Button, Input, Spinner) before feature components
- API client before hooks
- Hooks before page components
- Core implementation before enhancements

### Parallel Opportunities

- **Setup Phase**: T002, T003, T004, T005, T006 can run in parallel
- **Foundational Phase**: T010, T011 can run in parallel (different components)
- **User Story 1**: T013, T014 can start in parallel (component + hook)
- **User Story 2**: T020, T021 can start in parallel (component + hook)
- **User Story 4**: T036 can run independently (FilterBar component)
- **User Story 7**: T062, T063, T064 can run in parallel (different component updates)
- **User Story 8**: T071, T072 can run in parallel (different message components)
- **Polish Phase**: T081-T086, T090-T091 can all run in parallel (documentation + linting)

**If team has multiple developers**:
- After Foundational complete, can work on P1 stories in parallel (3 developers)
- After P1 complete, can work on P2 stories in parallel (3 developers)
- Mobile responsive (US7) can be worked on alongside other stories

---

## Parallel Example: User Story 1

```bash
# After Foundational phase complete, these can start simultaneously:
Developer 1: T013 - Create TaskItem component
Developer 2: T014 - Create useTasks hook
# Then they collaborate on:
Developer 1 or 2: T015-T019 - Dashboard page integration
```

## Parallel Example: Multiple User Stories

```bash
# After User Story 1 complete (view task list working):
Developer A: User Story 2 (Create tasks) - T020-T028
Developer B: User Story 3 (Toggle completion) - T029-T035
Developer C: User Story 4 (Filter tasks) - T036-T043
# All can proceed in parallel since US1 provides the foundation
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Goal**: Get working task management in user's hands as quickly as possible

**Include**:
- Phase 1: Setup (verification only)
- Phase 2: Foundational (T007-T012)
- Phase 3: User Story 1 - View tasks (T013-T019)
- Phase 4: User Story 2 - Create tasks (T020-T028)
- Phase 5: User Story 3 - Toggle completion (T029-T035)

**Total MVP Tasks**: 35 tasks
**Estimated Effort**: 2-3 days for single developer
**Value**: Users can view, create, and complete tasks - core todo functionality

### Post-MVP Increments

**Increment 1: Enhanced CRUD** (P2 priority)
- Phase 6: User Story 4 - Filter tasks (T036-T043)
- Phase 7: User Story 5 - Edit tasks (T044-T053)

**Increment 2: Mobile + Delete** (P2-P3 priority)
- Phase 9: User Story 7 - Mobile responsive (T062-T070)
- Phase 8: User Story 6 - Delete tasks (T054-T061)

**Increment 3: Polish** (P3 priority)
- Phase 10: User Story 8 - Error communication (T071-T080)
- Phase 11: Polish & documentation (T081-T094)

### Testing Strategy (Manual)

**Per User Story** (Independent Tests from spec.md):
1. **US1**: Authenticate → View dashboard → Verify task list displays with all fields
2. **US2**: Click "+ New Task" → Fill form → Submit → Verify task appears in list
3. **US3**: Click task checkbox → Verify status updates → Refresh page → Verify persists
4. **US4**: Click filter buttons → Verify correct tasks show → Create task → Verify filter persists
5. **US5**: Click "Edit" → Modify task → Save → Verify changes appear
6. **US6**: Click "Delete" → Confirm → Verify task removed
7. **US7**: Access on mobile device → Verify layout adapts → Verify all features work
8. **US8**: Trigger error (disconnect network) → Verify error message → Retry → Verify success

**Acceptance**: All 25 functional requirements (FR-001 to FR-025) and 10 success criteria (SC-001 to SC-010) validated

---

## Task Completion Checklist

Before marking any task complete, verify:
- [ ] Code follows TypeScript strict mode (no `any` types)
- [ ] Functions are max 30 lines (per constitution)
- [ ] Tailwind CSS used exclusively (no inline styles)
- [ ] Loading and error states implemented for async operations
- [ ] Component has JSDoc comment (for polish phase)
- [ ] Code is formatted with Prettier
- [ ] ESLint warnings resolved
- [ ] Manual test passes for the feature area
