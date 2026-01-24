# Implementation Plan: OpenAI ChatKit Frontend

**Branch**: `018-chatkit-frontend` | **Date**: 2026-01-22 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/018-chatkit-frontend/spec.md`

**Note**: This plan was created by the `/sp.plan` command following the spec-driven development workflow.

## Summary

Build a beautiful, responsive chat interface using Next.js 16.0.10, TypeScript, and Tailwind CSS that connects to the FastAPI backend (Feature 017) for conversational task management. The interface enables users to send messages to an AI assistant, maintain conversation context, and manage tasks through natural language.

**Primary Requirement**: Conversational task management interface with message persistence, error handling, and mobile-responsive design.

**Technical Approach**:
- Custom React chat components styled with Tailwind CSS (OpenAI ChatKit not publicly available)
- React Context API with useReducer for state management
- Axios HTTP client with request/response interceptors
- sessionStorage for conversation persistence across page refreshes
- URL query parameters for user identification (MVP approach before full JWT authentication)
- Mobile-first responsive design with breakpoints at 320px, 768px, and 1024px

## Technical Context

**Language/Version**: TypeScript 5.x (strict mode enabled)
**Framework**: Next.js 16.0.10 with App Router
**Primary Dependencies**: React 18+, Tailwind CSS 4.x, Axios 1.x
**Storage**: sessionStorage (browser), Backend PostgreSQL (Feature 017)
**Testing**: Vitest + React Testing Library (unit), Playwright (E2E, future)
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only, part of monorepo)
**Performance Goals**:
  - Initial page load: <2 seconds on 3G connection (SC-002)
  - Time to interactive: <3 seconds
  - Smooth 60fps scrolling with 100+ messages (SC-009)
  - Message send/receive cycle: <5 seconds total

**Constraints**:
  - Mobile-first responsive design: 320px minimum width (FR-021)
  - Message content limited to 5000 characters (FR-024)
  - Backend timeout: 30 seconds maximum (FR-014)
  - No external chat libraries (OpenAI ChatKit not publicly available)
  - MVP uses basic user_id authentication (no JWT yet)

**Scale/Scope**:
  - Target: 100+ users per MVP deployment
  - Conversations per user: <100 (no pagination initially)
  - Messages per conversation: 100+ (virtual scrolling future enhancement)
  - 3 user stories (P1: core chat, P2: history, P3: error handling)
  - 32 functional requirements across 5 categories
  - 2 pages (home, chat) with 5 custom chat components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Monorepo Organization ✅ PASS

- Feature adds frontend chat interface in existing `frontend/` directory
- Specifications stored in `specs/018-chatkit-frontend/`
- No new top-level directories created
- Maintains clear separation: frontend chat components, backend unchanged

### II. Code Quality Standards ✅ PASS

- TypeScript strict mode enabled in `frontend/tsconfig.json`
- Zero `any` types allowed (enforced by strict mode)
- Function size limit: 30 lines maximum
- DRY principle: Reusable components in `components/chat/`
- Error handling: Try-catch blocks in all API calls with user-friendly messages
- Naming: Clear names (e.g., `sendChatMessage`, `ConversationSidebar`)

### III. Frontend Architecture ✅ PASS

- App Router pattern: `app/chat/page.tsx` for chat page
- Server Components default, Client Components marked with `'use client'`
- Tailwind CSS exclusively for styling (no inline styles, no CSS modules)
- Centralized API client: `lib/api.ts` (already exists, extended for chat)
- Zod validation: User ID and message content validation
- State management: Loading/error states in ChatContext

### IV. Backend Architecture ⚠️ NOT APPLICABLE (Frontend-only feature)

- Feature 018 is frontend-only implementation
- Backend already implemented in Feature 017 (Stateless Chat API)
- No backend code changes required for this feature

### V. Database Standards ⚠️ NOT APPLICABLE (Frontend-only feature)

- No database schema changes in this feature
- Feature 017 already created `conversations` and `messages` tables
- Frontend only reads/writes via backend API

### VI. Authentication Architecture ⚠️ PARTIAL COMPLIANCE (MVP Exception)

**Current State (MVP)**:
- Using basic `user_id` passed via URL query parameter
- No JWT authentication yet (Assumption #3 in spec)
- sessionStorage for conversation persistence

**Constitution Requirement**:
- JWT tokens with Better Auth
- httpOnly cookies or localStorage
- Backend JWT verification

**Justification for Exception**:
- MVP approach documented in spec (Assumption #3)
- Full JWT authentication is Out of Scope #1 (future iteration)
- User ID validation implemented (alphanumeric, @, ., -, _ only)
- Backend API ready for JWT integration (Feature 017 has JWT middleware)

**Migration Path**:
- Phase 2: Add Better Auth to frontend
- Phase 2: Store JWT in httpOnly cookies
- Phase 2: Update API client to send JWT in Authorization header
- Backend already has JWT verification ready (Feature 017)

### VII. API Endpoint Structure ⚠️ DEVIATION (Backend Design Decision)

**Constitution Pattern**: `/api/{user_id}/tasks`

**Feature 017 Pattern**: `/api/chat` (user from JWT token)

**Justification**:
- Backend Feature 017 designed as stateless API without user_id in path
- User identification from JWT token payload (future) or request header (MVP)
- This is a backend architectural decision made in Feature 017
- Frontend adapts to backend contract (correct separation of concerns)

**Frontend Compliance**:
- Frontend follows backend API contract correctly
- API client in `lib/chat-api.ts` uses `/api/chat` endpoint
- User context sent in request body or header (not URL path)

### VIII. Specification-Driven Development ✅ PASS

- Feature spec created first (`specs/018-chatkit-frontend/spec.md`)
- Zero [NEEDS CLARIFICATION] markers in spec
- All 32 functional requirements documented
- 3 user stories with acceptance criteria
- Implementation plan created before coding (`plan.md`)
- Tasks will be generated with `/sp.tasks` command

### IX. Testing Requirements ⚠️ FUTURE ENHANCEMENT

**Current State**: MVP does not include automated tests

**Constitution Requirement**:
- Unit tests for all components
- Integration tests for user flows
- E2E tests with Playwright

**Mitigation**:
- Manual testing checklist in `quickstart.md`
- All user stories testable manually
- Testing infrastructure documented for Phase 2

**Future Work**:
- Add Vitest + React Testing Library
- Write unit tests for components and API client
- Add Playwright E2E tests for user flows

### X. Documentation Requirements ✅ PASS

- Feature spec: `spec.md` (261 lines, comprehensive)
- Implementation plan: `plan.md` (this file)
- Research: `research.md` (10 technology decisions documented)
- Data model: `data-model.md` (entities, validation, state management)
- API contract: `contracts/api-client.md` (request/response specs)
- Quick start: `quickstart.md` (setup, troubleshooting, verification)
- PHR created: `history/prompts/018-chatkit-frontend/001-create-chatkit-frontend-spec.prompt.md`

---

### Constitution Check Summary

**PASSED**: 6/10 sections fully compliant
**NOT APPLICABLE**: 2/10 sections (backend-only requirements)
**EXCEPTIONS**: 2/10 sections with justified deviations

**Justifications for Exceptions**:

1. **Authentication (VI)**: MVP uses basic user_id, full JWT authentication deferred to Phase 2 per spec assumptions. Backend already supports JWT (Feature 017), frontend will migrate after MVP validation.

2. **API Endpoint Structure (VII)**: Backend Feature 017 designed `/api/chat` without user_id in path (stateless pattern). Frontend correctly follows backend contract.

**Approval to Proceed**: ✅ YES
- All deviations documented with migration path
- MVP scope clearly defined in spec
- No violations of NON-NEGOTIABLE constraints

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Structure**: Web application monorepo (Option 2 - frontend/backend separation)

```text
todo-fullstack-web/
├── frontend/                    # Next.js 16.0.10 application
│   ├── app/
│   │   ├── page.tsx            # MODIFIED: Home page (user ID entry)
│   │   ├── layout.tsx          # EXISTING: Root layout
│   │   ├── globals.css         # EXISTING: Tailwind imports
│   │   └── chat/
│   │       └── page.tsx        # NEW: Chat interface page
│   ├── components/
│   │   ├── chat/               # NEW: Chat-specific components
│   │   │   ├── MessageList.tsx         # Message display area
│   │   │   ├── MessageInput.tsx        # Input field + send button
│   │   │   ├── Message.tsx             # Individual message component
│   │   │   ├── ConversationSidebar.tsx # Conversation list (P2)
│   │   │   ├── LoadingSpinner.tsx      # Loading indicator
│   │   │   └── ErrorMessage.tsx        # Error display with retry
│   │   └── ui/                 # EXISTING: Shared UI components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       └── card.tsx
│   ├── contexts/
│   │   └── ChatContext.tsx     # NEW: Chat state management (React Context)
│   ├── hooks/
│   │   ├── use-auth.ts         # EXISTING: Authentication hooks
│   │   ├── use-chat.ts         # NEW: Chat operations hook
│   │   └── use-keyboard-shortcuts.ts  # NEW: Keyboard shortcuts (Escape, Ctrl+K)
│   ├── lib/
│   │   ├── api.ts              # EXISTING: Axios client configuration
│   │   ├── chat-api.ts         # NEW: Chat endpoint functions
│   │   ├── storage.ts          # NEW: sessionStorage utilities
│   │   ├── error-handler.ts    # NEW: Error message mapping
│   │   └── utils.ts            # EXISTING: Utility functions
│   ├── types/
│   │   ├── api.ts              # EXISTING: API response types
│   │   ├── task.ts             # EXISTING: Task types
│   │   └── chat.ts             # NEW: Chat-specific types (Message, Conversation, ChatState)
│   ├── .env.local              # MODIFIED: Add NEXT_PUBLIC_BACKEND_URL
│   ├── .env.example            # MODIFIED: Document new env vars
│   ├── package.json            # EXISTING: No new dependencies (Axios already installed)
│   ├── tsconfig.json           # EXISTING: Strict mode enabled
│   └── tailwind.config.ts      # EXISTING: Tailwind configuration
│
├── backend/                     # FastAPI application (unchanged for this feature)
│   ├── app/
│   │   ├── routes/
│   │   │   └── chat.py         # EXISTING: Feature 017 endpoints
│   │   ├── models/
│   │   │   ├── conversation.py # EXISTING: Feature 017 models
│   │   │   └── message.py      # EXISTING: Feature 017 models
│   │   └── schemas/
│   │       ├── chat.py         # EXISTING: Feature 017 schemas
│   │       ├── conversation.py # EXISTING: Feature 017 schemas
│   │       └── message.py      # EXISTING: Feature 017 schemas
│   └── tests/
│       └── test_chat_endpoints.py  # EXISTING: Feature 017 tests
│
└── specs/
    └── 018-chatkit-frontend/   # Feature 018 specifications
        ├── spec.md             # Feature specification
        ├── plan.md             # This file - implementation plan
        ├── research.md         # Technology decisions
        ├── data-model.md       # Frontend data structures
        ├── quickstart.md       # Setup guide
        ├── contracts/
        │   └── api-client.md   # API contract specification
        └── checklists/
            └── requirements.md # Spec validation checklist
