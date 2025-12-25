import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output for production deployment with Node.js server
  output: 'standalone',

  // Disable image optimization for better performance
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
