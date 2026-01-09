/**
 * Dropdown Component
 *
 * Wraps Radix UI DropdownMenu with fade+slide-down animation and item hover effects.
 * Fully accessible with keyboard navigation.
 */

'use client';

import * as RadixDropdown from '@radix-ui/react-dropdown-menu';
import { motion } from 'framer-motion';
import { Check, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

export function Dropdown({ children, ...props }: RadixDropdown.DropdownMenuProps) {
  return <RadixDropdown.Root {...props}>{children}</RadixDropdown.Root>;
}

export function DropdownTrigger({ children, ...props }: RadixDropdown.DropdownMenuTriggerProps) {
  return <RadixDropdown.Trigger {...props}>{children}</RadixDropdown.Trigger>;
}

interface DropdownContentProps extends RadixDropdown.DropdownMenuContentProps {
  className?: string;
}

export function DropdownContent({
  children,
  className,
  sideOffset = 4,
  ...props
}: DropdownContentProps) {
  return (
    <RadixDropdown.Portal>
      <RadixDropdown.Content
        sideOffset={sideOffset}
        className={cn(
          'z-50 min-w-[12rem] overflow-hidden rounded-lg',
          'bg-white dark:bg-gray-800',
          'border border-gray-200 dark:border-gray-700',
          'shadow-lg',
          'animate-[fadeIn_0.2s_ease-out]',
          className
        )}
        asChild
        {...props}
      >
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
        >
          <div className="p-1">{children}</div>
        </motion.div>
      </RadixDropdown.Content>
    </RadixDropdown.Portal>
  );
}

interface DropdownItemProps extends RadixDropdown.DropdownMenuItemProps {
  className?: string;
  inset?: boolean;
}

export function DropdownItem({ className, inset, ...props }: DropdownItemProps) {
  return (
    <RadixDropdown.Item
      className={cn(
        'relative flex cursor-pointer select-none items-center rounded-md px-3 py-2 text-sm outline-none',
        'transition-colors duration-150',
        'text-gray-700 dark:text-gray-300',
        'hover:bg-gray-100 dark:hover:bg-gray-700',
        'focus:bg-gray-100 dark:focus:bg-gray-700',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        inset && 'pl-8',
        className
      )}
      {...props}
    />
  );
}

interface DropdownCheckboxItemProps extends RadixDropdown.DropdownMenuCheckboxItemProps {
  className?: string;
}

export function DropdownCheckboxItem({ className, children, ...props }: DropdownCheckboxItemProps) {
  return (
    <RadixDropdown.CheckboxItem
      className={cn(
        'relative flex cursor-pointer select-none items-center rounded-md py-2 pl-8 pr-3 text-sm outline-none',
        'transition-colors duration-150',
        'text-gray-700 dark:text-gray-300',
        'hover:bg-gray-100 dark:hover:bg-gray-700',
        'focus:bg-gray-100 dark:focus:bg-gray-700',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      {...props}
    >
      <span className="absolute left-2 flex h-4 w-4 items-center justify-center">
        <RadixDropdown.ItemIndicator>
          <Check className="h-4 w-4" />
        </RadixDropdown.ItemIndicator>
      </span>
      {children}
    </RadixDropdown.CheckboxItem>
  );
}

interface DropdownRadioItemProps extends RadixDropdown.DropdownMenuRadioItemProps {
  className?: string;
}

export function DropdownRadioItem({ className, children, ...props }: DropdownRadioItemProps) {
  return (
    <RadixDropdown.RadioItem
      className={cn(
        'relative flex cursor-pointer select-none items-center rounded-md py-2 pl-8 pr-3 text-sm outline-none',
        'transition-colors duration-150',
        'text-gray-700 dark:text-gray-300',
        'hover:bg-gray-100 dark:hover:bg-gray-700',
        'focus:bg-gray-100 dark:focus:bg-gray-700',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      {...props}
    >
      <span className="absolute left-2 flex h-4 w-4 items-center justify-center">
        <RadixDropdown.ItemIndicator>
          <div className="h-2 w-2 rounded-full bg-current" />
        </RadixDropdown.ItemIndicator>
      </span>
      {children}
    </RadixDropdown.RadioItem>
  );
}

export function DropdownLabel({ className, ...props }: RadixDropdown.DropdownMenuLabelProps) {
  return (
    <RadixDropdown.Label
      className={cn('px-3 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400', className)}
      {...props}
    />
  );
}

export function DropdownSeparator({ className, ...props }: RadixDropdown.DropdownMenuSeparatorProps) {
  return (
    <RadixDropdown.Separator
      className={cn('-mx-1 my-1 h-px bg-gray-200 dark:bg-gray-700', className)}
      {...props}
    />
  );
}

interface DropdownSubProps extends RadixDropdown.DropdownMenuSubProps {}

export function DropdownSub({ ...props }: DropdownSubProps) {
  return <RadixDropdown.Sub {...props} />;
}

export function DropdownSubTrigger({
  className,
  inset,
  children,
  ...props
}: RadixDropdown.DropdownMenuSubTriggerProps & { inset?: boolean }) {
  return (
    <RadixDropdown.SubTrigger
      className={cn(
        'flex cursor-pointer select-none items-center rounded-md px-3 py-2 text-sm outline-none',
        'transition-colors duration-150',
        'text-gray-700 dark:text-gray-300',
        'hover:bg-gray-100 dark:hover:bg-gray-700',
        'focus:bg-gray-100 dark:focus:bg-gray-700',
        'data-[state=open]:bg-gray-100 dark:data-[state=open]:bg-gray-700',
        inset && 'pl-8',
        className
      )}
      {...props}
    >
      {children}
      <ChevronRight className="ml-auto h-4 w-4" />
    </RadixDropdown.SubTrigger>
  );
}

export function DropdownSubContent({
  className,
  ...props
}: RadixDropdown.DropdownMenuSubContentProps) {
  return (
    <RadixDropdown.SubContent
      className={cn(
        'z-50 min-w-[12rem] overflow-hidden rounded-lg',
        'bg-white dark:bg-gray-800',
        'border border-gray-200 dark:border-gray-700',
        'shadow-lg',
        'p-1',
        className
      )}
      {...props}
    />
  );
}
