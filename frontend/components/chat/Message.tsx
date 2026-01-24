/**
 * Message Component (Optimized)
 * Feature: 018-chatkit-frontend - Phase 6 (Polish)
 *
 * Renders a single chat message with role-based styling
 * Memoized to prevent unnecessary re-renders
 */

import { memo } from "react";
import { Bot, User as UserIcon } from "lucide-react";
import type { UIMessage } from "@/types/chat";

interface MessageProps {
  message: UIMessage;
}

export const Message = memo(function Message({ message }: MessageProps) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";

  // Format timestamp
  const timestamp = new Date(message.created_at).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      className={`flex gap-3 animate-slide-up ${
        isUser ? "justify-end" : "justify-start"
      }`}
      role="article"
      aria-label={`Message from ${isUser ? "you" : "assistant"}`}
    >
      {/* Assistant avatar */}
      {isAssistant && (
        <div
          className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center flex-shrink-0"
          aria-hidden="true"
        >
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      {/* Message bubble */}
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-gradient-to-r from-blue-500 to-indigo-600 text-white"
            : "bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700"
        }`}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
        <p
          className={`text-xs mt-1 ${
            isUser ? "text-blue-100" : "text-gray-500 dark:text-gray-400"
          }`}
        >
          {timestamp}
          {message.status === "pending" && " • Sending..."}
          {message.status === "failed" && " • Failed"}
        </p>
      </div>

      {/* User avatar */}
      {isUser && (
        <div
          className="w-8 h-8 bg-gray-300 dark:bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0"
          aria-hidden="true"
        >
          <UserIcon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </div>
      )}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison: only re-render if message ID or status changes
  return (
    prevProps.message.id === nextProps.message.id &&
    prevProps.message.status === nextProps.message.status
  );
});
