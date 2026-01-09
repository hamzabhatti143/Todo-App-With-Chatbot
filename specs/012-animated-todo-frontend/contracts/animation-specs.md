# Animation Specifications

**Feature**: 012-animated-todo-frontend
**Date**: 2026-01-02
**Purpose**: Define all animation behaviors, timing, and motion patterns

---

## Animation Principles

### Core Guidelines

1. **Performance First**: Only animate `transform` and `opacity` (GPU-accelerated properties)
2. **Respect User Preferences**: Honor `prefers-reduced-motion` media query
3. **Subtle & Purposeful**: Animations should enhance UX, not distract
4. **Consistent Timing**: Use standardized durations and easing functions
5. **60fps Target**: All animations must maintain 60fps on modern devices

---

## Animation Timing Standards

### Duration Guidelines

```typescript
export const ANIMATION_DURATIONS = {
  instant: 0,         // No animation (reduced motion)
  fastest: 100,       // Micro-interactions (hover feedback)
  fast: 200,          // Quick transitions (button press)
  normal: 300,        // Standard animations (fade, slide)
  slow: 400,          // Deliberate animations (modal open)
  slowest: 600,       // Emphasis animations (checkmark draw)
} as const;
```

### Easing Functions

```typescript
export const ANIMATION_EASINGS = {
  easeIn: [0.4, 0, 1, 1],           // Accelerating
  easeOut: [0, 0, 0.2, 1],          // Decelerating (default for most)
  easeInOut: [0.4, 0, 0.2, 1],      // Smooth start and end
  spring: { type: 'spring', stiffness: 300, damping: 25 }, // Natural bounce
} as const;
```

---

## Component-Specific Animations

### 1. Button Animations

#### Hover State
```typescript
const buttonHover = {
  scale: 1.02,
  transition: { duration: 0.2, ease: ANIMATION_EASINGS.easeOut }
};
```

#### Active/Tap State
```typescript
const buttonTap = {
  scale: 0.98,
  transition: { duration: 0.1 }
};
```

#### Loading State
```typescript
const buttonLoading = {
  opacity: 0.6,
  transition: { duration: 0.2 }
};

// Spinner rotation
const spinnerRotate = {
  rotate: 360,
  transition: {
    duration: 1,
    repeat: Infinity,
    ease: 'linear'
  }
};
```

**Implementation**:
```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.2 }}
>
  {loading ? <Spinner /> : children}
</motion.button>
```

---

### 2. Input Animations

#### Floating Label
```typescript
const labelFloat = {
  unfocused: {
    y: 0,
    scale: 1,
    color: 'rgb(107, 114, 128)', // gray-500
  },
  focused: {
    y: -24,
    scale: 0.875,
    color: 'rgb(59, 130, 246)', // blue-500
    transition: { duration: 0.2, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Focus Glow
```typescript
const focusGlow = {
  boxShadow: [
    '0 0 0 0 rgba(59, 130, 246, 0)',
    '0 0 0 4px rgba(59, 130, 246, 0.1)',
  ],
  transition: { duration: 0.2 }
};
```

#### Error Shake
```typescript
const errorShake = {
  x: [0, -4, 4, -4, 4, 0],
  transition: { duration: 0.5, ease: ANIMATION_EASINGS.easeInOut }
};
```

**Implementation**:
```tsx
<motion.div animate={hasError ? errorShake : {}}>
  <motion.label
    animate={isFocused || hasValue ? 'focused' : 'unfocused'}
    variants={labelFloat}
  >
    {label}
  </motion.label>
  <input onFocus={() => setFocused(true)} onBlur={() => setFocused(false)} />
