import { fileURLToPath, URL } from 'node:url'
import cssInjectedByJsPlugin from 'vite-plugin-css-injected-by-js'
import pkg from './package.json';
const path = require('path');
const { defineConfig } = require('vite');
const vue = require('@vitejs/plugin-vue');
const component = 'orbit-component-{{ project }}'
const external = Array.from(new Set([
  ...Object.keys(pkg.dependencies || {}),
  ...['vue', 'vue-router', 'pinia', 'socket.io-client']
]))

export default defineConfig({
  build: {
    sourcemap: true,
    lib: {
      entry: path.resolve(__dirname, 'index.js'),
      name: component,
      fileName: (format) => `${component}.${format}.js`,
    },
    rollupOptions: {
      external: external,
      output: [{format: "es"}],
    }
  },
  plugins: [
    vue(),
    cssInjectedByJsPlugin()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }  
});