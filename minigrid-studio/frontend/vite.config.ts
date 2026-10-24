import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Default mode: the web app talks to the FastAPI backend (dev server proxies /api to MGS_API_URL).
// Mode "demo" (`vite build --mode demo --base /app/`): in-browser demo, the engine runs in Pyodide;
// its assets come from demo-public/ (tools/web_demo/build_assets.py).
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  publicDir: mode === "demo" ? "demo-public" : "public",
  define: { "import.meta.env.VITE_DEMO": JSON.stringify(mode === "demo" ? "1" : "") },
  build: { outDir: mode === "demo" ? "dist-demo" : "dist" },
  worker: { format: "es" },
  server: {
    port: 5173,
    proxy: { "/api": process.env.MGS_API_URL ?? "http://127.0.0.1:8000" },
  },
}));
