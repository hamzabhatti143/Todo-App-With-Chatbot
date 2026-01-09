# Frontend Development Guidelines

This file provides guidance for AI assistants working on the Next.js frontend.

## Architecture Principles

1. **App Router First**: Use Next.js App Router (app/ directory) with Server Components by default
2. **Client Components**: Only use "use client" directive when needed for interactivity, hooks, or browser APIs
3. **Type Safety**: Maintain strict TypeScript with zero `any` types
4. **Component Organization**: Separate UI components (components/ui/) from feature components (components/features/)

## Code Standards

### TypeScript
- Use strict mode (already configured in tsconfig.json)
- Define interfaces for all props and data structures in types/
- Use Zod schemas in validation/ for runtime validation
- Prefer type inference where obvious

### React Components
- Prefer functional components with hooks
- Use Server Components for static/data-fetching components
- Use Client Components only when needed:
  - useState, useEffect, or other React hooks
  - Event handlers (onClick, onChange, etc.)
  - Browser APIs (localStorage, window, etc.)
  - Third-party libraries requiring client-side rendering

Example Server Component:
```typescript
// app/tasks/page.tsx
import { TaskList } from '@/components/features/task-list'

export default async function TasksPage() {
  return (
    <main>
      <h1>My Tasks</h1>
      <TaskList />
    </main>
  )
}
```

Example Client Component:
```typescript
// components/features/task-form.tsx
'use client'

import { useState } from 'react'

export function TaskForm() {
  const [title, setTitle] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle form submission
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Styling
- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
- Minimum touch target: 44x44px
- Support minimum width: 320px
- Color system: Use Tailwind's default palette
- Spacing: Use Tailwind's spacing scale (4px increments)

### API Integration
- Create API client functions in lib/api.ts
- Use Axios for HTTP requests
- Include JWT token in Authorization header
- Handle errors with try/catch and display user-friendly messages
- Type all API responses with TypeScript interfaces

Example API client:
```typescript
// lib/api.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function getTasks(userId: string) {
  const response = await apiClient.get(`/api/${userId}/tasks`)
  return response.data
}
```

### State Management
- Use React hooks (useState, useReducer) for local state
- Use Better Auth for authentication state
- Create custom hooks in hooks/ for shared logic
- Avoid prop drilling with composition patterns

### Validation
- Define Zod schemas in validation/ directory
- Validate form inputs before API calls
- Display validation errors inline near inputs

Example validation:
```typescript
// validation/task.ts
import { z } from 'zod'

export const createTaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  description: z.string().max(1000).optional(),
})

export type CreateTaskInput = z.infer<typeof createTaskSchema>
```

## File Organization

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── tasks/             # Tasks feature pages
│   └── auth/              # Authentication pages
├── components/
│   ├── ui/                # Reusable UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── checkbox.tsx
│   └── features/          # Feature-specific components
│       ├── task-list.tsx
│       ├── task-form.tsx
│       └── task-item.tsx
├── lib/
│   ├── api.ts             # API client
│   ├── auth.ts            # Better Auth configuration
│   └── utils.ts           # Utility functions
├── types/
│   ├── task.ts            # Task type definitions
│   └── user.ts            # User type definitions
├── hooks/
│   ├── use-tasks.ts       # Custom hooks
│   └── use-auth.ts
└── validation/
    └── task.ts            # Zod schemas
```

## Testing Guidelines

- Write unit tests for utility functions
- Write integration tests for API client functions
- Test user interactions with React Testing Library
- Aim for >80% code coverage on critical paths

## Performance Considerations

- Use Server Components to reduce client-side JavaScript
- Implement code splitting with dynamic imports
- Optimize images with Next.js Image component
- Use React.memo() sparingly and only when profiling shows benefit
- Lazy load components below the fold

## Accessibility

- Use semantic HTML elements
- Include ARIA labels where needed
- Ensure keyboard navigation works
- Maintain sufficient color contrast (WCAG AA)
- Test with screen readers

