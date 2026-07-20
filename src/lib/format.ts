/** Helpers de formatage (fr-FR). */

export const fmtInt = (x: number | null | undefined): string =>
  x == null ? "—" : Math.round(x).toLocaleString("fr-FR");

export const fmtNum = (x: number | null | undefined, digits = 1): string =>
  x == null ? "—" : x.toLocaleString("fr-FR", { maximumFractionDigits: digits });

export const fmtPct = (x: number | null | undefined, digits = 1): string =>
  x == null ? "—" : `${(x * 100).toFixed(digits)} %`;

export const fmtMoney = (x: number | null | undefined, currency = "USD"): string =>
  x == null ? "—" : `${Math.round(x).toLocaleString("fr-FR")} ${currency}`;

export const fmtKwhToMwh = (kwh: number | null | undefined): string =>
  kwh == null ? "—" : `${(kwh / 1000).toLocaleString("fr-FR", { maximumFractionDigits: 0 })} MWh`;

export const STAGE_LABELS: Record<string, string> = {
  identifiee: "Identifiée",
  qualifiee: "Qualifiée",
  term_sheet: "Term sheet",
  mandat: "Mandat",
  bouclage_financier: "Bouclage financier",
  realisee: "Réalisée",
  abandonnee: "Abandonnée",
};

export const CRITICALITY_LABELS: Record<string, string> = {
  faible: "Faible",
  moyenne: "Moyenne",
  elevee: "Élevée",
  critique: "Critique",
};

export const TECH_LABELS: Record<string, string> = {
  solaire: "Solaire",
  stockage: "Stockage",
  hybride: "Hybride",
  groupe_backup: "Groupe d'appoint",
};

export const FINANCING_LABELS: Record<string, string> = {
  equity: "Fonds propres",
  dette: "Dette",
  mixte: "Mixte",
  aucune: "Aucune",
};
