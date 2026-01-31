# Chat Errors Fix: Backend Not Running

**Date**: 2026-01-24
**Status**: ✅ ROOT CAUSE DIAGNOSED
**Issue**: "Failed to load conversation" and chat message sending errors

---

## 🔍 Root Cause

**The backend server is NOT running!**

Both errors are caused by the same issue: the FastAPI backend is not running on `localhost:8000`, so all API requests to `/api/conversations` and `/api/chat` fail with network errors.

---

## 📊 Diagnosis Summary

### Error 1: "Failed to load conversation"
**What happens**: When the chat page loads, `ConversationSidebar` tries to fetch conversations from `/api/conversations`

**Code location**: `frontend/components/chat/ConversationSidebar.tsx:35`

**API call**:
```typescript
const conversations = await conversationsApi.list()
// Calls: GET http://localhost:8000/api/conversations
```

**Error**: Network error (ECONNREFUSED) because backend is not running

---

### Error 2: "Chat message sending fails"
**What happens**: When user types a message and presses Enter, the app tries to send it to `/api/chat`

**Code location**: `frontend/hooks/use-chat.ts:74`

**API call**:
```typescript
const response = await chatApi.sendMessage(requestData)
// Calls: POST http://localhost:8000/api/chat
```

**Error**: Network error (ECONNREFUSED) because backend is not running

---

## ✅ Solution

### Start the Backend Server

You need to run the FastAPI backend on `localhost:8000`.

#### Option 1: Run with Uvicorn (Recommended)

```bash
cd /mnt/d/todo-fullstack-web/backend

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
./venv/Scripts/activate  # On Windows

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Option 2: Run with Docker Compose

```bash
cd /mnt/d/todo-fullstack-web

# Start both frontend and backend
docker-compose up
```

---

## 🧪 Verify Backend is Running

### 1. Check Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{"status":"healthy"}
```

### 2. Check API Documentation

Open in browser: http://localhost:8000/docs

You should see the FastAPI Swagger UI with all API endpoints.

### 3. Check Conversations Endpoint (Requires Auth)

```bash
# Get your auth token from browser localStorage
curl -X GET http://localhost:8000/api/conversations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected**: Returns `[]` or list of conversations

---

## 🔄 Complete Startup Workflow

### Step 1: Start Backend

```bash
cd /mnt/d/todo-fullstack-web/backend

# On Windows (WSL)
./venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# On Linux/Mac
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for**: `Application startup complete.`

### Step 2: Start Frontend

```bash
cd /mnt/d/todo-fullstack-web/frontend

npm run dev
```

**Wait for**: `Ready on http://localhost:3000`

### Step 3: Test Chat

1. Open http://localhost:3000
2. Sign in with your account
3. Click "Perform Tasks With AI" button
4. You should see the chat interface
5. Conversation history should load (or show "No conversations yet")
6. Type a message and press Enter
7. You should receive a response

---

## 📁 Configuration Check

### Frontend Configuration

**File**: `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=https://hamzabhatti-todo-ai-chatbot.hf.space
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000  # ✅ Correct for local dev
```

**Note**:
- `NEXT_PUBLIC_API_URL` is for task API (points to HuggingFace Space)
- `NEXT_PUBLIC_BACKEND_URL` is for chat API (should point to localhost for local dev)

### Backend Configuration

**File**: `backend/.env`

```env
DATABASE_URL=postgresql://...
GEMINI_API_KEY=AIzaSyAMPjMQNu-vdA9GnaSNdcIA_KWAegofbkE
GEMINI_MODEL=gemini-2.0-flash
JWT_SECRET_KEY=...
```

All configured correctly.

---

## 🚨 Common Issues

### Issue 1: Port 8000 Already in Use

**Error**:
```
ERROR:    [Errno 98] Address already in use
```

**Solution**:
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)

# Or use a different port
uvicorn app.main:app --reload --port 8001
# Then update NEXT_PUBLIC_BACKEND_URL to http://localhost:8001
```

### Issue 2: Virtual Environment Not Found

**Error**:
```
bash: venv/Scripts/python.exe: No such file or directory
```

**Solution**:
```bash
cd /mnt/d/todo-fullstack-web/backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
./venv/Scripts/activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Issue 3: Database Connection Error

