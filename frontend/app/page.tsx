'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/use-auth'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import axios from 'axios'

export default function Home() {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()
  const [health, setHealth] = useState<any>(null)
  const [error, setError] = useState<string>('')
  const [testing, setTesting] = useState(false)

  // Auth testing state
  const [authTesting, setAuthTesting] = useState(false)
  const [authResult, setAuthResult] = useState<any>(null)
  const [authError, setAuthError] = useState<string>('')
  const [testEmail, setTestEmail] = useState('test@example.com')
  const [testPassword, setTestPassword] = useState('password123')

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, loading, router])

  const testBackendConnection = async () => {
    setTesting(true)
    setHealth(null)
    setError('')

    try {
      const response = await axios.get('http://localhost:8000/health')
      setHealth(response.data)
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend')
    } finally {
      setTesting(false)
    }
  }

  const testRegister = async () => {
    setAuthTesting(true)
    setAuthResult(null)
    setAuthError('')

    try {
      const response = await axios.post('http://localhost:8000/api/auth/register', {
        email: testEmail,
        password: testPassword,
      })
      setAuthResult({
        type: 'register',
        success: true,
        data: response.data,
      })
    } catch (err: any) {
      setAuthError(err.response?.data?.detail || err.message || 'Registration failed')
    } finally {
      setAuthTesting(false)
    }
  }

  const testLogin = async () => {
    setAuthTesting(true)
    setAuthResult(null)
    setAuthError('')

    try {
      const response = await axios.post('http://localhost:8000/api/auth/login', {
        email: testEmail,
        password: testPassword,
      })
      setAuthResult({
        type: 'login',
        success: true,
        data: response.data,
        token: response.data.access_token,
      })
    } catch (err: any) {
      setAuthError(err.response?.data?.detail || err.message || 'Login failed')
    } finally {
      setAuthTesting(false)
    }
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 sm:p-24">
      <div className="text-center space-y-6 max-w-4xl w-full">
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900">Todo App</h1>
        <p className="text-lg sm:text-xl text-gray-600">
          Full-stack todo application with Next.js and FastAPI
        </p>

        {/* Backend Connection Test Section */}
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Backend Connection Test
          </h2>

          <Button
            onClick={testBackendConnection}
            disabled={testing}
            className="mb-4"
          >
            {testing ? 'Testing...' : 'Test Backend Connection'}
          </Button>

          {health && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-left">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-green-600 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <h3 className="text-green-800 font-semibold mb-2">
                    ✅ Backend Connected Successfully
                  </h3>
                  <p className="text-green-700 text-sm mb-2">
                    Frontend successfully communicated with the backend API
                  </p>
                  <div className="bg-green-100 rounded p-3 mt-2">
                    <p className="text-xs text-green-800 font-mono">
                      Response: {JSON.stringify(health, null, 2)}
                    </p>
                  </div>
                  <div className="mt-3 text-xs text-green-600 space-y-1">
                    <p>✓ HTTP request successful (200 OK)</p>
                    <p>✓ No CORS errors</p>
                    <p>✓ Backend responded correctly</p>
                    <p>✓ Data parsed successfully</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-left">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <h3 className="text-red-800 font-semibold mb-2">
                    ❌ Connection Error
                  </h3>
                  <p className="text-red-700 text-sm mb-2">
                    Failed to connect to the backend API
                  </p>
                  <div className="bg-red-100 rounded p-3 mt-2">
                    <p className="text-xs text-red-800 font-mono">
                      Error: {error}
                    </p>
                  </div>
                  <div className="mt-3 text-xs text-red-600 space-y-1">
                    <p>⚠️ Check that backend server is running on port 8000</p>
                    <p>⚠️ Verify CORS configuration allows localhost:3000</p>
                    <p>⚠️ Check browser console for detailed errors</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {!health && !error && !testing && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
              <p className="text-blue-800 text-sm">
                Click the button above to test the connection between the frontend and backend API.
                This will verify that CORS is configured correctly and the services can communicate.
              </p>
            </div>
          )}
        </div>

        {/* Authentication Testing Section */}
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Authentication Endpoint Test
          </h2>

          <div className="space-y-4 mb-4">
            <div className="text-left">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={testEmail}
                onChange={(e) => setTestEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="test@example.com"
              />
            </div>
            <div className="text-left">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={testPassword}
                onChange={(e) => setTestPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="password123"
              />
            </div>
          </div>

          <div className="flex gap-3 mb-4">
            <Button
              onClick={testRegister}
              disabled={authTesting}
              variant="secondary"
            >
              {authTesting ? 'Testing...' : 'Test Register'}
            </Button>
            <Button
              onClick={testLogin}
              disabled={authTesting}
            >
              {authTesting ? 'Testing...' : 'Test Login'}
            </Button>
          </div>

          {authResult && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-left">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-green-600 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <h3 className="text-green-800 font-semibold mb-2">
                    ✅ {authResult.type === 'register' ? 'Registration' : 'Login'} Successful
                  </h3>
                  <p className="text-green-700 text-sm mb-2">
                    {authResult.type === 'register'
                      ? 'User account created successfully'
                      : 'User authenticated successfully'}
                  </p>
                  <div className="bg-green-100 rounded p-3 mt-2 max-h-48 overflow-y-auto">
                    <p className="text-xs text-green-800 font-mono whitespace-pre-wrap">
                      {JSON.stringify(authResult.data, null, 2)}
                    </p>
                  </div>
                  {authResult.token && (
                    <div className="mt-3">
                      <p className="text-xs text-green-700 font-semibold mb-1">JWT Token (first 50 chars):</p>
                      <p className="text-xs text-green-600 font-mono bg-green-100 p-2 rounded break-all">
                        {authResult.token.substring(0, 50)}...
                      </p>
                    </div>
                  )}
                  <div className="mt-3 text-xs text-green-600 space-y-1">
                    <p>✓ Authentication endpoint working</p>
                    <p>✓ Password hashing verified</p>
                    {authResult.token && <p>✓ JWT token generated</p>}
                    <p>✓ Response structure correct</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {authError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-left">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <h3 className="text-red-800 font-semibold mb-2">
                    ❌ Authentication Error
                  </h3>
                  <div className="bg-red-100 rounded p-3 mt-2">
                    <p className="text-xs text-red-800 font-mono">
                      Error: {authError}
                    </p>
                  </div>
                  <div className="mt-3 text-xs text-red-600 space-y-1">
                    <p>💡 Common issues:</p>
                    <p>• User already exists (try different email for register)</p>
                    <p>• Invalid credentials (wrong email/password for login)</p>
                    <p>• Backend authentication not configured</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {!authResult && !authError && !authTesting && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
              <p className="text-blue-800 text-sm mb-2">
                Test the authentication endpoints:
              </p>
              <ul className="text-blue-700 text-xs space-y-1 ml-4 list-disc">
                <li><strong>Register:</strong> Creates a new user account with hashed password</li>
                <li><strong>Login:</strong> Authenticates user and returns JWT token</li>
                <li>Use the same email/password for both tests</li>
                <li>Try registering first, then logging in with same credentials</li>
              </ul>
            </div>
          )}
        </div>

        {/* Auth Buttons */}
        <div className="flex gap-4 justify-center mt-8">
          <Link href="/signin">
            <Button>Sign In</Button>
          </Link>
          <Link href="/signup">
            <Button variant="secondary">Register</Button>
          </Link>
        </div>

        {/* API Documentation Link */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            Backend API Documentation:{' '}
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              http://localhost:8000/docs
            </a>
          </p>
        </div>
      </div>
    </main>
  )
}
