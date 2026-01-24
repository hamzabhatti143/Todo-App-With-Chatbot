/**
 * Type definitions for chat functionality
 * Feature: 018-chatkit-frontend
 */

// Core message type (matches backend response)
export interface Message {
  id: string;
  conversation_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
  task_data?: {
    action?: string;
    task_id?: string;
    task_title?: string;
  } | null;
}

// Extended message type for UI state management
export interface UIMessage extends Message {
  status?: "pending" | "sent" | "failed";
  tempId?: string;
}

// Conversation type
export interface Conversation {
  id: string;
  title?: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
  last_message?: string;
}

// Conversation list item (for sidebar)
export interface ConversationListItem {
  id: string;
  title: string;
  last_message: string;
  updated_at: string;
  message_count: number;
}

// Chat state for context
export interface ChatState {
  messages: UIMessage[];
  loading: boolean;
  error: string | null;
  conversationId: string | null;
  userId: string;
  inputValue: string;
  isOnline: boolean;
}

// Chat reducer actions
export type ChatAction =
  | { type: "ADD_MESSAGE"; payload: UIMessage }
  | { type: "UPDATE_MESSAGE"; payload: { tempId: string; message: Message } }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null }
  | { type: "SET_CONVERSATION_ID"; payload: string }
  | { type: "SET_INPUT_VALUE"; payload: string }
  | { type: "SET_ONLINE"; payload: boolean }
  | { type: "CLEAR_CONVERSATION" }
  | { type: "LOAD_CONVERSATION"; payload: Conversation };

// API Request/Response types
export interface ChatRequest {
  content: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  role: "assistant";
  content: string;
  created_at: string;
  task_data?: {
    action?: string;
    task_id?: string;
    task_title?: string;
  } | null;
}

export type ConversationListResponse = ConversationListItem[];

export interface ConversationDetailResponse {
  id: string;
  messages: {
    message_id: string;
    role: "user" | "assistant";
    content: string;
    created_at: string;
    task_data?: {
      action?: string;
      task_id?: string;
      task_title?: string;
    } | null;
  }[];
  created_at: string;
}

// Error type
export interface ApiError {
  type: "network" | "validation" | "server" | "unauthorized" | "timeout" | "unknown";
  message: string;
  statusCode?: number;
}

// User session type
export interface UserSession {
  userId: string;
  conversationId: string | null;
  isAuthenticated: boolean;
}

// Type aliases for backward compatibility
export type ChatMessage = Message;
export type ChatMessageRequest = ChatRequest;
export type ChatMessageResponse = ChatResponse;
export type ConversationWithMessages = Conversation;
