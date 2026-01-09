/**
 * Task List Component
 */

'use client'

import { TaskItem } from './task-item'
import type { Task } from '@/types/task'

interface TaskListProps {
  tasks: Task[]
  onToggleComplete: (taskId: string) => Promise<{ success: boolean; error?: string }>
  onDelete: (taskId: string) => Promise<{ success: boolean; error?: string }>
  onEdit?: (task: Task) => void
}

export function TaskList({ tasks, onToggleComplete, onDelete, onEdit }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No tasks yet. Create your first task to get started!</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  )
}
