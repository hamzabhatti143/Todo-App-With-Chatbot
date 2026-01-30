/**
 * Tasks Hook
 */

'use client'

import { useState, useEffect } from 'react'
import { tasksApi, handleApiError } from '@/lib/api'
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'

export function useTasks(username: string | null) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchTasks = async () => {
    if (!username) return

    try {
      setLoading(true)
      setError(null)
      const data = await tasksApi.getAll(username)
      setTasks(data)
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [username])

  const createTask = async (data: TaskCreate): Promise<{ success: boolean; error?: string }> => {
    if (!username) return { success: false, error: 'User not authenticated' }

    try {
      const newTask = await tasksApi.create(username, data)
      setTasks((prev) => [newTask, ...prev])
      return { success: true }
    } catch (err) {
      return { success: false, error: handleApiError(err) }
    }
  }

  const updateTask = async (taskId: string, data: TaskUpdate): Promise<{ success: boolean; error?: string }> => {
    if (!username) return { success: false, error: 'User not authenticated' }

    try {
      const updatedTask = await tasksApi.update(username, taskId, data)
      setTasks((prev) => prev.map((task) => (task.id === taskId ? updatedTask : task)))
      return { success: true }
    } catch (err) {
      return { success: false, error: handleApiError(err) }
    }
  }

  const deleteTask = async (taskId: string): Promise<{ success: boolean; error?: string }> => {
    if (!username) return { success: false, error: 'User not authenticated' }

    try {
      await tasksApi.delete(username, taskId)
      setTasks((prev) => prev.filter((task) => task.id !== taskId))
      return { success: true }
    } catch (err) {
      return { success: false, error: handleApiError(err) }
    }
  }

  const toggleComplete = async (taskId: string): Promise<{ success: boolean; error?: string }> => {
    if (!username) return { success: false, error: 'User not authenticated' }

    try {
      const updatedTask = await tasksApi.toggleComplete(username, taskId)
      setTasks((prev) => prev.map((task) => (task.id === taskId ? updatedTask : task)))
      return { success: true }
    } catch (err) {
      return { success: false, error: handleApiError(err) }
    }
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
  }
}
