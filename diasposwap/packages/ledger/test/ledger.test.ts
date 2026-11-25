import { describe, expect, it } from 'vitest';
import fc from 'fast-check';
import { Ledger, LedgerError } from '@diasposwap/ledger';

const A = { type: 'COLLECTION', currency: 'EUR', scope: 'FR' } as const;
const L = { type: 'CUSTOMER_FUNDS', currency: 'EUR', scope: 'FR:o1' } as const;
const X = { type: 'COLLECTION', currency: 'XAF', scope: 'CM' } as const;

describe('ledger', () => {
  it('rejects unbalanced or cross-currency-unbalanced entries', () => {
    const l = new Ledger();
    expect(() => l.post({ idempotencyKey: 'k', at: '', description: '', reference: '', postings: [{ account: A, amount: 100n }, { account: L, amount: -99n }] })).toThrow(LedgerError);
    expect(() => l.post({ idempotencyKey: 'k', at: '', description: '', reference: '', postings: [{ account: A, amount: 100n }, { account: X, amount: -100n }] })).toThrow(LedgerError);
  });

  it('is idempotent and immutable; corrections are reversals', () => {
    const l = new Ledger();
    const e = l.post({ idempotencyKey: 'k1', at: 't', description: 'd', reference: 'r', postings: [{ account: A, amount: 100n }, { account: L, amount: -100n }] });
    expect(l.post({ idempotencyKey: 'k1', at: 't', description: 'd', reference: 'r', postings: [{ account: A, amount: 100n }, { account: L, amount: -100n }] })).toBe(e);
    expect(() => l.post({ idempotencyKey: 'k1', at: 't', description: 'd', reference: 'r', postings: [{ account: A, amount: 5n }, { account: L, amount: -5n }] })).toThrow();
    expect(Object.isFrozen(e)).toBe(true);
    expect(() => { (e.postings[0] as { amount: bigint }).amount = 1n; }).toThrow();
    expect(l.naturalBalance(L)).toBe(100n);
    const rev = l.reverse(e.id, 't2', 'test');
    expect(rev.reverses).toBe(e.id);
    expect(l.balance(A)).toBe(0n);
    expect(l.all()).toHaveLength(2);
    expect(() => l.reverse(e.id, 't3', 'again')).toThrow();
  });

  it('property: any sequence of balanced entries keeps a zero trial balance', () => {
    fc.assert(fc.property(fc.array(fc.bigInt({ min: 1n, max: 10n ** 9n }), { maxLength: 50 }), (amounts) => {
      const l = new Ledger();
      amounts.forEach((a, i) => l.post({ idempotencyKey: `k${i}`, at: '', description: '', reference: '', postings: [{ account: A, amount: a }, { account: L, amount: -a }] }));
      expect(l.isBalanced()).toBe(true);
    }));
  });
});
