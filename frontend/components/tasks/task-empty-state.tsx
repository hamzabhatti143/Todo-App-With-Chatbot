/**
 * Task Empty State Component
 *
 * Displays when no tasks exist, with animated illustration,
 * fade-in animation, and call-to-action button.
 */

'use client';

import { motion } from 'framer-motion';
import { Plus, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { FadeIn } from '@/components/animations/fade-in';

interface TaskEmptyStateProps {
  onCreateNew?: () => void;
}

export function TaskEmptyState({ onCreateNew }: TaskEmptyStateProps) {
  return (
    <FadeIn className="flex flex-col items-center justify-center py-16 px-4">
      {/* Animated Illustration */}
      <motion.div
        className="relative w-32 h-32 mb-6"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{
          duration: 0.5,
          ease: 'easeOut',
          delay: 0.1,
        }}
      >
        {/* Circle background */}
        <motion.div
          className="absolute inset-0 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{
            duration: 0.6,
            ease: [0.34, 1.56, 0.64, 1],
            delay: 0.2,
          }}
        />

        {/* Checkmark icon */}
        <motion.div
          className="absolute inset-0 flex items-center justify-center"
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{
            duration: 0.6,
            ease: [0.34, 1.56, 0.64, 1],
            delay: 0.4,
          }}
        >
          <CheckCircle2 className="h-16 w-16 text-blue-500 dark:text-blue-400" />
        </motion.div>

        {/* Floating particles */}
        {[...Array(3)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 rounded-full bg-blue-400 dark:bg-blue-500"
            style={{
              top: `${20 + i * 25}%`,
              left: `${10 + i * 30}%`,
            }}
            animate={{
              y: [0, -20, 0],
              opacity: [0.3, 1, 0.3],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: i * 0.3,
              ease: 'easeInOut',
            }}
          />
        ))}
      </motion.div>

      {/* Text */}
      <motion.h3
        className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.5 }}
      >
        No tasks yet
      </motion.h3>

      <motion.p
        className="text-gray-600 dark:text-gray-400 text-center max-w-sm mb-6"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.6 }}
      >
        Get started by creating your first task. Stay organized and boost your productivity!
      </motion.p>

      {/* CTA Button */}
      {onCreateNew && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.7 }}
        >
          <Button onClick={onCreateNew} size="lg">
            <Plus className="h-5 w-5 mr-2" />
            Create your first task
          </Button>
        </motion.div>
      )}
    </FadeIn>
  );
}
