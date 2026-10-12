"use client";

import { useEffect, useId, useMemo, useState, type ReactNode } from "react";
import { FlaskConical, Plus, Save, Trash2 } from "lucide-react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select, Textarea } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, ApiError, orgPath } from "@/lib/api";
import type { Loc } from "@/lib/format";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Json, Project, ProjectInputs } from "@/lib/types";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------- field definitions

type Kind = "text" | "int" | "num" | "pct" | "date" | "bool" | "select";
interface Def {
  key: string;
  label: [string, string]; // en, fr (units in the label)
  kind: Kind;
  options?: string[];
  hint?: [string, string];
}

const d = (key: string, en: string, fr: string, kind: Kind, options?: string[]): Def => ({ key, label: [en, fr], kind, options });

const GENERAL: Def[] = [
  d("project_name", "Project name", "Nom du projet", "text"),
  d("country", "Country", "Pays", "text"),
  d("currency", "Local currency code (3 letters)", "Code de la monnaie locale (3 lettres)", "text"),
  d("financial_close", "Financial close (date)", "Bouclage financier (date)", "date"),
  d("construction_quarters", "Construction period (quarters)", "Durée de construction (trimestres)", "int"),
  d("operating_years", "Operating period (years)", "Durée d'exploitation (années)", "int"),
  d("residual_value_pct_nbv", "Residual value (% of net book value)", "Valeur résiduelle (% de la valeur nette comptable)", "pct"),
];

const TECHNICAL: Def[] = [
  d("pv_kwp", "PV capacity (kWp)", "Puissance PV (kWc)", "num"),
  d("battery_kwh", "Battery capacity (kWh)", "Capacité batterie (kWh)", "num"),
  d("diesel_kw", "Diesel genset (kW)", "Groupe diesel (kW)", "num"),
  d("network_km", "Distribution network (km)", "Réseau de distribution (km)", "num"),
  d("deliverable_energy_kwh_pa", "Deliverable energy (kWh per year)", "Énergie livrable (kWh par an)", "num"),
  d("technical_loss", "Technical losses (%)", "Pertes techniques (%)", "pct"),
  d("commercial_loss", "Commercial losses (%)", "Pertes commerciales (%)", "pct"),
  d("diesel_share", "Diesel share of generation (%)", "Part du diesel dans la production (%)", "pct"),
  d("diesel_cost_per_kwh", "Diesel fuel cost (LCY per kWh)", "Coût du carburant (LCY par kWh)", "num"),
  d("diesel_kgco2_per_kwh", "Diesel emission factor (kgCO2 per kWh)", "Facteur d'émission diesel (kgCO2 par kWh)", "num"),
  d("battery_life_years", "Battery life (years)", "Durée de vie batterie (années)", "num"),
  d("battery_replacement_usd_per_kwh", "Battery replacement cost (USD per kWh)", "Coût de remplacement batterie (USD par kWh)", "num"),
  d("battery_cost_decline_pa", "Battery cost decline (% per year)", "Baisse du coût des batteries (% par an)", "pct"),
];

const CUSTOMER_COLS: Def[] = [
  d("name", "Name", "Nom", "text"),
  d("category", "Category", "Catégorie", "select", ["household", "commercial", "industrial", "agricultural", "institutional", "anchor"]),
  d("connections_target", "Connections (target)", "Raccordements (cible)", "int"),
  d("start_quarter", "Start (operating quarter)", "Début (trimestre d'exploitation)", "int"),
  d("ramp_quarters", "Ramp (quarters)", "Montée en charge (trimestres)", "int"),
  d("kwh_per_connection_month", "Consumption (kWh per month)", "Consommation (kWh par mois)", "num"),
  d("demand_growth_pa", "Demand growth (% per year)", "Croissance de la demande (% par an)", "pct"),
  d("tariff_per_kwh", "Tariff (LCY per kWh)", "Tarif (LCY par kWh)", "num"),
  d("fixed_charge_month", "Fixed charge (LCY per month)", "Abonnement (LCY par mois)", "num"),
  d("connection_fee", "Connection fee (LCY)", "Frais de raccordement (LCY)", "num"),
  d("monthly_income", "Monthly income (LCY, optional)", "Revenu mensuel (LCY, facultatif)", "num"),
];

