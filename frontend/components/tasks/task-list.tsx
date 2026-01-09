/**
 * Task List Component
 *
 * Displays tasks with staggered children animation on load,
 * layout shift animation when tasks are added/removed,
 * and empty state handling.
 */

'use client';

import { AnimatePresence } from 'framer-motion';
import { StaggerChildren, StaggerItem } from '@/components/animations/stagger-children';
import { TaskCard } from './task-card';
import { TaskEmptyState } from './task-empty-state';
import type { Task } from '@/types/task';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onCreateNew?: () => void;
}

export function TaskList({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  onCreateNew,
}: TaskListProps) {
  // Show empty state if no tasks
  if (tasks.length === 0) {
    return <TaskEmptyState onCreateNew={onCreateNew} />;
  }

  return (
    <StaggerChildren
      staggerDelay={0.1}
      delayChildren={0.1}
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      <AnimatePresence mode="popLayout">
        {tasks.map((task) => (
          <StaggerItem key={task.id}>
            <TaskCard
              task={task}
              onToggleComplete={onToggleComplete}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          </StaggerItem>
        ))}
      </AnimatePresence>
    </StaggerChildren>
  );
}
