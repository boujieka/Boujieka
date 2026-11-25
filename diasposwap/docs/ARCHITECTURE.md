# Architecture

Modular monolith in an npm-workspaces monorepo. The financial core is a set of pure TypeScript packages; the mobile
app and the API are thin shells around them. No microservices.

```mermaid
flowchart LR
  subgraph Apps
    M[apps/mobile<br/>Expo SDK 58]
    A[apps/api<br/>NestJS]
    AD[apps/admin<br/>not built]
  end
  subgraph Core packages
    ST[shared-types<br/>money, FX, corridors, states]
    ME[matching-engine<br/>SwapEngine]
    LG[ledger<br/>double entry]
    CE[compliance-engine<br/>simulated]
    SE[settlement-engine<br/>orchestrator + providers]
    LQ[liquidity<br/>SwapLiquidity]
  end
  P[(PostgreSQL<br/>Phase 4)]
  R[(Redis/BullMQ<br/>Phase 4)]
  M --> SE
  A --> SE
  AD -.-> A
  SE --> ME & LG & CE
  ME & LG & CE & LQ --> ST
  A -.-> P & R
```

Today the mobile app embeds the engines (offline demo) and the API keeps state in memory. Phase 4 moves persistence to
PostgreSQL (`apps/api/prisma/schema.prisma`) and the app to the API.

## End-to-end flow (France → Cameroon)

```mermaid
sequenceDiagram
  participant A as Amina (FR)
  participant S as SwapSimulator
  participant C as Compliance (sim)
  participant P1 as SEPA (sim)
  participant E as SwapEngine
  participant P2 as Mobile Money CM (sim)
  participant B as Jean (CM)
  A->>S: quote(1000 EUR) → fee 7.50, 655 957 XAF
  A->>S: createOrder(quote, Paul, Idempotency-Key)
  S->>C: evaluate → ALLOW
  A->>S: fund → P1.collect(1007.50 EUR)
  P1-->>S: signed webhook SUCCEEDED → ledger, QUEUED
  B->>S: order CM→FR 655 957 XAF (funded the same way via P2)
  S->>E: runMatching → EXACT allocation
  S->>P2: payout 655 957 XAF to Paul (from Jean's XAF)
  S->>P1: payout 1000 EUR to Grace (from Amina's EUR)
  P1-->>S: webhook SUCCEEDED
  P2-->>S: webhook SUCCEEDED
  S->>S: ledger + reconciliation → both orders SETTLED
```

No euro crosses into Cameroon and no franc CFA crosses into France: each currency stays in its country.

## Ledger postings (simulated accounts)

| Event | Debit | Credit |
|---|---|---|
| Collection confirmed | `COLLECTION` (country) principal+fee | `CUSTOMER_FUNDS` (order) principal; `FEE_REVENUE` fee |
| Allocation | `CUSTOMER_FUNDS` (taker) | `BENEFICIARY_PAYABLE` (maker's beneficiary) — and symmetrically in the other currency |
| Payout confirmed | `BENEFICIARY_PAYABLE` | `COLLECTION` |
| Refund initiated | `CUSTOMER_FUNDS` remainder; `FEE_REVENUE` pro-rata fee | `REFUND_PAYABLE` |
| Refund confirmed | `REFUND_PAYABLE` | `COLLECTION` |

Each entry balances **per currency**; an allocation entry contains two independently balanced currency legs.
`reconcile()` checks the trial balance and that every successful provider operation has exactly the ledger effect
expected on the `COLLECTION` account of its country.

## Transfer state machine

```mermaid
stateDiagram-v2
  [*] --> DRAFT
  DRAFT --> QUOTED
  QUOTED --> PENDING_VERIFICATION
  PENDING_VERIFICATION --> PENDING_FUNDING: compliance ALLOW / review approved
  PENDING_VERIFICATION --> FAILED: BLOCK / review rejected
  PENDING_FUNDING --> FUNDED: collection webhook
  FUNDED --> QUEUED
  QUEUED --> PARTIALLY_MATCHED
  QUEUED --> MATCHED
  PARTIALLY_MATCHED --> MATCHED
  PARTIALLY_MATCHED --> SETTLEMENT_PENDING: dust / expiry, remainder refunded
  MATCHED --> SETTLEMENT_PENDING
  SETTLEMENT_PENDING --> SETTLED: all payouts confirmed + ledger clear
  SETTLEMENT_PENDING --> DISPUTED: payout failed after retries
  DISPUTED --> SETTLED: operator fix
  QUEUED --> EXPIRED
  EXPIRED --> REFUND_PENDING
  QUEUED --> REFUND_PENDING: user cancel
  REFUND_PENDING --> REFUNDED
```

The full table (including `CANCELLED`) is `TRANSITIONS` in `packages/shared-types/src/transfer.ts`.

## Persistence (PostgreSQL, Prisma 7)

Slice 1 persists the **ledger**. Rules live in two layers on purpose:

| Rule | Application (`PostgresLedger`) | Database (migration `ledger_integrity`) |
|---|---|---|
| Balanced per currency, ≥ 2 postings, no zero amounts | `validatePostings` (clear error) | deferred constraint triggers + CHECK, at COMMIT |
| Append-only | no update/delete methods | triggers refuse UPDATE / DELETE / TRUNCATE |
| History can't be extended | entry + postings in one transaction | postings only in the transaction that created the entry |
| Idempotency | look-up by key, compare postings | `idempotencyKey` UNIQUE (race: loser re-reads the winner) |
| One reversal per entry | checked before insert | `reversesId` UNIQUE + self-FK |

Production hardening still to do: run the app with a role that has only INSERT/SELECT on ledger tables (triggers can be
disabled by a table owner), and back the trigger check with periodic reconciliation.

## Concurrency and idempotency

| Risk | In this version | Phase 4 (Postgres) |
|---|---|---|
| Two matching runs at once | in-process lock (`MATCHING_IN_PROGRESS`) | single matching worker per corridor (BullMQ), `SELECT … FOR UPDATE SKIP LOCKED`, optimistic `version` column |
| Double order on retry | `Idempotency-Key` → same order | `@@unique([userId, idempotencyKey])` |
| Double payout | provider idempotency key `payoutId:attemptN`; new attempt only after a confirmed failure | `@@unique([providerId, kind, idempotencyKey])` |
| Webhook replay | event id de-duplication | `WebhookEvent` primary key |
| Double ledger posting | ledger idempotency key | `LedgerEntry.idempotencyKey @unique` |
