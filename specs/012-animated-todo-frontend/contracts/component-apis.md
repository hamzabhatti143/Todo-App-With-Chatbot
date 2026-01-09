# Component API Contracts

**Feature**: 012-animated-todo-frontend
**Date**: 2026-01-02
**Purpose**: Define TypeScript interfaces and component prop contracts

---

## UI Primitive Components

### Button

```typescript
// components/ui/button.tsx
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export function Button(props: ButtonProps): JSX.Element;
```

**Usage Example**:
```tsx
<Button
  variant="primary"
  size="md"
  loading={isSubmitting}
  leftIcon={<PlusIcon />}
  onClick={handleClick}
>
  Add Task
</Button>
```

---

### Input

```typescript
// components/ui/input.tsx
export interface InputProps {
  label: string;
  type?: 'text' | 'email' | 'password' | 'search';
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  error?: string;
  placeholder?: string;
  autoFocus?: boolean;
  required?: boolean;
  disabled?: boolean;
  maxLength?: number;
  icon?: React.ReactNode;
  className?: string;
}

export function Input(props: InputProps): JSX.Element;
```

**Usage Example**:
```tsx
<Input
  label="Task Title"
  type="text"
  value={title}
  onChange={setTitle}
  error={errors.title}
  placeholder="Enter task title..."
  required
  maxLength={200}
/>
```

---

### Card

```typescript
// components/ui/card.tsx
export interface CardProps {
  variant?: 'glass' | 'solid';
  hover?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export function Card(props: CardProps): JSX.Element;
```

**Usage Example**:
```tsx
<Card variant="glass" hover padding="md">
  <h3>Card Title</h3>
  <p>Card content</p>
</Card>
```

---

### Checkbox

```typescript
// components/ui/checkbox.tsx
export interface CheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
  indeterminate?: boolean;
  className?: string;
}

export function Checkbox(props: CheckboxProps): JSX.Element;
```

**Usage Example**:
```tsx
<Checkbox
  checked={task.completed}
  onChange={handleToggle}
  label="Mark as complete"
/>
```

---

### Dialog

```typescript
// components/ui/dialog.tsx
export interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
}

export function Dialog(props: DialogProps): JSX.Element;

export interface DialogHeaderProps {
  children: React.ReactNode;
}

export function DialogHeader(props: DialogHeaderProps): JSX.Element;

export interface DialogFooterProps {
  children: React.ReactNode;
}

export function DialogFooter(props: DialogFooterProps): JSX.Element;
```

**Usage Example**:
```tsx
<Dialog
  open={isOpen}
  onOpenChange={setIsOpen}
  title="Create Task"
  description="Add a new task to your list"
  size="md"
>
  <DialogHeader>
    <h2>Task Details</h2>
  </DialogHeader>
  {/* Form content */}
  <DialogFooter>
    <Button variant="ghost" onClick={handleCancel}>Cancel</Button>
    <Button variant="primary" onClick={handleSubmit}>Save</Button>
  </DialogFooter>
</Dialog>
```

---

### Dropdown

```typescript
// components/ui/dropdown.tsx
export interface DropdownItem {
  label: string;
  value: string;
  icon?: React.ReactNode;
  onClick: () => void;
  variant?: 'default' | 'danger';
  disabled?: boolean;
  divider?: boolean; // Show divider after this item
}

export interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: 'start' | 'center' | 'end';
  side?: 'top' | 'right' | 'bottom' | 'left';
  className?: string;
}

export function Dropdown(props: DropdownProps): JSX.Element;
```

**Usage Example**:
```tsx
<Dropdown
  trigger={<Button variant="ghost"><MoreIcon /></Button>}
  items={[
    { label: 'Edit', value: 'edit', icon: <EditIcon />, onClick: handleEdit },
    { label: 'Delete', value: 'delete', icon: <TrashIcon />, onClick: handleDelete, variant: 'danger' }
  ]}
  align="end"
/>
```

---

### Tabs

```typescript
// components/ui/tabs.tsx
export interface Tab {
  value: string;
  label: string;
  count?: number;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: Tab[];
  value: string;
  onChange: (value: string) => void;
  variant?: 'default' | 'pills';
  className?: string;
}

export function Tabs(props: TabsProps): JSX.Element;
```

**Usage Example**:
```tsx
<Tabs
  tabs={[
    { value: 'all', label: 'All', count: 10 },
    { value: 'active', label: 'Active', count: 6 },
    { value: 'completed', label: 'Completed', count: 4 }
  ]}
  value={filter}
  onChange={setFilter}
  variant="pills"
/>
```

---

### Avatar

