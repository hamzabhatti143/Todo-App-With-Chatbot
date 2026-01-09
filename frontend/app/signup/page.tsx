/**
 * Sign Up Page
 *
 * User registration page with SignUpForm component, page fade-in animation,
 * API integration, and success animation before redirect.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { SignupForm } from '@/components/auth/signup-form';
import { SuccessCheckmark } from '@/components/animations/checkmark-draw';
import { FadeIn } from '@/components/animations/fade-in';
import { Card } from '@/components/ui/card';
import { useAuth } from '@/hooks/use-auth';

export default function SignUpPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (data: { email: string; password: string }) => {
    const result = await register(data);

    if (!result.success) {
      throw new Error(result.error || 'Registration failed');
    }

    // Show success animation
    setShowSuccess(true);

    // Redirect to dashboard after animation
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Background Pattern */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-200/20 to-transparent dark:from-blue-900/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-purple-200/20 to-transparent dark:from-purple-900/20 rounded-full blur-3xl" />
      </div>

      <FadeIn className="w-full max-w-md relative z-10">
        <AnimatePresence mode="wait">
          {!showSuccess ? (
            <motion.div
              key="form"
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
            >
              <Card variant="glass" padding="lg" className="shadow-2xl">
                {/* Header */}
                <div className="text-center mb-8">
                  <motion.h1
                    className="text-3xl font-bold text-gray-900 dark:text-gray-100"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                  >
                    Create your account
                  </motion.h1>
                  <motion.p
                    className="mt-2 text-gray-600 dark:text-gray-400"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                  >
                    Get started with your free account
                  </motion.p>
                </div>

                {/* Form */}
                <SignupForm
                  onSubmit={handleSubmit}
                  onSigninClick={() => router.push('/signin')}
                />
              </Card>
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
                className="mt-6 text-xl font-semibold text-gray-900 dark:text-gray-100"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.4 }}
              >
                Account created successfully!
              </motion.p>
              <motion.p
                className="mt-2 text-gray-600 dark:text-gray-400"
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
