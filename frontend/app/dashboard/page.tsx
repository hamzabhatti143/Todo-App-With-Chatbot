/**
 * Dashboard Page
 *
 * Main dashboard with TaskList, floating action button, loading skeleton,
 * error state UI, filtering, search, sort, and optimistic UI updates.
 */

'use client';

import { useState, useEffect, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Plus, AlertCircle, Bot } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { TaskSearch } from '@/components/tasks/task-search';
import { TaskFilters } from '@/components/tasks/task-filters';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { FadeIn } from '@/components/animations/fade-in';
import type { Task, TaskCreate, FilterType, SortType } from '@/types/task';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, username, loading: authLoading } = useAuth();
  const {
    tasks,
    loading: tasksLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
  } = useTasks(username);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [fabMenuOpen, setFabMenuOpen] = useState(false);

  // Filter, search, and sort state
  const [filter, setFilter] = useState<FilterType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sort, setSort] = useState<SortType>('newest');

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/signin');
    }
  }, [isAuthenticated, authLoading, router]);

  // Handle create task
  const handleCreateTask = async (data: TaskCreate) => {
    const result = await createTask(data);
    if (result.success) {
      setIsFormOpen(false);
    } else if (result.error) {
      // Re-throw error so form can display it
      throw new Error(result.error);
    }
  };

  // Handle edit task
  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  // Handle update task
  const handleUpdateTask = async (data: TaskCreate) => {
    if (editingTask) {
      const result = await updateTask(editingTask.id, data);
      if (result.success) {
        setIsFormOpen(false);
        setEditingTask(null);
      } else if (result.error) {
        // Re-throw error so form can display it
        throw new Error(result.error);
      }
    }
  };

  // Handle delete task
  const handleDeleteTask = async (taskId: string) => {
    await deleteTask(taskId);
  };

  // Handle toggle complete
  const handleToggleComplete = async (taskId: string) => {
    await toggleComplete(taskId);
  };

  // Handle form close
  const handleFormClose = (open: boolean) => {
    setIsFormOpen(open);
    if (!open) {
      setEditingTask(null);
    }
  };

  // Handle clear filters
  const handleClearFilters = () => {
    setFilter('all');
    setSearchQuery('');
    setSort('newest');
  };

  // Filter tasks by status (useMemo for performance)
  const filteredTasks = useMemo(() => {
    let result = [...tasks];

    // Apply status filter
    if (filter === 'active') {
      result = result.filter((task) => !task.completed);
    } else if (filter === 'completed') {
      result = result.filter((task) => task.completed);
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (task) =>
          task.title.toLowerCase().includes(query) ||
          task.description?.toLowerCase().includes(query)
      );
    }

    return result;
  }, [tasks, filter, searchQuery]);

  // Sort tasks (useMemo for performance)
  const sortedTasks = useMemo(() => {
    const result = [...filteredTasks];

    switch (sort) {
      case 'newest':
        result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        break;
      case 'oldest':
        result.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        break;
      case 'title-asc':
        result.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'title-desc':
        result.sort((a, b) => b.title.localeCompare(a.title));
        break;
    }

    return result;
  }, [filteredTasks, sort]);

  // Calculate task counts
  const taskCounts = useMemo(
    () => ({
      all: tasks.length,
      active: tasks.filter((t) => !t.completed).length,
      completed: tasks.filter((t) => t.completed).length,
    }),
    [tasks]
  );

  // Show loading state
  if (authLoading || !isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <LoadingSkeleton />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <FadeIn>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              My Tasks
            </h1>
            <p className="mt-2 text-gray-400">
              Manage your tasks and stay organized
            </p>
          </div>

          {/* Desktop Action Buttons */}
          <div className="hidden sm:flex gap-3">
            <Button
              onClick={() => router.push('/chat')}
              size="lg"
              className="bg-purple-600 hover:bg-purple-700 text-white"
            >
              <Bot className="h-5 w-5 mr-2" />
              Perform Tasks With AI
            </Button>
            <Button
              onClick={() => setIsFormOpen(true)}
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Plus className="h-5 w-5 mr-2" />
              New Task
            </Button>
          </div>
        </div>
      </FadeIn>

      {/* Error State */}
      {error && (
        <ErrorState error={error} onRetry={fetchTasks} />
      )}

      {/* Search */}
      <FadeIn delay={0.1}>
        <TaskSearch value={searchQuery} onChange={setSearchQuery} />
      </FadeIn>

      {/* Filters */}
      <FadeIn delay={0.2}>
        <TaskFilters
          filter={filter}
          onFilterChange={setFilter}
          sort={sort}
          onSortChange={setSort}
          taskCounts={taskCounts}
          onClearFilters={handleClearFilters}
        />
      </FadeIn>

      {/* Task List */}
      {tasksLoading ? (
        <LoadingSkeleton />
      ) : (
        <TaskList
          tasks={sortedTasks}
          onToggleComplete={handleToggleComplete}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
          onCreateNew={() => setIsFormOpen(true)}
        />
      )}

      {/* Floating Action Buttons (Mobile) */}
      <div className="fixed bottom-6 right-6 sm:hidden z-10 flex flex-col items-end gap-3">
        {/* Floating Menu Options */}
        {fabMenuOpen && (
          <>
            <motion.button
              onClick={() => {
                router.push('/chat');
                setFabMenuOpen(false);
              }}
              className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-full shadow-lg"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: 0.05 }}
            >
              <Bot className="h-5 w-5" />
              <span className="text-sm font-medium">AI Chat</span>
            </motion.button>
            <motion.button
              onClick={() => {
                setIsFormOpen(true);
                setFabMenuOpen(false);
              }}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-full shadow-lg"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ delay: 0.1 }}
            >
              <Plus className="h-5 w-5" />
              <span className="text-sm font-medium">New Task</span>
            </motion.button>
          </>
        )}

        {/* Main FAB Button */}
        <motion.button
          onClick={() => setFabMenuOpen(!fabMenuOpen)}
          className="w-14 h-14 bg-gradient-to-br from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-full shadow-lg flex items-center justify-center"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1, rotate: fabMenuOpen ? 45 : 0 }}
          transition={{
            type: 'spring',
            stiffness: 500,
            damping: 30,
          }}
        >
          <Plus className="h-6 w-6" />
        </motion.button>
      </div>

      {/* Task Form Modal */}
      <TaskForm
        open={isFormOpen}
        onOpenChange={handleFormClose}
        onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
        mode={editingTask ? 'edit' : 'create'}
        initialData={editingTask}
      />
    </div>
  );
}

