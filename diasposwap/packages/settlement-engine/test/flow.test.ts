import { createHmac } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { hmacHex, SimulatedProvider, SwapSimulator, seedDemo, SimulationError } from '@diasposwap/settlement-engine';
import { analyseLiquidity } from '@diasposwap/liquidity';

function clock(start = '2026-11-25T10:00:00.000Z') {
  let t = Date.parse(start);
  return { now: () => new Date(t), advance: (ms: number) => { t += ms; } };
}

function setup(opts: { benBRef?: string } = {}) {
  const c = clock();
  const sim = new SwapSimulator({ now: c.now });
  sim.addUser({ profile: { userId: 'alice', fullName: 'Amina Mbarga', country: 'FR', kycLevel: 'VERIFIED', emailVerified: true, phoneVerified: true, pep: false }, fundingRef: 'SIM-FR-****0001', history: [] });
  sim.addUser({ profile: { userId: 'bob', fullName: 'Jean Essomba', country: 'CM', kycLevel: 'VERIFIED', emailVerified: true, phoneVerified: true, pep: false }, fundingRef: 'SIM-CM-****0002', history: [] });
  sim.addBeneficiary({ id: 'benA', ownerId: 'alice', fullName: 'Paul Mbarga', country: 'CM', verified: true, accountRef: 'SIM-MOMO-CM-****11' });
  sim.addBeneficiary({ id: 'benB', ownerId: 'bob', fullName: 'Grace Essomba', country: 'FR', verified: true, accountRef: opts.benBRef ?? 'SIM-IBAN-FR-****22' });
  return { sim, c };
}

function place(sim: SwapSimulator, user: 'alice' | 'bob', amount: bigint, key: string, allowPartial = true) {
  const q = user === 'alice' ? sim.quote('alice', 'FR', 'CM', amount) : sim.quote('bob', 'CM', 'FR', amount);
  const o = sim.createOrder({ quoteId: q.id, beneficiaryId: user === 'alice' ? 'benA' : 'benB', idempotencyKey: key, allowPartial });
  sim.fund(o.id);
  return o;
}

describe('portable HMAC', () => {
  it('matches node:crypto', () => {
    for (const msg of ['', 'abc', 'x'.repeat(1000), '{"é":"ü"}']) {
      expect(hmacHex('secret', msg)).toBe(createHmac('sha256', 'secret').update(msg).digest('hex'));
    }
    expect(hmacHex('k'.repeat(100), 'm')).toBe(createHmac('sha256', 'k'.repeat(100)).update('m').digest('hex'));
  });
});

