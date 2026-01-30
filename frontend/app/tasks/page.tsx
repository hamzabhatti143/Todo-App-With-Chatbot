/**
 * Tasks Page
 *
 * Dedicated page for viewing all tasks in a detailed view with backend integration.
 */

'use client';

import { useRouter } from 'next/navigation';
import { ArrowLeft, Plus } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { Container } from '@/components/layout/container';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FadeIn } from '@/components/animations/fade-in';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import type { Task, TaskCreate } from '@/types/task';

export default function TasksPage() {
  const router = useRouter();
  const { username } = useAuth();
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
  } = useTasks(username);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const handleCreateTask = async (data: TaskCreate) => {
    const result = await createTask(data);
    if (result.success) {
      setIsFormOpen(false);
    } else if (result.error) {
      throw new Error(result.error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const handleUpdateTask = async (data: TaskCreate) => {
    if (editingTask) {
      const result = await updateTask(editingTask.id, data);
      if (result.success) {
        setIsFormOpen(false);
        setEditingTask(null);
      } else if (result.error) {
        throw new Error(result.error);
      }
    }
  };

  const handleFormClose = (open: boolean) => {
    setIsFormOpen(open);
    if (!open) {
      setEditingTask(null);
    }
  };

  return (
    <Container maxWidth="lg" padding="lg">
      <div className="min-h-[60vh] space-y-6">
        <FadeIn>
          <div className="flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={() => router.push('/dashboard')}
              className="mb-4 text-gray-300 hover:text-white hover:bg-slate-800/50"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>

            <Button
              onClick={() => setIsFormOpen(true)}
              className="mb-4 bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Plus className="h-5 w-5 mr-2" />
              New Task
            </Button>
          </div>
        </FadeIn>

        <FadeIn delay={0.1}>
          <div className="mb-6">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-2">
              All Tasks
            </h1>
            <p className="text-gray-400">
              View and manage all your tasks in one place
            </p>
          </div>
        </FadeIn>

        <FadeIn delay={0.2}>
          {loading ? (
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <p className="text-gray-400 text-center py-8">Loading tasks...</p>
            </Card>
          ) : error ? (
            <Card padding="lg" className="bg-red-900/20 border-red-500/50">
              <p className="text-red-300 text-center py-8">{error}</p>
            </Card>
          ) : (
            <TaskList
              tasks={tasks}
              onToggleComplete={toggleComplete}
              onEdit={handleEditTask}
              onDelete={deleteTask}
              onCreateNew={() => setIsFormOpen(true)}
            />
          )}
        </FadeIn>
      </div>

      {/* Task Form Modal */}
      <TaskForm
        open={isFormOpen}
        onOpenChange={handleFormClose}
        onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
        mode={editingTask ? 'edit' : 'create'}
        initialData={editingTask}
      />
    </Container>
  );
}
