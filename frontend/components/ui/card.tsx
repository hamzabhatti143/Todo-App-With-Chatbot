/**
 * Card Component
 *
 * Flexible card component with glassmorphism variant and hover lift effect.
 * Supports configurable padding and can be used with or without motion.
 */

'use client';

import React from 'react';
import { motion, MotionProps } from 'framer-motion';
import { cn } from '@/lib/utils';
import { hoverLift } from '@/lib/animations';

interface CardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, keyof MotionProps> {
  variant?: 'default' | 'glass';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  children: React.ReactNode;
}

export function Card({
  variant = 'default',
  padding = 'md',
  hover = false,
  className,
  children,
  ...props
}: CardProps) {
  const baseStyles = 'rounded-lg transition-shadow duration-200';

  const variantStyles = {
    default: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-md',
    glass: 'glass-card',
  };

  const paddingStyles = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  if (hover) {
    return (
      <motion.div
        className={cn(baseStyles, variantStyles[variant], paddingStyles[padding], className)}
        whileHover={hoverLift}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div
      className={cn(baseStyles, variantStyles[variant], paddingStyles[padding], className)}
      {...props}
    >
      {children}
    </div>
  );
}

/**
 * Card Header Component
 */
export function CardHeader({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('mb-4', className)} {...props}>
      {children}
    </div>
  );
}

/**
 * Card Title Component
 */
export function CardTitle({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3 className={cn('text-lg font-semibold text-gray-900 dark:text-gray-100', className)} {...props}>
      {children}
    </h3>
  );
}

/**
 * Card Description Component
 */
export function CardDescription({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p className={cn('text-sm text-gray-600 dark:text-gray-400', className)} {...props}>
      {children}
    </p>
  );
}

/**
 * Card Content Component
 */
export function CardContent({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('', className)} {...props}>
      {children}
    </div>
  );
}

/**
 * Card Footer Component
 */
export function CardFooter({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('mt-4 flex items-center gap-2', className)} {...props}>
      {children}
    </div>
  );
}
