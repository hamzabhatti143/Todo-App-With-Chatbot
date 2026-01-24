"use client";

/**
 * Chat Page - Main conversation interface with sidebar
 * Feature: 018-chatkit-frontend - Phase 4 (P2)
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";
import { ChatProvider } from "@/contexts/ChatContext";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { ConversationSidebar } from "@/components/chat/ConversationSidebar";
import { LoadingSpinner } from "@/components/chat/LoadingSpinner";
import { ArrowLeft, Menu, X } from "lucide-react";
import Link from "next/link";

export default function ChatPage() {
  const router = useRouter();
  const { isAuthenticated, loading: authLoading, userId } = useAuth();
  const [loading, setLoading] = useState(true);
  const [userIdState, setUserIdState] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("User");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    // Check authentication
    if (!authLoading && !isAuthenticated) {
      // Redirect to sign in
      router.push("/signin?redirect=/chat");
      return;
    }

    if (isAuthenticated && userId) {
      setUserIdState(userId);
      // Set user name from userId (extract from email format if present)
      if (userId.includes("@")) {
        setUserName(userId.split("@")[0]);
      } else {
        setUserName(userId);
      }
      setLoading(false);
    }
  }, [isAuthenticated, authLoading, userId, router]);

  if (loading || authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-slate-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!userIdState) {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-slate-950">
      {/* Header with Back Button and Mobile Menu Toggle */}
      <div className="p-4 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 flex items-center justify-between">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="hidden sm:inline">Back to Dashboard</span>
          <span className="sm:hidden">Back</span>
        </Link>

        {/* Mobile menu toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="md:hidden p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg"
          aria-label="Toggle conversation list"
        >
          {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        <ChatProvider userId={userIdState}>
          {/* Sidebar - Hidden on mobile, visible on desktop */}
          <aside
            className={`${
              sidebarOpen ? "block" : "hidden"
            } md:block w-full md:w-80 flex-shrink-0 absolute md:relative inset-y-0 left-0 z-10 md:z-0 top-[73px] md:top-0`}
          >
            <ConversationSidebar />
          </aside>

          {/* Chat Interface */}
          <div className="flex-1 overflow-hidden">
            <ChatInterface userId={userIdState} userName={userName} />
          </div>
        </ChatProvider>
      </div>
    </div>
  );
}
