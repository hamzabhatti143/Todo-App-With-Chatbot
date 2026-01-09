# Research: Production-Ready Animated Todo Frontend

**Feature**: 012-animated-todo-frontend
**Date**: 2026-01-02
**Purpose**: Document technology research, best practices, and architectural decisions for animated frontend implementation

---

## Phase 0: Technology Research & Best Practices

### 1. Animation Library Selection

#### Decision: Framer Motion v11

**Rationale**:
- **Performance**: Built on Web Animations API with automatic GPU acceleration
- **Developer Experience**: Declarative API with React-first design
- **Features**: Built-in support for gestures, layout animations, and SVG path animations
- **Bundle Size**: ~30KB gzipped (tree-shakeable)
- **TypeScript Support**: Full type definitions included
- **Accessibility**: Automatic `prefers-reduced-motion` support via `useReducedMotion()` hook

**Alternatives Considered**:
- **React Spring**: More physics-based, but larger bundle and steeper learning curve
- **CSS Transitions**: Limited to simple animations, no gesture support
- **GSAP**: Powerful but not React-idiomatic and requires separate license for commercial use
- **Motion One**: Smaller bundle but less React integration and smaller ecosystem

**Best Practices**:
```typescript
// Use motion components with layout animations
import { motion } from 'framer-motion';

// Define animation variants for reusability
const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
};

// Use GPU-accelerated properties only (transform, opacity)
<motion.div
  initial="hidden"
  animate="visible"
  variants={fadeIn}
  style={{ willChange: 'transform, opacity' }} // Hint to browser
/>
```

---

### 2. UI Component Primitives

#### Decision: Radix UI v1

**Rationale**:
- **Accessibility**: WCAG-compliant with keyboard navigation and ARIA attributes
- **Headless**: No styles included, full Tailwind integration
- **Composition**: Composable primitives (Dialog, Dropdown, Tabs, Checkbox)
- **Focus Management**: Automatic focus trap and restoration
- **TypeScript**: Full type safety
- **Bundle Size**: Individual packages are small (~5-10KB each)

**Components to Use**:
- `@radix-ui/react-dialog` - Modals for task creation/editing
- `@radix-ui/react-dropdown-menu` - User menu, sort dropdown
- `@radix-ui/react-tabs` - Filter tabs (All, Active, Completed)
- `@radix-ui/react-checkbox` - Task completion checkboxes

**Alternatives Considered**:
- **Headless UI**: Good option but less comprehensive than Radix
- **React ARIA**: Too low-level, more boilerplate required
- **Shadcn UI**: Uses Radix under the hood, but we'll build our own variants for customization

**Best Practices**:
```typescript
// Wrap Radix primitives with custom styling
import * as Dialog from '@radix-ui/react-dialog';
import { motion } from 'framer-motion';

export function Modal({ children, ...props }) {
  return (
    <Dialog.Root {...props}>
      <Dialog.Portal>
        <Dialog.Overlay asChild>
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          />
        </Dialog.Overlay>
        <Dialog.Content asChild>
          <motion.div
            className="fixed left-1/2 top-1/2 glass-card"
            initial={{ x: '-50%', y: '-48%', opacity: 0, scale: 0.95 }}
            animate={{ x: '-50%', y: '-50%', opacity: 1, scale: 1 }}
          >
            {children}
          </motion.div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

### 3. Icon System

#### Decision: Lucide React v0.460

**Rationale**:
- **Consistency**: Fork of Feather Icons with more icons (1000+)
- **React Optimized**: Individual icon imports for tree-shaking
- **Customizable**: Stroke width, size, color via props
- **Bundle Size**: ~1KB per icon (tree-shakeable)
- **TypeScript Support**: Full type definitions

**Icons to Use**:
- `CheckCircle2`, `Circle` - Task completion
- `Plus`, `X` - Add/close actions
- `Edit2`, `Trash2` - Task editing/deletion
- `Search`, `Filter` - Search and filtering
- `Sun`, `Moon` - Dark mode toggle
- `Menu`, `ChevronDown` - Navigation

**Alternatives Considered**:
- **Heroicons**: Smaller set, similar quality
- **React Icons**: Larger bundle, multiple icon sets
- **Font Awesome**: Too heavy, not React-native

**Best Practices**:
```typescript
import { CheckCircle2, Circle } from 'lucide-react';

// Use consistent sizing across application
<CheckCircle2
  className="h-5 w-5 text-green-500"
  strokeWidth={2}
  aria-hidden="true" // Icons are decorative
