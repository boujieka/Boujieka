import type { FieldStatus, InstrumentType } from "./types";

export const FIELD_STATUS_LABEL: Record<FieldStatus, string> = {
  not_disclosed: "Not disclosed",
  not_available: "Not available",
  pending: "Pending",
};

/** Label for an empty field. A null without a recorded reason is "Not available". */
export function emptyLabel(status: FieldStatus | undefined): string {
  return FIELD_STATUS_LABEL[status ?? "not_available"];
}

/** Large amounts in compact form with the currency always shown: "23.45bn XAF". */
export function formatAmount(value: string | null, currency: string): string | null {
  if (value === null) return null;
  const n = Number(value);
  const abs = Math.abs(n);
  const [div, unit] =
    abs >= 1e12 ? [1e12, "tn"] : abs >= 1e9 ? [1e9, "bn"] : abs >= 1e6 ? [1e6, "m"] : [1, ""];
  return `${(n / div).toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: div > 1 ? 2 : 0 })}${unit} ${currency}`;
}

export function formatPct(value: string | null, digits = 3): string | null {
  if (value === null) return null;
  return `${Number(value).toFixed(digits)}%`;
}

export function formatRatio(value: string | null, digits = 2): string | null {
  if (value === null) return null;
  return `${Number(value).toFixed(digits)}×`;
}

export function formatShare(value: string | null): string | null {
  if (value === null) return null;
  return `${(Number(value) * 100).toFixed(1)}%`;
}

export function formatBps(value: string | null): string | null {
  if (value === null) return null;
  const n = Number(value);
  return `${n > 0 ? "+" : ""}${n.toFixed(1)} bp`;
}

export function formatDate(value: string | null): string | null {
  if (!value) return null;
  // Dates are ISO calendar dates; render without timezone shifting.
  const [y, m, d] = value.slice(0, 10).split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function formatTenor(days: number | null): string | null {
  if (days === null) return null;
  if (days < 365) {
    const weeks = Math.round(days / 7);
    return days % 7 === 0 ? `${weeks}W` : `${days}D`;
  }
  const years = days / 365;
  return Number.isInteger(years) ? `${years}Y` : `${years.toFixed(1)}Y`;
}

export const INSTRUMENT_LABEL: Record<InstrumentType, string> = {
  treasury_bill: "T-Bill",
  treasury_bond: "T-Bond",
  eurobond: "Eurobond",
  infrastructure_bond: "Infra bond",
  sukuk: "Sukuk",
  regional_bond: "Regional bond",
  other: "Other",
};

export function titleCase(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function addDays(iso: string, days: number): string {
  const d = new Date(`${iso}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

export function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}
