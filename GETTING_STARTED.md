# Getting Started - Todo Full-Stack Web Application

**Status**: ✅ Ready to Use
**Date**: 2026-01-25

---

## Quick Start (5 Minutes)

### Prerequisites

✅ Backend server running on port 8002
✅ Frontend server running on port 3000
✅ Test user created in database

### Step 1: Verify Backend is Running

Open your browser and visit: http://localhost:8002/health

**Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

If you see this, your backend is ready! ✅

### Step 2: Verify Frontend is Running

Open your browser and visit: http://localhost:3000

You should see the Todo application homepage.

### Step 3: Login to the Application

1. Navigate to http://localhost:3000/chat (or click "Chat" in the navigation)
2. If not logged in, you'll be redirected to the login page
3. Use the test credentials:
   - **Email**: `test_chat_user@example.com`
   - **Password**: `SecurePassword123!`
4. Click "Login"

### Step 4: Test the Chat Feature

Once logged in, you'll see the chat interface.

**Try these commands**:

1. **Create a task**:
   - Type: "Add a task to buy groceries tomorrow"
   - Press Enter
   - Wait for AI response (takes 2-5 seconds)
   - Check that the task was created

2. **List tasks**:
   - Type: "Show me all my tasks"
   - Press Enter
   - AI will display your task list

3. **Create multiple tasks**:
   - Type: "I need to finish the report by Friday, call the client on Monday, and schedule a meeting next week"
   - Press Enter
   - AI should create 3 separate tasks

---

## Service URLs

### Backend API
- **Base URL**: http://localhost:8002
- **API Docs (Swagger)**: http://localhost:8002/docs
- **Alternative Docs (ReDoc)**: http://localhost:8002/redoc
- **Health Check**: http://localhost:8002/health

### Frontend Application
- **Home Page**: http://localhost:3000
- **Chat Interface**: http://localhost:3000/chat
- **Dashboard**: http://localhost:3000/dashboard

---

## Test Credentials

### Test User
- **Email**: `test_chat_user@example.com`
- **Password**: `SecurePassword123!`

To create additional users:
1. Visit: http://localhost:3000/auth/signup
2. Fill in the registration form
3. OR use the backend API:
   ```bash
   curl -X POST http://localhost:8002/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "newuser@example.com",
       "password": "SecurePassword123!"
     }'
   ```

---

## Common Tasks

### Restart Backend Server

```bash
cd /mnt/d/todo-fullstack-web/backend

# Stop existing server
pkill -f "uvicorn.*8002"

# Start server
./venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8002
```

### Restart Frontend Server

```bash
cd /mnt/d/todo-fullstack-web/frontend

# Stop existing server (Ctrl+C if running in terminal)
# OR
pkill -f "next dev"

# Start server
npm run dev
```

### Run Database Migrations

```bash
cd /mnt/d/todo-fullstack-web/backend

# Check current migration status
alembic current

# Apply all pending migrations
alembic upgrade head
```

### View Backend Logs

The backend outputs logs to the terminal where it's running. Look for:
- `INFO: Application startup complete` - Server started successfully
- `Authentication: Successfully authenticated user` - User logged in
- `Chat endpoint called by user` - Chat message received
- `Saved assistant message` - AI response sent

### Test API Endpoints

```bash
cd /mnt/d/todo-fullstack-web/backend

# Test health endpoint
./venv/Scripts/python.exe test_connection.py

# Test end-to-end flow
./venv/Scripts/python.exe test_end_to_end.py
```

---

## Troubleshooting

### Issue: Backend not responding

**Symptoms**: Frontend shows "Network error" or cannot connect

**Solution**:
1. Check if backend is running: http://localhost:8002/health
2. Check backend logs for errors
3. Restart backend server
4. Verify `.env` file has correct `DATABASE_URL`

### Issue: 401 Unauthorized

**Symptoms**: API returns "Could not validate credentials"

**Solution**:
1. Check if JWT token is stored in localStorage
2. Try logging out and logging in again
3. Check browser console for errors
4. Verify `JWT_SECRET_KEY` matches in frontend and backend

### Issue: 403 Forbidden

**Symptoms**: API returns "Not authorized to access this resource"

**Solution**:
1. Verify you're logged in
2. Check that the user_id in the URL matches your user
3. Check backend logs for authentication details
4. Ensure JWT token hasn't expired (30-minute lifetime)

### Issue: Frontend not loading

**Symptoms**: Browser shows "Cannot connect" or blank page

**Solution**:
1. Check if frontend is running: `lsof -i :3000` or `netstat -ano | findstr :3000`
2. Check for errors in frontend terminal
3. Restart frontend server
4. Clear browser cache and reload
5. Check `.env.local` has correct `NEXT_PUBLIC_BACKEND_URL`

### Issue: AI agent not creating tasks

**Symptoms**: Chat works but tasks aren't created

**Solution**:
1. Check backend logs for agent errors
2. Verify `OPENAI_API_KEY` in `.env` is valid
3. Check if database migration for tasks table is applied
4. Try a simpler command: "Add a task to test"

---

## API Testing with Swagger

1. Open: http://localhost:8002/docs
2. Click "Authorize" button (top right)
3. Login to get a JWT token:
   - Use POST /api/auth/login
   - Enter email and password
   - Copy the `access_token` from response
4. Click "Authorize" again and paste token
5. Now you can test all endpoints interactively

**Popular Endpoints to Test**:
- `POST /api/chat` - Send a chat message
- `GET /api/conversations` - List your conversations
- `GET /api/{user_id}/tasks` - List your tasks

---

## Environment Variables Reference

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://neondb_owner:password@host/neondb?sslmode=require

# Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OpenAI API (for AI agent)
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1024
OPENAI_TIMEOUT=30

# Rate Limiting
RATE_LIMIT_CHAT=10/minute
RATE_LIMIT_AGENT=5/minute
```

### Frontend (.env.local)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_BACKEND_URL=http://localhost:8002

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

---

## Next Steps

1. ✅ **Explore the Chat Interface**
   - Create tasks via natural language
   - List, complete, and manage tasks
   - View conversation history

2. ✅ **Test Multi-User Isolation**
   - Create a second user account
   - Verify each user sees only their own data

3. ✅ **Customize the AI Agent**
   - Modify prompts in `backend/app/agent.py`
   - Adjust AI temperature and max tokens
   - Add custom MCP tools

4. ✅ **Deploy to Production**
   - Use Neon PostgreSQL for database (already configured)
   - Deploy frontend to Vercel
   - Deploy backend to Railway or Fly.io
   - Update CORS_ORIGINS and API URLs

---

## Support Files

- **Implementation Summary**: `backend/IMPLEMENTATION_COMPLETE.md`
- **Test Scripts**: `backend/test_connection.py`, `backend/test_end_to_end.py`
- **User Creation**: `backend/create_test_user.py`
- **Status Report**: `CURRENT_STATUS.md`

---

## Success Indicators

You'll know everything is working when:

✅ Health endpoint returns `{"status": "healthy", "database": "connected"}`
✅ You can login at http://localhost:3000
✅ Chat interface loads without errors
✅ Sending a message gets an AI response
✅ Created tasks appear in the task list
✅ Conversation history is saved and retrievable

**Enjoy your fully functional Todo application with AI-powered task management!** 🎉

---

**Last Updated**: 2026-01-25
**Version**: 1.0.0
**Status**: Production Ready
