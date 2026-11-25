import { CURRENCIES, type CurrencyCode, divFloor, MoneyError, pow10 } from './money';

/**
 * An exchange rate is an exact rational number: `num / den` units of `quote` (major)
 * per 1 unit of `base` (major). Example: 1 EUR = 655.957 XAF -> { num: 655957n, den: 1000n }.
 */
export interface FxRate {
  base: CurrencyCode;
  quote: CurrencyCode;
  num: bigint;
  den: bigint;
  /** ISO timestamp of the cotation. */
  asOf: string;
  /** Seconds the cotation stays valid. */
  validForSeconds: number;
  /** Where the rate comes from. 'OFFICIAL_PEG' is a legal fixed parity; 'SIMULATED' is demo data. */
  source: 'OFFICIAL_PEG' | 'SIMULATED';
}

export function invert(rate: FxRate): FxRate {
  return { ...rate, base: rate.quote, quote: rate.base, num: rate.den, den: rate.num };
}

/** Convert minor units of `rate.base` into minor units of `rate.quote`, rounding DOWN. */
export function convertFloor(amountMinor: bigint, rate: FxRate): bigint {
  if (rate.num <= 0n || rate.den <= 0n) throw new MoneyError('Invalid FX rate');
  const eFrom = CURRENCIES[rate.base].exponent;
  const eTo = CURRENCIES[rate.quote].exponent;
  return divFloor(amountMinor * rate.num * pow10(eTo), rate.den * pow10(eFrom));
}

/**
 * Largest amount of base minor units whose floor-conversion does not exceed `quoteMinor`.
 * floor(x * k) <= Q  <=>  x <= floor(Q / k) when k > 0 (with k rational), computed exactly.
 */
export function maxBaseForQuote(quoteMinor: bigint, rate: FxRate): bigint {
  const eFrom = CURRENCIES[rate.base].exponent;
  const eTo = CURRENCIES[rate.quote].exponent;
  // x * num * 10^eTo / (den * 10^eFrom) < Q + 1  =>  x < (Q + 1) * den * 10^eFrom / (num * 10^eTo)
  const n = (quoteMinor + 1n) * rate.den * pow10(eFrom);
  const d = rate.num * pow10(eTo);
  let x = divFloor(n, d);
  if (x * d === n) x -= 1n; // strict inequality
  while (x > 0n && convertFloor(x, rate) > quoteMinor) x -= 1n; // defensive; never loops in practice
  return x < 0n ? 0n : x;
}

export function isRateValid(rate: FxRate, now: Date): boolean {
  if (rate.source === 'OFFICIAL_PEG') return true;
  return now.getTime() <= Date.parse(rate.asOf) + rate.validForSeconds * 1000;
}

export function rateToDisplay(rate: FxRate, decimals = 4): string {
  const scaled = divFloor(rate.num * pow10(decimals), rate.den).toString().padStart(decimals + 1, '0');
  return `${scaled.slice(0, -decimals)}.${scaled.slice(-decimals)}`;
}

/** Fixed parity 1 EUR = 655.957 XAF = 655.957 XOF (legal pegs of the CFA francs). */
export const EUR_CFA_PEG = { num: 655957n, den: 1000n } as const;

/**
 * Reference rate table, everything expressed against EUR.
 * EUR/XAF and EUR/XOF are the official fixed parities. ALL OTHER RATES ARE SIMULATED
 * placeholders for the demo and must be replaced by a licensed market-data feed.
 */
export function referenceRates(asOf: string): Record<CurrencyCode, FxRate> {
  const mk = (quote: CurrencyCode, num: bigint, den: bigint, source: FxRate['source']): FxRate => ({
    base: 'EUR', quote, num, den, asOf, validForSeconds: 15 * 60, source,
  });
  return {
    EUR: mk('EUR', 1n, 1n, 'OFFICIAL_PEG'),
    XAF: mk('XAF', EUR_CFA_PEG.num, EUR_CFA_PEG.den, 'OFFICIAL_PEG'),
    XOF: mk('XOF', EUR_CFA_PEG.num, EUR_CFA_PEG.den, 'OFFICIAL_PEG'),
    CAD: mk('CAD', 150n, 100n, 'SIMULATED'),
    USD: mk('USD', 108n, 100n, 'SIMULATED'),
    GBP: mk('GBP', 85n, 100n, 'SIMULATED'),
    NGN: mk('NGN', 1650n, 1n, 'SIMULATED'),
    ZAR: mk('ZAR', 20n, 1n, 'SIMULATED'),
  };
}

/** Cross rate from -> to through EUR, exact. */
export function crossRate(from: CurrencyCode, to: CurrencyCode, table: Record<CurrencyCode, FxRate>): FxRate {
  const a = table[from];
  const b = table[to];
  const source = a.source === 'SIMULATED' || b.source === 'SIMULATED' ? 'SIMULATED' : 'OFFICIAL_PEG';
  // to per from = (to per EUR) / (from per EUR)
  const num = b.num * a.den;
  const den = b.den * a.num;
  const g = gcd(num, den);
  return {
    base: from, quote: to, num: num / g, den: den / g,
    asOf: a.asOf < b.asOf ? a.asOf : b.asOf,
    validForSeconds: Math.min(a.validForSeconds, b.validForSeconds),
    source,
  };
}

export function gcd(a: bigint, b: bigint): bigint {
  let x = a < 0n ? -a : a;
  let y = b < 0n ? -b : b;
  while (y) [x, y] = [y, x % y];
  return x || 1n;
}
