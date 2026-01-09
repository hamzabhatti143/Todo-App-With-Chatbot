# Data Model: Component Architecture & State Management

**Feature**: 012-animated-todo-frontend
**Date**: 2026-01-02
**Purpose**: Define component hierarchy, state models, and data flow patterns

---

## Component Architecture

### Component Hierarchy

```
App (Root Layout)
├── ThemeProvider (Context)
└── AuthProvider (Context)
    │
    ├── Landing Page (/)
    │   └── Redirect Logic (→ /dashboard or /signin)
    │
    ├── Auth Routes (/signin, /signup)
    │   ├── SignInPage
    │   │   └── SignInForm
    │   │       ├── Input (email)
    │   │       ├── Input (password)
    │   │       ├── Checkbox (remember me)
    │   │       └── Button (submit)
    │   │
    │   └── SignUpPage
    │       └── SignUpForm
    │           ├── Input (email)
    │           ├── Input (password)
    │           ├── PasswordStrength
    │           └── Button (submit)
    │
    └── Dashboard Layout (/dashboard)
        ├── Navbar
        │   ├── Logo
        │   ├── SearchInput (optional)
        │   ├── ThemeToggle
        │   └── UserDropdown
        │       ├── Avatar
        │       └── DropdownMenu
        │           ├── Profile
        │           ├── Settings
        │           └── Logout
        │
        ├── Sidebar (Desktop Only)
        │   ├── Navigation Links
        │   └── Collapse Toggle
        │
        └── Main Content
            ├── Dashboard Page
            │   ├── Header
            │   │   ├── Title
            │   │   └── AddTaskButton
            │   │
            │   ├── TaskFilters
            │   │   ├── Tabs (All, Active, Completed)
            │   │   ├── SearchInput
            │   │   └── SortDropdown
            │   │
            │   ├── TaskList
            │   │   ├── TaskCard (repeated)
            │   │   │   ├── Checkbox
            │   │   │   ├── Title
            │   │   │   ├── Description
            │   │   │   ├── Timestamp
            │   │   │   └── Actions (Edit, Delete)
            │   │   │
            │   │   └── TaskEmptyState (conditional)
            │   │       └── Illustration
            │   │
            │   └── TaskFormModal (conditional)
            │       └── Dialog
            │           ├── Input (title)
            │           ├── Textarea (description)
            │           ├── Button (cancel)
            │           └── Button (save)
```

---

## Component Specifications

### 1. UI Primitives (`components/ui/`)

#### Button
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit';
}

// Animations: Hover scale (1.02), active scale (0.98), loading spinner
```

#### Input
```typescript
interface InputProps {
  label: string;
  type?: 'text' | 'email' | 'password' | 'search';
  value: string;
  onChange: (value: string) => void;
  error?: string;
  placeholder?: string;
  autoFocus?: boolean;
  required?: boolean;
}

// Animations: Floating label, focus glow, error shake
```

#### Card
```typescript
interface CardProps {
  variant?: 'glass' | 'solid';
  hover?: boolean; // Enable hover lift effect
  children: React.ReactNode;
  className?: string;
}

// Animations: Hover lift (translateY -4px), shadow increase
```

#### Checkbox
```typescript
interface CheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
}

// Animations: Checkmark draw (SVG path), scale on check
```

#### Dialog
```typescript
interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
}

// Animations: Backdrop fade, content scale + opacity, slide up on mobile
```

#### Dropdown
```typescript
interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: 'start' | 'center' | 'end';
}

interface DropdownItem {
  label: string;
  icon?: React.ReactNode;
  onClick: () => void;
  variant?: 'default' | 'danger';
}

// Animations: Content fade + slide down, item hover highlight
```

#### Tabs
```typescript
interface TabsProps {
  tabs: Tab[];
  value: string;
  onChange: (value: string) => void;
}

interface Tab {
  value: string;
  label: string;
  count?: number; // Optional badge count
}

// Animations: Indicator slide, content fade
```

#### Avatar
```typescript
interface AvatarProps {
  src?: string;
  alt: string;
  fallback: string; // Initials
  size?: 'sm' | 'md' | 'lg';
}

// Animations: Image fade in, hover scale
```

---

### 2. Layout Components (`components/layout/`)

#### Navbar
```typescript
interface NavbarProps {
  user: User;
  onLogout: () => void;
}

// State: Scroll position (for blur effect)
// Animations: Blur backdrop on scroll, logo pulse
```

#### Sidebar
```typescript
interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