**Error**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**:
- Check `DATABASE_URL` in `backend/.env`
- Ensure PostgreSQL is running
- Verify database credentials
- Run migrations: `alembic upgrade head`

### Issue 4: Gemini API Quota Still Exhausted

**Error**:
```
429 You exceeded your current quota
```

**Solution**:
- Wait 24 hours for quota reset
- OR upgrade to Gemini API paid plan
- See `CHATBOT_ISSUE_SUMMARY.md` for details

---

## 📝 Error Flow Diagram

```
User opens chat page
    ↓
ConversationSidebar.tsx loads
    ↓
Calls: conversationsApi.list()
    ↓
API client sends: GET http://localhost:8000/api/conversations
    ↓
❌ Connection refused (backend not running)
    ↓
Network error caught
    ↓
setError("Failed to load conversations")
    ↓
User sees error message
```

```
User types message and presses Enter
    ↓
ChatInput calls: sendMessage(content)
    ↓
use-chat.ts calls: chatApi.sendMessage()
    ↓
API client sends: POST http://localhost:8000/api/chat
    ↓
❌ Connection refused (backend not running)
    ↓
Network error caught
    ↓
Optimistic message removed
    ↓
setError("Network error. Please check your connection.")
    ↓
User sees error message
```

---

## 🎯 Quick Fix Checklist

- [ ] Open terminal in `/mnt/d/todo-fullstack-web/backend`
- [ ] Activate virtual environment
- [ ] Run `uvicorn app.main:app --reload`
- [ ] Wait for "Application startup complete"
- [ ] Open http://localhost:8000/docs to verify
- [ ] Refresh chat page in browser
- [ ] Test sending a message

---

## 📚 Related Documentation

- **Gemini API Quota**: `CHATBOT_ISSUE_SUMMARY.md`
- **Chat Feature Usage**: `CHAT_FEATURE_USAGE_GUIDE.md`
- **Authentication**: `TEST_CHAT_AUTHENTICATION.md`
- **Backend Setup**: `backend/README.md`

---

## ✅ Summary

| Issue | Cause | Solution |
|-------|-------|----------|
| "Failed to load conversation" | Backend not running | Start backend server |
| "Chat message sending fails" | Backend not running | Start backend server |
| Network errors | Connection refused to localhost:8000 | Run `uvicorn app.main:app --reload` |

---

## 🔧 Technical Details

### Frontend API Configuration

**File**: `frontend/lib/api.ts:18`

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hamzabhatti-todo-ai-chatbot.hf.space'
```

This is for task API (GET/POST/DELETE tasks).

**File**: `frontend/lib/chat-api.ts:17`

```typescript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
```

This is for chat API (conversations and messages).

### Backend Endpoints

- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}` - Get conversation with messages
- `GET /api/conversations/{id}/messages` - Get messages for conversation
- `POST /api/chat` - Send chat message and get AI response
- `GET /health` - Health check endpoint

All require JWT authentication in `Authorization` header.

---

## 💡 Prevention

### 1. Always start backend before testing chat

```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### 2. Use Docker Compose for easy startup

```bash
docker-compose up
```

This starts both frontend and backend together.

### 3. Add health check to frontend

Consider adding a health check that shows a warning if backend is unreachable:

```typescript
useEffect(() => {
  const checkBackend = async () => {
    try {
      await fetch('http://localhost:8000/health')
      console.log('✅ Backend is running')
    } catch {
      console.warn('⚠️ Backend is not running on localhost:8000')
    }
  }
  checkBackend()
}, [])
```

---

## 📞 Next Steps

1. **Start the backend server** using one of the methods above
2. **Verify it's running** by checking http://localhost:8000/docs
3. **Refresh the chat page** in your browser
4. **Test conversation history** - should load without errors
5. **Test sending a message** - should work if Gemini API quota is available

---

**Status**: ✅ Root cause identified - backend not running
**Action Required**: User must start the backend server
**Files Modified**: None (no code changes needed)
**Configuration**: All correct - just need to start the server

---

**Fixed By**: Claude Code Agent
**Date**: 2026-01-24
**Diagnosis Time**: 5 minutes
**Solution**: Start backend server
