---
id: 0001
title: Full-Stack Constitution Creation
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "full-stack", "monorepo", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

Create constitution for Full-Stack Todo Web Application monorepo:

**PROJECT STRUCTURE:**
- Monorepo with frontend/ (Next.js 16+) and backend/ (FastAPI)
- Spec-Kit Plus for organized specifications in specs/ folder
- Docker Compose for local development environment

**CODE QUALITY STANDARDS:**
- TypeScript strict mode enabled, no 'any' types
- Python type hints mandatory on all functions
- Functions maximum 30 lines
- No code duplication (DRY principle)
- Proper error handling everywhere
- Clear variable and function names

**FRONTEND STANDARDS (Next.js 16+):**
- App Router architecture only
- Server Components by default
- Client Components only for interactivity ('use client')
- TypeScript for all files
- Tailwind CSS for all styling (no inline styles, no CSS modules)
- API calls through centralized client (lib/api.ts)
- Better Auth for authentication with JWT tokens
- Zod for form validation
- Proper loading and error states

**BACKEND STANDARDS (FastAPI):**
- RESTful API design with proper HTTP methods
- SQLModel ORM for all database operations
- Pydantic schemas for request/response validation
- JWT authentication middleware on protected routes
- User data isolation (filter all queries by user_id)
- Proper status codes (200, 201, 400, 401, 404, 500)
- CORS configuration for frontend origin
- Environment variables for all configuration

**DATABASE STANDARDS:**
- Neon Serverless PostgreSQL
- SQLModel for models and queries
- Alembic for migrations
- Proper foreign key constraints
- Indexes on frequently queried columns (user_id, created_at)
- Timestamps (created_at, updated_at) on all tables
- Soft deletes where appropriate

**AUTHENTICATION ARCHITECTURE:**
- Better Auth on frontend with JWT plugin enabled
- JWT tokens in Authorization: Bearer <token> header
- Backend verifies JWT with shared BETTER_AUTH_SECRET
- Extract user_id from token and match with URL parameter
- Return 401 Unauthorized for invalid/missing tokens
- Token expiry: 7 days default

**API ENDPOINT STRUCTURE:**
- Base: /api/{user_id}/tasks
- All endpoints require JWT authentication
- User can only access their own data
- Endpoints: GET (list), POST (create), GET /{id} (detail), PUT /{id} (update), DELETE /{id} (delete), PATCH /{id}/complete (toggle)

**DEVELOPMENT WORKFLOW:**
- Spec-driven development only via Spec-Kit Plus
- No manual coding allowed
- Workflow: /specify → /plan → /tasks → /implement
- Use @fastapi-backend-dev for backend
- Use @nextjs-frontend-dev for frontend
- Use @database-architect for schema
- Use @auth-expert for authentication
- Use @code-reviewer after implementation
- Use @documentation-writer for docs

**DOCUMENTATION REQUIREMENTS:**
- Root README.md with project overview
- CLAUDE.md with development workflow
- Frontend README.md and CLAUDE.md
- Backend README.md and CLAUDE.md
- Specs in specs/ folder organized by type
- Inline docstrings for all functions
- API documentation via FastAPI OpenAPI

**FEATURES TO IMPLEMENT:**
1. User Authentication (signup, signin, session management)
2. Task CRUD Operations (create, read, update, delete)
3. Task Completion Toggle
4. User Data Isolation
5. Responsive UI

All features must follow this constitution strictly.

## Response snapshot

Created comprehensive constitution (v1.0.0) for Full-Stack Todo Web Application with:
- 10 core principles (5 marked NON-NEGOTIABLE)
- Architecture & Stack section with complete technology specifications
- Security Standards covering authentication, API, and data security
- Development Workflow with 8-step feature implementation process
- Documentation Requirements for all layers (root, frontend, backend, specs)
- Features to Implement organized in 4 phases
- Governance section with amendment process and versioning policy

Key principles established:
- Monorepo organization (frontend/backend separation)
- Code quality standards (TypeScript strict, Python type hints, max 30 lines/function)
- Frontend architecture (Next.js 16+ App Router, Server Components, Tailwind CSS)
- Backend architecture (FastAPI, SQLModel, Pydantic schemas, JWT auth)
- Database standards (Neon PostgreSQL, Alembic migrations, proper indexing)
- Authentication architecture (Better Auth + JWT, user isolation, 401 on unauthorized)
- API endpoint structure (RESTful, /api/{user_id}/tasks pattern)
- Spec-driven development workflow (prohibits manual coding)
- Agent-based development (8 specialized agents + 3 auto-invoke skills)
- Testing & quality gates (type safety, linting, code review, integration tests)

All templates validated for alignment with constitution principles.

## Outcome

- ✅ Impact: Constitution v1.0.0 ratified, establishes project governance and technical standards for full-stack development
- 🧪 Tests: N/A (constitution document, not code)
- 📁 Files: Created .specify/memory/constitution.md with complete principles and governance
- 🔁 Next prompts: /sp.specify for first feature specification (likely authentication or task CRUD)
- 🧠 Reflection: Constitution successfully integrates Spec-Kit Plus workflow with specialized agent ecosystem, ensures consistency across frontend/backend, and enforces security-first approach via JWT authentication and user isolation

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders filled, templates validated, governance established
- Graders run and results (PASS/FAIL): PASS - Constitution complete, versioned, and propagated to templates
- Prompt variant (if applicable): Standard /sp.constitution command with comprehensive user requirements
- Next experiment (smallest change to try): Monitor first feature specification to validate constitution principles are clear and actionable
