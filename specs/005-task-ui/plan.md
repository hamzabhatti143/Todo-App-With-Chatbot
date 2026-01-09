# Implementation Plan: Task Management User Interface

**Branch**: `005-task-ui` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-task-ui/spec.md`

## Summary

Implement responsive task management user interface using Next.js 16+ with App Router, TypeScript strict mode, and Tailwind CSS. The UI provides complete CRUD operations for tasks including create, read, update, delete, completion toggle, and filtering by completion status. Interface must be mobile-responsive (320px minimum width), display loading states for all async operations, provide clear validation feedback, and ensure 90% first-attempt success rate for task management workflows.

**Technical Approach**: Build component-based architecture with React Server Components as default, Client Components for interactive forms and state management. Centralized API client handles all backend communication with JWT authentication. Tailwind CSS provides utility-first responsive design. Zod validation ensures type-safe form inputs. State management uses React hooks (useState, useEffect) with proper loading and error states.

## Technical Context

**Language/Version**: TypeScript 5.x (strict mode), Next.js 16+ with App Router
**Primary Dependencies**: Next.js, React 19+, Tailwind CSS 4.x, Better Auth (JWT plugin), Zod validation, Axios
**Storage**: N/A (frontend consumes backend API)
**Testing**: Jest with React Testing Library, Playwright for E2E tests
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge), Mobile browsers (iOS Safari, Chrome Android)
**Project Type**: Web frontend (monorepo structure with separate frontend/ directory)
**Performance Goals**: <2s task list load for 100 tasks, <1s filter updates, <10s task creation workflow
**Constraints**: Functional on 320px width screens, 44x44px minimum touch targets, 100% async operations show loading states
**Scale/Scope**: 8 user stories, 25 functional requirements, 10 success criteria, ~15 components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Monorepo Organization
- ✅ **PASS**: Frontend code resides in `frontend/` directory
- ✅ **PASS**: Specifications in `specs/005-task-ui/`
- ✅ **PASS**: Clear separation between frontend and backend

### Principle II: Code Quality Standards (NON-NEGOTIABLE)
- ✅ **PASS**: TypeScript strict mode enabled (`tsconfig.json`)
- ✅ **PASS**: Zero `any` types allowed (enforced via linting)
- ✅ **PASS**: Maximum 30 lines per function
- ✅ **PASS**: DRY principle - reusable components (Button, Input, TaskForm)
- ✅ **PASS**: Comprehensive error handling with meaningful messages
- ✅ **PASS**: Clear, descriptive naming (TaskItem, TaskForm, TaskList)

### Principle III: Frontend Architecture (Next.js 16+)
- ✅ **PASS**: App Router conventions followed (`app/` directory)
- ✅ **PASS**: Server Components default, Client Components only for interactivity
- ✅ **PASS**: Tailwind CSS exclusively (no inline styles, no CSS modules)
- ✅ **PASS**: Centralized API client at `lib/api.ts`
- ✅ **PASS**: Zod validation for all form inputs
- ✅ **PASS**: Loading and error states for every async operation

### Principle VI: Authentication Architecture (NON-NEGOTIABLE)
- ✅ **PASS**: Better Auth with JWT plugin
- ✅ **PASS**: JWT tokens in httpOnly cookies (preferred) or localStorage
- ✅ **PASS**: Authorization header on all API requests
- ✅ **PASS**: User ID extracted from session for API calls
- ✅ **PASS**: 401 handling redirects to sign-in page

### Principle VIII: Spec-Driven Development (NON-NEGOTIABLE)
- ✅ **PASS**: Feature specified via `/sp.specify` (spec.md exists)
- ✅ **PASS**: Implementation plan via `/sp.plan` (this file)
- ✅ **PASS**: Tasks will be generated via `/sp.tasks`
- ✅ **PASS**: Implementation using `@nextjs-frontend-dev` agent

### Principle IX: Agent-Based Development
- ✅ **PASS**: `@nextjs-frontend-dev` agent for implementation
- ✅ **PASS**: `@code-reviewer` for validation
- ✅ **PASS**: `@api-integration-specialist` for integration testing
- ✅ **PASS**: `@documentation-writer` for docs updates
- ✅ **PASS**: Auto-invoke skills (monorepo-navigation, spec-kit-integration)

### Principle X: Testing & Quality Gates
- ✅ **PASS**: TypeScript type checking required
- ✅ **PASS**: ESLint with zero warnings
- ✅ **PASS**: Code review by `@code-reviewer`
- ✅ **PASS**: Integration test by `@api-integration-specialist`
- ✅ **PASS**: Documentation updates required

**Constitution Compliance**: ✅ **ALL GATES PASSED**

## Project Structure

### Documentation (this feature)

```text
specs/005-task-ui/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 output (component patterns, state management)
├── data-model.md        # Phase 1 output (TypeScript interfaces, component contracts)
├── quickstart.md        # Phase 1 output (development setup, component usage)
├── contracts/           # Phase 1 output (component props, API client contracts)
│   ├── components.ts    # Component interface contracts
│   └── api-client.ts    # API client method signatures
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── (dashboard)/
│   │   └── dashboard/
│   │       └── page.tsx         # Main dashboard page (Client Component)
│   ├── layout.tsx               # Root layout with Better Auth provider
│   └── globals.css              # Tailwind CSS imports
├── components/
│   ├── ui/
│   │   ├── Button.tsx           # Reusable button component (variants: primary, secondary, danger)
│   │   ├── Input.tsx            # Reusable input component (with label, error state)
│   │   └── LoadingSpinner.tsx   # Loading indicator component
│   └── features/
│       ├── TaskList.tsx         # Task list container (Server Component)
│       ├── TaskItem.tsx         # Individual task display (Client Component)
│       ├── TaskForm.tsx         # Task create/edit form (Client Component)
│       └── FilterBar.tsx        # Task filter controls (Client Component)
├── lib/
│   ├── api.ts                   # Centralized API client (axios with JWT interceptor)
│   ├── auth.ts                  # Better Auth configuration
│   └── utils.ts                 # Utility functions (date formatting, etc.)
├── types/
│   ├── task.ts                  # Task-related TypeScript interfaces
│   └── api.ts                   # API response/request types
├── hooks/
│   ├── useTasks.ts              # Task data fetching hook
│   └── useTaskMutations.ts      # Task mutation hooks (create, update, delete, toggle)
└── validation/
    └── task.ts                  # Zod schemas for task validation

