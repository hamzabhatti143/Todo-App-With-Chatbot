# Data Model: OpenAI ChatKit Frontend

**Feature**: 018-chatkit-frontend
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document defines the frontend data structures for the chat interface. These models represent the **client-side state** and are distinct from the backend database models (defined in Feature 017).

## Entity Relationships

```
User Session (browser)
    │
    ├── has one → Current Conversation
    │                 │
    │                 └── contains many → Messages
    │
    └── can access many → Conversation List
                              │
                              └── each has many → Messages
```

## Core Entities

### 1. Message

Represents a single message in a conversation (user or assistant).

**Source**: Backend API response + local user input

**Fields**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `id` | `string` | Yes | UUID format | Unique message identifier from backend |
| `role` | `"user" \| "assistant"` | Yes | Enum | Message sender role |
| `content` | `string` | Yes | 1-5000 chars | Message text content |
| `created_at` | `string` (ISO 8601) | Yes | Valid datetime | Message creation timestamp |
| `task_data` | `object \| null` | No | Valid JSON | Optional task metadata from agent (P2 feature) |

**Validation Rules** (from spec):
- **FR-023**: Content cannot be empty or whitespace-only
- **FR-024**: Content limited to 5000 characters
- **FR-004**: Role determines visual styling (user vs assistant)
- **FR-005**: Timestamp displayed for each message

**State Transitions**:
1. **Pending**: User types message → local state (not yet Message)
2. **Sending**: POST request initiated → optimistic Message with temporary ID
3. **Sent**: Backend confirms → replace temporary ID with real ID
4. **Failed**: Error response → mark as failed, show retry option

**TypeScript Definition**:
```typescript
interface Message {
  id: string;                    // UUID from backend
  role: "user" | "assistant";    // Message sender
  content: string;               // Message text (1-5000 chars)
  created_at: string;            // ISO 8601 timestamp
  task_data?: {                  // Optional task metadata
    action?: string;             // e.g., "add_task", "list_tasks"
    task_id?: string;            // Task UUID if applicable
    task_title?: string;         // Task title if applicable
  } | null;
}

// Extended for UI state
interface UIMessage extends Message {
  status?: "pending" | "sent" | "failed";  // Local UI status
  tempId?: string;                          // Temporary ID before backend confirm
}
```

---

### 2. Conversation

Represents a chat thread with its message history.

**Source**: Backend API response + local session state

**Fields**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `id` | `string` | Yes | UUID format | Unique conversation identifier from backend |
| `title` | `string` | No | Max 50 chars | Auto-generated from first user message |
| `messages` | `Message[]` | Yes | Array | List of messages in chronological order |
| `created_at` | `string` (ISO 8601) | Yes | Valid datetime | Conversation creation timestamp |
| `updated_at` | `string` (ISO 8601) | Yes | Valid datetime | Last message timestamp |
| `last_message` | `string` | No | Max 100 chars | Preview text for sidebar (P2 feature) |

**Validation Rules** (from spec):
- **FR-012**: Conversation ID obtained from first message response
- **FR-015**: Conversation ID persisted in sessionStorage
- **FR-020**: Title truncated to 50 characters from first user message
- **SC-009**: Support conversations with 100+ messages without performance degradation

**State Transitions**:
1. **New**: No conversation_id → first message creates conversation
2. **Active**: Has conversation_id → subsequent messages append to existing
3. **Resumed**: Loaded from sessionStorage or conversation list API
4. **Archived**: No longer active but retrievable from backend (P2 feature)

**TypeScript Definition**:
```typescript
interface Conversation {
  id: string;                    // UUID from backend
  title?: string;                // Auto-generated from first message (max 50 chars)
  messages: Message[];           // Chronological message list
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp (last message)
  last_message?: string;         // Preview for sidebar (max 100 chars, P2)
}

// Minimal for conversation list (P2 feature)
interface ConversationListItem {
  id: string;
  title: string;
  last_message: string;
  updated_at: string;
}
```

---

### 3. ChatState

Represents the current UI state of the chat interface (React Context state).

**Source**: Local React state (useReducer)

**Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `messages` | `UIMessage[]` | Yes | `[]` | Messages in current conversation |
| `loading` | `boolean` | Yes | `false` | Backend request in progress |
| `error` | `string \| null` | Yes | `null` | Error message to display |
| `conversationId` | `string \| null` | Yes | `null` | Current conversation ID |
| `userId` | `string` | Yes | (from URL) | Current user identifier |
| `inputValue` | `string` | Yes | `""` | Current input field value |
| `isOnline` | `boolean` | Yes | `true` | Network connectivity status |

**Validation Rules** (from spec):
- **FR-006**: Input disabled when `loading === true`
- **FR-007**: Show loading indicator when `loading === true`
- **FR-013**: Display `error` message when not null
- **FR-022**: Show retry option when error is network-related
- **FR-023**: Prevent send when `inputValue.trim() === ""`
- **FR-024**: Show character counter when `inputValue.length > 4500`

