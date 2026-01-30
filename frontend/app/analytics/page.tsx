/**
 * Analytics Page
 *
 * Task analytics and productivity insights page with backend integration.
 * Shows statistics, charts, and trends for task completion.
 */

'use client';

import { useRouter } from 'next/navigation';
import { useMemo } from 'react';
import { ArrowLeft, TrendingUp, CheckCircle, Clock, Calendar } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { Container } from '@/components/layout/container';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FadeIn } from '@/components/animations/fade-in';

export default function AnalyticsPage() {
  const router = useRouter();
  const { username } = useAuth();
  const { tasks, loading } = useTasks(username);

  // Calculate analytics data
  const analytics = useMemo(() => {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;

    // Calculate tasks created this week
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    const thisWeek = tasks.filter(t => new Date(t.created_at) > oneWeekAgo).length;

    return { total, completed, pending, thisWeek };
  }, [tasks]);

  return (
    <Container maxWidth="lg" padding="lg">
      <div className="min-h-[60vh] space-y-6">
        <FadeIn>
          <Button
            variant="ghost"
            onClick={() => router.push('/dashboard')}
            className="mb-4 text-gray-300 hover:text-white hover:bg-slate-800/50"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </FadeIn>

        <FadeIn delay={0.1}>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-6">
            Analytics & Insights
          </h1>
        </FadeIn>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <FadeIn delay={0.15}>
            <Card padding="md" className="bg-slate-900/50 border-slate-700/50 border-l-4 border-l-blue-500">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-blue-600/20 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Total Tasks</p>
                  <p className="text-2xl font-bold text-white">{loading ? '...' : analytics.total}</p>
                </div>
              </div>
            </Card>
          </FadeIn>

          <FadeIn delay={0.2}>
            <Card padding="md" className="bg-slate-900/50 border-slate-700/50 border-l-4 border-l-green-500">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-green-600/20 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Completed</p>
                  <p className="text-2xl font-bold text-white">{loading ? '...' : analytics.completed}</p>
                </div>
              </div>
            </Card>
          </FadeIn>

          <FadeIn delay={0.25}>
            <Card padding="md" className="bg-slate-900/50 border-slate-700/50 border-l-4 border-l-yellow-500">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-yellow-600/20 rounded-lg">
                  <Clock className="h-6 w-6 text-yellow-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Pending</p>
                  <p className="text-2xl font-bold text-white">{loading ? '...' : analytics.pending}</p>
                </div>
              </div>
            </Card>
          </FadeIn>

          <FadeIn delay={0.3}>
            <Card padding="md" className="bg-slate-900/50 border-slate-700/50 border-l-4 border-l-purple-500">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-purple-600/20 rounded-lg">
                  <Calendar className="h-6 w-6 text-purple-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">This Week</p>
                  <p className="text-2xl font-bold text-white">{loading ? '...' : analytics.thisWeek}</p>
                </div>
              </div>
            </Card>
          </FadeIn>
        </div>

        {/* Charts Section */}
        <FadeIn delay={0.35}>
          <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
            <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4">
              Productivity Insights
            </h2>
            <p className="text-gray-400 mb-6">
              Track your task completion rate, productivity trends, and performance metrics
              over time.
            </p>
            <div className="bg-gradient-to-br from-blue-600/10 to-indigo-600/10 border border-blue-500/30 rounded-lg p-8 text-center">
              <TrendingUp className="h-16 w-16 text-blue-400 mx-auto mb-4" />
              <p className="text-sm text-blue-200 font-medium">
                <strong>Coming Soon:</strong> Interactive Charts & Graphs
              </p>
              <ul className="mt-4 space-y-2 text-sm text-blue-300 text-left max-w-md mx-auto">
                <li>• Task completion trends over time</li>
                <li>• Daily, weekly, and monthly productivity charts</li>
                <li>• Category and priority distribution</li>
                <li>• Time-to-completion analytics</li>
                <li>• Customizable date ranges and filters</li>
                <li>• Export reports as PDF or CSV</li>
              </ul>
            </div>
          </Card>
        </FadeIn>

        {/* Activity Timeline */}
        <FadeIn delay={0.4}>
          <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
            <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4">
              Recent Activity
            </h2>
            <p className="text-gray-400">
              Your recent task activity will be displayed here, showing task creations,
              completions, and updates.
            </p>
            <div className="mt-4 bg-slate-800/50 border border-slate-700/50 rounded-lg p-6 text-center">
              <Calendar className="h-12 w-12 text-gray-500 mx-auto mb-2" />
              <p className="text-sm text-gray-400">
                Activity timeline coming soon
              </p>
            </div>
          </Card>
        </FadeIn>
      </div>
    </Container>
  );
}