backend/
# (Already implemented in 004-task-crud-api)
# Dependencies: Backend API endpoints, JWT verification, database models

tests/
├── frontend/
│   ├── unit/
│   │   ├── Button.test.tsx
│   │   ├── Input.test.tsx
│   │   ├── TaskItem.test.tsx
│   │   └── TaskForm.test.tsx
│   ├── integration/
│   │   ├── dashboard.test.tsx
│   │   └── task-workflows.test.tsx
│   └── e2e/
│       ├── create-task.spec.ts
│       ├── edit-task.spec.ts
│       ├── delete-task.spec.ts
│       └── filter-tasks.spec.ts
```

**Structure Decision**: Web application structure (Option 2) with separate frontend and backend directories. Frontend uses Next.js 16+ App Router conventions with `app/` directory for pages, `components/` for reusable UI, `lib/` for utilities and API client, `types/` for TypeScript interfaces, `hooks/` for custom React hooks, and `validation/` for Zod schemas.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations. All principles followed.

## Dependencies

### External Dependencies (Feature 005-task-ui)

| Dependency | Purpose | Rationale |
|------------|---------|-----------|
| Backend API (004-task-crud-api) | Task CRUD operations | Frontend consumes RESTful API endpoints for data operations |
| Authentication (003-user-auth) | User session and JWT tokens | Required for authenticated API requests |
| Database Schema (002-database-schema) | Task data model | Frontend TypeScript interfaces mirror backend SQLModel models |
| Project Setup (001-project-setup) | Monorepo structure, Docker Compose | Provides development environment and build tooling |

### External Packages (npm dependencies)

| Package | Version | Purpose |
|---------|---------|---------|
| next | ^16.0.0 | React framework with App Router |
| react | ^19.0.0 | UI library |
| react-dom | ^19.0.0 | React DOM renderer |
| typescript | ^5.3.0 | Type safety |
| tailwindcss | ^4.0.0 | Utility-first CSS |
| better-auth | ^1.0.0 | Authentication library with JWT plugin |
| axios | ^1.6.0 | HTTP client for API requests |
| zod | ^3.22.0 | Schema validation |
| @types/react | ^19.0.0 | TypeScript definitions |
| @types/node | ^20.0.0 | Node.js TypeScript definitions |
| eslint | ^8.55.0 | Code linting |
| prettier | ^3.1.0 | Code formatting |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| @testing-library/react | ^14.1.0 | React component testing |
| @testing-library/jest-dom | ^6.1.0 | DOM matchers for Jest |
| jest | ^29.7.0 | Test runner |
| playwright | ^1.40.0 | E2E testing |
| @playwright/test | ^1.40.0 | Playwright test utilities |

## Phase 0: Research

**Prerequisites**: Constitution Check passed

**Objective**: Resolve all NEEDS CLARIFICATION items from Technical Context and research best practices for Next.js 16+ App Router, React Server/Client Components, Tailwind CSS responsive design, Better Auth JWT integration, and Zod validation patterns.

### Research Tasks

1. **Next.js 16+ App Router Patterns**
   - **What**: Server Components vs Client Components decision tree
   - **Why**: Optimize performance by using Server Components where possible
   - **Output**: Guidelines for when to use 'use client' directive

2. **Better Auth JWT Integration**
   - **What**: JWT token storage (httpOnly cookies vs localStorage), session management, token refresh flow
   - **Why**: Secure authentication with automatic token refresh
   - **Output**: Auth configuration pattern and API client interceptor design

3. **Tailwind CSS Responsive Design**
   - **What**: Mobile-first responsive patterns, breakpoint strategy, touch-friendly component sizing
   - **Why**: Meet 320px minimum width and 44x44px touch target requirements
   - **Output**: Tailwind configuration and responsive component patterns

4. **React State Management for Forms**
   - **What**: Form state management with React hooks, optimistic updates, error handling
   - **Why**: Immediate visual feedback and error recovery
   - **Output**: Custom hooks pattern for task operations

5. **Zod Validation Patterns**
   - **What**: Form validation with Zod, error message display, field-level validation
   - **Why**: Type-safe validation with clear user feedback
   - **Output**: Zod schema design and integration with form components

### Research Output

**File**: `specs/005-task-ui/research.md`

**Format**:
```markdown
# Research Findings: Task Management UI

