# API Client Contract

**Feature**: 018-chatkit-frontend
**Date**: 2026-01-22
**Backend**: Feature 017 (Stateless Chat API)

## Overview

This document defines the contract between the Next.js frontend and the FastAPI backend for chat operations.

## Base Configuration

### Environment Variables

```env
# .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Axios Instance

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

// Request interceptor: Add user context (MVP: no JWT yet)
apiClient.interceptors.request.use((config) => {
  // In future: Add JWT token from localStorage
  // config.headers.Authorization = `Bearer ${getToken()}`;
  return config;
});

// Response interceptor: Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      return Promise.reject({
        type: 'server',
        statusCode: error.response.status,
        message: error.response.data?.detail || 'Server error',
      });
    } else if (error.request) {
      // Request made but no response (network error)
      return Promise.reject({
        type: 'network',
        message: 'Network error. Please check your connection.',
      });
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      return Promise.reject({
        type: 'timeout',
        message: 'Request timed out. Please try again.',
      });
    } else {
      // Unknown error
      return Promise.reject({
        type: 'unknown',
        message: error.message || 'An unexpected error occurred',
      });
    }
  }
);

export default apiClient;
```

---

## Endpoint: POST /api/chat

**Purpose**: Send a chat message and receive AI assistant response

**Requirements**: FR-009, FR-010, FR-011, FR-012, FR-013, FR-014

### Request

**Method**: `POST`

**URL**: `/api/chat`

**Headers**:
```
Content-Type: application/json
```

**Body**:
```typescript
interface ChatRequest {
  content: string;           // Required: Message content (1-5000 chars)
  conversation_id?: string;  // Optional: UUID of existing conversation
}
```

**Example**:
```json
{
  "content": "Add buy groceries to my tasks",
  "conversation_id": null
}
```

**Validation** (Frontend):
- `content` must not be empty or whitespace-only (FR-023)
- `content` must be ≤5000 characters (FR-024)
- `conversation_id` must be valid UUID if provided (FR-012)

### Response (Success)

**Status**: `200 OK`

**Body**:
```typescript
interface ChatResponse {
  conversation_id: string;   // UUID of conversation (new or existing)
  message_id: string;        // UUID of assistant's message
  role: "assistant";         // Always "assistant" for response
  content: string;           // Assistant's text response
  created_at: string;        // ISO 8601 timestamp
  task_data?: {              // Optional: Task metadata if tool was called
    action?: string;         // e.g., "add_task", "list_tasks", "complete_task"
    task_id?: string;        // Task UUID if applicable
    task_title?: string;     // Task title if applicable
  } | null;
}
```

**Example**:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "660e8400-e29b-41d4-a716-446655440001",
  "role": "assistant",
  "content": "I've added 'Buy groceries' to your tasks!",
  "created_at": "2026-01-22T12:00:05.123456Z",
  "task_data": {
    "action": "add_task",
    "task_id": "770e8400-e29b-41d4-a716-446655440002",
    "task_title": "Buy groceries"
  }
}
```

### Response (Error)

**400 Bad Request**:
```json
{
  "detail": "Message content cannot be empty"
}
```

**401 Unauthorized** (Future: JWT authentication):
```json
{
  "detail": "Invalid or missing authentication token"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "An unexpected error occurred. Please try again."
}
```

**503 Service Unavailable**:
```json
{
  "detail": "Database is unavailable. Please try again later."
}
```

### Frontend Implementation

```typescript
// lib/chat-api.ts
import apiClient from './api';
import type { ChatRequest, ChatResponse } from '@/types/chat';

export const sendChatMessage = async (
  content: string,
  conversationId: string | null
): Promise<ChatResponse> => {
  const request: ChatRequest = {
    content,
    ...(conversationId && { conversation_id: conversationId }),
  };

  const response = await apiClient.post<ChatResponse>('/api/chat', request);
  return response.data;
};
```

**Usage Example**:
```typescript
try {
  const response = await sendChatMessage("Add buy groceries", null);
  console.log(response.conversation_id); // Save to sessionStorage
  console.log(response.content);         // Display assistant message
} catch (error) {
  if (error.type === 'network') {
    // Show "You're offline" message
  } else if (error.type === 'timeout') {
    // Show "Request timed out" with retry option
  } else {
    // Show generic error message
  }
}
```

---

## Endpoint: GET /api/conversations (P2 Feature)

**Purpose**: Retrieve list of user's conversations for sidebar

**Requirements**: FR-016, FR-017 (User Story 2)

### Request

**Method**: `GET`

**URL**: `/api/conversations`

**Headers**:
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>  // Future: JWT authentication
```

