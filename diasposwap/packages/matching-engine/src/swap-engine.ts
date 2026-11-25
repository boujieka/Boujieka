import {
  type CorridorConfig, type CountryCode, type CurrencyCode, type FxRate, type TransferOrder, type TransferState,
  COUNTRIES, INITIAL_CORRIDORS, convertFloor, crossRate, findCorridor, isRateValid, maxBaseForQuote, minBig,
} from '@diasposwap/shared-types';

/**
 * SwapEngine: deterministic, auditable bilateral matching of reciprocal transfer orders.
 *
 * Levels implemented here:
 *   1. EXACT   - two reciprocal orders that consume each other fully (up to indivisible FX rounding)
 *   2. PARTIAL - a fraction of one order against a fraction of another
 *   3. MULTIPLE - one order filled by several opposite orders (falls out of the FIFO pass)
 * Level 4 (multilateral cycles) lives in multilateral.ts and is SIMULATION ONLY.
 *
 * The engine never reads the clock or random numbers: same input -> same output.
 * It never relaxes compliance: only orders with compliance === 'CLEARED' are considered.
 */
export interface Allocation {
  id: string;
  kind: 'EXACT' | 'PARTIAL';
  /** Taker order (older or processed first) and maker order (opposite direction). */
  takerOrderId: string;
  makerOrderId: string;
  /** Minor units of the taker's send currency; paid locally to the MAKER's beneficiary. */
  takerAmount: bigint;
  takerCurrency: CurrencyCode;
  /** Minor units of the maker's send currency; paid locally to the TAKER's beneficiary. */
  makerAmount: bigint;
  makerCurrency: CurrencyCode;
  /** Rate used: maker currency per taker currency (exact rational). */
  rate: FxRate;
  /** Country where takerAmount is paid out (= taker.fromCountry). */
  takerLegCountry: CountryCode;
  /** Country where makerAmount is paid out (= maker.fromCountry). */
  makerLegCountry: CountryCode;
}

export type SkipReason =
  | 'NOT_MATCHABLE_STATE' | 'COMPLIANCE_NOT_CLEARED' | 'EXPIRED' | 'NO_REMAINING' | 'UNKNOWN_CORRIDOR'
  | 'CORRIDOR_DISABLED' | 'CURRENCY_MISMATCH' | 'ABOVE_CORRIDOR_LIMIT' | 'STALE_RATE' | 'INVALID_AMOUNTS';

export interface MatchRunInput {
  runId: string;
  orders: readonly TransferOrder[];
  /** Reference rates against EUR (see referenceRates). */
  rates: Record<CurrencyCode, FxRate>;
  now: Date;
  corridors?: readonly CorridorConfig[];
}

export interface MatchRunResult {
  runId: string;
  allocations: Allocation[];
  /** Orders after the run (inputs are never mutated). */
  orders: TransferOrder[];
  skipped: { orderId: string; reason: SkipReason }[];
  /** Orders now past expiry: the caller must move them to EXPIRED and refund the remaining principal. */
  expired: string[];
  /** Partially matched orders whose remainder is below the corridor minimum fill (refund candidates). */
  dust: { orderId: string; remaining: bigint }[];
}

const MATCHABLE: readonly TransferState[] = ['QUEUED', 'PARTIALLY_MATCHED'];

export function eligibility(o: TransferOrder, now: Date, corridors: readonly CorridorConfig[], rates: Record<CurrencyCode, FxRate>): SkipReason | null {
  if (!MATCHABLE.includes(o.state)) return 'NOT_MATCHABLE_STATE';
  if (o.compliance !== 'CLEARED') return 'COMPLIANCE_NOT_CLEARED';
  if (o.principal <= 0n || o.remaining < 0n || o.remaining > o.principal) return 'INVALID_AMOUNTS';
  if (o.remaining === 0n) return 'NO_REMAINING';
  if (Date.parse(o.expiresAt) <= now.getTime()) return 'EXPIRED';
  const corridor = findCorridor(o.fromCountry, o.toCountry, corridors);
  if (!corridor) return 'UNKNOWN_CORRIDOR';
  if (corridor.mode !== 'SIMULATION') return 'CORRIDOR_DISABLED';
  if (COUNTRIES[o.fromCountry].currency !== o.sendCurrency || COUNTRIES[o.toCountry].currency !== o.receiveCurrency) return 'CURRENCY_MISMATCH';
  const inEur = convertFloor(o.principal, crossRate(o.sendCurrency, 'EUR', rates));
  if (inEur > corridor.maxOrderEurCents) return 'ABOVE_CORRIDOR_LIMIT';
  return null;
}

