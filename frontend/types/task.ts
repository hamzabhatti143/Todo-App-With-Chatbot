/**
 * Task Type Definitions
 *
 * TypeScript interfaces for task entities and operations.
 * Matches backend SQLModel schema for type safety.
 */

import { z } from 'zod';

/**
 * Task entity from database
 */
export interface Task {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * Input for creating a new task
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Input for updating an existing task
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

/**
 * Filter options for task list
 */
export type FilterType = 'all' | 'active' | 'completed';

/**
 * Legacy filter type (alias for backwards compatibility)
 */
export type TaskFilter = FilterType;

/**
 * Sort options for task list
 */
export type SortType = 'newest' | 'oldest' | 'title-asc' | 'title-desc';

/**
 * Task list state
 */
export interface TaskListState {
  tasks: Task[];
  filter: FilterType;
  sort: SortType;
  searchQuery: string;
}

/**
 * Task statistics
 */
export interface TaskStats {
  total: number;
  active: number;
  completed: number;
  completionRate: number;
}

/**
 * Zod schema for task creation validation
 */
export const createTaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title must be less than 200 characters'),
  description: z.string().max(1000, 'Description must be less than 1000 characters').optional(),
});
