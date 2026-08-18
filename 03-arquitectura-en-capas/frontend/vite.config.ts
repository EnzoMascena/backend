import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo, las llamadas a /api/* van al backend FastAPI.
    // Así evitamos problemas de CORS y el frontend habla con
    // http://localhost:8000 sin tocar URLs absolutas.
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