export const isReciprocal = (a: TransferOrder, b: TransferOrder): boolean =>
  a.fromCountry === b.toCountry && a.toCountry === b.fromCountry &&
  a.sendCurrency === b.receiveCurrency && a.receiveCurrency === b.sendCurrency;

const byPriority = (a: TransferOrder, b: TransferOrder): number =>
  a.createdAt < b.createdAt ? -1 : a.createdAt > b.createdAt ? 1 : a.id < b.id ? -1 : a.id > b.id ? 1 : 0;

export function runMatching(input: MatchRunInput): MatchRunResult {
  const corridors = input.corridors ?? INITIAL_CORRIDORS;
  const work = new Map<string, TransferOrder>();
  const skipped: MatchRunResult['skipped'] = [];
  const expired: string[] = [];
  const ids = new Set<string>();

  for (const o of input.orders) {
    if (ids.has(o.id)) throw new Error(`Duplicate order id ${o.id}`);
    ids.add(o.id);
    const reason = eligibility(o, input.now, corridors, input.rates);
    if (reason) {
      skipped.push({ orderId: o.id, reason });
      if (reason === 'EXPIRED') expired.push(o.id);
      continue;
    }
    work.set(o.id, { ...o });
  }

  // group by unordered country pair
  const pairs = new Map<string, TransferOrder[]>();
  for (const o of work.values()) {
    const key = [o.fromCountry, o.toCountry].sort().join('|');
    const list = pairs.get(key) ?? [];
    list.push(o);
    pairs.set(key, list);
  }

  const allocations: Allocation[] = [];
  let seq = 0;
  const nextId = () => `${input.runId}:a${(++seq).toString().padStart(5, '0')}`;

  for (const key of [...pairs.keys()].sort()) {
    const list = (pairs.get(key) ?? []).sort(byPriority);
    const first = list[0];
    if (!first) continue;
    const sideX = list.filter((o) => o.fromCountry === first.fromCountry);
    const sideY = list.filter((o) => o.fromCountry !== first.fromCountry);
    if (sideX.length === 0 || sideY.length === 0) continue;

    const rateXY = crossRate(first.sendCurrency, first.receiveCurrency, input.rates);
    if (!isRateValid(rateXY, input.now)) {
      for (const o of list) skipped.push({ orderId: o.id, reason: 'STALE_RATE' });
      continue;
    }
    const corridor = findCorridor(first.fromCountry, first.toCountry, corridors);
    if (!corridor) continue;
    const minFillIn = (c: CurrencyCode) => convertFloor(corridor.minFillEurCents, crossRate('EUR', c, input.rates));
    const rateFor = (t: TransferOrder, m: TransferOrder) => crossRate(t.sendCurrency, m.sendCurrency, input.rates);

    const record = (t: TransferOrder, m: TransferOrder, takerAmount: bigint, makerAmount: bigint, kind: Allocation['kind']): Allocation => ({
      id: nextId(), kind,
      takerOrderId: t.id, makerOrderId: m.id,
      takerAmount, takerCurrency: t.sendCurrency,
      makerAmount, makerCurrency: m.sendCurrency,
      rate: rateFor(t, m),
      takerLegCountry: t.fromCountry, makerLegCountry: m.fromCountry,
    });

    // ---- Pass 1: exact matches (both orders fully consumed, up to indivisible rounding) ----
    const merged = [...sideX, ...sideY].sort(byPriority);
    for (const t of merged) {
      if (t.remaining === 0n) continue;
      const opposite = t.fromCountry === first.fromCountry ? sideY : sideX;
      for (const m of opposite) {
        if (m.remaining === 0n || !isReciprocal(t, m)) continue;
        const r = rateFor(t, m);
        const cap = maxBaseForQuote(m.remaining, r);
        if (cap !== t.remaining) continue; // taker must be fully consumed and maker must be able to absorb all of it
        const makerAmount = convertFloor(t.remaining, r);
        const leftover = m.remaining - makerAmount;
        if (maxBaseForQuote(leftover, r) !== 0n) continue; // maker leftover must be unusable rounding only
        if (makerAmount <= 0n) continue;
        allocations.push(record(t, m, t.remaining, makerAmount, 'EXACT'));
        t.remaining = 0n;
        m.remaining = leftover;
        break;
      }
    }

    // ---- Pass 2: FIFO partial / multiple matching ----
    for (const t of merged) {
      if (t.remaining === 0n) continue;
      const opposite = t.fromCountry === first.fromCountry ? sideY : sideX;
      const tentative: { m: TransferOrder; alloc: Allocation }[] = [];
      const takerStart = t.remaining;
      for (const m of opposite) {
        if (t.remaining === 0n) break;
        if (m.remaining === 0n || !isReciprocal(t, m)) continue;
        const r = rateFor(t, m);
        const cap = maxBaseForQuote(m.remaining, r);
        const takerAmount = minBig(t.remaining, cap);
        if (takerAmount <= 0n) continue;
        const makerAmount = convertFloor(takerAmount, r);
        if (makerAmount <= 0n) continue;
        const closesTaker = takerAmount === t.remaining;
        const closesMaker = maxBaseForQuote(m.remaining - makerAmount, r) === 0n;
        if (takerAmount < minFillIn(t.sendCurrency) && !closesTaker && !closesMaker) continue;
        if (!m.allowPartial && !(closesMaker && m.remaining === m.principal)) continue; // all-or-none maker
        const alloc = record(t, m, takerAmount, makerAmount, 'PARTIAL');
        tentative.push({ m, alloc });
        t.remaining -= takerAmount;
        m.remaining -= makerAmount;
      }
      if (!t.allowPartial && (t.remaining !== 0n || takerStart !== t.principal)) {
        // all-or-none taker not fully filled in this run: roll back
        for (const { m, alloc } of tentative) m.remaining += alloc.makerAmount;
        t.remaining = takerStart;
        continue;
      }
      for (const { alloc } of tentative) allocations.push(alloc);
    }
  }

  // ---- derive states, dust ----
  const dust: MatchRunResult['dust'] = [];
  const out: TransferOrder[] = input.orders.map((orig) => {
    const w = work.get(orig.id);
    if (!w) return { ...orig };
    let state: TransferState = w.state;
    if (w.remaining === 0n) state = 'MATCHED';
    else if (w.remaining < orig.remaining || w.remaining < w.principal) state = 'PARTIALLY_MATCHED';
    if (state === 'PARTIALLY_MATCHED') {
      const corridor = findCorridor(w.fromCountry, w.toCountry, corridors);
      const remEur = convertFloor(w.remaining, crossRate(w.sendCurrency, 'EUR', input.rates));
      if (corridor && remEur < corridor.minFillEurCents) dust.push({ orderId: w.id, remaining: w.remaining });
    }
    return { ...w, state };
  });

  const result: MatchRunResult = { runId: input.runId, allocations, orders: out, skipped, expired, dust };
  verifyRun(input.orders, result);
  return result;
}

