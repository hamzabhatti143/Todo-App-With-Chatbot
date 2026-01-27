/**
 * Tabs Component
 *
 * Wraps Radix UI Tabs with animated sliding indicator using layoutId
 * and content fade transitions.
 */

'use client';

import * as RadixTabs from '@radix-ui/react-tabs';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

export function Tabs({ className, ...props }: RadixTabs.TabsProps) {
  return <RadixTabs.Root className={cn('w-full', className)} {...props} />;
}

interface TabsListProps extends RadixTabs.TabsListProps {
  className?: string;
}

export function TabsList({ className, ...props }: TabsListProps) {
  return (
    <RadixTabs.List
      className={cn(
        'inline-flex items-center justify-center rounded-lg',
        'bg-slate-800/60',
        'p-1',
        className
      )}
      {...props}
    />
  );
}

interface TabsTriggerProps extends RadixTabs.TabsTriggerProps {
  className?: string;
}

export function TabsTrigger({ className, children, value, ...props }: TabsTriggerProps) {
  return (
    <RadixTabs.Trigger
      value={value}
      className={cn(
        'relative inline-flex items-center justify-center whitespace-nowrap',
        'rounded-md px-4 py-2 text-sm font-medium',
        'transition-all duration-200',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        'text-gray-400',
        'hover:text-gray-100',
        'data-[state=active]:text-gray-100',
        className
      )}
      {...props}
    >
      {children}
      <AnimatePresence>
        <RadixTabs.Trigger value={value} asChild>
          <motion.div
            className="absolute inset-0 z-[-1] rounded-md bg-slate-700 shadow-sm"
            layoutId="activeTab"
            initial={false}
            transition={{
              type: 'spring',
              stiffness: 500,
              damping: 30,
            }}
          />
        </RadixTabs.Trigger>
      </AnimatePresence>
    </RadixTabs.Trigger>
  );
}

interface TabsContentProps extends RadixTabs.TabsContentProps {
  className?: string;
}

export function TabsContent({ className, children, ...props }: TabsContentProps) {
  return (
    <RadixTabs.Content
      className={cn(
        'mt-4',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2',
        className
      )}
      asChild
      {...props}
    >
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
      >
        {children}
      </motion.div>
    </RadixTabs.Content>
  );
}
