import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "https://ec528-fall-2023.github.io/Evolution-of-Kubernetes-/",
})
