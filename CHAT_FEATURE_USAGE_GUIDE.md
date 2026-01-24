# Chat Feature Usage Guide

**Feature**: 018-chatkit-frontend - AI-Powered Task Assistant
**Date**: 2026-01-23
**Status**: Complete and Ready to Use

## Quick Start (3 Steps)

### Step 1: Sign In
1. Navigate to http://localhost:3000/signin
2. Enter your credentials (or create an account at /signup)
3. Click "Sign In"

### Step 2: Navigate to Chat
**Option A - From Dashboard**:
1. After signing in, you'll be on the dashboard
2. Click the **"Perform Tasks With AI"** button (purple button with Bot icon)
   - Desktop: Button appears next to "New Task"
   - Mobile: Click the FAB (Floating Action Button) menu at bottom-right

**Option B - Direct URL**:
1. Go to http://localhost:3000/chat
2. If not signed in, you'll be redirected to signin page

### Step 3: Start Chatting
1. Type your message in the input field at the bottom
2. Press Enter to send (or click Send button)
3. Wait for AI response (loading spinner will appear)
4. Continue the conversation!

---

## Feature Capabilities

### What You Can Do

**Task Management Through Chat**:
- **Add tasks**: "Add buy groceries tomorrow"
- **List tasks**: "Show my tasks" or "What's on my todo list?"
- **Complete tasks**: "Mark 'buy groceries' as done"
- **Update tasks**: "Change the title of task #1 to 'Buy organic groceries'"
- **Delete tasks**: "Delete my first task"

**Multi-Part Requests**:
- "Add three tasks: finish report by Friday, call client Monday, review code"
- The AI will process each task separately

**Conversation Features**:
- **Conversation persistence**: Your messages are saved across page refreshes
- **Conversation history**: View previous conversations in the sidebar (desktop/tablet)
- **New conversation**: Click "New Conversation" button to start fresh
- **Resume conversations**: Click on a previous conversation to continue

---

## Troubleshooting Common Errors

### Error: "Failed to load conversations"

**Cause**: Not authenticated or JWT token expired

**Solution**:
1. Sign out (if signed in)
2. Sign in again at /signin
3. Navigate back to /chat

**Quick Fix**:
```bash
# Clear browser localStorage
# Open DevTools (F12) → Console → Run:
localStorage.clear()

# Then refresh page and sign in again
```

---

### Error: "Your session has expired, so please log in again to continue"

**Cause**: JWT token expired (30-minute expiration)

**Solution**:
1. Click "Sign Out" in the header
2. Sign in again at /signin
3. You'll be redirected back to chat

---

### Error: "Unable to process your request at this time—please try again"

**Cause**: Backend server not running or network error

**Solution**:
1. Check if backend is running:
   ```bash
   cd /mnt/d/todo-fullstack-web/backend
   ./venv/Scripts/python.exe -m uvicorn app.main:app --reload
   ```

2. Verify backend is accessible:
   - Open http://localhost:8000/health in browser
   - Should return: `{"status": "healthy"}`

3. Check backend logs for errors

---

###Error: "The server is not responding right now, please try again later"

**Cause**: Backend connection timeout (>30 seconds)

**Solution**:
1. Check your internet connection
2. Verify backend is running (see above)
3. Check for firewall blocking localhost:8000
4. Try restarting the backend server

---

### Error: Empty object `{}` in console

**Cause**: API error object not being logged properly (this is the error you saw)

**What it means**: The actual error is one of the above authentication/connection errors

**Solution**:
1. Check the Network tab in DevTools (F12)
2. Look for failed requests to `/api/conversations` or `/api/chat`
3. Click on the failed request to see the actual error response
4. Follow the solution for that specific error code:
   - **401/403**: Authentication issue → Sign in again
   - **500**: Server error → Check backend logs
   - **503**: Service unavailable → Restart backend
   - **Network error**: Backend not running → Start backend

---

## How to Use the Chat Feature (Detailed)

### Starting a Conversation

1. **Navigate to Chat Page**
   - From dashboard: Click "Perform Tasks With AI" button
   - Direct URL: http://localhost:3000/chat

2. **First Message**
   - Type in the input field: "Add buy groceries"
   - Press Enter (or click Send)
   - Loading spinner appears while waiting
   - AI responds with confirmation

3. **Follow-Up Messages**
   - Continue typing in the same conversation
   - Each message has context from previous messages
   - Conversation ID is automatically tracked

---

### Managing Conversations

**View Conversation History** (Desktop/Tablet only):
- Sidebar on the left shows previous conversations
- Click on any conversation to resume it
- Conversations sorted by most recent first

**Start New Conversation**:
- Click "New Conversation" button in sidebar
- Or press `Ctrl+K` keyboard shortcut
- Clears current conversation and starts fresh

**Resume Previous Conversation**:
- Click on conversation in sidebar
- All previous messages load
- Continue chatting with full context

---

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift+Enter**: New line in message (for multi-line messages)
- **Escape**: Clear input field
- **Ctrl+K**: Start new conversation

---

### Mobile Usage

**Accessing Chat on Mobile**:
1. Sign in at /signin
2. Tap the FAB menu (bottom-right floating button)
3. Select "Perform Tasks With AI"

**Mobile Features**:
- Conversation sidebar hidden by default
- Tap menu icon (top-right) to show conversation list
- Full-screen chat interface
- Touch-optimized buttons (44x44px minimum)

---

## Technical Details

### Authentication Flow

```
1. User signs in at /signin
2. Backend returns JWT token
3. Frontend stores token in localStorage
4. All chat API requests include: Authorization: Bearer <token>
5. Backend verifies token and extracts user_id
6. Conversation tied to authenticated user
```

