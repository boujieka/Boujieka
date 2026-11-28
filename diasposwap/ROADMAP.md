# Roadmap

Revised 2026-11-28 after the business-model review. Scope, order, prices and thresholds below are **proposals to
validate**, not commitments. Every figure marked *(hyp.)* is an unvalidated hypothesis.

## Strategy in one paragraph

DiaspoSwap no longer sells "a cheaper transfer if a counterparty shows up". It sells a **guaranteed transfer**,
delivered within an announced time, **cheaper than the market because part of it is offset behind the scenes**.
Compensation becomes the cost engine, not the product. The service runs **on top of licensed institutions**: an agent
or technology arrangement with an EU payment institution, and a **bank** on the CEMAC side, where Article 30 of CEMAC
Regulation 02/18 requires settlements with abroad to go "exclusivement par le canal des établissements de crédit".
DiaspoSwap never holds customer funds. The partner bank absorbs the structural imbalance (the residual leg) and shares
the correspondent-banking savings.

## Business model changes

| # | Change | Why | Where it shows |
|---|---|---|---|
| B1 | Two options at send time: **Guaranteed** (~2 % *(hyp.)*, delivered within hours) and **Eco** (~1 % *(hyp.)*, waits up to 72 h for a counterparty, else refunded) | Customers buy speed and certainty; waiting must be a paid choice, not a defect | Product, pricing |
| B2 | Unmatched amounts settle through the **partner's conventional channel** instead of being refunded | Removes the waiting problem without DiaspoSwap holding liquidity | Settlement engine |
| B3 | Price = **fixed fee (1–2 € *(hyp.)*) + %**, with a different % for offset vs conventional | At 0.75 %, an offset euro earns ~3× less than a conventional one under the simulator's cost assumptions; the saving must be shared, not given away | Pricing |
| B4 | Build the scarce direction (CM → FR) from **documented, recurring, pooled flows**: tuition fees, importers, medical bills | The reverse flow will not appear on its own; Article 95 requires supporting documents for these transfers anyway | Go-to-market, app |
| B5 | Legal structure: agent / technology provider of licensed institutions; **no customer funds held** | Lowest regulatory and liquidity exposure | Legal |
| B6 | Later: license SwapEngine and liquidity forecasts to other operators | Only credible once real data proves the gain | V5 |

Unit economics *(hyp.)* with offset 1.5 %, conventional 2.5 %, costs 0.30 % / 1.20 %, 70 % offset:
margin per euro = 0.7 × 1.5 % + 0.3 × 2.5 % − (0.7 × 0.30 % + 0.3 × 1.20 %) = **1.23 %**.
Break-even monthly volume = fixed costs ÷ 1.23 % ≈ **1.6 M€** at 20 k€/month, **4.9 M€** at 60 k€/month
(the original 0.75 %-only model needed 11.1 M€ at 20 k€).

## Phases with gates and stop criteria

| Phase | Content | Go to next phase if… | Status |
|---|---|---|---|
| **0. Validation** (0–3 months, no real money) | Legal opinions France + CEMAC (Art. 30, 87, 95); 30–50 interviews in both directions; waiting list capturing direction and amount; approach one CEMAC bank and one EU payment institution; identify 2–3 anchor sources of CM → FR flows | A legal path is identified **and** at least one bank letter of intent **and** the scarce direction is a meaningful share of declared demand (threshold set before starting) | **not started** |
| **1. Pilot** (3–9 months) | FR → CM only, under the partner's licence, capped volumes, a few hundred users, Guaranteed option available | **Positive contribution margin per transaction** (all costs), fraud within target, delivery time met | not started |
| **2. Extension** | Congo (same XAF zone and regulator), then Senegal and Côte d'Ivoire (BCEAO, another regulator) | Corridor 1 profitable | not started |
| **3. Platform** | License SwapEngine and SwapLiquidity forecasts to operators | Real data proves the netting gain | not started |

