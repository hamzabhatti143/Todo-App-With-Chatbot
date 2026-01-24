# Quickstart Guide: Stateless Chat API Backend

**Feature**: 017-chat-api
**Date**: 2026-01-18
**Audience**: Developers integrating with the chat API

## Overview

This guide helps you quickly get started with the FastAPI chat backend. It covers setup, configuration, API usage, and common scenarios.

## Prerequisites

- Python 3.11+ installed
- PostgreSQL database (Neon Serverless PostgreSQL recommended)
- Google Gemini API key ([get one here](https://makersuite.google.com/app/apikey))
- Docker (optional, for containerized development)

---

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key Dependencies**:
- `fastapi==0.115.6` - Web framework
- `sqlmodel==0.0.22` - ORM
- `google-generativeai==0.8.3` - Gemini AI integration
- `uvicorn==0.34.0` - ASGI server
- `python-jose==3.3.0` - JWT tokens
- `slowapi` - Rate limiting

### 2. Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Database (required)
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Authentication (required)
JWT_SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini AI (required)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

# CORS (required)
CORS_ORIGINS=http://localhost:3000

# Rate Limiting (optional)
REDIS_URL=redis://localhost:6379  # For distributed rate limiting
```

**Important**: `JWT_SECRET_KEY` must be ≥32 characters and shared with frontend.

### 3. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Running upgrade -> xxx, add conversations table
INFO  [alembic.runtime.migration] Running upgrade xxx -> yyy, add messages table
```

### 4. Start the Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
TodoBot initialized: gemini-2.0-flash-exp
Registered 5 MCP tools: ['add_task', 'list_tasks', 'complete_task', 'update_task', 'delete_task']
```

### 5. Verify Installation

Open browser to http://localhost:8000/docs

You should see the FastAPI auto-generated documentation (Swagger UI).

**Test Health Endpoint**:
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status": "ok"}
```

---

## API Usage

### Authentication

All chat endpoints require JWT authentication.

#### 1. Register User (First Time)

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "email": "user@example.com",
  "created_at": "2026-01-16T10:00:00Z"
}
```

#### 2. Login and Get Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save the `access_token` for subsequent requests.**

### Chat Endpoint

#### Send First Message (Creates New Conversation)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Add buy groceries tomorrow",
    "conversation_id": null
  }'
```

**Response**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "880e8400-e29b-41d4-a716-446655440003",
  "role": "assistant",
  "content": "I've created a task titled 'Buy groceries' for tomorrow. Would you like me to add any specific items to the description?",
  "created_at": "2026-01-16T10:00:05Z",
  "task_data": {
    "tasks": [
      {
        "result": "Task created: Buy groceries (ID: aa0e8400-e29b-41d4-a716-446655440005)"
      }
    ]
  }
}
```

**Save the `conversation_id` to continue the conversation.**

#### Send Follow-Up Message (Continue Conversation)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Show me all my tasks",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Response**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "bb0e8400-e29b-41d4-a716-446655440006",
  "role": "assistant",
  "content": "Here are your tasks:\n◯ Buy groceries (pending)",
  "created_at": "2026-01-16T10:01:05Z",
  "task_data": null
}
```

---

## Common Scenarios

### Scenario 1: User Creates Multiple Tasks in One Message

**Request**:
```json
{
  "content": "Add three tasks: buy groceries, call mom, and finish report by Friday"
}
```

**What Happens**:
1. TodoBot agent parses the message
2. Calls `add_task()` three times
3. Returns conversational response with all task confirmations

**Response**:
```json
{
  "conversation_id": "...",
  "message_id": "...",
  "role": "assistant",
  "content": "I've created three tasks for you:\n✅ Buy groceries\n✅ Call mom\n✅ Finish report by Friday",
  "created_at": "...",
  "task_data": {
    "tasks": [
      {"result": "Task created: Buy groceries (ID: ...)"},
      {"result": "Task created: Call mom (ID: ...)"},
      {"result": "Task created: Finish report (ID: ...)"}
    ]
  }
}
```

