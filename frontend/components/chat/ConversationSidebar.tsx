"use client";

/**
 * ConversationSidebar Component
 * Feature: 018-chatkit-frontend - Phase 4 (P2)
 *
 * Displays list of previous conversations with ability to resume
 */

import { useEffect, useState } from "react";
import { MessageSquare, Plus, Loader2 } from "lucide-react";
import { getConversations } from "@/lib/chat-api";
import type { ConversationListItem } from "@/types/chat";
import { useChatContext } from "@/contexts/ChatContext";

export function ConversationSidebar() {
  const { state, loadConversation, startNewConversation } = useChatContext();
  const [conversations, setConversations] = useState<ConversationListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setLoading(true);
    setError(null);
    try {
      const conversations = await getConversations();
      setConversations(conversations);
    } catch (err: any) {
      setError("Failed to load conversations");
      // Better error logging for debugging
      if (err?.response) {
        console.error("API Error:", {
          status: err.response.status,
          message: err.response.data?.detail || err.message,
          url: err.config?.url,
        });
      } else if (err?.request) {
        console.error("Network Error: No response received", err.message);
      } else {
        console.error("Error:", err.message || err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConversation = async (conversationId: string) => {
    await loadConversation(conversationId);
  };

  const handleNewConversation = () => {
    startNewConversation();
    // Refresh conversation list after a delay
    setTimeout(loadConversations, 1000);
  };

  return (
    <div className="h-full flex flex-col bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-700">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-slate-700">
        <button
          onClick={handleNewConversation}
          className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-4 py-2 rounded-lg hover:scale-105 transition-transform"
        >
          <Plus className="w-5 h-5" />
          New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
          </div>
        ) : error ? (
          <div className="p-4 text-center text-red-500 text-sm">{error}</div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
            No conversations yet
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {conversations.map((conversation) => {
              const isActive = state.conversationId === conversation.id;
              const date = new Date(conversation.updated_at);
              const dateStr = date.toLocaleDateString([], {
                month: "short",
                day: "numeric",
              });

              return (
                <button
                  key={conversation.id}
                  onClick={() => handleSelectConversation(conversation.id)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    isActive
                      ? "bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800"
                      : "hover:bg-gray-100 dark:hover:bg-slate-800"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <MessageSquare
                      className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                        isActive ? "text-blue-600" : "text-gray-400"
                      }`}
                    />
                    <div className="flex-1 min-w-0">
                      <p
                        className={`text-sm font-medium truncate ${
                          isActive
                            ? "text-blue-900 dark:text-blue-100"
                            : "text-gray-900 dark:text-white"
                        }`}
                      >
                        {conversation.title || "Untitled Conversation"}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 truncate mt-1">
                        {conversation.last_message}
                      </p>
                      <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                        {dateStr}
                      </p>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
