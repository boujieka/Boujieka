import { describe, expect, it } from 'vitest';
import { referenceRates } from '@diasposwap/shared-types';
import { type CustomerProfile, evaluateTransfer, screenName } from '@diasposwap/compliance-engine';

const now = new Date('2026-11-25T10:00:00.000Z');
const rates = referenceRates(now.toISOString());
const customer: CustomerProfile = { userId: 'u1', fullName: 'Amina Mbarga', country: 'FR', kycLevel: 'VERIFIED', emailVerified: true, phoneVerified: true, pep: false };
const beneficiary = { id: 'b1', fullName: 'Paul Mbarga', country: 'CM' as const, verified: true };
const request = { amountMinor: 100000n, currency: 'EUR' as const, from: 'FR' as const, to: 'CM' as const };

describe('compliance (simulated)', () => {
  it('allows a normal verified transfer and labels itself simulated', () => {
    const r = evaluateTransfer({ customer, beneficiary, request, history: [], now, rates });
    expect(r.decision).toBe('ALLOW');
    expect(r.simulated).toBe(true);
  });
  it('blocks watchlist hits regardless of accents/order', () => {
    expect(screenName('testperson SANCTION')).toBe(true);
    const r = evaluateTransfer({ customer, beneficiary: { ...beneficiary, fullName: 'Sanction Testpérson' }, request, history: [], now, rates });
    expect(r.decision).toBe('BLOCK');
    expect(r.reasons).toContain('sanctions_beneficiary');
  });
  it('enforces KYC limits and rolling limits', () => {
    expect(evaluateTransfer({ customer: { ...customer, kycLevel: 'BASIC' }, beneficiary, request, history: [], now, rates }).reasons).toContain('single_limit');
    const history = Array.from({ length: 4 }, () => ({ at: '2026-11-20T00:00:00.000Z', eurCents: 2_500_00n }));
    expect(evaluateTransfer({ customer, beneficiary, request, history, now, rates }).reasons).toContain('rolling_30d_limit');
  });
  it('sends PEPs and unverified beneficiaries to review', () => {
    expect(evaluateTransfer({ customer: { ...customer, pep: true }, beneficiary, request, history: [], now, rates }).decision).toBe('REVIEW');
    expect(evaluateTransfer({ customer, beneficiary: { ...beneficiary, verified: false }, request, history: [], now, rates }).decision).toBe('REVIEW');
  });
  it('blocks unknown corridors', () => {
    const r = evaluateTransfer({ customer, beneficiary: { ...beneficiary, country: 'NG' }, request: { ...request, to: 'NG' }, history: [], now, rates });
    expect(r.decision).toBe('BLOCK');
  });
});
