/**
 * Settings Page
 *
 * User settings and preferences page.
 * Allows users to manage their profile, notifications, and app preferences.
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, User, Bell, Lock, Palette, Globe, Save } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import { Container } from '@/components/layout/container';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { FadeIn } from '@/components/animations/fade-in';

export default function SettingsPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  // Load user data from localStorage on mount
  useEffect(() => {
    if (isAuthenticated) {
      const storedEmail = localStorage.getItem('user_email') || '';
      const storedName = localStorage.getItem('user_name') || 'User';
      setEmail(storedEmail);
      setName(storedName);
    }
  }, [isAuthenticated]);

  const handleSaveProfile = () => {
    setIsSaving(true);
    // Save to localStorage (in future, this will call backend API)
    localStorage.setItem('user_name', name);
    localStorage.setItem('user_email', email);

    setTimeout(() => {
      setIsSaving(false);
      alert('Profile settings saved successfully!');
    }, 500);
  };

  return (
    <Container maxWidth="lg" padding="lg">
      <div className="min-h-[60vh] space-y-6">
        <FadeIn>
          <Button
            variant="ghost"
            onClick={() => router.push('/dashboard')}
            className="mb-4 text-gray-300 hover:text-white hover:bg-slate-800/50"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </FadeIn>

        <FadeIn delay={0.1}>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-2">
            Settings
          </h1>
          <p className="text-gray-400">
            Manage your account settings and preferences
          </p>
        </FadeIn>

        <div className="space-y-6">
          {/* Profile Settings */}
          <FadeIn delay={0.15}>
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-blue-600/20 rounded-lg">
                  <User className="h-5 w-5 text-blue-400" />
                </div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Profile Settings
                </h2>
              </div>

              <div className="space-y-4">
                <div>
                  <label
                    htmlFor="name"
                    className="block text-sm font-medium text-gray-300 mb-2"
                  >
                    Full Name
                  </label>
                  <Input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your full name"
                    className="bg-slate-800/50 border-slate-700/50 text-white placeholder-gray-500"
                  />
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-300 mb-2"
                  >
                    Email Address
                  </label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="bg-slate-800/50 border-slate-700/50 text-white placeholder-gray-500"
                  />
                </div>

                <Button
                  onClick={handleSaveProfile}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white"
                  disabled={isSaving}
                >
                  <Save className="h-4 w-4 mr-2" />
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </Button>
              </div>
            </Card>
          </FadeIn>

          {/* Notifications */}
          <FadeIn delay={0.2}>
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-green-600/20 rounded-lg">
                  <Bell className="h-5 w-5 text-green-400" />
                </div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Notifications
                </h2>
              </div>

              <p className="text-gray-400 mb-4">
                Manage your notification preferences and alerts.
              </p>

              <div className="bg-green-600/10 border border-green-500/30 rounded-lg p-4">
                <p className="text-sm text-green-200 font-medium mb-2">
                  <strong>Coming Soon:</strong>
                </p>
                <ul className="space-y-1 text-sm text-green-300">
                  <li>• Email notifications for task reminders</li>
                  <li>• Push notifications for mobile app</li>
                  <li>• Daily summary emails</li>
                  <li>• Customizable notification schedules</li>
                </ul>
              </div>
            </Card>
          </FadeIn>

          {/* Security */}
          <FadeIn delay={0.25}>
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-red-600/20 rounded-lg">
                  <Lock className="h-5 w-5 text-red-400" />
                </div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Security
                </h2>
              </div>

              <p className="text-gray-400 mb-4">
                Manage your password and security settings.
              </p>

              <div className="bg-red-600/10 border border-red-500/30 rounded-lg p-4">
                <p className="text-sm text-red-200 font-medium mb-2">
                  <strong>Coming Soon:</strong>
                </p>
                <ul className="space-y-1 text-sm text-red-300">
                  <li>• Change password</li>
                  <li>• Two-factor authentication (2FA)</li>
                  <li>• Active sessions management</li>
                  <li>• Security audit log</li>
                </ul>
              </div>
            </Card>
          </FadeIn>

          {/* Appearance */}
          <FadeIn delay={0.3}>
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-600/20 rounded-lg">
                  <Palette className="h-5 w-5 text-purple-400" />
                </div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Appearance
                </h2>
              </div>

              <p className="text-gray-400 mb-4">
                Customize the look and feel of your todo app.
              </p>

              <div className="bg-purple-600/10 border border-purple-500/30 rounded-lg p-4">
                <p className="text-sm text-purple-200 mb-2">
                  <strong>Theme:</strong> Use the dark mode toggle in the navbar to switch
                  between light and dark themes.
                </p>
                <p className="text-sm text-purple-300 mt-2">
                  <strong>Coming Soon:</strong> Custom color themes, font size options,
                  and layout preferences.
                </p>
              </div>
            </Card>
          </FadeIn>

          {/* Preferences */}
          <FadeIn delay={0.35}>
            <Card padding="lg" className="bg-slate-900/50 border-slate-700/50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-indigo-600/20 rounded-lg">
                  <Globe className="h-5 w-5 text-indigo-400" />
                </div>
                <h2 className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Preferences
                </h2>
              </div>

              <p className="text-gray-400 mb-4">
                Configure your app preferences and defaults.
              </p>

              <div className="bg-indigo-600/10 border border-indigo-500/30 rounded-lg p-4">
                <p className="text-sm text-indigo-200 font-medium mb-2">
                  <strong>Coming Soon:</strong>
                </p>
                <ul className="space-y-1 text-sm text-indigo-300">
                  <li>• Language and locale settings</li>
                  <li>• Date and time format preferences</li>
                  <li>• Default task view and sorting</li>
                  <li>• Keyboard shortcuts configuration</li>
                </ul>
              </div>
            </Card>
          </FadeIn>
        </div>
      </div>
    </Container>
  );
}
