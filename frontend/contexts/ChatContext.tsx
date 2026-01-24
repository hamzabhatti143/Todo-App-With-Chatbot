"use client";

/**
 * Chat Context for State Management
 * Feature: 018-chatkit-frontend
 */

import React, { createContext, useContext, useReducer, useCallback, ReactNode } from "react";
import type { ChatState, ChatAction, UIMessage, Conversation, Message } from "@/types/chat";
import { sendChatMessage, getConversationDetail } from "@/lib/chat-api";
import { saveConversationId, clearSession } from "@/lib/storage";
import { getErrorMessage } from "@/lib/error-handler";
import type { ApiError } from "@/types/chat";

// Initial state
const initialState: ChatState = {
  messages: [],
  loading: false,
  error: null,
  conversationId: null,
  userId: "",
  inputValue: "",
  isOnline: typeof navigator !== "undefined" ? navigator.onLine : true,
};

// Reducer function
function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };

    case "UPDATE_MESSAGE":
      return {
        ...state,
        messages: state.messages.map((msg) =>
          msg.tempId === action.payload.tempId
            ? { ...action.payload.message, status: "sent" as const }
            : msg
        ),
      };

    case "SET_LOADING":
      return {
        ...state,
        loading: action.payload,
      };

    case "SET_ERROR":
      return {
        ...state,
        error: action.payload,
      };

    case "SET_CONVERSATION_ID":
      return {
        ...state,
        conversationId: action.payload,
      };

    case "SET_INPUT_VALUE":
      return {
        ...state,
        inputValue: action.payload,
      };

    case "SET_ONLINE":
      return {
        ...state,
        isOnline: action.payload,
      };

    case "CLEAR_CONVERSATION":
      return {
        ...state,
        messages: [],
        conversationId: null,
        error: null,
      };

    case "LOAD_CONVERSATION":
      return {
        ...state,
        conversationId: action.payload.id,
        messages: action.payload.messages.map((msg) => ({ ...msg, status: "sent" as const })),
      };

    default:
      return state;
  }
}

// Context value interface
interface ChatContextValue {
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
  sendMessage: (content: string) => Promise<void>;
  loadConversation: (conversationId: string) => Promise<void>;
  startNewConversation: () => void;
  retryLastMessage: () => Promise<void>;
}

// Create context
const ChatContext = createContext<ChatContextValue | undefined>(undefined);

// Provider props
interface ChatProviderProps {
  children: ReactNode;
  userId: string;
}

// Provider component
export function ChatProvider({ children, userId }: ChatProviderProps) {
  const [state, dispatch] = useReducer(chatReducer, {
    ...initialState,
    userId,
  });

  // Send message function
  const sendMessage = useCallback(
    async (content: string) => {
      // Validate content
      const trimmed = content.trim();
      if (!trimmed) {
        dispatch({ type: "SET_ERROR", payload: "Message cannot be empty" });
        return;
      }

      if (trimmed.length > 5000) {
        dispatch({ type: "SET_ERROR", payload: "Message too long (max 5000 characters)" });
        return;
      }

      // Clear previous error
      dispatch({ type: "SET_ERROR", payload: null });

      // Add optimistic user message
      const tempId = `temp-${Date.now()}`;
      const userMessage: UIMessage = {
        id: tempId,
        conversation_id: state.conversationId || "",
        tempId,
        role: "user",
        content: trimmed,
        created_at: new Date().toISOString(),
        status: "pending",
      };
      dispatch({ type: "ADD_MESSAGE", payload: userMessage });

      // Set loading state
      dispatch({ type: "SET_LOADING", payload: true });

      try {
        // Send to backend
        const response = await sendChatMessage(trimmed, state.conversationId);

        // Update user message with real ID
        const confirmedUserMessage: Message = {
          id: tempId, // Keep temp ID since backend doesn't return user message ID
          conversation_id: response.conversation_id,
          role: "user",
          content: trimmed,
          created_at: userMessage.created_at,
        };
        dispatch({ type: "UPDATE_MESSAGE", payload: { tempId, message: confirmedUserMessage } });

        // Add assistant message
        const assistantMessage: UIMessage = {
          id: response.message_id,
          conversation_id: response.conversation_id,
          role: response.role,
          content: response.content,
          created_at: response.created_at,
          task_data: response.task_data,
          status: "sent",
        };
        dispatch({ type: "ADD_MESSAGE", payload: assistantMessage });

        // Save conversation ID if first message
        if (!state.conversationId) {
          dispatch({ type: "SET_CONVERSATION_ID", payload: response.conversation_id });
          saveConversationId(userId, response.conversation_id);
        }
      } catch (err) {
        const error = err as ApiError;
        const errorMessage = getErrorMessage(error);
        dispatch({ type: "SET_ERROR", payload: errorMessage });

        // Mark user message as failed
        const failedMessage = { ...userMessage, status: "failed" as const };
        dispatch({
          type: "UPDATE_MESSAGE",
          payload: { tempId, message: failedMessage },
        });
      } finally {
        dispatch({ type: "SET_LOADING", payload: false });
      }
    },
    [state.conversationId, userId]
  );

  // Load conversation function
  const loadConversation = useCallback(async (conversationId: string) => {
    dispatch({ type: "SET_LOADING", payload: true });
    dispatch({ type: "SET_ERROR", payload: null });

    try {
      const conversation = await getConversationDetail(conversationId);

      // Map backend messages to frontend format
      const messages: Message[] = conversation.messages.map((msg) => ({
        id: msg.message_id,
        conversation_id: conversationId,
        role: msg.role,
        content: msg.content,
        created_at: msg.created_at,
        task_data: msg.task_data,
      }));

      const conversationData: Conversation = {
        id: conversation.id,
        messages,
        created_at: conversation.created_at,
        updated_at: messages[messages.length - 1]?.created_at || conversation.created_at,
      };

      dispatch({ type: "LOAD_CONVERSATION", payload: conversationData });
    } catch (err) {
      const error = err as ApiError;
      const errorMessage = getErrorMessage(error);
      dispatch({ type: "SET_ERROR", payload: errorMessage });
    } finally {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  }, []);

  // Start new conversation
  const startNewConversation = useCallback(() => {
    dispatch({ type: "CLEAR_CONVERSATION" });
    clearSession();
  }, []);

  // Retry last failed message
  const retryLastMessage = useCallback(async () => {
    const lastMessage = state.messages[state.messages.length - 1];
    if (lastMessage && lastMessage.role === "user" && lastMessage.status === "failed") {
      await sendMessage(lastMessage.content);
    }
  }, [state.messages, sendMessage]);

  const value: ChatContextValue = {
    state,
    dispatch,
    sendMessage,
    loadConversation,
    startNewConversation,
    retryLastMessage,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

// Custom hook to use chat context
export function useChatContext() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChatContext must be used within ChatProvider");
  }
  return context;
}
