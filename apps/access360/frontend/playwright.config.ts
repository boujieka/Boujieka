import { defineConfig, devices } from "@playwright/test";

const FRONTEND = process.env.E2E_BASE_URL || "http://127.0.0.1:3000";
const JWT = process.env.A360_JWT_SECRET || "dev-secret-0123456789abcdef";
const DEMO_PW = process.env.A360_DEMO_PASSWORD || "Demo-password-2027";

export default defineConfig({
  testDir: "./e2e",
  timeout: 120_000,
  expect: { timeout: 20_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [["list"]],
  use: { baseURL: FRONTEND, trace: "retain-on-failure", viewport: { width: 1440, height: 900 }, acceptDownloads: true },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } } }],
  // Starts the real FastAPI backend and Next.js unless they are already running.
  webServer: [
    {
      command: `bash -c "cd ../backend && . .venv/bin/activate && A360_JWT_SECRET=${JWT} A360_DEMO_PASSWORD=${DEMO_PW} python -m app.seed demo; A360_JWT_SECRET=${JWT} exec uvicorn app.main:app --port 8000"`,
      url: "http://127.0.0.1:8000/api/health",
      reuseExistingServer: true,
      timeout: 60_000,
    },
    {
      command: "npm run build && npm run start",
      url: `${FRONTEND}/api/health`,
      reuseExistingServer: true,
      timeout: 300_000,
    },
  ],
});
