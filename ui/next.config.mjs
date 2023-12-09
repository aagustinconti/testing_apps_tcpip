import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

export default withBundleAnalyzer({
  output: 'standalone',
  reactStrictMode: false,
  eslint: {
    ignoreDuringBuilds: true,
  },
});
