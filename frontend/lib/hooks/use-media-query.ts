'use client';

/**
 * useMediaQuery Hook
 *
 * Reactive hook for responsive breakpoints and media queries.
 * Automatically updates on window resize.
 */

import { useEffect, useState } from 'react';

/**
 * useMediaQuery hook for responsive breakpoints
 *
 * @param {string} query - CSS media query string
 * @returns {boolean} Whether the media query matches
 *
 * @example
 * ```tsx
 * function ResponsiveComponent() {
 *   const isMobile = useMediaQuery('(max-width: 640px)');
 *   const isTablet = useMediaQuery('(min-width: 641px) and (max-width: 1024px)');
 *   const isDark = useMediaQuery('(prefers-color-scheme: dark)');
 *
 *   return (
 *     <div>
 *       {isMobile && <MobileView />}
 *       {isTablet && <TabletView />}
 *       {!isMobile && !isTablet && <DesktopView />}
 *     </div>
 *   );
 * }
 * ```
 */
export function useMediaQuery(query: string): boolean {
  // Initialize with false for SSR safety
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    // Check if window is available (client-side only)
    if (typeof window === 'undefined') {
      return;
    }

    const mediaQuery = window.matchMedia(query);

    // Set initial value
    setMatches(mediaQuery.matches);

    // Create event handler
    const handleChange = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    // Modern browsers support addEventListener
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }

    // Legacy browsers use addListener
    mediaQuery.addListener(handleChange);
    return () => mediaQuery.removeListener(handleChange);
  }, [query]);

  return matches;
}

/**
 * Predefined breakpoint hooks for common screen sizes
 * Based on Tailwind CSS default breakpoints
 */

/**
 * Check if screen width is extra small (< 640px)
 */
export function useIsXs(): boolean {
  return useMediaQuery('(max-width: 639px)');
}

/**
 * Check if screen width is small or larger (>= 640px)
 */
export function useIsSm(): boolean {
  return useMediaQuery('(min-width: 640px)');
}

/**
 * Check if screen width is medium or larger (>= 768px)
 */
export function useIsMd(): boolean {
  return useMediaQuery('(min-width: 768px)');
}

/**
 * Check if screen width is large or larger (>= 1024px)
 */
export function useIsLg(): boolean {
  return useMediaQuery('(min-width: 1024px)');
}

/**
 * Check if screen width is extra large or larger (>= 1280px)
 */
export function useIsXl(): boolean {
  return useMediaQuery('(min-width: 1280px)');
}

/**
 * Check if screen width is 2xl or larger (>= 1536px)
 */
export function useIs2Xl(): boolean {
  return useMediaQuery('(min-width: 1536px)');
}

/**
 * Check if user prefers dark color scheme
 */
export function usePrefersColorSchemeDark(): boolean {
  return useMediaQuery('(prefers-color-scheme: dark)');
}

/**
 * Check if user prefers reduced motion
 */
export function usePrefersReducedMotion(): boolean {
  return useMediaQuery('(prefers-reduced-motion: reduce)');
}
