# Chat Interface - Feature 018

**AI-Powered Conversational Task Management**

## Overview

The chat interface provides a beautiful, responsive UI for interacting with TodoBot, an AI assistant powered by Google Gemini 2.0 Flash. Users can manage their tasks through natural language conversations.

## Features

### ✅ Phase 1-3: Core Chat (MVP)
- **Real-time Messaging**: Send messages and receive AI responses
- **Conversation Persistence**: Messages saved across sessions
- **Loading States**: Visual feedback during API requests
- **Error Handling**: User-friendly error messages with retry options
- **Responsive Design**: Mobile-first (320px+), tablet (768px+), desktop (1024px+)
- **Welcome Message**: Contextual greeting for new users
- **Character Limit**: 5000 character max with counter
- **Keyboard Support**: Enter to send, Shift+Enter for line breaks

### ✅ Phase 4: Conversation History
- **Conversation List**: Sidebar showing previous conversations
- **Resume Conversations**: Load full message history
- **New Conversation**: Start fresh chats
- **Mobile Toggle**: Hamburger menu for conversation list
- **Active Indicator**: Highlight current conversation

### ✅ Phase 5: Enhanced Error Handling
- **Error Types**: Network, timeout, server, validation, unauthorized
- **Retry Logic**: Smart retry for transient errors
- **Offline Detection**: Navigator.onLine support
- **Error Recovery**: Clear error messages and recovery actions

### ✅ Phase 6: Polish & Optimization
- **Performance**: React.memo on Message component
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation
- **Keyboard Shortcuts**: Ctrl+K for new conversation, Escape to clear
- **Smooth Animations**: Slide-up for messages, fade-in for errors

## File Structure

```
frontend/
├── app/chat/
│   └── page.tsx                    # Main chat page with sidebar
├── components/chat/
│   ├── ChatInterface.tsx           # Main chat component
│   ├── MessageList.tsx             # Message display area
│   ├── MessageInput.tsx            # Input field with validation
│   ├── Message.tsx                 # Individual message (memoized)
│   ├── ConversationSidebar.tsx     # Conversation history
│   ├── LoadingSpinner.tsx          # Loading indicator
│   └── ErrorMessage.tsx            # Error display with retry
├── contexts/
│   └── ChatContext.tsx             # State management (useReducer)
├── hooks/
│   └── use-keyboard-shortcuts.ts   # Keyboard event handling
├── lib/
│   ├── chat-api.ts                 # API client for chat endpoints
│   ├── storage.ts                  # SessionStorage utilities
│   └── error-handler.ts            # Error message mapping
└── types/
    └── chat.ts                     # TypeScript definitions
```

## Usage

### Accessing the Chat

1. **Sign In**: Navigate to `/signin` and authenticate
2. **Go to Chat**: Click "Chat" or navigate to `/chat`
3. **Start Chatting**: Type a message and press Enter

### Example Conversations

```
You: Add buy groceries
Bot: ✅ I've added 'Buy groceries' to your tasks!

You: Show my tasks
Bot: Here are your tasks:
     1. Buy groceries (incomplete)
     2. Finish report (incomplete)

You: Mark task 1 as done
Bot: 🎉 Awesome! Marked 'Buy groceries' as complete.
```

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Ctrl/Cmd + K**: Start new conversation
- **Escape**: Clear error messages (future: close modals)

## API Integration

### Backend Endpoints

**POST /api/chat**
- Send a chat message
- Receives AI response
- Returns conversation_id for persistence

**GET /api/conversations**
- List all user conversations
- Sorted by updated_at (most recent first)

**GET /api/conversations/{id}**
- Get full conversation history
- Returns all messages in chronological order

### Environment Variables

