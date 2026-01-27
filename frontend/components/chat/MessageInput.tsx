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
    <div className="glass-navbar backdrop-blur-xl p-4 border-t border-slate-700/50 bg-slate-900/95">
      <div className="flex gap-3 items-end">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Shift+Enter for line break)"
            disabled={disabled}
            rows={1}
            className="w-full resize-none bg-slate-800/60 border border-slate-700/50 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-400/30 disabled:opacity-50 text-white placeholder-white/50 transition-all"
          />
          {showCharCounter && (
            <p className={`text-xs mt-1 ${charLimitReached ? "text-red-400" : "text-white/60"}`}>
              {charCount}/5000 characters
            </p>
          )}
        </div>
        <button
          onClick={handleSend}
          disabled={!input.trim() || disabled || charLimitReached}
          className="w-10 h-10 btn-primary rounded-full flex items-center justify-center hover:scale-110 transition-all disabled:opacity-50 disabled:hover:scale-100 shadow-lg"
          aria-label="Send message"
        >
          <Send className="w-5 h-5 text-white" />
        </button>
      </div>
    </div>
  );
}