**Query Parameters**: None (authenticated user determined from JWT)

### Response (Success)

**Status**: `200 OK`

**Body**:
```typescript
interface ConversationListResponse {
  conversations: ConversationListItem[];
}

interface ConversationListItem {
  id: string;            // Conversation UUID
  title: string;         // Auto-generated from first message (max 50 chars)
  last_message: string;  // Preview of last message (max 100 chars)
  updated_at: string;    // ISO 8601 timestamp of last message
}
```

**Example**:
```json
{
  "conversations": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Add buy groceries to my tasks",
      "last_message": "I've added 'Buy groceries' to your tasks!",
      "updated_at": "2026-01-22T12:00:05.123456Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "title": "What tasks do I have?",
      "last_message": "You have 3 active tasks: Buy groceries, Finish...",
      "updated_at": "2026-01-21T15:30:00.000000Z"
    }
  ]
}
```

**Sorting**: Conversations ordered by `updated_at` descending (most recent first)

### Response (Error)

**401 Unauthorized**:
```json
{
  "detail": "Invalid or missing authentication token"
}
```

### Frontend Implementation

```typescript
// lib/chat-api.ts
export const getConversations = async (): Promise<ConversationListItem[]> => {
  const response = await apiClient.get<ConversationListResponse>('/api/conversations');
  return response.data.conversations;
};
```

**Usage Example**:
```typescript
// In conversation sidebar component
const [conversations, setConversations] = useState<ConversationListItem[]>([]);

useEffect(() => {
  const loadConversations = async () => {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error("Failed to load conversations", error);
    }
  };
  loadConversations();
}, []);
```

---

## Endpoint: GET /api/conversations/{id} (P2 Feature)

**Purpose**: Retrieve full conversation history for resuming

**Requirements**: FR-017, FR-018 (User Story 2)

### Request

**Method**: `GET`

**URL**: `/api/conversations/{id}`

**Path Parameters**:
- `id` (string, required): Conversation UUID

**Headers**:
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>  // Future: JWT authentication
```

### Response (Success)

**Status**: `200 OK`

**Body**:
```typescript
interface ConversationDetailResponse {
  id: string;                // Conversation UUID
  messages: MessageDetail[]; // Full message history
  created_at: string;        // ISO 8601 timestamp of first message
}

interface MessageDetail {
  message_id: string;        // Message UUID
  role: "user" | "assistant"; // Message sender
  content: string;           // Message text
  created_at: string;        // ISO 8601 timestamp
  task_data?: {              // Optional: Task metadata
    action?: string;
    task_id?: string;
    task_title?: string;
  } | null;
}
```

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "message_id": "msg-1-uuid",
      "role": "user",
      "content": "Add buy groceries to my tasks",
      "created_at": "2026-01-22T12:00:00.000000Z",
      "task_data": null
    },
    {
      "message_id": "msg-2-uuid",
      "role": "assistant",
      "content": "I've added 'Buy groceries' to your tasks!",
      "created_at": "2026-01-22T12:00:05.123456Z",
      "task_data": {
        "action": "add_task",
        "task_id": "task-uuid",
        "task_title": "Buy groceries"
      }
    },
    {
      "message_id": "msg-3-uuid",
      "role": "user",
      "content": "Show my tasks",
      "created_at": "2026-01-22T12:01:00.000000Z",
      "task_data": null
    },
    {
      "message_id": "msg-4-uuid",
      "role": "assistant",
      "content": "You have 3 tasks:\n1. Buy groceries (incomplete)\n2. Finish report (incomplete)\n3. Call client (incomplete)",
      "created_at": "2026-01-22T12:01:03.456789Z",
      "task_data": {
        "action": "list_tasks"
      }
    }
  ],
  "created_at": "2026-01-22T12:00:00.000000Z"
}
```

**Message Ordering**: Messages ordered chronologically (oldest first)

**Message Limit**: Backend returns last 20 messages (Feature 017 context limit)

### Response (Error)

**401 Unauthorized**:
```json
{
  "detail": "Invalid or missing authentication token"
}
```

**404 Not Found**:
```json
{
  "detail": "Conversation not found"
}
```

**403 Forbidden**:
```json
{
  "detail": "You do not have permission to access this conversation"
}
```

### Frontend Implementation

```typescript
// lib/chat-api.ts
export const getConversationDetail = async (
  conversationId: string
): Promise<ConversationDetailResponse> => {
  const response = await apiClient.get<ConversationDetailResponse>(
    `/api/conversations/${conversationId}`
  );
  return response.data;
};
```