**State Transitions** (Reducer Actions):
```typescript
type ChatAction =
  | { type: "ADD_MESSAGE"; payload: UIMessage }
  | { type: "UPDATE_MESSAGE"; payload: { tempId: string; message: Message } }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null }
  | { type: "SET_CONVERSATION_ID"; payload: string }
  | { type: "SET_INPUT_VALUE"; payload: string }
  | { type: "SET_ONLINE"; payload: boolean }
  | { type: "CLEAR_CONVERSATION" }
  | { type: "LOAD_CONVERSATION"; payload: Conversation };
```

**TypeScript Definition**:
```typescript
interface ChatState {
  messages: UIMessage[];         // Current conversation messages
  loading: boolean;              // Backend request in progress
  error: string | null;          // Error message or null
  conversationId: string | null; // Current conversation ID
  userId: string;                // Current user ID from session
  inputValue: string;            // Input field value
  isOnline: boolean;             // Network connectivity status
}

// Reducer for state management
type ChatReducer = (state: ChatState, action: ChatAction) => ChatState;
```

---

### 4. UserSession

Represents the current user session in browser storage.

**Source**: URL query parameters + sessionStorage

**Fields**:

| Field | Type | Required | Storage | Description |
|-------|------|----------|---------|-------------|
| `userId` | `string` | Yes | sessionStorage | User identifier (email or ID) |
| `conversationId` | `string \| null` | No | sessionStorage | Active conversation ID |
| `isAuthenticated` | `boolean` | Yes | derived | Whether user has valid session |

**Validation Rules** (from spec):
- **FR-002**: User ID validated (alphanumeric, @, ., -, _ only)
- **FR-015**: Conversation ID persisted across page refreshes
- **Assumption #3**: Basic user_id authentication (no JWT in MVP)

**State Transitions**:
1. **Unauthenticated**: No userId in sessionStorage → redirect to home page
2. **Authenticated**: Valid userId → allow chat access
3. **Session End**: Browser close → sessionStorage cleared

**TypeScript Definition**:
```typescript
interface UserSession {
  userId: string;                // User identifier (validated)
  conversationId: string | null; // Active conversation or null
  isAuthenticated: boolean;      // Derived: !!userId
}

// Storage utilities
interface SessionStorage {
  saveUserId: (userId: string) => void;
  getUserId: () => string | null;
  saveConversationId: (userId: string, conversationId: string) => void;
  getConversationId: (userId: string) => string | null;
  clearSession: () => void;
}
```

---

## API Response Mapping

### POST /api/chat Response → Message

**Backend Response** (Feature 017):
```json
{
  "conversation_id": "uuid-string",
  "message_id": "uuid-string",
  "role": "assistant",
  "content": "I've added 'Buy groceries' to your tasks!",
  "created_at": "2026-01-22T12:00:00Z",
  "task_data": {
    "action": "add_task",
    "task_id": "task-uuid",
    "task_title": "Buy groceries"
  }
}
```

**Frontend Mapping**:
```typescript
const mapResponseToMessage = (response: ChatMessageResponse): Message => ({
  id: response.message_id,
  role: response.role,
  content: response.content,
  created_at: response.created_at,
  task_data: response.task_data || null,
});
```

### GET /api/conversations/{id} Response → Conversation

**Backend Response** (Feature 017, P2):
```json
{
  "id": "conversation-uuid",
  "messages": [
    {
      "message_id": "msg-1",
      "role": "user",
      "content": "Add buy groceries",
      "created_at": "2026-01-22T12:00:00Z",
      "task_data": null
    },
    {
      "message_id": "msg-2",
      "role": "assistant",
      "content": "Task added!",
      "created_at": "2026-01-22T12:00:05Z",
      "task_data": { "action": "add_task", "task_id": "uuid" }
    }
  ],
  "created_at": "2026-01-22T12:00:00Z"
}
```

**Frontend Mapping**:
```typescript
const mapResponseToConversation = (response: ConversationDetailResponse): Conversation => ({
  id: response.id,
  title: response.messages[0]?.content.slice(0, 50) || "New Conversation",
  messages: response.messages.map(msg => ({
    id: msg.message_id,
    role: msg.role,
    content: msg.content,
    created_at: msg.created_at,
    task_data: msg.task_data,
  })),
  created_at: response.created_at,
  updated_at: response.messages[response.messages.length - 1]?.created_at || response.created_at,
  last_message: response.messages[response.messages.length - 1]?.content.slice(0, 100) || "",
});
```

---

## Validation Rules Summary

### Input Validation (Frontend)

**User ID** (FR-002):
```typescript
const USER_ID_REGEX = /^[a-zA-Z0-9@._-]+$/;
const validateUserId = (userId: string): boolean => {
  if (!userId || userId.trim().length === 0) return false;
  if (!USER_ID_REGEX.test(userId)) return false;
  return true;
};
```

**Message Content** (FR-023, FR-024):
```typescript
const validateMessageContent = (content: string): { valid: boolean; error?: string } => {
  const trimmed = content.trim();
  if (trimmed.length === 0) {
    return { valid: false, error: "Message cannot be empty" };
  }
  if (trimmed.length > 5000) {
    return { valid: false, error: "Message too long (max 5000 characters)" };
  }
  return { valid: true };
};
```

