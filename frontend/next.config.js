/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
  },

  productionBrowserSourceMaps: false,

  // ✅ MUST be top-level in Next 16
  optimizePackageImports: ['lucide-react', '@radix-ui/react-icons'],
}

module.exports = nextConfig
