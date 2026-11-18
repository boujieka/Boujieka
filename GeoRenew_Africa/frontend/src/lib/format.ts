/** Mise en forme des nombres et étiquettes de nature des valeurs (CLAUDE.md §2, PROMPT §V). */
import type { Nature } from "../types";

const nf = (digits: number) =>
  new Intl.NumberFormat("fr-FR", { minimumFractionDigits: digits, maximumFractionDigits: digits });

export function formatHa(m2: number | null | undefined, digits = 2): string {
  if (m2 === null || m2 === undefined || Number.isNaN(m2)) return "—";
  return `${nf(digits).format(m2 / 10_000)} ha`;
}

export function formatNumber(v: number | null | undefined, digits = 2, unit = ""): string {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  return `${nf(digits).format(v)}${unit ? ` ${unit}` : ""}`;
}

export const NATURE_LABELS: Record<Nature, string> = {
  renseigne: "Renseigné",
  calcule: "Calculé",
  hypothetique: "Hypothétique",
  inconnu: "Inconnu",
};

export function natureLabel(n: string): string {
  return NATURE_LABELS[n as Nature] ?? n;
}

export function shortHash(h: string | null | undefined, n = 12): string {
  return h ? h.slice(0, n) : "—";
}
