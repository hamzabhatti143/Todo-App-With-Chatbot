/**
 * ConversationList Component
 *
 * Displays a list of user's conversations with message counts and timestamps.
 */

'use client'

import { MessageSquare, Plus, Loader2 } from 'lucide-react'
import type { ConversationListItem } from '@/types/chat'

interface ConversationListProps {
  conversations: ConversationListItem[]
  activeConversationId: string | null
  loading: boolean
  error: string | null
  onSelectConversation: (conversationId: string) => void
  onNewConversation: () => void
}

export function ConversationList({
  conversations,
  activeConversationId,
  loading,
  error,
  onSelectConversation,
  onNewConversation,
}: ConversationListProps) {
  // Format relative time
  const formatRelativeTime = (dateString: string): string => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`

    return date.toLocaleDateString()
  }

  return (
    <div className="flex flex-col h-full bg-white border-r border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Conversations</h2>
        <button
          onClick={onNewConversation}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span className="text-sm font-medium">New Conversation</span>
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="p-4 bg-red-50 border-b border-red-200">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Conversation List */}
      {!loading && !error && (
        <div className="flex-1 overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="p-4 text-center">
              <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p className="text-sm text-gray-500">No conversations yet</p>
              <p className="text-xs text-gray-400 mt-1">
                Start a new conversation to get started
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {conversations.map((conversation) => (
                <button
                  key={conversation.id}
                  onClick={() => onSelectConversation(conversation.id)}
                  className={`w-full text-left p-4 hover:bg-gray-50 transition-colors ${
                    activeConversationId === conversation.id
                      ? 'bg-blue-50 border-l-4 border-l-blue-600'
                      : 'border-l-4 border-l-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between mb-1">
                    <div className="flex items-center space-x-2">
                      <MessageSquare
                        className={`w-4 h-4 ${
                          activeConversationId === conversation.id
                            ? 'text-blue-600'
                            : 'text-gray-400'
                        }`}
                      />
                      <span
                        className={`text-sm font-medium ${
                          activeConversationId === conversation.id
                            ? 'text-blue-900'
                            : 'text-gray-900'
                        }`}
                      >
                        Conversation
                      </span>
                    </div>
                    <span className="text-xs text-gray-500">
                      {formatRelativeTime(conversation.updated_at)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      {conversation.message_count} message{conversation.message_count !== 1 ? 's' : ''}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
