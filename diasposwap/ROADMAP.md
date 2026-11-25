# Roadmap

Proposed by the project brief; scope and order are design proposals to validate, not commitments.

| Version | Theme | Content | Status |
|---|---|---|---|
| **V1.0** | Proof of concept | Expo app, bilateral matching (exact/partial/multiple), simulated payouts, ledger, tests | **in progress — vertical MVP done** |
| V2.0 | Community marketplace | Postgres persistence, real auth + MFA, communities, referral, admin console | not started |
| V3.0 | Intelligent clearing network | Multilateral netting (still simulated), liquidity optimisation, min-cost flow | engine prototype only |
| V4.0 | Regulated FinTech | Legal opinions, licensed partners, real KYC/AML providers, pilot corridor | not started — blocked on legal |
| V5.0 | Infrastructure | Institutional SwapEngine API, white label | not started |

## Next steps for V1.0 (ordered)
1. Persistence: ~~ledger in Postgres with DB-enforced integrity~~ (slice 1 done); next: repositories for orders, quotes,
   allocations, payouts, provider operations and webhook events; async orchestrator; row locking for matching.
2. Point the mobile app at the API (TanStack Query hooks already isolate rates; extend to quotes/orders).
3. Real authentication: email/phone OTP, password or passkey, MFA, session rotation.
4. `apps/admin` (web): stats, corridor configuration with four-eyes, review queue, reconciliation, world flow map.
5. BullMQ jobs: scheduled matching per corridor, expiry sweeps, payout retries; WebSocket notifications.
6. Remaining screens: phone/email verification, identity verification, payment options, waiting list, communities,
   referral, help centre, disputes, security settings (MFA/biometrics), dedicated matching-search/result screens.
7. Observability: structured JSON logs, request ids, metrics, alerting.

## Screens requested vs built
Built (13 routes): splash gate, onboarding (+language), demo login, dashboard, new transfer (+country selection,
calculator, live quote), confirmation, tracking (matching search/progress, partial/complete match, settlement
tracking), receipt, history, profile (+language), beneficiaries, notifications, corridor liquidity.
Placeholders marked "Bientôt": communities, referral, help centre, disputes. Not built: sign-up, phone/email
verification, identity verification, payment options, waiting-list screen, security settings beyond the info row.