describe('vertical MVP: France -> Cameroon swap, end to end (simulation)', () => {
  it('quote, order, compliance, funding, exact match, two local payouts, ledger, reconciliation', () => {
    const { sim } = setup();
    const q = sim.quote('alice', 'FR', 'CM', 100000n);
    expect(q.fee).toBe(750n); // 0.75 % of 1000 EUR (simulation hypothesis)
    expect(q.total).toBe(100750n);
    expect(q.estimatedReceive).toBe(655957n);

    const a = sim.createOrder({ quoteId: q.id, beneficiaryId: 'benA', idempotencyKey: 'k-a' });
    expect(a.state).toBe('PENDING_FUNDING');
    expect(sim.createOrder({ quoteId: q.id, beneficiaryId: 'benA', idempotencyKey: 'k-a' })).toBe(a); // idempotent
    sim.fund(a.id);
    const b = place(sim, 'bob', 655957n, 'k-b');
    sim.settleAllPending(); // collections confirmed by signed webhooks
    expect(a.state).toBe('QUEUED');
    expect(b.state).toBe('QUEUED');

    const run = sim.runMatching();
    expect(run.allocations).toHaveLength(1);
    expect(a.state).toBe('SETTLEMENT_PENDING');
    expect(b.state).toBe('SETTLEMENT_PENDING');

    sim.settleAllPending(); // both local payouts succeed
    expect(a.state).toBe('SETTLED');
    expect(b.state).toBe('SETTLED');

    const va = sim.userView(a.id);
    expect(va.beneficiaryReceived).toBe(655957n); // Paul received XAF in Cameroon
    expect(sim.userView(b.id).beneficiaryReceived).toBe(100000n); // Grace received EUR in France
    expect(JSON.stringify(va, (_k, v) => (typeof v === 'bigint' ? v.toString() : v))).not.toMatch(/bob|Essomba|SIM-IBAN/);

    expect(sim.ledger.isBalanced()).toBe(true);
    const rec = sim.reconcile();
    expect(rec.issues).toEqual([]);
    // what stays in the FR collection account is exactly the fee
    expect(sim.ledger.balance({ type: 'COLLECTION', currency: 'EUR', scope: 'FR' })).toBe(750n);
    expect(sim.ledger.balance({ type: 'COLLECTION', currency: 'XAF', scope: 'CM' })).toBe(4920n); // bob's 0.75 % fee
    // a full audit trail exists
    expect(sim.audit.filter((s) => s.orderId === a.id).map((s) => s.to)).toEqual(
      ['QUOTED', 'PENDING_VERIFICATION', 'PENDING_FUNDING', 'FUNDED', 'QUEUED', 'MATCHED', 'SETTLEMENT_PENDING', 'SETTLED']);
  });

  it('partial match then completion by a second order (multiple matching)', () => {
    const { sim } = setup();
    const a = place(sim, 'alice', 100000n, 'a');
    const b1 = place(sim, 'bob', 327978n, 'b1');
    sim.settleAllPending();
    sim.runMatching();
    expect(a.state).toBe('PARTIALLY_MATCHED');
    sim.settleAllPending();
    expect(a.state).toBe('PARTIALLY_MATCHED'); // not settled while unmatched remainder exists
    const b2 = place(sim, 'bob', 327979n, 'b2');
    sim.settleAllPending();
    sim.runMatching();
    sim.settleAllPending();
    expect(a.state).toBe('SETTLED');
    expect(sim.userView(a.id).matchCount).toBe(2);
    expect([b1.state, b2.state]).toEqual(['SETTLED', 'SETTLED']);
    expect(sim.reconcile().issues).toEqual([]);
  });

  it('expired unmatched order is refunded in full, fee included', () => {
    const { sim, c } = setup();
    const a = place(sim, 'alice', 100000n, 'a');
    sim.settleAllPending();
    c.advance(73 * 3600_000);
    sim.runMatching();
    expect(a.state).toBe('REFUND_PENDING');
    sim.settleAllPending();
    expect(a.state).toBe('REFUNDED');
    expect(sim.ledger.balance({ type: 'COLLECTION', currency: 'EUR', scope: 'FR' })).toBe(0n);
    expect(sim.reconcile().issues).toEqual([]);
  });

  it('cancellation: allowed before funding or while queued unmatched, refused once matched', () => {
    const { sim } = setup();
    const q = sim.quote('alice', 'FR', 'CM', 1000n);
    const o = sim.createOrder({ quoteId: q.id, beneficiaryId: 'benA', idempotencyKey: 'c1' });
    expect(sim.cancel(o.id, 'alice').state).toBe('CANCELLED');
    const a = place(sim, 'alice', 100000n, 'c2');
    sim.settleAllPending();
    expect(sim.cancel(a.id, 'alice').state).toBe('REFUND_PENDING');
    const a2 = place(sim, 'alice', 100000n, 'c3');
    place(sim, 'bob', 655957n, 'c4');
    sim.settleAllPending();
    sim.runMatching();
    expect(() => sim.cancel(a2.id, 'alice')).toThrow(SimulationError);
  });

  it('failure of one settlement leg: retries, then exception + DISPUTED, never SETTLED; operator fix completes it', () => {
    const { sim } = setup({ benBRef: 'SIM-IBAN-FR-****22-FAIL' });
    const a = place(sim, 'alice', 100000n, 'a');
    const b = place(sim, 'bob', 655957n, 'b');
    sim.settleAllPending();
    sim.runMatching();
    sim.settleAllPending();
    expect(a.state).toBe('SETTLED'); // alice's beneficiary in Cameroon was paid
    expect(b.state).toBe('DISPUTED'); // bob's beneficiary payout in France failed 3 times
    expect(sim.exceptions).toHaveLength(1);
    const po = [...sim.payouts.values()].find((p) => p.beneficiaryOrderId === b.id)!;
    expect(po.attempts).toBe(3);
    // money for bob's beneficiary is still owed, not lost
    expect(sim.ledger.naturalBalance({ type: 'BENEFICIARY_PAYABLE', currency: 'EUR', scope: `FR:${b.id}` })).toBe(100000n);
    expect(sim.reconcile().issues).toEqual([]);
    sim.resolvePayoutException(po.id, 'SIM-IBAN-FR-****33');
    sim.settleAllPending();
    expect(b.state).toBe('SETTLED');
  });

  it('webhook security: forged signature rejected, replay ignored, no double payment', () => {
    const { sim } = setup();
    const a = place(sim, 'alice', 100000n, 'a');
    const p = sim.providers.find((x) => x.id === 'sim_sepa') as SimulatedProvider;
    const wh = p.complete(a.collectionRef!);
    expect(sim.handleWebhook('sim_sepa', wh.rawBody, 'deadbeef')).toEqual({ accepted: false, reason: 'INVALID_SIGNATURE' });
    expect(sim.handleWebhook('sim_sepa', wh.rawBody.replace('SUCCEEDED', 'FAILED'), wh.signature).accepted).toBe(false);
    expect(sim.handleWebhook('sim_sepa', wh.rawBody, wh.signature)).toEqual({ accepted: true });
    expect(sim.handleWebhook('sim_sepa', wh.rawBody, wh.signature)).toEqual({ accepted: true, duplicate: true });
    expect(sim.ledger.all().filter((e) => e.reference === a.id)).toHaveLength(1);
    // same funding requested twice -> same provider operation
    expect(() => sim.fund(a.id)).toThrow(); // no longer PENDING_FUNDING
    expect(p.all().filter((o) => o.kind === 'COLLECTION')).toHaveLength(1);
  });

  it('compliance block stops the order before funding; matching cannot bypass it', () => {
    const { sim } = setup();
    sim.addBeneficiary({ id: 'bad', ownerId: 'alice', fullName: 'Ivan Exemplenko', country: 'CM', verified: true, accountRef: 'x' });
    const q = sim.quote('alice', 'FR', 'CM', 100000n);
    const o = sim.createOrder({ quoteId: q.id, beneficiaryId: 'bad', idempotencyKey: 'bad' });
    expect(o.state).toBe('FAILED');
    expect(() => sim.fund(o.id)).toThrow();
    place(sim, 'bob', 655957n, 'b');
    sim.settleAllPending();
    expect(sim.runMatching().allocations).toHaveLength(0);
  });

  it('concurrent matching runs are refused and a second sequential run does not double allocate', () => {
    const { sim } = setup();
    place(sim, 'alice', 100000n, 'a');
    place(sim, 'bob', 655957n, 'b');
    sim.settleAllPending();
    (sim as unknown as { matchingLock: boolean }).matchingLock = true;
    expect(() => sim.runMatching()).toThrow(/in progress/);
    (sim as unknown as { matchingLock: boolean }).matchingLock = false;
    expect(sim.runMatching().allocations).toHaveLength(1);
    expect(sim.runMatching().allocations).toHaveLength(0);
    expect(sim.payouts.size).toBe(2);
  });

  it('rejects an expired quote', () => {
    const { sim, c } = setup();
    const q = sim.quote('alice', 'FR', 'CM', 1000n);
    c.advance(16 * 60_000);
    expect(() => sim.createOrder({ quoteId: q.id, beneficiaryId: 'benA', idempotencyKey: 'x' })).toThrow(/expired/i);
  });
});

