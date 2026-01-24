/**
 * Chat API Client
 * Feature: 018-chatkit-frontend
 *
 * Dedicated API client for chat endpoints using backend URL (localhost:8000)
 */

import axios from "axios";
import type {
  ChatRequest,
  ChatResponse,
  ConversationListResponse,
  ConversationDetailResponse,
  ApiError,
} from "@/types/chat";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// Log backend URL for debugging
if (typeof window !== "undefined") {
  console.log("💬 Chat API Configuration:", {
    url: BACKEND_URL,
    env: process.env.NEXT_PUBLIC_BACKEND_URL,
    source: process.env.NEXT_PUBLIC_BACKEND_URL ? "environment variable" : "fallback",
  });
}

// Create dedicated axios instance for chat endpoints
const chatApiClient = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000, // 30 second timeout (FR-014)
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add authentication token
chatApiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
chatApiClient.interceptors.response.use(
  (response) => response,
  (error): Promise<ApiError> => {
    if (error.response) {
      // Server responded with error status
      return Promise.reject({
        type: "server" as const,
        statusCode: error.response.status,
        message: error.response.data?.detail || "Server error",
      });
    } else if (error.request) {
      // Request made but no response (network error)
      return Promise.reject({
        type: "network" as const,
        message: "Network error. Please check your connection.",
      });
    } else if (error.code === "ECONNABORTED") {
      // Timeout
      return Promise.reject({
        type: "timeout" as const,
        message: "Request timed out. Please try again.",
      });
    } else {
      // Unknown error
      return Promise.reject({
        type: "unknown" as const,
        message: error.message || "An unexpected error occurred",
      });
    }
  }
);

/**
 * Send a chat message to the backend
 * @param content - Message content (1-5000 chars)
 * @param conversationId - Optional conversation ID for continuing conversation
 * @returns Chat response with assistant message
 */
export const sendChatMessage = async (
  content: string,
  conversationId: string | null
): Promise<ChatResponse> => {
  const request: ChatRequest = {
    content,
    ...(conversationId && { conversation_id: conversationId }),
  };

  const response = await chatApiClient.post<ChatResponse>("/api/chat", request);
  return response.data;
};

/**
 * Get list of user's conversations (P2 feature)
 * @returns List of conversation summaries
 */
export const getConversations = async (): Promise<ConversationListResponse> => {
  const response = await chatApiClient.get<ConversationListResponse>("/api/conversations");
  return response.data;
};

/**
 * Get detailed conversation with full message history (P2 feature)
 * @param conversationId - Conversation ID
 * @returns Conversation with messages
 */
export const getConversationDetail = async (
  conversationId: string
): Promise<ConversationDetailResponse> => {
  const response = await chatApiClient.get<ConversationDetailResponse>(
    `/api/conversations/${conversationId}`
  );
  return response.data;
};

/**
 * Check if backend is healthy
 * @returns True if backend is accessible
 */
export const checkHealth = async (): Promise<boolean> => {
  try {
    const response = await chatApiClient.get("/health");
    return response.data.status === "healthy";
  } catch {
    return false;
  }
};
