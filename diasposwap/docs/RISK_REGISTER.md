# Risk register

Revised 2026-11-28 after the business-model review. Likelihood / impact: L = low, M = medium, H = high, ? = unknown.
Ratings are judgements, not measurements. Owner roles are placeholders until a team exists. Status of each mitigation:
✅ done (in code, tested) · 🟡 partly done · ❌ not done. KRI = key risk indicator to monitor from the pilot.

Evidence note: statements about CEMAC Regulation 02/18 come from an OCR reading of the official BEAC copy (Articles 30,
56/63, 87, 88, 95, 96). The OCR did not find the word "compensation" in the readable text; BEAC instructions, COBAC
texts and Regulation 04/18 were **not** read. None of this is legal advice.

## 1. Regulatory and legal

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R1 | The model is unlicensed money transmission or prohibited FX activity. In CEMAC, **Art. 30** requires settlements with abroad to go "exclusivement par le canal des établissements de crédit"; **Art. 87** subjects foreign money-transfer companies to BEAC terms; **Art. 88** requires declaring transfers > 100 M FCFA 30 days ahead | H | H | Legal opinions France + CEMAC before any live corridor; operate only as agent / technology provider of licensed institutions, with a **bank** on the CEMAC side; corridors locked to SIMULATION in code | 🟡 (lock ✅, opinions ❌) | Opinions obtained per corridor | Legal |
| R12 | Trademark conflict on "DiaspoSwap" or the logo | ? | M | Search OAPI, EUIPO, WIPO, USPTO, CIPO before launch | ❌ | — | Legal |
| R23 | **Supporting documents** required for CM → FR family/study transfers (**Art. 95–96**) add friction exactly on the scarce direction | H | M | Document upload and review in the app; partner with institutions that already hold the documents (schools, importers) | ❌ | Share of CM → FR orders abandoned at the document step | Product |
| R18 | **Customer-fund safeguarding** and partner insolvency: funds collected must be protected (EU safeguarding rules, from memory, to confirm) | M | H | DiaspoSwap never holds funds; the licensed partner safeguards them; contractually verified | ❌ | — | Legal / Finance |
| R30 | Data protection across zones (GDPR in France, local laws in each corridor country), possible data-localisation rules | M | M | DPIA, processing register, retention schedule, data-transfer basis | ❌ | — | Legal |

## 2. Business model and market

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R2 | No bank / payment institution / Mobile Money partner accepts the model | M | H | Phase 0 partner discovery; pitch the correspondent-cost saving to the bank; fallback = technology provider (B6) | ❌ | Letters of intent obtained | CEO |
| R3 | Structural imbalance (diaspora → Africa ≫ Africa → diaspora) leaves orders unmatched | H | H | Partner bank as residual counterparty (B2); Guaranteed / Eco options (B1); build documented CM → FR flows (B4); SwapLiquidity measures it ✅ | 🟡 | Match rate and median time to match per direction | Treasury |
| R22 | **Unit economics**: a % fee alone does not cover per-transaction costs; at 0.75 % an offset euro earns ~3× less than a conventional one under the simulator's assumptions | H | H | Fixed fee + %, separate offset / conventional prices (B3); measure full cost per transaction in the pilot | ❌ | Contribution margin per transaction | CEO / Finance |
| R29 | **Weak moat**: bilateral netting is easy to build; large operators already net their own flows internally (from general knowledge, unverified) | H | M | Compete on partner network, data and corridor depth, not on the algorithm; multi-operator netting only later | ❌ | — | CEO |
| R20 | **Seasonality and concentration**: one corridor, one Mobile Money operator, tuition-season peaks | H | M | Second corridor in the same zone (Congo); second provider; liquidity forecasts per season | ❌ | Volume share of top corridor / top provider | Treasury |
| R9 | Users perceive estimated timings or savings as guarantees | M | M | Timings labelled indicative; no savings shown without a documented reference ✅; Guaranteed option states a firm promise (B1) | 🟡 | Complaints about delays | Product |
| R11 | Demo/simulation artefacts presented to investors as live traction | M | H | Persistent "Mode simulation" banner, receipts state "no value", generated demo data | ✅ | — | CEO |

## 3. Financial and market risk

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R28 | **FX risk on non-CFA corridors** (CAD, USD, GBP, NGN, ZAR); NGN volatility and capital controls | H on NGN | H | Start with EUR ↔ XAF only; licensed rate feed; short quote validity ✅ (15 min); no open FX positions held by DiaspoSwap | 🟡 | Rate moves within quote validity | Treasury |
| R21 | **Change in the CFA franc regime** (peg or currency reform; reform discussed on the UMOA side since 2019, from general knowledge) | L | H | Monitor; pricing and FX code already support non-pegged rates ✅ | 🟡 | — | CEO |
| R10 | Simulated non-CFA rates mistaken for real market rates | M | M | Rates flagged `SIMULATED` in UI and API ✅; licensed feed needed | 🟡 | — | Product |
| R6 | FX rounding or arithmetic errors | L | H | bigint minor units, exact rationals, floor rounding, property tests, invariant audit | ✅ | Reconciliation breaks | Engineering |

