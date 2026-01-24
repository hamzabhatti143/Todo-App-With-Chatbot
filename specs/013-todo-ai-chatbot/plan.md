# Implementation Plan: Todo AI Chatbot

**Branch**: `013-todo-ai-chatbot` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/013-todo-ai-chatbot/spec.md`

## Summary

Build a conversational AI-powered todo application that enables users to manage tasks through natural language chat. The system uses Gemini 2.0 Flash AI agent with MCP (Model Context Protocol) tools for task operations, OpenAI ChatKit for the frontend chat UI, FastAPI backend with stateless architecture, and PostgreSQL for persistent storage of tasks and conversation history. Users authenticate via Better Auth with JWT tokens, ensuring complete data isolation between users.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.7.2 (strict mode) + Node.js 18+
- Backend: Python 3.10+ with type hints

**Primary Dependencies**:
- Frontend: Next.js 16.0.10 (App Router), OpenAI ChatKit, Axios, Better Auth, Tailwind CSS
- Backend: FastAPI 0.115.6, Gemini 2.0 Flash SDK, MCP SDK 0.5.0, SQLModel 0.0.22, OpenAI Agents SDK 1.0.0

**Storage**:
- Neon Serverless PostgreSQL (PostgreSQL 16)
- Tables: users, tasks, conversations, messages
- Migrations: Alembic 1.14.0

**Testing**:
- Backend: pytest with httpx for async tests
- Frontend: React Testing Library (future)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge) - mobile responsive (375px+)
- Backend: Linux server with Python 3.10+ runtime

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- Task creation: < 3 seconds end-to-end
- Task listing: < 2 seconds
- Task completion: < 2 seconds
- AI intent recognition: 90% accuracy
- Concurrent users: 100 without degradation > 5 seconds

**Constraints**:
- Stateless backend (no in-memory sessions)
- Database-only state persistence
- JWT token expiration: 30 minutes (configurable)
- Message length limit: 5000 characters
- Task title: 200 characters max
- Task description: 1000 characters max
- Mobile-first responsive design (min width 375px)

**Scale/Scope**:
- MVP for 100+ concurrent users
- Multi-tenant with complete user isolation
- English language only (no i18n in MVP)
- Single-region deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Monorepo Organization ✅

**Status**: COMPLIANT

This feature adds a new AI chatbot system alongside the existing todo app monorepo. The structure maintains clear separation:
- `frontend/` - Next.js ChatKit UI (new chat components added)
- `backend/` - FastAPI with MCP tools and Gemini agent (new modules added)
- `specs/013-todo-ai-chatbot/` - This feature's specifications
- `.claude/` - Agent configurations remain unchanged
- `docker-compose.yml` - Will be extended for development environment

**Rationale**: Monorepo structure preserved. New chat features integrate into existing frontend/backend folders.

### Principle II: Code Quality Standards (NON-NEGOTIABLE) ✅

**Status**: COMPLIANT

All code will adhere to strict quality standards:
- **TypeScript**: Strict mode enabled, zero `any` types
- **Python**: Type hints mandatory on all MCP tools, FastAPI endpoints, and Gemini agent integration
- **Function Size**: Maximum 30 lines (enforced in code review)
- **DRY Principle**: MCP tools are reusable, API client centralized
- **Error Handling**: Comprehensive try-catch for Gemini API calls, database operations, and ChatKit integration
- **Naming**: Clear names like `create_task_tool`, `GeminiAgentService`, `ChatMessage`

**Rationale**: Quality standards ensure maintainability. AI agent integration requires careful error handling.

### Principle III: Frontend Architecture (Next.js 16+) ⚠️ PARTIAL DEVIATION

**Status**: COMPLIANT with clarification

- **Server Components**: ChatKit requires client components for interactivity (`'use client'` directive)
- **Styling**: Tailwind CSS exclusively (ChatKit styled with Tailwind)
- **API Client**: Centralized at `lib/api.ts` for chat and task endpoints
- **Forms**: Zod validation for chat message input
- **State Management**: Loading states for AI responses, error states for API failures

**Clarification**: OpenAI ChatKit is inherently a client component library (requires browser interactivity for chat). This is justified as chat UI cannot be server-rendered. All non-chat components will remain server components.

**Rationale**: Chat interfaces require client-side state (messages, typing indicators, real-time updates). Server Components used everywhere else.

### Principle IV: Backend Architecture (FastAPI) ✅

**Status**: COMPLIANT

- **ORM**: SQLModel for all database operations (users, tasks, conversations, messages)
- **Validation**: Pydantic schemas for chat messages, task operations, and agent responses
- **Authentication**: JWT middleware on `/api/chat` endpoints
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Internal Server Error)
- **CORS**: Configured for frontend origin only
- **Configuration**: Environment variables for GEMINI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET

**Rationale**: FastAPI's async support ideal for AI agent calls. Pydantic integrates with MCP tool definitions.

### Principle V: Database Standards ✅

**Status**: COMPLIANT

- **Provider**: Neon Serverless PostgreSQL (existing database extended)
- **ORM**: SQLModel models with `Table=True`
- **Migrations**: Alembic for new tables (conversations, messages)
- **Constraints**: Foreign keys (conversations → users, messages → conversations, tasks → users)
- **Indexes**: `user_id` on conversations and tasks, `conversation_id` on messages
- **Timestamps**: `created_at` and `updated_at` on all tables
- **Soft Deletes**: Not required for MVP

**Rationale**: Extends existing database schema. Conversation history requires two new tables.

### Principle VI: Authentication Architecture (NON-NEGOTIABLE) ✅

**Status**: COMPLIANT

- **Frontend**: Better Auth with JWT plugin (existing auth reused)
- **Token Storage**: httpOnly cookies (existing implementation)
- **Token Transport**: `Authorization: Bearer <token>` header on all `/api/chat` requests
- **Backend Verification**: JWT signature verified with `BETTER_AUTH_SECRET`
- **User Isolation**: `user_id` extracted from token, all queries filter by user_id
- **Unauthorized Access**: 401 for invalid/missing tokens
- **Token Expiry**: 30 minutes (configurable)

**Rationale**: Reuses existing auth system. Chat endpoints protected like task endpoints.

### Principle VII: API Endpoint Structure ⚠️ DEVIATION JUSTIFIED

**Status**: PARTIAL DEVIATION (justified)

**Existing pattern**: `/api/{user_id}/tasks`

**New pattern for chat**: `/api/chat` (no user_id in URL)

**Justification**:
- Chat endpoint is stateless - user_id extracted from JWT token only
- No specific resource ID in URL (messages are created on-the-fly)
- Conversation history retrieved via JWT user_id, not URL parameter

**New endpoints**:
- `POST /api/chat` - Send message, receive AI response (user_id from JWT)
- `GET /api/conversations/{conversation_id}` - Retrieve conversation history (user_id from JWT)
- `GET /api/conversations` - List user's conversations (user_id from JWT)

**User isolation maintained**: All endpoints verify JWT user_id matches conversation owner or task owner.

**Rationale**: Chat interface uses JWT-only user identification (no URL parameter). This is more RESTful for chat resources.

### Principle VIII: Spec-Driven Development (NON-NEGOTIABLE) ✅

**Status**: COMPLIANT

This plan follows the workflow:
1. ✅ **Specify**: `/sp.specify` completed - spec.md created
2. ✅ **Plan**: `/sp.plan` in progress - this plan.md
3. ⏳ **Tasks**: `/sp.tasks` next - tasks.md to be generated
4. ⏳ **Implement**: Will use @fastapi-backend-dev and @nextjs-frontend-dev
5. ⏳ **Review**: @code-reviewer will validate against constitution
6. ⏳ **Document**: @documentation-writer will update README and CLAUDE.md

**Rationale**: Following spec-driven workflow. No manual coding planned.

### Principle IX: Agent-Based Development ✅

**Status**: COMPLIANT

Agents to be used:
- **@database-architect**: Design conversations and messages tables
- **@fastapi-backend-dev**: Implement MCP tools, Gemini agent integration, chat endpoints
- **@nextjs-frontend-dev**: Integrate OpenAI ChatKit, create chat UI components
- **@auth-expert**: Extend JWT middleware to chat endpoints
- **@code-reviewer**: Review full implementation
- **@api-integration-specialist**: Test chat → backend → Gemini → MCP tools flow
- **@documentation-writer**: Update README, CLAUDE.md with ChatKit and Gemini setup

**Skills**:
- **monorepo-navigation**: Navigate between frontend/backend
- **jwt-auth-workflow**: Apply JWT patterns to chat endpoints

**Rationale**: Specialized agents ensure consistency. @database-architect critical for conversation schema.

### Principle X: Testing & Quality Gates ✅

**Status**: COMPLIANT

Quality gates for this feature:
- **Type Safety**: TypeScript strict mode (frontend), Python type hints (backend MCP tools)
- **Linting**: ESLint (frontend), Ruff (backend)
- **Code Review**: @code-reviewer validates MCP tool implementation and ChatKit integration
- **Integration Test**: @api-integration-specialist tests chat message → Gemini → task creation flow
- **Authentication Test**: JWT flow with chat endpoints
- **User Isolation**: Verify user A cannot access user B's conversations or tasks via chat
- **Documentation**: Update README with Gemini API key setup, ChatKit domain key configuration

**Rationale**: Same quality gates as existing features. AI agent integration adds complexity requiring thorough testing.

### Constitution Compliance Summary

**Compliant**: 8/10 principles fully compliant
**Deviations**: 2 justified deviations
  1. **Principle III (Frontend)**: ChatKit requires client components (justified - chat UI cannot be server-rendered)
  2. **Principle VII (API structure)**: Chat endpoint uses JWT-only user identification (justified - more RESTful for chat resources)

**Overall Status**: ✅ APPROVED to proceed

All deviations are architecturally sound and documented. No violations of NON-NEGOTIABLE principles.

## Project Structure

### Documentation (this feature)

```text
specs/013-todo-ai-chatbot/
├── spec.md                # Feature specification (completed)
├── plan.md                # This file (in progress)
├── research.md            # Phase 0: Technology research and decisions
├── data-model.md          # Phase 1: Database schema for conversations/messages
├── quickstart.md          # Phase 1: Setup instructions for Gemini & ChatKit
├── contracts/             # Phase 1: API contracts
│   ├── chat.openapi.yaml  # Chat endpoint contract
│   └── mcp-tools.json     # MCP tool definitions
├── checklists/            # Quality validation checklists
│   └── requirements.md    # Specification checklist (completed)
└── tasks.md               # Phase 2: Generated by /sp.tasks command
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── user.py              # Existing user model
│   │   ├── task.py              # Existing task model
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── schemas/
│   │   ├── auth.py              # Existing auth schemas
│   │   ├── task.py              # Existing task schemas
│   │   ├── chat.py              # NEW: Chat message schemas
│   │   └── conversation.py      # NEW: Conversation schemas
│   ├── services/
│   │   ├── auth.py              # Existing JWT verification
│   │   ├── task_service.py      # Existing task CRUD
│   │   ├── gemini_agent.py      # NEW: Gemini AI agent service
│   │   ├── mcp_server.py        # NEW: MCP tool server
│   │   └── conversation_service.py # NEW: Conversation persistence
│   ├── routes/
│   │   ├── auth.py              # Existing auth endpoints
│   │   ├── tasks.py             # Existing task endpoints
│   │   ├── chat.py              # NEW: Chat endpoints
│   │   └── conversations.py     # NEW: Conversation retrieval
│   ├── mcp_tools/
│   │   ├── __init__.py          # NEW: MCP tools package
│   │   ├── add_task.py          # NEW: Add task MCP tool
│   │   ├── list_tasks.py        # NEW: List tasks MCP tool
│   │   ├── complete_task.py     # NEW: Complete task MCP tool
│   │   ├── update_task.py       # NEW: Update task MCP tool
│   │   └── delete_task.py       # NEW: Delete task MCP tool
│   ├── main.py                  # Existing FastAPI app (extend with chat routes)
│   └── config.py                # Existing config (add GEMINI_API_KEY)
├── alembic/
│   └── versions/
│       └── 003_add_conversations_messages.py # NEW: Migration for chat tables
├── tests/
│   ├── test_auth.py             # Existing auth tests
│   ├── test_tasks.py            # Existing task tests
│   ├── test_chat.py             # NEW: Chat endpoint tests
│   ├── test_mcp_tools.py        # NEW: MCP tool tests
│   └── test_gemini_agent.py     # NEW: Gemini agent tests
├── requirements.txt             # Extend with google-generativeai, mcp-sdk, openai agents
└── .env.example                 # Add GEMINI_API_KEY

