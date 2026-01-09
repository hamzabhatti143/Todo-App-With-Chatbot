# Quickstart: Frontend-Backend API Communication Verification

**Feature**: 011-frontend-backend-api
**Prerequisites**: Both frontend and backend servers must be running

## 🚀 Quick Test (30 seconds)

### Step 1: Start Servers

**Backend** (Terminal 1):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

### Step 2: Open Test Page

Navigate to: **http://localhost:3000**

### Step 3: Test Health Check

1. Look for **"Backend Connection Test"** section
2. Click **"Test Backend Connection"** button
3. ✅ Success: Green box shows `{"status":"ok"}`
4. ❌ Error: Red box shows troubleshooting steps

### Step 4: Test Authentication

1. Scroll to **"Authentication Endpoint Test"** section
2. Email: `test@example.com` (default)
3. Password: `password123` (default)
4. Click **"Test Register"** → Verify user created
5. Click **"Test Login"** → Verify JWT token received

---

## 📋 What Gets Tested

### Health Check (`/health`)
- ✓ Backend server is running
- ✓ Frontend can make HTTP requests
- ✓ CORS is configured correctly
- ✓ Response is valid JSON
- ✓ No network errors

### Registration (`/api/auth/register`)
- ✓ User account creation works
- ✓ Password hashing is functional
- ✓ Database persistence works
- ✓ Duplicate email detection works
- ✓ Response includes user ID

### Login (`/api/auth/login`)
- ✓ User authentication works
- ✓ Password verification works
- ✓ JWT token generation works
- ✓ Token has correct structure
- ✓ Invalid credentials are rejected

---

## 🔍 Browser DevTools Verification

### Console Tab (F12 → Console)
**Expected**: No errors

```
No CORS errors
No network errors
No JavaScript errors
```

### Network Tab (F12 → Network)

**After Health Check**:
```
Request: GET http://localhost:8000/health
Status: 200 OK
Response: {"status":"ok"}
Headers: Access-Control-Allow-Origin: http://localhost:3000
```

**After Registration**:
```
Request: POST http://localhost:8000/api/auth/register
Status: 201 Created
Response: {
  "id": "uuid",
  "email": "test@example.com",
  "created_at": "...",
  "updated_at": "..."
}
```

**After Login**:
```
Request: POST http://localhost:8000/api/auth/login
Status: 200 OK
Response: {
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## ⚠️ Common Issues & Fixes

### Issue 1: "Connection Failed" Error

**Symptoms**: Red error box, "Failed to connect to backend"

**Cause**: Backend server not running

**Fix**:
```bash
# Check backend is running
curl http://localhost:8000/health

# If not running, start it
cd backend
source venv/bin/activate
uvicorn app.main:app --port 8000 --reload
```

---

### Issue 2: CORS Error in Console

**Symptoms**: Browser console shows CORS error

**Cause**: CORS misconfiguration

**Fix**:
```bash
# Verify backend .env has correct CORS_ORIGINS
cd backend
cat .env | grep CORS_ORIGINS

# Should show:
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# If not, update .env and restart backend
```

---

### Issue 3: "User Already Exists" Error

**Symptoms**: Registration fails with "User already exists"

**Cause**: Email already registered in database

**Fix**:
```bash
# Option 1: Use different email
Change email to: test2@example.com

# Option 2: Reset database (SQLite)
cd backend
rm test.db
# Restart backend (will recreate tables)

# Option 3: Test login instead
Click "Test Login" button with existing credentials
```

---

### Issue 4: Invalid Credentials on Login

**Symptoms**: Login fails with "Invalid credentials"

**Cause**: User not registered or wrong password

**Fix**:
```bash
# Ensure user is registered first
1. Click "Test Register" button
2. Wait for success message
3. Then click "Test Login" button

# Use exact same email/password for both
```

---

### Issue 5: Frontend Page Shows "Loading..."

**Symptoms**: Page stuck on "Loading..." text

**Cause**: Frontend server not running or compilation error

**Fix**:
```bash
# Check frontend terminal for errors
cd frontend
npm run dev