export class InvariantViolation extends Error {}

/**
 * Independent audit of a run. Throws on any violation:
 * - conservation: remaining_after = remaining_before - sum(allocated) for every order, never negative
 * - no allocation on an ineligible / non-cleared order
 * - every allocation is reciprocal, positive and rate-consistent (floor conversion)
 */
export function verifyRun(before: readonly TransferOrder[], r: MatchRunResult): void {
  const prev = new Map(before.map((o) => [o.id, o]));
  const after = new Map(r.orders.map((o) => [o.id, o]));
  const used = new Map<string, bigint>();
  const skippedIds = new Set(r.skipped.map((s) => s.orderId));
  for (const a of r.allocations) {
    const t = prev.get(a.takerOrderId);
    const m = prev.get(a.makerOrderId);
    if (!t || !m) throw new InvariantViolation(`Allocation ${a.id} references unknown order`);
    if (skippedIds.has(t.id) || skippedIds.has(m.id)) throw new InvariantViolation(`Allocation ${a.id} uses a skipped order`);
    if (t.compliance !== 'CLEARED' || m.compliance !== 'CLEARED') throw new InvariantViolation(`Allocation ${a.id} bypasses compliance`);
    if (!isReciprocal(t, m)) throw new InvariantViolation(`Allocation ${a.id} is not reciprocal`);
    if (a.takerAmount <= 0n || a.makerAmount <= 0n) throw new InvariantViolation(`Allocation ${a.id} non-positive`);
    if (convertFloor(a.takerAmount, a.rate) !== a.makerAmount) throw new InvariantViolation(`Allocation ${a.id} rate-inconsistent`);
    used.set(t.id, (used.get(t.id) ?? 0n) + a.takerAmount);
    used.set(m.id, (used.get(m.id) ?? 0n) + a.makerAmount);
  }
  for (const [id, o] of prev) {
    const n = after.get(id);
    if (!n) throw new InvariantViolation(`Order ${id} disappeared`);
    const u = used.get(id) ?? 0n;
    if (u > o.remaining) throw new InvariantViolation(`Order ${id} over-allocated`);
    if (n.remaining !== o.remaining - u) throw new InvariantViolation(`Order ${id} conservation broken`);
    if (n.principal !== o.principal) throw new InvariantViolation(`Order ${id} principal changed`);
  }
}
