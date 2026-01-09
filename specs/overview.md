# Project Architecture Overview

**Project**: Todo Full-Stack Web Application
**Version**: 1.0.0
**Last Updated**: 2025-12-30
**Status**: Production Ready

## Executive Summary

A modern, production-ready multi-user todo application demonstrating best practices in full-stack web development. Built using specification-driven development with Claude Code and Spec-Kit Plus, this project showcases end-to-end type safety, secure authentication, user isolation, and responsive design.

## Project Vision

Create a maintainable, secure, and scalable todo application that serves as both a functional product and a reference implementation for:
- Spec-driven development methodology
- Full-stack TypeScript/Python integration
- JWT authentication with user isolation
- Mobile-first responsive design
- AI-assisted development workflows

## Technology Stack

### Frontend Architecture

**Framework**: Next.js 15.1.0 with App Router
- **Why**: Server Components reduce client-side JavaScript, improving performance and SEO
- **Benefits**: Built-in routing, API routes, image optimization, and TypeScript support

**Language**: TypeScript 5.7.2 (Strict Mode)
- **Why**: Compile-time type safety prevents runtime errors
- **Benefits**: Better IDE support, refactoring confidence, self-documenting code

**Styling**: Tailwind CSS 4.0.0
- **Why**: Utility-first approach eliminates CSS file management
- **Benefits**: Rapid development, consistent design system, automatic purging of unused styles

**Authentication**: Better Auth 1.0.7 with JWT Plugin
- **Why**: Modern authentication library designed for Next.js
- **Benefits**: Built-in JWT support, session management, extensible architecture

**Validation**: Zod 3.24.1
- **Why**: Type-safe schema validation with TypeScript inference
- **Benefits**: Runtime validation matches TypeScript types, clear error messages

**HTTP Client**: Axios 1.7.9
- **Why**: Interceptors for auth tokens, better error handling than fetch
- **Benefits**: Request/response transformation, automatic JSON parsing

### Backend Architecture

**Framework**: FastAPI 0.115.6
- **Why**: High-performance async Python framework with automatic OpenAPI docs
- **Benefits**: Native async/await, Pydantic integration, excellent type support

**Language**: Python 3.11+
- **Why**: Modern Python with enhanced type hints and performance improvements
- **Benefits**: Pattern matching, better error messages, faster execution

**ORM**: SQLModel 0.0.22
- **Why**: Combines SQLAlchemy and Pydantic for type-safe database operations
- **Benefits**: Single model definition for DB and API schemas, async support

**Database**: PostgreSQL 16
- **Why**: Robust ACID compliance, JSON support, excellent performance
- **Benefits**: Data integrity, complex queries, proven reliability

**Migrations**: Alembic 1.14.0
- **Why**: Industry standard for SQLAlchemy-based migrations
- **Benefits**: Version control for database schema, rollback capability

**Authentication**: python-jose 3.3.0 + Passlib 1.7.4
- **Why**: JWT token creation/verification and secure password hashing
- **Benefits**: Stateless authentication, bcrypt hashing with automatic salting

**Server**: Uvicorn 0.34.0
- **Why**: Lightning-fast ASGI server for FastAPI
- **Benefits**: WebSocket support, async request handling

### Development Tools

**Containerization**: Docker Compose
- **Why**: Consistent development environment across all machines
- **Benefits**: Isolated services, easy onboarding, production parity

**AI Development**: Claude Code + Spec-Kit Plus
- **Why**: AI-assisted specification-driven development
- **Benefits**: Faster development, comprehensive documentation, consistent code quality

**Testing**: Pytest 8.3.4 + httpx 0.28.1
- **Why**: Async test support for FastAPI applications
- **Benefits**: 62/62 tests passing, integration test coverage

