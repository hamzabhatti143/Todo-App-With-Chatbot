# Implementation Plan: Stateless Chat API Backend

**Branch**: `017-chat-api` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/017-chat-api/spec.md`

**Note**: This plan documents the implementation approach for the FastAPI backend chat API that integrates the Gemini AI agent with database-persisted conversation state.

## Summary

This feature implements a production-ready FastAPI backend with a stateless chat endpoint (`POST /api/chat`) that:
- Accepts natural language messages from authenticated users
- Manages conversation persistence in PostgreSQL via Conversation and Message models
- Integrates TodoBot agent (Feature 016) with MCP task tools (Feature 015)
- Returns AI-generated responses with tool execution details
- Operates without in-memory session state for horizontal scalability

**Technical Approach**: RESTful API using FastAPI with SQLModel ORM, Pydantic validation, JWT authentication, and Gemini 2.0 Flash AI integration through Google's GenerativeAI SDK.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.115.6, SQLModel 0.0.22, Pydantic 2.10.4, google-generativeai 0.8.3, Uvicorn 0.34.0
**Storage**: Neon Serverless PostgreSQL 16 with SQLModel ORM, Alembic migrations
**Testing**: Pytest 8.3.4, httpx 0.28.1 for async testing
**Target Platform**: Linux server (Docker containerized), ASGI server via Uvicorn
**Project Type**: Web backend (monorepo structure: backend/ + frontend/)
**Performance Goals**: <5 seconds p95 for end-to-end request, 100 concurrent requests without degradation
**Constraints**: Stateless architecture (no in-memory session state), 20 message context limit per agent invocation
**Scale/Scope**: Multi-user system with user isolation, horizontal scaling support, conversation history persistence

**Key Integrations**:
- **Feature 016**: TodoBot Gemini AI agent (AgentRequest/AgentResponse interfaces)
- **Feature 015**: MCP Task Server tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Feature 014**: Database models (Conversation, Message tables)
- **Feature 013**: Chat UI frontend integration
- **Authentication**: JWT token validation via get_current_user dependency

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Monorepo Organization ✅ PASS
- **Status**: Compliant
- **Evidence**: Backend implementation in `backend/` directory, frontend in `frontend/`, specs in `specs/017-chat-api/`
- **Notes**: Maintains clear separation of concerns within established monorepo structure

### Principle II: Code Quality Standards ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - Python type hints on all function signatures (routes, agent, schemas)
  - Functions under 30 lines (chat endpoint broken into service calls)
  - DRY principle applied (ConversationService abstracts database operations)
  - Comprehensive error handling with try-catch blocks
  - Clear naming conventions (ChatMessageRequest, TodoBot, get_current_user)
- **Notes**: All quality gates met

### Principle III: Frontend Architecture ⚠️ NOT APPLICABLE
- **Status**: Not applicable to backend-only feature
- **Notes**: Frontend implementation is separate feature (013)

### Principle IV: Backend Architecture ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - SQLModel for all database operations (Conversation, Message models)
  - Pydantic schemas for validation (ChatMessageRequest, ChatMessageResponse)
  - JWT middleware on protected routes (get_current_user dependency)
  - Proper HTTP status codes (200, 201, 400, 401, 403, 404, 500, 503)
  - CORS configured via CORS_ORIGINS environment variable
  - All secrets in environment variables (GEMINI_API_KEY, DATABASE_URL)
- **Notes**: RESTful patterns followed, stateless architecture achieved

### Principle V: Database Standards ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - Neon Serverless PostgreSQL (Feature 014)
  - SQLModel models with `Table=True` (Conversation, Message)
  - Foreign keys enforced (message.conversation_id → conversation.id)
  - Indexes on user_id, conversation_id, created_at
  - Timestamps on all tables (created_at, updated_at)
- **Notes**: Alembic migrations in place from Feature 014

### Principle VI: Authentication Architecture ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - JWT tokens via get_current_user dependency
  - Authorization header required on /api/chat endpoint
  - User isolation enforced (current_user.id checked in ConversationService)
  - 401 returned for invalid/missing tokens
  - User ID from JWT payload used for all operations
- **Notes**: Stateless authentication, no session state

### Principle VII: API Endpoint Structure ⚠️ PARTIAL - DEVIATION JUSTIFIED
- **Status**: Deviation justified
- **Evidence**:
  - Endpoint: `POST /api/chat` (not `/api/{user_id}/chat`)
  - User ID extracted from JWT token (current_user), not URL parameter
- **Justification**:
  - Chat endpoint does not require user_id in URL because user context comes from JWT token
  - Conversation ownership verified through database queries (conversation.user_id == current_user.id)
  - Simpler API contract for frontend (no redundant user_id parameter)
  - Still maintains user isolation through JWT validation
- **Complexity Tracking**: See "Complexity Tracking" section below

### Principle VIII: Spec-Driven Development ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - Feature specification exists (spec.md)
  - Implementation plan being created (this document)
  - Tasks will be generated via /sp.tasks
  - No manual coding outside spec workflow
- **Notes**: Following Spec-Kit Plus workflow

### Principle IX: Agent-Based Development ✅ PASS
- **Status**: Compliant
- **Evidence**:
  - @fastapi-backend-dev agent used for implementation
  - Code structured for agent-driven development
- **Notes**: Specialized agents available for review and documentation

### Principle X: Testing & Quality Gates ⚠️ PENDING
- **Status**: Pending completion
- **Required Actions**:
  - [ ] Type safety validation (mypy on backend code)
  - [ ] Linting (Ruff on backend code)
  - [ ] @code-reviewer approval
  - [ ] Integration test with frontend
  - [ ] JWT flow end-to-end test
  - [ ] User isolation verification test
  - [ ] Documentation updates (README, CLAUDE.md)
- **Notes**: Tests will be created in implementation phase

**Overall Status**: ✅ **APPROVED FOR PHASE 0 RESEARCH** (with 1 justified deviation documented)

## Project Structure

### Documentation (this feature)

```text
specs/017-chat-api/
├── spec.md              # Feature specification (user stories, requirements)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology decisions and patterns
├── data-model.md        # Phase 1: Database schema and models
├── quickstart.md        # Phase 1: Setup and usage guide
├── contracts/           # Phase 1: API contracts (OpenAPI specs)
│   ├── chat-api.yaml   # Chat endpoint contract
│   └── schemas.yaml    # Request/response schemas
└── tasks.md             # Phase 2: Implementation tasks (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Settings and environment variables
│   ├── database.py                  # Database connection and session
│   ├── dependencies.py              # FastAPI dependencies (auth, session)
│   ├── agent.py                     # TodoBot Gemini AI agent
│   │
│   ├── models/                      # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py         # Feature 014
│   │   └── message.py              # Feature 014
│   │
│   ├── schemas/                     # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── chat.py                 # THIS FEATURE
│   │
│   ├── routes/                      # API endpoint routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── conversations.py
│   │   └── chat.py                 # THIS FEATURE
│   │
│   ├── services/                    # Business logic services
│   │   ├── conversation_service.py # Conversation CRUD operations
│   │   └── gemini_service.py       # Gemini API wrapper
│   │
│   ├── mcp_server/                  # MCP Task Server integration (Feature 015)
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── tools.py                # Task management tools
│   │   └── tool_registry.py
│   │
│   └── middleware/                  # Custom middleware
│       ├── logging.py              # Request/response logging
│       └── rate_limit.py           # Rate limiting for chat endpoint
│
├── alembic/                         # Database migrations
│   ├── versions/
│   │   ├── xxx_add_conversations.py
│   │   └── xxx_add_messages.py
│   └── env.py
│
├── tests/                           # Backend tests
│   ├── conftest.py
│   ├── test_chat_endpoints.py      # THIS FEATURE
│   ├── test_conversation_endpoints.py
│   ├── test_agent.py               # THIS FEATURE
│   └── test_auth.py
│
├── requirements.txt                 # Python dependencies
└── .env.example                    # Environment variable template

