import { money, num, pct, ratio, years, type Loc } from "./format";

export type MetricKind = "pct" | "lcy" | "usd" | "ratio" | "years" | "num" | "lcy_kwh" | "usd_kwh";

export interface MetricDef {
  key: string;
  en: string;
  fr: string;
  kind: MetricKind;
}

/** KPI cards on the Results tab, in display order. */
export const RESULT_KPIS: MetricDef[] = [
  { key: "project_irr_pre_subsidy", en: "Project IRR before subsidy", fr: "TRI projet avant subvention", kind: "pct" },
  { key: "project_irr_post_subsidy", en: "Project IRR after subsidy", fr: "TRI projet après subvention", kind: "pct" },
  { key: "equity_irr", en: "Equity IRR", fr: "TRI actionnaire", kind: "pct" },
  { key: "project_npv_post_subsidy", en: "Project NPV after subsidy", fr: "VAN projet après subvention", kind: "lcy" },
  { key: "project_npv_pre_subsidy", en: "Project NPV before subsidy", fr: "VAN projet avant subvention", kind: "lcy" },
  { key: "dscr_min", en: "Minimum DSCR", fr: "DSCR minimal", kind: "ratio" },
  { key: "dscr_avg", en: "Average DSCR", fr: "DSCR moyen", kind: "ratio" },
  { key: "llcr_cod", en: "LLCR at COD", fr: "LLCR à la mise en service", kind: "ratio" },
  { key: "payback_years", en: "Payback", fr: "Délai de récupération", kind: "years" },
  { key: "lcoe_per_kwh_sold", en: "LCOE per kWh sold", fr: "LCOE par kWh vendu", kind: "lcy_kwh" },
  { key: "lcoe_per_kwh_sold_usd", en: "LCOE per kWh sold (USD)", fr: "LCOE par kWh vendu (USD)", kind: "usd_kwh" },
  { key: "cost_per_connection", en: "Cost per connection", fr: "Coût par raccordement", kind: "lcy" },
  { key: "cost_per_connection_usd", en: "Cost per connection (USD)", fr: "Coût par raccordement (USD)", kind: "usd" },
  { key: "viability_gap_per_connection", en: "Viability gap per connection", fr: "Déficit de viabilité par raccordement", kind: "lcy" },
  { key: "subsidy_per_connection", en: "Subsidy per connection", fr: "Subvention par raccordement", kind: "lcy" },
  { key: "equity_peak", en: "Peak equity", fr: "Fonds propres maximum", kind: "lcy" },
  { key: "equity_support_total", en: "Equity support", fr: "Soutien en fonds propres", kind: "lcy" },
  { key: "closure_cover", en: "Closure cover", fr: "Couverture de clôture", kind: "ratio" },
  { key: "capital_grant_undisbursed", en: "Capital grant undisbursed", fr: "Subvention d'investissement non décaissée", kind: "lcy" },
  { key: "capex_total_usd", en: "Total capex (USD)", fr: "Investissement total (USD)", kind: "usd" },
  { key: "connections_target", en: "Connections (target)", fr: "Raccordements (cible)", kind: "num" },
];

/** Columns in the run summary (`key`) of a run. */
export const SUMMARY_KPIS: MetricDef[] = [
  { key: "capex_total_usd", en: "Total capex (USD)", fr: "Investissement total (USD)", kind: "usd" },
  { key: "connections_target", en: "Connections (target)", fr: "Raccordements (cible)", kind: "num" },
  { key: "project_irr_post_subsidy", en: "Project IRR after subsidy", fr: "TRI projet après subvention", kind: "pct" },
  { key: "equity_irr", en: "Equity IRR", fr: "TRI actionnaire", kind: "pct" },
  { key: "dscr_min", en: "Minimum DSCR", fr: "DSCR minimal", kind: "ratio" },
  { key: "lcoe_per_kwh_sold_usd", en: "LCOE per kWh sold (USD)", fr: "LCOE par kWh vendu (USD)", kind: "usd_kwh" },
  { key: "viability_gap_per_connection", en: "Viability gap per connection", fr: "Déficit de viabilité par raccordement", kind: "lcy" },
];

export function fmtMetric(kind: MetricKind, v: unknown, ccy: string, l: Loc): string {
  switch (kind) {
    case "pct":
      return pct(v, l);
    case "lcy":
      return money(v, ccy, l);
    case "usd":
      return money(v, "USD", l);
    case "lcy_kwh":
      return `${money(v, ccy, l, 2)}/kWh`;
    case "usd_kwh":
      return `${money(v, "USD", l, 3)}/kWh`;
    case "ratio":
      return ratio(v, l);
    case "years":
      return years(v, l);
    default:
      return num(v, l);
  }
}

export const label = (m: MetricDef, l: Loc) => (l === "fr" ? m.fr : m.en);

/** Sources and uses keys, labelled. */
export const SOURCES = [
  ["equity", "Equity", "Fonds propres"],
  ["debt", "Debt", "Dette"],
  ["grants_in_construction", "Grants during construction", "Subventions pendant la construction"],
  ["sources_total", "Total sources", "Total des ressources"],
] as const;

export const USES = [
  ["capex", "Capex", "Investissements"],
  ["interest_during_construction", "Interest during construction", "Intérêts intercalaires"],
  ["financing_fees", "Financing fees", "Frais de financement"],
  ["tax_during_construction", "Tax during construction", "Impôts pendant la construction"],
  ["dsra_initial", "Initial DSRA funding", "Dotation initiale du DSRA"],
  ["uses_total", "Total uses", "Total des emplois"],
  ["cash_at_cod", "Plus cash held at COD (sources = uses + cash)", "Plus trésorerie détenue à la mise en service (ressources = emplois + trésorerie)"],
] as const;

export const ANNUAL_COLS = [
  ["connections_end", "Connections (end of year)", "Raccordements (fin d'année)", "num"],
  ["energy_sold_kwh", "Energy sold (kWh)", "Énergie vendue (kWh)", "num"],
  ["revenue", "Revenue", "Chiffre d'affaires", "lcy"],
  ["ebitda", "EBITDA", "EBITDA", "lcy"],
  ["cfads", "CFADS", "CFADS", "lcy"],
  ["debt_service", "Debt service", "Service de la dette", "lcy"],
  ["dscr", "DSCR", "DSCR", "ratio"],
  ["net_income", "Net income", "Résultat net", "lcy"],
] as const;