**Code Quality**: ESLint + Ruff + MyPy
- **Why**: Automated code quality enforcement
- **Benefits**: Consistent style, early error detection

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                      (Mobile/Desktop)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ App Router (Server Components + Client Components)       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Authentication (Better Auth + JWT)                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ API Client (Axios with Interceptors)                     │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ UI Components (Tailwind CSS)                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ REST API (JSON)
                         │ Authorization: Bearer <JWT>
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ CORS Middleware (Origin Validation)                      │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ JWT Authentication Dependency                            │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ API Routes (RESTful Endpoints)                           │  │
│  │  - /api/auth/* (register, login)                         │  │
│  │  - /api/{user_id}/tasks/* (CRUD operations)              │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Pydantic Schemas (Request/Response Validation)           │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ SQLModel ORM (Database Abstraction)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ SQL Queries (Parameterized)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Tables:                                                   │  │
│  │  - users (id, email, hashed_password, created_at)        │  │
│  │  - tasks (id, title, description, completed, user_id,    │  │
│  │           created_at, updated_at)                        │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Indexes:                                                  │  │
│  │  - user_id (tasks table)                                 │  │
│  │  - title (tasks table)                                   │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Constraints:                                              │  │
│  │  - Foreign key: tasks.user_id → users.id                 │  │
│  │  - Unique: users.email                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

#### Authentication Flow

```
1. User Registration:
   Browser → POST /api/auth/register {email, password}
   Backend → Hash password with bcrypt
   Backend → Store user in database
   Backend → Auto-login user
   Backend → Return JWT token
   Frontend → Store token in localStorage
   Frontend → Redirect to dashboard

2. User Login:
   Browser → POST /api/auth/login {email, password}
   Backend → Verify password hash
   Backend → Create JWT with user_id in payload
   Backend → Return {access_token, token_type}
   Frontend → Store token in localStorage
   Frontend → Decode token to extract user_id
   Frontend → Redirect to dashboard

3. Authenticated Request:
   Frontend → Axios interceptor adds Authorization header
   Backend → Extract JWT from header
   Backend → Verify signature with SECRET_KEY
   Backend → Extract user_id from token payload
   Backend → Compare with URL parameter user_id
   Backend → Return 403 if mismatch, 401 if invalid token
```

#### Task Management Flow

```
1. List Tasks:
   Frontend → GET /api/{user_id}/tasks
   Backend → Verify JWT, extract user_id
   Backend → Query: SELECT * FROM tasks WHERE user_id = ?
   Backend → Return task list as JSON
   Frontend → Render in UI with filters

2. Create Task:
   Frontend → Validate with Zod schema
   Frontend → POST /api/{user_id}/tasks {title, description}
   Backend → Validate with Pydantic schema
   Backend → Create task with user_id from JWT
   Backend → Return created task (201 status)
   Frontend → Add to local state, show success message

3. Toggle Completion:
   Frontend → PATCH /api/{user_id}/tasks/{task_id}/complete
   Backend → Verify ownership (task.user_id == JWT.user_id)
   Backend → Update completed field
   Backend → Return updated task
   Frontend → Update UI immediately

4. Update Task:
   Frontend → PUT /api/{user_id}/tasks/{task_id} {title, description}
   Backend → Verify ownership
   Backend → Update fields, set updated_at
   Backend → Return updated task
   Frontend → Close edit form, update display

5. Delete Task:
   Frontend → Show confirmation dialog
   Frontend → DELETE /api/{user_id}/tasks/{task_id}
   Backend → Verify ownership
   Backend → Delete from database (204 status)
   Frontend → Remove from UI
```

### Security Architecture

#### Authentication & Authorization

1. **Password Security**
   - Hashed with bcrypt (cost factor 12)
   - Automatic salt generation
   - Constant-time comparison prevents timing attacks

2. **JWT Token Security**
   - HS256 algorithm (HMAC-SHA256)
   - Shared secret between frontend and backend
   - 30-minute expiration (configurable)
   - Payload contains user_id in `sub` claim

3. **User Isolation**
   - Every endpoint checks: `JWT.user_id == URL.user_id`
   - Database queries filter by user_id: `WHERE user_id = ?`
   - 403 Forbidden returned for unauthorized access attempts

4. **Input Validation**
   - Frontend: Zod schemas validate before submission
   - Backend: Pydantic schemas validate on every request
   - Double validation prevents malicious client bypasses

5. **SQL Injection Prevention**
   - SQLModel uses parameterized queries automatically
   - No raw SQL in application code
   - ORM layer provides abstraction

6. **XSS Prevention**
   - React escapes all content by default
   - No `dangerouslySetInnerHTML` usage
   - Backend could add HTML entity escaping (defense-in-depth)

7. **CORS Protection**
   - Whitelist-only origins (no `*`)
   - Configured via environment variable
   - Credentials allowed for cookie support

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_users_email ON users(email);
```

**Fields**:
- `id` - UUID primary key, automatically generated
- `email` - Unique email address for login
- `hashed_password` - Bcrypt hash of user's password
- `created_at` - Account creation timestamp

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_title ON tasks(title);
```

**Fields**:
- `id` - UUID primary key
- `title` - Task title (max 200 characters)
- `description` - Optional description (max 1000 characters)
- `completed` - Boolean flag for completion status
- `user_id` - Foreign key to users table
- `created_at` - Task creation timestamp
- `updated_at` - Last modification timestamp

**Relationships**:
- One-to-many: User → Tasks (one user has many tasks)
- Cascade delete: Deleting user deletes all their tasks

**Indexes**:
- `user_id` - Optimizes user-specific queries (primary access pattern)
- `title` - Enables future search functionality

## API Reference

### Authentication Endpoints

#### POST /api/auth/register

Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2025-12-30T12:00:00Z"
}
```

**Errors**:
- 400: Email already registered
- 422: Invalid email format or weak password

#### POST /api/auth/login

Authenticate and receive JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errors**:
- 401: Invalid credentials
- 422: Missing required fields

### Task Endpoints

All task endpoints require `Authorization: Bearer <token>` header.

#### GET /api/{user_id}/tasks

List all tasks for authenticated user.

**Response** (200 OK):
```json
[
  {
    "id": "uuid-string",
    "title": "Complete project documentation",
    "description": "Write comprehensive docs",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z"
  }
]
```

**Errors**:
- 401: Invalid or missing token
- 403: user_id doesn't match authenticated user

#### POST /api/{user_id}/tasks

Create a new task.

**Request**:
```json
{
  "title": "New task",
  "description": "Optional description"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid-string",
  "title": "New task",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Errors**:
- 401: Unauthorized
- 403: Forbidden
- 422: Validation error (title too long, etc.)

#### GET /api/{user_id}/tasks/{task_id}

Get a specific task.

**Response** (200 OK):
```json
{
  "id": "task-uuid",
  "title": "Task title",
  "description": "Description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T11:00:00Z"
}
```

**Errors**:
- 404: Task not found
- 403: Task belongs to different user

#### PUT /api/{user_id}/tasks/{task_id}

Update a task.

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "id": "task-uuid",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:30:00Z"
}
```

#### PATCH /api/{user_id}/tasks/{task_id}/complete

Toggle task completion status.

**Response** (200 OK):
```json
{
  "id": "task-uuid",
  "title": "Task title",
  "description": "Description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:45:00Z"
}
```

#### DELETE /api/{user_id}/tasks/{task_id}

Delete a task permanently.

**Response** (204 No Content):
```
(empty response)
```

## Feature Specifications

### Implemented Features

1. **[001-project-setup](001-project-setup/spec.md)** - Project architecture and monorepo setup
2. **[002-database-schema](002-database-schema/spec.md)** - Database models and migrations
3. **[003-user-auth](003-user-auth/spec.md)** - User registration and JWT authentication
4. **[004-task-crud-api](004-task-crud-api/spec.md)** - Task CRUD API endpoints
5. **[005-task-ui](005-task-ui/spec.md)** - Task management user interface

### Feature Roadmap

#### Phase 1: Core Functionality (Complete)
- ✅ User registration and login
- ✅ JWT authentication
- ✅ Task CRUD operations
- ✅ User isolation
- ✅ Responsive mobile UI

#### Phase 2: Enhanced UX (Proposed)
- ⏳ Task categories/tags
- ⏳ Task search functionality
- ⏳ Sorting options (by date, title, priority)
- ⏳ Pagination for large task lists
- ⏳ Bulk operations (select multiple tasks)
- ⏳ Dark mode theme

#### Phase 3: Advanced Features (Proposed)
- ⏳ Task due dates and reminders
- ⏳ Priority levels
- ⏳ Subtasks/nested tasks
- ⏳ File attachments
- ⏳ Task sharing between users
- ⏳ Activity log/audit trail

#### Phase 4: Performance & Scale (Proposed)
- ⏳ Real-time updates (WebSockets)
- ⏳ Optimistic UI updates
- ⏳ Offline support (PWA)
- ⏳ Caching strategy
- ⏳ Rate limiting
- ⏳ Database connection pooling

## Development Standards

### Code Quality Requirements

1. **Type Safety**
   - TypeScript strict mode enabled
   - Zero `any` types allowed
   - Python type hints on all function signatures

2. **Function Size**
   - Maximum 30 lines per function
   - Extract complex logic into utilities

3. **DRY Principle**
   - No code duplication
   - Shared logic in lib/ directories

4. **Error Handling**
   - Try-catch blocks for all async operations
   - User-friendly error messages
   - Proper HTTP status codes

5. **Naming Conventions**
   - Descriptive variable and function names
   - PascalCase for components and classes
   - camelCase for functions and variables
   - SCREAMING_SNAKE_CASE for constants

6. **Styling**
   - Tailwind CSS exclusively
   - No inline styles
   - No CSS modules
   - Mobile-first responsive design

### Testing Requirements

1. **Backend**
   - Unit tests for all business logic
   - Integration tests for API endpoints
   - Database tests with in-memory SQLite
   - Target: >80% code coverage

2. **Frontend**
   - Component tests with React Testing Library
   - Integration tests for user flows
   - E2E tests with Playwright (future)

### Documentation Requirements

1. **Code Documentation**
   - JSDoc comments for all components
   - Docstrings for all Python functions
   - README in each major directory

2. **Specification Documentation**
   - Feature spec before implementation
   - Architecture decisions documented
   - API contracts specified

3. **User Documentation**
   - Setup instructions
   - Environment variable reference
   - Troubleshooting guide

## Deployment Strategy

### Development Environment

- Docker Compose with hot reload
- Local PostgreSQL instance
- Development secrets in .env files

### Staging Environment (Proposed)

- Neon Serverless PostgreSQL
- Vercel for frontend hosting
- Fly.io or Railway for backend
- Automated deployments on push to `develop` branch

### Production Environment (Proposed)

- Neon Serverless PostgreSQL (production tier)
- Vercel for frontend (CDN + edge functions)
- Fly.io or Railway for backend (auto-scaling)
- Automated deployments on push to `main` branch
- Health checks and monitoring
- Backup strategy for database

## Performance Targets

### Backend Performance

- List tasks: <200ms (currently ~50ms)
- Create task: <300ms (currently ~100ms)
- Update task: <300ms (currently ~100ms)
- Delete task: <200ms (currently ~75ms)
- Toggle completion: <200ms (currently ~75ms)

### Frontend Performance

- Initial page load: <2 seconds
- Time to interactive: <3 seconds
- Task list render: <500ms for 100 tasks
- Filter update: <1 second
- Form submission feedback: <100ms

### Database Performance

- Indexed queries: <50ms
- User isolation filter: <10ms overhead
- Connection pooling: 20 concurrent connections

## Monitoring & Observability (Proposed)

- Error tracking (Sentry)
- Performance monitoring (Vercel Analytics)
- Database monitoring (Neon metrics)
- Uptime monitoring (UptimeRobot)
- Log aggregation (Logtail or Papertrail)

## Constitution & Governance

All development must follow the project constitution at:
**`.specify/memory/constitution.md`**

Key principles:
- Spec-driven development (no manual coding)
- Type safety (TypeScript + Python type hints)
- Security first (JWT, password hashing, user isolation)
- Code quality gates (linting, testing, review)
- Documentation requirements (specs, README, inline docs)

## Links & Resources

- **Live API Docs**: http://localhost:8000/docs
- **Constitution**: `.specify/memory/constitution.md`
- **Development Guide**: `CLAUDE.md`
- **Frontend Docs**: `frontend/README.md`
- **Backend Docs**: `backend/README.md`
- **Code Review Report**: `CODE_REVIEW_REPORT.md`

## Version History

- **1.0.0** (2025-12-30) - Initial release with core functionality
  - User authentication
  - Task CRUD operations
  - Responsive UI
  - 62/62 backend tests passing
  - Production ready
