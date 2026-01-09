/**
 * StaggerChildren Animation Wrapper
 *
 * Wraps children in a staggered animation container.
 * Each child animates in sequence with a configurable stagger delay.
 */

'use client';

import React from 'react';
import { motion, Variants } from 'framer-motion';
import { staggerItem } from '@/lib/animations';

interface StaggerChildrenProps {
  children: React.ReactNode;
  staggerDelay?: number;
  delayChildren?: number;
  className?: string;
}

export function StaggerChildren({
  children,
  staggerDelay = 0.1,
  delayChildren = 0.1,
  className,
}: StaggerChildrenProps) {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay,
        delayChildren,
      },
    },
    exit: {
      opacity: 0,
      transition: {
        staggerChildren: staggerDelay * 0.5,
        staggerDirection: -1,
      },
    },
  };

  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      exit="exit"
      variants={containerVariants}
    >
      {children}
    </motion.div>
  );
}

/**
 * StaggerItem - Individual item to be used inside StaggerChildren
 */
interface StaggerItemProps {
  children: React.ReactNode;
  className?: string;
}

export function StaggerItem({ children, className }: StaggerItemProps) {
  return (
    <motion.div className={className} variants={staggerItem}>
      {children}
    </motion.div>
  );
}

/**
 * StaggerList - Convenience component for staggered lists
 */
interface StaggerListProps {
  items: React.ReactNode[];
  staggerDelay?: number;
  delayChildren?: number;
  className?: string;
  itemClassName?: string;
}

export function StaggerList({
  items,
  staggerDelay = 0.1,
  delayChildren = 0.1,
  className,
  itemClassName,
}: StaggerListProps) {
  return (
    <StaggerChildren staggerDelay={staggerDelay} delayChildren={delayChildren} className={className}>
      {items.map((item, index) => (
        <StaggerItem key={index} className={itemClassName}>
          {item}
        </StaggerItem>
      ))}
    </StaggerChildren>
  );
}
