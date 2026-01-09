/**
 * SignIn Form Component
 *
 * User login form with email, password, remember-me checkbox,
 * Zod validation, error shake animations, and loading state.
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { signinSchema, type SigninInput } from '@/validation/user';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';

interface SigninFormProps {
  onSubmit: (data: SigninInput) => Promise<void>;
  onSignupClick?: () => void;
  className?: string;
}

export function SigninForm({ onSubmit, onSignupClick, className }: SigninFormProps) {
  const [formData, setFormData] = useState<SigninInput>({
    email: '',
    password: '',
    rememberMe: false,
  });
  const [errors, setErrors] = useState<Partial<Record<keyof SigninInput, string>>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (field: keyof SigninInput) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
    // Clear error for this field when user types
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleRememberMeChange = (checked: boolean) => {
    setFormData((prev) => ({ ...prev, rememberMe: checked }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate with Zod
    const result = signinSchema.safeParse(formData);

    if (!result.success) {
      const fieldErrors: Partial<Record<keyof SigninInput, string>> = {};
      result.error.errors.forEach((error) => {
        const field = error.path[0] as keyof SigninInput;
        if (!fieldErrors[field]) {
          fieldErrors[field] = error.message;
        }
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      setIsSubmitting(true);
      await onSubmit(result.data);
    } catch (error) {
      setErrors({ email: 'Invalid email or password. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className={cn('space-y-6', className)}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      {/* Email Input */}
      <div className="relative">
        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none z-10" />
        <Input
          type="email"
          value={formData.email}
          onChange={handleChange('email')}
          error={errors.email}
          className="pl-10"
          placeholder="Email address"
          required
          disabled={isSubmitting}
        />
      </div>

      {/* Password Input */}
      <div className="relative">
        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none z-10" />
        <Input
          type={showPassword ? 'text' : 'password'}
          value={formData.password}
          onChange={handleChange('password')}
          error={errors.password}
          className="pl-10 pr-10"
          placeholder="Password"
          required
          disabled={isSubmitting}
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          tabIndex={-1}
        >
          {showPassword ? (
            <EyeOff className="h-5 w-5" />
          ) : (
            <Eye className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* Remember Me & Forgot Password */}
      <div className="flex items-center justify-between">
        <Checkbox
          id="rememberMe"
          checked={formData.rememberMe}
          onCheckedChange={handleRememberMeChange}
          label="Remember me"
          disabled={isSubmitting}
        />

        <button
          type="button"
          className="text-sm font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
          disabled={isSubmitting}
        >
          Forgot password?
        </button>
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full"
        loading={isSubmitting}
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </Button>

      {/* Sign Up Link */}
      {onSignupClick && (
        <p className="text-center text-sm text-gray-600 dark:text-gray-400">
          Don't have an account?{' '}
          <button
            type="button"
            onClick={onSignupClick}
            className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
          >
            Sign up
          </button>
        </p>
      )}
    </motion.form>
  );
}
