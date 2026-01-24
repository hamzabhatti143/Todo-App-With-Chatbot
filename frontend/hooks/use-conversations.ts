/**
 * Conversations Hook
 *
 * Custom hook for managing conversation list and loading conversation history.
 */

'use client'

import { useState, useEffect, useCallback } from 'react'
import { conversationsApi, handleApiError } from '@/lib/api'
import { appEvents, APP_EVENTS } from '@/lib/events'
import type { ConversationListItem } from '@/types/chat'

export function useConversations() {
  const [conversations, setConversations] = useState<ConversationListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchConversations = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await conversationsApi.list(50, 0)
      setConversations(data)
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchConversations()
  }, [fetchConversations])

  // Listen for auth events to reload/clear conversations
  useEffect(() => {
    const handleLogin = () => {
      // Reload conversations when user logs in
      fetchConversations()
    }

    const handleLogout = () => {
      // Clear conversations when user logs out
      setConversations([])
      setError(null)
    }

    appEvents.on(APP_EVENTS.USER_LOGGED_IN, handleLogin)
    appEvents.on(APP_EVENTS.USER_LOGGED_OUT, handleLogout)

    return () => {
      appEvents.off(APP_EVENTS.USER_LOGGED_IN, handleLogin)
      appEvents.off(APP_EVENTS.USER_LOGGED_OUT, handleLogout)
    }
  }, [fetchConversations])

  return {
    conversations,
    loading,
    error,
    refetch: fetchConversations,
  }
}