```typescript
// components/ui/avatar.tsx
export interface AvatarProps {
  src?: string;
  alt: string;
  fallback: string; // Initials or single character
  size?: 'sm' | 'md' | 'lg' | 'xl';
  status?: 'online' | 'offline' | 'away';
  className?: string;
}

export function Avatar(props: AvatarProps): JSX.Element;
```

**Usage Example**:
```tsx
<Avatar
  src={user.avatar}
  alt={user.email}
  fallback={user.email[0].toUpperCase()}
  size="md"
  status="online"
/>
```

---

## Layout Components

### Navbar

```typescript
// components/layout/navbar.tsx
export interface NavbarProps {
  user: User;
  onLogout: () => void;
}

export function Navbar(props: NavbarProps): JSX.Element;
```

**Usage Example**:
```tsx
<Navbar
  user={currentUser}
  onLogout={handleLogout}
/>
```

---

### Sidebar

```typescript
// components/layout/sidebar.tsx
export interface SidebarItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  active?: boolean;
  badge?: string | number;
}

export interface SidebarProps {
  items: SidebarItem[];
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar(props: SidebarProps): JSX.Element;
```

**Usage Example**:
```tsx
<Sidebar
  items={[
    { label: 'Dashboard', href: '/dashboard', icon: <HomeIcon />, active: true },
    { label: 'Tasks', href: '/tasks', icon: <CheckIcon />, badge: 5 }
  ]}
  collapsed={isSidebarCollapsed}
  onToggle={toggleSidebar}
/>
```

---

### Container

```typescript
// components/layout/container.tsx
export interface ContainerProps {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
}

export function Container(props: ContainerProps): JSX.Element;
```

**Usage Example**:
```tsx
<Container maxWidth="lg" padding="md">
  <h1>Dashboard</h1>
  <TaskList tasks={tasks} />
</Container>
```

---

## Task Components

### TaskCard

```typescript
// components/tasks/task-card.tsx
export interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => Promise<void>;
  animationDelay?: number; // For staggered animations
}

export function TaskCard(props: TaskCardProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskCard
  task={task}
  onToggle={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
  animationDelay={index * 0.1}
/>
```

---

### TaskList

```typescript
// components/tasks/task-list.tsx
export interface TaskListProps {
  tasks: Task[];
  filter: FilterType;
  searchQuery: string;
  sortBy: SortType;
  onToggle: (id: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => Promise<void>;
  loading?: boolean;
}

export function TaskList(props: TaskListProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskList
  tasks={tasks}
  filter={currentFilter}
  searchQuery={search}
  sortBy={sortOption}
  onToggle={toggleTask}
  onEdit={openEditModal}
  onDelete={deleteTask}
  loading={isLoading}
/>
```

---

### TaskForm

```typescript
// components/tasks/task-form.tsx
export interface TaskFormProps {
  mode: 'create' | 'edit';
  task?: Task;
  onSubmit: (data: TaskInput) => Promise<void>;
  onCancel: () => void;
}

export function TaskForm(props: TaskFormProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskForm
  mode="create"
  onSubmit={createTask}
  onCancel={closeModal}
/>

<TaskForm
  mode="edit"
  task={selectedTask}
  onSubmit={updateTask}
  onCancel={closeModal}
/>
```

---

### TaskFilters

```typescript
// components/tasks/task-filters.tsx
export interface TaskFilterCounts {
  all: number;
  active: number;
  completed: number;
}

export interface TaskFiltersProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  sortBy: SortType;
  onSortChange: (sort: SortType) => void;
  counts: TaskFilterCounts;
}

export function TaskFilters(props: TaskFiltersProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskFilters
  activeFilter={filter}
  onFilterChange={setFilter}
  searchQuery={searchQuery}
  onSearchChange={setSearchQuery}
  sortBy={sortBy}
  onSortChange={setSortBy}
  counts={{ all: 10, active: 6, completed: 4 }}
/>
```

---

### TaskSearch

```typescript
// components/tasks/task-search.tsx
export interface TaskSearchProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  debounce?: number; // Milliseconds
}

export function TaskSearch(props: TaskSearchProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskSearch
  value={searchQuery}
  onChange={setSearchQuery}
  placeholder="Search tasks..."
  debounce={300}
/>
```

---

### TaskEmptyState

```typescript
// components/tasks/task-empty-state.tsx
export interface TaskEmptyStateProps {
  filter: FilterType;
  searchQuery: string;
  onCreateTask: () => void;
  onClearSearch?: () => void;
}

export function TaskEmptyState(props: TaskEmptyStateProps): JSX.Element;
```

