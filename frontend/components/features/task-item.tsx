/**
 * Task Item Component
 */

'use client'

import { useState } from 'react'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import type { Task } from '@/types/task'

interface TaskItemProps {
  task: Task
  onToggleComplete: (taskId: string) => Promise<{ success: boolean; error?: string }>
  onDelete: (taskId: string) => Promise<{ success: boolean; error?: string }>
  onEdit?: (task: Task) => void
}

export function TaskItem({ task, onToggleComplete, onDelete, onEdit }: TaskItemProps) {
  const [loading, setLoading] = useState(false)

  const handleToggle = async () => {
    setLoading(true)
    await onToggleComplete(task.id)
    setLoading(false)
  }

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this task?')) {
      setLoading(true)
      await onDelete(task.id)
      setLoading(false)
    }
  }

  const handleEdit = () => {
    if (onEdit) {
      onEdit(task)
    }
  }

  return (
    <div className="flex flex-col sm:flex-row items-start space-y-3 sm:space-y-0 sm:space-x-3 p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start space-x-3 flex-1 w-full">
        <div className="flex-shrink-0 pt-1">
          <Checkbox
            checked={task.completed}
            onCheckedChange={handleToggle}
            disabled={loading}
          />
        </div>

        <div className="flex-1 min-w-0">
          <h3 className={`text-base font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      <div className="flex space-x-2 sm:flex-shrink-0 w-full sm:w-auto">
        {onEdit && (
          <Button
            variant="secondary"
            size="sm"
            onClick={handleEdit}
            disabled={loading}
            className="flex-1 sm:flex-none min-w-[44px] min-h-[44px] sm:min-w-0 sm:min-h-0"
          >
            Edit
          </Button>
        )}
        <Button
          variant="danger"
          size="sm"
          onClick={handleDelete}
          disabled={loading}
          className="flex-1 sm:flex-none min-w-[44px] min-h-[44px] sm:min-w-0 sm:min-h-0"
        >
          Delete
        </Button>
      </div>
    </div>
  )
}
