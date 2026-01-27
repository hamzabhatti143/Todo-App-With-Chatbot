"use client";

/**
 * ConversationSidebar Component
 * Feature: 018-chatkit-frontend - Phase 4 (P2)
 *
 * Displays list of previous conversations with ability to resume
 */

import { useEffect, useState } from "react";
import { MessageSquare, Plus } from "lucide-react";
import { getConversations } from "@/lib/chat-api";
import type { ConversationListItem } from "@/types/chat";
import { useChatContext } from "@/contexts/ChatContext";
import { Loading } from "@/components/ui/loading";

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
    <div className="h-full flex flex-col glass backdrop-blur-xl border-r border-slate-700/50 bg-slate-900/90">
      {/* Header */}
      <div className="p-4 border-b border-slate-700/50 animate-slide-down">
        <button
          onClick={handleNewConversation}
          className="w-full btn-primary flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transition-all"
        >
          <Plus className="w-5 h-5" />
          New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto smooth-scroll">
        {loading ? (
          <div className="p-8">
            <Loading variant="spinner" size="md" text="Loading conversations..." />
          </div>
        ) : error ? (
          <div className="p-4 text-center text-red-400 text-sm animate-shake">{error}</div>
        ) : conversations.length === 0 ? (
          <div className="p-4 text-center text-white/60 text-sm animate-fade-in">
            No conversations yet
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {conversations.map((conversation, index) => {
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
                  className={`w-full text-left p-3 rounded-xl transition-all animate-slide-up ${
                    isActive
                      ? "glass-card border-primary-400/50 shadow-lg transform scale-[1.02] bg-slate-800/90"
                      : "glass-button hover:glass-card hover:transform hover:scale-[1.01] bg-slate-800/60 hover:bg-slate-800/80"
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="flex items-start gap-2">
                    <MessageSquare
                      className={`w-4 h-4 mt-0.5 flex-shrink-0 transition-colors ${
                        isActive ? "text-primary-400" : "text-white/50"
                      }`}
                    />
                    <div className="flex-1 min-w-0">
                      <p
                        className={`text-sm font-medium truncate ${
                          isActive
                            ? "text-white"
                            : "text-white/90"
                        }`}
                      >
                        {conversation.title || "Untitled Conversation"}
                      </p>
                      <p className="text-xs text-white/60 truncate mt-1">
                        {conversation.last_message}
                      </p>
                      <p className="text-xs text-white/40 mt-1">
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
