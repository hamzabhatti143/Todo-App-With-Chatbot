/**
 * Navbar Component
 *
 * Sticky navigation bar with blur-on-scroll effect, user avatar dropdown,
 * and theme toggle button. Responsive with mobile menu support.
 */

'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Moon, Sun, LogOut, User, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useTheme } from '@/lib/hooks/use-theme';
import { Avatar } from '@/components/ui/avatar';
import {
  Dropdown,
  DropdownTrigger,
  DropdownContent,
  DropdownItem,
  DropdownSeparator,
  DropdownLabel,
} from '@/components/ui/dropdown';
import { Button } from '@/components/ui/button';
import { Container } from './container';

interface NavbarProps {
  user?: {
    name?: string;
    email?: string;
    avatarUrl?: string;
  };
  onLogout?: () => void;
  className?: string;
}

export function Navbar({ user, onLogout, className }: NavbarProps) {
  const [scrolled, setScrolled] = useState(false);
  const { toggleTheme, isDark } = useTheme();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      className={cn(
        'fixed top-0 left-0 right-0 z-40 transition-all duration-200',
        scrolled
          ? 'glass-navbar shadow-lg'
          : 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-transparent',
        className
      )}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      <Container maxWidth="full" padding="md">
        <div className="flex items-center justify-between h-16">
          {/* Logo / Brand */}
          <div className="flex items-center">
            <motion.a
              href="/"
              className="text-xl font-bold text-gray-900 dark:text-gray-100"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              TaskFlow
            </motion.a>
          </div>

          {/* Right Side - Theme Toggle & User Menu */}
          <div className="flex items-center gap-2">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="rounded-full w-11 h-11 p-0"
            >
              <motion.div
                initial={false}
                animate={{ rotate: isDark ? 180 : 0 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
              >
                {isDark ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </motion.div>
            </Button>

            {/* User Menu */}
            {user && (
              <Dropdown>
                <DropdownTrigger asChild>
                  <button
                    className="rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 min-h-[44px] min-w-[44px] flex items-center justify-center"
                    aria-label="User menu"
                  >
                    <Avatar
                      src={user.avatarUrl}
                      name={user.name || user.email}
                      size="md"
                    />
                  </button>
                </DropdownTrigger>

                <DropdownContent align="end" className="w-56">
                  <DropdownLabel>My Account</DropdownLabel>
                  <DropdownSeparator />

                  <DropdownItem>
                    <User className="mr-2 h-4 w-4" />
                    <span className="flex-1">{user.name || 'User'}</span>
                  </DropdownItem>

                  <DropdownItem>
                    <div className="flex flex-col">
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {user.email}
                      </span>
                    </div>
                  </DropdownItem>

                  <DropdownSeparator />

                  <DropdownItem>
                    <Settings className="mr-2 h-4 w-4" />
                    <span>Settings</span>
                  </DropdownItem>

                  <DropdownSeparator />

                  <DropdownItem
                    onClick={onLogout}
                    className="text-red-600 dark:text-red-400 focus:text-red-600 dark:focus:text-red-400"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownItem>
                </DropdownContent>
              </Dropdown>
            )}
          </div>
        </div>
      </Container>
    </motion.nav>
  );
}

/**
 * NavbarSpacer - Add this below Navbar to prevent content from hiding under the fixed navbar
 */
export function NavbarSpacer() {
  return <div className="h-16" />;
}
