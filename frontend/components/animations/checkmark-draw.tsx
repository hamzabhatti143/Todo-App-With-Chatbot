/**
 * CheckmarkDraw Animation Component
 *
 * SVG checkmark with path draw animation.
 * Smoothly animates the checkmark path from 0 to complete with onComplete callback.
 */

'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface CheckmarkDrawProps {
  size?: number;
  strokeWidth?: number;
  color?: string;
  duration?: number;
  delay?: number;
  onComplete?: () => void;
  className?: string;
}

export function CheckmarkDraw({
  size = 64,
  strokeWidth = 4,
  color = 'currentColor',
  duration = 0.6,
  delay = 0,
  onComplete,
  className,
}: CheckmarkDrawProps) {
  const variants = {
    hidden: {
      pathLength: 0,
      opacity: 0,
    },
    visible: {
      pathLength: 1,
      opacity: 1,
      transition: {
        pathLength: {
          duration,
          delay,
          ease: 'easeOut',
        },
        opacity: {
          duration: 0.2,
          delay,
        },
      },
    },
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cn('overflow-visible', className)}
    >
      <motion.path
        d="M 12 32 L 26 46 L 52 18"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        variants={variants}
        initial="hidden"
        animate="visible"
        onAnimationComplete={onComplete}
      />
    </svg>
  );
}

/**
 * CheckmarkCircleDraw - Checkmark with animated circle background
 */
interface CheckmarkCircleDrawProps extends CheckmarkDrawProps {
  circleColor?: string;
  fillCircle?: boolean;
}

export function CheckmarkCircleDraw({
  size = 64,
  strokeWidth = 4,
  color = 'white',
  circleColor = '#10b981',
  fillCircle = true,
  duration = 0.6,
  delay = 0,
  onComplete,
  className,
}: CheckmarkCircleDrawProps) {
  const circleVariants = {
    hidden: {
      scale: 0,
      opacity: 0,
    },
    visible: {
      scale: 1,
      opacity: 1,
      transition: {
        duration: 0.3,
        delay,
        ease: [0.34, 1.56, 0.64, 1], // Spring-like easing
      },
    },
  };

  const checkmarkVariants = {
    hidden: {
      pathLength: 0,
      opacity: 0,
    },
    visible: {
      pathLength: 1,
      opacity: 1,
      transition: {
        pathLength: {
          duration,
          delay: delay + 0.2,
          ease: 'easeOut',
        },
        opacity: {
          duration: 0.2,
          delay: delay + 0.2,
        },
      },
    },
  };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cn('overflow-visible', className)}
    >
      <motion.circle
        cx="32"
        cy="32"
        r="28"
        fill={fillCircle ? circleColor : 'none'}
        stroke={fillCircle ? 'none' : circleColor}
        strokeWidth={fillCircle ? 0 : strokeWidth}
        variants={circleVariants}
        initial="hidden"
        animate="visible"
      />
      <motion.path
        d="M 16 32 L 26 42 L 48 22"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        variants={checkmarkVariants}
        initial="hidden"
        animate="visible"
        onAnimationComplete={onComplete}
      />
    </svg>
  );
}

/**
 * SuccessCheckmark - Pre-configured checkmark with success colors
 */
interface SuccessCheckmarkProps {
  size?: number;
  onComplete?: () => void;
  className?: string;
}

export function SuccessCheckmark({ size = 64, onComplete, className }: SuccessCheckmarkProps) {
  return (
    <CheckmarkCircleDraw
      size={size}
      strokeWidth={4}
      color="white"
      circleColor="#10b981"
      fillCircle
      duration={0.6}
      delay={0}
      onComplete={onComplete}
      className={className}
    />
  );
}
