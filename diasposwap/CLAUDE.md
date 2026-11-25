# DiaspoSwap — permanent project rules

These rules apply to every change in `diasposwap/`.

## Money and finance
- Amounts are `bigint` **minor units** everywhere (EUR = cents, XAF/XOF = units). Never JavaScript `number` for money,
  never floats. Over JSON, amounts are decimal **strings** of minor units.
- FX rates are exact rationals (`num/den`). Conversions round **down** (`convertFloor`) unless a rule says otherwise.
- XAF (CEMAC) and XOF (UMOA) are distinct currencies even though both are pegged at 655.957 per EUR.
- The ledger is append-only and double-entry: every entry balances per currency. Corrections are reversal entries.
- A transfer is `SETTLED` only after every local payout to its beneficiary is confirmed **and** the ledger shows nothing
  still owed. Every state change goes through `assertTransition` and is written to the audit log.
- The matching engine never relaxes compliance: only `compliance === 'CLEARED'` orders are matchable, and `verifyRun`
  must keep passing (conservation, no over-allocation, reciprocity, rate consistency).
- Multilateral netting stays **simulation only** until legal/regulatory validation.

## Honesty
- This is a simulation. Never present a simulated payment, rate, KYC check or receipt as real. Keep the
  "Mode simulation — aucun argent réel" banner on every app screen.
- Never invent integrations, partners, licences, statistics or savings figures. The dashboard shows no "savings"
  until a documented reference price exists.
- Never claim something works without running it. Record what was actually run in `PROGRESS.md`.

## Security
- No secrets in the repo; `.env.example` only. No real bank data, phone numbers or names of real people in tests/demo.
- Users never see counterparty identity or account data (`SwapSimulator.userView`).
- Webhooks: verify the HMAC over the raw body, de-duplicate by event id.
- Ask the user before any paid service, external publication, deployment, or real-money integration.

## Engineering
- TypeScript strict. Keep engines pure and deterministic (no clock or randomness inside `runMatching`).
- Don't disable or skip tests to get green. Don't delete files without a reason.
- Commands: `npm test`, `npm run typecheck`, `npm run mobile:web:export` (from `diasposwap/`).
- Expo: use `npx expo install` for app dependencies (SDK-compatible versions). SDK 58.
- The repository root also hosts an unrelated project (Cartouche). Do not modify it from DiaspoSwap work.