const CAPEX_COLS: Def[] = [
  d("name", "Item", "Poste", "text"),
  d("category", "Category", "Catégorie", "select", ["generation", "storage", "network", "metering", "development", "other"]),
  d("amount", "Amount", "Montant", "num"),
  d("currency", "Currency", "Monnaie", "select", ["LCY", "USD"]),
  d("asset_life_years", "Asset life (years)", "Durée de vie (années)", "num"),
  d("replace_at_end_of_life", "Replace at end of life (not storage)", "Remplacer en fin de vie (hors stockage)", "bool"),
  d("replacement_cost_share", "Replacement cost (% of amount)", "Coût de remplacement (% du montant)", "pct"),
  d("real_price_change_pa", "Real price change (% per year)", "Variation réelle du prix (% par an)", "pct"),
];

const OPEX: Def[] = [
  d("fixed_pa", "Fixed opex (LCY per year)", "Charges fixes (LCY par an)", "num"),
  d("per_connection_pa", "Opex per connection (LCY per year)", "Charges par raccordement (LCY par an)", "num"),
  d("insurance_pct_capex", "Insurance (% of capex per year)", "Assurance (% de l'investissement par an)", "pct"),
  d("collection_efficiency", "Collection efficiency (%)", "Taux de recouvrement (%)", "pct"),
];

const MACRO: Def[] = [
  d("inflation_pa", "Local inflation (% per year)", "Inflation locale (% par an)", "pct"),
  d("tariff_indexation", "Tariff indexation (% of inflation)", "Indexation tarifaire (% de l'inflation)", "pct"),
  d("fx_lcy_per_usd", "Exchange rate (LCY per USD)", "Taux de change (LCY par USD)", "num"),
  d("fx_depreciation_pa", "LCY depreciation against USD (% per year)", "Dépréciation de la LCY face à l'USD (% par an)", "pct"),
  d("tax_rate", "Corporate tax rate (%)", "Taux d'impôt sur les sociétés (%)", "pct"),
  d("grant_income_taxable", "Grant income taxable", "Subvention imposable", "bool"),
  d("discount_rate_pa", "Discount rate (% per year, nominal)", "Taux d'actualisation (% par an, nominal)", "pct"),
  d("equity_target_irr_pa", "Target equity IRR (%, optional)", "TRI actionnaire cible (%, facultatif)", "pct"),
];

const FINANCING: Def[] = [
  d("debt_basis", "Debt sizing basis", "Base de dimensionnement de la dette", "select", ["capex_net_of_grant", "gross_capex"]),
  d("dsra_quarters", "DSRA (quarters of debt service)", "DSRA (trimestres de service de la dette)", "int"),
  d("maintenance_reserve", "Maintenance reserve for battery replacement", "Réserve de maintenance pour le remplacement des batteries", "bool"),
  d("lockup_dscr", "Distribution lock-up DSCR (x)", "DSCR de blocage des distributions (x)", "num"),
  d("min_cash", "Minimum cash (LCY)", "Trésorerie minimale (LCY)", "num"),
];

const TRANCHE_COLS: Def[] = [
  d("name", "Name", "Nom", "text"),
  d("kind", "Kind", "Type", "select", ["senior", "concessional"]),
  d("currency", "Currency", "Monnaie", "select", ["LCY", "USD"]),
  d("share_of_capex", "Share of capex (%)", "Part de l'investissement (%)", "pct"),
  d("rate_pa", "Interest rate (% per year)", "Taux d'intérêt (% par an)", "pct"),
  d("tenor_years", "Tenor (years)", "Durée (années)", "num"),
  d("grace_quarters", "Grace (quarters)", "Différé (trimestres)", "int"),
  d("upfront_fee", "Upfront fee (%)", "Commission initiale (%)", "pct"),
  d("amortisation", "Amortisation", "Amortissement", "select", ["annuity", "straight_line"]),
];

