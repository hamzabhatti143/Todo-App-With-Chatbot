'use client';

/**
 * useTheme Hook
 *
 * Manages dark mode theme state with localStorage persistence.
 * Automatically applies theme class to document element.
 */

import { useEffect, useState } from 'react';

export type Theme = 'light' | 'dark';

interface UseThemeReturn {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  isDark: boolean;
  mounted: boolean;
}

/**
 * Get the initial theme - always returns dark mode
 */
function getInitialTheme(): Theme {
  // Always return dark mode as default
  return 'dark';
}

/**
 * Apply theme class to document element
 */
function applyTheme(theme: Theme): void {
  if (typeof window === 'undefined') return;

  const root = document.documentElement;

  if (theme === 'dark') {
    root.classList.add('dark');
  } else {
    root.classList.remove('dark');
  }
}

/**
 * useTheme hook for dark mode management
 *
 * @returns {UseThemeReturn} Theme state and controls
 *
 * @example
 * ```tsx
 * function ThemeToggle() {
 *   const { theme, toggleTheme, isDark } = useTheme();
 *
 *   return (
 *     <button onClick={toggleTheme}>
 *       {isDark ? '🌙 Dark' : '☀️ Light'}
 *     </button>
 *   );
 * }
 * ```
 */
export function useTheme(): UseThemeReturn {
  const [theme, setThemeState] = useState<Theme>(() => getInitialTheme());
  const [mounted, setMounted] = useState(false);

  // Mark as mounted on first render
  useEffect(() => {
    setMounted(true);
  }, []);

  // Apply dark theme on mount
  useEffect(() => {
    if (mounted) {
      // Always apply dark theme
      applyTheme('dark');
    }
  }, [mounted]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  const toggleTheme = () => {
    setThemeState((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const isDark = theme === 'dark';

  return {
    theme,
    setTheme,
    toggleTheme,
    isDark,
    mounted,
  };
}
