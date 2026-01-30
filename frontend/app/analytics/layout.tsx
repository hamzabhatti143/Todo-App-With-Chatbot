/**
 * Analytics Layout
 *
 * Inherits the dashboard layout with Navbar and Sidebar.
 */

'use client';

import { useAuth } from '@/hooks/use-auth';
import { Navbar, NavbarSpacer } from '@/components/layout/navbar';
import { Sidebar, SidebarSpacer } from '@/components/layout/sidebar';

export default function AnalyticsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, username, logout } = useAuth();

  // Get user info
  const user = isAuthenticated && username
    ? {
        name: username,
        email: localStorage.getItem('user_email') || 'user@example.com',
      }
    : undefined;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      {/* Animated Background Gradients */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 -left-4 w-96 h-96 bg-blue-500/5 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" />
        <div className="absolute top-0 -right-4 w-96 h-96 bg-purple-500/5 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500/5 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '4s' }} />
      </div>

      <Navbar user={user} onLogout={logout} />
      <NavbarSpacer />

      <div className="flex relative z-10">
        <Sidebar />
        <SidebarSpacer />

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
