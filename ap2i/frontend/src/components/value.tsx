"use client";

import { currencyEntries, fmtAmount, fmtDate, fmtNumber, fmtPct, isMissing } from "@/lib/format";
import { useI18n } from "./i18n-provider";

/** The single place where a missing value is rendered: always the "Not available" label, never 0. */
export function NA() {
  const { d } = useI18n();
  return <span className="text-muted italic">{d.common.na}</span>;
}

export function V({ value }: { value: React.ReactNode | null | undefined }) {
  if (value === null || value === undefined || value === "") return <NA />;
  return <>{value}</>;
}

export function Num({ value, digits = 0 }: { value: string | number | null | undefined; digits?: number }) {
  const { locale } = useI18n();
  const s = fmtNumber(value, locale, digits);
  return s === null ? <NA /> : <span className="tabular-nums">{s}</span>;
}

export function Amount({ value, currency }: { value: string | number | null | undefined; currency: string | null | undefined }) {
  const { locale } = useI18n();
  const s = fmtAmount(value, currency, locale);
  return s === null ? <NA /> : <span className="whitespace-nowrap tabular-nums">{s}</span>;
}

/** Per-currency amounts listed separately — never summed. null / empty map → Not available. */
export function MoneyList({ value, inline = false }: { value: Record<string, string> | null | undefined; inline?: boolean }) {
  const { locale } = useI18n();
  const entries = currencyEntries(value);
  if (!entries.length) return <NA />;
  if (inline) {
    return (
      <span className="tabular-nums">
        {entries.map(([c, v], i) => (
          <span key={c} className="whitespace-nowrap">
            {i > 0 ? " · " : ""}
            {fmtAmount(v, c, locale) ?? "—"}
          </span>
        ))}
      </span>
    );
  }
  return (
    <ul className="space-y-0.5 tabular-nums">
      {entries.map(([c, v]) => (
        <li key={c} className="whitespace-nowrap">
          {fmtAmount(v, c, locale) ?? <NA />}
        </li>
      ))}
    </ul>
  );
}

export function DateV({ value, time = false }: { value: string | null | undefined; time?: boolean }) {
  const { locale } = useI18n();
  const s = fmtDate(value, locale, time);
  return s === null ? <NA /> : <time dateTime={value ?? undefined}>{s}</time>;
}

export function Pct({ value, digits = 1 }: { value: string | number | null | undefined; digits?: number }) {
  const { locale } = useI18n();
  const s = fmtPct(value, locale, digits);
  return s === null ? <NA /> : <span className="tabular-nums">{s}</span>;
}

export function Text({ value }: { value: string | null | undefined }) {
  if (isMissing(value)) return <NA />;
  return <span className="whitespace-pre-line break-anywhere">{value}</span>;
}
