"use client";

/**
 * MessageInput Component
 * Feature: 018-chatkit-frontend
 *
 * Text input with send button
 */

import { useState, KeyboardEvent } from "react";
import { Send } from "lucide-react";

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled: boolean;
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim() || disabled) return;
    onSend(input);
    setInput("");
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const charCount = input.length;
  const showCharCounter = charCount > 4500;
  const charLimitReached = charCount > 5000;

  return (
    <div className="border-t border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-4">
      <div className="flex gap-3 items-end">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Shift+Enter for line break)"
            disabled={disabled}
            rows={1}
            className="w-full resize-none bg-transparent border-none focus:outline-none disabled:opacity-50 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
          />
          {showCharCounter && (
            <p className={`text-xs mt-1 ${charLimitReached ? "text-red-500" : "text-gray-500"}`}>
              {charCount}/5000 characters
            </p>
          )}
        </div>
        <button
          onClick={handleSend}
          disabled={!input.trim() || disabled || charLimitReached}
          className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center hover:scale-110 transition-transform disabled:opacity-50 disabled:hover:scale-100"
          aria-label="Send message"
        >
          <Send className="w-5 h-5 text-white" />
        </button>
      </div>
    </div>
  );
}
