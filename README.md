# Todo Full-Stack Web Application

A modern, production-ready multi-user todo application built with spec-driven development using Claude Code and Spec-Kit Plus. Features a Next.js frontend, FastAPI backend, and PostgreSQL database with comprehensive JWT authentication and user isolation.

## Features

- **User Authentication**: Secure signup/login with JWT tokens and Better Auth
- **Task Management**: Full CRUD operations for tasks with completion tracking
- **User Isolation**: Each user can only access and manage their own tasks
- **Responsive Design**: Mobile-first UI that works on all screen sizes (320px+)
- **Real-time Validation**: Client and server-side validation with instant feedback
- **Type Safety**: End-to-end type safety with TypeScript and Python type hints
- **Auto-generated API Docs**: Interactive OpenAPI documentation at `/docs`

## Technology Stack

### Frontend
- **Next.js 15.1.0** - React framework with App Router for server-side rendering
- **React 19.0.0** - Modern UI library with Server Components
- **TypeScript 5.7.2** - Type-safe JavaScript with strict mode
- **Tailwind CSS 4.0.0** - Utility-first CSS framework
- **Better Auth 1.0.7** - Authentication library with JWT plugin
- **Axios 1.7.9** - HTTP client for API requests
- **Zod 3.24.1** - Schema validation for forms

### Backend
- **Python 3.11+** - Modern Python with type hints
- **FastAPI 0.115.6** - High-performance async web framework
- **SQLModel 0.0.22** - SQL ORM with Pydantic integration
- **PostgreSQL 16** - Robust relational database
- **Alembic 1.14.0** - Database migration management
- **python-jose 3.3.0** - JWT token handling
- **Passlib 1.7.4** - Secure password hashing with bcrypt
- **Uvicorn 0.34.0** - ASGI server for production

### Development Tools
- **Docker Compose** - Containerized development environment
- **Claude Code** - AI-powered development assistant
- **Spec-Kit Plus** - Specification-driven development workflow
- **Pytest** - Backend testing framework (62/62 tests passing)
- **ESLint** - Frontend code quality
- **Ruff** - Python linting and formatting

## Quick Start

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.11 or higher
- **Docker** and **Docker Compose** (for containerized setup)
- **Git** for version control

### Option 1: Docker Compose (Recommended)

The fastest way to get started with all services running:

```bash
# 1. Clone the repository
git clone <repository-url>
cd todo-fullstack-web

# 2. Create environment files
cp frontend/.env.example frontend/.env.local
cp backend/.env backend/.env

# 3. Update secrets in both .env files
# Set BETTER_AUTH_SECRET to the same value in both files (minimum 32 characters)
# Set JWT_SECRET_KEY in backend/.env (minimum 32 characters)

# 4. Start all services
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# PostgreSQL: localhost:5432
```

### Option 2: Manual Setup

For development with more control:

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update .env.local with your configuration
# NEXT_PUBLIC_API_URL=http://localhost:8000
# BETTER_AUTH_SECRET=<32+ character secret>
# BETTER_AUTH_URL=http://localhost:3000

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env .env  # Edit with your values

# Update .env with your configuration:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_db
# BETTER_AUTH_SECRET=<same as frontend>
# JWT_SECRET_KEY=<32+ character secret>
# CORS_ORIGINS=http://localhost:3000

# Create database
createdb todo_db

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## Project Structure

