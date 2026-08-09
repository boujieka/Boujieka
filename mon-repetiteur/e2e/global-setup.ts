import { spawn, type ChildProcess } from "node:child_process";
import { E2E_BASE_URL, E2E_PORT } from "./config";

/**
 * Starts a production `next start` server (assumes `next build` already
 * ran — see the test:e2e npm script) on a dedicated port, waits for it
 * to answer /api/health, and hands control to the spec files. Assumes
 * the local Supabase stack is already running, same as the integration
 * tests in tests/*.test.ts (this suite doesn't manage that lifecycle —
 * it's slow to start/reset and shared with the rest of the dev loop).
 */
export default async function globalSetup() {
  // Spawn the local `next` binary directly (not via `npx`, which adds an
  // extra wrapper process that can swallow the kill signal on teardown)
  // in its own process group (detached), so teardown can kill the whole
  // group — `next start` itself doesn't always propagate SIGTERM to
  // every child it spawns.
  const server: ChildProcess = spawn(
    "node_modules/.bin/next",
    ["start", "-p", String(E2E_PORT)],
    {
      cwd: process.cwd(),
      stdio: ["ignore", "pipe", "pipe"],
      env: process.env,
      detached: true,
    },
  );

  let serverOutput = "";
  server.stdout?.on("data", (chunk) => {
    serverOutput += chunk.toString();
  });
  server.stderr?.on("data", (chunk) => {
    serverOutput += chunk.toString();
  });

  const deadline = Date.now() + 30_000;
  let ready = false;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`${E2E_BASE_URL}/api/health`);
      if (res.ok) {
        ready = true;
        break;
      }
    } catch {
      // server not accepting connections yet — keep polling
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  if (!ready) {
    killServerGroup(server);
    throw new Error(
      `E2E server didn't become ready on ${E2E_BASE_URL} within 30s.\n--- server output ---\n${serverOutput}`,
    );
  }

  return async function teardown() {
    killServerGroup(server);
  };
}

function killServerGroup(server: ChildProcess): void {
  if (!server.pid) return;
  try {
    // Negative pid = kill the whole detached process group, not just the
    // immediate child — catches whatever `next start` spawned under it.
    process.kill(-server.pid, "SIGTERM");
  } catch {
    server.kill("SIGTERM");
  }
}
