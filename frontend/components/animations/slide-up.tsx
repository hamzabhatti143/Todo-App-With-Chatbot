/**
 * SlideUp Animation Wrapper
 *
 * Wraps children in a slide-up animation with configurable delay and distance.
 * Uses Framer Motion for smooth entrance animations.
 */

'use client';

import React from 'react';
import { motion, Variants } from 'framer-motion';

interface SlideUpProps {
  children: React.ReactNode;
  delay?: number;
  distance?: number;
  duration?: number;
  className?: string;
}

export function SlideUp({
  children,
  delay = 0,
  distance = 20,
  duration = 0.4,
  className,
}: SlideUpProps) {
  const variants: Variants = {
    hidden: {
      opacity: 0,
      y: distance,
    },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration,
        delay,
        ease: 'easeOut',
      },
    },
    exit: {
      opacity: 0,
      y: distance,
      transition: {
        duration: duration * 0.75,
        ease: 'easeIn',
      },
    },
  };

  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      exit="exit"
      variants={variants}
    >
      {children}
    </motion.div>
  );
}

/**
 * SlideUpView - Only animates when scrolled into view
 */
interface SlideUpViewProps extends SlideUpProps {
  once?: boolean;
}

export function SlideUpView({
  children,
  delay = 0,
  distance = 20,
  duration = 0.4,
  once = true,
  className,
}: SlideUpViewProps) {
  const variants: Variants = {
    hidden: {
      opacity: 0,
      y: distance,
    },
    visible: {
      opacity: 1,
      y: 0,
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
      variants={variants}
    >
      {children}
    </motion.div>
  );
}
