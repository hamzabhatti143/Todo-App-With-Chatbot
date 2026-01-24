"use client";

/**
 * MessageList Component
 * Feature: 018-chatkit-frontend
 *
 * Renders list of messages with auto-scroll
 */

import { useEffect, useRef } from "react";
import { Message } from "./Message";
import type { UIMessage } from "@/types/chat";

interface MessageListProps {
  messages: UIMessage[];
}

export function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto space-y-4 px-4 py-4">
      {messages.map((message) => (
        <Message key={message.id || message.tempId} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
