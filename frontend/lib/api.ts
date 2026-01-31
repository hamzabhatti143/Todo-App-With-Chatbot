/**
 * API Client
 *
 * Axios-based client for communicating with the FastAPI backend.
 */

import axios, { AxiosError } from 'axios'
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'
import type { UserCreate, UserLogin, Token, User } from '@/types/user'
import type {
  ChatMessageRequest,
  ChatMessageResponse,
  ConversationListItem,
  ConversationWithMessages,
  ChatMessage
} from '@/types/chat'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hamzabhatti-todo-ai-chatbot.hf.space'

// Log API URL for debugging (will show in browser console)
if (typeof window !== 'undefined') {
  console.log('🔗 API Configuration:', {
    url: API_URL,
    env: process.env.NEXT_PUBLIC_API_URL,
    source: process.env.NEXT_PUBLIC_API_URL ? 'environment variable' : 'fallback'
  })
}

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for AI chat requests (can take 20-30s)
})

// Add auth request interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle 401 Unauthorized - token expired or invalid
      if (error.response.status === 401) {
        // Clear auth state
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user_id')

        // Redirect to sign in page
        if (typeof window !== 'undefined') {
          window.location.href = '/signin?expired=true'
        }
      }

      // Handle 403 Forbidden - access denied
      if (error.response.status === 403) {
        // Error will be caught by the calling code
        // and displayed to user
        console.error('Access denied:', error.response.data)
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  register: async (data: UserCreate): Promise<User> => {
    const response = await apiClient.post('/api/auth/register', data)
    return response.data
  },

  login: async (data: UserLogin): Promise<Token> => {
    const response = await apiClient.post('/api/auth/login', data)
    return response.data
  },
}

// Tasks API
export const tasksApi = {
  getAll: async (username: string): Promise<Task[]> => {
    const response = await apiClient.get(`/api/${username}/tasks`)
    return response.data
  },

  getOne: async (username: string, taskId: string): Promise<Task> => {
    const response = await apiClient.get(`/api/${username}/tasks/${taskId}`)
    return response.data
  },

  create: async (username: string, data: TaskCreate): Promise<Task> => {
    const response = await apiClient.post(`/api/${username}/tasks`, data)
    return response.data
  },

  update: async (username: string, taskId: string, data: TaskUpdate): Promise<Task> => {
    const response = await apiClient.put(`/api/${username}/tasks/${taskId}`, data)
    return response.data
  },

  delete: async (username: string, taskId: string): Promise<void> => {
    await apiClient.delete(`/api/${username}/tasks/${taskId}`)
  },

  toggleComplete: async (username: string, taskId: string): Promise<Task> => {
    const response = await apiClient.patch(`/api/${username}/tasks/${taskId}/complete`)
    return response.data
  },
}

// Chat API
export const chatApi = {
  sendMessage: async (data: ChatMessageRequest): Promise<ChatMessageResponse> => {
    const response = await apiClient.post('/api/chat', data)
    return response.data
  },
}

// Conversations API
export const conversationsApi = {
  list: async (limit: number = 50, offset: number = 0): Promise<ConversationListItem[]> => {
    const response = await apiClient.get('/api/conversations', {
      params: { limit, offset },
    })
    return response.data
  },

  get: async (conversationId: string): Promise<ConversationWithMessages> => {
    const response = await apiClient.get(`/api/conversations/${conversationId}`)
    return response.data
  },

  getMessages: async (conversationId: string): Promise<ChatMessage[]> => {
    const response = await apiClient.get(`/api/conversations/${conversationId}/messages`)
    return response.data
  },
}

// Error handling helper
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail: string }>
    return axiosError.response?.data?.detail || axiosError.message || 'An error occurred'
  }
  return 'An unexpected error occurred'
}