frontend/                            # Frontend (Feature 013 - separate)
├── app/
│   └── chat/
│       └── page.tsx
├── components/chat/
└── hooks/
    └── use-chat.ts
```

**Structure Decision**: Web application (monorepo) structure selected. Backend implementation in `backend/` with FastAPI routes, SQLModel models, and Pydantic schemas. Frontend in `frontend/` with Next.js App Router. This feature adds chat endpoint (`routes/chat.py`), chat schemas (`schemas/chat.py`), and integrates existing agent (`agent.py`) and database models (`models/conversation.py`, `models/message.py`).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Chat endpoint does not include `{user_id}` in URL path (`POST /api/chat` instead of `POST /api/{user_id}/chat`) | Cleaner API for chat functionality where user context is implicit from authentication | Including `{user_id}` in URL would be redundant when user ID is already extracted from JWT token. The chat endpoint doesn't require explicit user context in the URL because: (1) User is always operating on their own conversations, (2) Conversation ownership is validated in service layer, (3) Frontend doesn't need to construct user-specific URLs, (4) Maintains same security guarantees through JWT validation |

**Post-Implementation Review**: This deviation maintains user isolation security while providing a cleaner API contract. All other endpoints (`/api/{user_id}/tasks`) follow the standard pattern because they operate on explicit user-scoped resources. Chat operates implicitly on the authenticated user's data, making the user_id parameter unnecessary.
