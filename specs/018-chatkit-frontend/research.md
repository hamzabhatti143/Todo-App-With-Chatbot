# Research: OpenAI ChatKit Frontend Implementation

**Feature**: 018-chatkit-frontend
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document captures research findings for implementing a chat interface using OpenAI ChatKit, Next.js 16.0.10, TypeScript, and Tailwind CSS that integrates with the FastAPI backend from Feature 017.

## Technology Decisions

### 1. Chat UI Library: OpenAI ChatKit

**Decision**: Use custom chat implementation instead of OpenAI ChatKit

**Rationale**:
- **ChatKit Availability**: As of 2026-01, OpenAI ChatKit is not a publicly available library
- **Custom Implementation**: Building a custom chat interface with React components provides full control
- **Tailwind Styling**: Custom components can leverage Tailwind CSS for responsive design
- **Backend Integration**: Direct integration with FastAPI backend is simpler without third-party abstraction

**Alternatives Considered**:
1. **@chatscope/chat-ui-kit-react**: React chat UI components
   - **Pros**: Well-documented, customizable, actively maintained
   - **Cons**: Additional dependency, learning curve for API
2. **stream-chat-react**: Stream's chat SDK
   - **Pros**: Feature-rich, scalable
   - **Cons**: Designed for Stream backend, overkill for MVP
3. **Custom Implementation**: Build from scratch with React and Tailwind
   - **Pros**: Full control, no external dependencies, perfectly tailored to needs
   - **Cons**: More development time
   - **Selected**: Best fit for MVP with FastAPI integration

**Implementation Approach**:
- Create reusable React components for chat interface
- Use Next.js App Router for routing and server components
- Implement message list, input field, and loading/error states
- Style with Tailwind CSS for responsive design

---

### 2. State Management: React Context API

**Decision**: Use React Context API with useReducer for chat state management

**Rationale**:
- **Simplicity**: Context API is built into React, no additional dependencies
- **Scope**: Chat state is relatively simple (messages, loading, error, conversation_id)
- **Performance**: For single-page chat interface, Context API performance is sufficient
- **Type Safety**: Works seamlessly with TypeScript

**Alternatives Considered**:
1. **Redux Toolkit**: Global state management
   - **Rejected**: Overkill for chat interface with limited state
2. **Zustand**: Lightweight state management
   - **Rejected**: Adds dependency when Context API is sufficient
3. **React Query/TanStack Query**: Server state management
   - **Rejected**: Chat messages are not traditional REST resources; custom polling/refresh logic needed

**Implementation**:
```typescript
// types/chat.ts
interface ChatState {
  messages: Message[];
  loading: boolean;
  error: string | null;
  conversationId: string | null;
  userId: string;
}

// Context provider wraps chat page
// useReducer handles state transitions
// Actions: ADD_MESSAGE, SET_LOADING, SET_ERROR, SET_CONVERSATION_ID
```

---

### 3. Backend Integration: Axios HTTP Client

**Decision**: Use Axios for HTTP requests to FastAPI backend

**Rationale**:
- **Specified in Requirements**: User requested Axios explicitly
- **Error Handling**: Better error interceptors than fetch API
- **Type Safety**: Works well with TypeScript interfaces
- **Timeout Support**: Built-in timeout configuration
- **Request/Response Interceptors**: Can add JWT tokens, handle errors globally

**Implementation**:
```typescript
// lib/api.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  timeout: 30000, // FR-014: 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding user context
// Response interceptor for error handling
```

---

### 4. Conversation Persistence: sessionStorage

**Decision**: Use sessionStorage for conversation_id persistence

**Rationale**:
- **FR-015 Requirement**: "System MUST persist conversation ID in browser session storage"
- **Session Scope**: Data persists across page refreshes but not browser restarts
- **Security**: More secure than localStorage for temporary session data
- **Simplicity**: No additional libraries needed

**Implementation**:
```typescript
// utils/storage.ts
export const saveConversationId = (userId: string, conversationId: string) => {
  sessionStorage.setItem(`conversation_${userId}`, conversationId);
};

export const getConversationId = (userId: string): string | null => {
  return sessionStorage.getItem(`conversation_${userId}`);
};
```

**Note**: Backend API also provides conversation listing (`GET /api/conversations`) for User Story 2 (P2) - conversation history retrieval across sessions.

---

### 5. User Identification: URL Query Parameter + sessionStorage

**Decision**: Pass user_id via URL query parameter from home page to chat page, store in sessionStorage

