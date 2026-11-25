# Progress

Last updated: 2026-11-25 (persistence slice 1 added on branch `diasposwap/postgres-persistence`). Everything runs in **simulation mode**; no real money, provider, KYC or market-data
integration exists.

## Phase 1 — Architecture ✅
- Inspected the repository: it already hosts an unrelated project (Cartouche, WAEMU bond data). Nothing was reusable
  for DiaspoSwap, so DiaspoSwap lives in its own folder `diasposwap/` and the existing project was not modified.
- npm-workspaces monorepo; modular monolith (no microservices). Decisions recorded in `docs/ARCHITECTURE.md`.

## Phase 2 — Expo app ✅ (vertical slice)
- Expo SDK 58, Expo Router, NativeWind 4 (Tailwind 3), Zustand, TanStack Query, React Hook Form + Zod, i18next FR/EN,
  SecureStore, light/dark. React Compiler and typed routes disabled (see "Decisions").
- 13 routes built (list in `ROADMAP.md`); permanent "Mode simulation — aucun argent réel" banner.
- Brand mark + logo set and generated icons/splash (`docs/brand/`).

## Phase 3 — Financial engines ✅
- SwapEngine levels 1–3 + multilateral simulation; SwapLiquidity; double-entry ledger; simulated compliance;
  settlement orchestrator with simulated providers and HMAC webhooks; reproducible demo data (1000 users / 5000 orders).

## Phase 4 — Backend 🟡 partial
- NestJS API over the engines, **in-memory state**. Demo auth (headers), roles, four-eyes compliance decisions,
  idempotency keys, signed webhooks, reconciliation, liquidity, demo endpoints. OpenAPI 3.1 written by hand.
- Prisma schema written and validated; **not wired** (no Postgres connection, no migrations run).
- Not done: real auth/MFA, Postgres persistence, Redis/BullMQ jobs, WebSocket notifications, mobile app → API.

## Phase 4a — PostgreSQL persistence, slice 1: the ledger ✅
- Prisma **7.10.1** (latest stable; npm's `latest` tag points to an RC, 8.0.0-rc.35, deliberately not used) with the
  `@prisma/adapter-pg` driver adapter and `prisma.config.ts`. Generated client in `apps/api/src/generated/` (gitignored).
- Migrations: `20261125225829_init` (generated from the schema) and `20261125230000_ledger_integrity` (hand-written).
  The database itself enforces: balanced per currency at COMMIT, at least two postings, no zero posting, append-only
  (UPDATE/DELETE/TRUNCATE refused), no postings added to an entry from an earlier transaction, one reversal per entry.
- `LedgerStore` async interface (`packages/ledger`), with `InMemoryLedgerStore` and `PostgresLedger`
  (`apps/api/src/persistence/`). One contract suite runs against both.
- **Not yet wired**: `SwapSimulator` and the API still use the in-memory ledger; orders, payouts, provider operations
  and webhooks are not persisted. Next slice: make the orchestrator async over repository interfaces.

## Phase 5 — Administration ❌ not started
- `apps/admin` does not exist. Admin capabilities exist only as API endpoints (`/v1/admin/*`) and the in-app
  read-only liquidity screen.

## Phase 6 — Validation (what was actually run, 2026-11-25)
| Check | Command | Result |
|---|---|---|
| Unit + property + API e2e tests | `npm test` | **42/42 passed** (7 files) |
| Typecheck engines, API, mobile | `npm run typecheck` | passed |
| Mutation check of the invariant audit | engine edited to under-deduct by 1 unit | 5 tests failed as expected; code restored, all pass |
| Mobile web bundle | `npm run mobile:web:export` | passed |
| Browser walkthrough, FR → CM, light + dark | `npm run e2e:web` (Playwright/Chromium, 390×844, fr-FR) | passed: onboarding → login → quote 1000 EUR → 655 957 XAF → confirm → queued → simulated reciprocal order → matching → payouts → SETTLED → receipt → history; **0 console/page errors** |
| API boots as a server | `tsx src/main.ts`, curl `/health`, admin 401 / matching with key | passed |
| Dockerfile install + boot steps | reproduced in an isolated copy without the mobile workspace | passed |
| Docker image build | `docker build` | **not run**: no Docker daemon in this environment |
| Compose file | `docker compose config` | valid |
| Prisma schema | `prisma@6 validate` | valid |
| GitHub Actions workflow | YAML parse only | **not executed** on GitHub yet |
| Native iOS/Android run | — | **not run** (no simulator/device here); only web was exercised |

Persistence slice 1 (local PostgreSQL 16.15):
| Check | Result |
|---|---|
| `prisma migrate deploy` on an empty database | both migrations applied |
| Drift, migrations vs schema (`migrate diff --exit-code`) | none; a deliberate schema change is detected (exit 2) |
| `npm test` with `TEST_DATABASE_URL` | **59/59 passed** (42 previous + 17 ledger: 6 contract × 2 stores, 5 raw-SQL attacks) |
| `npm test` without a database | 48 passed, 5 database-only tests skipped with a warning |
| Same without a database but `CI=true` | fails with "TEST_DATABASE_URL is required in CI" (no silent skip in CI) |
| `npm run typecheck` | passed (now regenerates the Prisma client first) |

## Problems met and how they were handled
- Headless Chromium reports `en-US`, so the app started in English and the French-text e2e selectors failed — fixed by
  running the walkthrough with `fr-FR` (the app's locale detection was correct).
- Web sessions are memory-only by design (no secrets in browser storage), so a page reload logs out — the e2e
  navigates through the tab bar instead.
- Four-eyes rule bug found by the API tests: officers were identified by a 4-character key prefix, so two different
  keys counted as one officer. Fixed: identity is a hash of the full key.
- Security headers were applied only in `main.ts`, so the tested app differed from the served app. Fixed with a
  shared `configureApp()`.
- Contrast audit: gold-on-light-gold text (4.21:1) failed WCAG AA for small text in the simulation banner and state
  pills. Switched to petrol text (11.94:1).

## Problems met (persistence slice)
- `prisma migrate dev` is interactive and hung in a non-TTY shell; `migrate deploy` / `migrate diff` are used instead.
- A hand-written FK on `reversesId` would have shown up as schema drift; the reversal is now a declared self-relation.
- The typecheck passed against a stale generated client, so `typecheck` (and CI) now run `prisma generate` first.

## Decisions
- React Compiler off: the simulator mutates objects in place and compiler memoisation could hide updates. Revisit
  once state comes from the API as immutable snapshots.
- Typed routes off to keep `tsc` deterministic without a running dev server.
- `expo-notifications` not installed: push requires an EAS project; an in-app notification centre is derived from the
  audit log instead.
- Fee 0.75 % (inside the brief's 0.5–1 % hypothesis), clearly labelled as a hypothesis.
- No "savings" figure: no documented reference price exists yet.

## Next steps
See `ROADMAP.md` → "Next steps for V1.0".
