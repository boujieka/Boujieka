# DiaspoSwap

**L'argent circule localement. La valeur voyage.** · *Money stays local. Value goes global.*

DiaspoSwap matches people sending money in opposite directions between two countries (e.g. France → Cameroon and
Cameroon → France) so that each side is paid out **locally**, from the other side's funds, instead of moving money
across the border.

> ## ⚠️ Simulation mode — no real money
> This version moves **no real money**. Every payment provider is simulated, every ledger entry is flagged
> `simulated`, compliance checks use a fictional watchlist and demo thresholds, and all non-CFA exchange rates are
> placeholders. No corridor may be activated for real operations without prior legal, regulatory and licensed-partner
> authorisation in each jurisdiction (EU, CEMAC, UMOA, Canada, US, UK, Nigeria, South Africa).

## What is in this folder

| Path | What it is | Status |
|---|---|---|
| `packages/shared-types` | bigint money, exact rational FX, corridors, transfer state machine | tested |
| `packages/matching-engine` | **SwapEngine**: exact / partial / multiple matching + multilateral cycle simulation | tested (incl. property tests) |
| `packages/ledger` | append-only double-entry ledger, idempotent, reversals | tested |
| `packages/compliance-engine` | simulated KYC tiers, watchlist, PEP, velocity, structuring | tested |
| `packages/settlement-engine` | simulated providers, HMAC webhooks, end-to-end orchestrator, demo data | tested |
| `packages/liquidity` | **SwapLiquidity**: corridor imbalance, prefunding need, uncertainty | tested |
| `apps/mobile` | Expo SDK 58 app (FR/EN, light/dark) running the engines in-app | typechecked, web bundle driven end-to-end in Chromium |
| `apps/api` | NestJS REST API over the same engines, in-memory state | e2e-tested with supertest; boots with `tsx` |
| `apps/api/prisma/` | PostgreSQL schema + migrations (Prisma 7) | ledger persisted with DB-enforced integrity, tested; other tables **not wired yet** |
| `infrastructure/` | Dockerfile + Compose (API, Postgres, Redis) | compose config validated; image build **not run** (no Docker daemon here) |
| `docs/` | architecture, matching engine, security, risks, API spec, design system, brand | |

Not built yet (see `ROADMAP.md`): `apps/admin` web console, persistence beyond the ledger, BullMQ jobs, WebSocket notifications,
push notifications, real authentication/MFA, 17 of the 30 requested screens.

## Live demo (simulation)

**https://diasposwap.expo.app** — web version on EAS Hosting (project `boujieks-conglomerate-group/diasposwap`).
Same simulation as the app: fictional profiles, no real money. Data lives in the browser tab and resets on reload.

## Quick start

Requires Node.js 22.

```bash
cd diasposwap
npm install
npm test               # engines, property tests, API e2e (+ PostgreSQL ledger tests if TEST_DATABASE_URL is set)
npm run typecheck      # engines + API + mobile
npm run mobile         # Expo dev server (Expo Go / dev build / press w for web)
DIASPOSWAP_ADMIN_KEYS=ops-dev-key:ops npm run api    # API on :3000
```

Demo walkthrough in the app: onboarding → demo login (any 4-digit PIN) → **Envoyer** 1000 EUR to Cameroon → confirm →
on the tracking screen: *Simuler un ordre inverse* → *Lancer le matching* → *Confirmer les paiements simulés* → receipt.

API walkthrough: see `docs/api/README.md`.

## Documentation

- `docs/ARCHITECTURE.md` — components, data flow, ledger postings, state machine (diagrams)
- `docs/MATCHING_ENGINE.md` — SwapEngine algorithms and invariants
- `docs/SECURITY.md` — security & compliance design, what is simulated
- `docs/RISK_REGISTER.md` — product, regulatory, financial and technical risks
- `docs/api/openapi.yaml` — REST API (OpenAPI 3.1)
- `docs/DESIGN_SYSTEM.md`, `docs/brand/BRAND.md` — design tokens, logo usage
- `PROGRESS.md`, `ROADMAP.md`, `CHANGELOG.md`, `CLAUDE.md`
