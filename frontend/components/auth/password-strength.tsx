/**
 * Password Strength Indicator
 *
 * Real-time password strength calculation with animated bar fill
 * and color transitions (red → yellow → green).
 */

'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

export type PasswordStrength = 0 | 1 | 2 | 3 | 4;

interface PasswordStrengthProps {
  password: string;
  className?: string;
}

/**
 * Calculate password strength (0-4 scale)
 */
export function calculatePasswordStrength(password: string): PasswordStrength {
  if (!password) return 0;

  let strength = 0;

  // Length check
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;

  // Character variety checks
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++; // Mixed case
  if (/\d/.test(password)) strength++; // Contains numbers
  if (/[^a-zA-Z0-9]/.test(password)) strength++; // Contains special characters

  // Cap at 4
  return Math.min(strength, 4) as PasswordStrength;
}

/**
 * Get strength label
 */
function getStrengthLabel(strength: PasswordStrength): string {
  const labels = ['Too weak', 'Weak', 'Fair', 'Good', 'Strong'];
  return labels[strength];
}

/**
 * Get strength color
 */
function getStrengthColor(strength: PasswordStrength): {
  bg: string;
  text: string;
} {
  const colors = [
    { bg: 'bg-gray-200 dark:bg-gray-700', text: 'text-gray-500 dark:text-gray-400' },
    { bg: 'bg-red-500', text: 'text-red-600 dark:text-red-400' },
    { bg: 'bg-orange-500', text: 'text-orange-600 dark:text-orange-400' },
    { bg: 'bg-yellow-500', text: 'text-yellow-600 dark:text-yellow-400' },
    { bg: 'bg-green-500', text: 'text-green-600 dark:text-green-400' },
  ];
  return colors[strength];
}

export function PasswordStrength({ password, className }: PasswordStrengthProps) {
  const strength = calculatePasswordStrength(password);
  const label = getStrengthLabel(strength);
  const color = getStrengthColor(strength);

  if (!password) return null;

  return (
    <div className={cn('space-y-2', className)}>
      {/* Strength bars */}
      <div className="flex gap-1">
        {[1, 2, 3, 4].map((level) => (
          <div
            key={level}
            className="h-1 flex-1 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden"
          >
            <motion.div
              className={cn('h-full', level <= strength ? color.bg : '')}
              initial={{ width: 0 }}
              animate={{ width: level <= strength ? '100%' : '0%' }}
              transition={{
                duration: 0.3,
                ease: 'easeOut',
                delay: level * 0.05,
              }}
            />
          </div>
        ))}
      </div>

      {/* Strength label */}
      <motion.p
        className={cn('text-xs font-medium', color.text)}
        initial={{ opacity: 0, y: -5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        Password strength: {label}
      </motion.p>

      {/* Strength tips */}
      {strength < 4 && (
        <motion.div
          className="text-xs text-gray-600 dark:text-gray-400 space-y-1"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.2 }}
        >
          <p className="font-medium">To improve strength:</p>
          <ul className="list-disc list-inside space-y-0.5">
            {password.length < 12 && <li>Use at least 12 characters</li>}
            {!/[a-z]/.test(password) && <li>Include lowercase letters</li>}
            {!/[A-Z]/.test(password) && <li>Include uppercase letters</li>}
            {!/\d/.test(password) && <li>Include numbers</li>}
            {!/[^a-zA-Z0-9]/.test(password) && <li>Include special characters (!@#$%^&*)</li>}
          </ul>
        </motion.div>
      )}
    </div>
  );
}
