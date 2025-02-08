import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // Ou outra porta se precisar
    proxy: {
      '/api': 'http://127.0.0.1:5000', // Ajuste conforme o backend
    },
  },
});
