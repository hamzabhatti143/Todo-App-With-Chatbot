/**
 * Task Form Modal Component
 *
 * Modal dialog for creating and editing tasks with slide-up animation,
 * Zod validation, and mode prop for create/edit.
 */

'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { createTaskSchema, type Task, type TaskCreate } from '@/types/task';
import { cn } from '@/lib/utils';

interface TaskFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: TaskCreate) => Promise<void>;
  mode?: 'create' | 'edit';
  initialData?: Task | null;
}

export function TaskForm({
  open,
  onOpenChange,
  onSubmit,
  mode = 'create',
  initialData,
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof TaskCreate, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form with initial data in edit mode
  useEffect(() => {
    if (mode === 'edit' && initialData) {
      setFormData({
        title: initialData.title,
        description: initialData.description || '',
      });
    } else {
      setFormData({ title: '', description: '' });
    }
    setErrors({});
  }, [mode, initialData, open]);

  const handleChange = (field: keyof TaskCreate) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
    // Clear error for this field when user types
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate with Zod
    const result = createTaskSchema.safeParse(formData);

    if (!result.success) {
      const fieldErrors: Partial<Record<keyof TaskCreate, string>> = {};
      result.error.errors.forEach((error) => {
        const field = error.path[0] as keyof TaskCreate;
        if (!fieldErrors[field]) {
          fieldErrors[field] = error.message;
        }
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      setIsSubmitting(true);
      await onSubmit(result.data);
      onOpenChange(false);
      // Reset form
      setFormData({ title: '', description: '' });
    } catch (error) {
      setErrors({ title: 'An error occurred. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>
            {mode === 'create' ? 'Create New Task' : 'Edit Task'}
          </DialogTitle>
          <DialogDescription>
            {mode === 'create'
              ? 'Add a new task to your list. Click save when you\'re done.'
              : 'Make changes to your task. Click save when you\'re done.'}
          </DialogDescription>
        </DialogHeader>

        <motion.form
          onSubmit={handleSubmit}
          className="space-y-4 py-4"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Title Input */}
          <div className="space-y-2">
            <label
              htmlFor="title"
              className="text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Title <span className="text-red-500">*</span>
            </label>
            <Input
              id="title"
              value={formData.title}
              onChange={handleChange('title')}
              error={errors.title}
              placeholder="Enter task title"
              required
              disabled={isSubmitting}
              autoFocus
            />
          </div>

          {/* Description Textarea */}
          <div className="space-y-2">
            <label
              htmlFor="description"
              className="text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Description
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={handleChange('description')}
              placeholder="Enter task description (optional)"
              disabled={isSubmitting}
              rows={4}
              className={cn(
                'w-full px-3 py-2.5 border rounded-lg shadow-sm',
                'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'transition-all duration-200',
                'resize-none',
                'border-gray-300 dark:border-gray-600',
                'dark:bg-gray-800 dark:text-gray-100',
                'disabled:opacity-50 disabled:cursor-not-allowed',
                errors.description && 'border-red-500 focus:ring-red-500'
              )}
            />
            {errors.description && (
              <p className="text-sm text-red-600 dark:text-red-400">
                {errors.description}
              </p>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="secondary"
              onClick={() => onOpenChange(false)}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button type="submit" loading={isSubmitting} disabled={isSubmitting}>
              {isSubmitting
                ? mode === 'create'
                  ? 'Creating...'
                  : 'Saving...'
                : mode === 'create'
                ? 'Create Task'
                : 'Save Changes'}
            </Button>
          </DialogFooter>
        </motion.form>
      </DialogContent>
    </Dialog>
  );
}
