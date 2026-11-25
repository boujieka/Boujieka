# Security and compliance design

**Everything below marked (SIM) is simulated.** None of it is a substitute for licensed KYC/AML/sanctions providers,
legal opinions, or a regulator-approved compliance programme.

## Implemented in this version
| Control | Where | Notes |
|---|---|---|
| Exact money arithmetic | `shared-types` | bigint minor units; no floats |
| Append-only double-entry ledger, reversals | `ledger` | entries frozen; idempotency keys |
| Explicit state machine + audit trail | `shared-types`, `SwapSimulator.audit` | every transition logged with actor and reason |
| KYC tiers and limits (SIM) | `compliance-engine` | demo thresholds, not regulatory figures |
| Sanctions screening (SIM) | `compliance-engine` | fictional watchlist, accent/word-order normalisation |
| PEP → review (SIM) | `compliance-engine` | enhanced due diligence required |
| Velocity / structuring heuristics (SIM) | `compliance-engine` | review triggers |
| Compliance cannot be bypassed by matching | `matching-engine` | eligibility filter + `verifyRun` audit |
| Four-eyes compliance decisions | `apps/api` `AdminController.decide` | two different officers; tested |
| Role-based admin access | `apps/api` `AdminGuard` | demo API keys `ops` / `compliance` |
| Webhook HMAC-SHA256 over raw body, constant-time compare | `settlement-engine`, API | replay de-duplication |
| Idempotency for orders, provider ops, ledger | engine + API | |
| Counterparty privacy | `SwapSimulator.userView` | tested: no counterparty name/account in user responses |
| Order enumeration resistance | API | "not yours" and "not found" both return 404 |
| HTTP hardening | `apps/api/src/configure.ts` | `nosniff`, `no-store`, `no-referrer`, no `x-powered-by` |
| Secure session storage on device | `apps/mobile/src/lib/session.ts` | SecureStore (Keychain/Keystore); memory only on web |

## Not implemented (required before any real use)
- Real authentication: password/passkey + MFA, short-lived tokens, refresh rotation, device binding, rate limiting,
  account lockout. The demo uses an `X-Demo-User` header and a fake PIN.
- Encryption at rest of PII and account references (envelope encryption with a KMS); TLS termination; secret manager.
- Licensed KYC/KYB, sanctions & PEP screening, adverse media, transaction monitoring, STR/SAR filing workflow.
- Data protection: GDPR / Loi camerounaise / other local laws — DPIA, retention schedule, data-subject requests,
  cross-border data transfer basis. The schema has `deletedAt`, retention is not yet configurable.
- Fraud: device fingerprinting, behavioural signals, chargeback handling for card/SEPA collections.
- Observability: structured logs exist only as Nest defaults; no tracing, alerting or tamper-evident log shipping.
- Penetration test, threat model review, dependency scanning in CI.

## Regulatory validation needed per jurisdiction (non-exhaustive, to be confirmed by counsel)
Whether matching reciprocal flows and paying out locally is a regulated payment / money-remittance / foreign-exchange
activity, and under which licence or partner agreement, must be validated **before** any live corridor — notably under:
EU payment-services and AML rules (France), CEMAC exchange regulation and payment-services rules (Cameroon, Congo),
UMOA/BCEAO rules (Senegal, Côte d'Ivoire), Canadian MSB/AML rules, US money-transmitter (federal + state) rules,
UK payment-services rules, Nigerian and South African exchange-control and payment rules. Mobile Money and bank
partners must explicitly authorise this use of their services.
