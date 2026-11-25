import { describe, expect, it } from 'vitest';
import fc from 'fast-check';
import { type CountryCode, type TransferOrder, COUNTRIES, referenceRates } from '@diasposwap/shared-types';
import { ProductionRefused, runMatching, simulateMultilateral, verifyRun } from '@diasposwap/matching-engine';

const NOW = new Date('2026-11-25T10:00:00.000Z');
const rates = referenceRates(NOW.toISOString());
let n = 0;
function order(from: CountryCode, to: CountryCode, principal: bigint, extra: Partial<TransferOrder> = {}): TransferOrder {
  n++;
  return {
    id: extra.id ?? `o${n.toString().padStart(4, '0')}`, userId: `u${n}`, fromCountry: from, toCountry: to,
    sendCurrency: COUNTRIES[from].currency, receiveCurrency: COUNTRIES[to].currency,
    principal, remaining: principal, createdAt: `2026-11-25T09:${String(n % 60).padStart(2, '0')}:00.000Z`,
    expiresAt: '2026-11-28T00:00:00.000Z', allowPartial: true, state: 'QUEUED', compliance: 'CLEARED', ...extra,
  };
}

describe('SwapEngine - bilateral', () => {
  it('level 1: exact match France -> Cameroon vs Cameroon -> France', () => {
    const a = order('FR', 'CM', 100000n); // 1000.00 EUR
    const b = order('CM', 'FR', 655957n); // 655 957 XAF
    const r = runMatching({ runId: 'r1', orders: [a, b], rates, now: NOW });
    expect(r.allocations).toHaveLength(1);
    expect(r.allocations[0]).toMatchObject({ kind: 'EXACT', takerAmount: 100000n, makerAmount: 655957n });
    expect(r.orders.map((o) => o.state)).toEqual(['MATCHED', 'MATCHED']);
  });

  it('level 2: partial match leaves the remainder queued', () => {
    const a = order('FR', 'CM', 100000n);
    const b = order('CM', 'FR', 327978n); // ~500 EUR
    const r = runMatching({ runId: 'r2', orders: [a, b], rates, now: NOW });
    expect(r.allocations).toHaveLength(1);
    const oa = r.orders.find((o) => o.id === a.id)!;
    expect(oa.state).toBe('PARTIALLY_MATCHED');
    expect(oa.remaining).toBe(50000n); // 327 978 XAF absorbs exactly 500.00 EUR (floor)
    expect(r.allocations[0]!.makerAmount).toBeLessThanOrEqual(327978n);
  });

  it('level 3: one 1000 EUR order filled by three opposite orders (400/350/250)', () => {
    const big = order('FR', 'CM', 100000n);
    const o1 = order('CM', 'FR', 262383n); // 400 EUR = 262 382.8
    const o2 = order('CM', 'FR', 229585n); // 350 EUR = 229 584.95
    const o3 = order('CM', 'FR', 163990n); // 250 EUR = 163 989.25
    const r = runMatching({ runId: 'r3', orders: [big, o1, o2, o3], rates, now: NOW });
    expect(r.allocations).toHaveLength(3);
    expect(r.allocations.reduce((s, a) => s + (a.takerOrderId === big.id ? a.takerAmount : a.makerAmount), 0n)).toBe(100000n);
    expect(r.orders.find((o) => o.id === big.id)!.state).toBe('MATCHED');
  });

  it('never matches orders that are not compliance-cleared, expired, or in the wrong state', () => {
    const a = order('FR', 'CM', 100000n, { compliance: 'REVIEW' });
    const b = order('CM', 'FR', 655957n);
    const c = order('FR', 'CM', 100000n, { expiresAt: '2026-11-25T09:00:00.000Z' });
    const d = order('FR', 'CM', 100000n, { state: 'PENDING_FUNDING' });
    const r = runMatching({ runId: 'r4', orders: [a, b, c, d], rates, now: NOW });
    expect(r.allocations).toHaveLength(0);
    expect(r.skipped).toEqual(expect.arrayContaining([
      { orderId: a.id, reason: 'COMPLIANCE_NOT_CLEARED' },
      { orderId: c.id, reason: 'EXPIRED' },
      { orderId: d.id, reason: 'NOT_MATCHABLE_STATE' },
    ]));
    expect(r.expired).toEqual([c.id]);
  });

  it('respects all-or-none orders', () => {
    const a = order('FR', 'CM', 100000n, { allowPartial: false });
    const b = order('CM', 'FR', 327978n);
    const r = runMatching({ runId: 'r5', orders: [a, b], rates, now: NOW });
    expect(r.allocations).toHaveLength(0);
    expect(r.orders.find((o) => o.id === a.id)!.remaining).toBe(100000n);
  });

  it('refuses a stale simulated rate', () => {
    const a = order('GB', 'NG', 10000n);
    const b = order('NG', 'GB', 1650000n);
    const stale = referenceRates('2026-11-24T00:00:00.000Z');
    const r = runMatching({ runId: 'r6', orders: [a, b], rates: stale, now: NOW });
    expect(r.allocations).toHaveLength(0);
    expect(r.skipped.every((s) => s.reason === 'STALE_RATE')).toBe(true);
  });

  it('is deterministic', () => {
    const os = [order('FR', 'CM', 50000n), order('CM', 'FR', 100000n), order('FR', 'CM', 70000n), order('CM', 'FR', 400000n)];
    const r1 = runMatching({ runId: 'x', orders: os, rates, now: NOW });
    const r2 = runMatching({ runId: 'x', orders: os, rates, now: NOW });
    expect(r1).toEqual(r2);
  });

  it('property: conservation and no double allocation across random books', () => {
    const pairs: [CountryCode, CountryCode][] = [['FR', 'CM'], ['FR', 'SN'], ['CA', 'CM'], ['GB', 'NG'], ['CG', 'CM']];
    const arbOrder = fc.record({
      pair: fc.constantFrom(...pairs), flip: fc.boolean(), eur: fc.integer({ min: 1, max: 4_000 }), cents: fc.integer({ min: 0, max: 99 }),
      partial: fc.boolean(), minute: fc.integer({ min: 0, max: 59 }),
    });
    fc.assert(fc.property(fc.array(arbOrder, { maxLength: 40 }), (specs) => {
      const orders = specs.map((s, i) => {
        const [x, y] = s.flip ? [s.pair[1], s.pair[0]] : s.pair;
        const cur = COUNTRIES[x].currency;
        const r = rates[cur];
        const eurCents = BigInt(s.eur * 100 + s.cents);
        const exp = cur === 'XAF' || cur === 'XOF' ? 0n : 2n;
        const principal = (eurCents * r.num * 10n ** exp) / (r.den * 100n) || 1n;
        return order(x, y, principal, { id: `p${i.toString().padStart(3, '0')}`, allowPartial: s.partial, createdAt: `2026-11-25T08:${String(s.minute).padStart(2, '0')}:00.000Z` });
      });
      const res = runMatching({ runId: 'prop', orders, rates, now: NOW });
      verifyRun(orders, res); // throws on violation
      for (const o of res.orders) expect(o.remaining >= 0n && o.remaining <= o.principal).toBe(true);
      const ids = new Set(res.allocations.map((a) => a.id));
      expect(ids.size).toBe(res.allocations.length);
    }), { numRuns: 200 });
  });
});

describe('SwapEngine - multilateral (simulation only)', () => {
  it('finds the FR -> CM -> CA -> FR cycle and reduces gross cross-border volume', () => {
    const os = [order('FR', 'CM', 100000n), order('CM', 'CA', 655957n), order('CA', 'FR', 150000n)];
    const r = simulateMultilateral(os, rates, { mode: 'simulation' });
    expect(r.simulationOnly).toBe(true);
    expect(r.bilateral).toHaveLength(0);
    expect(r.cycles).toHaveLength(1);
    expect(r.cycles[0]!.path).toEqual(['CA', 'FR', 'CM', 'CA']);
    expect(r.grossBefore).toBe(300000n);
    expect(r.grossAfterMultilateral).toBe(0n);
  });

  it('refuses production mode', () => {
    expect(() => simulateMultilateral([], rates, { mode: 'production' })).toThrow(ProductionRefused);
  });
});
