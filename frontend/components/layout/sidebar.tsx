/**
 * Sidebar Component
 *
 * Collapsible sidebar with smooth width transition and localStorage persistence.
 * Responsive - hidden on mobile/tablet, shown on desktop.
 */

'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, Home, CheckSquare, Settings, BarChart3 } from 'lucide-react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { useIsLg } from '@/lib/hooks/use-media-query';

const SIDEBAR_STORAGE_KEY = 'sidebar-collapsed';

interface SidebarProps {
  className?: string;
}

interface NavItem {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  href: string;
  active?: boolean;
}

export function Sidebar({ className }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const isDesktop = useIsLg();
  const pathname = usePathname();

  // Load collapsed state from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(SIDEBAR_STORAGE_KEY);
    if (stored !== null) {
      setIsCollapsed(stored === 'true');
    }
  }, []);

  // Save collapsed state to localStorage
  const toggleCollapsed = () => {
    const newState = !isCollapsed;
    setIsCollapsed(newState);
    localStorage.setItem(SIDEBAR_STORAGE_KEY, String(newState));
  };

  // Navigation items
  const navItems: NavItem[] = [
    { label: 'Dashboard', icon: Home, href: '/dashboard', active: pathname === '/dashboard' },
    { label: 'Tasks', icon: CheckSquare, href: '/tasks', active: pathname === '/tasks' },
    { label: 'Analytics', icon: BarChart3, href: '/analytics', active: pathname === '/analytics' },
    { label: 'Settings', icon: Settings, href: '/settings', active: pathname === '/settings' },
  ];

  // Hide sidebar on mobile/tablet
  if (!isDesktop) {
    return null;
  }

  return (
    <motion.aside
      className={cn(
        'fixed left-0 top-16 bottom-0 z-30',
        'bg-slate-900/50 backdrop-blur-xl',
        'border-r border-slate-700/50',
        'transition-all duration-300 ease-in-out',
        className
      )}
      initial={false}
      animate={{
        width: isCollapsed ? 64 : 256,
      }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
    >
      <div className="flex flex-col h-full">
        {/* Collapse Toggle Button */}
        <div className="flex items-center justify-end p-4 border-b border-slate-700/50">
          <button
            onClick={toggleCollapsed}
            className="p-3 rounded-lg hover:bg-slate-800/50 transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
            aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            <motion.div
              initial={false}
              animate={{ rotate: isCollapsed ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronLeft className="h-5 w-5 text-gray-300" />
            </motion.div>
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navItems.map((item) => (
            <SidebarItem
              key={item.href}
              item={item}
              isCollapsed={isCollapsed}
            />
          ))}
        </nav>
      </div>
    </motion.aside>
  );
}

/**
 * SidebarItem - Individual navigation item
 */
interface SidebarItemProps {
  item: NavItem;
  isCollapsed: boolean;
}

function SidebarItem({ item, isCollapsed }: SidebarItemProps) {
  const Icon = item.icon;

  return (
    <Link
      href={item.href}
      className={cn(
        'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
        'hover:bg-slate-800/50',
        item.active
          ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
          : 'text-gray-300 border border-transparent',
        isCollapsed && 'justify-center'
      )}
    >
      <Icon
        className={cn(
          'h-5 w-5 flex-shrink-0',
          item.active
            ? 'text-blue-400'
            : 'text-gray-400'
        )}
      />

      <AnimatePresence>
        {!isCollapsed && (
          <motion.span
            className="font-medium text-sm truncate"
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: 'auto' }}
            exit={{ opacity: 0, width: 0 }}
            transition={{ duration: 0.2 }}
          >
            {item.label}
          </motion.span>
        )}
      </AnimatePresence>
    </Link>
  );
}

/**
 * SidebarSpacer - Add this to main content to prevent overlap with sidebar
 */
interface SidebarSpacerProps {
  isCollapsed?: boolean;
}

export function SidebarSpacer({ isCollapsed }: SidebarSpacerProps) {
  const isDesktop = useIsLg();
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(SIDEBAR_STORAGE_KEY);
    if (stored !== null) {
      setCollapsed(stored === 'true');
    }
  }, []);

  if (!isDesktop) {
    return null;
  }

  return (
    <motion.div
      initial={false}
      animate={{
        width: isCollapsed ?? collapsed ? 64 : 256,
      }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="flex-shrink-0"
    />
  );
}