// State: Collapsed state (persisted in localStorage)
// Animations: Width transition, icon rotation
```

#### Container
```typescript
interface ContainerProps {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

// Responsive padding, centered layout
```

---

### 3. Task Components (`components/tasks/`)

#### TaskCard
```typescript
interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

// State: Hover state, swipe progress (mobile)
// Animations: Hover lift, checkbox draw, strikethrough, delete slide-out
```

#### TaskList
```typescript
interface TaskListProps {
  tasks: Task[];
  filter: FilterType;
  searchQuery: string;
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

// State: Filtered tasks (computed)
// Animations: Staggered children, layout shift on filter change
```

#### TaskForm
```typescript
interface TaskFormProps {
  mode: 'create' | 'edit';
  task?: Task; // Required in edit mode
  onSubmit: (data: TaskInput) => Promise<void>;
  onCancel: () => void;
}

// State: Form values, validation errors, loading
// Animations: Modal slide up, success checkmark, error shake
```

#### TaskFilters
```typescript
interface TaskFiltersProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  sortBy: SortType;
  onSortChange: (sort: SortType) => void;
  counts: { all: number; active: number; completed: number };
}

// Animations: Tab indicator slide, search icon pulse
```

#### TaskSearch
```typescript
interface TaskSearchProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

// Animations: Focus glow, icon rotate
```

#### TaskEmptyState
```typescript
interface TaskEmptyStateProps {
  filter: FilterType;
  onCreateTask: () => void;
}

// Animations: Fade in, floating illustration
```

---

### 4. Auth Components (`components/auth/`)

#### SignInForm
```typescript
interface SignInFormProps {
  onSubmit: (data: SignInInput) => Promise<void>;
  onSignUpClick: () => void;
}

// State: Email, password, remember me, loading, errors
// Animations: Input float, button loading, success redirect
```

#### SignUpForm
```typescript
interface SignUpFormProps {
  onSubmit: (data: SignUpInput) => Promise<void>;
  onSignInClick: () => void;
}

// State: Email, password, confirm password, loading, errors
// Animations: Input float, password strength, button loading
```

#### PasswordStrength
```typescript
interface PasswordStrengthProps {
  password: string;
}

// State: Strength score (0-4)
// Animations: Bar fill, color transition (red → yellow → green)
```

---

### 5. Animation Components (`components/animations/`)

#### FadeIn
```typescript
interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
}

// Wrapper for fade-in animation
```

#### SlideUp
```typescript
interface SlideUpProps {
  children: React.ReactNode;
  delay?: number;
}

// Wrapper for slide-up animation
```

#### StaggerChildren
```typescript
interface StaggerChildrenProps {
  children: React.ReactNode;
  stagger?: number; // Delay between children
}

// Container for staggered child animations
```

#### CheckmarkDraw
```typescript
interface CheckmarkDrawProps {
  size?: number;
  color?: string;
  onComplete?: () => void;
}

// SVG checkmark with path draw animation
```

---

## State Models

### 1. Task State

```typescript
// types/task.ts
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  userId: string;
  createdAt: string; // ISO 8601
  updatedAt: string; // ISO 8601
}

export interface TaskInput {
  title: string;
  description?: string;
}

export type FilterType = 'all' | 'active' | 'completed';
export type SortType = 'date-desc' | 'date-asc' | 'title-asc' | 'title-desc';

export interface TaskFilters {
  filter: FilterType;
  search: string;
  sort: SortType;
}
```

### 2. User State

```typescript
// types/user.ts
export interface User {
  id: string;
  email: string;
  createdAt: string;
}

export interface SignInInput {
  email: string;
  password: string;
  rememberMe: boolean;
}

export interface SignUpInput {
  email: string;
  password: string;
  confirmPassword: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}
```

### 3. Theme State

```typescript
// types/theme.ts
export type Theme = 'light' | 'dark';

export interface ThemeState {
  theme: Theme;
  toggleTheme: () => void;
}
```

### 4. UI State

```typescript
// types/ui.ts
export interface ModalState {
  taskForm: {
    open: boolean;
    mode: 'create' | 'edit';
    task?: Task;
  };
  deleteConfirmation: {
    open: boolean;
    taskId?: string;
  };
}

export interface SidebarState {
  collapsed: boolean;
}
```

---

## Data Flow

### 1. Task CRUD Flow

```
User Action → Component Event Handler → API Call → State Update → UI Re-render

Example: Create Task
1. User clicks "Add Task" button
2. TaskFormModal opens with empty form
3. User fills title and description
4. User clicks "Save"
5. Form validates input with Zod schema
6. API call: POST /api/{userId}/tasks
7. Success: Update local state with new task
8. Animation: Success checkmark, modal close, new task fades in
9. Failure: Show error message, shake form
```

### 2. Authentication Flow

```
Sign In:
1. User enters email and password
2. Client validates with Zod schema
3. API call: POST /api/auth/login
4. Success: Store JWT in localStorage, decode user ID, redirect to /dashboard
5. Failure: Show error message, shake form

