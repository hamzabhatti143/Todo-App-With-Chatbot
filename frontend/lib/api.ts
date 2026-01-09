/**
 * API Client
 *
 * Axios-based client for communicating with the FastAPI backend.
 */

import axios, { AxiosError } from 'axios'
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'
import type { UserCreate, UserLogin, Token, User } from '@/types/user'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

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
  getAll: async (userId: string): Promise<Task[]> => {
    const response = await apiClient.get(`/api/${userId}/tasks`)
    return response.data
  },

  getOne: async (userId: string, taskId: string): Promise<Task> => {
    const response = await apiClient.get(`/api/${userId}/tasks/${taskId}`)
    return response.data
  },

  create: async (userId: string, data: TaskCreate): Promise<Task> => {
    const response = await apiClient.post(`/api/${userId}/tasks`, data)
    return response.data
  },

  update: async (userId: string, taskId: string, data: TaskUpdate): Promise<Task> => {
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, data)
    return response.data
  },

  delete: async (userId: string, taskId: string): Promise<void> => {
    await apiClient.delete(`/api/${userId}/tasks/${taskId}`)
  },

  toggleComplete: async (userId: string, taskId: string): Promise<Task> => {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`)
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
