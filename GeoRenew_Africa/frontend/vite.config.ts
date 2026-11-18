/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En développement, l'API FastAPI tourne sur le port 8000 ; le navigateur ne parle qu'à Vite.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": process.env.GEORENEW_API ?? "http://127.0.0.1:8000" } },
  test: { environment: "node" },
});