</motion.div>
```

---

### 3. Card Animations

#### Hover Lift
```typescript
const cardLift = {
  rest: {
    y: 0,
    scale: 1,
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  hover: {
    y: -4,
    scale: 1.02,
    boxShadow: '0 12px 24px rgba(0, 0, 0, 0.15)',
    transition: { duration: 0.2, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Glassmorphism Blur
```css
/* Applied via Tailwind */
.glass-card {
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.7);
  transition: backdrop-filter 0.3s ease;
}

.glass-card:hover {
  backdrop-filter: blur(16px);
}
```

**Implementation**:
```tsx
<motion.div
  className="glass-card"
  initial="rest"
  whileHover="hover"
  variants={cardLift}
>
  {children}
</motion.div>
```

---

### 4. Checkbox Animations

#### Check Animation (SVG Path Draw)
```typescript
const checkmarkDraw = {
  hidden: {
    pathLength: 0,
    opacity: 0,
  },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: {
      pathLength: { duration: 0.6, ease: ANIMATION_EASINGS.easeOut },
      opacity: { duration: 0.2 }
    }
  }
};
```

#### Box Scale
```typescript
const checkboxScale = {
  unchecked: { scale: 1 },
  checked: {
    scale: [1, 1.2, 1],
    transition: { duration: 0.3, ease: ANIMATION_EASINGS.spring }
  }
};
```

**Implementation**:
```tsx
<motion.div
  animate={checked ? 'checked' : 'unchecked'}
  variants={checkboxScale}
>
  <svg>
    <motion.path
      d="M5 12l5 5L20 7"
      initial="hidden"
      animate={checked ? 'visible' : 'hidden'}
      variants={checkmarkDraw}
    />
  </svg>
</motion.div>
```

---

### 5. Modal/Dialog Animations

#### Backdrop Fade
```typescript
const backdropFade = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Content Scale In (Desktop)
```typescript
const modalScale = {
  hidden: {
    opacity: 0,
    scale: 0.95,
    y: '-48%', // Slightly above center
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: '-50%', // Perfect center
    transition: { duration: 0.3, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Bottom Sheet Slide (Mobile)
```typescript
const bottomSheet = {
  hidden: {
    y: '100%',
    opacity: 0,
  },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.4, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

**Implementation**:
```tsx
<AnimatePresence>
  {open && (
    <>
      <motion.div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        initial="hidden"
        animate="visible"
        exit="hidden"
        variants={backdropFade}
      />
      <motion.div
        className="modal-content"
        initial="hidden"
        animate="visible"
        exit="hidden"
        variants={isMobile ? bottomSheet : modalScale}
      >
        {children}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

---

### 6. Dropdown Menu Animations

#### Menu Fade + Slide Down
```typescript
const dropdownMenu = {
  hidden: {
    opacity: 0,
    y: -10,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.2,
      ease: ANIMATION_EASINGS.easeOut
    }
  }
};
```

#### Item Hover
```typescript
const menuItemHover = {
  backgroundColor: 'rgba(59, 130, 246, 0.1)',
  x: 4,
  transition: { duration: 0.15 }
};
```

**Implementation**:
```tsx
<AnimatePresence>
  {open && (
    <motion.div
      initial="hidden"
      animate="visible"
      exit="hidden"
      variants={dropdownMenu}
    >
      {items.map(item => (
        <motion.div
          key={item.value}
          whileHover={menuItemHover}
        >
          {item.label}
        </motion.div>
      ))}
    </motion.div>
  )}
</AnimatePresence>
```

---

### 7. Tabs Animations

#### Indicator Slide
```typescript
const tabIndicator = {
  layout: true, // Enable layout animation
  transition: {
    type: 'spring',
    stiffness: 300,
    damping: 30
  }
};
```

#### Content Fade
```typescript
const tabContent = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.3, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

**Implementation**:
```tsx
<div className="relative">
  {tabs.map(tab => (
    <button key={tab.value} onClick={() => onChange(tab.value)}>
      {tab.label}
      {value === tab.value && (
        <motion.div
          layoutId="tab-indicator"
          className="absolute bottom-0 h-0.5 bg-blue-500"
          transition={tabIndicator.transition}
        />
      )}
    </button>
  ))}
</div>

<AnimatePresence mode="wait">
  <motion.div
    key={value}
    initial="hidden"
    animate="visible"
    exit="hidden"
    variants={tabContent}
  >
    {/* Tab content */}
  </motion.div>
</AnimatePresence>
```

---

### 8. Task Card Animations

#### Entry Animation (Staggered)
```typescript
const taskCardEntry = {
  hidden: {
    opacity: 0,
    y: 20,
    scale: 0.95,
  },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      delay: i * 0.1, // Stagger delay
      duration: 0.4,
      ease: ANIMATION_EASINGS.easeOut
    }
  })
};
```

#### Completion Animation
```typescript
const taskComplete = {
  strikethrough: {
    scaleX: [0, 1],
    originX: 0,
    transition: { duration: 0.5, ease: ANIMATION_EASINGS.easeOut }
  },
  fade: {
    opacity: [1, 0.6],
    transition: { duration: 0.3 }
  }
};
```

#### Delete Animation
```typescript
const taskDelete = {
  opacity: 0,
  x: -100,
  scale: 0.8,
  transition: { duration: 0.3, ease: ANIMATION_EASINGS.easeIn }
};
```

#### Hover Actions Reveal
```typescript
const taskActionsReveal = {
  hidden: { opacity: 0, x: 10 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.2, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

**Implementation**:
```tsx
<motion.div
  custom={index}
  initial="hidden"
  animate="visible"
  exit={isDeleting ? taskDelete : undefined}
  variants={taskCardEntry}
  whileHover="hover"
>
  <motion.h3
    style={{
      textDecoration: completed ? 'line-through' : 'none',
    }}
    animate={completed ? 'strikethrough' : {}}
  >
    {title}
  </motion.h3>

  <motion.div
    initial="hidden"
    variants={taskActionsReveal}
    animate="visible"
  >
    <Button onClick={handleEdit}>Edit</Button>
    <Button onClick={handleDelete}>Delete</Button>
  </motion.div>
</motion.div>
```

---

### 9. List Animations

#### Staggered Children
```typescript
const staggerContainer = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
};

const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Layout Shift (Auto-animate on reorder)
```typescript
<motion.div layout transition={{ duration: 0.3, ease: ANIMATION_EASINGS.easeOut }}>
  {/* Content that changes position */}
</motion.div>
```

**Implementation**:
```tsx
<motion.ul
  initial="hidden"
  animate="visible"
  variants={staggerContainer}
>
  <AnimatePresence>
    {tasks.map((task, i) => (
      <motion.li
        key={task.id}
        layout
        variants={staggerItem}
        exit={{ opacity: 0, x: -100 }}
      >
        <TaskCard task={task} />
      </motion.li>
    ))}
  </AnimatePresence>
</motion.ul>
```

---

### 10. Page Transitions

#### Fade In On Load
```typescript
const pageTransition = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.4, ease: ANIMATION_EASINGS.easeOut }
  }
};
```

#### Slide Up Content
```typescript
const contentSlide = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: ANIMATION_EASINGS.easeOut,
      staggerChildren: 0.1
    }
  }
};
```

**Implementation**:
```tsx
<motion.div
  initial="hidden"
  animate="visible"
  variants={pageTransition}
>
  <motion.div variants={contentSlide}>
    <h1>Page Title</h1>
    <TaskFilters />
    <TaskList />
  </motion.div>
</motion.div>
```

---

### 11. Loading States

#### Skeleton Pulse
```typescript
const skeletonPulse = {
  opacity: [0.5, 1, 0.5],
  transition: {
    duration: 1.5,
    repeat: Infinity,
    ease: 'easeInOut'
  }
};
```

#### Spinner Rotation
```typescript
const spinnerRotate = {
  rotate: 360,
  transition: {
    duration: 1,
    repeat: Infinity,
    ease: 'linear'
  }
};
```

**Implementation**:
```tsx
<motion.div
  className="skeleton h-4 bg-gray-200 rounded"
  animate={skeletonPulse}
/>

<motion.div
  animate={spinnerRotate}
>
  <LoaderIcon />
</motion.div>
```

---

### 12. Success/Error Feedback

#### Success Checkmark
```typescript
const successCheckmark = {
  scale: [0, 1.2, 1],
  opacity: [0, 1, 1],
  transition: {
    duration: 0.6,
    ease: ANIMATION_EASINGS.spring
  }
};
```

#### Error Shake
```typescript
const errorShake = {
  x: [0, -10, 10, -10, 10, 0],
  transition: {
    duration: 0.5,
    ease: ANIMATION_EASINGS.easeInOut
  }
};
```

**Implementation**:
```tsx
{success && (
  <motion.div animate={successCheckmark}>
    <CheckCircle className="text-green-500" />
  </motion.div>
)}

{error && (
  <motion.div animate={errorShake}>
    <AlertCircle className="text-red-500" />
  </motion.div>
)}
```

---

## Reduced Motion Support

### Media Query Hook

```typescript
// lib/hooks/use-reduced-motion.ts
import { useReducedMotion } from 'framer-motion';

export function useAnimationConfig() {
  const shouldReduceMotion = useReducedMotion();

  return {
    duration: shouldReduceMotion ? 0 : undefined,
    disabled: shouldReduceMotion,
  };
}
```

### Conditional Animations

```typescript
function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  const variants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: shouldReduceMotion ? 0 : 0.3 }
    }
  };

  return <motion.div variants={variants} />;
}
```

---

## Performance Optimization

### GPU Acceleration

```typescript
// Always set will-change during animation
<motion.div
  style={{ willChange: 'transform' }}
  animate={{ scale: 1.1 }}
  onAnimationComplete={() => {
    // Remove will-change after animation
  }}
/>
```

### Layout Animations

```typescript
// Use layout prop for size/position changes
<motion.div layout>
  {/* Content that changes size */}
</motion.div>
```

### Exit Animations

```typescript
// Wrap with AnimatePresence for unmount animations
<AnimatePresence mode="wait">
  {show && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

---

## Animation Testing Checklist

- [ ] All animations run at 60fps on target devices
- [ ] Reduced motion preference is respected
- [ ] No layout thrashing (no animating width/height directly)
- [ ] Exit animations complete before unmount
- [ ] Staggered animations don't block UI
- [ ] Loading states have smooth transitions
- [ ] Form validation feedback is immediate
- [ ] Success/error animations are clear and brief
- [ ] Mobile swipe gestures work smoothly
- [ ] Dark mode transitions are smooth (300ms)

---

**Animation Specifications Complete**: All component animations, timing, and motion patterns defined.
