/**
 * Money is always held as an integer number of MINOR units (bigint).
 * JavaScript floating point numbers are never used for amounts.
 */
export type CurrencyCode = 'EUR' | 'XAF' | 'XOF' | 'CAD' | 'USD' | 'GBP' | 'NGN' | 'ZAR';

export interface CurrencyInfo {
  code: CurrencyCode;
  /** ISO 4217 minor-unit exponent (EUR = 2, XAF/XOF = 0). */
  exponent: number;
  nameFr: string;
  nameEn: string;
  symbol: string;
}

/** ISO 4217 minor units. XAF (CEMAC) and XOF (UEMOA) are distinct currencies, both with 0 decimals. */
export const CURRENCIES: Readonly<Record<CurrencyCode, CurrencyInfo>> = {
  EUR: { code: 'EUR', exponent: 2, nameFr: 'Euro', nameEn: 'Euro', symbol: '€' },
  XAF: { code: 'XAF', exponent: 0, nameFr: 'Franc CFA (CEMAC)', nameEn: 'Central African CFA franc', symbol: 'FCFA' },
  XOF: { code: 'XOF', exponent: 0, nameFr: 'Franc CFA (UEMOA)', nameEn: 'West African CFA franc', symbol: 'FCFA' },
  CAD: { code: 'CAD', exponent: 2, nameFr: 'Dollar canadien', nameEn: 'Canadian dollar', symbol: 'CA$' },
  USD: { code: 'USD', exponent: 2, nameFr: 'Dollar américain', nameEn: 'US dollar', symbol: 'US$' },
  GBP: { code: 'GBP', exponent: 2, nameFr: 'Livre sterling', nameEn: 'Pound sterling', symbol: '£' },
  NGN: { code: 'NGN', exponent: 2, nameFr: 'Naira', nameEn: 'Naira', symbol: '₦' },
  ZAR: { code: 'ZAR', exponent: 2, nameFr: 'Rand', nameEn: 'Rand', symbol: 'R' },
};

export interface Money {
  readonly amount: bigint; // minor units
  readonly currency: CurrencyCode;
}

export class MoneyError extends Error {}

export function money(amount: bigint, currency: CurrencyCode): Money {
  return { amount, currency };
}

function sameCurrency(a: Money, b: Money): void {
  if (a.currency !== b.currency) throw new MoneyError(`Currency mismatch: ${a.currency} vs ${b.currency}`);
}

export const add = (a: Money, b: Money): Money => (sameCurrency(a, b), money(a.amount + b.amount, a.currency));
export const sub = (a: Money, b: Money): Money => (sameCurrency(a, b), money(a.amount - b.amount, a.currency));
export const isZero = (a: Money): boolean => a.amount === 0n;
export const minBig = (a: bigint, b: bigint): bigint => (a < b ? a : b);
export const maxBig = (a: bigint, b: bigint): bigint => (a > b ? a : b);
export const pow10 = (n: number): bigint => 10n ** BigInt(n);

/** Integer division rounding towards negative infinity (amounts are non-negative in practice). */
export function divFloor(n: bigint, d: bigint): bigint {
  if (d === 0n) throw new MoneyError('Division by zero');
  const q = n / d;
  return (n % d !== 0n && (n < 0n) !== (d < 0n)) ? q - 1n : q;
}

export function divCeil(n: bigint, d: bigint): bigint {
  return -divFloor(-n, d);
}

/**
 * Parse a decimal string ("1000", "1000.5", "1 000,50") into minor units.
 * Rejects more decimals than the currency allows rather than silently rounding.
 */
export function parseMajor(input: string, currency: CurrencyCode): bigint {
  const exp = CURRENCIES[currency].exponent;
  const cleaned = input.trim().replace(/[\s  ]/g, '').replace(',', '.');
  if (!/^\d+(\.\d+)?$/.test(cleaned)) throw new MoneyError(`Invalid amount: "${input}"`);
  const [intPart = '0', frac = ''] = cleaned.split('.');
  if (frac.length > exp) throw new MoneyError(`${currency} allows at most ${exp} decimals`);
  return BigInt(intPart) * pow10(exp) + BigInt((frac + '0'.repeat(exp)).slice(0, exp) || '0');
}

/** Format minor units as a plain decimal string, e.g. 100050n EUR -> "1000.50". */
export function toMajorString(amount: bigint, currency: CurrencyCode): string {
  const exp = CURRENCIES[currency].exponent;
  const neg = amount < 0n;
  const abs = neg ? -amount : amount;
  if (exp === 0) return `${neg ? '-' : ''}${abs}`;
  const s = abs.toString().padStart(exp + 1, '0');
  return `${neg ? '-' : ''}${s.slice(0, -exp)}.${s.slice(-exp)}`;
}

/** Human formatting with thousands separators (locale-light, no floats). */
export function formatMoney(m: Money, locale: 'fr' | 'en' = 'fr'): string {
  const [intPart = '0', frac] = toMajorString(m.amount, m.currency).split('.');
  const neg = intPart.startsWith('-');
  const digits = neg ? intPart.slice(1) : intPart;
  const sep = locale === 'fr' ? ' ' : ',';
  const dec = locale === 'fr' ? ',' : '.';
  const grouped = digits.replace(/\B(?=(\d{3})+(?!\d))/g, sep);
  const body = `${neg ? '-' : ''}${grouped}${frac !== undefined ? dec + frac : ''}`;
  const sym = CURRENCIES[m.currency].symbol;
  return locale === 'fr' ? `${body} ${sym}` : `${sym} ${body}`;
}