```
todo-fullstack-web/
├── .claude/                    # AI agent configurations
│   ├── agents/                # Development agents (frontend, backend, etc.)
│   ├── subagents/             # Sub-agents (reviewer, docs, integration)
│   ├── skills/                # Auto-invoke skills
│   └── commands/              # Custom workflow commands
├── .specify/                   # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md    # Project constitution and principles
│   └── templates/             # Spec, plan, tasks templates
├── specs/                      # Feature specifications
│   ├── 001-project-setup/     # Project setup spec
│   ├── 002-database-schema/   # Database schema spec
│   ├── 003-user-auth/         # Authentication spec
│   ├── 004-task-crud-api/     # Task API spec
│   └── 005-task-ui/           # Task UI spec
├── frontend/                   # Next.js application
│   ├── app/                   # App Router pages
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Landing page
│   │   ├── dashboard/         # Protected dashboard
│   │   └── auth/              # Login/register pages
│   ├── components/            # React components
│   │   ├── ui/                # Reusable UI components
│   │   └── features/          # Feature-specific components
│   ├── lib/                   # Utilities and API client
│   │   ├── api.ts             # Centralized API client
│   │   └── utils.ts           # Helper functions
│   ├── hooks/                 # Custom React hooks
│   │   ├── use-auth.ts        # Authentication hook
│   │   └── use-tasks.ts       # Task management hook
│   ├── types/                 # TypeScript type definitions
│   ├── validation/            # Zod validation schemas
│   ├── package.json           # Frontend dependencies
│   └── README.md              # Frontend documentation
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app initialization
│   │   ├── auth.py            # JWT utilities
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── models/            # SQLModel database models
│   │   │   ├── user.py        # User model
│   │   │   └── task.py        # Task model
│   │   ├── routes/            # API route handlers
│   │   │   ├── auth.py        # Auth endpoints
│   │   │   └── tasks.py       # Task endpoints
│   │   └── schemas/           # Pydantic request/response schemas
│   │       ├── user.py        # User schemas
│   │       └── task.py        # Task schemas
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Test files (62 tests)
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
├── docker-compose.yml          # Development environment
├── CLAUDE.md                   # Development workflow guide
└── README.md                   # This file
```

## Environment Variables

### Frontend (.env.local)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://hamzabhatti-todo-ai-chatbot.hf.space` | Yes |
| `BETTER_AUTH_SECRET` | Authentication secret (32+ chars) | `<random-32-char-string>` | Yes |
| `BETTER_AUTH_URL` | Frontend URL for auth callbacks | `http://localhost:3000` | Yes |