### Scenario 2: User Asks to Complete a Task

**Request**:
```json
{
  "content": "Mark 'buy groceries' as complete",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**What Happens**:
1. Agent calls `list_tasks()` to find task ID
2. Matches "buy groceries" to task title
3. Calls `complete_task(task_id)`
4. Confirms completion

**Response**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "...",
  "role": "assistant",
  "content": "✓ Marked 'Buy groceries' as complete!",
  "created_at": "...",
  "task_data": null
}
```

### Scenario 3: Conversation Context Maintained

**Message 1**:
```json
{"content": "Add buy milk"}
```

**Response 1**:
```json
{
  "content": "I've added 'Buy milk' to your tasks.",
  ...
}
```

**Message 2** (references previous context):
```json
{
  "content": "Actually, make that 2 gallons",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 2** (understands "that" refers to milk task):
```json
{
  "content": "I've updated the task to '2 gallons of milk'.",
  ...
}
```

**How It Works**:
- Last 20 messages sent to Gemini as context
- Agent uses conversation history to resolve references
- Database stores full conversation history

---

## Error Handling

### Invalid Conversation ID

**Request**:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Hello",
    "conversation_id": "00000000-0000-0000-0000-000000000000"
  }'
```

**Response** (404 Not Found):
```json
{
  "detail": "Conversation 00000000-0000-0000-0000-000000000000 not found"
}
```

### Missing Authentication Token

**Request** (no Authorization header):
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello"}'
```

**Response** (401 Unauthorized):
```json
{
  "detail": "Not authenticated"
}
```

### Empty Message

**Request**:
```json
{
  "content": "",
  "conversation_id": null
}
```

**Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "content"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Rate Limit Exceeded

**Request** (11th request in same minute):
```bash
curl -X POST http://localhost:8000/api/chat ...
```

**Response** (429 Too Many Requests):
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

**Headers**:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642348800
Retry-After: 45
```

---

## Development Tips

### 1. Use Interactive API Docs

Open http://localhost:8000/docs in browser for interactive testing.

**Benefits**:
- Try endpoints without curl/Postman
- See request/response schemas
- Automatic JWT token management

### 2. Enable Debug Logging

Set environment variable:
```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

**Output**:
```
DEBUG:     GET /api/chat HTTP/1.1
DEBUG:     Request: {"content": "Hello", "conversation_id": null}
INFO:      Saved user message 880e8400-... in conversation 550e8400-...
DEBUG:     Agent response: AgentResponse(message='Hi! How can I help?', tool_calls=[])
INFO:      Saved assistant message bb0e8400-...
```

### 3. Test with Different Users

Each JWT token represents a different user. Create multiple users to test user isolation:

```bash
# User 1
curl -X POST .../auth/register -d '{"email": "user1@test.com", "password": "pass123"}'
USER1_TOKEN=$(curl -X POST .../auth/login -d '...' | jq -r .access_token)

# User 2
curl -X POST .../auth/register -d '{"email": "user2@test.com", "password": "pass123"}'
USER2_TOKEN=$(curl -X POST .../auth/login -d '...' | jq -r .access_token)

# User 1 creates conversation
CONV_ID=$(curl -X POST .../chat -H "Authorization: Bearer $USER1_TOKEN" -d '...' | jq -r .conversation_id)

# User 2 tries to access User 1's conversation (should fail with 404)
curl -X POST .../chat -H "Authorization: Bearer $USER2_TOKEN" -d "{\"content\":\"Hello\",\"conversation_id\":\"$CONV_ID\"}"
```

**Expected**: User 2 receives 404 Not Found (conversation doesn't exist for User 2).

### 4. Monitor Database State

```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# Check conversations
SELECT id, user_id, created_at FROM conversations ORDER BY created_at DESC LIMIT 5;

