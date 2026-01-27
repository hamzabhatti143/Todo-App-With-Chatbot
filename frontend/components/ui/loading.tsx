"use client";

/**
 * Loading Animation Component
 *
 * Provides various loading animations for different use cases
 */

import { Loader2 } from "lucide-react";

interface LoadingProps {
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "spinner" | "dots" | "pulse" | "bars";
  text?: string;
  fullScreen?: boolean;
}

export function Loading({
  size = "md",
  variant = "spinner",
  text,
  fullScreen = false,
}: LoadingProps) {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12",
    xl: "w-16 h-16",
  };

  const containerClasses = fullScreen
    ? "fixed inset-0 flex items-center justify-center bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm z-50"
    : "flex items-center justify-center p-4";

  const renderAnimation = () => {
    switch (variant) {
      case "spinner":
        return (
          <Loader2
            className={`${sizeClasses[size]} animate-spin text-primary-500`}
          />
        );

      case "dots":
        return (
          <div className="flex gap-2">
            <div className={`${sizeClasses[size]} bg-primary-500 rounded-full animate-bounce`} style={{ animationDelay: "0ms" }}></div>
            <div className={`${sizeClasses[size]} bg-primary-500 rounded-full animate-bounce`} style={{ animationDelay: "150ms" }}></div>
            <div className={`${sizeClasses[size]} bg-primary-500 rounded-full animate-bounce`} style={{ animationDelay: "300ms" }}></div>
          </div>
        );

      case "pulse":
        return (
          <div className={`${sizeClasses[size]} bg-primary-500 rounded-full animate-ping`}></div>
        );

      case "bars":
        return (
          <div className="flex gap-1 items-end">
            <div className="w-1 h-8 bg-primary-500 animate-pulse" style={{ animationDelay: "0ms" }}></div>
            <div className="w-1 h-10 bg-primary-500 animate-pulse" style={{ animationDelay: "150ms" }}></div>
            <div className="w-1 h-6 bg-primary-500 animate-pulse" style={{ animationDelay: "300ms" }}></div>
            <div className="w-1 h-10 bg-primary-500 animate-pulse" style={{ animationDelay: "450ms" }}></div>
            <div className="w-1 h-8 bg-primary-500 animate-pulse" style={{ animationDelay: "600ms" }}></div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className={containerClasses}>
      <div className="flex flex-col items-center gap-3 animate-fade-in">
        {renderAnimation()}
        {text && (
          <p className="text-sm font-medium text-slate-700 dark:text-white/80 animate-pulse">
            {text}
          </p>
        )}
      </div>
    </div>
  );
}

/**
 * Page Loading Spinner
 */
export function PageLoading({ text = "Loading..." }: { text?: string }) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center gap-4 animate-fade-in">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-primary-200 dark:border-primary-900 rounded-full"></div>
          <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
        </div>
        <p className="text-lg font-medium text-slate-900 dark:text-white/95">{text}</p>
      </div>
    </div>
  );
}

/**
 * Button Loading State
 */
export function ButtonLoading() {
  return (
    <Loader2 className="w-4 h-4 animate-spin" />
  );
}

/**
 * Skeleton Loading
 */
interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className = "" }: SkeletonProps) {
  return (
    <div
      className={`bg-slate-200 dark:bg-slate-700 animate-pulse rounded ${className}`}
    ></div>
  );
}

/**
 * Card Skeleton
 */
export function CardSkeleton() {
  return (
    <div className="glass-card p-4 space-y-3 animate-fade-in">
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <div className="flex gap-2 mt-4">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  );
}

/**
 * List Skeleton
 */
export function ListSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="space-y-2 animate-fade-in">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 p-3 glass-card">
          <Skeleton className="w-10 h-10 rounded-full flex-shrink-0" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-3 w-1/2" />
          </div>
        </div>
      ))}
    </div>
  );
}