describe('demo dataset', () => {
  it('generates a reproducible 1000-user / 5000-order book that stays balanced and reconciled', () => {
    const c = clock();
    const sim = new SwapSimulator({ now: c.now });
    const seeded = seedDemo(sim, { seed: 7 });
    expect(seeded.users).toHaveLength(1000);
    expect(seeded.orders.length + seeded.failedCreates).toBe(5000);
    const run = sim.runMatching();
    sim.settleAllPending();
    expect(run.allocations.length).toBeGreaterThan(100);
    const kinds = new Set(run.allocations.map((a) => a.kind));
    expect(kinds.has('PARTIAL')).toBe(true);
    const states = new Set([...sim.orders.values()].map((o) => o.state));
    for (const s of ['SETTLED', 'FAILED', 'QUEUED']) expect(states.has(s as never)).toBe(true);
    expect(sim.ledger.isBalanced()).toBe(true);
    expect(sim.reconcile().issues).toEqual([]);
    const liq = analyseLiquidity({ orders: [...sim.orders.values()], rates: sim.rates(), now: c.now() });
    expect(liq).toHaveLength(10);
    // same seed -> same result
    const sim2 = new SwapSimulator({ now: clock().now });
    seedDemo(sim2, { seed: 7 });
    expect(sim2.runMatching().allocations.length).toBe(run.allocations.length);
  }, 60_000);
});
