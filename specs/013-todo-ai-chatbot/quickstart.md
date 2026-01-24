# Quickstart Guide: Todo AI Chatbot

**Feature**: 013-todo-ai-chatbot
**Date**: 2026-01-16
**Prerequisites**: Node.js 18+, Python 3.10+, Neon PostgreSQL account

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [API Keys](#api-keys)
4. [Database Setup](#database-setup)
5. [Installation](#installation)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Node.js**: Version 18+ (for frontend)
  ```bash
  node --version  # Should be >= 18.0.0
  ```

- **Python**: Version 3.10+ (for backend)
  ```bash
  python --version  # Should be >= 3.10.0
  ```

- **PostgreSQL**: Neon Serverless PostgreSQL account
  - Sign up at https://neon.tech

### Required Accounts

- **Google AI Studio**: For Gemini API key
  - Sign up at https://makersuite.google.com/app/apikey

- **OpenAI**: For ChatKit domain key (if required)
  - Sign up at https://platform.openai.com/

## Environment Setup

### 1. Clone and Navigate to Project

```bash
cd /path/to/todo-fullstack-web
git checkout 013-todo-ai-chatbot
```

### 2. Frontend Environment Variables

Create `frontend/.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-32-character-secret-key-here
BETTER_AUTH_URL=http://localhost:3000

# ChatKit Configuration (if required)
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=your-chatkit-domain-key

# Allowed Domains
NEXT_PUBLIC_ALLOWED_DOMAINS=localhost:3000,localhost:8000
```

### 3. Backend Environment Variables

Create `backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1024
GEMINI_RATE_LIMIT=100
GEMINI_TIMEOUT=30

# Better Auth Configuration (must match frontend)
BETTER_AUTH_SECRET=your-32-character-secret-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Rate Limiting
RATE_LIMIT_CHAT=10/minute
RATE_LIMIT_AGENT=5/minute

# Optional: Redis for rate limiting
# REDIS_URL=redis://localhost:6379
```

## API Keys

### 1. Obtain Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **Get API Key**
3. Create a new API key or use existing one
4. Copy the API key
5. Add to `backend/.env`:
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

### 2. Obtain Neon PostgreSQL Connection String

1. Go to [Neon Dashboard](https://console.neon.tech/)
2. Create a new project or select existing
3. Navigate to **Connection Details**
4. Copy the connection string
5. Add to `backend/.env`:
   ```env
   DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require
   ```

### 3. Generate Better Auth Secret

Generate a secure 32-character secret:

```bash
# On Linux/Mac:
openssl rand -base64 32

# On Windows (PowerShell):
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

Add the same secret to both `frontend/.env.local` and `backend/.env`:

```env
BETTER_AUTH_SECRET=your-generated-secret-here
```

### 4. Obtain ChatKit Domain Key (Optional)

If using OpenAI ChatKit's domain-restricted features:

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to **API Keys**
3. Create a new restricted API key for your domain
4. Add to `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=your-chatkit-key
   ```

## Database Setup

### 1. Run Alembic Migrations

Navigate to backend and run migrations:

```bash
cd backend

# Verify Alembic is installed
pip show alembic

# Run migrations to create conversations and messages tables
alembic upgrade head

# Verify tables were created
# (Connect to your Neon database and run)
# SELECT tablename FROM pg_tables WHERE schemaname='public';
# Should show: users, tasks, conversations, messages
```

### 2. Verify Database Connection

Test the database connection:

```bash
cd backend
python -c "from app.core.database import engine; from sqlmodel import Session; Session(engine).close(); print('Database connection successful')"
```

## Installation

### 1. Install Frontend Dependencies

```bash
cd frontend

# Install npm packages
npm install

# Verify ChatKit installation
npm list @openai/chatkit

# Expected output: @openai/chatkit@latest (or specific version)
```

### 2. Install Backend Dependencies

```bash
cd backend

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Verify key packages
pip show google-generativeai mcp slowapi sqlmodel

# Expected: All packages should be installed with correct versions
```

### 3. Verify Installation

Run verification scripts:

```bash
# Backend verification
cd backend
python -c "import google.generativeai as genai; print(f'Gemini SDK version: {genai.__version__}')"
python -c "from app.config import get_settings; s = get_settings(); print('Config loaded successfully')"

# Frontend verification
cd frontend
npm list --depth=0 | grep -E '(next|react|@openai/chatkit)'
```

## Running the Application

### 1. Start Backend Server

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

### 2. Start Frontend Server

Open a new terminal:

```bash
cd frontend

# Start Next.js development server
npm run dev

# Expected output:
# ▲ Next.js 15.1.0
# - Local:        http://localhost:3000
# - Environments: .env.local
```

### 3. Verify Services Are Running

**Backend Health Check**:
```bash
curl http://localhost:8000/docs
# Should open FastAPI Swagger UI in browser
```

**Frontend Health Check**:
```bash
curl http://localhost:3000
# Should return HTML of Next.js homepage
```

### 4. Test Authentication

1. Open browser to http://localhost:3000/signup
2. Register a new user account:
   - Email: test@example.com
   - Password: TestPassword123!
3. You should be redirected to the dashboard
4. Verify JWT token is stored (check browser localStorage)

### 5. Test Chat Interface

1. Navigate to http://localhost:3000/chat (once implemented)
2. Send a test message: "Add a task to buy groceries"
3. Verify:
   - Message appears in chat UI
   - AI responds with confirmation
   - Task is created in database
   - Conversation is persisted

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_chat.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run MCP tools tests
pytest tests/test_mcp_tools.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests (once test framework is set up)
npm test

# Run specific test
npm test -- ChatInterface.test.tsx

# Run with coverage
npm test -- --coverage
```

### Integration Tests

Test the full chat flow manually:

1. **User Registration**:
   - Navigate to `/signup`
   - Create account
   - Verify JWT token received

2. **Task Creation via Chat**:
   - Navigate to `/chat`
   - Send: "Create a task to finish project report"
   - Verify task appears in dashboard

3. **Task Listing via Chat**:
   - Send: "Show me all my tasks"
   - Verify all tasks are listed

4. **Task Completion via Chat**:
   - Send: "Mark 'finish project report' as complete"
   - Verify task status updates

5. **Task Deletion via Chat**:
   - Send: "Delete the grocery task"
   - Verify task is removed

6. **Conversation History**:
   - Refresh page
   - Verify previous messages are loaded

7. **User Isolation**:
   - Create second user account
   - Verify User A cannot see User B's tasks or conversations

## Troubleshooting

### Common Issues

#### 1. Database Connection Fails

**Error**: `FATAL: password authentication failed for user`

**Solution**:
- Verify DATABASE_URL is correct in `backend/.env`
- Check Neon dashboard for correct credentials
- Ensure `sslmode=require` is in connection string
- Test connection: `psql <DATABASE_URL>`

#### 2. Gemini API Key Invalid

**Error**: `google.api_core.exceptions.PermissionDenied: API key not valid`

**Solution**:
- Verify GEMINI_API_KEY in `backend/.env`
- Check API key is active in Google AI Studio
- Ensure no extra whitespace in .env file
- Test: `python -c "from app.services.gemini_service import GeminiService; s = GeminiService(); print('API key valid')"`

#### 3. CORS Error on Frontend

**Error**: `Access to fetch at 'http://localhost:8000/api/chat' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
- Verify CORS_ORIGINS includes `http://localhost:3000` in `backend/.env`
- Restart backend server after updating .env
- Check FastAPI CORS middleware configuration in `app/main.py`

#### 4. Rate Limit Exceeded

**Error**: `429 Rate Limit Exceeded`

**Solution**:
- Wait for rate limit window to reset (shown in Retry-After header)
- Adjust rate limits in `backend/.env`:
  ```env
  RATE_LIMIT_CHAT=20/minute  # Increase from 10
  ```
- Restart backend server

#### 5. ChatKit Components Not Rendering

**Error**: `Module not found: Can't resolve '@openai/chatkit'`

**Solution**:
- Verify installation: `npm list @openai/chatkit`
- Reinstall if missing: `npm install @openai/chatkit --save`
- Clear Next.js cache: `rm -rf .next && npm run dev`
- Check TypeScript configuration allows the import

#### 6. Alembic Migration Fails

**Error**: `sqlalchemy.exc.ProgrammingError: (psycopg.errors.DuplicateTable) relation "conversations" already exists`

**Solution**:
- Check current migration: `alembic current`
- Downgrade if needed: `alembic downgrade -1`
- Re-run migration: `alembic upgrade head`
- Verify in database: `SELECT tablename FROM pg_tables WHERE tablename='conversations';`

#### 7. JWT Token Expired During Chat

**Error**: `401 Unauthorized: Token expired`

**Solution**:
- Frontend should detect expired token and redirect to login
- Implement token refresh in Better Auth configuration
- Increase token expiration in `backend/.env`:
  ```env
  JWT_EXPIRATION_MINUTES=60  # Increase from 30
  ```

#### 8. MCP Tools Not Executing

**Error**: `Tool 'create_task' not found in registry`

**Solution**:
- Verify MCP tool registration in `app/main.py` startup event
- Check tool names match between Gemini agent and MCP registry
- Restart backend server
- Test tool execution: `pytest tests/test_mcp_tools.py::test_create_task`

### Debug Mode

Enable debug logging for troubleshooting:

**Backend**:
```python
# backend/app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend**:
```typescript
// frontend/next.config.js
module.exports = {
  reactStrictMode: true,
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
}
```

### Health Checks

Run system health checks:

```bash
# Backend health check
curl http://localhost:8000/health

# Database connection check
cd backend && python -c "from app.core.database import engine; from sqlmodel import Session; Session(engine).close(); print('✓ Database OK')"

# Gemini API check
cd backend && python -c "from app.services.gemini_service import GeminiService; s = GeminiService(); s.generate_text('Hello'); print('✓ Gemini API OK')"

# Frontend build check
cd frontend && npm run build
```

## Next Steps

After successful setup:

1. **Read the Feature Specification**: See `specs/013-todo-ai-chatbot/spec.md` for detailed requirements
2. **Review Implementation Plan**: See `specs/013-todo-ai-chatbot/plan.md` for architecture decisions
3. **Explore API Contracts**: See `specs/013-todo-ai-chatbot/contracts/` for endpoint definitions
4. **Check Data Model**: See `specs/013-todo-ai-chatbot/data-model.md` for database schema
5. **Run `/sp.tasks`**: Generate implementation tasks from the plan

## Support

For issues or questions:

- Check existing GitHub issues
- Review the project README
- Consult the constitution at `.specify/memory/constitution.md`
- See technology research at root `AI_CHATBOT_TECH_RESEARCH.md`

## Summary

You should now have:
- ✅ All environment variables configured
- ✅ API keys obtained and added
- ✅ Database migrations applied
- ✅ Frontend and backend dependencies installed
- ✅ Both servers running successfully
- ✅ Authentication tested
- ✅ Ready to implement chat features

The system is ready for implementation. Proceed to `/sp.tasks` to generate the task breakdown.
