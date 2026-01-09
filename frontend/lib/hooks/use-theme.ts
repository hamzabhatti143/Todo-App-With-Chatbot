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
}

const THEME_STORAGE_KEY = 'todo-app-theme';

/**
 * Get the initial theme from localStorage or system preference
 */
function getInitialTheme(): Theme {
  // Check if window is available (client-side)
  if (typeof window === 'undefined') {
    return 'light';
  }

  // Check localStorage first
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  if (storedTheme === 'light' || storedTheme === 'dark') {
    return storedTheme;
  }

  // Fall back to system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }

  return 'light';
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

  useEffect(() => {
    // Apply theme on mount
    applyTheme(theme);
  }, []);

  useEffect(() => {
    // Apply theme whenever it changes
    applyTheme(theme);

    // Persist to localStorage
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  useEffect(() => {
    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleChange = (e: MediaQueryListEvent) => {
      // Only update if user hasn't manually set a theme
      const hasStoredTheme = localStorage.getItem(THEME_STORAGE_KEY);
      if (!hasStoredTheme) {
        setThemeState(e.matches ? 'dark' : 'light');
      }
    };

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }

    // Legacy browsers
    mediaQuery.addListener(handleChange);
    return () => mediaQuery.removeListener(handleChange);
  }, []);

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
  };
}
