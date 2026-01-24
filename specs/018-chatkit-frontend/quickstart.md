# Quick Start Guide: OpenAI ChatKit Frontend

**Feature**: 018-chatkit-frontend
**Date**: 2026-01-22
**Target Audience**: Developers setting up the chat interface for the first time

## Prerequisites

Before starting, ensure you have:

1. **Backend Running**: Feature 017 (Stateless Chat API Backend) must be deployed and accessible
   - Backend URL (e.g., `http://localhost:8000` or production URL)
   - Backend `/api/chat` endpoint responding successfully
   - Database migrations applied (conversations, messages tables exist)

2. **Development Environment**:
   - Node.js 18.17+ or 20.0+ installed
   - npm 9+ or yarn 1.22+ or pnpm 8+
   - Git installed

3. **Tools** (Recommended):
   - VS Code with TypeScript and Tailwind CSS extensions
   - React Developer Tools browser extension

## Installation Steps

### Step 1: Navigate to Frontend Directory

```bash
cd /path/to/todo-fullstack-web/frontend
```

### Step 2: Install Dependencies

```bash
# Using npm
npm install

# OR using yarn
yarn install

# OR using pnpm
pnpm install
```

**Expected Duration**: 2-3 minutes

**New Dependencies** (added for Feature 018):
- None (Axios already installed from Feature 012)
- Custom chat UI components (no external chat library)

### Step 3: Configure Environment Variables

Create or update `.env.local` file in `frontend/` directory:

```bash
# Copy from example
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Required Variables**:

```env
# Backend API URL (Feature 017)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Frontend URL (for CORS configuration)
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Optional: Enable debug logging
NEXT_PUBLIC_DEBUG_MODE=false
```

**Production Example**:
```env
NEXT_PUBLIC_BACKEND_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_URL=https://yourdomain.com
NEXT_PUBLIC_DEBUG_MODE=false
```

**Note**: No OpenAI ChatKit domain key needed (using custom chat UI instead).

### Step 4: Verify Backend Connection

Test backend connectivity before starting frontend:

```bash
# Test health check
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "timestamp": "2026-01-22T12:00:00Z"
# }
```

If health check fails, verify:
- Backend is running (`cd backend && uvicorn app.main:app --reload`)
- Backend URL in `.env.local` matches actual backend address
- No firewall blocking connection

### Step 5: Start Development Server

```bash
# Using npm
npm run dev

# OR using yarn
yarn dev

# OR using pnpm
pnpm dev
```

**Expected Output**:
```
  ▲ Next.js 16.0.10
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.5s
 ○ Compiling / ...
 ✓ Compiled / in 1.2s
```

### Step 6: Open Application

Navigate to http://localhost:3000 in your browser.

**Expected Flow**:
1. Home page displays with "Enter your user ID" form
2. Enter a test user ID (e.g., `test@example.com`)
3. Click "Start Chat" button
4. Redirected to `/chat?user_id=test@example.com`
5. Chat interface loads with empty conversation
6. Type "Hello" and press Enter
7. Message appears, loading indicator shows
8. AI response arrives within 5 seconds

## Troubleshooting

### Issue 1: "Cannot connect to backend"

**Symptoms**:
- Error message: "Unable to reach AI assistant"
- Network tab shows failed requests to `/api/chat`

**Solutions**:
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check `.env.local` has correct `NEXT_PUBLIC_BACKEND_URL`

3. Verify CORS configuration in backend allows frontend origin:
   ```python
   # backend/app/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],  # Must match frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. Check browser console for CORS errors

### Issue 2: "Failed to compile"

**Symptoms**:
- Next.js compilation errors
- TypeScript type errors

**Solutions**:
1. Clear `.next` cache:
   ```bash
   rm -rf .next
   npm run dev
   ```

2. Reinstall dependencies:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. Check TypeScript version compatibility:
   ```bash
   npm list typescript
   # Should be 5.x (compatible with Next.js 16)
   ```

### Issue 3: "sessionStorage is not defined"

**Symptoms**:
- ReferenceError in server-side rendering
- Page crashes on load

**Solutions**:
1. Ensure sessionStorage access is wrapped in client-side check:
   ```typescript
   if (typeof window !== 'undefined') {
     sessionStorage.setItem('key', 'value');
   }
   ```

