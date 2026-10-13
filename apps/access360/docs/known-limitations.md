# Known limitations register (MVP 0.1.0)

| # | Area | Limitation | Consequence | Planned resolution |
|---|---|---|---|---|
| L1 | Engine | No hourly sizing or dispatch: deliverable energy and the diesel share come from the design study | Unserved energy and fuel use are only as good as that study | Optional hourly module (PyPSA or similar) in a later phase |
| L2 | Engine | RESOLVED (milestone 2): receivable days on collectable billing and payable days on operating costs; inventory still not modelled | | |
| L3 | Engine | RESOLVED (milestone 2): one local currency tranche can be sculpted so that total debt service = CFADS ÷ target DSCR, sized by present value and capped by its share of capex; fixed point iteration with a convergence flag. USD tranches cannot be sculpted | | |
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
| L16 | Exports | RESOLVED (milestone 2): the Excel export is a live formula model (Inputs, Model, Summary), verified against the engine after LibreOffice recalculation on 4 cases in the test suite. Exception: a sculpted tranche's debt service is written as values from the engine, because a live formula would need iteration. Not yet opened in Microsoft Excel | | Test in Microsoft Excel |
| L17 | Exports | Only the one-page teaser and the Excel model exist; the other 8 document types in the brief do not | | Phase 2 and 3 |
| L18 | Product | Marketplace, data rooms, Delivery, Verify, Academy, Copilot, subscriptions and payments are not implemented | | Phases 2 to 4 |
| L19 | Storage | Generated files are stored on the local disk | Not durable across hosts | Object storage |
| L20 | Validation | An independent AI review was done and the product owner approved the MVP (docs/reviews), but no documented line by line expert review of the engine exists yet, and the export has not been tested in Microsoft Excel | | Human project finance review before any client relies on outputs |
| L21 | Engine | RESOLVED (milestone 2): the DSRA is drawn before equity support and refilled ahead of distributions | | |
| L22 | Engine | Asset transfer compensation applies to NBV including capitalised finance costs (review F19) | May differ from the country rule | Configurable base per country rule |
| L23 | Engine | No salvage credit for a replacement made shortly before the horizon end when the residual value is 0 (review F20) | LCOE and the revenue requirement are slightly overstated | Pro rata salvage of late replacements |
| L24 | Engine | An unrealised FX gain on USD debt during construction is taxed in cash before COD (review F04) | Conservative; most regimes would defer it | Country tax profile |
| L25 | Optimizer | Grid options serve 100% of demand whatever the supply hours; only the service tier changes (review F18) | Weak grids look better than they are | Unserved energy from supply hours |
| L26 | Optimizer | Option F has the same engineering cost as option D; the value of the anchor contract is not priced (review F17) | F and D differ only by the anchor gate | Demand risk pricing |