**Usage Example**:
```tsx
<TaskEmptyState
  filter={currentFilter}
  searchQuery={searchQuery}
  onCreateTask={openCreateModal}
  onClearSearch={clearSearch}
/>
```

---

## Auth Components

### SignInForm

```typescript
// components/auth/signin-form.tsx
export interface SignInFormProps {
  onSubmit: (data: SignInInput) => Promise<void>;
  onSignUpClick: () => void;
  onForgotPasswordClick?: () => void;
}

export function SignInForm(props: SignInFormProps): JSX.Element;
```

**Usage Example**:
```tsx
<SignInForm
  onSubmit={handleSignIn}
  onSignUpClick={navigateToSignUp}
  onForgotPasswordClick={openForgotPassword}
/>
```

---

### SignUpForm

```typescript
// components/auth/signup-form.tsx
export interface SignUpFormProps {
  onSubmit: (data: SignUpInput) => Promise<void>;
  onSignInClick: () => void;
}

export function SignUpForm(props: SignUpFormProps): JSX.Element;
```

**Usage Example**:
```tsx
<SignUpForm
  onSubmit={handleSignUp}
  onSignInClick={navigateToSignIn}
/>
```

---

### PasswordStrength

```typescript
// components/auth/password-strength.tsx
export type PasswordStrength = 0 | 1 | 2 | 3 | 4;

export interface PasswordStrengthProps {
  password: string;
  showLabel?: boolean;
}

export function PasswordStrength(props: PasswordStrengthProps): JSX.Element;

export function calculatePasswordStrength(password: string): PasswordStrength;
```

**Usage Example**:
```tsx
<PasswordStrength
  password={password}
  showLabel
/>
```

---

## Animation Components

### FadeIn

```typescript
// components/animations/fade-in.tsx
export interface FadeInProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  className?: string;
}

export function FadeIn(props: FadeInProps): JSX.Element;
```

**Usage Example**:
```tsx
<FadeIn delay={0.2} duration={0.5}>
  <TaskCard task={task} />
</FadeIn>
```

---

### SlideUp

```typescript
// components/animations/slide-up.tsx
export interface SlideUpProps {
  children: React.ReactNode;
  delay?: number;
  distance?: number; // Pixels to slide
  className?: string;
}

export function SlideUp(props: SlideUpProps): JSX.Element;
```

**Usage Example**:
```tsx
<SlideUp delay={0.1} distance={20}>
  <div>Content slides up</div>
</SlideUp>
```

---

### StaggerChildren

```typescript
// components/animations/stagger-children.tsx
export interface StaggerChildrenProps {
  children: React.ReactNode;
  stagger?: number; // Delay between children in seconds
  className?: string;
}

export function StaggerChildren(props: StaggerChildrenProps): JSX.Element;
```

**Usage Example**:
```tsx
<StaggerChildren stagger={0.1}>
  {tasks.map(task => (
    <TaskCard key={task.id} task={task} />
  ))}
</StaggerChildren>
```

---

### CheckmarkDraw

```typescript
// components/animations/checkmark-draw.tsx
export interface CheckmarkDrawProps {
  size?: number; // Width/height in pixels
  color?: string; // Stroke color
  strokeWidth?: number;
  duration?: number; // Animation duration in seconds
  onComplete?: () => void;
  className?: string;
}

export function CheckmarkDraw(props: CheckmarkDrawProps): JSX.Element;
```

**Usage Example**:
```tsx
<CheckmarkDraw
  size={64}
  color="#10b981"
  strokeWidth={3}
  duration={0.6}
  onComplete={closeModal}
/>
```

---

## Type Definitions

### Core Types

```typescript
// types/task.ts
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

export interface TaskInput {
  title: string;
  description?: string;
}

export type FilterType = 'all' | 'active' | 'completed';

export type SortType =
  | 'date-desc'
  | 'date-asc'
  | 'title-asc'
  | 'title-desc';
```

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
```

```typescript
// types/api.ts
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  message: string;
  field?: string;
  code?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
```

---

## Utility Functions

### Animation Utilities

```typescript
// lib/animations.ts
export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
};

export const slideUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.3 } }
};

export const staggerContainer: Variants = {
  visible: { transition: { staggerChildren: 0.1 } }
};

export const hoverLift = {
  rest: { y: 0, scale: 1 },
  hover: { y: -4, scale: 1.02, transition: { duration: 0.2 } }
};
```

### Validation Utilities

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

export function truncate(text: string, length: number): string {
  return text.length > length ? text.slice(0, length) + '...' : text;
}
```

---

**Component API Contracts Complete**: All component interfaces, prop types, and usage examples defined.
