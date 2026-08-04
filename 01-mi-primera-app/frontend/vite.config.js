import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy: redirige /api/* al backend en localhost:8000
    // Así el frontend puede hacer fetch("/api/tasks")
    // sin problemas de CORS ni URLs absolutas.
    //
    // EN PRODUCCIÓN: no existe este proxy. El frontend se
    // builda como archivos estáticos y se sirve desde nginx
    // o similar, que redirige /api al backend.
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
