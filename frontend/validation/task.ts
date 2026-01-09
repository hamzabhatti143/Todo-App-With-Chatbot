/**
 * Task Validation Schemas
 */

import { z } from 'zod'

export const createTaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title must be 200 characters or less'),
  description: z.string().max(1000, 'Description must be 1000 characters or less').optional().nullable(),
})

export const updateTaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title must be 200 characters or less').optional(),
  description: z.string().max(1000, 'Description must be 1000 characters or less').optional().nullable(),
  completed: z.boolean().optional(),
})

export type CreateTaskInput = z.infer<typeof createTaskSchema>
export type UpdateTaskInput = z.infer<typeof updateTaskSchema>