const SUBSIDIES: Def[] = [
  d("capital_grant", "Capital grant (LCY)", "Subvention d'investissement (LCY)", "num"),
  d("rbf_per_connection", "Results based payment (LCY per connection)", "Paiement aux résultats (LCY par raccordement)", "num"),
  d("rbf_verification_lag_quarters", "RBF verification lag (quarters)", "Délai de vérification RBF (trimestres)", "int"),
  d("rbf_cap", "RBF programme cap (LCY, optional)", "Plafond du programme RBF (LCY, facultatif)", "num"),
  d("tariff_support_per_kwh", "Tariff support (LCY per kWh billed)", "Soutien tarifaire (LCY par kWh facturé)", "num"),
  d("tariff_support_years", "Tariff support duration (years)", "Durée du soutien tarifaire (années)", "num"),
];

const MILESTONE_COLS: Def[] = [d("quarter", "Model quarter (0 = financial close)", "Trimestre du modèle (0 = bouclage)", "int"), d("share", "Share of grant (%)", "Part de la subvention (%)", "pct")];

const GRID: Def[] = [
  d("enabled", "Grid arrival modelled", "Arrivée du réseau modélisée", "bool"),
  d("operating_year", "Operating year of grid arrival", "Année d'exploitation de l'arrivée du réseau", "int"),
  d("treatment", "Treatment", "Traitement", "select", ["interconnect", "asset_transfer", "stranded"]),
  d("compensation_pct_nbv", "Compensation (% of net book value)", "Indemnisation (% de la valeur nette comptable)", "pct"),
  d("tariff_factor_after", "Tariff multiplier after interconnection (x)", "Multiplicateur tarifaire après interconnexion (x)", "num"),
  d("demand_factor_after", "Demand multiplier after interconnection (x)", "Multiplicateur de demande après interconnexion (x)", "num"),
  d("regulatory_source", "Regulatory source (citation)", "Source réglementaire (référence)", "text"),
];

const REVIEW: Def[] = [d("reviewed_by", "Reviewed by", "Revu par", "text"), d("reviewed_on", "Review date", "Date de la revue", "date"), d("note", "Note", "Note", "text")];

const ROW_DEFAULTS: Record<string, Record<string, Json>> = {
  customers: { name: "", category: "household", connections_target: 0, start_quarter: 0, ramp_quarters: 4, kwh_per_connection_month: 0, demand_growth_pa: 0, tariff_per_kwh: 0, fixed_charge_month: 0, connection_fee: 0, monthly_income: null },
  capex: { name: "", category: "generation", amount: 0, currency: "LCY", asset_life_years: 20, replace_at_end_of_life: false, replacement_cost_share: 1, real_price_change_pa: 0 },
  "financing.debt": { name: "", kind: "senior", currency: "LCY", share_of_capex: 0, rate_pa: 0, tenor_years: 10, grace_quarters: 0, upfront_fee: 0, amortisation: "annuity" },
  "subsidies.grant_milestones": { quarter: 0, share: 1 },
};

// ---------------------------------------------------------------- tree helpers

type Obj = { [k: string]: Json };
const isObj = (v: unknown): v is Obj => !!v && typeof v === "object" && !Array.isArray(v);

function getAt(root: Json, path: (string | number)[]): Json | undefined {
  let cur: Json | undefined = root;
  for (const k of path) {
    if (cur === null || cur === undefined || typeof cur !== "object") return undefined;
    cur = (cur as Record<string | number, Json>)[k as never];
  }
  return cur;
}

function setAt(root: Obj, path: (string | number)[], value: Json | undefined): Obj {
  const out = structuredClone(root);
  let cur: Record<string | number, Json> = out;
  for (let i = 0; i < path.length - 1; i++) {
    const k = path[i];
    const next = cur[k as never];
    if (next === null || next === undefined || typeof next !== "object") cur[k as never] = (typeof path[i + 1] === "number" ? [] : {}) as Json;
    cur = cur[k as never] as unknown as Record<string | number, Json>;
  }
  const last = path[path.length - 1];
  if (value === undefined) {
    if (Array.isArray(cur)) cur[last as number] = null;
    else delete cur[last as never];
  } else cur[last as never] = value;
  return out;
}