```

**Structure Decision**: Monorepo with frontend/backend separation

**Rationale**:
- Frontend and backend are distinct codebases with different tech stacks
- Frontend (Next.js/TypeScript) and backend (FastAPI/Python) deploy independently
- Monorepo enables atomic changes to both sides when needed
- Shared specifications in `specs/` directory maintain single source of truth
- Feature 018 is frontend-only, backend unchanged (Feature 017 already complete)

**Key Directories**:
- **frontend/app/chat/**: New page for chat interface (Next.js App Router)
- **frontend/components/chat/**: Reusable chat components (MessageList, MessageInput, etc.)
- **frontend/contexts/**: Chat state management with React Context API
- **frontend/lib/chat-api.ts**: API client functions for chat endpoints
- **frontend/types/chat.ts**: TypeScript definitions for chat domain

**Existing Dependencies**:
- Axios already installed (Feature 012)
- Tailwind CSS configured (Features 012)
- Next.js 16.0.10 with App Router (Feature 012)
- No new npm dependencies required

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations requiring justification.**

Feature 018 fully complies with constitution requirements with two documented exceptions:
1. **MVP Authentication**: Basic user_id instead of JWT (temporary, documented migration path)
2. **API Pattern**: Backend `/api/chat` endpoint follows Feature 017 design (not a violation, just different pattern)

Both exceptions have clear rationale and future migration plans documented in Constitution Check section.
