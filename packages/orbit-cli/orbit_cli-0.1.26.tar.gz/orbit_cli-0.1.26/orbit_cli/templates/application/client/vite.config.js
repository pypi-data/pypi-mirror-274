import { fileURLToPath, URL } from 'node:url'
import { defineConfig, searchForWorkspaceRoot } from 'vite'
import vue from '@vitejs/plugin-vue'
import requireTransform from 'vite-plugin-require-transform';
import basicSsl from '@vitejs/plugin-basic-ssl';
import cssInjectedByJsPlugin from 'vite-plugin-css-injected-by-js'

export default defineConfig({
  plugins: [
    vue(),
    requireTransform({}),
    basicSsl(),
    cssInjectedByJsPlugin()
  ],
  server: {
    host: '0.0.0.0',
    https: true,
    hmr: {
      protocol: 'wss',
      host: 'localhost',
      clientPort: 5173
    },
    fs: {
      allow: [
        searchForWorkspaceRoot(process.cwd()),
      ]
    }
  },
  build: {
    sourcemap: true,
    chunkSizeWarningLimit: 4096,
    commonjsOptions: {
      esmExternals: true 
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  }
})











