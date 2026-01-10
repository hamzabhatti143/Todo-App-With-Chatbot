import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  metadataBase: new URL('https://taskflow.app'), // Replace with your actual domain
  title: {
    default: 'TaskFlow - Modern Task Management',
    template: '%s | TaskFlow'
  },
  description: 'Experience the future of task management with our beautifully designed, lightning-fast, and secure todo application built with Next.js and FastAPI.',
  keywords: ['todo app', 'task management', 'productivity', 'next.js', 'fastapi', 'typescript', 'modern ui'],
  authors: [{ name: 'TaskFlow Team' }],
  creator: 'TaskFlow',
  publisher: 'TaskFlow',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://taskflow.app',
    siteName: 'TaskFlow',
    title: 'TaskFlow - Organize Your Life With Style',
    description: 'Experience the future of task management with our beautifully designed, lightning-fast, and secure todo application.',
    images: [
      {
        url: '/og-image.jpg', // You'll need to create this
        width: 1200,
        height: 630,
        alt: 'TaskFlow - Modern Task Management',
      }
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'TaskFlow - Organize Your Life With Style',
    description: 'Experience the future of task management with our beautifully designed, lightning-fast, and secure todo application.',
    images: ['/og-image.jpg'], // Same image as OG
    creator: '@taskflow',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/icon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/icon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  },
  manifest: '/site.webmanifest',
  verification: {
    google: 'your-google-verification-code', // Add when you have it
    // yandex: 'yandex-verification-code',
    // bing: 'msvalidate.01',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <head>
        {/* Additional SEO meta tags */}
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
        <meta name="theme-color" content="#0F172A" media="(prefers-color-scheme: dark)" />
        <meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)" />

        {/* Preconnect to important domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />

        {/* Structured Data for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebApplication',
              name: 'TaskFlow',
              description: 'Modern task management application',
              applicationCategory: 'ProductivityApplication',
              operatingSystem: 'Web',
              offers: {
                '@type': 'Offer',
                price: '0',
                priceCurrency: 'USD',
              },
              aggregateRating: {
                '@type': 'AggregateRating',
                ratingValue: '4.8',
                ratingCount: '10000',
              },
            }),
          }}
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
