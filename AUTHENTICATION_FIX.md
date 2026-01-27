# Authentication Fix Guide

**Issue**: Frontend showing "Could not validate credentials" (401 errors)
**Root Cause**: Old JWT token in browser localStorage from previous database/user
**Status**: ✅ FIX AVAILABLE

---

## The Problem

The frontend has a JWT token stored in `localStorage` that references a user ID (`5ae72e70-1647-4b5e-a703-88779f9fe1b5`) that doesn't exist in the current database. The current test user has a different ID (`cd3e7385-5d9c-40be-81e5-82a58a7d1afe`).

**Backend Logs Show**:
```
Authentication: Extracted user_id from token: 5ae72e70-1647-4b5e-a703-88779f9fe1b5
Authentication: User 5ae72e70-1647-4b5e-a703-88779f9fe1b5 not found in database
401 Unauthorized
```

---

## Quick Fix (1 Minute)

### Option 1: Clear Browser Storage (Recommended)

1. Open your browser at http://localhost:3000
2. Open Developer Tools (F12 or Right-click → Inspect)
3. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
4. Find "Local Storage" → "http://localhost:3000"
5. Delete these keys:
   - `auth_token`
   - `user_id`
6. Refresh the page (F5)
7. You should be redirected to the login page
8. Login with:
   - Email: `test_chat_user@example.com`
   - Password: `SecurePassword123!`

### Option 2: Use Incognito/Private Window

1. Open a new Incognito/Private window
2. Go to http://localhost:3000
3. Login with test credentials

### Option 3: Click Logout (If Available)

1. If you can see a logout button, click it
2. This will clear localStorage automatically
3. Then login again with correct credentials

---

## Detailed Explanation

### What Happened

1. **Previous Session**: You had logged in before, and the frontend stored a JWT token
2. **Database Changed**: The backend is now using a different database (or migrations were reset)
3. **Token Mismatch**: The old token references a user that no longer exists
4. **401 Errors**: Backend rejects all requests because it can't find the user

### How JWT Authentication Works

```
┌─────────────┐
│   Browser   │
│ localStorage│
│  auth_token │
└──────┬──────┘
       │
       │ Bearer eyJhbGci...
       ▼
┌─────────────┐
│   Backend   │
│  Decode JWT │
│  Extract ID │
└──────┬──────┘
       │
       │ Look up user_id
       ▼
┌─────────────┐
│  Database   │
│ Find user?  │
└─────────────┘

✅ User found → 200 OK
❌ User not found → 401 Unauthorized
```

### Why This Happens

This is common during development when:
- Database is reset or migrations are run
- Switching between different database instances
- Test data is cleared
- Backend is redeployed with new database

---

## Automatic Fix (Already Implemented)

The frontend **already has automatic handling** for this in `lib/api.ts`:

```typescript
// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Automatically clear auth state
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_id')

      // Redirect to sign in
      window.location.href = '/signin?expired=true'
    }
    return Promise.reject(error)
  }
)
```

**However**, this only triggers **after** the first 401 error. So you'll see:
1. First request → 401 error → localStorage cleared
2. Page redirect to /signin
3. Login again → Fresh token → Everything works

---

## Testing the Fix

### Step 1: Clear Storage (Use Quick Fix Above)

### Step 2: Login

Visit http://localhost:3000/signin and login:
- Email: `test_chat_user@example.com`
- Password: `SecurePassword123!`

### Step 3: Verify Authentication

Open Developer Tools Console and check:
```javascript
localStorage.getItem('auth_token')
// Should return: "eyJhbGciOiJIUzI1NiIs..."

localStorage.getItem('user_id')
// Should return: "cd3e7385-5d9c-40be-81e5-82a58a7d1afe"
```

### Step 4: Test Chat

1. Navigate to http://localhost:3000/chat
2. Send a message: "Add a task to buy groceries"
3. Wait for response (2-5 seconds)
4. You should see AI response without errors

### Step 5: Check Network Tab

Open Developer Tools → Network tab:
- Look for `/api/chat` request
- Should show status: 200 OK
- Headers should include: `Authorization: Bearer eyJhbGci...`

---

## Preventing This Issue

### For Development

1. **Use Consistent Database**:
   - Don't reset migrations while developing
   - Or clear localStorage after resetting

2. **Test User Script**:
   - Run `./venv/Scripts/python.exe create_test_user.py` after database reset
   - This creates the test user in the new database

3. **Logout Before Changes**:
   - Always logout before resetting backend/database
   - Or use Incognito mode for testing

### For Production

The automatic 401 handler ensures that:
- Expired tokens are automatically cleared
- User is redirected to login
- No manual intervention needed

---

## Troubleshooting

### Still Getting 401 After Clearing Storage?

1. **Check Backend is Running**:
   ```bash
   curl http://localhost:8002/health
   ```
   Should return: `{"status": "healthy", "database": "connected"}`

2. **Check Test User Exists**:
   ```bash
   cd /mnt/d/todo-fullstack-web/backend
   ./venv/Scripts/python.exe test_connection.py
   ```

3. **Check Backend Logs**:
   Look at backend terminal for errors

4. **Verify Environment Variables**:
   - Backend: `JWT_SECRET_KEY` in `.env`
   - Frontend: Correct `NEXT_PUBLIC_API_URL` in `.env.local`

### Login Not Working?

1. **User Doesn't Exist**:
   ```bash
   ./venv/Scripts/python.exe create_test_user.py
   ```

2. **Wrong Password**:
   - Password: `SecurePassword123!` (case-sensitive, with exclamation mark)

3. **Backend Not Responding**:
   - Check if backend is running on port 8002
   - Check CORS is allowing localhost:3000

### Chat Still Shows Errors?

1. **Refresh Page**: After login, refresh the chat page
2. **Check Console**: Look for JavaScript errors
3. **Check Network Tab**: Verify requests have Authorization header
4. **Check Backend Logs**: Look for request processing

---

## Summary

**The Fix**:
1. Clear localStorage (auth_token and user_id)
2. Login again with test credentials
3. Everything will work!

**Why It Works**:
- Fresh token with correct user_id
- Backend can find the user in database
- All requests authenticated properly

**Prevention**:
- Use logout before database changes
- Or use Incognito mode for testing
- Or clear storage manually when needed

---

**Last Updated**: 2026-01-25
**Status**: Issue Identified and Fix Documented
**Time to Fix**: 1 minute (clear storage + login)
