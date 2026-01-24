/**
 * Error handling utilities for chat API
 * Feature: 018-chatkit-frontend
 */

import type { ApiError } from "@/types/chat";

/**
 * Convert API error to user-friendly message
 */
export const getErrorMessage = (error: ApiError): string => {
  if (error.type === "network") {
    return "You're offline. Please check your connection.";
  }

  if (error.type === "timeout") {
    return "Request timed out. Please try again.";
  }

  if (error.statusCode === 400) {
    return error.message || "Invalid request. Please check your input.";
  }

  if (error.statusCode === 401) {
    return "Your session has expired. Please log in again.";
  }

  if (error.statusCode === 403) {
    return "You do not have permission to access this resource.";
  }

  if (error.statusCode === 404) {
    return "Conversation not found.";
  }

  if (error.statusCode === 500) {
    return "Unable to reach AI assistant. Please try again.";
  }

  if (error.statusCode === 503) {
    return "Service temporarily unavailable. Please try again later.";
  }

  return error.message || "An unexpected error occurred. Please try again.";
};

/**
 * Check if error is retryable
 */
export const isRetryable = (error: ApiError): boolean => {
  return (
    error.type === "network" ||
    error.type === "timeout" ||
    error.statusCode === 500 ||
    error.statusCode === 503
  );
};
