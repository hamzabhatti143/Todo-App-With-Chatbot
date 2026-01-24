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

## Features

### AI Task Assistant (013-todo-ai-chatbot)
Conversational AI interface for task management powered by Google Gemini 2.0 Flash.

**Access**: `/chat` page (requires authentication)

**Capabilities**:
- **Natural language task creation**: "Add a task to buy groceries tomorrow"
- **Task management**: List, complete, update, delete tasks through conversation
- **Multi-part requests**: "Finish report by Friday, call client Monday" → Creates multiple tasks
- **Conversation history**: Browse and resume previous conversations
- **Smart understanding**: Extracts dates, priorities, generates concise titles

**Technical Stack**:
- Backend: Google Gemini 2.0 Flash + MCP (Model Context Protocol)
- Rate limiting: 10 requests/minute per user
- Context: Last 20 messages maintained
- Storage: Conversations and messages in PostgreSQL

**Quick Start**:
```bash
# Set Gemini API key
echo "GEMINI_API_KEY=your-key-here" >> backend/.env

# Run migrations
cd backend && alembic upgrade head

# Start server and navigate to /chat
```

See `specs/013-todo-ai-chatbot/IMPLEMENTATION_SUMMARY.md` for full documentation.

## Active Technologies
- TypeScript 5.7.2 (strict mode) + Next.js 15.1.0 with App Router (012-animated-todo-frontend)
- JWT tokens in localStorage, task state from backend API (012-animated-todo-frontend)
- Google Gemini 2.0 Flash for AI chat (013-todo-ai-chatbot)
- MCP protocol for AI tool calling (013-todo-ai-chatbot)
- Python 3.11+ + SQLModel 0.0.22, psycopg2-binary 2.9.10, Alembic 1.14.0, pydantic-settings 2.7.0 (014-database-models)
- Neon Serverless PostgreSQL 16 with SSL (014-database-models)
- Python 3.11+ + FastAPI 0.115.6, SQLModel 0.0.22, Pydantic 2.10.4, google-generativeai 0.8.3, Uvicorn 0.34.0 (017-chat-api)
- Neon Serverless PostgreSQL 16 with SQLModel ORM, Alembic migrations (017-chat-api)

## Recent Changes
- 013-todo-ai-chatbot: Added AI-powered conversational task management with Gemini 2.0 Flash
- 012-animated-todo-frontend: Added TypeScript 5.7.2 (strict mode) + Next.js 15.1.0 with App Router