**Stop or pivot criteria** (fix the thresholds before Phase 0):
- no partner bank after 6 months → keep only the technology-provider route (B6);
- negative margin per transaction at the end of the pilot → revisit pricing or stop B2C;
- scarce direction durably below the threshold → drop pure netting, keep a conventional service with netting as treasury optimisation only.

## Product and engineering backlog

Ordered by what Phase 0 and the pilot need. Everything stays in **simulation** until a partner and a legal opinion exist.

### Business-model changes in code (simulation)
1. **Fallback leg** (B2): a "conventional" `PaymentProvider` path for amounts not offset in time, instead of a refund; the order states it as such.
2. **Guaranteed / Eco options** (B1) in quote and order, with the delivery promise shown before confirmation.
3. **Pricing per corridor** (B3): fixed fee + % for offset and for conventional; configurable, no hard-coded 0.75 %.
4. **Supporting documents** for CM → FR transfers (B4, Art. 95): upload, review status, block funding until reviewed.
5. **Waiting list** with direction and amount (Phase 0 measurement), shareable from the live demo.

### Operational risk controls (see `docs/RISK_REGISTER.md`)
6. **Irrevocable funding only**: SEPA credit transfer (instant if possible); no card, no direct debit; holding period for new accounts (R16).
7. **Collusion guard**: no matching between linked accounts (shared device, beneficiary or contact details); link analysis report (R15).
8. **Beneficiary name check** before payout; automatic split of payouts above Mobile Money wallet limits (R25).
9. **Second provider per country** and a retry queue for partner outages (R24).
10. **Settlement-timing guard**: release the two legs together, or hold both until both are confirmable (R17).

### Platform work (from V1.0, still needed)
11. Persistence: ledger done in slice 1 (PR #6, not yet merged); next: orders, quotes, allocations, payouts,
    provider operations, webhook events; async orchestrator; row locking for matching.
12. Point the mobile app at the API (TanStack Query hooks already isolate rates).
13. Real authentication: phone/email OTP, passkey or password, MFA, session rotation (R8).
14. `apps/admin`: stats, corridor configuration with four-eyes, review queue, reconciliation, exception queue.
15. Jobs: scheduled matching per corridor, expiry sweeps, payout retries; notifications.
16. Observability: structured logs, request ids, the KRIs of the risk register as metrics, alerting.
17. iOS TestFlight builds: configuration ready (`docs/RELEASE_TESTFLIGHT.md`); needs Apple credentials.

**Not before a partner exists:** the admin console beyond the exception queue, multilateral netting work, new corridors.

## Indicators to track from the pilot
Match rate and median time to match (per corridor and direction) · share of Guaranteed vs Eco · refund rate ·
payout failure rate · reconciliation breaks (count, age) · post-payment reversal rate · compliance queue age ·
full cost per transaction · contribution margin per transaction.

## Previous version plan (for reference)

| Version | Theme | Status |
|---|---|---|
| V1.0 | Proof of concept: app, bilateral matching, simulated payouts, ledger, tests | **vertical MVP done**; live demo at https://diasposwap.expo.app |
| V2.0 | Community marketplace | superseded by Phases 0–1 above |
| V3.0 | Intelligent clearing network | engine prototype only; after Phase 2 |
| V4.0 | Regulated FinTech | now Phase 0–1 (partner-backed, not own licences first) |
| V5.0 | Infrastructure / white label | now Phase 3 (B6) |

## Screens requested vs built
Built (13 routes): splash gate, onboarding (+language), demo login, dashboard, new transfer (+country selection,
calculator, live quote), confirmation, tracking (matching search/progress, partial/complete match, settlement
tracking), receipt, history, profile (+language), beneficiaries, notifications, corridor liquidity.
Placeholders marked "Bientôt": communities, referral, help centre, disputes. Not built: sign-up, phone/email
verification, identity verification, payment options, waiting-list screen, document upload, security settings beyond
the info row.