frontend/
├── app/
│   ├── (auth)/
│   │   ├── signin/page.tsx      # Existing sign in
│   │   └── signup/page.tsx      # Existing sign up
│   ├── dashboard/
│   │   └── page.tsx             # Existing task dashboard
│   ├── chat/
│   │   └── page.tsx             # NEW: Chat interface page
│   └── layout.tsx               # Existing root layout
├── components/
│   ├── ui/
│   │   ├── button.tsx           # Existing
│   │   ├── input.tsx            # Existing
│   │   └── card.tsx             # Existing
│   ├── chat/
│   │   ├── ChatInterface.tsx    # NEW: OpenAI ChatKit wrapper
│   │   ├── ChatMessage.tsx      # NEW: Individual message component
│   │   ├── ChatInput.tsx        # NEW: Message input component
│   │   └── TaskDisplay.tsx      # NEW: Inline task display in chat
│   └── tasks/
│       └── TaskList.tsx         # Existing task list
├── lib/
│   ├── api.ts                   # Existing API client (extend with chat methods)
│   ├── auth.ts                  # Existing Better Auth config
│   ├── chatkit-config.ts        # NEW: ChatKit configuration
│   └── utils.ts                 # Existing utilities
├── types/
│   ├── auth.ts                  # Existing auth types
│   ├── task.ts                  # Existing task types
│   ├── chat.ts                  # NEW: Chat message types
│   └── conversation.ts          # NEW: Conversation types
├── package.json                 # Extend with @openai/chatkit, google-generativeai types
└── .env.local.example           # Add NEXT_PUBLIC_CHATKIT_DOMAIN_KEY