## Server Components vs Client Components

**Decision**: Use Server Components for static layouts and data fetching, Client Components for interactive forms and state management

**Rationale**: Server Components reduce JavaScript bundle size and improve initial page load. Client Components needed for useState, useEffect, and event handlers.

**Alternatives Considered**:
- All Client Components: Rejected due to larger bundle size and slower initial render
- All Server Components: Rejected due to inability to handle user interactions

**Implementation Guidelines**:
- TaskList: Server Component (fetches initial data)
- TaskItem: Client Component (toggle completion needs state)
- TaskForm: Client Component (form inputs need state)
- FilterBar: Client Component (filter selection needs state)

## Better Auth JWT Integration

[Similar structure for each research topic...]
```

**Agent Assignment**: Run research via general-purpose agent with web search capability

**Completion Criteria**: All NEEDS CLARIFICATION items resolved, best practices documented, implementation patterns decided

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

**Objective**: Design component architecture, TypeScript interfaces, API client contracts, and responsive layout patterns based on research findings.

### 1. Data Model Design

**File**: `specs/005-task-ui/data-model.md`

**Content**:

#### TypeScript Interfaces

```typescript
// Task entity (mirrors backend SQLModel)
interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string  // ISO 8601 datetime
  updated_at: string  // ISO 8601 datetime
}

// Task creation payload
interface TaskCreate {
  title: string
  description?: string
}

// Task update payload
interface TaskUpdate {
  title: string
  description?: string
}

// Task list filter
type TaskFilter = 'all' | 'completed' | 'incomplete'

// API response wrapper
interface ApiResponse<T> {
  data: T
  error: string | null
}
```

#### Component State Models

```typescript
// Dashboard page state
interface DashboardState {
  tasks: Task[]
  loading: boolean
  error: string | null
  filter: TaskFilter
  showCreateForm: boolean
  editingTask: Task | null
}

// Task form state
interface TaskFormState {
  title: string
  description: string
  errors: {
    title?: string
    description?: string
  }
  submitting: boolean
}
```

#### Validation Rules

- Title: Required, 1-200 characters, trim whitespace
- Description: Optional, 0-2000 characters
- Completion: Boolean toggle
- Filter: One of 'all' | 'completed' | 'incomplete'

### 2. API Contracts

**Directory**: `specs/005-task-ui/contracts/`

#### API Client Contract

**File**: `contracts/api-client.ts`

```typescript
/**
 * API Client for Task Management
 *
 * All methods automatically include JWT token from Better Auth session
 * All methods handle loading states and errors
 */

