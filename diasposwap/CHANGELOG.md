# Changelog

## Unreleased — PostgreSQL persistence, slice 1
### Added
- Prisma 7.10.1 + `@prisma/adapter-pg`; migrations `init` and `ledger_integrity` (database-enforced double entry,
  append-only history, one reversal per entry).
- `LedgerStore` interface with in-memory and PostgreSQL implementations, shared contract tests, raw-SQL rule tests.
- CI: PostgreSQL 16 service, migrations applied to an empty database, drift check.

## 0.1.0 — 2026-11-25 (simulation)
### Added
- Financial core packages: shared-types (bigint money, exact FX, corridors, state machine), ledger, matching-engine
  (SwapEngine levels 1–3 + multilateral simulation), compliance-engine (simulated), settlement-engine (simulated
  providers, HMAC webhooks, orchestrator, demo data), liquidity (SwapLiquidity).
- Mobile app (Expo SDK 58): 13 routes, FR/EN, light/dark, permanent simulation banner, demo tools.
- NestJS API (in-memory) with demo auth, four-eyes compliance decisions, webhooks, reconciliation, liquidity.
- Prisma schema (validated, not wired), Dockerfile + Compose, GitHub Actions workflow.
- Brand mark and logo set; generated app icons and splash.
- Documentation: architecture, matching engine, security, risk register, OpenAPI, design system, brand.
