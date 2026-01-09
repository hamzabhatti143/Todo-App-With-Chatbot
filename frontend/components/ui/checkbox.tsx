/**
 * Checkbox Component
 *
 * Wraps Radix UI Checkbox with checkmark draw animation and scale-on-check effect.
 * Fully accessible with keyboard navigation and ARIA attributes.
 */

'use client';

import React from 'react';
import * as RadixCheckbox from '@radix-ui/react-checkbox';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CheckboxProps {
  id?: string;
  checked?: boolean;
  defaultChecked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  label?: string;
  className?: string;
}

export const Checkbox = React.forwardRef<
  React.ElementRef<typeof RadixCheckbox.Root>,
  CheckboxProps
>(({ id, checked, defaultChecked, onCheckedChange, disabled, label, className }, ref) => {
  const checkboxId = id || `checkbox-${label?.replace(/\s+/g, '-').toLowerCase() || Math.random()}`;

  return (
    <div className="flex items-center">
      <div className="p-3 -m-3">
        <RadixCheckbox.Root
          ref={ref}
          id={checkboxId}
          checked={checked}
          defaultChecked={defaultChecked}
          onCheckedChange={onCheckedChange}
          disabled={disabled}
          className={cn(
            'peer relative flex h-5 w-5 shrink-0 items-center justify-center rounded border-2 transition-all duration-200',
            'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'border-gray-300 dark:border-gray-600',
            'data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600',
            'data-[state=checked]:dark:bg-blue-500 data-[state=checked]:dark:border-blue-500',
            'hover:border-blue-500 dark:hover:border-blue-400',
            className
          )}
        >
        <RadixCheckbox.Indicator className="flex items-center justify-center">
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{
              type: 'spring',
              stiffness: 500,
              damping: 30,
            }}
          >
            <Check className="h-3.5 w-3.5 text-white" strokeWidth={3} />
          </motion.div>
        </RadixCheckbox.Indicator>
      </RadixCheckbox.Root>
      </div>

      {label && (
        <label
          htmlFor={checkboxId}
          className="ml-2 text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer select-none peer-disabled:cursor-not-allowed peer-disabled:opacity-50"
        >
          {label}
        </label>
      )}
    </div>
  );
});

Checkbox.displayName = 'Checkbox';
