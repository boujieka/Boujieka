# Risk register

Likelihood / impact: L = low, M = medium, H = high. Owner roles are placeholders until a team exists.

| # | Risk | L | I | Mitigation (status) | Owner |
|---|---|---|---|---|---|
| R1 | The model is classified as unlicensed money transmission or prohibited FX compensation in one or more corridors | M | H | Legal opinions per jurisdiction before any live corridor; operate only through licensed partners; corridors locked to SIMULATION (done in code) | Legal |
| R2 | No partner (bank/PSP/Mobile Money) accepts the model | M | H | Early partner discovery; white-label positioning of SwapEngine for licensed institutions | CEO |
| R3 | Structural corridor imbalance (diaspora → Africa ≫ Africa → diaspora) leaves orders unmatched for long | H | H | SwapLiquidity measures it; refunds on expiry; prefunding by a licensed partner; multilateral netting (sim) | Treasury |
| R4 | Money laundering / sanctions evasion via matched flows | M | H | Compliance gate before funding; matching cannot bypass it; licensed screening + monitoring needed | Compliance |
| R5 | Counterparty exposure if one leg is paid and the other fails | M | H | Both legs funded before matching; failed payouts retried then escalated; funds stay as `BENEFICIARY_PAYABLE` (tested) | Ops |
| R6 | FX rounding or arithmetic errors | L | H | bigint minor units, exact rationals, floor rounding, property tests, invariant audit | Engineering |
| R7 | Double payout / replayed webhook | L | H | Idempotency keys, event de-duplication, HMAC (tested) | Engineering |
| R8 | Data breach exposing PII / account data | M | H | Not yet mitigated beyond design: encryption at rest, masking, access control, pen test required | Security |
| R9 | Users perceive estimated timings or savings as guarantees | M | M | Timings labelled indicative; no savings shown without a documented reference (done) | Product |
| R10 | Simulated non-CFA rates mistaken for real market rates | M | M | Rates flagged `SIMULATED` in UI and API; licensed market data feed required | Product |
| R11 | Demo/simulation artefacts presented to investors as live traction | M | H | Persistent "Mode simulation" banner; receipts state "no value"; demo data is generated and labelled | CEO |
| R12 | Trademark conflict on "DiaspoSwap" or the logo | ? | M | Not checked. Search OAPI, EUIPO, WIPO, USPTO, CIPO before launch | Legal |
| R13 | Single in-memory process loses state on restart | H (today) | M | Acceptable for demo only; Postgres persistence is Phase 4 | Engineering |
| R14 | Dependency on fast-moving Expo/React Native versions | M | L | `expo install` pinning, CI typecheck + web bundle | Engineering |
