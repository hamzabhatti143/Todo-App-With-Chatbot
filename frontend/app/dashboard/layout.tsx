/**
 * Dashboard Layout
 *
 * Main layout for authenticated dashboard pages with Navbar, Sidebar (desktop only),
 * and main content area with proper responsive grid.
 */

'use client';

import { useAuth } from '@/hooks/use-auth';
import { Navbar, NavbarSpacer } from '@/components/layout/navbar';
import { Sidebar, SidebarSpacer } from '@/components/layout/sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, userId, logout } = useAuth();

  // Get user info (in a real app, this would come from useAuth)
  const user = isAuthenticated && userId
    ? {
        name: 'User',
        email: localStorage.getItem('user_email') || 'user@example.com',
      }
    : undefined;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Navbar */}
      <Navbar user={user} onLogout={logout} />

      {/* Spacer for fixed navbar */}
      <NavbarSpacer />

      <div className="flex">
        {/* Sidebar (desktop only) */}
        <Sidebar />

        {/* Sidebar Spacer */}
        <SidebarSpacer />

        {/* Main Content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
