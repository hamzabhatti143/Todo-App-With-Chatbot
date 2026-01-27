/**
 * Floating 3D Animation Component
 *
 * Creates floating 3D elements with perspective transforms
 */

'use client';

import { motion } from 'framer-motion';
import { useReducedMotion } from 'framer-motion';

interface Floating3DProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  intensity?: 'low' | 'medium' | 'high';
  className?: string;
}

export function Floating3D({
  children,
  delay = 0,
  duration = 6,
  intensity = 'medium',
  className = ''
}: Floating3DProps) {
  const prefersReducedMotion = useReducedMotion();

  // Define intensity levels for 3D movement
  const intensityLevels = {
    low: { rotate: 5, translate: 10, scale: 0.02 },
    medium: { rotate: 10, translate: 20, scale: 0.05 },
    high: { rotate: 15, translate: 30, scale: 0.08 },
  };

  const { rotate, translate, scale } = intensityLevels[intensity];

  if (prefersReducedMotion) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
      animate={{
        rotateX: [0, rotate, -rotate, 0],
        rotateY: [0, -rotate, rotate, 0],
        rotateZ: [0, rotate / 2, -rotate / 2, 0],
        translateY: [0, -translate, 0],
        translateX: [0, translate / 2, -translate / 2, 0],
        scale: [1, 1 + scale, 1],
      }}
      transition={{
        duration,
        repeat: Infinity,
        ease: 'easeInOut',
        delay,
      }}
    >
      {children}
    </motion.div>
  );
}

/**
 * 3D Card Tilt Effect
 *
 * Card that tilts based on mouse position for 3D effect
 */

interface Card3DTiltProps {
  children: React.ReactNode;
  className?: string;
  maxTilt?: number;
}

export function Card3DTilt({
  children,
  className = '',
  maxTilt = 15
}: Card3DTiltProps) {
  const prefersReducedMotion = useReducedMotion();

  if (prefersReducedMotion) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
      whileHover={{
        scale: 1.05,
        rotateX: 0,
        rotateY: 0,
        transition: { duration: 0.2 },
      }}
      onHoverStart={(event) => {
        const card = event.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * maxTilt;
        const rotateY = ((centerX - x) / centerX) * maxTilt;

        // Apply rotation (this would need state management for full effect)
      }}
      whileTap={{ scale: 0.95 }}
    >
      <div style={{ transform: 'translateZ(50px)' }}>
        {children}
      </div>
    </motion.div>
  );
}

/**
 * 3D Rotating Cube
 *
 * Pure CSS 3D cube with rotating animation
 */

interface Cube3DProps {
  size?: number;
  colors?: string[];
  speed?: number;
}

export function Cube3D({
  size = 100,
  colors = [
    'from-blue-500 to-blue-600',
    'from-purple-500 to-purple-600',
    'from-pink-500 to-pink-600',
    'from-cyan-500 to-cyan-600',
    'from-green-500 to-green-600',
    'from-yellow-500 to-yellow-600',
  ],
  speed = 20
}: Cube3DProps) {
  const prefersReducedMotion = useReducedMotion();

  return (
    <div
      className="relative"
      style={{
        width: size,
        height: size,
        perspective: '1000px',
      }}
    >
      <motion.div
        className="relative w-full h-full"
        style={{
          transformStyle: 'preserve-3d',
        }}
        animate={!prefersReducedMotion ? {
          rotateX: 360,
          rotateY: 360,
        } : {}}
        transition={{
          duration: speed,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        {/* Front face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[0]} opacity-80`}
          style={{
            transform: `translateZ(${size / 2}px)`,
          }}
        />
        {/* Back face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[1]} opacity-80`}
          style={{
            transform: `translateZ(-${size / 2}px) rotateY(180deg)`,
          }}
        />
        {/* Right face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[2]} opacity-80`}
          style={{
            transform: `rotateY(90deg) translateZ(${size / 2}px)`,
          }}
        />
        {/* Left face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[3]} opacity-80`}
          style={{
            transform: `rotateY(-90deg) translateZ(${size / 2}px)`,
          }}
        />
        {/* Top face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[4]} opacity-80`}
          style={{
            transform: `rotateX(90deg) translateZ(${size / 2}px)`,
          }}
        />
        {/* Bottom face */}
        <div
          className={`absolute inset-0 bg-gradient-to-br ${colors[5]} opacity-80`}
          style={{
            transform: `rotateX(-90deg) translateZ(${size / 2}px)`,
          }}
        />
      </motion.div>
    </div>
  );
}

/**
 * 3D Sphere/Orb
 *
 * Rotating sphere with gradient and glow effect
 */

interface Sphere3DProps {
  size?: number;
  gradient?: string;
  speed?: number;
}

export function Sphere3D({
  size = 150,
  gradient = 'from-blue-400 via-purple-500 to-pink-500',
  speed = 10
}: Sphere3DProps) {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      className={`rounded-full bg-gradient-to-br ${gradient} relative`}
      style={{
        width: size,
        height: size,
        boxShadow: `
          0 0 ${size * 0.5}px ${size * 0.1}px rgba(139, 92, 246, 0.3),
          inset 0 0 ${size * 0.3}px ${size * 0.05}px rgba(255, 255, 255, 0.2)
        `,
      }}
      animate={!prefersReducedMotion ? {
        rotateY: 360,
        scale: [1, 1.05, 1],
      } : {}}
      transition={{
        rotateY: {
          duration: speed,
          repeat: Infinity,
          ease: 'linear',
        },
        scale: {
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        },
      }}
    >
      {/* Shine/highlight effect */}
      <div
        className="absolute top-[20%] left-[20%] w-[30%] h-[30%] rounded-full bg-white/40 blur-xl"
      />
    </motion.div>
  );
}

/**
 * Parallax 3D Layer
 *
 * Creates parallax effect with multiple 3D layers
 */

interface Parallax3DProps {
  children: React.ReactNode;
  depth?: number;
  className?: string;
}

export function Parallax3D({
  children,
  depth = 0.5,
  className = ''
}: Parallax3DProps) {
  const prefersReducedMotion = useReducedMotion();

  if (prefersReducedMotion) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      style={{
        transformStyle: 'preserve-3d',
      }}
      initial={{ y: 0 }}
      whileInView={{
        y: 0,
        transition: {
          duration: 0.8,
        }
      }}
      viewport={{ once: false, amount: 0.3 }}
      onViewportEnter={() => {
        // Parallax effect on scroll would be implemented here
      }}
    >
      <div style={{ transform: `translateZ(${depth * 100}px)` }}>
        {children}
      </div>
    </motion.div>
  );
}
