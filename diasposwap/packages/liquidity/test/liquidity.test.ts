import { describe, expect, it } from 'vitest';
import { type TransferOrder, referenceRates } from '@diasposwap/shared-types';
import { analyseLiquidity } from '@diasposwap/liquidity';

const now = new Date('2026-11-25T10:00:00.000Z');
const base = { userId: 'u', createdAt: '2026-11-20T00:00:00.000Z', expiresAt: '2026-12-01T00:00:00.000Z', allowPartial: true, state: 'QUEUED', compliance: 'CLEARED' } as const;

describe('SwapLiquidity', () => {
  it('measures imbalance, prefunding need and flags uncertainty', () => {
    const orders: TransferOrder[] = [
      { ...base, id: '1', fromCountry: 'FR', toCountry: 'CM', sendCurrency: 'EUR', receiveCurrency: 'XAF', principal: 300000n, remaining: 300000n },
      { ...base, id: '2', fromCountry: 'CM', toCountry: 'FR', sendCurrency: 'XAF', receiveCurrency: 'EUR', principal: 655957n, remaining: 655957n },
    ];
    const fr = analyseLiquidity({ orders, rates: referenceRates(now.toISOString()), now }).find((c) => c.corridorId === 'FR-CM')!;
    expect(fr.pendingAB).toBe(300000n);
    expect(fr.pendingBA).toBe(100000n);
    expect(fr.matchable).toBe(100000n);
    expect(fr.prefundingNeed).toBe(200000n);
    expect(fr.dominantDirection).toBe('FR>CM');
    expect(fr.imbalanceBps).toBe(5000);
    expect(fr.uncertainty).toBe('HIGH');
  });
});
