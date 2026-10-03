# Implementation plan

Starting point: an empty repository (one commit, a one-line README). No existing architecture to
preserve.

## Architecture

- **Backend:** FastAPI + SQLAlchemy 2 + Alembic on PostgreSQL 16. Redis + Celery (or equivalent)
  will arrive with scheduled work in Phase 2 and Phase 5.
- **Frontend:** Next.js (App Router, server components) + TypeScript + Tailwind + shadcn-style
  components + Recharts. The browser only talks to Next.js; Next.js talks to the API server-side,
  so no API credential ever reaches the client.
- **Provenance model:** `ProvenanceMixin` on every market-data table (source, source document,
  URL, publication date, extraction date, verification status, data nature, confidence,
  synthetic flag, per-field "why empty" status). Calculated values are never stored alongside
  official ones. They are computed in `app/analytics` and served in a separate `calculated` block.
- **Idempotency:** natural-key unique constraints (auction = security + date + type;
  document = content SHA-256; opportunity = dedup key).
- **All of Africa:** countries, monetary zones, sources and instruments are data, not code.
  Adding a country means adding rows plus source configuration.

## Phases

| # | Scope | Key dependencies |
|---|---|---|
| **1 ✅** | Schema, models, provenance, seed (unverified reference + synthetic), read API, basic dashboard, tests | — |
| 1b | **Security baseline before any non-local deployment:** authentication, roles (viewer / analyst / admin), API rate limiting (Redis), audit log table + middleware, secret management | Redis, identity provider decision |
| 2 | Source ingestion: operator-confirmed source URLs, crawler per source, document store (S3-compatible), PDF text extraction + OCR fallback, field extraction to *staging* tables, human verification queue, promotion to core tables | Confirmed official URLs; Celery + Redis; pdf/OCR libs; storage bucket |
| 3 | Historical analytics: per-market yield-convention registry, convention normalisation, bond pricing/YTM with day counts, fitted curves (clearly labelled), auction comparison views | Verified conventions per market (Phase 2 documents) |
| **4 (partial) ✅** | Opportunity Engine, built early on synthetic data (see PHASE_4_REPORT.md). **Done:** upcoming/new auctions, yield moves, demand vs. history, higher historical yield, curve inversion, refinancing concentration, cancelled/postponed; Radar UI. **Pending:** buybacks/switches and Eurobond signals (need ingested announcements), threshold calibration on real data | Phase 2 data; Phase 3 history |
| 5 | Daily scan (scheduled, idempotent): crawl → extract → diff → validate → alerts → *Africa Sovereign Debt Daily* report with per-statement source links; email / dashboard / webhook alerts with user filters | Phases 2–4; email provider |
| 6 | Investor Subscription Guide from verified `SubscriptionRoute` rows; investor-eligibility filter on the calendar | Verified procedural documents |
| 7 | Sovereign Funding Engine: scenario comparison (bills / bonds / Eurobonds / concessional) with explicit assumptions; no prescriptions | Phase 3 curves; FX assumptions |
| 8 | Public API: keys, quotas, versioned schemas, OpenAPI docs, global search | 1b |

Global search ("Kenya T-bill", "bonds above 10%") is planned alongside Phase 4, when structured
filters exist to map queries onto.