/**
 * Loading Skeleton Component
 */
function LoadingSkeleton() {
  return (
    <div className="space-y-3">
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="bg-slate-900/50 backdrop-blur-sm rounded-lg p-4 border border-slate-700/50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: i * 0.1 }}
        >
          <div className="flex items-start gap-3">
            {/* Checkbox skeleton */}
            <div className="w-5 h-5 rounded bg-slate-700/50 animate-pulse" />

            <div className="flex-1 space-y-2">
              {/* Title skeleton */}
              <div className="h-5 bg-slate-700/50 rounded animate-pulse w-3/4" />

              {/* Description skeleton */}
              <div className="h-4 bg-slate-700/50 rounded animate-pulse w-1/2" />

              {/* Time skeleton */}
              <div className="h-3 bg-slate-700/50 rounded animate-pulse w-24" />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}

/**
 * Error State Component
 */
interface ErrorStateProps {
  error: string;
  onRetry: () => void;
}

function ErrorState({ error, onRetry }: ErrorStateProps) {
  return (
    <FadeIn>
      <Card variant="default" padding="lg" className="bg-red-900/20 border-red-500/50">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            <AlertCircle className="h-6 w-6 text-red-400" />
          </div>

          <div className="flex-1">
            <h3 className="text-lg font-semibold text-red-100">
              Something went wrong
            </h3>
            <p className="mt-1 text-sm text-red-300">
              {error}
            </p>

            <Button
              onClick={onRetry}
              variant="secondary"
              size="sm"
              className="mt-4 bg-red-600 hover:bg-red-700 text-white"
            >
              Try again
            </Button>
          </div>
        </div>
      </Card>
    </FadeIn>
  );
}