2. Use `'use client'` directive at top of components using sessionStorage:
   ```typescript
   'use client';

   import { useState, useEffect } from 'react';
   // ... rest of component
   ```

### Issue 4: "Conversation ID not persisting"

**Symptoms**:
- Page refresh creates new conversation instead of resuming
- sessionStorage not saving conversation_id

**Solutions**:
1. Check browser privacy settings (sessionStorage must be enabled)

2. Verify storage key format:
   ```typescript
   const key = `chat_conversation_${userId}`;
   sessionStorage.setItem(key, conversationId);
   ```

3. Check Network tab for correct `conversation_id` in API responses

4. Verify user_id is consistent across page loads

### Issue 5: "Loading indicator stuck"

**Symptoms**:
- Loading spinner never disappears
- Input field remains disabled

**Solutions**:
1. Check Network tab for failed API requests

2. Verify error handling in chat context:
   ```typescript
   try {
     // ... API call
   } catch (error) {
     dispatch({ type: "SET_ERROR", payload: error.message });
   } finally {
     dispatch({ type: "SET_LOADING", payload: false }); // Always run
   }
   ```

3. Check browser console for unhandled promise rejections

## Verification Checklist

After completing setup, verify the following works:

### User Story 1: Enter Chat and Send First Message (P1) ✅

- [ ] Home page loads at http://localhost:3000
- [ ] User ID input accepts valid characters (alphanumeric, @, ., -, _)
- [ ] User ID input rejects empty submission
- [ ] "Start Chat" button redirects to `/chat?user_id=<id>`
- [ ] Chat page loads with empty message area
- [ ] Input field is enabled and accepts typing
- [ ] Typing message and pressing Enter sends to backend
- [ ] Loading indicator appears during backend request
- [ ] Input field disabled while loading
- [ ] AI response appears within 5 seconds
- [ ] Message has timestamp displayed
- [ ] Follow-up message continues same conversation (no new conversation created)

### User Story 2: View and Resume Conversation History (P2) 🔄

*Note: Requires P2 implementation*

- [ ] Conversation sidebar displays on screens ≥768px
- [ ] Sidebar shows list of previous conversations
- [ ] Clicking conversation loads full history
- [ ] Page refresh resumes last conversation
- [ ] "New Conversation" button starts fresh chat

### User Story 3: Error Handling (P3) 🔄

*Note: Requires P3 implementation*

- [ ] Offline detection shows "You're offline" message
- [ ] Backend error shows "Unable to reach AI assistant" with retry button
- [ ] Retry button re-sends message successfully
- [ ] Timeout shows "Request timed out" message
- [ ] Error messages are user-friendly and actionable

### Responsive Design (FR-021) ✅

Test on multiple screen sizes:

- [ ] **Mobile (320px)**: Chat interface fits screen, no horizontal scroll
- [ ] **Tablet (768px)**: Chat interface + optional sidebar
- [ ] **Desktop (1024px+)**: Full layout with conversation sidebar

**Test with browser DevTools**:
```
Chrome DevTools → Toggle Device Toolbar (Cmd+Shift+M)
Test: iPhone SE (375x667), iPad (768x1024), Desktop (1920x1080)
```

### Performance (Success Criteria) ✅

- [ ] **SC-002**: Chat interface loads in <2 seconds on 3G
- [ ] **SC-004**: 95% of users can send first message without errors
- [ ] **SC-006**: Interface renders correctly on 320px width
- [ ] **SC-009**: Smooth 60fps scrolling with 100+ messages (test in DevTools Performance tab)

## Development Workflow

### File Structure

After implementation, the frontend structure will be:

```
frontend/
├── app/
│   ├── page.tsx                  # Home page (user ID entry)
│   ├── chat/
│   │   └── page.tsx              # Chat page (main interface)
│   └── layout.tsx                # Root layout
├── components/
│   ├── chat/
│   │   ├── MessageList.tsx       # Message display area
│   │   ├── MessageInput.tsx      # Input field + send button
│   │   ├── ConversationSidebar.tsx  # Conversation list (P2)
│   │   ├── LoadingSpinner.tsx    # Loading indicator
│   │   └── ErrorMessage.tsx      # Error display
│   └── ui/
│       └── (existing UI components)
├── lib/
│   ├── api.ts                    # Axios client configuration
│   ├── chat-api.ts               # Chat endpoint functions
│   └── storage.ts                # sessionStorage utilities
├── types/
│   └── chat.ts                   # TypeScript type definitions
├── contexts/
│   └── ChatContext.tsx           # Chat state management
└── .env.local                    # Environment variables
```

