/**
 * Dialog Component
 *
 * Wraps Radix UI Dialog with animated backdrop fade, content scale-in (desktop),
 * and bottom-sheet slide (mobile) animations.
 */

'use client';

import React from 'react';
import * as RadixDialog from '@radix-ui/react-dialog';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useMediaQuery } from '@/lib/hooks/use-media-query';

interface DialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}

export function Dialog({ open, onOpenChange, children }: DialogProps) {
  return (
    <RadixDialog.Root open={open} onOpenChange={onOpenChange}>
      {children}
    </RadixDialog.Root>
  );
}

export function DialogTrigger({ children, ...props }: RadixDialog.DialogTriggerProps) {
  return <RadixDialog.Trigger {...props}>{children}</RadixDialog.Trigger>;
}

interface DialogContentProps {
  children: React.ReactNode;
  className?: string;
  showClose?: boolean;
}

export function DialogContent({ children, className, showClose = true }: DialogContentProps) {
  const isMobile = useMediaQuery('(max-width: 640px)');

  return (
    <RadixDialog.Portal forceMount>
      <AnimatePresence>
        <RadixDialog.Overlay key="dialog-overlay" asChild>
          <motion.div
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          />
        </RadixDialog.Overlay>

        <RadixDialog.Content key="dialog-content" asChild>
          {isMobile ? (
            // Mobile: Bottom sheet animation
            <motion.div
              className={cn(
                'fixed bottom-0 left-0 right-0 z-50',
                'max-h-[90vh] overflow-y-auto',
                'bg-white dark:bg-gray-900',
                'rounded-t-2xl shadow-2xl',
                className
              )}
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{
                type: 'spring',
                damping: 30,
                stiffness: 300,
              }}
            >
              {showClose && (
                <RadixDialog.Close className="absolute right-4 top-4 rounded-full p-3.5 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center">
                  <X className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                  <span className="sr-only">Close</span>
                </RadixDialog.Close>
              )}
              <div className="p-6">{children}</div>
            </motion.div>
          ) : (
            // Desktop: Centered modal with scale animation
            <motion.div
              className={cn(
                'fixed left-1/2 top-1/2 z-50',
                'w-full max-w-lg max-h-[90vh] overflow-y-auto',
                'bg-white dark:bg-gray-900',
                'rounded-lg shadow-2xl',
                'focus:outline-none',
                className
              )}
              style={{ x: '-50%', y: '-50%' }}
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              transition={{
                type: 'spring',
                damping: 25,
                stiffness: 300,
              }}
            >
              {showClose && (
                <RadixDialog.Close className="absolute right-4 top-4 rounded-full p-3.5 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center">
                  <X className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                  <span className="sr-only">Close</span>
                </RadixDialog.Close>
              )}
              <div className="p-6">{children}</div>
            </motion.div>
          )}
        </RadixDialog.Content>
      </AnimatePresence>
    </RadixDialog.Portal>
  );
}

export function DialogHeader({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('mb-4', className)} {...props}>
      {children}
    </div>
  );
}

export function DialogTitle({ className, children, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <RadixDialog.Title asChild>
      <h2 className={cn('text-xl font-semibold text-gray-900 dark:text-gray-100', className)} {...props}>
        {children}
      </h2>
    </RadixDialog.Title>
  );
}

export function DialogDescription({ className, children, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <RadixDialog.Description asChild>
      <p className={cn('text-sm text-gray-600 dark:text-gray-400 mt-2', className)} {...props}>
        {children}
      </p>
    </RadixDialog.Description>
  );
}

export function DialogFooter({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('mt-6 flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)} {...props}>
      {children}
    </div>
  );
}
