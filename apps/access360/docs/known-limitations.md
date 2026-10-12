# Known limitations register (MVP 0.1.0)

| # | Area | Limitation | Consequence | Planned resolution |
|---|---|---|---|---|
| L1 | Engine | No hourly sizing or dispatch: deliverable energy and the diesel share come from the design study | Unserved energy and fuel use are only as good as that study | Optional hourly module (PyPSA or similar) in a later phase |
| L2 | Engine | Billing and collection happen in the same quarter; no receivables, payables or inventory | Working capital is understated for post-paid customers | Receivable days and payable days inputs |
| L3 | Engine | Debt is sized as a share of capex, not sculpted to a target DSCR | Debt capacity is not optimised | DSCR sculpting and a debt sizing solver |
| L4 | Engine | Distributions are not limited by distributable reserves | Equity cash flows can run ahead of accounting profit | Option to restrict dividends to retained earnings |
| L5 | Engine | Capital grant and RBF accounting is a single analytical treatment (deferred income released over the weighted asset life) | Not an IFRS determination | Configurable presentation; accountant review |
| L6 | Engine | Tax: one rate, unlimited loss carry forward, paid in the same quarter; no capital allowances | Tax timing is approximate | Country tax profiles |
| L7 | Engine | Grid arrival treatments are generic and must cite a country rule; none is bundled | The treatment is the user's responsibility | Verified country rule library (Phase 2) |
| L8 | Engine | No Monte Carlo | Only deterministic sensitivities | After independent review of the deterministic engine |
| L9 | Engine | The minimum subsidy solver searches only the capital grant (same milestones), assuming monotonicity | Other subsidy mixes are not optimised | Multi-instrument optimisation with programme constraints |
| L10 | Optimizer | Screening on annual energy; battery sizing by rule of thumb; diesel sized on an assumed 35% load factor; grid options do not model generation adequacy | Not a least-cost electrification plan | Integration with geospatial least-cost tools and an hourly module |
| L11 | Map | No third-party datasets bundled (licences not cleared; network blocked during development). No administrative boundaries | Users must upload their own layers | Licensed data partnerships and a PostGIS ingestion pipeline |
| L12 | Data | PostGIS not enabled; geometry stored as GeoJSON | No spatial queries | Phase 2 migration |
| L13 | Security | TOTP secrets stored unencrypted in the database | A database leak exposes MFA seeds | Application-level encryption with a key held in a secret manager |
| L14 | Security | Login rate limiting is in memory (per process) | Not effective across instances | Redis-backed limiter |
| L15 | Security | No password reset by email, no session revocation list, no account deletion workflow yet | Manual handling | Phase 3 account lifecycle |
| L16 | Exports | The Excel export contains values, not live formulas | Users cannot change inputs inside Excel | Formula workbook generator |
| L17 | Exports | Only the one-page teaser and the Excel model exist; the other 8 document types in the brief do not | | Phase 2 and 3 |
| L18 | Product | Marketplace, data rooms, Delivery, Verify, Academy, Copilot, subscriptions and payments are not implemented | | Phases 2 to 4 |
| L19 | Storage | Generated files are stored on the local disk | Not durable across hosts | Object storage |
| L20 | Validation | No external model review yet; no test in Microsoft Excel of the export | | Independent review before any client relies on outputs |
