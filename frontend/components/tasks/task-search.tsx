/**
 * Task Search Component
 *
 * Search input with focus glow, icon animation, and debounced onChange handler.
 * Debounces user input by 300ms before triggering search.
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Search, X } from 'lucide-react';
import { debounce } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface TaskSearchProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
}

export function TaskSearch({
  value,
  onChange,
  placeholder = 'Search tasks...',
  className,
}: TaskSearchProps) {
  const [localValue, setLocalValue] = useState(value);
  const [isFocused, setIsFocused] = useState(false);

  // Debounced onChange handler
  const debouncedOnChange = useCallback(
    debounce((newValue: string) => {
      onChange(newValue);
    }, 300),
    [onChange]
  );

  // Update local value when external value changes
  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    debouncedOnChange(newValue);
  };

  const handleClear = () => {
    setLocalValue('');
    onChange('');
  };

  return (
    <div className={cn('relative', className)}>
      {/* Search Icon */}
      <motion.div
        className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        animate={{
          scale: isFocused ? 1.1 : 1,
          color: isFocused ? '#3b82f6' : '#9ca3af',
        }}
        transition={{ duration: 0.2 }}
      >
        <Search className="h-5 w-5" />
      </motion.div>

      {/* Input */}
      <input
        type="text"
        value={localValue}
        onChange={handleChange}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={placeholder}
        className={cn(
          'w-full pl-10 pr-10 py-2.5 border rounded-lg',
          'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
          'transition-all duration-200',
          'border-gray-300 dark:border-gray-600',
          'bg-white dark:bg-gray-800',
          'text-gray-900 dark:text-gray-100',
          'placeholder:text-gray-400 dark:placeholder:text-gray-500',
          isFocused && 'shadow-[0_0_0_3px_rgba(59,130,246,0.1)]'
        )}
      />

      {/* Clear Button */}
      {localValue && (
        <motion.button
          type="button"
          onClick={handleClear}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors p-2.5 min-h-[44px] min-w-[44px] flex items-center justify-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          transition={{ duration: 0.2 }}
        >
          <X className="h-4 w-4" />
        </motion.button>
      )}
    </div>
  );
}
