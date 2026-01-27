# TodoBot API Testing Guide

**Testing the Chat Endpoint with curl/Postman**

---

## 🌐 Endpoint Information

**Base URL**: `http://localhost:8000`
**Endpoint**: `POST /api/chat`
**Authentication**: Required (JWT Bearer token)
**Content-Type**: `application/json`

---

## 🔐 Getting a JWT Token

First, you need to authenticate and get a token:

### Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "created_at": "2026-01-24T12:00:00Z"
}
```

### Login to Get Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save the access_token** - you'll need it for all chat requests!

---

## 💬 Chat Endpoint Examples

### 1️⃣ Add a Task

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Add a task to buy groceries"
  }'
```

**Response:**
```json
{
  "conversation_id": "conv-uuid-123",
  "message_id": "msg-uuid-456",
  "role": "assistant",
  "content": "I've created the task to buy groceries. If you need anything else, just let me know!",
  "created_at": "2026-01-24T12:00:00Z",
  "task_data": {}
}
```

---

### 2️⃣ Add Task with Description

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Add prepare presentation with description: include Q4 sales charts",
    "conversation_id": "conv-uuid-123"
  }'
```

---

### 3️⃣ List All Tasks

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Show my tasks",
    "conversation_id": "conv-uuid-123"
  }'
```

**Response:**
```json
{
  "conversation_id": "conv-uuid-123",
  "message_id": "msg-uuid-789",
  "role": "assistant",
  "content": "Your tasks:\n◯ Buy groceries\n◯ Prepare presentation",
  "created_at": "2026-01-24T12:01:00Z",
  "task_data": {}
}
```

---

### 4️⃣ List Pending Tasks

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Show pending tasks",
    "conversation_id": "conv-uuid-123"
  }'
```

---

### 5️⃣ Update a Task

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Update the groceries task to Buy groceries from Whole Foods",
    "conversation_id": "conv-uuid-123"
  }'
```

---

### 6️⃣ Complete a Task

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Mark the groceries task as done",
    "conversation_id": "conv-uuid-123"
  }'
```

**Response:**
```json
{
  "conversation_id": "conv-uuid-123",
  "message_id": "msg-uuid-101",
  "role": "assistant",
  "content": "✓ Task completed: Buy groceries. Great job!",
  "created_at": "2026-01-24T12:02:00Z",
  "task_data": {}
}
```

---

### 7️⃣ Delete a Task

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Delete the presentation task",
    "conversation_id": "conv-uuid-123"
  }'
```

---

### 8️⃣ Show Completed Tasks

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "Show completed tasks",
    "conversation_id": "conv-uuid-123"
  }'
```

---

## 🔄 Conversation Flow

### Important: conversation_id

- **First message**: Omit `conversation_id` or set to `null`
  - A new conversation will be created
  - Response includes `conversation_id`

- **Follow-up messages**: Include the `conversation_id`
  - Maintains conversation context
  - Agent remembers previous messages

**Example Flow:**

```bash
# Message 1 (new conversation)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"content": "Add buy milk"}'

# Response includes: "conversation_id": "abc-123"

# Message 2 (same conversation)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "content": "Show my tasks",
    "conversation_id": "abc-123"
  }'
```

---

## 📝 Testing Script (Bash)

Save this as `test_todobot.sh`:

```bash
#!/bin/bash

# Configuration
BASE_URL="http://localhost:8000"
EMAIL="test@example.com"
PASSWORD="TestPassword123!"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== TodoBot API Test ===${NC}\n"

# Step 1: Login and get token
echo -e "${GREEN}Step 1: Logging in...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "Failed to get token. Registering new user..."
    curl -X POST $BASE_URL/api/auth/register \
      -H "Content-Type: application/json" \
      -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}"

    LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
      -H "Content-Type: application/json" \
      -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
fi

echo -e "Token: ${TOKEN:0:20}...\n"

# Step 2: Add a task
echo -e "${GREEN}Step 2: Adding a task...${NC}"
curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Add a task to buy groceries"}' | jq

echo ""

# Step 3: List tasks
echo -e "${GREEN}Step 3: Listing tasks...${NC}"
curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Show my tasks"}' | jq

echo ""

# Step 4: Complete task
echo -e "${GREEN}Step 4: Completing task...${NC}"
curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Mark the groceries task as done"}' | jq

echo ""

echo -e "${BLUE}=== Test Complete ===${NC}"
```

**Run it:**
```bash
chmod +x test_todobot.sh
./test_todobot.sh
```

---

## 🧪 Postman Collection

### Import into Postman

1. Create new collection: "TodoBot API"
2. Add environment variables:
   - `base_url`: `http://localhost:8000`
   - `token`: (will be set after login)

### Request 1: Login

- **Method**: POST
- **URL**: `{{base_url}}/api/auth/login`
- **Body**:
```json
{
  "email": "test@example.com",
  "password": "TestPassword123!"
}
```
- **Test Script**:
```javascript
pm.environment.set("token", pm.response.json().access_token);
```

### Request 2: Chat - Add Task

- **Method**: POST
- **URL**: `{{base_url}}/api/chat`
- **Headers**:
  - `Authorization`: `Bearer {{token}}`
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "content": "Add a task to buy groceries"
}
```
- **Test Script**:
```javascript
pm.environment.set("conversation_id", pm.response.json().conversation_id);
```

### Request 3: Chat - List Tasks

- **Method**: POST
- **URL**: `{{base_url}}/api/chat`
- **Headers**:
  - `Authorization`: `Bearer {{token}}`
- **Body**:
```json
{
  "content": "Show my tasks",
  "conversation_id": "{{conversation_id}}"
}
```

---

## 🐛 Debugging

### Check if server is running:

```bash
curl http://localhost:8000/docs
```

Should open FastAPI Swagger documentation.

### Check authentication:

```bash
# This should return 401 Unauthorized
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"content": "test"}'
```

### Check with valid token:

```bash
# This should work
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_VALID_TOKEN" \
  -d '{"content": "Hello"}'
```

### Common Issues:

1. **401 Unauthorized**: Token expired or invalid
   - Solution: Login again to get a new token

2. **403 Forbidden**: User mismatch or permissions issue
   - Solution: Verify user owns the conversation

3. **422 Unprocessable Entity**: Invalid request format
   - Solution: Check JSON syntax and required fields

4. **500 Internal Server Error**: Server-side error
   - Solution: Check backend logs

---

## 📊 Testing Checklist

- [ ] Can register a new user
- [ ] Can login and get token
- [ ] Can add a task via chat
- [ ] Can list tasks via chat
- [ ] Can update a task via chat
- [ ] Can complete a task via chat
- [ ] Can delete a task via chat
- [ ] Conversation context works across messages
- [ ] Agent responds appropriately to natural language
- [ ] Errors are handled gracefully

---

## 🚀 Quick Test

One-liner to test the entire flow:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPassword123!"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4) && \
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Add buy milk and show my tasks"}' | jq
```

---

**Happy Testing! 🎉**