```env
# .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## State Management

### ChatContext

Global state using React's `useReducer`:

```typescript
interface ChatState {
  messages: UIMessage[];
  loading: boolean;
  error: string | null;
  conversationId: string | null;
  userId: string;
  inputValue: string;
  isOnline: boolean;
}
```

### Actions

- `ADD_MESSAGE`: Add user/assistant message
- `UPDATE_MESSAGE`: Update message status (pending → sent)
- `SET_LOADING`: Toggle loading state
- `SET_ERROR`: Display error message
- `SET_CONVERSATION_ID`: Save conversation ID
- `LOAD_CONVERSATION`: Load full conversation history
- `CLEAR_CONVERSATION`: Start new conversation

## Error Handling

### Error Types

- **Network**: Offline, connection failed
- **Timeout**: Request exceeded 30 seconds
- **Server**: 500, 503 errors
- **Validation**: 400 errors (invalid input)
- **Unauthorized**: 401 errors (session expired)

### Recovery Options

- **Retryable Errors**: Network, timeout, 500, 503
  - Show "Try Again" button
  - Re-send last failed message

- **Non-Retryable Errors**: Validation, 401
  - Show clear error message
  - User must fix input or re-authenticate

## Performance Optimization

### React.memo

Message component is memoized with custom comparison:
```typescript
memo(Message, (prev, next) => {
  return prev.message.id === next.message.id &&
         prev.message.status === next.message.status
});
```

### Auto-Scroll

Messages auto-scroll to bottom on new messages using `useRef` and `scrollIntoView`.

### Lazy Loading (Future)

Virtual scrolling for 100+ messages with react-window.

## Accessibility

- **ARIA Labels**: All interactive elements labeled
- **Semantic HTML**: `<article>` for messages, `<nav>` for sidebar
- **Keyboard Navigation**: Tab through elements, Enter to activate
- **Screen Reader Support**: Role and aria-label attributes

## Responsive Design

### Breakpoints

- **Mobile**: 320px - 767px (sidebar hidden by default)
- **Tablet**: 768px - 1023px (sidebar visible, 320px wide)
- **Desktop**: 1024px+ (sidebar visible, 320px wide)

### Mobile Behavior

- Sidebar toggles with hamburger menu
- "Back" button text shortened on small screens
- Message bubbles max 70% width for readability

## Testing

### Manual Test Checklist

- [ ] Sign in and navigate to `/chat`
- [ ] Send message "Add buy groceries"
- [ ] Verify AI responds with task confirmation
- [ ] Send follow-up message "Show my tasks"
- [ ] Verify conversation continues (same conversation_id)
- [ ] Refresh page and verify messages persist
- [ ] Click "New Conversation" button
- [ ] Verify new conversation starts (no previous messages)
- [ ] Test on mobile (320px width)
- [ ] Test conversation sidebar toggle (mobile)
- [ ] Test error handling (disconnect network, send message)
- [ ] Verify retry button appears for network errors
- [ ] Test character counter (type 4500+ chars)
- [ ] Test Shift+Enter for line breaks

### Edge Cases

- ✅ Empty message (validation prevents send)
- ✅ Message > 5000 chars (shows error, prevents send)
- ✅ Rapid message sending (loading state prevents duplicates)
- ✅ Backend unavailable (shows error with retry)
- ✅ Session expired (redirects to signin)
- ✅ Page refresh mid-conversation (persists via sessionStorage)

## Troubleshooting

### "Network error" on every message

**Cause**: Backend not running or wrong URL
**Fix**:
1. Start backend: `cd backend && python run.py`
2. Verify `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` in `.env.local`

### Conversation not persisting

**Cause**: SessionStorage cleared or different userId
**Fix**: Check browser console for `conversation_id` in sessionStorage

### Sidebar not showing on desktop

**Cause**: Tailwind breakpoint issue
**Fix**: Verify screen width >= 768px, check `md:block` class applied

### Messages not auto-scrolling

**Cause**: messagesEndRef not triggering
**Fix**: Check `useEffect` dependency array includes `messages`

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Voice input integration
- [ ] Message search functionality
- [ ] Export conversation to PDF/Markdown
- [ ] Conversation folders/tags
- [ ] AI conversation summarization
- [ ] Multi-language support
- [ ] Dark mode toggle in chat header
- [ ] File upload support (images, documents)
- [ ] Code syntax highlighting in messages

## Dependencies

- **Next.js**: 16.1.1 (App Router)
- **React**: 19.2.3
- **TypeScript**: 5.7.2 (strict mode)
- **Tailwind CSS**: 4.1.18
- **Axios**: 1.7.9
- **Lucide React**: 0.460.0 (icons)
- **Framer Motion**: 11.18.2 (animations - optional)

## Related Documentation

- [Backend API Docs](http://localhost:8000/docs)
- [Feature Spec](../../specs/018-chatkit-frontend/spec.md)
- [Implementation Plan](../../specs/018-chatkit-frontend/plan.md)
- [Tasks Breakdown](../../specs/018-chatkit-frontend/tasks.md)

## Support

For issues or questions:
1. Check browser console for errors
2. Verify backend is running (`http://localhost:8000/health`)
3. Review [quickstart.md](../../specs/018-chatkit-frontend/quickstart.md)
4. Check [GitHub Issues](https://github.com/anthropics/claude-code/issues)