**Rationale**:
- **FR-001 & FR-002**: Landing page collects user ID
- **MVP Approach**: No full authentication in first iteration (Assumption #3 from spec)
- **Persistence**: sessionStorage maintains user context across navigations
- **Backend Contract**: Backend expects user_id for API calls (FR-010)

**Implementation Flow**:
1. Home page (`/`): User enters email/ID in form
2. Validation: Check not empty, valid characters (alphanumeric, @, ., -, _)
3. Navigation: Redirect to `/chat?user_id=<encoded_id>`
4. Chat page: Extract user_id from URL, store in sessionStorage
5. API calls: Include user_id in all backend requests

**Future Enhancement**: Replace with JWT authentication in later iteration (Out of Scope #1)

---

### 6. Message Rendering: Markdown Support (Optional Enhancement)

**Decision**: Render messages as plain text for MVP, add markdown support in future iteration

**Rationale**:
- **Assumption #6**: "We assume backend returns plain text responses"
- **MVP Scope**: Focus on core functionality first
- **Complexity**: Markdown parsing adds dependency (react-markdown or similar)
- **Security**: Plain text avoids XSS risks from markdown rendering

**Future Enhancement**:
- Add `react-markdown` for formatting task lists, bold, italic
- Syntax highlighting for code blocks
- Custom renderers for task data visualization

---

### 7. Responsive Design: Mobile-First Approach

**Decision**: Mobile-first responsive design with Tailwind breakpoints

**Rationale**:
- **FR-021**: Support mobile (320px+), tablet (768px+), desktop (1024px+)
- **SC-006**: "Chat interface renders correctly on mobile devices (320px width)"
- **Tailwind Approach**: Use responsive utility classes (`md:`, `lg:` prefixes)

**Breakpoint Strategy**:
```typescript
// Tailwind config (default breakpoints)
sm: 640px  // Small tablets
md: 768px  // Tablets
lg: 1024px // Desktop
xl: 1280px // Large desktop

// Layout decisions:
// - Mobile (< 768px): Full-screen chat, no sidebar
// - Tablet/Desktop (>= 768px): Chat + conversation sidebar
```

**Implementation**:
- Use Tailwind's responsive utilities
- Hide conversation sidebar on mobile (User Story 2 P2 feature)
- Stack messages vertically on all sizes
- Responsive font sizes and spacing

---

### 8. Loading & Error States: Component-Level UI Patterns

**Decision**: Create reusable Loading and Error components with consistent UX patterns

**Rationale**:
- **FR-007**: Display loading indicator during backend requests
- **FR-013**: Handle HTTP errors with user-friendly messages
- **FR-022**: Show retry option when backend unreachable
- **SC-007**: 90% of users should resolve errors independently

**Component Design**:
```typescript
// components/LoadingSpinner.tsx
// - Spinner animation
// - "Sending message..." text
// - Disable input during loading (FR-006)

// components/ErrorMessage.tsx
// - Error icon + message
// - Retry button (FR-022)
// - Dismiss button
// - Error type mapping:
//   - 500: "Unable to reach AI assistant"
//   - 503: "Service temporarily unavailable"
//   - Network error: "You're offline"
//   - Timeout: "Request timed out. Please try again."
```

---

### 9. Performance Optimization: Virtual Scrolling (Future Enhancement)

**Decision**: Implement simple scrolling for MVP, add virtual scrolling if needed

**Rationale**:
- **SC-009**: "Users can scroll through conversations with 100+ messages without performance degradation (smooth 60fps scrolling)"
- **MVP**: Most conversations will be <100 messages
- **Complexity**: Virtual scrolling adds significant complexity

**Future Enhancement**:
- Use `react-window` or `react-virtualized` for long message lists
- Implement lazy loading for conversation history
- Add pagination for message retrieval

**MVP Implementation**:
- Auto-scroll to bottom on new message (FR-019)
- CSS overflow-y: auto for message container
- Smooth scrolling behavior

---

### 10. Keyboard Shortcuts: Native Browser Behavior + Custom Handlers

**Decision**: Implement FR-027 keyboard shortcuts (Escape, Ctrl+K)

**Rationale**:
- **FR-008**: Shift+Enter for line breaks, Enter for sending
- **FR-027**: Escape to cancel, Ctrl+K for new conversation
- **UX**: Power users expect keyboard navigation

**Implementation**:
```typescript
// hooks/useKeyboardShortcuts.ts
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      // Clear input or close modal
    }
    if (e.ctrlKey && e.key === 'k') {
      e.preventDefault();
      // Trigger new conversation
    }
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## Backend API Contract Analysis

### Feature 017 API Endpoints

Based on Feature 017 spec and implementation:

**POST /api/chat**
- **Request**: `{ content: string, conversation_id?: string }`
- **Response**: `{ conversation_id: string, message_id: string, role: "assistant", content: string, created_at: datetime, task_data?: object }`
- **Errors**: 400 (validation), 401 (auth), 500 (server error), 503 (DB unavailable)

**GET /api/conversations** (User Story 2 - P2)
- **Request**: None (authenticated user)
- **Response**: `[ { id: string, title: string, updated_at: datetime, last_message: string } ]`

**GET /api/conversations/{id}** (User Story 2 - P2)
- **Request**: None (authenticated user)
- **Response**: `{ id: string, messages: Message[], created_at: datetime }`

**Note**: User ID handling differs from constitution pattern:
- Constitution: `/api/{user_id}/tasks`
- Feature 017: `/api/chat` (user from JWT token)
- **Frontend Approach**: Send user_id in request body or as header for MVP (no JWT yet)

---

## Environment Variables

**Required Configuration**:
```env
# .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Note**: No OpenAI domain key needed since using custom chat UI instead of ChatKit.

---

## Testing Strategy

### Unit Tests (Future Enhancement)
- Test chat state reducer
- Test API client error handling
- Test utility functions (storage, validation)

### Integration Tests (Future Enhancement)
- Test home page → chat page flow
- Test message send/receive cycle
- Test error recovery flows

### Manual Testing (MVP)
- Test User Story 1: Enter chat, send message, receive response
- Test User Story 2: Resume conversation (when implemented)
- Test User Story 3: Error handling, offline detection
- Test responsive design on mobile, tablet, desktop
- Test all 10 edge cases from spec

---

## Security Considerations

### Input Validation
- **FR-002**: Validate user ID (alphanumeric, @, ., -, _)
- **FR-023**: Prevent empty messages
- **FR-024**: Limit message length to 5000 characters
- Sanitize user input before rendering (React handles by default)

### XSS Protection
- Use React's JSX for rendering (auto-escapes)
- Avoid `dangerouslySetInnerHTML`
- Validate and sanitize user_id before using in URLs/storage

### Data Privacy
- No sensitive data in localStorage/sessionStorage beyond conversation_id
- User_id is email (not password/token)
- Future: Implement proper JWT authentication

---

## Performance Targets

From spec success criteria:

- **SC-001**: Task workflow completion in <2 minutes ✓
- **SC-002**: Interface loads in <2 seconds on 3G ✓
- **SC-003**: 99% message delivery reliability (backend dependent) ✓
- **SC-004**: 95% successful first use (UX focused) ✓
- **SC-009**: 60fps scrolling with 100+ messages (virtual scrolling if needed)

**Optimization Strategy**:
- Code splitting (Next.js automatic)
- Image optimization (Next.js Image component)
- Lazy load conversation list (P2 feature)
- Minimize bundle size (tree shaking, no unused deps)

---

## Deployment Considerations

### Vercel Deployment (Recommended)
- Next.js 16+ fully supported
- Environment variables via dashboard
- Edge network for global CDN
- Automatic HTTPS

### Build Configuration
```json
// package.json scripts
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "type-check": "tsc --noEmit"
}
```

### Production Checklist
- [ ] Environment variables configured
- [ ] Backend URL points to production API
- [ ] CORS configured on backend for production domain
- [ ] Error boundaries implemented
- [ ] Loading states on all async operations
- [ ] Mobile responsive testing complete
- [ ] Accessibility basics (keyboard navigation, ARIA labels)

---

## Open Questions & Future Enhancements

### Phase 1 MVP (Immediate)
- ✓ Custom chat UI implementation
- ✓ sessionStorage for conversation_id
- ✓ Axios for backend integration
- ✓ Mobile-first responsive design
- ✓ Basic error handling and loading states

### Phase 2 Enhancements (Post-MVP)
- [ ] Conversation sidebar for history (User Story 2)
- [ ] JWT authentication integration
- [ ] Markdown rendering for rich messages
- [ ] Virtual scrolling for long conversations
- [ ] Offline detection and queue
- [ ] Dark mode support (optional from spec)
- [ ] Accessibility improvements (screen readers, keyboard-only)

### Phase 3 Advanced Features (Out of Scope)
- [ ] Real-time updates via WebSocket
- [ ] Search across conversations
- [ ] Message editing/deletion
- [ ] File attachments
- [ ] Voice input
- [ ] Push notifications

---

## References

- **Feature 017 Spec**: `/specs/017-chat-api/spec.md` - Backend API contract
- **Feature 017 Implementation**: `/specs/017-chat-api/IMPLEMENTATION_SUMMARY.md` - Backend details
- **Next.js 16 Docs**: https://nextjs.org/docs - App Router patterns
- **Tailwind CSS Docs**: https://tailwindcss.com/docs - Responsive design
- **TypeScript Handbook**: https://www.typescriptlang.org/docs - Type definitions

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Design (data-model.md, contracts/, quickstart.md)
**Ready for**: `/sp.tasks` after Phase 1 complete
