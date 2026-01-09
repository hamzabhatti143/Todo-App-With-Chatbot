/**
 * SignUp Form Component
 *
 * User registration form with email, password, confirm password,
 * Zod validation, error shake animations, and loading state.
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { signupSchema, type SignupInput } from '@/validation/user';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { PasswordStrength } from './password-strength';
import { cn } from '@/lib/utils';

interface SignupFormProps {
  onSubmit: (data: Omit<SignupInput, 'confirmPassword'>) => Promise<void>;
  onSigninClick?: () => void;
  className?: string;
}

export function SignupForm({ onSubmit, onSigninClick, className }: SignupFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof SignupInput, string>>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (field: keyof SignupInput) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [field]: e.target.value }));
    // Clear error for this field when user types
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate with Zod
    const result = signupSchema.safeParse(formData);

    if (!result.success) {
      const fieldErrors: Partial<Record<keyof SignupInput, string>> = {};
      result.error.errors.forEach((error) => {
        const field = error.path[0] as keyof SignupInput;
        if (!fieldErrors[field]) {
          fieldErrors[field] = error.message;
        }
      });
      setErrors(fieldErrors);
      return;
    }

    try {
      setIsSubmitting(true);
      await onSubmit({
        email: result.data.email,
        password: result.data.password,
      });
    } catch (error) {
      setErrors({ email: 'An error occurred. Please try again.' });
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

      {/* Password Input with Strength Indicator */}
      <div className="space-y-2">
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

        {/* Password Strength Indicator */}
        <PasswordStrength password={formData.password} />
      </div>

      {/* Confirm Password Input */}
      <div className="relative">
        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none z-10" />
        <Input
          type={showConfirmPassword ? 'text' : 'password'}
          value={formData.confirmPassword}
          onChange={handleChange('confirmPassword')}
          error={errors.confirmPassword}
          className="pl-10 pr-10"
          placeholder="Confirm password"
          required
          disabled={isSubmitting}
        />
        <button
          type="button"
          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          tabIndex={-1}
        >
          {showConfirmPassword ? (
            <EyeOff className="h-5 w-5" />
          ) : (
            <Eye className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        className="w-full"
        loading={isSubmitting}
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Creating account...' : 'Create account'}
      </Button>

      {/* Sign In Link */}
      {onSigninClick && (
        <p className="text-center text-sm text-gray-600 dark:text-gray-400">
          Already have an account?{' '}
          <button
            type="button"
            onClick={onSigninClick}
            className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
          >
            Sign in
          </button>
        </p>
      )}
    </motion.form>
  );
}