**Usage Example**:
```typescript
// In chat context or page
const loadConversation = async (conversationId: string) => {
  dispatch({ type: "SET_LOADING", payload: true });
  try {
    const conversation = await getConversationDetail(conversationId);

    // Map backend messages to frontend Message type
    const messages: UIMessage[] = conversation.messages.map(msg => ({
      id: msg.message_id,
      role: msg.role,
      content: msg.content,
      created_at: msg.created_at,
      task_data: msg.task_data,
      status: "sent",
    }));

    dispatch({
      type: "LOAD_CONVERSATION",
      payload: {
        id: conversation.id,
        messages,
        created_at: conversation.created_at,
        updated_at: conversation.messages[conversation.messages.length - 1]?.created_at,
      }
    });

    // Save to sessionStorage
    sessionStorage.setItem(`chat_conversation_${userId}`, conversationId);
  } catch (error) {
    dispatch({
      type: "SET_ERROR",
      payload: "Failed to load conversation"
    });
  } finally {
    dispatch({ type: "SET_LOADING", payload: false });
  }
};
```

---

## Error Handling Strategy

### Error Types and User Messages

```typescript
// lib/error-handler.ts
export const getErrorMessage = (error: ApiError): string => {
  if (error.type === 'network') {
    return "You're offline. Please check your connection."; // FR-013
  }

  if (error.type === 'timeout') {
    return "Request timed out. Please try again."; // FR-014
  }

  if (error.statusCode === 400) {
    return error.message; // Validation error from backend
  }

  if (error.statusCode === 401) {
    return "Your session has expired. Please log in again.";
  }

  if (error.statusCode === 403) {
    return "You do not have permission to access this resource.";
  }

  if (error.statusCode === 404) {
    return "Conversation not found.";
  }

  if (error.statusCode === 500) {
    return "Unable to reach AI assistant. Please try again."; // FR-013
  }

  if (error.statusCode === 503) {
    return "Service temporarily unavailable. Please try again later."; // FR-013
  }

  return "An unexpected error occurred. Please try again.";
};

export const isRetryable = (error: ApiError): boolean => {
  return (
    error.type === 'network' ||
    error.type === 'timeout' ||
    error.statusCode === 500 ||
    error.statusCode === 503
  ); // FR-022
};
```

### Retry Logic

```typescript
// lib/retry.ts
export const retryWithExponentialBackoff = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  initialDelay: number = 1000
): Promise<T> => {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (i < maxRetries - 1 && isRetryable(error)) {
        const delay = initialDelay * Math.pow(2, i);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }

  throw lastError!;
};
```

---

## Testing Strategy

### API Client Tests

```typescript
// __tests__/lib/api.test.ts
import { describe, it, expect, vi } from 'vitest';
import apiClient from '@/lib/api';
import { sendChatMessage } from '@/lib/chat-api';

describe('API Client', () => {
  it('should add base URL to requests', () => {
    expect(apiClient.defaults.baseURL).toBe(process.env.NEXT_PUBLIC_BACKEND_URL);
  });

  it('should have 30 second timeout', () => {
    expect(apiClient.defaults.timeout).toBe(30000);
  });

  it('should handle network errors', async () => {
    vi.spyOn(apiClient, 'post').mockRejectedValueOnce({
      request: {},
      message: 'Network Error',
    });

    await expect(sendChatMessage("Test", null)).rejects.toMatchObject({
      type: 'network',
    });
  });

  it('should handle timeout errors', async () => {
    vi.spyOn(apiClient, 'post').mockRejectedValueOnce({
      code: 'ECONNABORTED',
      message: 'timeout exceeded',
    });

    await expect(sendChatMessage("Test", null)).rejects.toMatchObject({
      type: 'timeout',
    });
  });

  it('should handle server errors', async () => {
    vi.spyOn(apiClient, 'post').mockRejectedValueOnce({
      response: {
        status: 500,
        data: { detail: 'Internal server error' },
      },
    });

    await expect(sendChatMessage("Test", null)).rejects.toMatchObject({
      type: 'server',
      statusCode: 500,
    });
  });
});
```

---

## API Version Contract

**Current Version**: v1 (implicit in URLs)

**Breaking Change Policy**:
- Major version changes (v1 → v2): URL path change (e.g., `/api/v2/chat`)
- Minor version changes: Backward-compatible additions
- Patch version changes: Bug fixes only

**Frontend Handling**:
- Use versioned API client if backend adds `/api/v2/*` endpoints
- Maintain backward compatibility during transition period

---

**Contract Status**: ✅ Complete
**Backend Compatibility**: Feature 017 (Stateless Chat API Backend)
**Next**: Create `quickstart.md` with setup instructions