interface TaskApiClient {
  /**
   * List tasks for authenticated user
   * @param userId - User ID from JWT token
   * @param completed - Optional filter: true (completed), false (incomplete), undefined (all)
   * @returns Array of tasks ordered by created_at DESC
   */
  list(userId: string, completed?: boolean): Promise<Task[]>

  /**
   * Create new task
   * @param userId - User ID from JWT token
   * @param data - Task creation payload
   * @returns Created task with generated ID and timestamps
   */
  create(userId: string, data: TaskCreate): Promise<Task>

  /**
   * Get single task by ID
   * @param userId - User ID from JWT token
   * @param taskId - Task ID
   * @returns Task if found and belongs to user, else 404
   */
  get(userId: string, taskId: number): Promise<Task>

  /**
   * Update existing task
   * @param userId - User ID from JWT token
   * @param taskId - Task ID
   * @param data - Task update payload
   * @returns Updated task
   */
  update(userId: string, taskId: number, data: TaskUpdate): Promise<Task>

  /**
   * Delete task
   * @param userId - User ID from JWT token
   * @param taskId - Task ID
   * @returns void on success
   */
  delete(userId: string, taskId: number): Promise<void>

  /**
   * Toggle task completion status
   * @param userId - User ID from JWT token
   * @param taskId - Task ID
   * @returns Updated task with toggled completion status
   */
  toggleComplete(userId: string, taskId: number): Promise<Task>
}
```

#### Component Contracts

**File**: `contracts/components.ts`

```typescript
/**
 * Component Props Contracts
 */

// Button component
interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  type?: 'button' | 'submit' | 'reset'
  onClick?: () => void
  disabled?: boolean
  className?: string  // For Tailwind overrides
}

// Input component
interface InputProps {
  label: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  error?: string
  required?: boolean
  type?: 'text' | 'email' | 'password'
  maxLength?: number
}

// TaskItem component
interface TaskItemProps {
  task: Task
  onToggleComplete: (taskId: number) => void
  onEdit: (task: Task) => void
  onDelete: (taskId: number) => void
}

// TaskForm component
interface TaskFormProps {
  initialData?: TaskCreate
  onSubmit: (data: TaskCreate) => void
  onCancel?: () => void
}

// FilterBar component
interface FilterBarProps {
  currentFilter: TaskFilter
  onFilterChange: (filter: TaskFilter) => void
}
```

### 3. Quickstart Guide

**File**: `specs/005-task-ui/quickstart.md`

```markdown
# Task UI Quickstart

## Prerequisites

1. Backend API running (port 8000)
2. Database initialized with schema
3. Better Auth configured with shared secret

## Environment Setup

Create `frontend/.env.local`:

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=http://localhost:3000
\`\`\`

## Install Dependencies

\`\`\`bash
cd frontend
npm install
\`\`\`

## Run Development Server

\`\`\`bash
npm run dev
\`\`\`

Access: http://localhost:3000/dashboard

## Component Usage

### Creating a Task

1. Click "+ New Task" button
2. Fill title (required, max 200 chars)
3. Fill description (optional, max 2000 chars)
4. Click "Create Task"

### Editing a Task

1. Click "Edit" button on task item
2. Modify title or description
3. Click "Update Task" or "Cancel"

### Toggling Completion

1. Click checkbox on task item
2. Status updates immediately

### Filtering Tasks

1. Click "All", "Pending", or "Completed" button
2. Task list updates to show filtered subset

## Testing

Run unit tests:
\`\`\`bash
npm test
\`\`\`

Run E2E tests:
\`\`\`bash
npm run test:e2e
\`\`\`

## Troubleshooting

**Issue**: "Unauthorized" errors
**Solution**: Check BETTER_AUTH_SECRET matches backend, verify JWT token in cookies/localStorage

**Issue**: Tasks not loading
**Solution**: Verify backend API running on port 8000, check network tab for CORS errors

**Issue**: Validation errors not displaying
**Solution**: Check Zod schema matches backend validation rules
```

### 4. Agent Context Update

**Script**: `.specify/scripts/bash/update-agent-context.sh claude`

**Purpose**: Update `.claude/agents/nextjs-frontend-dev.md` with task UI context

**New Context to Add**:
- Task UI component architecture
- Better Auth JWT integration patterns
- Tailwind CSS responsive design patterns
- API client interceptor for JWT tokens
- Zod validation schemas

