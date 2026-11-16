import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  // Puerto fijo: es el origen que el backend habilita por CORS
  server: { port: 5173, strictPort: true },
});
