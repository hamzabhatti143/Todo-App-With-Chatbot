/**
 * Chat Hook
 *
 * Custom hook for managing chat messages and conversation state.
 */

'use client'

import { useState, useCallback, useEffect } from 'react'
import { chatApi, conversationsApi, handleApiError } from '@/lib/api'
import { appEvents, APP_EVENTS } from '@/lib/events'
import type { ChatMessage, ChatMessageRequest, ChatMessageResponse } from '@/types/chat'

interface UseChatOptions {
  initialConversationId?: string | null
}

export function useChat(options: UseChatOptions = {}) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [conversationId, setConversationId] = useState<string | null>(options.initialConversationId || null)
  const [loading, setLoading] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Load conversation history when conversation ID changes
  useEffect(() => {
    const loadConversation = async () => {
      if (!conversationId) {
        setMessages([])
        return
      }

      try {
        setLoadingHistory(true)
        setError(null)
        const conversationMessages = await conversationsApi.getMessages(conversationId)
        setMessages(conversationMessages)
      } catch (err) {
        setError(handleApiError(err))
      } finally {
        setLoadingHistory(false)
      }
    }

    loadConversation()
  }, [conversationId])

  const sendMessage = useCallback(
    async (content: string): Promise<{ success: boolean; error?: string; response?: ChatMessageResponse }> => {
      if (!content.trim()) {
        return { success: false, error: 'Message cannot be empty' }
      }

      try {
        setLoading(true)
        setError(null)

        // Add user message to UI immediately (optimistic update)
        const tempUserMessage: ChatMessage = {
          id: `temp-${Date.now()}`,
          conversation_id: conversationId || '',
          role: 'user',
          content: content.trim(),
          created_at: new Date().toISOString(),
        }
        setMessages((prev) => [...prev, tempUserMessage])

        // Send message to backend
        const requestData: ChatMessageRequest = {
          content: content.trim(),
          conversation_id: conversationId || undefined,
        }

        const response = await chatApi.sendMessage(requestData)

        // Update conversation ID if this is the first message
        if (!conversationId) {
          setConversationId(response.conversation_id)
        }

        // Replace temp message with actual user message and add assistant response
        setMessages((prev) => {
          // Remove temp message
          const withoutTemp = prev.filter((msg) => msg.id !== tempUserMessage.id)

          // Add user message (if not already included in response)
          const userMessage: ChatMessage = {
            id: tempUserMessage.id, // Keep temp ID since backend doesn't return user message
            conversation_id: response.conversation_id,
            role: 'user',
            content: content.trim(),
            created_at: new Date().toISOString(),
          }

          // Add assistant message
          const assistantMessage: ChatMessage = {
            id: response.message_id,
            conversation_id: response.conversation_id,
            role: 'assistant',
            content: response.content,
            created_at: response.created_at,
          }

          return [...withoutTemp, userMessage, assistantMessage]
        })

        return { success: true, response }
      } catch (err) {
        const errorMessage = handleApiError(err)
        setError(errorMessage)

        // Remove optimistic message on error
        setMessages((prev) => prev.filter((msg) => !msg.id.startsWith('temp-')))

        return { success: false, error: errorMessage }
      } finally {
        setLoading(false)
      }
    },
    [conversationId]
  )

  const clearMessages = useCallback(() => {
    setMessages([])
    setConversationId(null)
    setError(null)
  }, [])

  const loadConversation = useCallback((convId: string) => {
    setConversationId(convId)
  }, [])

  const startNewConversation = useCallback(() => {
    setMessages([])
    setConversationId(null)
    setError(null)
  }, [])

  // Listen for logout to clear chat state
  useEffect(() => {
    const handleLogout = () => {
      setMessages([])
      setConversationId(null)
      setError(null)
    }

    appEvents.on(APP_EVENTS.USER_LOGGED_OUT, handleLogout)

    return () => {
      appEvents.off(APP_EVENTS.USER_LOGGED_OUT, handleLogout)
    }
  }, [])

  return {
    messages,
    conversationId,
    loading,
    loadingHistory,
    error,
    sendMessage,
    clearMessages,
    loadConversation,
    startNewConversation,
  }
}
