/**
 * Formatting helpers. Rule: a missing value (null/undefined/"") is NEVER rendered as 0 — callers get
 * `null` back and display the localized "Not available" label. Amounts are formatted per currency;
 * nothing here adds amounts of different currencies.
 */
export type Locale = "fr" | "en";

export function isMissing(v: unknown): v is null | undefined | "" {
  return v === null || v === undefined || v === "";
}

export function toNumber(v: string | number | null | undefined): number | null {
  if (isMissing(v)) return null;
  const n = typeof v === "number" ? v : Number(v);
  return Number.isFinite(n) ? n : null;
}

const intl = (l: Locale) => (l === "fr" ? "fr-FR" : "en-GB");

export function fmtNumber(v: string | number | null | undefined, locale: Locale, digits = 0): string | null {
  const n = toNumber(v);
  if (n === null) return null;
  return new Intl.NumberFormat(intl(locale), { maximumFractionDigits: digits, minimumFractionDigits: 0 }).format(n);
}

export function fmtAmount(v: string | number | null | undefined, currency: string | null | undefined, locale: Locale): string | null {
  const s = fmtNumber(v, locale, 0);
  if (s === null) return null;
  return currency ? `${s} ${currency}` : s;
}

/** Compact amount (e.g. "10,2 Md USD" / "10.2B USD") for chart axes and KPI tiles. */
export function fmtCompact(v: string | number | null | undefined, currency: string | null | undefined, locale: Locale): string | null {
  const n = toNumber(v);
  if (n === null) return null;
  const s = new Intl.NumberFormat(intl(locale), { notation: "compact", maximumFractionDigits: 1 }).format(n);
  return currency ? `${s} ${currency}` : s;
}

export function fmtPct(ratio: string | number | null | undefined, locale: Locale, digits = 1): string | null {
  const n = toNumber(ratio);
  if (n === null) return null;
  return new Intl.NumberFormat(intl(locale), { style: "percent", maximumFractionDigits: digits }).format(n);
}

export function fmtDate(v: string | null | undefined, locale: Locale, withTime = false): string | null {
  if (isMissing(v)) return null;
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return v;
  return new Intl.DateTimeFormat(intl(locale), withTime ? { dateStyle: "medium", timeStyle: "short", timeZone: "UTC" } : { dateStyle: "medium", timeZone: "UTC" }).format(d);
}

/** Per-currency map → sorted entries; an empty/null map yields []. Never sums currencies. */
export function currencyEntries(m: Record<string, string> | null | undefined): [string, string][] {
  if (!m) return [];
  return Object.entries(m).sort(([a], [b]) => a.localeCompare(b));
}