## Common Patterns

### Loading States
```typescript
'use client'

import { useState, useEffect } from 'react'

export function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks().finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading...</div>
  return <ul>{tasks.map(task => ...)}</ul>
}
```

### Error Handling
```typescript
const [error, setError] = useState<string | null>(null)

try {
  await createTask(data)
} catch (err) {
  setError('Failed to create task. Please try again.')
}

{error && <div className="text-red-600">{error}</div>}
```

## Authentication Integration

### Better Auth Setup

The application uses Better Auth with JWT tokens for authentication. Token storage and management is handled in the `use-auth` hook.

**Authentication Flow**:
1. User submits credentials to `/api/auth/login`
2. Backend returns JWT token
3. Frontend stores token in localStorage
4. Axios interceptor adds token to all requests
5. Backend verifies token on protected endpoints

**Token Management**:
```typescript
// hooks/use-auth.ts
const login = async (credentials: UserLogin) => {
  const response = await authApi.login(credentials)
  localStorage.setItem('auth_token', response.access_token)
  localStorage.setItem('user_id', extractUserIdFromToken(response.access_token))
  setIsAuthenticated(true)
}

const logout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_id')
  setIsAuthenticated(false)
  router.push('/auth/login')
}
```

**Protected Routes**:
```typescript
// app/dashboard/page.tsx
'use client'

import { useAuth } from '@/hooks/use-auth'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Dashboard() {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login')
    }
  }, [isAuthenticated, loading, router])

  if (loading) return <LoadingSpinner />
  if (!isAuthenticated) return null

  return <DashboardContent />
}
```

## Custom Hooks

### use-auth Hook

Manages authentication state and provides login/logout functions.

```typescript
// Usage
const { isAuthenticated, userId, login, logout, register } = useAuth()
```

**Features**:
- Auto-loads auth state on mount
- Provides login/register/logout functions
- Handles token storage
- Redirects on auth state changes

### use-tasks Hook

Manages task CRUD operations with loading and error states.

```typescript
// Usage
const { tasks, loading, error, fetchTasks, createTask, updateTask, deleteTask, toggleComplete } = useTasks(userId)
```

**Features**:
- Automatic error handling
- Loading state management
- Optimistic UI updates
- Automatic refetch after mutations

## Component Patterns

### UI Component Pattern

Reusable UI components should be simple, typed, and composable:

```typescript
// components/ui/button.tsx
import { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  isLoading?: boolean
}

export function Button({
  variant = 'primary',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded font-medium transition'
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  }

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? 'Loading...' : children}
    </button>
  )
}
```

### Feature Component Pattern

Feature components combine UI components with business logic:

```typescript
// components/features/task-form.tsx
'use client'

import { useState } from 'react'
import { createTaskSchema } from '@/validation/task'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface TaskFormProps {
  onSubmit: (data: TaskCreate) => Promise<void>
  onCancel?: () => void
}

export function TaskForm({ onSubmit, onCancel }: TaskFormProps) {
  const [formData, setFormData] = useState({ title: '', description: '' })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    // Validate with Zod
    const result = createTaskSchema.safeParse(formData)
    if (!result.success) {
      const fieldErrors = result.error.flatten().fieldErrors
      setErrors(Object.fromEntries(
        Object.entries(fieldErrors).map(([key, val]) => [key, val?.[0] || ''])
      ))
      return
    }

    try {
      setIsSubmitting(true)
      await onSubmit(result.data)
      setFormData({ title: '', description: '' }) // Reset form
    } catch (error) {
      setErrors({ submit: 'Failed to create task' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Title"
        value={formData.title}
        onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
        error={errors.title}
        required
      />
      <Input
        label="Description"
        value={formData.description}
        onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
        error={errors.description}
      />
      {errors.submit && <ErrorMessage message={errors.submit} />}
      <div className="flex gap-2">
        <Button type="submit" isLoading={isSubmitting}>Create Task</Button>
        {onCancel && <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>}
      </div>
    </form>
  )
}
```