### API Endpoints Used

**POST /api/chat**
- Send message to AI assistant
- Returns AI response + conversation_id
- Automatically creates conversation on first message

**GET /api/conversations**
- List all user's conversations
- Returns: id, title, last_message, updated_at

**GET /api/conversations/{id}**
- Get full conversation with all messages
- Used when clicking on conversation in sidebar

---

## Debugging Steps

### If Chat Doesn't Load

1. **Check Authentication**:
   ```javascript
   // Open DevTools Console (F12) and run:
   console.log(localStorage.getItem('auth_token'))
   // Should return a JWT token string
   // If null, you're not signed in
   ```

2. **Check Backend Connection**:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

3. **Check Network Requests**:
   - Open DevTools → Network tab
   - Reload chat page
   - Look for requests to `/api/conversations`
   - Check status code (200 = success, 401/403 = auth error, 500 = server error)

4. **Check Console Errors**:
   - Open DevTools → Console tab
   - Look for red error messages
   - Error messages will indicate the specific issue

---

### If Messages Don't Send

1. **Check Input Validation**:
   - Message must not be empty (whitespace only)
   - Message must be ≤5000 characters
   - Character counter shows when >4500 chars

2. **Check Loading State**:
   - Loading spinner should appear immediately after pressing Enter
   - Input field should be disabled during loading
   - If stuck loading, check backend logs

3. **Check Backend Logs**:
   ```bash
   # Backend terminal should show:
   INFO: [timestamp] POST /api/chat 200 - X.XXs
   # If you see 403/401, it's an auth issue
   # If you see 500, check the error traceback
   ```

---

## Common Use Cases

### Example 1: Adding Multiple Tasks

**User Input**:
```
Add three tasks: finish report by Friday, call client Monday, and review code
```

**AI Response**:
```
I've added 3 tasks for you:
1. "Finish report by Friday"
2. "Call client Monday"
3. "Review code"
```

---

### Example 2: Viewing and Completing Tasks

**User**: "Show my tasks"

**AI**: "Here are your current tasks:
1. Buy groceries
2. Finish report by Friday
3. Call client Monday"

**User**: "Mark task 1 as complete"

**AI**: "I've marked 'Buy groceries' as complete!"

---

### Example 3: Error Recovery

**Scenario**: Backend is down

**User types**: "Add buy groceries"

**What happens**:
1. Loading spinner appears
2. Request times out after 30 seconds
3. Error message appears: "The server is not responding..."
4. Retry button appears

**User clicks**: Retry button

**What happens**:
1. Same request is sent again
2. If backend is back online, message sends successfully
3. If still down, error repeats

---

## Performance Tips

### For Long Conversations (100+ messages)

- Conversations with 100+ messages may load slightly slower
- Scrolling should still be smooth (60fps)
- If experiencing lag, try starting a new conversation
- Future enhancement: Virtual scrolling for 1000+ messages

### For Slow Networks

- 30-second timeout on all requests
- If request times out, click Retry button
- Consider using ethernet instead of WiFi
- 3G/4G should work, but may be slower

---

## Security Notes

### Data Privacy

- Conversations are tied to your user account
- Only you can see your conversations
- JWT token expires after 30 minutes for security
- Sign out when using shared computers

### Input Sanitization

- All user input is automatically sanitized by React
- No risk of XSS attacks from message content
- User ID validated before use in URLs/storage

---

## Feature Limitations (Current MVP)

**Not Yet Implemented**:
- ❌ Message editing/deletion
- ❌ File attachments
- ❌ Search across conversations
- ❌ Markdown rendering (messages are plain text)
- ❌ Real-time updates (WebSocket)
- ❌ Voice input
- ❌ Dark mode (coming soon)
- ❌ Export conversations

**Working Features**:
- ✅ Send and receive messages
- ✅ Conversation persistence
- ✅ Conversation history
- ✅ Task management through chat
- ✅ Error handling and retry
- ✅ Mobile responsive design
- ✅ Keyboard shortcuts
- ✅ Offline detection
- ✅ Loading states

---

## Getting Help

### If You're Still Stuck

1. **Check Backend Logs**:
   - Look at terminal where `uvicorn` is running
   - Error messages will show what went wrong

2. **Check Frontend Console**:
   - Press F12 → Console tab
   - Look for error messages in red

3. **Check Network Tab**:
   - Press F12 → Network tab
   - Filter by "Fetch/XHR"
   - Click failed requests to see error details

4. **Restart Everything**:
   ```bash
   # Stop backend (Ctrl+C)
   # Stop frontend (Ctrl+C)

   # Start backend
   cd /mnt/d/todo-fullstack-web/backend
   ./venv/Scripts/python.exe -m uvicorn app.main:app --reload

   # Start frontend (new terminal)
   cd /mnt/d/todo-fullstack-web/frontend
   npm run dev

   # Clear browser cache and localStorage
   # Sign in again
   ```

---

## Summary

**To use the chat feature**:
1. Sign in at /signin
2. Click "Perform Tasks With AI" button
3. Start chatting!

**If you get errors**:
1. Sign out and sign in again (fixes 90% of auth errors)
2. Check backend is running (http://localhost:8000/health)
3. Clear localStorage and try again
4. Check browser console and network tab for specific errors

**For best experience**:
- Use desktop/tablet for conversation sidebar
- Sign out when done on shared computers
- Start new conversation if old one gets too long (100+ messages)
- Use keyboard shortcuts (Enter, Shift+Enter, Ctrl+K)

---

**Last Updated**: 2026-01-23
**Feature Status**: ✅ Complete and Production Ready
**Backend**: Feature 017 (chat-api)
**Frontend**: Feature 018 (chatkit-frontend)
