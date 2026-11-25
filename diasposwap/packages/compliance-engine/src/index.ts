import {
  type CorridorConfig, type CountryCode, type CurrencyCode, type FxRate,
  INITIAL_CORRIDORS, convertFloor, crossRate, findCorridor,
} from '@diasposwap/shared-types';

/**
 * Compliance engine - SIMULATED. Every decision carries `simulated: true`.
 * It is NOT a real KYC/AML/sanctions system: the watchlist is fictional and the thresholds
 * are demo hypotheses, not regulatory figures. Real deployment requires licensed screening
 * providers and legal validation per jurisdiction (EU, CEMAC, UMOA, Canada, US, UK, Nigeria, South Africa).
 */
export type KycLevel = 'NONE' | 'BASIC' | 'VERIFIED' | 'ENHANCED';

export interface CustomerProfile {
  userId: string;
  fullName: string;
  country: CountryCode;
  kycLevel: KycLevel;
  emailVerified: boolean;
  phoneVerified: boolean;
  /** Politically exposed person flag (simulated declaration). */
  pep: boolean;
}

export interface BeneficiaryProfile {
  id: string;
  fullName: string;
  country: CountryCode;
  verified: boolean;
}

export interface TransferRequest {
  amountMinor: bigint;
  currency: CurrencyCode;
  from: CountryCode;
  to: CountryCode;
}

export interface HistoryItem { at: string; eurCents: bigint }

export type Decision = 'ALLOW' | 'REVIEW' | 'BLOCK';

export interface ComplianceResult {
  decision: Decision;
  reasons: string[];
  checks: { name: string; passed: boolean; detail: string }[];
  simulated: true;
}

/** Per-level limits in EUR cents (single transfer, rolling 30 days). Demo hypotheses only. */
export const KYC_LIMITS: Readonly<Record<KycLevel, { single: bigint; rolling30d: bigint }>> = {
  NONE: { single: 0n, rolling30d: 0n },
  BASIC: { single: 150_00n, rolling30d: 500_00n },
  VERIFIED: { single: 3_000_00n, rolling30d: 10_000_00n },
  ENHANCED: { single: 5_000_00n, rolling30d: 30_000_00n },
};

/** Fictional watchlist used only to exercise the screening path in tests and demo. */
export const SIMULATED_WATCHLIST: readonly string[] = ['Sanction Testperson', 'Blocked Demo Entity', 'Ivan Exemplenko'];

export function normalizeName(s: string): string {
  return s.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().replace(/[^a-z ]/g, ' ').split(/\s+/).filter(Boolean).sort().join(' ');
}

export function screenName(name: string, list: readonly string[] = SIMULATED_WATCHLIST): boolean {
  const n = normalizeName(name);
  return list.some((w) => normalizeName(w) === n);
}

export interface EvaluateInput {
  customer: CustomerProfile;
  beneficiary: BeneficiaryProfile;
  request: TransferRequest;
  history: readonly HistoryItem[];
  now: Date;
  rates: Record<CurrencyCode, FxRate>;
  corridors?: readonly CorridorConfig[];
  watchlist?: readonly string[];
}

export function evaluateTransfer(input: EvaluateInput): ComplianceResult {
  const { customer, beneficiary, request, history, now, rates } = input;
  const checks: ComplianceResult['checks'] = [];
  const block: string[] = [];
  const review: string[] = [];
  const add = (name: string, passed: boolean, detail: string, severity: 'BLOCK' | 'REVIEW') => {
    checks.push({ name, passed, detail });
    if (!passed) (severity === 'BLOCK' ? block : review).push(name);
  };

  const corridor = findCorridor(request.from, request.to, input.corridors ?? INITIAL_CORRIDORS);
  add('corridor', !!corridor && corridor.mode === 'SIMULATION', corridor ? `${corridor.id} ${corridor.mode}` : 'unknown corridor', 'BLOCK');
  add('beneficiary_country', beneficiary.country === request.to, `${beneficiary.country} vs ${request.to}`, 'BLOCK');
  add('contact_verified', customer.emailVerified && customer.phoneVerified, 'email + phone', 'BLOCK');
  add('kyc_present', customer.kycLevel !== 'NONE', customer.kycLevel, 'BLOCK');
  add('sanctions_customer', !screenName(customer.fullName, input.watchlist), 'simulated watchlist', 'BLOCK');
  add('sanctions_beneficiary', !screenName(beneficiary.fullName, input.watchlist), 'simulated watchlist', 'BLOCK');
  add('beneficiary_verified', beneficiary.verified, 'beneficiary verification', 'REVIEW');
  add('pep', !customer.pep || customer.kycLevel === 'ENHANCED', customer.pep ? 'PEP requires enhanced due diligence' : 'not PEP', 'REVIEW');

  const eur = convertFloor(request.amountMinor, crossRate(request.currency, 'EUR', rates));
  const limits = KYC_LIMITS[customer.kycLevel];
  add('single_limit', eur <= limits.single, `${eur} <= ${limits.single} EUR cents`, 'BLOCK');
  const since = now.getTime() - 30 * 86400_000;
  const rolling = history.filter((h) => Date.parse(h.at) >= since).reduce((s, h) => s + h.eurCents, 0n);
  add('rolling_30d_limit', rolling + eur <= limits.rolling30d, `${rolling + eur} <= ${limits.rolling30d} EUR cents`, 'BLOCK');
  const last24h = history.filter((h) => Date.parse(h.at) >= now.getTime() - 86400_000).length;
  add('velocity_24h', last24h < 5, `${last24h} transfers in 24h`, 'REVIEW');
  // structuring heuristic: several amounts just under the single limit
  const nearLimit = history.filter((h) => Date.parse(h.at) >= since && h.eurCents * 100n >= limits.single * 90n).length;
  add('structuring_pattern', nearLimit < 3, `${nearLimit} transfers >= 90% of limit in 30d`, 'REVIEW');

  const decision: Decision = block.length ? 'BLOCK' : review.length ? 'REVIEW' : 'ALLOW';
  return { decision, reasons: block.length ? block : review, checks, simulated: true };
}
