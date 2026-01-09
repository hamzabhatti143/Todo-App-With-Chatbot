<!--
Sync Impact Report:
- Version: 1.0.0 (Initial ratification)
- Principles added: 10 core principles established
- Sections added: Architecture & Stack, Security Standards, Development Workflow, Documentation Requirements
- Templates status:
  ✅ plan-template.md - Constitution Check section aligns with new principles
  ✅ spec-template.md - Requirements structure matches constitution standards
  ✅ tasks-template.md - Task categorization reflects principle-driven workflow
- Follow-up TODOs: None - all placeholders filled
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Monorepo Organization

The project MUST be organized as a monorepo with clear separation of concerns:
- `frontend/` - Next.js 16+ application (App Router)
- `backend/` - FastAPI application
- `specs/` - Spec-Kit Plus specifications organized by type
- `.claude/` - Agent configurations for specialized development
- `docker-compose.yml` - Development environment orchestration

**Rationale**: Monorepo enables atomic cross-stack changes, shared tooling, and unified versioning while maintaining clear boundaries between frontend, backend, and specifications.

### II. Code Quality Standards (NON-NEGOTIABLE)

All code MUST adhere to strict quality standards:
- **TypeScript**: Strict mode enabled, zero `any` types allowed
- **Python**: Type hints mandatory on all function signatures
- **Function Size**: Maximum 30 lines per function
- **DRY Principle**: No code duplication; extract reusable utilities
- **Error Handling**: Comprehensive try-catch with meaningful messages
- **Naming**: Clear, descriptive variable and function names

**Rationale**: These constraints prevent technical debt accumulation and ensure code remains maintainable and reviewable by humans and AI agents.

### III. Frontend Architecture (Next.js 16+)

Frontend MUST follow App Router conventions:
- **Server Components**: Default for all components
- **Client Components**: Only when interactivity required (`'use client'` directive)
- **Styling**: Tailwind CSS exclusively (no inline styles, no CSS modules)
- **API Client**: Centralized client at `lib/api.ts` for all backend calls
- **Forms**: Zod validation for all user inputs
- **State Management**: Loading and error states for every async operation

**Rationale**: Server Components reduce bundle size and improve performance. Centralized API client ensures consistent error handling and JWT token management.

### IV. Backend Architecture (FastAPI)

Backend MUST implement RESTful patterns:
- **ORM**: SQLModel for all database operations
- **Validation**: Pydantic schemas for request/response contracts
- **Authentication**: JWT middleware on all protected routes
- **Status Codes**: Proper HTTP codes (200, 201, 400, 401, 404, 500)
- **CORS**: Configured for frontend origin only
- **Configuration**: Environment variables for all secrets and URLs

**Rationale**: FastAPI's type system integrates with SQLModel and Pydantic for end-to-end type safety. Proper status codes enable clear frontend error handling.

### V. Database Standards

Database layer MUST follow these rules:
- **Provider**: Neon Serverless PostgreSQL exclusively
- **ORM**: SQLModel models with `Table=True`
- **Migrations**: Alembic for all schema changes (version controlled)
- **Constraints**: Foreign keys enforced at database level
- **Indexes**: Required on `user_id` and `created_at` columns
- **Timestamps**: `created_at` and `updated_at` on all tables
- **Soft Deletes**: Implemented where data retention required

**Rationale**: Neon provides serverless scaling. Alembic migrations ensure reproducible schema evolution. Indexes on user_id enable efficient multi-tenant queries.

### VI. Authentication Architecture (NON-NEGOTIABLE)

Authentication MUST use JWT tokens with Better Auth:
- **Frontend**: Better Auth library with JWT plugin enabled
- **Token Storage**: Secure httpOnly cookies (preferred) or localStorage
- **Token Transport**: `Authorization: Bearer <token>` header on all requests
- **Backend Verification**: JWT signature verified with shared `BETTER_AUTH_SECRET`
- **User Isolation**: `user_id` extracted from token and matched with URL parameter
- **Unauthorized Access**: Return 401 status for invalid/missing tokens
- **Token Expiry**: 7 days default with automatic refresh

**Rationale**: JWT enables stateless authentication. Shared secret between frontend/backend ensures trust. User ID matching prevents privilege escalation.

### VII. API Endpoint Structure

