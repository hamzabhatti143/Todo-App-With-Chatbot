/**
 * Avatar Component
 *
 * Wraps Radix UI Avatar with image fade-in, fallback initials, and size variants.
 * Automatically generates initials from name if image is unavailable.
 */

'use client';

import React from 'react';
import * as RadixAvatar from '@radix-ui/react-avatar';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

/**
 * Get initials from a name
 */
function getInitials(name: string): string {
  const parts = name.trim().split(' ');
  if (parts.length === 0) return '?';
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

export function Avatar({ src, alt, name, size = 'md', className }: AvatarProps) {
  const sizeStyles = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
    xl: 'h-16 w-16 text-lg',
  };

  const initials = name ? getInitials(name) : '?';
  const avatarAlt = alt || name || 'Avatar';

  return (
    <RadixAvatar.Root
      className={cn(
        'relative inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full',
        'bg-gradient-to-br from-blue-500 to-purple-600',
        sizeStyles[size],
        className
      )}
    >
      <RadixAvatar.Image
        src={src}
        alt={avatarAlt}
        className="h-full w-full object-cover"
        asChild
      >
        <motion.img
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        />
      </RadixAvatar.Image>

      <RadixAvatar.Fallback
        className="flex h-full w-full items-center justify-center font-semibold text-white"
        delayMs={150}
      >
        <motion.span
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          {initials}
        </motion.span>
      </RadixAvatar.Fallback>
    </RadixAvatar.Root>
  );
}

/**
 * Avatar Group Component
 *
 * Displays multiple avatars in a stacked layout
 */
interface AvatarGroupProps {
  children: React.ReactNode;
  max?: number;
  className?: string;
}

export function AvatarGroup({ children, max = 5, className }: AvatarGroupProps) {
  const childrenArray = React.Children.toArray(children);
  const displayedChildren = max ? childrenArray.slice(0, max) : childrenArray;
  const remainingCount = childrenArray.length - displayedChildren.length;

  return (
    <div className={cn('flex -space-x-2', className)}>
      {displayedChildren.map((child, index) => (
        <div
          key={index}
          className="ring-2 ring-white dark:ring-gray-900 rounded-full"
          style={{ zIndex: displayedChildren.length - index }}
        >
          {child}
        </div>
      ))}
      {remainingCount > 0 && (
        <div
          className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 dark:bg-gray-700 text-sm font-medium text-gray-700 dark:text-gray-300 ring-2 ring-white dark:ring-gray-900"
          style={{ zIndex: 0 }}
        >
          +{remainingCount}
        </div>
      )}
    </div>
  );
}
