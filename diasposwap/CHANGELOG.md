# Changelog

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