## Error Handling Best Practices

### API Error Handling

```typescript
// lib/api.ts - Error handling utility
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail: string }>

    // Backend validation errors
    if (axiosError.response?.status === 422) {
      return axiosError.response.data.detail || 'Validation error'
    }

    // Authentication errors
    if (axiosError.response?.status === 401) {
      return 'Authentication required. Please log in.'
    }

    // Authorization errors
    if (axiosError.response?.status === 403) {
      return 'You do not have permission to perform this action.'
    }

    // Not found errors
    if (axiosError.response?.status === 404) {
      return 'Resource not found.'
    }

    // Generic API errors
    return axiosError.response?.data?.detail || axiosError.message || 'An error occurred'
  }

  // Non-Axios errors
  return 'An unexpected error occurred'
}
```

### Component Error Boundaries

For catching React component errors (future enhancement):

```typescript
// components/error-boundary.tsx
'use client'

import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-50 border border-red-200 rounded">
          <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
          <p className="text-sm text-red-600 mt-2">{this.state.error?.message}</p>
        </div>
      )
    }

    return this.props.children
  }
}
```

## Responsive Design Guidelines

### Mobile-First Approach

Always start with mobile styles and add larger screen styles with breakpoints:

```typescript
<div className="
  p-4 sm:p-6 md:p-8              // Padding increases on larger screens
  text-sm sm:text-base md:text-lg // Text size scales up
  flex-col sm:flex-row            // Stack on mobile, row on desktop
  gap-2 sm:gap-4 md:gap-6         // Spacing increases
">
```

### Touch Target Sizing

Ensure all interactive elements meet minimum size requirements:

```typescript
// Minimum 44x44px for mobile touch targets
<button className="min-w-[44px] min-h-[44px] px-4 py-2">
  Click me
</button>
```

### Breakpoint Reference

Tailwind CSS breakpoints:
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

## Performance Optimization

### Code Splitting

Use dynamic imports for large components:

```typescript
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('@/components/heavy-component'), {
  loading: () => <LoadingSpinner />,
  ssr: false // Disable server-side rendering if not needed
})
```

### Memoization

Use React.memo() for expensive components that re-render frequently:

```typescript
import { memo } from 'react'

export const TaskItem = memo(function TaskItem({ task, onUpdate }: TaskItemProps) {
  return (
    <div>
      {/* Component content */}
    </div>
  )
}, (prevProps, nextProps) => {
  // Custom comparison function
  return prevProps.task.id === nextProps.task.id &&
         prevProps.task.completed === nextProps.task.completed
})
```

## Common Pitfalls

### 1. Forgetting 'use client' Directive

**Problem**: Using hooks or event handlers in Server Components
**Solution**: Add 'use client' at the top of the file

### 2. Direct localStorage Access in Server Components

**Problem**: localStorage is undefined during server-side rendering
**Solution**: Only access in useEffect or Client Components

### 3. Missing Error Boundaries

**Problem**: Errors crash the entire application
**Solution**: Wrap components in ErrorBoundary

### 4. Inline Function Props Causing Re-renders

**Problem**: New function created on every render
**Solution**: Use useCallback for functions passed as props

```typescript
const handleClick = useCallback(() => {
  // Handler logic
}, [dependencies])
```

### 5. Missing Loading States

**Problem**: Users don't know if action is processing
**Solution**: Always show loading indicators for async operations

## Dependencies

Refer to package.json for current versions. Key dependencies:
- next: ^15.1.0
- react: ^19.0.0
- better-auth: ^1.0.7
- axios: ^1.7.9
- zod: ^3.24.1
- tailwindcss: ^4.0.0
- typescript: ^5.7.2

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://better-auth.com)
- [Zod Documentation](https://zod.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
