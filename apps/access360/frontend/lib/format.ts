// Number formatting. Every figure displayed comes from the API; these helpers only format it.
// Negatives are shown in parentheses, percentages with one decimal.

export type Loc = "en" | "fr";
const tag = (l: Loc) => (l === "fr" ? "fr-FR" : "en-US");

export const DASH = "–";

function isNum(v: unknown): v is number {
  return typeof v === "number" && Number.isFinite(v);
}

function paren(s: string, neg: boolean) {
  return neg ? `(${s})` : s;
}

export function num(v: unknown, l: Loc = "en", decimals?: number): string {
  if (!isNum(v)) return DASH;
  const d = decimals ?? (Math.abs(v) < 10 && v !== Math.trunc(v) ? 2 : 0);
  const s = new Intl.NumberFormat(tag(l), { minimumFractionDigits: d, maximumFractionDigits: d }).format(Math.abs(v));
  return paren(s, v < 0);
}

/** Money with an explicit ISO-like currency code (LCY code from the inputs, or USD). */
export function money(v: unknown, ccy: string, l: Loc = "en", decimals?: number): string {
  if (!isNum(v)) return DASH;
  const d = decimals ?? (Math.abs(v) < 100 ? 2 : 0);
  const s = new Intl.NumberFormat(tag(l), { minimumFractionDigits: d, maximumFractionDigits: d }).format(Math.abs(v));
  return paren(`${s} ${ccy}`, v < 0);
}

/** Compact money for headline tiles, e.g. 1.43M USD. */
export function moneyCompact(v: unknown, ccy: string, l: Loc = "en"): string {
  if (!isNum(v)) return DASH;
  const s = new Intl.NumberFormat(tag(l), { notation: "compact", maximumFractionDigits: 2 }).format(Math.abs(v));
  return paren(`${s} ${ccy}`, v < 0);
}

export function pct(v: unknown, l: Loc = "en"): string {
  if (!isNum(v)) return DASH;
  const s = new Intl.NumberFormat(tag(l), { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(Math.abs(v * 100));
  return paren(`${s}%`, v < 0);
}

export function ratio(v: unknown, l: Loc = "en"): string {
  if (!isNum(v)) return DASH;
  const s = new Intl.NumberFormat(tag(l), { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Math.abs(v));
  return paren(`${s}x`, v < 0);
}

export function years(v: unknown, l: Loc = "en"): string {
  if (!isNum(v)) return DASH;
  return `${num(v, l, 1)} ${l === "fr" ? "ans" : "yrs"}`;
}

export function date(v: string | null | undefined, l: Loc = "en"): string {
  if (!v) return DASH;
  const d = new Date(v.length === 10 ? `${v}T00:00:00` : v);
  if (Number.isNaN(d.getTime())) return v;
  return new Intl.DateTimeFormat(tag(l), { year: "numeric", month: "short", day: "2-digit" }).format(d);
}

export function dateTime(v: string | null | undefined, l: Loc = "en"): string {
  if (!v) return DASH;
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return v;
  return new Intl.DateTimeFormat(tag(l), { year: "numeric", month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit" }).format(d);
}

/** Axis tick formatter: compact, parentheses for negatives. */
export function axisCompact(l: Loc) {
  const f = new Intl.NumberFormat(tag(l), { notation: "compact", maximumFractionDigits: 1 });
  return (v: number) => (v < 0 ? `(${f.format(-v)})` : f.format(v));
}
