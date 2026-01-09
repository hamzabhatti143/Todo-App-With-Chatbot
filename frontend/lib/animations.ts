/**
 * Animation Variants
 *
 * Framer Motion animation configurations for consistent animations across the app.
 * All animations use GPU-accelerated properties (transform, opacity) for performance.
 */

import { Variants } from 'framer-motion';

/**
 * Fade in animation
 * Use for: General element entrance
 */
export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.2,
      ease: 'easeIn',
    },
  },
};

/**
 * Slide up animation
 * Use for: Bottom-up reveals (modals, cards, notifications)
 */
export const slideUp: Variants = {
  hidden: {
    opacity: 0,
    y: 20
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: 20,
    transition: {
      duration: 0.3,
      ease: 'easeIn',
    },
  },
};

/**
 * Slide down animation
 * Use for: Top-down reveals (dropdowns, banners)
 */
export const slideDown: Variants = {
  hidden: {
    opacity: 0,
    y: -20
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.3,
      ease: 'easeIn',
    },
  },
};

/**
 * Scale in animation
 * Use for: Attention-grabbing elements (buttons, icons, success indicators)
 */
export const scaleIn: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.8
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.3,
      ease: [0.34, 1.56, 0.64, 1], // Spring-like easing
    },
  },
  exit: {
    opacity: 0,
    scale: 0.8,
    transition: {
      duration: 0.2,
      ease: 'easeIn',
    },
  },
};

/**
 * Stagger container animation
 * Use for: Parent container of list items or grid items
 */
export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      staggerChildren: 0.05,
      staggerDirection: -1,
    },
  },
};

/**
 * Stagger item animation
 * Use for: Child items in a staggered list (combine with staggerContainer)
 */
export const staggerItem: Variants = {
  hidden: {
    opacity: 0,
    y: 20
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    y: 10,
    transition: {
      duration: 0.2,
      ease: 'easeIn',
    },
  },
};

/**
 * Hover lift animation
 * Use for: Interactive cards and buttons
 * Apply with whileHover prop
 */
export const hoverLift = {
  scale: 1.02,
  y: -4,
  transition: {
    duration: 0.2,
    ease: 'easeOut',
  },
};

/**
 * Tap scale animation
 * Use for: Buttons and clickable elements
 * Apply with whileTap prop
 */
export const tapScale = {
  scale: 0.95,
  transition: {
    duration: 0.1,
    ease: 'easeInOut',
  },
};

/**
 * Shake animation
 * Use for: Error states, validation failures
 */
export const shake: Variants = {
  start: {
    x: [-4, 4, -4, 4, 0],
    transition: {
      duration: 0.5,
      ease: 'easeInOut',
    },
  },
};

/**
 * Draw animation for checkmark SVG paths
 * Use for: Checkbox completion animations
 */
export const draw: Variants = {
  hidden: {
    pathLength: 0,
    opacity: 0,
  },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: {
        duration: 0.6,
        ease: 'easeOut'
      },
      opacity: {
        duration: 0.2
      },
    },
  },
};

/**
 * Pulse glow animation
 * Use for: Loading states, active indicators
 */
export const pulseGlow: Variants = {
  pulse: {
    boxShadow: [
      '0 0 20px rgba(59, 130, 246, 0.5)',
      '0 0 40px rgba(59, 130, 246, 0.8)',
      '0 0 20px rgba(59, 130, 246, 0.5)',
    ],
    transition: {
      duration: 2,
      ease: 'easeInOut',
      repeat: Infinity,
    },
  },
};

/**
 * Rotate animation
 * Use for: Loading spinners, refresh icons
 */
export const rotate: Variants = {
  spin: {
    rotate: 360,
    transition: {
      duration: 1,
      ease: 'linear',
      repeat: Infinity,
    },
  },
};