# If TypeScript errors, fix them:
npx tsc --noEmit

# Check browser console for JavaScript errors
```

---

## 📊 Success Criteria Checklist

### Before Testing
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database accessible (SQLite or PostgreSQL)
- [ ] Environment variables configured (.env files)

### After Health Check Test
- [ ] Green success box appears
- [ ] Response shows `{"status":"ok"}`
- [ ] No CORS errors in console
- [ ] Network tab shows 200 OK status
- [ ] Response time under 2 seconds

### After Registration Test
- [ ] Green success box appears
- [ ] User ID (UUID) displayed
- [ ] Email matches input
- [ ] Created/updated timestamps shown
- [ ] No password in response

### After Login Test
- [ ] Green success box appears
- [ ] JWT token displayed (eyJ...)
- [ ] Token type is "bearer"
- [ ] Token has 3 parts (header.payload.signature)
- [ ] Token preview shows first 50 characters

### Browser DevTools
- [ ] Console has zero errors
- [ ] Network tab shows all 200/201 status codes
- [ ] CORS headers present in responses
- [ ] Request/response bodies are valid JSON

---

## 🎯 Next Steps

### After Successful Testing

1. **Test in Swagger UI**:
   - Visit http://localhost:8000/docs
   - Try endpoints interactively
   - Copy JWT token for protected endpoints

2. **Test Protected Endpoints** (if implemented):
   - Use JWT token from login
   - Test task CRUD operations
   - Verify user isolation

3. **Test Error Scenarios**:
   - Stop backend → Verify error handling
   - Use wrong credentials → Verify 401 error
   - Register duplicate email → Verify 400 error

4. **Integration Testing**:
   - Complete full user flow
   - Register → Login → Use token → Access protected resources

---

## 🛠️ Development Workflow

### Making Changes to Test Page

1. Edit `frontend/app/page.tsx`
2. Hot reload updates automatically
3. Refresh browser to see changes
4. Check console for errors

### Testing Different Scenarios

```typescript
// Test with different credentials
setTestEmail('newuser@example.com')
setTestPassword('newpassword123')

// Test error handling
try {
  // Make API call
} catch (err) {
  // Verify error displays correctly
}
```

### Debugging Tips

1. **Check Network Tab**: See exact request/response
2. **Check Console Tab**: See JavaScript errors
3. **Check Backend Logs**: See server-side errors
4. **Use Swagger UI**: Test endpoints independently

---

## 📚 Related Documentation

- **Feature Spec**: `specs/011-frontend-backend-api/spec.md`
- **Implementation Plan**: `specs/011-frontend-backend-api/plan.md`
- **Data Model**: `specs/011-frontend-backend-api/data-model.md`
- **API Contracts**: `specs/011-frontend-backend-api/contracts/`
- **Backend Docs**: http://localhost:8000/docs

---

## ✅ Validation Checklist

Run through this checklist to confirm everything works:

```
✅ Health Check Test
  ✅ Button clickable
  ✅ Shows loading state
  ✅ Displays success message
  ✅ Shows response data
  ✅ No console errors

✅ Registration Test
  ✅ Email/password inputs work
  ✅ Button clickable
  ✅ Shows loading state
  ✅ Displays success message
  ✅ Shows user ID and email
  ✅ Duplicate email error works

✅ Login Test
  ✅ Uses same credentials as registration
  ✅ Button clickable
  ✅ Shows loading state
  ✅ Displays JWT token
  ✅ Token structure correct
  ✅ Invalid credentials error works

✅ Browser DevTools
  ✅ No errors in Console tab
  ✅ Requests visible in Network tab
  ✅ 200/201 status codes
  ✅ CORS headers present
  ✅ JSON responses valid

✅ Error Handling
  ✅ Backend down → Error message
  ✅ CORS misconfigured → Error guidance
  ✅ Invalid input → Validation error
  ✅ Network timeout → Timeout error
```

**All checks passing?** ✅ Integration verified successfully!