/>
```

---

### 4. Tailwind CSS Custom Configuration

#### Decision: Tailwind CSS v4 with Custom Animations

**Rationale**:
- **Performance**: JIT compiler generates minimal CSS
- **Glassmorphism**: Custom backdrop-filter utilities
- **Custom Animations**: Extend with draw, shake, slide animations
- **Dark Mode**: Class-based strategy for instant toggle

**Custom Configuration**:
```typescript
// tailwind.config.ts
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Glassmorphism colors
        'glass-light': 'rgba(255, 255, 255, 0.7)',
        'glass-dark': 'rgba(17, 24, 39, 0.7)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'shake': 'shake 0.5s ease-in-out',
        'draw': 'draw 0.6s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        slideUp: {
          from: { transform: 'translateY(20px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          from: { transform: 'translateY(-20px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-4px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(4px)' },
        },
        draw: {
          from: { strokeDashoffset: '100' },
          to: { strokeDashoffset: '0' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' },
          '50%': { boxShadow: '0 0 40px rgba(59, 130, 246, 0.8)' },
        },
      },
    },
  },
  plugins: [],
};
```

**Glassmorphism Utilities**:
```css
/* globals.css */
@layer utilities {
  .glass-card {
    @apply bg-white/70 dark:bg-gray-900/70 backdrop-blur-lg border border-white/20 dark:border-gray-700/30 shadow-xl;
  }

  .glass-navbar {
    @apply bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-white/20 dark:border-gray-700/30;
  }
}
```

---

### 5. Animation Performance Optimization

#### Best Practices

**GPU-Accelerated Properties**:
- ✅ **Use**: `transform` (translate, scale, rotate), `opacity`
- ❌ **Avoid**: `width`, `height`, `top`, `left`, `margin`, `padding`

**Performance Tips**:
```typescript
// 1. Use will-change sparingly (only during animation)
<motion.div
  style={{ willChange: 'transform' }}
  animate={{ scale: 1.05 }}
  onAnimationComplete={() => {
    // Remove will-change after animation
  }}
/>

// 2. Use layout animations for size changes
<motion.div layout>
  {/* Content that changes size */}
</motion.div>

// 3. Debounce expensive operations
import { useDebouncedCallback } from 'use-debounce';

const handleSearch = useDebouncedCallback((query) => {
  filterTasks(query);
}, 300);

// 4. Virtualize long lists
import { useVirtualizer } from '@tanstack/react-virtual';
```

**Reduced Motion Support**:
```typescript
import { useReducedMotion } from 'framer-motion';

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

### 6. Form Validation

#### Decision: Zod v3.24

**Rationale**:
- **Type Inference**: TypeScript types automatically inferred from schemas
- **Composable**: Reusable schemas for task/auth validation
- **Error Messages**: Customizable, user-friendly error messages
- **Integration**: Works seamlessly with React Hook Form (if needed)

**Schemas**:
```typescript
// types/task.ts
import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less'),
  description: z.string()
    .max(1000, 'Description must be 1000 characters or less')
    .optional(),
});

export type TaskInput = z.infer<typeof taskSchema>;

// Usage in component
const handleSubmit = (data: unknown) => {
  const result = taskSchema.safeParse(data);
  if (!result.success) {
    setErrors(result.error.flatten().fieldErrors);
    return;
  }
  // result.data is now type-safe TaskInput
  createTask(result.data);
};
```

---

### 7. Dark Mode Implementation

#### Decision: Next.js + CSS Variables + Class Strategy

**Rationale**:
- **Instant Toggle**: No flash of incorrect theme
- **Persistence**: Store preference in localStorage
- **System Preference**: Respect `prefers-color-scheme`
- **Smooth Transition**: CSS transition on theme toggle

**Implementation**:
```typescript
// lib/hooks/use-theme.ts
import { useEffect, useState } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme');
    const system = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(stored as any || (system ? 'dark' : 'light'));
  }, []);

  const toggleTheme = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    localStorage.setItem('theme', next);
    document.documentElement.classList.toggle('dark', next === 'dark');
  };

  return { theme, toggleTheme };
}

// globals.css - Smooth theme transition
html {
  transition: background-color 300ms ease-in-out, color 300ms ease-in-out;
}
```

---

### 8. Responsive Design Strategy

#### Decision: Mobile-First with Tailwind Breakpoints

**Breakpoints**:
- **Mobile**: < 640px (default, no prefix)
- **Tablet**: 640px - 1024px (`sm:` and `md:`)
- **Desktop**: > 1024px (`lg:` and `xl:`)

**Layout Patterns**:
```typescript
// Task grid responsive columns
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {tasks.map(task => <TaskCard key={task.id} task={task} />)}
</div>

// Sidebar visibility
<aside className="hidden lg:block lg:w-64">
  <Sidebar />
</aside>

// Mobile bottom sheet vs desktop modal
const isMobile = useMediaQuery('(max-width: 640px)');

return isMobile ? (
  <BottomSheet>{content}</BottomSheet>
) : (
  <Dialog>{content}</Dialog>
);
```

