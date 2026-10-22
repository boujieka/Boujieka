import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  worker: { format: "es" },
  build: {
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: { manualChunks: { echarts: ["echarts"], maplibre: ["maplibre-gl"] } },
    },
  },
  test: { environment: "node", include: ["src/**/*.test.ts"] },
});
