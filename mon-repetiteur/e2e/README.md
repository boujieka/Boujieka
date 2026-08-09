# E2E suite (Phase 10 — QA, CLAUDE.md §29/§30)

Real-browser tests (Playwright, driven from plain Vitest — see
`vitest.e2e.config.mts`) against a production `next start` build and the
local Supabase stack. Distinct from `tests/*.test.ts` (Vitest +
`@supabase/supabase-js` integration tests against RLS, no browser) and
from the throwaway scratchpad scripts used ad hoc during earlier phases,
which were intentionally never committed.

## Running

```sh
npm run db:start   # local Supabase must already be running
npm run test:e2e   # builds, starts a server on :3200, runs the suite, tears down
```

In a sandboxed/offline dev environment where the `playwright` npm
package's pinned browser revision isn't available locally, point
`PLAYWRIGHT_CHROMIUM_PATH` at an already-installed Chromium binary
instead of trying to download one — see `e2e/config.ts`.

## Coverage

One spec file per CLAUDE.md §29 critical flow: `auth` (Registration +
Login), `dashboard`, `learn-exercise-progress` (Lesson -> Exercise ->
Progress, the core LEARN -> PRACTICE -> DIAGNOSE loop), `exam-archive`,
`mock-exam`, `ai-tutor`, plus `admin-authorization` (the Admin CMS's
staff gate, not in §29's list but the most security-sensitive UI-level
authorization boundary built so far).

**Known gap:** §29 also lists "Onboarding" — this product has no
distinct onboarding step (program/class default automatically; see
`src/app/learn/page.tsx`'s `DEFAULT_PROGRAM_CODE`, and `profiles`'s
migration comment noting `program_id`/`class_id` were never actually
added to that table). No test claims to cover a flow that doesn't exist.
