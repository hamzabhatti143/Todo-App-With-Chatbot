# Username Authentication Testing Guide

**Date**: 2026-01-30
**Status**: Ready for Testing

## Quick Start Testing

### 1. Start the Servers

```bash
# Terminal 1 - Backend
cd backend
./venv/Scripts/python.exe -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Test Registration Flow

1. Navigate to: http://localhost:3000/signup
2. Fill in the form:
   - **Username**: `testuser` (3-50 chars, alphanumeric + _ -)
   - **Email**: `test@example.com`
   - **Password**: `Test1234` (min 8 chars, 1 upper, 1 lower, 1 number)
   - **Confirm Password**: `Test1234`
3. Click "Sign up"
4. ✅ Should redirect to `/dashboard`
5. ✅ Should see "My Tasks" page

### 3. Verify JWT Token

1. Open browser DevTools → Application → Local Storage
2. Check for:
   - `auth_token`: JWT token string
   - `username`: `testuser`
3. Copy the JWT token value
4. Decode it at https://jwt.io
5. ✅ Payload should contain: `{"sub": "testuser", "exp": ...}`

### 4. Test Task Creation

1. On dashboard, click "New Task"
2. Fill in:
   - **Title**: `Test Task 1`
   - **Description**: `Testing username authentication`
3. Click "Create Task"
4. ✅ Task should appear in the list
5. Open DevTools → Network tab
6. Check the request URL
7. ✅ Should be: `/api/testuser/tasks` (not a UUID!)

### 5. Test Logout and Login

1. Click logout (if available) or clear localStorage manually
2. Navigate to: http://localhost:3000/signin
3. Fill in:
   - **Username**: `testuser` (NOT email!)
   - **Password**: `Test1234`
4. Click "Sign in"
5. ✅ Should redirect to `/dashboard`
6. ✅ Should see previously created task

### 6. Test User Isolation (Security)

**Create Second User**:
1. Logout from `testuser`
2. Register new user:
   - Username: `anotheruser`
   - Email: `another@example.com`
   - Password: `Another1234`
3. Create a task: "Another user's task"

**Attempt Unauthorized Access**:
1. Get `testuser`'s JWT token (login as `testuser`)
2. Open DevTools → Console
3. Try to access `anotheruser`'s tasks:
```javascript
fetch('http://localhost:8000/api/anotheruser/tasks', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
  }
}).then(r => r.json()).then(console.log)
```
4. ✅ Should return 403 Forbidden: "Not authorized to access these tasks"

### 7. Test API Endpoints Directly

**Register**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "email": "curl@example.com",
    "password": "Curl1234"
  }'
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "password": "Curl1234"
  }'
```

**Create Task** (replace TOKEN with output from login):
```bash
curl -X POST http://localhost:8000/api/curluser/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "API Created Task",
    "description": "Created via curl"
  }'
```

**Get Tasks**:
```bash
curl http://localhost:8000/api/curluser/tasks \
  -H "Authorization: Bearer TOKEN"
```

## Expected Behavior Checklist

### ✅ Registration
- [ ] Can register with username, email, password
- [ ] Username must be 3-50 characters
- [ ] Username can only contain letters, numbers, _, -
- [ ] Cannot register duplicate username (400 error)
- [ ] Cannot register duplicate email (400 error)
- [ ] Auto-login after registration
- [ ] Redirects to /dashboard

### ✅ Login
- [ ] Login requires **username** (not email)
- [ ] Correct credentials → success
- [ ] Wrong username → 401 Unauthorized
- [ ] Wrong password → 401 Unauthorized
- [ ] JWT token stored in localStorage
- [ ] Username stored in localStorage
- [ ] Redirects to /dashboard

### ✅ Task Management
- [ ] API URLs use `/api/{username}/tasks` format
- [ ] Can create tasks
- [ ] Can view own tasks
- [ ] Can update tasks
- [ ] Can delete tasks
- [ ] Can toggle task completion
- [ ] CANNOT access other users' tasks (403)

### ✅ JWT Token
- [ ] Token contains `"sub": "username"`
- [ ] Token expires after 30 minutes (default)
- [ ] Token signature verified on backend
- [ ] Invalid token → 401 Unauthorized
- [ ] Expired token → 401 Unauthorized

### ✅ UI/UX
- [ ] Signup form has username field (before email)
- [ ] Signin form uses username (not email)
- [ ] Validation errors display correctly
- [ ] Loading states show during API calls
- [ ] Success/error messages appear
- [ ] Dashboard shows username (if displayed)

## Common Issues & Solutions

### Issue: "Username already taken"
**Cause**: Username exists in database
**Solution**: Choose a different username

### Issue: "Invalid username or password"
**Cause**: Wrong credentials OR using email instead of username
**Solution**: Use USERNAME (not email) for login