**Conversation ID** (FR-012):
```typescript
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const validateConversationId = (id: string | null): boolean => {
  if (id === null) return true; // null is valid (new conversation)
  return UUID_REGEX.test(id);
};
```

---

## State Management Architecture

### Context Provider Structure

```typescript
// ChatContext.tsx
interface ChatContextValue {
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  sendMessage: (content: string) => Promise<void>;
  loadConversation: (conversationId: string) => Promise<void>;
  startNewConversation: () => void;
  retryLastMessage: () => Promise<void>;
}

const ChatContext = React.createContext<ChatContextValue | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const sendMessage = async (content: string) => {
    // 1. Validate content
    // 2. Add optimistic user message
    // 3. Set loading = true
    // 4. POST /api/chat
    // 5. Add assistant message
    // 6. Update conversation_id if first message
    // 7. Save conversation_id to sessionStorage
    // 8. Set loading = false
    // 9. Handle errors
  };

  const loadConversation = async (conversationId: string) => {
    // 1. Set loading = true
    // 2. GET /api/conversations/{id}
    // 3. Map response to messages
    // 4. dispatch LOAD_CONVERSATION
    // 5. Set loading = false
  };

  const startNewConversation = () => {
    // 1. dispatch CLEAR_CONVERSATION
    // 2. Clear conversationId from sessionStorage
  };

  const retryLastMessage = async () => {
    // 1. Find last failed message
    // 2. Re-send with sendMessage
  };

  return (
    <ChatContext.Provider value={{ state, dispatch, sendMessage, loadConversation, startNewConversation, retryLastMessage }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error("useChatContext must be used within ChatProvider");
  return context;
};
```

---

## Performance Considerations

### Message List Rendering

**For <100 messages** (MVP):
- Simple array mapping with `key={message.id}`
- Auto-scroll to bottom on new message (FR-019)
- Maintain scroll position when loading history (FR-026)

**For 100+ messages** (Future Enhancement):
- Virtual scrolling with `react-window` or `react-virtualized`
- Windowing to render only visible messages
- Lazy loading of conversation history

### State Update Optimization

**Reducer Design**:
- Immutable updates with spread operators
- Avoid re-rendering entire message list on input change
- Memoize expensive computations (e.g., message grouping by date)

**Context Optimization**:
- Split ChatContext into ChatStateContext + ChatActionsContext
- Prevent re-renders when only actions are needed

---

## Error Handling

### Error Types

```typescript
interface ChatError {
  type: "network" | "validation" | "server" | "unauthorized" | "timeout";
  message: string;
  retryable: boolean;
  statusCode?: number;
}

const ERROR_MESSAGES: Record<ChatError["type"], string> = {
  network: "You're offline. Please check your connection.",
  validation: "Message validation failed. Please try again.",
  server: "Unable to reach AI assistant. Please try again.",
  unauthorized: "Your session has expired. Please log in again.",
  timeout: "Request timed out. Please try again.",
};
```

### Error Recovery

**Retryable Errors** (FR-022):
- Network errors (offline, timeout)
- Server errors (500, 503)
- Action: Show retry button, preserve user input

**Non-Retryable Errors**:
- Validation errors (400)
- Unauthorized (401)
- Action: Show error message, clear error on new input

---

## Storage Schema (sessionStorage)

**Keys**:
```typescript
const STORAGE_KEYS = {
  USER_ID: "chat_user_id",
  CONVERSATION_ID: (userId: string) => `chat_conversation_${userId}`,
  DRAFT_MESSAGE: (userId: string) => `chat_draft_${userId}`, // Future: persist unsent message
};
```

**Example sessionStorage**:
```
chat_user_id: "john@example.com"
chat_conversation_john@example.com: "550e8400-e29b-41d4-a716-446655440000"
```

---

## Data Flow Diagrams

### Send Message Flow

```
User types message
  ↓
Validate content (1-5000 chars, not empty)
  ↓
dispatch ADD_MESSAGE (optimistic, tempId)
  ↓
dispatch SET_LOADING(true)
  ↓
POST /api/chat { content, conversation_id }
  ↓
[Backend processes, returns response]
  ↓
dispatch UPDATE_MESSAGE (replace tempId with real id)
  ↓
dispatch ADD_MESSAGE (assistant response)
  ↓
dispatch SET_CONVERSATION_ID (if first message)
  ↓
Save conversation_id to sessionStorage
  ↓
dispatch SET_LOADING(false)
  ↓
Auto-scroll to bottom (FR-019)
```

### Load Conversation Flow

```
User clicks conversation in sidebar (P2)
  ↓
dispatch SET_LOADING(true)
  ↓
GET /api/conversations/{id}
  ↓
Map response to Conversation
  ↓
dispatch LOAD_CONVERSATION
  ↓
Update sessionStorage with conversation_id
  ↓
dispatch SET_LOADING(false)
  ↓
Maintain scroll position (FR-026)
```

---

**Data Model Status**: ✅ Complete
**Next Phase**: Create `contracts/` directory with API specifications
**Ready for**: `quickstart.md` after contracts complete
