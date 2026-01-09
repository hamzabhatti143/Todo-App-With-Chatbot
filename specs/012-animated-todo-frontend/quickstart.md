# Quickstart Guide: Animated Todo Frontend

**Feature**: 012-animated-todo-frontend
**Date**: 2026-01-02
**Purpose**: Developer setup and implementation guide

---

## Prerequisites

Before implementing this feature, ensure:

- [x] Backend API is running on `http://localhost:8000`
- [x] Database is set up with users and tasks tables
- [x] Authentication endpoints (`/api/auth/register`, `/api/auth/login`) are functional
- [x] Task CRUD endpoints are functional
- [x] Node.js 18+ is installed
- [x] npm or yarn is installed

---

## Phase 1: Dependency Installation

### Step 1: Install Animation Libraries

```bash
cd frontend
npm install framer-motion@^11.0.0
```

### Step 2: Install UI Component Libraries

```bash
npm install @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu \
  @radix-ui/react-checkbox \
  @radix-ui/react-tabs \
  @radix-ui/react-avatar
```

### Step 3: Install Icon Library

```bash
npm install lucide-react@^0.460.0
```

### Step 4: Install Utility Libraries

```bash
npm install clsx tailwind-merge
npm install --save-dev @types/node
```

### Verify Installation

```bash
npm list framer-motion @radix-ui/react-dialog lucide-react
```

Expected output:
```
frontend@0.1.0
├── framer-motion@11.0.0
├── @radix-ui/react-dialog@1.x.x
└── lucide-react@0.460.0
```

---

## Phase 2: Tailwind Configuration

### Step 1: Update `tailwind.config.ts`

```typescript
// frontend/tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'glass-light': 'rgba(255, 255, 255, 0.7)',
        'glass-dark': 'rgba(17, 24, 39, 0.7)',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'shake': 'shake 0.5s ease-in-out',
        'draw': 'draw 0.6s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'spin': 'spin 1s linear infinite',
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
        spin: {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### Step 2: Add Glassmorphism Utilities to `globals.css`

```css
/* frontend/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .glass-card {
    @apply bg-white/70 dark:bg-gray-900/70 backdrop-blur-lg border border-white/20 dark:border-gray-700/30 shadow-xl;
  }

  .glass-navbar {
    @apply bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-white/20 dark:border-gray-700/30;
  }

  .glass-button {
    @apply bg-white/30 dark:bg-gray-800/30 backdrop-blur-sm border border-white/40 dark:border-gray-700/40;
  }
}

/* Smooth theme transition */
html {
  transition: background-color 300ms ease-in-out, color 300ms ease-in-out;
}

/* Ensure animations respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Phase 3: Create Core Utilities

### Step 1: Create `lib/utils.ts`

```typescript
// frontend/lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge Tailwind classes with proper precedence
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Format ISO date string to readable format
 */
export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

/**
 * Format ISO date string to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date: string): string {
  const now = new Date();
  const past = new Date(date);
  const diffMs = now.getTime() - past.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  return formatDate(date);
}

/**
 * Truncate text to specified length with ellipsis
 */
export function truncate(text: string, length: number): string {
  return text.length > length ? text.slice(0, length) + '...' : text;
}

