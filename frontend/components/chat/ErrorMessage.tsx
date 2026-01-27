/**
 * Error Message Component with Retry
 * Feature: 018-chatkit-frontend
 */

import { AlertCircle, X, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
  onRetry?: () => void;
  retryable?: boolean;
}

export function ErrorMessage({
  message,
  onDismiss,
  onRetry,
  retryable = false,
}: ErrorMessageProps) {
  return (
    <div className="bg-red-900/30 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg relative animate-slide-down">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          <p className="font-medium">{message}</p>
          {retryable && onRetry && (
            <button
              onClick={onRetry}
              className="mt-2 text-sm font-semibold text-red-300 hover:text-red-100 flex items-center gap-1"
            >
              <RefreshCw className="w-4 h-4" />
              Try Again
            </button>
          )}
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="flex-shrink-0 hover:text-red-100 transition-colors"
            aria-label="Dismiss error"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}
