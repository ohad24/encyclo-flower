/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["images.pexels.com", "storage.googleapis.com"],
  },
  env: {
    SERVER_BASE_URL: process.env.SERVER_BASE_URL,
    IMAGE_BASE_URL: process.env.IMAGE_BASE_URL,
    IMAGE_USER_BASE_URL: process.env.IMAGE_USER_BASE_URL,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
