/**
 * Task Form Component
 */

'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import type { Task, TaskCreate } from '@/types/task'

interface TaskFormProps {
  onSubmit: (data: TaskCreate) => Promise<{ success: boolean; error?: string }>
  onCancel?: () => void
  initialData?: Task | null
}

export function TaskForm({ onSubmit, onCancel, initialData }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  // Populate form with initial data for edit mode
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title)
      setDescription(initialData.description || '')
    }
  }, [initialData])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!title.trim()) {
      setError('Title is required')
      return
    }

    setLoading(true)
    const result = await onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
    })

    if (result.success) {
      setTitle('')
      setDescription('')
      onCancel?.()
    } else {
      setError(result.error || 'Failed to create task')
    }
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title"
        required
        maxLength={200}
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Description (optional)
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          maxLength={1000}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <div className="flex justify-end space-x-2">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" disabled={loading}>
          {loading ? (initialData ? 'Updating...' : 'Creating...') : (initialData ? 'Update Task' : 'Create Task')}
        </Button>
      </div>
    </form>
  )
}
