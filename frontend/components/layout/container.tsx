/**
 * Container Component
 *
 * Responsive container with configurable max-width variants and padding.
 * Centers content and provides consistent spacing across the application.
 */

'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  centerContent?: boolean;
  children: React.ReactNode;
}

export function Container({
  maxWidth = 'xl',
  padding = 'md',
  centerContent = true,
  className,
  children,
  ...props
}: ContainerProps) {
  const maxWidthStyles = {
    sm: 'max-w-screen-sm',    // 640px
    md: 'max-w-screen-md',    // 768px
    lg: 'max-w-screen-lg',    // 1024px
    xl: 'max-w-screen-xl',    // 1280px
    '2xl': 'max-w-screen-2xl', // 1536px
    full: 'max-w-full',
  };

  const paddingStyles = {
    none: 'px-0',
    sm: 'px-4',
    md: 'px-4 sm:px-6 lg:px-8',
    lg: 'px-6 sm:px-8 lg:px-12',
  };

  return (
    <div
      className={cn(
        'w-full',
        centerContent && 'mx-auto',
        maxWidthStyles[maxWidth],
        paddingStyles[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

/**
 * Section Component - Semantic wrapper for page sections
 */
interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  maxWidth?: ContainerProps['maxWidth'];
  padding?: ContainerProps['padding'];
  children: React.ReactNode;
}

export function Section({
  maxWidth = 'xl',
  padding = 'md',
  className,
  children,
  ...props
}: SectionProps) {
  return (
    <section className={cn('py-8 sm:py-12 lg:py-16', className)} {...props}>
      <Container maxWidth={maxWidth} padding={padding}>
        {children}
      </Container>
    </section>
  );
}
