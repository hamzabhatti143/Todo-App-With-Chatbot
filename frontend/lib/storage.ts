/**
 * SessionStorage utilities for chat feature
 * Feature: 018-chatkit-frontend
 */

const STORAGE_KEYS = {
  USER_ID: "chat_user_id",
  CONVERSATION_ID: (userId: string) => `chat_conversation_${userId}`,
} as const;

/**
 * Save user ID to sessionStorage
 */
export const saveUserId = (userId: string): void => {
  if (typeof window !== "undefined") {
    sessionStorage.setItem(STORAGE_KEYS.USER_ID, userId);
  }
};

/**
 * Get user ID from sessionStorage
 */
export const getUserId = (): string | null => {
  if (typeof window !== "undefined") {
    return sessionStorage.getItem(STORAGE_KEYS.USER_ID);
  }
  return null;
};

/**
 * Save conversation ID for a specific user
 */
export const saveConversationId = (userId: string, conversationId: string): void => {
  if (typeof window !== "undefined") {
    sessionStorage.setItem(STORAGE_KEYS.CONVERSATION_ID(userId), conversationId);
  }
};

/**
 * Get conversation ID for a specific user
 */
export const getConversationId = (userId: string): string | null => {
  if (typeof window !== "undefined") {
    return sessionStorage.getItem(STORAGE_KEYS.CONVERSATION_ID(userId));
  }
  return null;
};

/**
 * Clear all chat-related session storage
 */
export const clearSession = (): void => {
  if (typeof window !== "undefined") {
    const userId = getUserId();
    if (userId) {
      sessionStorage.removeItem(STORAGE_KEYS.CONVERSATION_ID(userId));
    }
    sessionStorage.removeItem(STORAGE_KEYS.USER_ID);
  }
};
