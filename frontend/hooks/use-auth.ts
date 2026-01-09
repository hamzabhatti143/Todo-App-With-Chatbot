/**
 * Authentication Hook
 */

'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authApi, handleApiError } from '@/lib/api'
import type { UserLogin, UserCreate } from '@/types/user'

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userId, setUserId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated on mount
    const token = localStorage.getItem('auth_token')
    const storedUserId = localStorage.getItem('user_id')

    if (token && storedUserId) {
      setIsAuthenticated(true)
      setUserId(storedUserId)
    }
    setLoading(false)
  }, [])

  const login = async (data: UserLogin): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await authApi.login(data)
      localStorage.setItem('auth_token', response.access_token)

      // Decode JWT to get user ID (simple base64 decode)
      const payload = JSON.parse(atob(response.access_token.split('.')[1]))
      const userId = payload.sub
      localStorage.setItem('user_id', userId)

      setIsAuthenticated(true)
      setUserId(userId)
      return { success: true }
    } catch (error) {
      return { success: false, error: handleApiError(error) }
    }
  }

  const register = async (data: UserCreate): Promise<{ success: boolean; error?: string }> => {
    try {
      await authApi.register(data)

      // Auto-login after registration
      const loginResult = await login({ email: data.email, password: data.password })
      return loginResult
    } catch (error) {
      return { success: false, error: handleApiError(error) }
    }
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_id')
    setIsAuthenticated(false)
    setUserId(null)
    router.push('/auth/login')
  }

  return {
    isAuthenticated,
    userId,
    loading,
    login,
    register,
    logout,
  }
}