---

### 9. Accessibility Patterns

#### WCAG AA Compliance

**Color Contrast**:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3.0:1 minimum
- UI components: 3.0:1 minimum

**Keyboard Navigation**:
```typescript
// Focus visible states
<button className="focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
  Click me
</button>

// Skip to main content
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

// Trap focus in modals (Radix handles this automatically)
```

**ARIA Labels**:
```typescript
<button aria-label="Delete task" onClick={handleDelete}>
  <Trash2 aria-hidden="true" />
</button>

<input
  aria-describedby="email-error"
  aria-invalid={!!errors.email}
/>
{errors.email && (
  <p id="email-error" role="alert">{errors.email}</p>
)}
```

---

### 10. State Management Strategy

#### Decision: React Hooks + Context (No External Library)

**Rationale**:
- **Simplicity**: Application state is not complex enough for Redux/Zustand
- **Server State**: Tasks fetched from API, not global state
- **Local State**: UI state (modals, filters) managed locally
- **Context**: Theme, auth state shared via context

**Patterns**:
```typescript
// Custom hook for task operations
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getTasks();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (input: TaskInput) => {
    const newTask = await api.createTask(input);
    setTasks(prev => [newTask, ...prev]); // Optimistic update
  };

  return { tasks, loading, error, fetchTasks, createTask };
}
```

---

## Summary of Technology Decisions

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| Animation | Framer Motion | ^11.0.0 | Best React integration, performance, DX |
| UI Primitives | Radix UI | ^1.0.0 | Accessibility, headless, composable |
| Icons | Lucide React | ^0.460.0 | Tree-shakeable, consistent, customizable |
| Styling | Tailwind CSS | ^4.0.0 | Utility-first, JIT, glassmorphism support |
| Validation | Zod | ^3.24.1 | Type inference, composable schemas |
| HTTP Client | Axios | ^1.7.9 | Existing, interceptors for auth |
| State | React Hooks | N/A | Sufficient for app complexity |
| Dark Mode | CSS Classes | N/A | Instant toggle, persistence |
| Responsive | Tailwind Breakpoints | N/A | Mobile-first, standard breakpoints |

---

## Key Architectural Decisions

### 1. Component Organization
- **UI Primitives** (`components/ui/`): Reusable, styled Radix wrappers
- **Feature Components** (`components/tasks/`, `components/auth/`): Domain-specific
- **Animation Wrappers** (`components/animations/`): Reusable motion components
- **Layout Components** (`components/layout/`): Navbar, sidebar, container

### 2. Animation Strategy
- **Define Variants Once**: Store in `lib/animations.ts` for consistency
- **GPU Acceleration**: Only animate `transform` and `opacity`
- **Reduced Motion**: Check `useReducedMotion()` for all animations
- **Performance Budget**: Max 16ms per frame (60fps)

### 3. Styling Approach
- **Tailwind Only**: No CSS modules, no inline styles
- **Custom Utilities**: Glassmorphism via `@layer utilities`
- **Dark Mode**: Class-based with CSS transitions
- **Responsive**: Mobile-first with Tailwind breakpoints

### 4. Accessibility First
- **Keyboard Navigation**: All interactions keyboard-accessible
- **ARIA Labels**: Descriptive labels on all interactive elements
- **Focus Management**: Radix primitives handle focus trapping
- **Color Contrast**: WCAG AA minimum (4.5:1 for text)
- **Reduced Motion**: Respect user preferences

---

## Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| Bundle Size | <500KB initial | Code-splitting, tree-shaking |
| Time to Interactive | <3s | Server Components, lazy loading |
| Animation FPS | 60fps | GPU-accelerated properties only |
| LCP | <2.5s | Image optimization, font preloading |
| CLS | <0.1 | Reserve space for dynamic content |

---

## Risk Mitigation

### Animation Performance
- **Risk**: Animations lag on older devices
- **Mitigation**: `useReducedMotion()`, performance monitoring, fallback to CSS

### Bundle Size
- **Risk**: Framer Motion and Radix UI increase bundle size
- **Mitigation**: Tree-shaking, code-splitting, lazy loading non-critical components

### Browser Compatibility
- **Risk**: `backdrop-filter` not supported in older browsers
- **Mitigation**: Progressive enhancement, fallback to solid background colors

### Accessibility
- **Risk**: Animations interfere with screen readers
- **Mitigation**: `aria-hidden` on decorative elements, test with NVDA/VoiceOver

---

**Research Complete**: All NEEDS CLARIFICATION items resolved. Ready for Phase 1 design.
