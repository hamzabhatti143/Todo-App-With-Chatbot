# Quick Start Guide - TodoBot Chat API

## 🚀 Running the Server

```bash
cd /mnt/d/todo-fullstack-web/backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
./venv/Scripts/activate   # Windows

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Server will be running at: http://localhost:8001
```

## 📝 Testing the Chat Endpoint

### Quick Test (Python)

```bash
python test_final.py
```

### Complete End-to-End Test

```bash
python test_complete.py
```

Expected output:
```
======================================================================
COMPLETE END-TO-END CHAT TEST
======================================================================

[1/7] Login...                                    [OK]
[2/7] List conversations...                       [OK]
[3/7] Send chat message...                        [OK]
[4/7] Send follow-up...                           [OK]
[5/7] Send command...                             [OK]
[6/7] Get conversation history...                 [OK]
[7/7] Test authentication...                      [OK]

======================================================================
ALL TESTS PASSED
======================================================================
```

## 🔑 API Usage

### 1. Login and Get Token

```bash
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test_chat_user@example.com","password":"SecurePassword123!"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"
```

### 2. Send Chat Message

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content":"Add a task to buy groceries"}' \
  | jq
```

Response:
```json
{
  "conversation_id": "c7fdae43-eeb3-45a4-8a9f-0d15f11f5971",
  "message_id": "...",
  "role": "assistant",
  "content": "I've added the task to buy groceries. If you need anything else, just let me know!",
  "created_at": "2026-01-25T06:05:07Z",
  "task_data": null
}
```

### 3. Continue Conversation

```bash
CONV_ID="c7fdae43-eeb3-45a4-8a9f-0d15f11f5971"  # From previous response

curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"content\":\"Show my tasks\",\"conversation_id\":\"$CONV_ID\"}" \
  | jq
```

### 4. Get Conversation History

```bash
curl -X GET "http://localhost:8001/api/conversations/$CONV_ID/messages" \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

### 5. List All Conversations

```bash
curl -X GET http://localhost:8001/api/conversations \
  -H "Authorization: Bearer $TOKEN" \
  | jq
```

## 💬 Chat Commands

TodoBot understands natural language. Try these commands:

### Add Tasks
- "Add a task to buy groceries"
- "Create a task: finish the report"
- "Remind me to call mom"

### List Tasks
- "Show my tasks"
- "List all pending tasks"
- "What do I need to do?"

### Complete Tasks
- "Mark the groceries task as done"
- "I finished the report"
- "Complete the first task"

### Update Tasks
- "Update the groceries task to include milk and bread"
- "Change the report task title to 'Finish quarterly report'"

### Delete Tasks
- "Delete the groceries task"
- "Remove the old meeting task"

## 🔍 Available Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Chat
- `POST /api/chat` - Send message to TodoBot
  - Headers: `Authorization: Bearer <token>`
  - Body: `{"content": "your message", "conversation_id": "optional-uuid"}`

### Conversations
- `GET /api/conversations` - List all user conversations
- `GET /api/conversations/{id}/messages` - Get conversation history

### Health
- `GET /` - Server health check
- `GET /health` - Database connectivity check
- `GET /docs` - Interactive API documentation (Swagger)
- `GET /redoc` - Alternative API documentation

## 🐛 Troubleshooting

### Server won't start on port 8000
**Solution**: Use port 8001 or another available port
```bash
python -m uvicorn app.main:app --port 8001
```

### "Could not validate credentials" error
**Solution**: Ensure you're sending the JWT token in the Authorization header
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" ...
```

### Rate limit errors (if re-enabled)
**Solution**: Wait 1 minute before retrying (default: 10 requests/minute)

### Database connection errors
**Solution**: Ensure SQLite database file exists and is writable
```bash
ls -la test.db
chmod 644 test.db  # If needed
```

## 📚 Documentation

- **FIX_SUMMARY.md** - Details on the recent bug fix
- **TODOBOT_COMMAND_GUIDE.md** - Complete command reference
- **QUICK_REFERENCE.md** - Quick command lookup
- **API_TESTING_GUIDE.md** - Detailed API testing examples
- **README_COMMANDS.md** - Overview of all documentation

## ✅ Verification Checklist

- [ ] Server starts successfully on port 8001
- [ ] Can login and receive JWT token
- [ ] Can send chat messages and receive responses
- [ ] TodoBot creates tasks correctly
- [ ] Conversation history is maintained
- [ ] Authentication works (401/403 for unauthorized requests)
- [ ] All tests in `test_complete.py` pass

## 🎉 Success Indicators

When everything is working, you should see:
- Server startup message: "Application startup complete"
- Chat responses from TodoBot
- Tasks being created/listed/completed/deleted
- Conversation history tracking correctly

---

**Need Help?** Run `python test_complete.py` to verify all functionality.
**API Docs**: http://localhost:8001/docs (when server is running)
