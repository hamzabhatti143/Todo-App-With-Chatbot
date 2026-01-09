/**
 * Task Card Component
 *
 * Individual task card with hover lift effect, checkbox with checkmark animation,
 * strikethrough on completion, edit/delete buttons that fade in on hover,
 * and swipe-to-delete gesture for mobile.
 */

'use client';

import { useState } from 'react';
import { motion, useMotionValue, useTransform, PanInfo } from 'framer-motion';
import { Pencil, Trash2 } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { formatRelativeTime } from '@/lib/utils';
import { cn } from '@/lib/utils';
import type { Task } from '@/types/task';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Swipe-to-delete for mobile
  const x = useMotionValue(0);
  const opacity = useTransform(x, [-150, 0], [0, 1]);
  const deleteOpacity = useTransform(x, [-150, -50, 0], [1, 0.5, 0]);

  const handleDragEnd = (_event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => {
    if (info.offset.x < -100) {
      // Swipe left threshold reached - delete
      handleDelete();
    } else {
      // Snap back
      x.set(0);
    }
  };

  const handleToggle = () => {
    onToggleComplete(task.id);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    await new Promise((resolve) => setTimeout(resolve, 300));
    onDelete(task.id);
  };

  return (
    <motion.div
      className="relative"
      initial={{ opacity: 0, y: 20 }}
      animate={
        isDeleting
          ? { opacity: 0, x: -300, transition: { duration: 0.3 } }
          : { opacity: 1, y: 0 }
      }
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.2 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
    >
      {/* Delete indicator (visible during swipe) */}
      <motion.div
        className="absolute inset-y-0 right-0 flex items-center justify-end px-6 bg-red-500 rounded-lg"
        style={{ opacity: deleteOpacity }}
      >
        <Trash2 className="h-5 w-5 text-white" />
      </motion.div>

      {/* Task Card */}
      <motion.div
        drag="x"
        dragConstraints={{ left: -150, right: 0 }}
        dragElastic={0.2}
        onDragEnd={handleDragEnd}
        style={{ x, opacity }}
        className={cn(
          'relative bg-white dark:bg-gray-800 rounded-lg p-4',
          'border border-gray-200 dark:border-gray-700',
          'shadow-sm transition-shadow',
          'cursor-pointer'
        )}
        whileHover={{ y: -2, boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)' }}
        transition={{ duration: 0.2 }}
      >
        <div className="flex items-start gap-3">
          {/* Checkbox */}
          <div className="flex-shrink-0 pt-0.5">
            <Checkbox
              checked={task.completed}
              onCheckedChange={handleToggle}
            />
          </div>

          {/* Task Content */}
          <div className="flex-1 min-w-0">
            <motion.h3
              className={cn(
                'text-base font-medium transition-colors',
                task.completed
                  ? 'text-gray-400 dark:text-gray-500'
                  : 'text-gray-900 dark:text-gray-100'
              )}
              animate={{
                textDecoration: task.completed ? 'line-through' : 'none',
              }}
              transition={{ duration: 0.2 }}
            >
              {task.title}
            </motion.h3>

            {task.description && (
              <motion.p
                className={cn(
                  'mt-1 text-sm transition-colors',
                  task.completed
                    ? 'text-gray-400 dark:text-gray-600'
                    : 'text-gray-600 dark:text-gray-400'
                )}
                animate={{
                  textDecoration: task.completed ? 'line-through' : 'none',
                }}
                transition={{ duration: 0.2 }}
              >
                {task.description}
              </motion.p>
            )}

            <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
              {formatRelativeTime(task.created_at)}
            </p>
          </div>

          {/* Action Buttons (fade in on hover) */}
          <motion.div
            className="flex items-center gap-1 flex-shrink-0"
            initial={{ opacity: 0, x: 10 }}
            animate={{
              opacity: isHovered ? 1 : 0,
              x: isHovered ? 0 : 10,
            }}
            transition={{ duration: 0.2 }}
          >
            <Button
              variant="ghost"
              size="sm"
              onClick={handleEdit}
              className="h-11 w-11 p-0"
              aria-label="Edit task"
            >
              <Pencil className="h-4 w-4" />
            </Button>

            <Button
              variant="ghost"
              size="sm"
              onClick={handleDelete}
              className="h-11 w-11 p-0 text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20"
              aria-label="Delete task"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </motion.div>
        </div>
      </motion.div>
    </motion.div>
  );
}
