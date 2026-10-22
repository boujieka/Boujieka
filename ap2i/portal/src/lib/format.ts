import type { Money } from "./agg";

export type Locale = "fr" | "en";

export function fmtNum(v: number | null | undefined, locale: Locale, digits = 0): string {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  return new Intl.NumberFormat(locale === "fr" ? "fr-FR" : "en-US", { maximumFractionDigits: digits }).format(v);
}

/** Compact amount: 17.95 Md / 17.95 bn */
export function fmtAmount(v: number | null | undefined, locale: Locale, currency?: string): string {
  if (v === null || v === undefined) return "—";
  const a = Math.abs(v);
  const [div, sfx] = a >= 1e9 ? [1e9, locale === "fr" ? " Md" : " bn"] : a >= 1e6 ? [1e6, locale === "fr" ? " M" : " M"] : a >= 1e3 ? [1e3, " k"] : [1, ""];
  return `${fmtNum(v / div, locale, div === 1 ? 0 : 2)}${sfx}${currency ? " " + currency : ""}`;
}

export function fmtPct(v: number | null | undefined, locale: Locale, digits = 0): string {
  if (v === null || v === undefined) return "—";
  return new Intl.NumberFormat(locale === "fr" ? "fr-FR" : "en-US", { style: "percent", maximumFractionDigits: digits }).format(v);
}

export function fmtDate(d: string | null | undefined, locale: Locale): string {
  if (!d) return "—";
  const t = Date.parse(d);
  if (Number.isNaN(t)) return d;
  return new Date(t).toLocaleDateString(locale === "fr" ? "fr-FR" : "en-GB", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
}

export function currencyLines(m: Record<string, number>, locale: Locale): string {
  const ks = Object.keys(m).sort();
  return ks.length ? ks.map((k) => fmtAmount(m[k], locale, k)).join(" · ") : "—";
}

export function moneyTooltip(m: Money, locale: Locale, t: (k: string) => string): string {
  const parts = [`${t("money.usdEq")}: ${fmtAmount(m.usd, locale, "USD")}`, `${t("money.byCurrency")}: ${currencyLines(m.byCurrency, locale)}`];
  if (Object.keys(m.unconverted).length) parts.push(`${t("money.unconverted")}: ${currencyLines(m.unconverted, locale)}`);
  parts.push(`${t("money.transactions")}: ${m.n}`);
  return parts.join("<br/>");
}

export const escapeHtml = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