docker-compose.yml               # Extend with environment variables for Gemini API key
README.md                        # Update with ChatKit and Gemini setup instructions
CLAUDE.md                        # Update with AI agent development patterns
```

**Structure Decision**: Web application monorepo structure. This feature extends the existing todo app monorepo by adding chat capabilities to both frontend and backend. New directories created:
- `backend/app/mcp_tools/` for MCP tool implementations
- `backend/app/services/gemini_agent.py` for AI agent integration
- `frontend/components/chat/` for ChatKit components
- `frontend/app/chat/` for chat page

Existing structures preserved:
- `backend/app/models/`, `backend/app/routes/` extended with new files
- `frontend/components/`, `frontend/lib/` extended with new utilities
- `specs/` follows Spec-Kit Plus conventions

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **ChatKit client components** (Principle III) | OpenAI ChatKit is a client-side library that requires browser interactivity for chat UI (messages, typing indicators, WebSocket connections) | Server Components cannot handle real-time chat interactions. ChatKit's architecture requires client-side state management. Alternative would be building custom chat UI from scratch (not in scope per spec). |
| **Chat endpoint pattern** (Principle VII) | Chat is a stateless resource where user_id is only in JWT token, not URL. Conversation history uses `/api/conversations/{id}` pattern. | Including user_id in URL for chat (`/api/{user_id}/chat`) is redundant and non-RESTful. Chat messages are not user-scoped resources in the URL - they're conversation-scoped. User isolation enforced via JWT verification. |

**Alternatives Considered**:
1. **Custom chat UI**: Rejected - building from scratch increases scope significantly. ChatKit provides production-ready chat UI with proper accessibility and mobile support.
2. **WebSocket-based chat**: Rejected - spec explicitly states stateless server architecture. ChatKit works with REST APIs (polling or HTTP streaming).
3. **URL-based user_id for chat**: Rejected - RESTful design principle states resources should be identified by URL, but chat messages belong to conversations, not users. User ownership verified via JWT.

## Phase 0: Research & Technology Decisions

**Prerequisites**: Constitution Check passed

**Unknowns to Research**:
1. OpenAI ChatKit integration patterns with Next.js App Router
2. Gemini 2.0 Flash SDK for Python (google-generativeai library)
3. MCP (Model Context Protocol) SDK 0.5.0 implementation patterns
4. OpenAI Agents SDK integration with Gemini models
5. Better Auth JWT integration with chat endpoints
6. Conversation history database schema design
7. Rate limiting strategies for AI agent endpoints
8. Error handling patterns for Gemini API failures

**Research Tasks**:
1. Research OpenAI ChatKit setup and configuration with domain allowlist
2. Research Gemini 2.0 Flash Python SDK (google-generativeai) for chat applications
3. Research MCP SDK 0.5.0 tool definition and registration patterns
4. Research OpenAI Agents SDK compatibility with Gemini models
5. Investigate Alembic migration strategy for adding conversation tables
6. Research rate limiting libraries for FastAPI (slowapi or fastapi-limiter)
7. Review best practices for handling long-running AI agent requests
8. Investigate conversation context management for multi-turn conversations

**Output**: `research.md` with decisions, rationale, and code examples for each technology.

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

### Data Model Design

**Output**: `data-model.md`

**Entities to Model**:

1. **User** (existing - extend)
   - Relationships: one-to-many with Conversations and Tasks

2. **Task** (existing - no changes)
   - Already has user_id foreign key

3. **Conversation** (new)
   - Fields: id (UUID), user_id (FK to users), created_at, updated_at
   - Relationships: one-to-many with Messages
   - Indexes: user_id (for user conversation list)

4. **Message** (new)
   - Fields: id (UUID), conversation_id (FK to conversations), role (enum: user/assistant), content (text, max 5000 chars), created_at
   - Relationships: many-to-one with Conversation
   - Indexes: conversation_id (for message history retrieval), created_at (for ordering)

5. **MCP Tool** (logical entity - not a database table)
   - Tool definitions: add_task, list_tasks, complete_task, update_task, delete_task
   - Each tool specifies input schema (Pydantic model) and output schema
   - Tools registered with Gemini agent at startup

**Validation Rules**:
- Message content: 1-5000 characters (enforced by Pydantic)
- Conversation user_id: Must match JWT user_id (enforced in API layer)
- Task operations via MCP tools: Must filter by user_id from conversation context

**State Transitions**:
- Conversation: created → active (on first message)
- Message: created (immutable - no updates or deletes in MVP)

### API Contracts

**Output**: `contracts/`

**Contracts to Generate**:

1. **`contracts/chat.openapi.yaml`** - Chat endpoints
   - POST /api/chat - Send message and receive AI response
   - GET /api/conversations - List user's conversations
   - GET /api/conversations/{conversation_id} - Retrieve conversation history

2. **`contracts/mcp-tools.json`** - MCP tool definitions
   - add_task tool: input (title, description), output (task object)
   - list_tasks tool: input (none), output (task array)
   - complete_task tool: input (task_id), output (updated task object)
   - update_task tool: input (task_id, title, description), output (updated task object)
   - delete_task tool: input (task_id), output (success boolean)

**OpenAPI Schema Patterns**:
- Authentication: `securitySchemes: { bearerAuth: { type: http, scheme: bearer } }`
- Error responses: 400 (validation), 401 (unauthorized), 500 (server error)
- Success responses: 200 (OK), 201 (created)

### Quickstart Guide

**Output**: `quickstart.md`

**Sections**:
1. **Prerequisites**: Node.js 18+, Python 3.10+, PostgreSQL (Neon account)
2. **Environment Setup**: Copy .env.example files, configure API keys
3. **Gemini API Key**: Obtain from Google AI Studio, add to backend/.env
4. **OpenAI ChatKit Domain Key**: Obtain from OpenAI, add to frontend/.env.local
5. **Database Setup**: Run Alembic migrations for conversation tables
6. **Install Dependencies**: npm install (frontend), pip install (backend)
7. **Run Development Servers**: npm run dev (frontend), uvicorn (backend)
8. **Test Chat Interface**: Navigate to /chat, send test message, verify task creation

### Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**New Technology to Add**:
- OpenAI ChatKit (chat UI library)
- Gemini 2.0 Flash (AI model)
- MCP SDK 0.5.0 (Model Context Protocol)
- OpenAI Agents SDK 1.0.0 (agent orchestration)
- google-generativeai (Python SDK)

**Preserve Manual Additions**: Existing agent context for Better Auth, SQLModel, FastAPI remains unchanged.

## Phase 2: Task Generation (Not Part of /sp.plan)

**Next Command**: `/sp.tasks`

The `/sp.tasks` command will read this plan and generate:
- `tasks.md` with dependency-ordered implementation tasks
- Tasks will be grouped by component (database, backend MCP tools, backend routes, frontend components, integration)
- Each task will reference this plan's design decisions

**Task Categories Expected**:
1. Database migrations (Alembic)
2. Backend MCP tool implementations
3. Backend Gemini agent service
4. Backend chat API routes
5. Frontend ChatKit integration
6. Frontend chat UI components
7. Integration testing
8. Documentation updates

## Next Steps

1. Execute Phase 0 research (create `research.md`)
2. Execute Phase 1 design (create `data-model.md`, `contracts/`, `quickstart.md`)
3. Update agent context with new technology stack
4. Re-run Constitution Check to verify design compliance
5. Run `/sp.tasks` to generate implementation tasks
6. Assign tasks to specialized agents (@database-architect, @fastapi-backend-dev, @nextjs-frontend-dev)

This plan provides a complete implementation roadmap while adhering to the project constitution. All design decisions are documented and justified.