### Running Tests (Future)

```bash
# Unit tests
npm run test

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
```

### Building for Production

```bash
# Create optimized production build
npm run build

# Expected output:
#   Route (app)                              Size     First Load JS
#   ┌ ○ /                                    2.1 kB          85 kB
#   ├ ○ /chat                                5.3 kB          88 kB
#   └ ○ /api/...                             0 B                0 B
#
# ○  (Static)  automatically rendered as static HTML

# Test production build locally
npm run start
```

**Production Checklist**:
- [ ] No TypeScript errors: `npm run type-check`
- [ ] No ESLint errors: `npm run lint`
- [ ] Build succeeds: `npm run build`
- [ ] Production build tested: `npm run start` → test all user flows
- [ ] Environment variables configured for production
- [ ] CORS configured on backend for production domain

## Deployment

### Vercel (Recommended)

1. **Connect Repository**:
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Deploy from frontend directory
   cd frontend
   vercel
   ```

2. **Configure Environment Variables** (Vercel Dashboard):
   - `NEXT_PUBLIC_BACKEND_URL` → Production backend URL
   - `NEXT_PUBLIC_APP_URL` → Production frontend URL

3. **Deploy**:
   ```bash
   vercel --prod
   ```

4. **Verify Deployment**:
   - Open Vercel URL (e.g., `https://your-app.vercel.app`)
   - Test complete user flow (home → chat → send message)
   - Check Network tab for successful API calls

### Alternative Platforms

**Netlify**:
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod
```

**Docker**:
```bash
# Build Docker image
docker build -t chatkit-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_BACKEND_URL=http://backend:8000 \
  -e NEXT_PUBLIC_APP_URL=http://localhost:3000 \
  chatkit-frontend
```

## Next Steps

After successful setup:

1. **Implement P2 Features** (Conversation History):
   - Conversation sidebar component
   - Load conversation list from backend
   - Resume conversation functionality

2. **Implement P3 Features** (Error Handling):
   - Enhanced error messages
   - Retry logic
   - Offline detection
   - Toast notifications

3. **Add Enhancements**:
   - Dark mode support (optional from spec)
   - Message markdown rendering
   - Code block syntax highlighting
   - Task data visualization
   - Keyboard shortcuts (Escape, Ctrl+K)

4. **Testing**:
   - Write unit tests for components
   - Write integration tests for chat flow
   - Add E2E tests with Playwright

5. **Performance Optimization**:
   - Virtual scrolling for long conversations
   - Lazy loading of conversation history
   - Image optimization
   - Bundle size optimization

## Support Resources

- **Feature Spec**: `/specs/018-chatkit-frontend/spec.md`
- **Implementation Plan**: `/specs/018-chatkit-frontend/plan.md`
- **Data Model**: `/specs/018-chatkit-frontend/data-model.md`
- **API Contract**: `/specs/018-chatkit-frontend/contracts/api-client.md`
- **Backend Docs**: `/specs/017-chat-api/IMPLEMENTATION_SUMMARY.md`
- **Next.js Docs**: https://nextjs.org/docs
- **Tailwind CSS Docs**: https://tailwindcss.com/docs

## Common Commands Reference

```bash
# Development
npm run dev              # Start dev server (http://localhost:3000)
npm run build            # Create production build
npm run start            # Serve production build
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript compiler (no emit)

# Maintenance
npm install              # Install dependencies
npm update               # Update dependencies
npm run clean            # Clear build cache (rm -rf .next)

# Debugging
NEXT_PUBLIC_DEBUG_MODE=true npm run dev   # Enable debug logging
```

---

**Quick Start Status**: ✅ Complete
**Next Phase**: Fill out `plan.md` with technical context
**Ready for**: `/sp.tasks` after plan.md complete