/**
 * Debounce function execution
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
```

### Step 2: Create `lib/animations.ts`

```typescript
// frontend/lib/animations.ts
import { Variants } from 'framer-motion';

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
};

export const slideUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut' },
  },
};

export const slideDown: Variants = {
  hidden: { opacity: 0, y: -20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut' },
  },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
};

export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
};

export const staggerItem: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut' },
  },
};

export const hoverLift = {
  rest: { y: 0, scale: 1, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  hover: {
    y: -4,
    scale: 1.02,
    boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
    transition: { duration: 0.2, ease: 'easeOut' },
  },
};

export const tapScale = {
  tap: { scale: 0.98 },
};
```

### Step 3: Create Custom Hooks Directory

```bash
mkdir -p frontend/lib/hooks
```

---

## Phase 4: Implementation Order

Follow this order to build the feature systematically:

### Phase 4.1: UI Primitives (Foundation)

1. **Button** (`components/ui/button.tsx`)
   - Variants: primary, secondary, ghost, danger
   - States: loading, disabled
   - Animations: hover, tap

2. **Input** (`components/ui/input.tsx`)
   - Floating label animation
   - Focus glow effect
   - Error shake animation

3. **Card** (`components/ui/card.tsx`)
   - Glassmorphism variant
   - Hover lift effect

4. **Checkbox** (`components/ui/checkbox.tsx`)
   - Checkmark draw animation
   - Box scale on check

5. **Dialog** (`components/ui/dialog.tsx`)
   - Modal with backdrop
   - Scale in animation (desktop)
   - Bottom sheet (mobile)

6. **Dropdown** (`components/ui/dropdown.tsx`)
   - Fade + slide down
   - Item hover effect

7. **Tabs** (`components/ui/tabs.tsx`)
   - Indicator slide animation
   - Content fade transition

8. **Avatar** (`components/ui/avatar.tsx`)
   - Image fade in
   - Fallback initials

### Phase 4.2: Layout Components

9. **Container** (`components/layout/container.tsx`)
10. **Navbar** (`components/layout/navbar.tsx`)
11. **Sidebar** (`components/layout/sidebar.tsx`)

### Phase 4.3: Animation Wrappers

12. **FadeIn** (`components/animations/fade-in.tsx`)
13. **SlideUp** (`components/animations/slide-up.tsx`)
14. **StaggerChildren** (`components/animations/stagger-children.tsx`)
15. **CheckmarkDraw** (`components/animations/checkmark-draw.tsx`)

### Phase 4.4: Auth Components

16. **PasswordStrength** (`components/auth/password-strength.tsx`)
17. **SignInForm** (`components/auth/signin-form.tsx`)
18. **SignUpForm** (`components/auth/signup-form.tsx`)

### Phase 4.5: Task Components

19. **TaskSearch** (`components/tasks/task-search.tsx`)
20. **TaskFilters** (`components/tasks/task-filters.tsx`)
21. **TaskEmptyState** (`components/tasks/task-empty-state.tsx`)
22. **TaskCard** (`components/tasks/task-card.tsx`)
23. **TaskList** (`components/tasks/task-list.tsx`)
24. **TaskForm** (`components/tasks/task-form.tsx`)

### Phase 4.6: Custom Hooks

25. **useTheme** (`lib/hooks/use-theme.ts`)
26. **useMediaQuery** (`lib/hooks/use-media-query.ts`)
27. **useTasks** (`lib/hooks/use-tasks.ts`)

### Phase 4.7: Pages

28. **Sign In Page** (`app/(auth)/signin/page.tsx`)
29. **Sign Up Page** (`app/(auth)/signup/page.tsx`)
30. **Dashboard Layout** (`app/(dashboard)/layout.tsx`)
31. **Dashboard Page** (`app/(dashboard)/page.tsx`)
32. **Root Layout** (`app/layout.tsx`)

---

## Phase 5: Testing Checklist

After implementation, verify:

### Functional Testing

- [ ] User can sign up with validation
- [ ] User can sign in with credentials
- [ ] User can create tasks
- [ ] User can view task list
- [ ] User can edit tasks
- [ ] User can delete tasks
- [ ] User can mark tasks as complete
- [ ] User can filter tasks (All, Active, Completed)
- [ ] User can search tasks
- [ ] User can toggle dark mode
- [ ] User can logout

### Animation Testing

- [ ] All animations run at 60fps
- [ ] Reduced motion is respected
- [ ] No janky transitions
- [ ] Staggered list animations work
- [ ] Modal animations are smooth
- [ ] Checkbox draw animation completes
- [ ] Hover effects are responsive
- [ ] Form validation shake works
- [ ] Success animations display correctly
- [ ] Delete animations complete before removal

### Responsive Testing

- [ ] Mobile (< 640px): Single column layout
- [ ] Tablet (640-1024px): Two column layout
- [ ] Desktop (> 1024px): Three column layout + sidebar
- [ ] Touch targets are 44x44px minimum
- [ ] Swipe gestures work on mobile
- [ ] Bottom sheet appears on mobile modals

### Accessibility Testing

- [ ] All interactive elements keyboard accessible
- [ ] Focus visible states are clear
- [ ] ARIA labels present on icon buttons
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Screen reader announces state changes
- [ ] Form errors are announced
- [ ] Modal focus trap works

### Performance Testing

- [ ] Initial bundle < 500KB
- [ ] Time to Interactive < 3s
- [ ] Largest Contentful Paint < 2.5s
- [ ] No console errors or warnings
- [ ] API calls include auth token
- [ ] Loading states display correctly
- [ ] Error handling works gracefully

---

## Phase 6: Common Issues & Solutions

### Issue: Framer Motion Layout Shift

**Problem**: Content jumps when animating
**Solution**: Wrap changing elements in `<motion.div layout>`

```tsx
<motion.div layout>
  {/* Content that changes size/position */}
</motion.div>
```

### Issue: Backdrop Filter Not Working

**Problem**: Glassmorphism not visible
**Solution**: Check browser support, provide fallback

```css
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
}

@supports not (backdrop-filter: blur(12px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.95); /* Solid fallback */
  }
}
```

### Issue: Animations Not Respecting Reduced Motion

**Problem**: Animations still play with reduced motion enabled
**Solution**: Use `useReducedMotion` hook

```tsx
import { useReducedMotion } from 'framer-motion';

function Component() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ y: shouldReduceMotion ? 0 : -20 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    />
  );
}
```

### Issue: Exit Animations Not Playing

**Problem**: Component disappears immediately
**Solution**: Wrap with `<AnimatePresence>`

```tsx
<AnimatePresence>
  {show && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

### Issue: TypeScript Errors with Radix UI

**Problem**: Type mismatches with `asChild` prop
**Solution**: Install `@types/react` and update imports

```bash
npm install --save-dev @types/react@latest
```

---

## Phase 7: Development Commands

### Start Development Server

```bash
cd frontend
npm run dev
```

Access at: `http://localhost:3000`

### Run Type Checking

```bash
npx tsc --noEmit
```

### Run Linting

```bash
npm run lint
```

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run start
```

---

## Phase 8: Environment Variables

Create `.env.local` in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

Ensure `BETTER_AUTH_SECRET` matches backend secret.

---

## Component Implementation Example

### Example: Creating the Button Component

```tsx
// frontend/components/ui/button.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  fullWidth = false,
  children,
  onClick,
  type = 'button',
  className,
}: ButtonProps) {
  const baseStyles = 'rounded-lg font-medium transition-colors focus-visible:ring-2 focus-visible:ring-offset-2';

  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus-visible:ring-gray-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        fullWidth && 'w-full',
        (disabled || loading) && 'opacity-50 cursor-not-allowed',
        className
      )}
    >
      {loading ? (
        <motion.div
          className="h-5 w-5 border-2 border-current border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
      ) : (
        children
      )}
    </motion.button>
  );
}
```

---

## Next Steps

After completing this quickstart:

1. Run `/sp.tasks` to generate implementation tasks
2. Use `@nextjs-frontend-dev` agent for component implementation
3. Test each component as you build
4. Use `@code-reviewer` for quality review
5. Update documentation as needed

---

**Quickstart Guide Complete**: All setup instructions, implementation order, and examples provided.
