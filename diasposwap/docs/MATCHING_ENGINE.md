# SwapEngine — matching engine

Source: `packages/matching-engine/src/`. Pure, deterministic (no clock, no randomness), auditable.

## Inputs and eligibility
An order is matchable only if: state `QUEUED` or `PARTIALLY_MATCHED`; `compliance === 'CLEARED'`; not expired; on a
configured corridor in `SIMULATION` mode; currencies consistent with countries; principal ≤ corridor ceiling.
Everything else is returned in `skipped` with a reason (`EXPIRED` orders are also listed in `expired` for refund).

Two orders are **reciprocal** when `A.from = B.to`, `A.to = B.from` and currencies mirror each other.

## Arithmetic
- Amounts: `bigint` minor units. Rate: exact rational (EUR/XAF = 655957/1000, the legal parity).
- `makerAmount = floor(takerAmount × rate)`; capacity of a maker in taker currency is the exact largest `x` with
  `floor(x × rate) ≤ maker.remaining` (`maxBaseForQuote`, property-tested).
- Indivisible rounding leftovers (e.g. 1–6 XAF, worth less than 1 euro cent) become **dust**: reported, then refunded.

## Levels
1. **Exact** — first pass: a taker and a maker that consume each other completely (up to indivisible rounding).
2. **Partial** — FIFO pass: the oldest order (taker) consumes the opposite queue in time priority.
3. **Multiple** — the same pass lets one order be filled by several opposite orders (e.g. 1000 EUR = 400 + 350 + 250).
4. **Multilateral (simulation only)** — `simulateMultilateral` builds a directed graph of pending EUR-equivalent flows,
   nets bilateral pairs, then greedily cancels the cycle with the largest bottleneck (cycles of length 3–4, e.g.
   FR → CM → CA → FR). It reports gross cross-border volume before/after. `mode: 'production'` throws.

Constraints honoured: all-or-none orders (`allowPartial = false`, for taker and maker), minimum fill per corridor
(avoids dust allocations), stale simulated rates (pair skipped), corridor ceilings, compliance status.

Not modelled yet (documented gaps): per-partner fees and liquidity in the objective, counterparty risk scores, provider
availability windows, min-cost-flow optimisation (the greedy cycle cancelling is not guaranteed optimal).

## Invariants (checked after every run by `verifyRun`)
- conservation: `remaining_after = remaining_before − Σ allocated` for every order; never negative; principal unchanged
- no allocation touches a skipped or non-cleared order
- every allocation is reciprocal, strictly positive and rate-consistent

A property test generates random books (up to 40 orders over 5 corridors, 200 runs) and asserts these invariants;
a deliberate mutation of the engine (`m.remaining -= makerAmount - 1n`) is caught by 5 tests.
