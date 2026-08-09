import "dotenv/config";
import { defineConfig } from "vitest/config";
import path from "node:path";

// Separate from vitest.config.mts on purpose: this suite drives a real
// browser against a real `next start` server + local Supabase (CLAUDE.md
// §29/§30's committed E2E suite), not React components in jsdom — it
// needs a Node environment, much longer timeouts, and its own
// globalSetup to manage the server process. Run via `npm run test:e2e`.
export default defineConfig({
  test: {
    environment: "node",
    include: ["e2e/**/*.spec.ts"],
    globalSetup: ["./e2e/global-setup.ts"],
    testTimeout: 60_000,
    hookTimeout: 40_000,
    // These flows share signed-in browser state per spec file and hit
    // the same local Postgres — running spec files in parallel would
    // just contend for the same server/db without saving much wall time.
    fileParallelism: false,
  },
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "./src"),
    },
  },
});
