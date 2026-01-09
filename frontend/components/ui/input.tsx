/**
 * Input Component
 *
 * Floating label input with focus glow and error shake animation.
 * Includes proper ARIA attributes for accessibility.
 */

'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    const [hasValue, setHasValue] = useState(!!props.value || !!props.defaultValue);

    const inputId = id || `input-${label?.replace(/\s+/g, '-').toLowerCase() || Math.random()}`;
    const errorId = `${inputId}-error`;

    const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(true);
      props.onFocus?.(e);
    };

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(false);
      setHasValue(!!e.target.value);
      props.onBlur?.(e);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(!!e.target.value);
      props.onChange?.(e);
    };

    const isFloating = isFocused || hasValue;

    return (
      <div className="w-full">
        <div className="relative">
          {label && (
            <motion.label
              htmlFor={inputId}
              className={cn(
                'absolute left-3 transition-all duration-200 ease-out pointer-events-none',
                isFloating
                  ? 'top-0 -translate-y-1/2 text-xs bg-white dark:bg-gray-900 px-1 text-blue-600 dark:text-blue-400'
                  : 'top-1/2 -translate-y-1/2 text-base text-gray-500 dark:text-gray-400'
              )}
              initial={false}
              animate={{
                scale: isFloating ? 0.85 : 1,
              }}
              transition={{ duration: 0.2, ease: 'easeOut' }}
            >
              {label}
            </motion.label>
          )}
          <motion.div
            animate={error ? { x: [-4, 4, -4, 4, 0] } : {}}
            transition={error ? { duration: 0.4 } : undefined}
          >
            <input
              ref={ref}
              id={inputId}
              className={cn(
                'w-full px-3 py-2.5 border rounded-lg shadow-sm',
                'focus:outline-none focus:ring-2 focus:ring-offset-0',
                'transition-all duration-200',
                'min-h-[44px]',
                error
                  ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500',
                'dark:bg-gray-800 dark:text-gray-100',
                isFocused && !error && 'shadow-[0_0_0_3px_rgba(59,130,246,0.1)]',
                className
              )}
              onFocus={handleFocus}
              onBlur={handleBlur}
              onChange={handleChange}
              aria-invalid={!!error}
              aria-describedby={error ? errorId : undefined}
              {...props}
            />
          </motion.div>
        </div>
        {error && (
          <motion.p
            id={errorId}
            className="mt-1 text-sm text-red-600 dark:text-red-400"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            role="alert"
          >
            {error}
          </motion.p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
