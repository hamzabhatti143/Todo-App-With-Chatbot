/**
 * FadeIn Animation Wrapper
 *
 * Wraps children in a fade-in animation with configurable delay and duration.
 * Uses Framer Motion for smooth entrance animations.
 */

'use client';

import React from 'react';
import { motion, Variants } from 'framer-motion';

interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}

export function FadeIn({ children, delay = 0, duration = 0.3, className }: FadeInProps) {
  const customVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration,
        delay,
        ease: 'easeOut',
      },
    },
  };

  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      exit="hidden"
      variants={customVariants}
    >
      {children}
    </motion.div>
  );
}

/**
 * FadeInView - Only animates when scrolled into view
 */
interface FadeInViewProps extends FadeInProps {
  once?: boolean;
}

export function FadeInView({ children, delay = 0, duration = 0.3, once = true, className }: FadeInViewProps) {
  const customVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration,
        delay,
        ease: 'easeOut',
      },
    },
  };

  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once, amount: 0.3 }}
      variants={customVariants}
    >
      {children}
    </motion.div>
  );
}