### Backend (.env)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/todo_db` | Yes |
| `BETTER_AUTH_SECRET` | Auth secret (must match frontend) | `<same-as-frontend>` | Yes |
| `JWT_SECRET_KEY` | JWT signing secret (32+ chars) | `<random-32-char-string>` | Yes |
| `JWT_ALGORITHM` | Algorithm for JWT encoding | `HS256` | No (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` | No (default: 30) |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` | Yes |
| `DEBUG` | Enable debug mode | `True` | No (default: False) |

**CRITICAL**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend for JWT token verification to work.

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT token

### Tasks (Protected)

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

- `GET /api/{user_id}/tasks` - Get all tasks for authenticated user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

### Documentation

- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - ReDoc API documentation
- `GET /openapi.json` - OpenAPI specification

## Development Workflow

This project uses spec-driven development with Claude Code and Spec-Kit Plus:

### 1. Specify Feature
```bash
/sp.specify [feature description]
```
Creates a detailed specification in `specs/features/`

### 2. Plan Implementation
```bash
/sp.plan
```
Generates architecture and implementation plan

### 3. Create Tasks
```bash
/sp.tasks
```
Breaks down feature into dependency-ordered tasks

### 4. Implement with Agents

Use specialized agents for implementation:

```bash
# Backend implementation
@fastapi-backend-dev implement [feature] backend

# Frontend implementation
@nextjs-frontend-dev implement [feature] frontend

# Database schema changes
@database-architect design [feature] schema

# Authentication changes
@auth-expert implement [feature] auth
```

### 5. Verify Integration
```bash
@api-integration-specialist test [feature] integration
```

### 6. Code Review
```bash
@code-reviewer review [feature]
```

### 7. Update Documentation
```bash
@documentation-writer update docs for [feature]
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_tasks.py

# Current status: 62/62 tests passing
```

### Frontend Tests

```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint

# Build validation
npm run build
```

## Available Scripts

### Frontend

- `npm run dev` - Start development server with hot reload
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

### Backend

- `uvicorn app.main:app --reload` - Start development server
- `pytest` - Run test suite
- `ruff check .` - Lint Python code
- `ruff format .` - Format Python code
- `mypy app/` - Type check Python code
- `alembic revision --autogenerate -m "message"` - Create migration
- `alembic upgrade head` - Apply migrations
- `alembic downgrade -1` - Rollback last migration

## Deployment

### Production Considerations

1. **Environment Variables**: Use secure, randomly generated secrets in production
2. **Database**: Configure Neon Serverless PostgreSQL connection string
3. **CORS**: Update `CORS_ORIGINS` to production frontend URL
4. **HTTPS**: Enforce HTTPS for all connections
5. **Token Storage**: Consider using httpOnly cookies instead of localStorage
6. **Database Migrations**: Always backup before running migrations
7. **Health Checks**: Backend provides `/health` endpoint for monitoring

### Docker Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Run production stack
docker-compose -f docker-compose.prod.yml up -d
```

## Security Features

- Password hashing with bcrypt (salted, constant-time comparison)
- JWT authentication with token expiration
- SQL injection prevention via SQLModel parameterized queries
- XSS prevention via React's automatic escaping
- CORS protection with whitelist-only origins
- Input validation with Pydantic and Zod
- User isolation enforced at database and API level
- No secrets in version control (.env files gitignored)

## Troubleshooting

### Frontend won't start
- Verify Node.js version: `node --version` (should be 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 3000 is available: `lsof -i :3000`

### Backend won't start
- Verify Python version: `python --version` (should be 3.11+)
- Activate virtual environment: `source venv/bin/activate`
- Check DATABASE_URL is correct
- Verify PostgreSQL is running: `pg_isready`

### Database connection fails
- Ensure PostgreSQL is running
- Verify credentials in DATABASE_URL
- Check database exists: `psql -l`
- Test connection: `psql $DATABASE_URL`

### CORS errors
- Verify `CORS_ORIGINS` includes frontend URL
- Check `NEXT_PUBLIC_API_URL` points to backend
- Ensure backend is running before frontend

### Authentication issues
- Verify `BETTER_AUTH_SECRET` matches in both .env files
- Check JWT token is included in request headers
- Ensure token hasn't expired (default 30 minutes)
- Clear localStorage and re-login

### Docker Compose issues
- Remove all containers: `docker-compose down -v`
- Rebuild images: `docker-compose build --no-cache`
- Check Docker daemon is running
- Verify port conflicts (3000, 8000, 5432)

## Code Standards

- **TypeScript**: Strict mode enabled, zero `any` types allowed
- **Python**: Type hints mandatory on all function signatures
- **Function Size**: Maximum 30 lines per function
- **DRY Principle**: No code duplication; extract reusable utilities
- **Error Handling**: Comprehensive try-catch with meaningful messages
- **Naming**: Clear, descriptive variable and function names
- **Styling**: Tailwind CSS exclusively (no inline styles, no CSS modules)

## Documentation

- **Root README.md** - This file (project overview and setup)
- **CLAUDE.md** - Development workflow with agents
- **frontend/README.md** - Frontend setup and architecture
- **frontend/CLAUDE.md** - Component patterns and best practices
- **backend/README.md** - Backend setup and API documentation
- **backend/CLAUDE.md** - Model design and endpoint patterns
- **specs/overview.md** - Architecture and feature roadmap
- **.specify/memory/constitution.md** - Project principles and governance

## Contributing

This project follows spec-driven development:

1. All features start with a specification in `specs/`
2. Specifications are reviewed before implementation
3. Implementation uses specialized agents
4. Code must pass @code-reviewer validation
5. All changes require documentation updates

See `CLAUDE.md` for detailed development workflow.

## License

[Your License Here]

## Support

- API Documentation: https://hamzabhatti-todo-ai-chatbot.hf.space/docs
- Project Constitution: `.specify/memory/constitution.md`
- Development Guide: `CLAUDE.md`

## Acknowledgments

Built with:
- Claude Code by Anthropic
- Spec-Kit Plus for specification-driven development
- Next.js, FastAPI, and PostgreSQL communities
