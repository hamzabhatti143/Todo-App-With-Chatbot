# Todo Full-Stack Web Application

## Project Overview
Modern multi-user todo web application with persistent storage.
Built using spec-driven development with Claude Code and Spec-Kit Plus.

## Monorepo Structure
```
todo-fullstack-web/
├── .claude/           # Agent configurations
├── .spec-kit/         # Spec-Kit config
├── specs/             # Feature specifications
├── frontend/          # Next.js 16+ application
├── backend/           # FastAPI application
└── docker-compose.yml # Development environment
```

## Technology Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth with JWT tokens
- **Spec-Driven**: Claude Code + Spec-Kit Plus

## Agents Available

### Development Agents
- **@nextjs-frontend-dev** - Frontend implementation
- **@fastapi-backend-dev** - Backend implementation
- **@database-architect** - Schema design
- **@auth-expert** - Authentication integration

### Sub-Agents
- **@code-reviewer** - Full-stack code review
- **@documentation-writer** - Documentation maintenance
- **@api-integration-specialist** - API integration testing
- **@deployment-specialist** - Deployment configuration

### Skills (Auto-Invoke)
- **monorepo-navigation** - Navigate frontend/backend
- **spec-kit-integration** - Manage specifications
- **jwt-auth-workflow** - Handle authentication

## Development Workflow

### 1. Specify Feature
```
/specify Feature description in specs/features/
```

### 2. Plan Implementation
```
/plan
```

### 3. Create Tasks
```
/tasks
```

### 4. Implement Backend
```
@fastapi-backend-dev implement [feature] backend
```

### 5. Implement Frontend
```
@nextjs-frontend-dev implement [feature] frontend
```

### 6. Verify Integration
```
@api-integration-specialist test [feature] integration
```

### 7. Review Code
```
@code-reviewer review [feature]
```

### 8. Update Documentation
```
@documentation-writer update docs for [feature]
```

## Running the Application

### Development Mode
```bash
# Both services
docker-compose up

# Frontend only
cd frontend && npm run dev

# Backend only
cd backend && uvicorn app.main:app --reload
```

### Environment Variables
See `.env.example` in frontend/ and backend/ folders.

## Code Standards
- TypeScript strict mode enabled
- Python type hints mandatory
- Tailwind CSS for all styling
- SQLModel for database operations
- JWT for authentication
- RESTful API design

## Reference Specifications
All specs in /specs folder:
- @specs/overview.md - Project summary
- @specs/features/*.md - Feature specs
- @specs/api/*.md - API endpoint specs
- @specs/database/*.md - Database schema specs
- @specs/ui/*.md - UI component specs

Always read relevant spec before implementing.

## Active Technologies
- TypeScript 5.7.2 (strict mode) + Next.js 15.1.0 with App Router (012-animated-todo-frontend)
- JWT tokens in localStorage, task state from backend API (012-animated-todo-frontend)

## Recent Changes
- 012-animated-todo-frontend: Added TypeScript 5.7.2 (strict mode) + Next.js 15.1.0 with App Router
