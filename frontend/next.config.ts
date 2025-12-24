import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export for production deployment
  output: 'export',

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },

  // Trailing slash for better nginx compatibility
  trailingSlash: true,
};

export default nextConfig;
