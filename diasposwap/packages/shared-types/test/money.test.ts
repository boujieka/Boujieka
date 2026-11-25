import { describe, expect, it } from 'vitest';
import fc from 'fast-check';
import {
  assertTransition, canTransition, convertFloor, crossRate, formatMoney, maxBaseForQuote, parseMajor, referenceRates,
  toMajorString, TransitionError,
} from '@diasposwap/shared-types';

const rates = referenceRates('2026-11-25T10:00:00.000Z');

describe('money', () => {
  it('parses and formats without floats', () => {
    expect(parseMajor('1000', 'EUR')).toBe(100000n);
    expect(parseMajor('1 000,50', 'EUR')).toBe(100050n);
    expect(parseMajor('655957', 'XAF')).toBe(655957n);
    expect(() => parseMajor('10.5', 'XAF')).toThrow();
    expect(() => parseMajor('1.234', 'EUR')).toThrow();
    expect(() => parseMajor('abc', 'EUR')).toThrow();
    expect(toMajorString(5n, 'EUR')).toBe('0.05');
    expect(formatMoney({ amount: 123456789n, currency: 'EUR' }, 'en')).toBe('€ 1,234,567.89');
    expect(formatMoney({ amount: 655957n, currency: 'XAF' }, 'fr')).toBe('655 957 FCFA');
  });

  it('applies the official EUR/XAF peg exactly', () => {
    const r = crossRate('EUR', 'XAF', rates);
    expect(convertFloor(100000n, r)).toBe(655957n); // 1000.00 EUR -> 655 957 XAF
    expect(convertFloor(1n, r)).toBe(6n); // 0.01 EUR -> 6.55957 -> 6 XAF (floor)
  });

  it('keeps XAF and XOF distinct even at the same parity', () => {
    const r = crossRate('XAF', 'XOF', rates);
    expect(r.base).toBe('XAF');
    expect(r.quote).toBe('XOF');
    expect(convertFloor(1000n, r)).toBe(1000n);
  });

  it('property: maxBaseForQuote is the exact largest feasible amount', () => {
    const r = crossRate('EUR', 'XAF', rates);
    const r2 = crossRate('XAF', 'EUR', rates);
    fc.assert(fc.property(fc.bigInt({ min: 0n, max: 10n ** 12n }), (q) => {
      for (const rate of [r, r2]) {
        const x = maxBaseForQuote(q, rate);
        expect(convertFloor(x, rate)).toBeLessThanOrEqual(q);
        expect(convertFloor(x + 1n, rate)).toBeGreaterThan(q);
      }
    }));
  });
});

describe('state machine', () => {
  it('allows the happy path and rejects shortcuts', () => {
    const path = ['DRAFT', 'QUOTED', 'PENDING_VERIFICATION', 'PENDING_FUNDING', 'FUNDED', 'QUEUED', 'MATCHED', 'SETTLEMENT_PENDING', 'SETTLED'] as const;
    for (let i = 0; i < path.length - 1; i++) expect(canTransition(path[i]!, path[i + 1]!)).toBe(true);
    expect(() => assertTransition('QUEUED', 'SETTLED')).toThrow(TransitionError);
    expect(() => assertTransition('PENDING_FUNDING', 'MATCHED')).toThrow(TransitionError);
    expect(() => assertTransition('REFUNDED', 'QUEUED')).toThrow(TransitionError);
  });
});
