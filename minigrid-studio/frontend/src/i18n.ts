export type Lang = "fr" | "en";

const dict = {
  title: { fr: "Mini-Grid Financial Model Studio", en: "Mini-Grid Financial Model Studio" },
  disclaimer: {
    fr: "Outil d'analyse. Ni certification BAD, Banque mondiale ou CrossBoundary, ni avis juridique ou d'investissement.",
    en: "Analysis tool. Not a certification by AfDB, the World Bank or CrossBoundary, nor legal or investment advice.",
  },
  email: { fr: "E-mail", en: "E-mail" },
  password: { fr: "Mot de passe", en: "Password" },
  login: { fr: "Se connecter", en: "Sign in" },
  logout: { fr: "Se déconnecter", en: "Sign out" },
  projects: { fr: "Projets", en: "Projects" },
  versions: { fr: "Versions de scénario", en: "Scenario versions" },
  run: { fr: "Calculer", en: "Calculate" },
  newVersion: { fr: "Nouvelle version (démo fictive)", en: "New version (fictitious demo)" },
  indicators: { fr: "Indicateurs", en: "Indicators" },
  source: { fr: "Source", en: "Source" },
  derived: { fr: "dérivé (sans équivalent Excel)", en: "derived (no Excel equivalent)" },
  experimental: { fr: "expérimental", en: "experimental" },
  warnings: { fr: "Alertes", en: "Warnings" },
  status_reconciled: { fr: "Moteur rapproché du classeur", en: "Engine reconciled with the workbook" },
  status_variant: { fr: "Variante (écarts au classeur)", en: "Variant (departs from the workbook)" },
  none: { fr: "Aucun", en: "None" },
  error: { fr: "Erreur", en: "Error" },
} as const;

export type Key = keyof typeof dict;

export function t(key: Key, lang: Lang): string {
  return dict[key][lang];
}

export function allKeysTranslated(): boolean {
  return Object.values(dict).every((v) => v.fr.length > 0 && v.en.length > 0);
}

export function formatValue(value: number | null, unit: string, lang: Lang): string {
  if (value === null || Number.isNaN(value)) return "n/a";
  const locale = lang === "fr" ? "fr-FR" : "en-GB";
  if (unit === "%") return new Intl.NumberFormat(locale, { style: "percent", maximumFractionDigits: 2 }).format(value);
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 2 }).format(value);
}
