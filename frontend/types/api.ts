/**
 * API Type Definitions
 *
 * TypeScript interfaces for API responses and errors.
 * Provides type safety for HTTP communication with backend.
 */

import { Task } from './task';
import { User } from './user';

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message?: string;
}

/**
 * API error response
 */
export interface ApiError {
  detail: string;
  status?: number;
  field?: string;
}

/**
 * Validation error with field-specific messages
 */
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

/**
 * FastAPI validation error response
 */
export interface FastAPIValidationError {
  detail: ValidationError[];
}

/**
 * Authentication response (login/register)
 */
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user?: User;
}

/**
 * Task list response
 */
export type TaskListResponse = Task[];

/**
 * Single task response
 */
export type TaskResponse = Task;

/**
 * User profile response
 */
export type UserResponse = User;

/**
 * Pagination metadata
 */
export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

/**
 * API request status
 */
export type RequestStatus = 'idle' | 'loading' | 'success' | 'error';

/**
 * API request state
 */
export interface RequestState<T = unknown> {
  status: RequestStatus;
  data: T | null;
  error: ApiError | null;
}