All API endpoints MUST follow consistent patterns:
- **Base URL**: `/api/{user_id}/tasks`
- **User Isolation**: All endpoints filtered by authenticated user's ID
- **CRUD Operations**:
  - `GET /api/{user_id}/tasks` - List user's tasks
  - `POST /api/{user_id}/tasks` - Create task
  - `GET /api/{user_id}/tasks/{id}` - Get task detail
  - `PUT /api/{user_id}/tasks/{id}` - Update task
  - `DELETE /api/{user_id}/tasks/{id}` - Delete task
  - `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

**Rationale**: URL-based user_id makes authorization explicit and auditable. RESTful verbs ensure predictable behavior.

### VIII. Spec-Driven Development (NON-NEGOTIABLE)

All development MUST follow Spec-Kit Plus workflow:
1. **Specify**: `/sp.specify` - Create feature specification in `specs/features/`
2. **Plan**: `/sp.plan` - Generate implementation plan with architecture decisions
3. **Tasks**: `/sp.tasks` - Break down into dependency-ordered tasks
4. **Implement**: Use specialized agents (@fastapi-backend-dev, @nextjs-frontend-dev)
5. **Review**: @code-reviewer validates against constitution
6. **Document**: @documentation-writer updates all relevant docs

**Manual coding is prohibited**. All code changes MUST originate from specifications.

**Rationale**: Spec-driven development ensures requirements are captured before implementation, reducing rework and enabling AI agents to work autonomously.

### IX. Agent-Based Development

Development MUST leverage specialized agents:
- **@fastapi-backend-dev**: Backend implementation (FastAPI, SQLModel)
- **@nextjs-frontend-dev**: Frontend implementation (Next.js, TypeScript, Tailwind)
- **@database-architect**: Schema design (PostgreSQL, SQLModel, Alembic)
- **@auth-expert**: Authentication integration (Better Auth, JWT)
- **@code-reviewer**: Full-stack code review against constitution
- **@api-integration-specialist**: Frontend-backend integration testing
- **@documentation-writer**: Documentation maintenance
- **@deployment-specialist**: Environment and deployment configuration

**Auto-invoke Skills**:
- **monorepo-navigation**: Auto-navigate between frontend/backend
- **spec-kit-integration**: Auto-reference specs before implementation
- **jwt-auth-workflow**: Auto-handle JWT authentication patterns

**Rationale**: Specialized agents encode domain expertise and ensure consistent patterns across the codebase.

### X. Testing & Quality Gates

Before marking any feature complete:
- **Type Safety**: TypeScript and Python type checkers MUST pass
- **Linting**: ESLint (frontend) and Ruff (backend) MUST pass with zero warnings
- **Code Review**: @code-reviewer MUST approve implementation
- **Integration Test**: @api-integration-specialist MUST verify frontend-backend flow
- **Authentication Test**: JWT flow MUST work end-to-end
- **User Isolation**: MUST verify user can only access own data
- **Documentation**: MUST update README, CLAUDE.md, and specs

**Rationale**: Quality gates prevent bugs from reaching production and ensure all code meets constitution standards.

## Architecture & Stack

### Technology Stack

**Frontend**:
- Next.js 16+ with App Router
- TypeScript (strict mode)
- Tailwind CSS
- Better Auth (JWT plugin)
- Zod validation

**Backend**:
- Python 3.11+
- FastAPI framework
- SQLModel ORM
- Pydantic schemas
- JWT authentication

**Database**:
- Neon Serverless PostgreSQL
- Alembic migrations

**Development**:
- Docker Compose (local environment)
- Claude Code + Spec-Kit Plus
- Specialized agents (8 agents + 3 skills)

### Project Structure

```
todo-fullstack-web/
├── .claude/                 # Agent configurations
│   ├── agents/             # Development agents
│   ├── subagents/          # Sub-agents (reviewer, docs, etc.)
│   ├── skills/             # Auto-invoke skills
│   └── commands/           # Custom workflows
├── .specify/               # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md # This file
│   ├── templates/          # Spec, plan, tasks templates
│   └── scripts/            # Automation scripts
├── specs/                  # Feature specifications
│   ├── overview.md
│   ├── features/           # Feature specs
│   ├── api/                # API endpoint specs
│   ├── database/           # Schema specs
│   └── ui/                 # UI component specs
├── frontend/               # Next.js application
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── lib/                # API client, utilities
│   └── types/              # TypeScript types
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── models.py       # SQLModel models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # JWT verification
│   │   └── routes/         # API endpoints
│   └── alembic/            # Database migrations
├── docker-compose.yml      # Dev environment
├── CLAUDE.md               # Development workflow
└── README.md               # Project overview
```

## Security Standards

### Authentication Security

- **Secrets**: `BETTER_AUTH_SECRET` MUST be minimum 32 characters
- **Transport**: HTTPS only in production
- **Storage**: Tokens in httpOnly cookies preferred over localStorage
- **Expiry**: 7-day token expiry with automatic refresh
- **Rotation**: Refresh token rotation on every renewal

### API Security

- **CORS**: Whitelist frontend origin only (no wildcards)
- **Validation**: All inputs validated with Pydantic/Zod
- **SQL Injection**: Prevented by SQLModel parameterized queries
- **XSS**: Prevented by React's default escaping
- **CSRF**: Protected via Better Auth CSRF tokens
- **Rate Limiting**: Implement on authentication endpoints

### Data Security

- **User Isolation**: EVERY query MUST filter by `user_id` from JWT token
- **Authorization**: Verify token user_id matches URL user_id parameter
- **Secrets Management**: NO hardcoded secrets; use environment variables
- **Database**: SSL required for all Neon connections
- **Logging**: Never log passwords, tokens, or sensitive user data

## Development Workflow

### Feature Implementation Workflow

1. **Specify**: Create feature specification
   ```
   /sp.specify [feature description]
   ```

2. **Plan**: Generate implementation plan
   ```
   /sp.plan
   ```

3. **Tasks**: Break down into tasks
   ```
   /sp.tasks
   ```

4. **Implement Backend**: Use backend agent
   ```
   @fastapi-backend-dev implement [feature] backend
   ```

5. **Implement Frontend**: Use frontend agent
   ```
   @nextjs-frontend-dev implement [feature] frontend
   ```

6. **Verify Integration**: Test API integration
   ```
   @api-integration-specialist test [feature] integration
   ```

7. **Review Code**: Full-stack code review
   ```
   @code-reviewer review [feature]
   ```

8. **Update Documentation**: Update all docs
   ```
   @documentation-writer update docs for [feature]
   ```

### Environment Setup

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<32+ character secret>
BETTER_AUTH_URL=http://localhost:3000
```

