import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: false,
    minify: "esbuild",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: process.env.VITE_API_URL || "http://localhost:5000",
        changeOrigin: true,
        secure: false, // Allow self-signed certificates in dev
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.error('❌ Proxy error:', err.message);
            console.error('   Make sure backend is running on http://localhost:5000');
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('🔄 Proxying:', req.method, req.url, '->', proxyReq.path);
          });
        },
      },
    },
  },
});