# Check messages in a conversation
SELECT role, content, created_at FROM messages
WHERE conversation_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY created_at ASC;
```

---

## Testing

### Unit Tests

```bash
cd backend
pytest tests/test_chat_endpoints.py -v
```

**Example Test Output**:
```
tests/test_chat_endpoints.py::test_create_first_message PASSED
tests/test_chat_endpoints.py::test_continue_conversation PASSED
tests/test_chat_endpoints.py::test_unauthorized_access PASSED
tests/test_chat_endpoints.py::test_empty_message_rejected PASSED
```

### Integration Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app --cov-report=html tests/
```

---

## Deployment

### Docker Compose (Development)

```bash
# Start all services
docker-compose up

# Services started:
# - Backend (port 8000)
# - Frontend (port 3000)
# - PostgreSQL (port 5432)
# - Redis (port 6379) [optional]
```

### Production (Cloud)

**Backend** (Railway, Fly.io, or Render):
1. Set environment variables in platform dashboard
2. Deploy from git repository
3. Run migrations: `alembic upgrade head`
4. Start server: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Database** (Neon Serverless PostgreSQL):
1. Create database at https://neon.tech
2. Copy connection string to `DATABASE_URL`
3. Enable SSL mode: `?sslmode=require`

**Scaling**:
- Horizontal: Add more server instances (stateless architecture)
- Vertical: Increase CPU/memory per instance
- Rate limiting: Use Redis for distributed rate limiting

---

## Troubleshooting

### Problem: "Connection refused" to database

**Solution**:
1. Check PostgreSQL is running: `pg_isready -h localhost`
2. Verify `DATABASE_URL` in `.env`
3. Check firewall allows port 5432

### Problem: "Gemini API key invalid"

**Solution**:
1. Verify `GEMINI_API_KEY` in `.env`
2. Check API key at https://makersuite.google.com/app/apikey
3. Ensure no leading/trailing spaces in .env file

### Problem: "TodoBot agent unavailable"

**Solution**:
1. Check Gemini API status: https://status.cloud.google.com
2. Verify internet connectivity
3. Check logs for rate limiting errors
4. Try different model: `GEMINI_MODEL=gemini-1.5-pro`

### Problem: "Rate limit exceeded" too quickly

**Solution**:
1. Increase limit: `rate_limit_chat: "20/minute"` in config.py
2. Use Redis for user-based rate limiting (not IP-based)
3. Check if multiple users sharing same IP (NAT/proxy)

### Problem: Conversation history not maintained

**Solution**:
1. Verify `conversation_id` included in request
2. Check database has messages: `SELECT COUNT(*) FROM messages WHERE conversation_id = '...'`
3. Verify 20-message limit not exceeded (older messages still in DB, but not sent to agent)

---

## API Reference

### Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API information | No |
| GET | `/health` | Health check | No |
| GET | `/docs` | Interactive API docs (Swagger) | No |
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login and get JWT token | No |
| POST | `/api/chat` | Send chat message | Yes (JWT) |
| GET | `/api/conversations` | List user's conversations | Yes (JWT) |
| GET | `/api/conversations/{id}` | Get conversation with messages | Yes (JWT) |

### Request Schemas

#### ChatMessageRequest

```typescript
{
  content: string;        // 1-5000 characters
  conversation_id?: UUID; // Optional; null creates new conversation
}
```

#### ChatMessageResponse

```typescript
{
  conversation_id: UUID;
  message_id: UUID;
  role: "assistant";
  content: string;
  created_at: DateTime;
  task_data?: {          // Optional; present if tasks created/modified
    tasks: Array<{
      result: string;
    }>;
  };
}
```

---

## Next Steps

1. **Explore Agent Capabilities**: Try different task management commands
2. **Integrate Frontend**: Use Next.js frontend from Feature 013
3. **Customize Agent**: Modify system instructions in `app/agent.py`
4. **Add More Tools**: Extend MCP tool registry with custom tools
5. **Monitor Performance**: Add logging and metrics for production

---

**Need Help?**

- API Documentation: http://localhost:8000/docs
- Feature Spec: `/specs/017-chat-api/spec.md`
- Implementation Plan: `/specs/017-chat-api/plan.md`
- Research: `/specs/017-chat-api/research.md`

---

**Last Updated**: 2026-01-18
