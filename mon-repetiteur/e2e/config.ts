/**
 * Shared E2E constants (CLAUDE.md §29/§30's committed Playwright suite —
 * distinct from the throwaway scratchpad scripts used during earlier
 * phases, which were never committed on purpose).
 *
 * The port is dedicated to this suite (not the dev/preview port) so it
 * doesn't collide with a `next dev`/`next start` a developer already has
 * running locally.
 */
export const E2E_PORT = 3200;
export const E2E_BASE_URL = `http://localhost:${E2E_PORT}`;

/**
 * The local Playwright browser cache pinned by this project's
 * `playwright` devDependency may not match a pre-installed browser
 * revision in a sandboxed/offline dev environment (no network access to
 * fetch the matching one). When that's the case, point this at an
 * already-installed Chromium binary — e.g. in this repo's own sandboxed
 * CI environment: PLAYWRIGHT_CHROMIUM_PATH=/opt/pw-browsers/chromium.
 * Left unset, Playwright falls back to its own default resolution
 * (correct for a normal dev machine/CI that ran `npx playwright install`).
 */
export const CHROMIUM_EXECUTABLE_PATH = process.env.PLAYWRIGHT_CHROMIUM_PATH || undefined;

export const TEST_PASSWORD = "correct horse battery staple";
