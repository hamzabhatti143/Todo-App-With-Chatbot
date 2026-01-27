'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/use-auth'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { motion, useReducedMotion } from 'framer-motion'
import {
  Zap,
  Shield,
  Smartphone,
  ArrowRight,
  Sparkles,
  Layers,
  Cloud,
  Lock,
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'
import { Floating3D, Cube3D, Sphere3D, Card3DTilt } from '@/components/animations/floating-3d'

export default function Home() {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const prefersReducedMotion = useReducedMotion()

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, loading, router])

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Loading...</p>
        </motion.div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 relative overflow-hidden">
      {/* Professional Navbar */}
      <ProfessionalNavbar
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
      />

      {/* Animated Background Gradients */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-0 -left-4 w-96 h-96 bg-blue-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={!prefersReducedMotion ? {
            scale: [1, 1.1, 1],
            x: [0, 30, 0],
            y: [0, -50, 0],
          } : {}}
          transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute top-0 -right-4 w-96 h-96 bg-purple-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={!prefersReducedMotion ? {
            scale: [1, 1.2, 1],
            x: [0, -30, 0],
            y: [0, 50, 0],
          } : {}}
          transition={{ duration: 9, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        />
        <motion.div
          className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500/10 rounded-full mix-blend-multiply filter blur-3xl"
          animate={!prefersReducedMotion ? {
            scale: [1, 0.9, 1],
            x: [0, 50, 0],
            y: [0, -30, 0],
          } : {}}
          transition={{ duration: 11, repeat: Infinity, ease: "easeInOut", delay: 4 }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 pt-24">
        {/* Hero Section */}
        <section className="container mx-auto px-4 pt-12 pb-32 sm:pt-20 sm:pb-40 relative">
          {/* 3D Floating Shapes in Background */}
          <div className="absolute top-20 right-10 hidden lg:block">
            <Floating3D delay={0} duration={8} intensity="medium">
              <Sphere3D size={120} gradient="from-blue-400 via-purple-500 to-pink-500" speed={15} />
            </Floating3D>
          </div>

          <div className="absolute top-40 left-10 hidden lg:block">
            <Floating3D delay={1} duration={10} intensity="low">
              <Cube3D size={80} speed={25} />
            </Floating3D>
          </div>

          <div className="absolute bottom-20 right-20 hidden lg:block">
            <Floating3D delay={0.5} duration={12} intensity="high">
              <Sphere3D size={100} gradient="from-cyan-400 via-blue-500 to-purple-500" speed={12} />
            </Floating3D>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-5xl mx-auto relative z-10"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              whileHover={{ scale: 1.05 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 backdrop-blur-sm mb-8 cursor-default"
            >
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span className="text-sm font-medium bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Modern Task Management
              </span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight"
            >
              <span className="bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
                Organize Your Life
              </span>
              <br />
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                With Style
              </span>
            </motion.h1>

            {/* Subheading */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-xl sm:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed"
            >
              Experience the future of task management with our beautifully designed,
              lightning-fast, and secure todo application built with Next.js and FastAPI
            </motion.p>

            {/* CTA Buttons with 3D Effects */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
              style={{ perspective: '1000px' }}
            >
              <Link href="/signup">
                <motion.div
                  whileHover={{
                    scale: 1.05,
                    rotateX: -5,
                    rotateY: 5,
                  }}
                  whileTap={{ scale: 0.95 }}
                  style={{ transformStyle: 'preserve-3d' }}
                >
                  <Button
                    size="lg"
                    className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 rounded-xl text-lg font-semibold shadow-2xl shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40"
                    style={{ transform: 'translateZ(30px)' }}
                  >
                    Get Started Free
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </motion.div>
              </Link>
              <Link href="/signin">
                <motion.div
                  whileHover={{
                    scale: 1.05,
                    rotateX: -5,
                    rotateY: -5,
                  }}
                  whileTap={{ scale: 0.95 }}
                  style={{ transformStyle: 'preserve-3d' }}
                >
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 rounded-xl text-lg font-semibold shadow-2xl shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40"
                    style={{ transform: 'translateZ(30px)' }}
                  >
                    Sign In
                  </Button>
                </motion.div>
              </Link>
            </motion.div>

            {/* Stats with 3D Effects */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto"
              style={{ perspective: '1000px' }}
            >
              {[
                { label: 'Active Users', value: '10K+' },
                { label: 'Tasks Completed', value: '1M+' },
                { label: 'Success Rate', value: '99.9%' },
              ].map((stat, index) => (
                <motion.div
                  key={index}
                  className="text-center"
                  style={{ transformStyle: 'preserve-3d' }}
                  whileHover={{
                    scale: 1.15,
                    rotateY: 10,
                    rotateX: -10,
                  }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <div
                    className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2"
                    style={{ transform: 'translateZ(40px)' }}
                  >
                    {stat.value}
                  </div>
                  <div
                    className="text-sm text-gray-500"
                    style={{ transform: 'translateZ(20px)' }}
                  >
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-4 pb-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">
              <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Powerful Features
              </span>
            </h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Everything you need to stay productive and organized
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <FeatureCard
              icon={<Zap className="w-8 h-8" />}
              title="Lightning Fast"
              description="Built with Next.js 15 and optimized for speed. Experience instant loading and smooth interactions."
              gradient="from-yellow-500 to-orange-500"
              delay={0}
            />

            <FeatureCard
              icon={<Shield className="w-8 h-8" />}
              title="Secure by Default"
              description="JWT authentication, encrypted data, and secure API endpoints keep your tasks safe and private."
              gradient="from-blue-500 to-cyan-500"
              delay={0.1}
            />

            <FeatureCard
              icon={<Smartphone className="w-8 h-8" />}
              title="Mobile Optimized"
              description="Responsive design that works flawlessly on all devices. Manage tasks anywhere, anytime."
              gradient="from-purple-500 to-pink-500"
              delay={0.2}
            />

            <FeatureCard
              icon={<Layers className="w-8 h-8" />}
              title="Smart Organization"
              description="Advanced filtering, sorting, and search capabilities to find exactly what you need."
              gradient="from-green-500 to-emerald-500"
              delay={0.3}
            />

            <FeatureCard
              icon={<Cloud className="w-8 h-8" />}
              title="Cloud Sync"
              description="Your tasks are synced across all devices in real-time with our robust backend."
              gradient="from-indigo-500 to-blue-500"
              delay={0.4}
            />

            <FeatureCard
              icon={<Lock className="w-8 h-8" />}
              title="Privacy First"
              description="Your data belongs to you. We use industry-standard encryption and never share your information."
              gradient="from-red-500 to-rose-500"
              delay={0.5}
            />
          </div>
        </section>

        {/* Tech Stack Section with 3D Parallax */}
        <section className="container mx-auto px-4 pb-32 relative">
          {/* Additional 3D floating elements */}
          <div className="absolute top-10 left-5 hidden md:block opacity-50">
            <Floating3D delay={0.3} duration={14} intensity="low">
              <Cube3D size={60} speed={30} />
            </Floating3D>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto relative z-10"
            style={{ perspective: '1500px' }}
          >
            <motion.div
              className="glass-card p-12 text-center bg-slate-900/50 border-slate-700/50"
              style={{ transformStyle: 'preserve-3d' }}
              whileInView={{
                rotateX: [5, 0],
                rotateY: [5, 0],
              }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h3
                className="text-3xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
                style={{ transform: 'translateZ(50px)' }}
              >
                Built with Modern Technology
              </h3>
              <p
                className="text-gray-400 mb-8 text-lg"
                style={{ transform: 'translateZ(30px)' }}
              >
                Leveraging the latest and greatest in web development
              </p>
              <div
                className="grid grid-cols-2 md:grid-cols-4 gap-6"
                style={{ transform: 'translateZ(20px)' }}
              >
                {[
                  { name: 'Next.js 15', color: 'from-white to-gray-400' },
                  { name: 'TypeScript', color: 'from-blue-400 to-blue-600' },
                  { name: 'FastAPI', color: 'from-green-400 to-emerald-600' },
                  { name: 'PostgreSQL', color: 'from-blue-300 to-cyan-500' },
                ].map((tech, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{
                      scale: 1.15,
                      rotateY: 15,
                      rotateX: -15,
                    }}
                    style={{
                      transformStyle: 'preserve-3d',
                      transform: `translateZ(${40 + index * 10}px)`,
                    }}
                    className="px-4 py-3 rounded-lg bg-slate-800/50 border border-slate-700/50 hover:border-slate-600/50 transition-all cursor-default"
                  >
                    <span className={`font-semibold bg-gradient-to-r ${tech.color} bg-clip-text text-transparent`}>
                      {tech.name}
                    </span>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* CTA Section with 3D Effects */}
        <section className="container mx-auto px-4 pb-32 relative">
          {/* Final 3D floating sphere */}
          <div className="absolute bottom-10 left-10 hidden lg:block opacity-60">
            <Floating3D delay={0.7} duration={9} intensity="medium">
              <Sphere3D size={90} gradient="from-pink-400 via-purple-500 to-blue-500" speed={14} />
            </Floating3D>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center relative z-10"
            style={{ perspective: '1200px' }}
          >
            <motion.div
              className="glass-card p-12 bg-slate-900/50 border-2 border-slate-700/50"
              style={{ transformStyle: 'preserve-3d' }}
              whileInView={{
                rotateX: [-5, 0],
                scale: [0.95, 1],
              }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h3
                className="text-4xl font-bold mb-4 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent"
                style={{ transform: 'translateZ(60px)' }}
              >
                Ready to Get Started?
              </h3>
              <p
                className="text-gray-400 text-lg mb-8"
                style={{ transform: 'translateZ(40px)' }}
              >
                Join thousands of users who are already organizing their life with style
              </p>
              <div style={{ transform: 'translateZ(50px)' }}>
                <Link href="/signup">
                  <motion.div
                    whileHover={{
                      scale: 1.1,
                      rotateX: -10,
                      rotateY: 5,
                    }}
                    whileTap={{ scale: 0.95 }}
                    style={{ transformStyle: 'preserve-3d' }}
                  >
                    <Button
                      size="lg"
                      className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 rounded-xl text-lg font-semibold shadow-2xl shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40"
                    >
                      Create Free Account
                      <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </motion.div>
                </Link>
              </div>
            </motion.div>
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="container mx-auto px-4 py-12 border-t border-slate-800/50">
          <div className="text-center text-gray-500 text-sm">
            <p className="mb-2">
              © 2025 Modern Todo App. Built with{' '}
              <span className="text-red-400">♥</span> using Next.js & FastAPI
            </p>
            <p>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 transition-colors"
              >
                API Documentation
              </a>
            </p>
          </div>
        </footer>
      </div>
    </main>
  )
}

// Professional Navbar Component
interface ProfessionalNavbarProps {
  mobileMenuOpen: boolean
  setMobileMenuOpen: (open: boolean) => void
}

function ProfessionalNavbar({ mobileMenuOpen, setMobileMenuOpen }: ProfessionalNavbarProps) {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, type: "spring" }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/50 shadow-lg'
          : 'bg-transparent'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                TaskFlow
              </span>
            </Link>
          </motion.div>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            <Link href="#features">
              <motion.span
                whileHover={{ scale: 1.05 }}
                className="text-gray-300 hover:text-white transition-colors cursor-pointer"
              >
                Features
              </motion.span>
            </Link>
            <Link href="http://localhost:8000/docs" target="_blank">
              <motion.span
                whileHover={{ scale: 1.05 }}
                className="text-gray-300 hover:text-white transition-colors cursor-pointer"
              >
                API Docs
              </motion.span>
            </Link>

            <Link href="/signin">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Sign In
                </Button>
              </motion.div>
            </Link>
            <Link href="/signup">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Get Started
                </Button>
              </motion.div>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg bg-slate-800/50"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </motion.button>
        </div>

        {/* Mobile Menu */}
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{
            height: mobileMenuOpen ? 'auto' : 0,
            opacity: mobileMenuOpen ? 1 : 0,
          }}
          transition={{ duration: 0.3 }}
          className="md:hidden overflow-hidden"
        >
          <div className="py-4 space-y-4">
            <Link href="#features" className="block text-gray-300 hover:text-white">
              Features
            </Link>
            <Link href="http://localhost:8000/docs" target="_blank" className="block text-gray-300 hover:text-white">
              API Docs
            </Link>
            <Link href="/signin" className="block">
              <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600">Sign In</Button>
            </Link>
            <Link href="/signup" className="block">
              <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600">Get Started</Button>
            </Link>
          </div>
        </motion.div>
      </div>
    </motion.nav>
  )
}

// Feature Card Component with improved dark theme colors
interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
  gradient: string
  delay: number
}

function FeatureCard({ icon, title, description, gradient, delay }: FeatureCardProps) {
  const prefersReducedMotion = useReducedMotion()
  const [rotateX, setRotateX] = useState(0)
  const [rotateY, setRotateY] = useState(0)

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (prefersReducedMotion) return

    const card = e.currentTarget
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const centerX = rect.width / 2
    const centerY = rect.height / 2

    const rotateXValue = ((y - centerY) / centerY) * 10
    const rotateYValue = ((centerX - x) / centerX) * 10

    setRotateX(-rotateXValue)
    setRotateY(rotateYValue)
  }

  const handleMouseLeave = () => {
    setRotateX(0)
    setRotateY(0)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay, duration: 0.5 }}
      className="group relative"
      style={{
        perspective: '1000px',
      }}
    >
      <motion.div
        className="relative"
        style={{
          transformStyle: 'preserve-3d',
        }}
        animate={{
          rotateX: rotateX,
          rotateY: rotateY,
        }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        whileHover={{ scale: 1.05 }}
      >
        <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-300 -z-10"
             style={{ background: `linear-gradient(to right, var(--tw-gradient-stops))` }} />
        <div
          className="glass-card p-8 h-full hover:border-slate-600/50 transition-all duration-300 bg-slate-900/50 border-slate-700/50"
          style={{
            transform: 'translateZ(50px)',
          }}
        >
          <motion.div
            whileHover={!prefersReducedMotion ? { rotateZ: 360 } : {}}
            transition={{ duration: 0.5 }}
            className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${gradient} mb-4`}
            style={{
              transform: 'translateZ(75px)',
            }}
          >
            <div className="text-white">
              {icon}
            </div>
          </motion.div>
          <h3 className="text-xl font-bold mb-3 text-white" style={{ transform: 'translateZ(60px)' }}>
            {title}
          </h3>
          <p className="text-gray-400 leading-relaxed" style={{ transform: 'translateZ(40px)' }}>
            {description}
          </p>
        </div>
      </motion.div>
    </motion.div>
  )
}
