/**
 * Loading Spinner Component
 * Feature: 018-chatkit-frontend
 */

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
}

export function LoadingSpinner({ size = "md" }: LoadingSpinnerProps) {
  const sizes = {
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  return (
    <div className="flex items-center justify-center">
      <div
        className={`${sizes[size]} border-4 border-white/30 border-t-white rounded-full animate-spin`}
        aria-label="Loading"
      />
    </div>
  );
}
