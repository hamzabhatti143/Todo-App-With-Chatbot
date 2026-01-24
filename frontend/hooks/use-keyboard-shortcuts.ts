/**
 * Keyboard Shortcuts Hook
 * Feature: 018-chatkit-frontend - Phase 6 (Polish)
 */

import { useEffect } from "react";

interface KeyboardShortcuts {
  onEscape?: () => void;
  onNewConversation?: () => void; // Ctrl+K or Cmd+K
}

export function useKeyboardShortcuts({ onEscape, onNewConversation }: KeyboardShortcuts) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Escape key
      if (event.key === "Escape" && onEscape) {
        onEscape();
      }

      // Ctrl+K or Cmd+K for new conversation
      if ((event.ctrlKey || event.metaKey) && event.key === "k" && onNewConversation) {
        event.preventDefault();
        onNewConversation();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onEscape, onNewConversation]);
}