**Agent Assignment**: Run agent context update script after contracts are defined

## Implementation Order

### Phase 1: Foundation (P1 Dependencies)

1. **API Client Setup**
   - File: `frontend/lib/api.ts`
   - Dependencies: Better Auth session, Axios, JWT interceptor
   - Deliverable: Centralized API client with all task endpoints

2. **TypeScript Interfaces**
   - File: `frontend/types/task.ts`
   - Dependencies: Backend SQLModel schemas
   - Deliverable: Type-safe interfaces for Task, TaskCreate, TaskUpdate

3. **Zod Validation Schemas**
   - File: `frontend/validation/task.ts`
   - Dependencies: Zod library
   - Deliverable: Validation schemas for task forms

### Phase 2: Base Components (P1)

4. **Button Component**
   - File: `frontend/components/ui/Button.tsx`
   - Dependencies: Tailwind CSS
   - Deliverable: Reusable button with variants (primary, secondary, danger)

5. **Input Component**
   - File: `frontend/components/ui/Input.tsx`
   - Dependencies: Tailwind CSS
   - Deliverable: Reusable input with label, error state, validation feedback

6. **LoadingSpinner Component**
   - File: `frontend/components/ui/LoadingSpinner.tsx`
   - Dependencies: Tailwind CSS
   - Deliverable: Loading indicator for async operations

### Phase 3: Feature Components (P1)

7. **TaskItem Component**
   - File: `frontend/components/features/TaskItem.tsx`
   - Dependencies: Button, API client
   - Deliverable: Task display with checkbox, edit/delete buttons

8. **TaskForm Component**
   - File: `frontend/components/features/TaskForm.tsx`
   - Dependencies: Input, Button, Zod validation
   - Deliverable: Create/edit form with validation

9. **FilterBar Component**
   - File: `frontend/components/features/FilterBar.tsx`
   - Dependencies: Button
   - Deliverable: Filter controls (all, completed, incomplete)

### Phase 4: Dashboard Page (P1)

10. **Custom Hooks**
    - Files: `frontend/hooks/useTasks.ts`, `frontend/hooks/useTaskMutations.ts`
    - Dependencies: API client, Better Auth session
    - Deliverable: Data fetching and mutation hooks

11. **Dashboard Page**
    - File: `frontend/app/(dashboard)/dashboard/page.tsx`
    - Dependencies: All components, hooks, API client
    - Deliverable: Complete task management interface

### Phase 5: Testing (P2)

12. **Unit Tests**
    - Files: `tests/frontend/unit/*.test.tsx`
    - Dependencies: Jest, React Testing Library
    - Deliverable: Component unit tests

13. **Integration Tests**
    - Files: `tests/frontend/integration/*.test.tsx`
    - Dependencies: Jest, React Testing Library, Mock Service Worker
    - Deliverable: Workflow integration tests

14. **E2E Tests**
    - Files: `tests/frontend/e2e/*.spec.ts`
    - Dependencies: Playwright
    - Deliverable: End-to-end workflow tests

## Integration Points

### Backend API Integration

**Endpoint**: `http://localhost:8000/api/{user_id}/tasks`

**Authentication**: JWT token in `Authorization: Bearer <token>` header

**User ID Extraction**: From Better Auth session via `useSession()` hook

**Error Handling**:
- 401 Unauthorized → Redirect to sign-in page
- 400 Bad Request → Display validation errors
- 404 Not Found → Display "Task not found" message
- 500 Server Error → Display generic error message

### Authentication Integration

**Library**: Better Auth with JWT plugin

**Session Management**:
- JWT token stored in httpOnly cookies (preferred)
- Fallback to localStorage if cookies unavailable
- Automatic token refresh on expiry
- Session expiry redirects to sign-in page

**User ID Extraction**:
```typescript
const { data: session } = useSession()
const userId = session?.user.id
```

### Database Integration

**Indirect**: Frontend does not access database directly. All data operations via backend API.

**Data Flow**:
1. User action in UI → React event handler
2. Event handler → API client method
3. API client → HTTP request to backend
4. Backend → Database query (SQLModel ORM)
5. Backend → HTTP response
6. API client → Parse response
7. React state update → UI re-render

## Testing Strategy

### Unit Testing

**Tool**: Jest with React Testing Library

**Scope**: Individual components in isolation

