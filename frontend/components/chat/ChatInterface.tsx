"use client";

/**
 * ChatInterface Component
 * Feature: 018-chatkit-frontend
 *
 * Main chat interface integrating all components
 */

import { useChatContext } from "@/contexts/ChatContext";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";
import { LoadingSpinner } from "./LoadingSpinner";
import { ErrorMessage } from "./ErrorMessage";
import { Bot } from "lucide-react";
import { isRetryable } from "@/lib/error-handler";
import type { ApiError } from "@/types/chat";

interface ChatInterfaceProps {
  userId: string;
  userName: string;
}

export function ChatInterface({ userName }: ChatInterfaceProps) {
  const { state, sendMessage, retryLastMessage } = useChatContext();

  const handleSend = async (message: string) => {
    await sendMessage(message);
  };

  const handleRetry = async () => {
    await retryLastMessage();
  };

  // Welcome message if no messages yet
  const messages = state.messages.length === 0
    ? [
        {
          id: "welcome",
          conversation_id: "",
          role: "assistant" as const,
          content: `👋 Hi ${userName}! I'm TodoBot, your AI task assistant. I can help you manage your tasks through natural language. Try saying "Add buy groceries" or "Show my tasks"!`,
          created_at: new Date().toISOString(),
        },
      ]
    : state.messages;

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white dark:bg-slate-900 border-b border-gray-200 dark:border-slate-700 p-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">TodoBot</h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">AI Task Assistant</p>
          </div>
          <div className="ml-auto text-right">
            <p className="text-sm font-medium text-gray-900 dark:text-white">{userName}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {state.conversationId ? `Conversation #${state.conversationId.slice(0, 8)}` : "New conversation"}
            </p>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {state.error && (
        <div className="p-4">
          <ErrorMessage
            message={state.error}
            onDismiss={() => {
              /* Clear error via dispatch if needed */
            }}
            onRetry={handleRetry}
            retryable={isRetryable({ type: "unknown", message: state.error } as ApiError)}
          />
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden flex flex-col bg-gray-50 dark:bg-slate-950">
        <MessageList messages={messages} />

        {/* Loading indicator */}
        {state.loading && (
          <div className="px-4 pb-4">
            <div className="flex gap-3 justify-start animate-slide-up">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white dark:bg-slate-800 px-4 py-3 rounded-2xl border border-gray-200 dark:border-slate-700">
                <LoadingSpinner size="sm" />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <MessageInput onSend={handleSend} disabled={state.loading} />
    </div>
  );
}