**Backend** (`.env`):
```
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
BETTER_AUTH_SECRET=<same as frontend>
CORS_ORIGINS=http://localhost:3000
```

**CRITICAL**: `BETTER_AUTH_SECRET` MUST be identical in frontend and backend.

### Running the Application

**Full Stack**:
```bash
docker-compose up
```

**Frontend Only**:
```bash
cd frontend && npm run dev
```

**Backend Only**:
```bash
cd backend && uvicorn app.main:app --reload
```

## Documentation Requirements

### Root Documentation

- **README.md**: Project overview, setup instructions, quick start
- **CLAUDE.md**: Development workflow, agent usage, code standards
- **docker-compose.yml**: Local development environment definition

### Frontend Documentation

- **frontend/README.md**: Frontend setup, structure, component patterns
- **frontend/CLAUDE.md**: Component architecture, API client usage, auth patterns
- **Component JSDoc**: All components MUST have JSDoc comments

### Backend Documentation

- **backend/README.md**: Backend setup, structure, API patterns
- **backend/CLAUDE.md**: Model design, authentication, endpoint patterns
- **Endpoint Docstrings**: All endpoints MUST have docstrings
- **OpenAPI**: Auto-generated via FastAPI at `/docs` and `/redoc`

### Spec-Kit Documentation

- **specs/overview.md**: Project summary, architecture overview
- **specs/features/\*.md**: Feature specifications (user stories, requirements)
- **specs/api/\*.md**: API endpoint specifications (contracts, examples)
- **specs/database/\*.md**: Database schema specifications (models, relationships)
- **specs/ui/\*.md**: UI component specifications (wireframes, behavior)

### Documentation Update Policy

After EVERY feature implementation:
1. Update relevant specs in `specs/` folder
2. Update README files if setup changes
3. Update CLAUDE.md if workflow changes
4. Add/update inline documentation (JSDoc, docstrings)
5. Verify OpenAPI docs reflect new endpoints

## Features to Implement

### Phase 1: Authentication
- User signup with email/password
- User signin with JWT token issuance
- Session management with Better Auth
- Protected route middleware
- Logout functionality

### Phase 2: Task Management
- Create task (POST)
- List tasks (GET)
- Get task detail (GET)
- Update task (PUT)
- Delete task (DELETE)
- Toggle task completion (PATCH)

### Phase 3: User Experience
- Responsive UI (mobile, tablet, desktop)
- Loading states for all async operations
- Error messages for validation failures
- Success feedback for completed actions
- Empty states for no tasks

### Phase 4: Data Isolation
- User can only view own tasks
- User can only modify own tasks
- Unauthorized access returns 401
- URL manipulation prevented via JWT verification

All features MUST follow this constitution strictly.

## Governance

### Constitution Authority

This constitution supersedes all other development practices, guidelines, or conventions. When conflicts arise, constitution principles MUST take precedence.

### Amendment Process

1. **Proposal**: Document proposed change with rationale
2. **Impact Analysis**: Identify affected code, specs, and workflows
3. **Migration Plan**: Define steps to bring existing code into compliance
4. **Approval**: Requires explicit user confirmation
5. **Update**: Increment version, update `LAST_AMENDED_DATE`
6. **Propagation**: Update all dependent templates and documentation

### Versioning Policy

Constitution versions follow semantic versioning:
- **MAJOR**: Breaking changes (principle removal/redefinition requiring code changes)
- **MINOR**: New principles or sections added
- **PATCH**: Clarifications, wording improvements, non-breaking refinements

### Compliance Review

**Pre-Implementation**: Every `/sp.plan` MUST include "Constitution Check" section validating compliance.

**Post-Implementation**: Every feature MUST pass @code-reviewer validation against constitution before merge.

**Complexity Justification**: Any violation of constitution principles MUST be documented in plan.md "Complexity Tracking" section with justification and alternatives considered.

### Runtime Guidance

Agents and developers MUST reference `CLAUDE.md` for runtime development guidance. All agent configurations in `.claude/` MUST align with constitution principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