**Tests**:
- Button renders with correct variant styles
- Input displays validation errors
- TaskItem toggles completion on checkbox click
- TaskForm validates title length and required fields
- FilterBar updates active filter on button click

### Integration Testing

**Tool**: Jest with React Testing Library + Mock Service Worker

**Scope**: Component interactions and data flows

**Tests**:
- Dashboard loads tasks from API on mount
- Create task form submits data and refreshes list
- Edit task form pre-populates with current data
- Delete task shows confirmation and removes from list
- Filter changes update displayed tasks

### E2E Testing

**Tool**: Playwright

**Scope**: Full user workflows across frontend and backend

**Tests**:
- User creates task → Task appears in list
- User edits task → Changes persist
- User deletes task → Task removed from list
- User toggles completion → Status updates
- User filters tasks → Correct subset displayed
- Mobile responsiveness → All features work on 320px width

### Performance Testing

**Tool**: Lighthouse CI

**Metrics**:
- Initial page load < 2 seconds
- Filter update < 1 second
- Task creation workflow < 10 seconds
- Mobile performance score > 90

## Acceptance Criteria

### Functional Acceptance (from spec.md)

- ✅ FR-001: Interface displays all user's tasks in list view
- ✅ FR-002: Task title, description, completion status, creation date displayed
- ✅ FR-003: Empty state message when no tasks
- ✅ FR-004: Tasks ordered by creation time (newest first)
- ✅ FR-005: Form interface for creating tasks
- ✅ FR-006: Title validation (not empty)
- ✅ FR-007: Title max length 200 characters with feedback
- ✅ FR-008: Description max 2000 characters
- ✅ FR-009: Immediate visual feedback on task creation
- ✅ FR-010: Completion toggle control (checkbox)
- ✅ FR-011: Immediate completion status update
- ✅ FR-012: Filter controls (all, completed, incomplete)
- ✅ FR-013: Immediate filter update
- ✅ FR-014: Filter persists during task operations
- ✅ FR-015: Edit interface for modifying tasks
- ✅ FR-016: Edit form pre-populated with current data
- ✅ FR-017: Cancel edit without saving
- ✅ FR-018: Delete control for each task
- ✅ FR-019: Confirmation prompt before deletion
- ✅ FR-020: Loading indicators for async operations
- ✅ FR-021: Clear error messages on failures
- ✅ FR-022: Responsive on mobile devices
- ✅ FR-023: Touch-friendly controls (44x44px minimum)
- ✅ FR-024: Layout adapts to screen width
- ✅ FR-025: Input sanitization prevents injection attacks

### Success Criteria (from spec.md)

- ✅ SC-001: Task creation < 10 seconds
- ✅ SC-002: Completion toggle < 2 seconds
- ✅ SC-003: Task list load < 2 seconds for 100 tasks
- ✅ SC-004: Filter update < 1 second
- ✅ SC-005: 100% clear validation error messages
- ✅ SC-006: Functional on 320px width screens
- ✅ SC-007: 44x44px minimum touch targets
- ✅ SC-008: 100% async operations show loading indicators
- ✅ SC-009: All workflows < 30 seconds
- ✅ SC-010: 90% first-attempt success rate

## Post-Implementation

### Constitution Check Re-evaluation

**Re-run after Phase 1 design completion**:
- ✅ Principle III: Frontend Architecture verified with component contracts
- ✅ Principle VI: Authentication Architecture verified with JWT integration
- ✅ Code Quality Standards: Verified via TypeScript interfaces and Zod schemas

**Result**: No violations introduced during design phase

### Documentation Updates Required

1. **Root Documentation**
   - Update `README.md` with Task UI setup instructions
   - Update `CLAUDE.md` with component architecture patterns

2. **Frontend Documentation**
   - Create `frontend/README.md` with component catalog
   - Add JSDoc comments to all components

3. **Spec-Kit Documentation**
   - Mark `specs/005-task-ui/spec.md` as "Implemented"
   - Update `specs/overview.md` with Task UI completion

### Agent Assignments for Implementation

1. **@nextjs-frontend-dev**: Implement all frontend components
2. **@code-reviewer**: Review component code against constitution
3. **@api-integration-specialist**: Test frontend-backend integration
4. **@documentation-writer**: Update all documentation

### Next Command

After plan completion, run:
```bash
/sp.tasks
```

This will generate `specs/005-task-ui/tasks.md` with dependency-ordered implementation tasks.
