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
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Header */}
      <div className="glass-navbar backdrop-blur-xl p-4 animate-slide-down bg-slate-900/95 border-b border-slate-700/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center shadow-lg animate-pulse-subtle">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">TodoBot</h2>
            <p className="text-sm text-white/80">AI Task Assistant</p>
          </div>
          <div className="ml-auto text-right">
            <p className="text-sm font-medium text-white/95">{userName}</p>
            <p className="text-xs text-white/60">
              {state.conversationId ? `Conversation #${state.conversationId.slice(0, 8)}` : "New conversation"}
            </p>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {state.error && (
        <div className="p-4 animate-slide-down">
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
      <div className="flex-1 overflow-hidden flex flex-col bg-slate-900/50">
        <MessageList messages={messages} />

        {/* Loading indicator */}
        {state.loading && (
          <div className="px-4 pb-4">
            <div className="flex gap-3 justify-start animate-slide-up">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center shadow-lg">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="glass-card px-4 py-3 rounded-2xl bg-slate-800/90 border-slate-700/50">
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