function emptyInputs(p: Project): Obj {
  return {
    project_name: p.name,
    country: p.country,
    currency: "",
    construction_quarters: 2,
    operating_years: 20,
    technical: {},
    customers: [],
    capex: [],
    opex: {},
    macro: {},
    financing: { debt: [], debt_basis: "capex_net_of_grant", dsra_quarters: 2, maintenance_reserve: true, lockup_dscr: 1.2, min_cash: 0 },
    subsidies: { capital_grant: 0, grant_milestones: [], rbf_per_connection: 0, rbf_verification_lag_quarters: 2, tariff_support_per_kwh: 0, tariff_support_years: 0 },
    grid_arrival: { enabled: false, operating_year: 10, treatment: "interconnect", compensation_pct_nbv: 0, tariff_factor_after: 1, demand_factor_after: 1 },
    provenance: "user_estimate",
    review: null,
  };
}

// ---------------------------------------------------------------- controls

/** Number input that keeps the typed text while editing; percentages are shown x100 and stored as fractions. */
export function NumberBox({ id, value, onChange, pct, int, invalid, describedBy, disabled, compact }: { id?: string; value: Json | undefined; onChange: (v: number | undefined) => void; pct?: boolean; int?: boolean; invalid?: boolean; describedBy?: string; disabled?: boolean; compact?: boolean }) {
  const shown = typeof value === "number" ? (pct ? +(value * 100).toPrecision(12) : value) : null;
  const [text, setText] = useState(shown === null ? "" : String(shown));
  useEffect(() => {
    const parsed = text.trim() === "" ? null : Number(text.replace(",", "."));
    if (parsed !== shown) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- sync from external value (e.g. demo load)
      setText(shown === null ? "" : String(shown));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [shown]);
  return (
    <div className="relative">
      <Input
        id={id}
        inputMode={int ? "numeric" : "decimal"}
        value={text}
        disabled={disabled}
        aria-invalid={invalid}
        aria-describedby={describedBy}
        className={cn("tabular text-right", pct && "pr-7", compact && "h-8 min-w-24 px-2 text-xs")}
        onChange={(e) => {
          const s = e.target.value;
          setText(s);
          if (s.trim() === "") return onChange(undefined);
          const n = Number(s.replace(",", "."));
          if (Number.isFinite(n)) onChange(pct ? n / 100 : int ? Math.trunc(n) : n);
        }}
      />
      {pct ? <span className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-xs text-subtle-foreground">%</span> : null}
    </div>
  );
}

function Control({ def, value, onChange, id, invalid, describedBy, disabled, compact, locale }: { def: Def; value: Json | undefined; onChange: (v: Json | undefined) => void; id?: string; invalid?: boolean; describedBy?: string; disabled?: boolean; compact?: boolean; locale: Loc }) {
  const cls = compact ? "h-8 px-2 text-xs" : undefined;
  switch (def.kind) {
    case "bool":
      return (
        <input id={id} type="checkbox" className="size-4 accent-emerald-600" checked={value === true} disabled={disabled} aria-describedby={describedBy} onChange={(e) => onChange(e.target.checked)} />
      );
    case "select":
      return (
        <Select id={id} value={typeof value === "string" ? value : ""} disabled={disabled} aria-invalid={invalid} aria-describedby={describedBy} className={cls} onChange={(e) => onChange(e.target.value)}>
          {value === undefined || value === null ? <option value="">–</option> : null}
          {(def.options ?? []).map((o) => (
            <option key={o} value={o}>
              {o.replace(/_/g, " ")}
            </option>
          ))}
        </Select>
      );
    case "date":
      return <Input id={id} type="date" value={typeof value === "string" ? value : ""} disabled={disabled} aria-invalid={invalid} aria-describedby={describedBy} className={cls} onChange={(e) => onChange(e.target.value || undefined)} />;
    case "text":
      return (
        <Input
          id={id}
          value={typeof value === "string" ? value : ""}
          disabled={disabled}
          aria-invalid={invalid}
          aria-describedby={describedBy}
          className={cn(cls, compact && "min-w-36")}
          lang={locale}
          onChange={(e) => onChange(e.target.value === "" && def.key !== "name" && def.key !== "project_name" ? undefined : e.target.value)}
        />
      );
    default:
      return <NumberBox id={id} value={value} onChange={onChange} pct={def.kind === "pct"} int={def.kind === "int"} invalid={invalid} describedBy={describedBy} disabled={disabled} compact={compact} />;
  }
}

function ScalarField({ def, base, state, set, errors, disabled }: { def: Def; base: (string | number)[]; state: Obj; set: (p: (string | number)[], v: Json | undefined) => void; errors: Record<string, string>; disabled: boolean }) {
  const { locale } = useI18n();
  const id = useId();
  const path = [...base, def.key];
  const err = errors[path.join(".")];
  const errId = `${id}-err`;
  const lbl = def.label[locale === "fr" ? 1 : 0];
  if (def.kind === "bool") {
    return (
      <div className="flex flex-col gap-1 self-end pb-2">
        <label className="flex items-center gap-2 text-sm">
          <Control def={def} value={getAt(state, path)} onChange={(v) => set(path, v)} id={id} disabled={disabled} locale={locale} />
          <span>{lbl}</span>
        </label>
        {err ? <p className="text-xs text-danger-700">{err}</p> : null}
      </div>
    );
  }
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor={id}>{lbl}</Label>
      <Control def={def} value={getAt(state, path)} onChange={(v) => set(path, v)} id={id} invalid={!!err} describedBy={err ? errId : undefined} disabled={disabled} locale={locale} />
      {err ? (
        <p id={errId} className="text-xs text-danger-700">
          {err}
        </p>
      ) : null}
    </div>
  );
}

function Section({ title, description, children, id }: { title: string; description?: string; children: ReactNode; id: string }) {
  return (
    <Card id={id}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description ? <CardDescription>{description}</CardDescription> : null}
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

function Grid({ defs, base, ...rest }: { defs: Def[]; base: (string | number)[]; state: Obj; set: (p: (string | number)[], v: Json | undefined) => void; errors: Record<string, string>; disabled: boolean }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {defs.map((df) => (
        <ScalarField key={df.key} def={df} base={base} {...rest} />
      ))}
    </div>
  );
}

function RowsTable({ path, cols, state, set, errors, disabled, testId }: { path: string; cols: Def[]; state: Obj; set: (p: (string | number)[], v: Json | undefined) => void; errors: Record<string, string>; disabled: boolean; testId?: string }) {
  const { t, locale } = useI18n();
  const base = path.split(".");
  const rows = (getAt(state, base) as Json[] | undefined) ?? [];
  const arrErr = errors[path];
  return (
    <div className="flex flex-col gap-2" data-testid={testId}>
      {rows.length === 0 ? <p className="text-sm text-muted-foreground">{t("inputs.noRows")}</p> : null}
      {rows.length > 0 ? (
        <div className="overflow-x-auto rounded-md border border-border">
          <table className="w-full border-collapse text-xs">
            <thead className="bg-surface-muted">
              <tr>
                {cols.map((c) => (
                  <th key={c.key} scope="col" className="px-2 py-2 text-left align-bottom font-medium text-muted-foreground">
                    {c.label[locale === "fr" ? 1 : 0]}
                  </th>
                ))}
                <th className="w-10 px-2 py-2">
                  <span className="sr-only">{t("common.actions")}</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((_, i) => (
                <tr key={i} className="border-t border-border">
                  {cols.map((c) => {
                    const p = [...base, i, c.key];
                    const err = errors[p.join(".")];
                    return (
                      <td key={c.key} className="px-1.5 py-1.5 align-top">
                        <Control def={c} value={getAt(state, p)} onChange={(v) => set(p, v === undefined && c.key === "monthly_income" ? null : v)} invalid={!!err} disabled={disabled} compact locale={locale} />
                        {err ? <p className="mt-0.5 max-w-40 text-[11px] text-danger-700">{err}</p> : null}
                      </td>
                    );
                  })}
                  <td className="px-1.5 py-1.5 align-top">
                    <Button
                      type="button"
                      size="icon"
                      variant="ghost"
                      className="size-8"
                      disabled={disabled}
                      aria-label={`${t("common.remove")} ${i + 1}`}
                      onClick={() => {
                        const next = rows.filter((__, j) => j !== i);
                        set(base, next);
                      }}
                    >
                      <Trash2 aria-hidden />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
      {arrErr ? <p className="text-xs text-danger-700">{arrErr}</p> : null}
      <div>
        <Button type="button" size="sm" variant="outline" disabled={disabled} onClick={() => set(base, [...rows, structuredClone(ROW_DEFAULTS[path]) as Json])}>
          <Plus aria-hidden /> {t("inputs.addRow")}
        </Button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------- tab

export function InputsTab({ project, onSaved }: { project: Project; onSaved: () => void }) {
  const { org, canEdit } = useSession();
  const { t, locale } = useI18n();
  const [state, setState] = useState<Obj>(() => (isObj(project.inputs) ? (structuredClone(project.inputs) as Obj) : emptyInputs(project)));
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [msg, setMsg] = useState<{ kind: "success" | "danger" | "warning"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [dirty, setDirty] = useState(false);
  const disabled = !canEdit;

  const set = (p: (string | number)[], v: Json | undefined) => {
    setState((s) => setAt(s, p, v));
    setDirty(true);
  };

  async function loadDemo() {
    try {
      const r = await api<{ label: string; inputs: ProjectInputs }>("/api/engine/demo-inputs");
      setState(structuredClone(r.inputs) as Obj);
      setErrors({});
      setDirty(true);
      setMsg({ kind: "warning", text: `${r.label}. ${t("inputs.demoLoaded")}` });
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    }
  }

  async function save() {
    if (!org) return;
    setBusy(true);
    setMsg(null);
    setErrors({});
    try {
      const r = await api<{ inputs_version: number }>(orgPath(org.id, `/projects/${project.id}/inputs`), { method: "PUT", body: state });
      setMsg({ kind: "success", text: t("inputs.saveOk", { v: r.inputs_version }) });
      setDirty(false);
      onSaved();
    } catch (err) {
      if (err instanceof ApiError && err.status === 422) {
        setErrors(err.fieldErrors());
        setMsg({ kind: "danger", text: t("inputs.errors") });
      } else {
        setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
      }
    } finally {
      setBusy(false);
    }
  }

  const errorList = useMemo(() => Object.entries(errors), [errors]);
  const reviewOn = isObj(state.review);
  const common = { state, set, errors, disabled };
  const sec = (k: DictKey) => t(k);

  return (
    <div className="flex flex-col gap-5">
      <div className="sticky top-[57px] z-20 -mx-1 flex flex-col gap-3 rounded-lg border border-border bg-surface/95 p-3 backdrop-blur lg:top-[100px]">
        <div className="flex flex-wrap items-center gap-2">
          <Button type="button" onClick={save} disabled={disabled || busy} data-testid="save-inputs">
            <Save aria-hidden /> {busy ? t("common.saving") : t("common.save")}
          </Button>
          <Button type="button" variant="gold" onClick={loadDemo} disabled={disabled} data-testid="load-demo-inputs">
            <FlaskConical aria-hidden /> {t("inputs.loadDemo")}
          </Button>
          {dirty ? <span className="text-xs text-gold-700">•</span> : null}
          <span className="text-xs text-subtle-foreground">{t("inputs.pctNote")}</span>
        </div>
        <p className="text-xs text-gold-700">{t("inputs.demoWarning")}</p>
        {msg ? (
          <Alert variant={msg.kind} data-testid="inputs-message">
            {msg.text}
          </Alert>
        ) : null}
        {errorList.length ? (
          <ul className="max-h-32 overflow-y-auto text-xs text-danger-700">
            {errorList.map(([k, v]) => (
              <li key={k}>
                <span className="font-mono">{k || "inputs"}</span>: {v}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
      {!project.inputs ? <Alert variant="info">{t("inputs.none")}</Alert> : null}
      {!canEdit ? <Alert variant="warning">{t("common.notAllowed")}</Alert> : null}

      <Section id="sec-general" title={sec("inputs.sec.general")}>
        <Grid defs={GENERAL} base={[]} {...common} />
      </Section>
      <Section id="sec-technical" title={sec("inputs.sec.technical")}>
        <Grid defs={TECHNICAL} base={["technical"]} {...common} />
      </Section>
      <Section id="sec-customers" title={sec("inputs.sec.customers")}>
        <RowsTable path="customers" cols={CUSTOMER_COLS} {...common} testId="customers-table" />
      </Section>
      <Section id="sec-capex" title={sec("inputs.sec.capex")}>
        <RowsTable path="capex" cols={CAPEX_COLS} {...common} testId="capex-table" />
      </Section>
      <Section id="sec-opex" title={sec("inputs.sec.opex")}>
        <Grid defs={OPEX} base={["opex"]} {...common} />
      </Section>
      <Section id="sec-macro" title={sec("inputs.sec.macro")}>
        <Grid defs={MACRO} base={["macro"]} {...common} />
      </Section>
      <Section id="sec-financing" title={sec("inputs.sec.financing")}>
        <div className="flex flex-col gap-5">
          <Grid defs={FINANCING} base={["financing"]} {...common} />
          <div>
            <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("inputs.sec.tranches")}</h3>
            <RowsTable path="financing.debt" cols={TRANCHE_COLS} {...common} />
          </div>
        </div>
      </Section>
      <Section id="sec-subsidies" title={sec("inputs.sec.subsidies")}>
        <div className="flex flex-col gap-5">
          <Grid defs={SUBSIDIES} base={["subsidies"]} {...common} />
          <div>
            <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("inputs.sec.milestones")}</h3>
            <RowsTable path="subsidies.grant_milestones" cols={MILESTONE_COLS} {...common} />
          </div>
        </div>
      </Section>
      <Section id="sec-grid" title={sec("inputs.sec.grid")}>
        <Grid defs={GRID} base={["grid_arrival"]} {...common} />
      </Section>
      <Section id="sec-provenance" title={sec("inputs.sec.provenance")}>
        <Grid defs={[d("provenance", "Provenance of the inputs", "Provenance des hypothèses", "select", ["sourced", "user_estimate", "illustrative"])]} base={[]} {...common} />
      </Section>
      <Section id="sec-review" title={sec("inputs.sec.review")} description={t("inputs.reviewNote")}>
        <label className="mb-4 flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="size-4 accent-emerald-600"
            checked={reviewOn}
            disabled={disabled}
            onChange={(e) => set(["review"], e.target.checked ? { reviewed_by: "", reviewed_on: new Date().toISOString().slice(0, 10), note: "" } : null)}
          />
          {t("inputs.reviewEnabled")}
        </label>
        {reviewOn ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {REVIEW.map((df) =>
              df.key === "note" ? (
                <div key="note" className="flex flex-col gap-1 sm:col-span-2 lg:col-span-3">
                  <Label htmlFor="review-note">{df.label[locale === "fr" ? 1 : 0]}</Label>
                  <Textarea id="review-note" value={typeof getAt(state, ["review", "note"]) === "string" ? (getAt(state, ["review", "note"]) as string) : ""} disabled={disabled} onChange={(e) => set(["review", "note"], e.target.value)} />
                </div>
              ) : (
                <ScalarField key={df.key} def={df} base={["review"]} {...common} />
              ),
            )}
          </div>
        ) : null}
      </Section>
    </div>
  );
}