### Issue: 403 Forbidden on task operations
**Cause**: JWT username doesn't match URL username
**Solution**: Ensure logged in as correct user

### Issue: 401 Unauthorized
**Cause**: Missing, invalid, or expired JWT token
**Solution**: Login again to get fresh token

### Issue: Frontend shows "userId" instead of "username"
**Cause**: Cached localStorage data from old implementation
**Solution**: Clear localStorage and login again

### Issue: Database error "column username does not exist"
**Cause**: Database not recreated with new schema
**Solution**: Run migration again (already completed)

## Verification Commands

### Check Database Schema
```bash
# From backend directory
./venv/Scripts/python.exe -c "from app.database import engine; from sqlmodel import inspect; inspector = inspect(engine); print('Users table columns:'); print(inspector.get_columns('users'))"
```

### Check Registered Users
```bash
./venv/Scripts/python.exe -c "from app.database import engine; from app.models.user import User; from sqlmodel import Session, select; session = Session(engine); users = session.exec(select(User)).all(); print(f'Total users: {len(users)}'); [print(f'- {u.username} ({u.email})') for u in users]"
```

### Check Tasks
```bash
./venv/Scripts/python.exe -c "from app.database import engine; from app.models.task import Task; from sqlmodel import Session, select; session = Session(engine); tasks = session.exec(select(Task)).all(); print(f'Total tasks: {len(tasks)}'); [print(f'- {t.title} (user_id: {t.user_id})') for t in tasks]"
```

## Test Data

### Sample Users
| Username | Email | Password |
|----------|-------|----------|
| testuser | test@example.com | Test1234 |
| johndoe | john@example.com | John1234 |
| janedoe | jane@example.com | Jane1234 |

### Sample Tasks
- Buy groceries for the week
- Complete project documentation
- Schedule dentist appointment
- Review pull requests
- Plan team meeting agenda

## Performance Expectations

All timings with database on localhost:

- Registration: < 500ms
- Login: < 300ms
- Get tasks list: < 200ms
- Create task: < 300ms
- Update task: < 300ms
- Delete task: < 200ms

## Security Validation

### ✅ Password Security
- [ ] Passwords hashed with bcrypt (never stored plain)
- [ ] Password requires complexity (upper, lower, number)
- [ ] Minimum 8 characters enforced

### ✅ JWT Security
- [ ] Signed with SECRET_KEY (check .env)
- [ ] Algorithm: HS256
- [ ] Expiration set and enforced
- [ ] Token required for all task operations

### ✅ User Isolation
- [ ] Cannot view other users' tasks
- [ ] Cannot create tasks for other users
- [ ] Cannot update other users' tasks
- [ ] Cannot delete other users' tasks
- [ ] All checks return 403 Forbidden

### ✅ Input Validation
- [ ] Frontend validates with Zod
- [ ] Backend validates with Pydantic
- [ ] SQL injection prevented (SQLModel ORM)
- [ ] XSS prevented (React escaping)

## Success Criteria

Implementation is successful if:

1. ✅ New users can register with username
2. ✅ Users can login with username (not email)
3. ✅ JWT token contains username in `sub` claim
4. ✅ API URLs use `/api/{username}/tasks` format
5. ✅ User isolation works (403 for other users' data)
6. ✅ All CRUD operations function correctly
7. ✅ Frontend pages use `username` from auth hook
8. ✅ No TypeScript errors in frontend
9. ✅ No Python errors in backend
10. ✅ Database has username column with unique constraint

## Rollback Instructions

If critical issues found:

1. Stop both servers
2. Revert code changes:
```bash
git checkout HEAD~1 -- backend/app/models/user.py backend/app/schemas/user.py backend/app/routes/auth.py backend/app/routes/tasks.py backend/app/dependencies.py frontend/types/user.ts frontend/lib/api.ts frontend/hooks/use-auth.ts frontend/hooks/use-tasks.ts frontend/components/auth/ frontend/validation/user.ts frontend/app/dashboard/page.tsx frontend/app/tasks/page.tsx frontend/app/analytics/page.tsx frontend/app/chat/page.tsx
```
3. Clear database and recreate with old schema
4. Restart servers

## Next Steps After Testing

Once all tests pass:

1. Update CLAUDE.md with username authentication notes
2. Update API documentation
3. Create Alembic migration for production (if using production DB)
4. Consider: Reserved usernames list (admin, api, www, etc.)
5. Consider: Username change functionality
6. Consider: Username search/directory feature
7. Monitor for username enumeration vulnerabilities

## Questions for Product Decision

- [ ] Should usernames be public (visible in URLs)?
- [ ] Should we allow username changes later?
- [ ] Do we need a reserved usernames list?
- [ ] Should we add profanity filter for usernames?
- [ ] Do we want case-insensitive usernames? (johndoe = JohnDoe)