Protected Routes:
1. User navigates to /dashboard
2. Layout checks for JWT in localStorage
3. If missing: Redirect to /signin
4. If present: Decode JWT, fetch user data, render dashboard
```

### 3. Filtering Flow

```
1. User clicks "Active" filter tab
2. Update filter state: 'all' → 'active'
3. Compute filtered tasks: tasks.filter(t => !t.completed)
4. Animation: Tab indicator slides, completed tasks fade out
5. Render filtered task list with staggered animation
```

### 4. Theme Toggle Flow

```
1. User clicks theme toggle button
2. toggleTheme() function called
3. Update theme state: 'light' → 'dark'
4. Update localStorage: theme = 'dark'
5. Update document class: document.documentElement.classList.add('dark')
6. CSS transitions all colors over 300ms
```

---

## Animation Variants

### Global Animation Definitions

```typescript
// lib/animations.ts
export const fadeIn = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

export const slideUp = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut' }
  }
};

export const slideDown = {
  hidden: { opacity: 0, y: -20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut' }
  }
};

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

export const staggerContainer = {
  visible: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export const listItem = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.3, ease: 'easeOut' }
  }
};

export const hoverLift = {
  rest: { y: 0, scale: 1, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  hover: {
    y: -4,
    scale: 1.02,
    boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
    transition: { duration: 0.2, ease: 'easeOut' }
  }
};

export const tapScale = {
  tap: { scale: 0.98 }
};

export const checkmarkDraw = {
  hidden: { pathLength: 0, opacity: 0 },
  visible: {
    pathLength: 1,
    opacity: 1,
    transition: { duration: 0.6, ease: 'easeOut' }
  }
};

export const shake = {
  shake: {
    x: [0, -4, 4, -4, 4, 0],
    transition: { duration: 0.5, ease: 'easeInOut' }
  }
};
```

---

## Custom Hooks

### useTasks

```typescript
// lib/hooks/use-tasks.ts
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, []);

  const createTask = useCallback(async (input: TaskInput) => {
    const newTask = await api.createTask(input);
    setTasks(prev => [newTask, ...prev]);
    return newTask;
  }, []);

  const updateTask = useCallback(async (id: string, input: Partial<TaskInput>) => {
    const updated = await api.updateTask(id, input);
    setTasks(prev => prev.map(t => t.id === id ? updated : t));
    return updated;
  }, []);

  const deleteTask = useCallback(async (id: string) => {
    await api.deleteTask(id);
    setTasks(prev => prev.filter(t => t.id !== id));
  }, []);

  const toggleTask = useCallback(async (id: string) => {
    const updated = await api.toggleTask(id);
    setTasks(prev => prev.map(t => t.id === id ? updated : t));
    return updated;
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTask
  };
}
```

### useTheme

```typescript
// lib/hooks/use-theme.ts
export function useTheme() {
  const [theme, setTheme] = useState<Theme>('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme') as Theme;
    const system = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initial = stored || (system ? 'dark' : 'light');
    setTheme(initial);
    document.documentElement.classList.toggle('dark', initial === 'dark');
  }, []);

  const toggleTheme = useCallback(() => {
    const next: Theme = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    localStorage.setItem('theme', next);
    document.documentElement.classList.toggle('dark', next === 'dark');
  }, [theme]);

  return { theme, toggleTheme };
}
```

### useMediaQuery

```typescript
// lib/hooks/use-media-query.ts
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}
```

---

## Validation Schemas

### Task Validation

```typescript
// types/task.ts
import { z } from 'zod';

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less')
    .trim(),
  description: z.string()
    .max(1000, 'Description must be 1000 characters or less')
    .trim()
    .optional(),
});

export type TaskInput = z.infer<typeof taskSchema>;
```

### Auth Validation

```typescript
// types/user.ts
import { z } from 'zod';

export const signInSchema = z.object({
  email: z.string()
    .email('Please enter a valid email address')
    .toLowerCase(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().default(false),
});

export const signUpSchema = z.object({
  email: z.string()
    .email('Please enter a valid email address')
    .toLowerCase(),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

export type SignInInput = z.infer<typeof signInSchema>;
export type SignUpInput = z.infer<typeof signUpSchema>;
```

---

## Performance Considerations

### Component Memoization

```typescript
// Memoize expensive computed values
const filteredTasks = useMemo(() => {
  return tasks.filter(task => {
    const matchesFilter =
      filter === 'all' ? true :
      filter === 'active' ? !task.completed :
      task.completed;

    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesFilter && matchesSearch;
  });
}, [tasks, filter, searchQuery]);

// Memoize callbacks to prevent re-renders
const handleToggle = useCallback((id: string) => {
  toggleTask(id);
}, [toggleTask]);
```

### Virtual Scrolling (Future Optimization)

```typescript
// For lists with 100+ tasks
import { useVirtualizer } from '@tanstack/react-virtual';

const parentRef = useRef<HTMLDivElement>(null);
const virtualizer = useVirtualizer({
  count: filteredTasks.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 120, // Estimated task card height
});
```

---

**Data Model Complete**: Component architecture, state models, and data flow patterns defined. Ready for contract generation.