## 4. Financial crime and fraud

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R4 | Money laundering / sanctions evasion via matched flows (FATF typologies report of 3 Sept 2026 describes value moving through compensation mechanisms without funds crossing borders) | M | H | Compliance gate before funding; matching cannot bypass it ✅; licensed screening and transaction monitoring needed | 🟡 | Alerts, STRs filed, review time | Compliance |
| R15 | **Collusion**: one network posts both sides of a match, so the engine offsets dirty money perfectly. The risk specific to this model | M | H | Block matching between linked accounts (device, beneficiary, contact details); link analysis | ❌ | Share of matches between linked accounts | Compliance |
| R16 | **Post-payment reversal**: card chargeback or direct-debit dispute after the other leg is paid out. Not handled in the current code | M | H | Irrevocable funding only (SEPA credit transfer, instant if possible); holding period for new accounts; per-user limits | ❌ | Reversal rate, loss per month | Risk |
| R31 | Account takeover, identity fraud, money mules | M | H | Real authentication with MFA and device binding; licensed KYC with liveness | ❌ (demo auth only) | Takeover incidents | Security |

## 5. Operational

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R5 | Counterparty exposure if one leg is paid and the other fails | M | H | Both legs funded before matching; failed payouts retried 3× then exception + DISPUTED; funds stay owed as `BENEFICIARY_PAYABLE` | ✅ (tested) | Open exceptions and their age | Ops |
| R17 | **Settlement-timing gap** between the two legs (holidays in two zones, cut-off times, outages) | M | M | Release both legs together or hold both; holiday calendars per zone | ❌ | Time between leg confirmations | Ops |
| R24 | **Partner outage** (Mobile Money or bank API down) | M | M | Second provider per country; retry queue; customer communication | ❌ (one simulated provider per country) | Provider availability, queued payouts | Ops |
| R25 | **Beneficiary errors and wallet limits**: wrong Mobile Money number, name mismatch, daily/wallet caps | H | M | Name check before payout; automatic split above limits; retries ✅ | 🟡 | Payout failure rate | Ops |
| R27 | **Compliance review backlog**: false positives stall orders, which starves matching | M | M | Four-eyes review ✅; target review times; staffing | 🟡 | Review queue age | Compliance |
| R32 | **Reconciliation breaks** against real partner statements (cut-offs, time zones, fees netted by partners) | M | H | `reconcile()` and double-entry ledger ✅; DB-enforced ledger integrity (PR #6); daily reconciliation against real statements needed | 🟡 | Breaks count and age | Finance |
| R7 | Double payout / replayed webhook | L | H | Idempotency keys, event de-duplication, HMAC | ✅ (tested) | Duplicate events rejected | Engineering |
| R19 | Customer support across two time zones and languages; disputes and complaints | M | M | Support process, complaint SLA, dispute workflow | ❌ | Complaint age, SLA breaches | Ops |
| R26 | **Key person** dependency (founder, undocumented knowledge) | H | M | Documentation (CLAUDE.md, docs/), shared access, second operator | 🟡 | — | CEO |

## 6. Technology and security

| # | Risk | L | I | Mitigation | Status | KRI | Owner |
|---|---|---|---|---|---|---|---|
| R8 | Data breach exposing PII or account data | M | H | Encryption at rest, masking, access control, penetration test | ❌ beyond design | Security findings open | Security |
| R13 | State loss on restart (API state in memory) | H (today) | M | Ledger persisted with DB-enforced integrity (PR #6); rest of persistence next | 🟡 | — | Engineering |
| R14 | Dependency on fast-moving Expo / React Native versions | M | L | `expo install` pinning, CI typecheck + web bundle, expo-doctor 20/20 | ✅ | — | Engineering |

## Changes in this revision
- **R1** rewritten with the CEMAC articles actually read; likelihood raised from M to H.
- **R3** now points to the business-model fixes (partner bank as residual counterparty, Guaranteed / Eco options).
- **R13** updated for the ledger persistence slice (PR #6, not yet merged).
- **New**: R15–R32. They cover collusion, post-payment reversal, settlement timing,
  safeguarding, seasonality, CFA regime, unit economics, documents (Art. 95), partner outage, beneficiary errors, key
  person, review backlog, non-CFA FX, weak moat, data protection, account takeover, reconciliation, support.
- Columns added: status of mitigation and KRI.
