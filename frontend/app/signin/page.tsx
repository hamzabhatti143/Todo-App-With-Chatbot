/**
 * Sign In Page
 *
 * User login page with modern dark theme matching home page,
 * gradient backgrounds, and smooth animations.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { SigninForm } from '@/components/auth/signin-form';
import { SuccessCheckmark } from '@/components/animations/checkmark-draw';
import { FadeIn } from '@/components/animations/fade-in';
import { useAuth } from '@/hooks/use-auth';
import type { SigninInput } from '@/validation/user';
import { Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function SignInPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (data: SigninInput) => {
    const result = await login({ email: data.email, password: data.password });

    if (!result.success) {
      throw new Error(result.error || 'Login failed');
    }

    // Show success animation
    setShowSuccess(true);

    // Redirect to dashboard after animation
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 relative overflow-hidden">
      {/* Animated Background Gradients - Same as Home Page */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-0 -left-4 w-96 h-96 bg-blue-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{
            scale: [1, 1.1, 1],
            x: [0, 30, 0],
            y: [0, -50, 0],
          }}
          transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute top-0 -right-4 w-96 h-96 bg-purple-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            x: [0, -30, 0],
            y: [0, 50, 0],
          }}
          transition={{ duration: 9, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        />
        <motion.div
          className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={{
            scale: [1, 0.9, 1],
            x: [0, 50, 0],
            y: [0, -30, 0],
          }}
          transition={{ duration: 11, repeat: Infinity, ease: "easeInOut", delay: 4 }}
        />
      </div>

      <FadeIn className="w-full max-w-md relative z-10">
        <AnimatePresence mode="wait">
          {!showSuccess ? (
            <motion.div
              key="form"
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
            >
              {/* Logo/Brand */}
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="text-center mb-8"
              >
                <Link href="/" className="inline-flex items-center gap-2">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                    <Sparkles className="w-7 h-7 text-white" />
                  </div>
                  <span className="text-2xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                    TaskFlow
                  </span>
                </Link>
              </motion.div>

              {/* Card with Dark Theme */}
              <div className="glass-card p-8 shadow-2xl bg-slate-900/50 border-slate-700/50">
                {/* Header */}
                <div className="text-center mb-8">
                  <motion.h1
                    className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                  >
                    Welcome back
                  </motion.h1>
                  <motion.p
                    className="mt-2 text-gray-400"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                  >
                    Sign in to your account to continue
                  </motion.p>
                </div>

                {/* Form */}
                <SigninForm
                  onSubmit={handleSubmit}
                  onSignupClick={() => router.push('/signup')}
                />
              </div>

              {/* Footer Link */}
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="mt-6 text-center text-sm text-gray-500"
              >
                Don't have an account?{' '}
                <Link
                  href="/signup"
                  className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                >
                  Sign up for free
                </Link>
              </motion.p>
            </motion.div>
          ) : (
            <motion.div
              key="success"
              className="flex flex-col items-center justify-center py-12"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <SuccessCheckmark size={96} onComplete={() => {}} />
              <motion.p
                className="mt-6 text-xl font-semibold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.4 }}
              >
                Welcome back!
              </motion.p>
              <motion.p
                className="mt-2 text-gray-400"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.5 }}
              >
                Redirecting to dashboard...
              </motion.p>
            </motion.div>
          )}
        </AnimatePresence>
      </FadeIn>
    </div>
  );
}
