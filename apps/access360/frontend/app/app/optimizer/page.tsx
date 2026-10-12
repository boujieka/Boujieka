"use client";

import { useEffect, useId, useState } from "react";
import { Award, CheckCircle2, Loader2, Star, XCircle } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { ChartFrame, OptionsScatter } from "@/components/charts";
import { ErrorBox, PageHeader } from "@/components/page";
import { NumberBox } from "@/components/project/inputs-form";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, ApiError } from "@/lib/api";
import { num, pct } from "@/lib/format";
import { useI18n } from "@/lib/i18n";
import type { CompareResult, Json } from "@/lib/types";
import { cn } from "@/lib/utils";

type Obj = Record<string, Json>;
type L = [string, string, ("pct" | "int" | "num" | "text" | "bool" | "tri")?];

const SETTLEMENT: Record<string, L> = {
  name: ["Settlement name", "Nom de la localité", "text"],
  households: ["Households", "Ménages", "int"],
  businesses: ["Businesses", "Commerces", "int"],
  productive_users: ["Productive users (mills, pumps, cold rooms)", "Usages productifs (moulins, pompes, chambres froides)", "int"],
  institutions: ["Institutions", "Institutions", "int"],
  anchor_present: ["Anchor customer present", "Client d'ancrage présent", "bool"],
  anchor_kwh_month: ["Anchor demand (kWh per month)", "Demande du client d'ancrage (kWh par mois)"],
  household_kwh_month: ["Household demand (kWh per month)", "Demande par ménage (kWh par mois)"],
  business_kwh_month: ["Business demand (kWh per month)", "Demande par commerce (kWh par mois)"],
  productive_kwh_month: ["Productive user demand (kWh per month)", "Demande par usage productif (kWh par mois)"],
  institution_kwh_month: ["Institution demand (kWh per month)", "Demande par institution (kWh par mois)"],
  household_income_month: ["Household income (LCY per month)", "Revenu des ménages (LCY par mois)"],
  distance_to_grid_km: ["Distance to grid (km, empty = unknown)", "Distance au réseau (km, vide = inconnue)"],
  grid_has_capacity: ["Grid has spare capacity", "Le réseau a de la capacité disponible", "tri"],
  grid_supply_hours: ["Grid supply (hours per day)", "Fourniture du réseau (heures par jour)"],
  dispersed_household_share: ["Dispersed households (%)", "Ménages dispersés (%)", "pct"],
};

const COSTS: Record<string, L> = {
  discount_rate_pa: ["Discount rate (% per year)", "Taux d'actualisation (% par an)", "pct"],
  horizon_years: ["Horizon (years)", "Horizon (années)", "int"],
  grid_densification_max_km: ["Densification range (km)", "Portée de la densification (km)"],
  grid_extension_max_km: ["Extension range (km)", "Portée de l'extension (km)"],
  mv_line_per_km: ["MV line (LCY per km)", "Ligne MT (LCY par km)"],
  lv_network_per_connection: ["LV network (LCY per connection)", "Réseau BT (LCY par raccordement)"],
  grid_connection_per_connection: ["Grid connection (LCY per connection)", "Raccordement réseau (LCY par raccordement)"],
  grid_cost_of_supply_per_kwh: ["Grid cost of supply (LCY per kWh)", "Coût de fourniture réseau (LCY par kWh)"],
  grid_om_pct_capex: ["Grid O&M (% of capex per year)", "Exploitation réseau (% de l'investissement par an)", "pct"],
  grid_kgco2_per_kwh: ["Grid emission factor (kgCO2 per kWh)", "Facteur d'émission réseau (kgCO2 par kWh)"],
  pv_per_kwp: ["PV (LCY per kWp)", "PV (LCY par kWc)"],
  battery_per_kwh: ["Battery (LCY per kWh)", "Batterie (LCY par kWh)"],
  battery_life_years: ["Battery life (years)", "Durée de vie batterie (années)"],
  diesel_per_kw: ["Diesel genset (LCY per kW)", "Groupe diesel (LCY par kW)"],
  diesel_fuel_per_kwh: ["Diesel fuel (LCY per kWh)", "Carburant (LCY par kWh)"],
  diesel_kgco2_per_kwh: ["Diesel emission factor (kgCO2 per kWh)", "Facteur d'émission diesel (kgCO2 par kWh)"],
  minigrid_network_per_connection: ["Mini grid network (LCY per connection)", "Réseau mini-réseau (LCY par raccordement)"],
  minigrid_om_pct_capex: ["Mini grid O&M (% of capex per year)", "Exploitation mini-réseau (% de l'investissement par an)", "pct"],
  pv_yield_kwh_per_kwp_pa: ["PV yield (kWh per kWp per year)", "Productible PV (kWh par kWc par an)"],
  network_loss: ["Network losses (%)", "Pertes réseau (%)", "pct"],
  battery_share_of_daily_energy: ["Battery share of daily energy (%)", "Part de l'énergie journalière via batterie (%)", "pct"],
  battery_depth_of_discharge: ["Battery depth of discharge (%)", "Profondeur de décharge (%)", "pct"],
  anchor_daytime_share: ["Anchor daytime share (%)", "Part diurne du client d'ancrage (%)", "pct"],
  hybrid_diesel_share: ["Hybrid diesel share (%)", "Part diesel en hybride (%)", "pct"],
  shs_cost_per_household: ["Solar home system (LCY per household)", "Kit solaire (LCY par ménage)"],
  shs_kwh_month_capacity: ["Solar home system capacity (kWh per month)", "Capacité du kit solaire (kWh par mois)"],
  shs_life_years: ["Solar home system life (years)", "Durée de vie du kit (années)"],
  shs_om_pct_capex: ["Solar home system O&M (% of capex per year)", "Maintenance des kits (% de l'investissement par an)", "pct"],
  months_densification: ["Time to electrify: densification (months)", "Délai : densification (mois)"],
  months_extension: ["Time to electrify: extension (months)", "Délai : extension (mois)"],
  months_minigrid: ["Time to electrify: mini grid (months)", "Délai : mini-réseau (mois)"],
  months_shs: ["Time to electrify: solar home systems (months)", "Délai : kits solaires (mois)"],
  affordability_share_of_income: ["Affordability limit (% of income)", "Seuil d'accessibilité (% du revenu)", "pct"],
  max_unserved_share: ["Maximum unserved demand (%)", "Demande non servie maximale (%)", "pct"],
  tariff_household_per_kwh: ["Tariff, households (LCY per kWh)", "Tarif, ménages (LCY par kWh)"],
  tariff_business_per_kwh: ["Tariff, businesses (LCY per kWh)", "Tarif, commerces (LCY par kWh)"],
  tariff_productive_per_kwh: ["Tariff, productive users (LCY per kWh)", "Tarif, usages productifs (LCY par kWh)"],
  tariff_institution_per_kwh: ["Tariff, institutions (LCY per kWh)", "Tarif, institutions (LCY par kWh)"],
  tariff_anchor_per_kwh: ["Tariff, anchor (LCY per kWh)", "Tarif, client d'ancrage (LCY par kWh)"],
};

const WEIGHTS: Record<string, L> = {
  economic_cost: ["Economic cost (%)", "Coût économique (%)", "pct"],
  time: ["Time to electrify (%)", "Délai d'électrification (%)", "pct"],
  service_quality: ["Service quality (%)", "Qualité de service (%)", "pct"],
  subsidy_efficiency: ["Subsidy efficiency (%)", "Efficacité de la subvention (%)", "pct"],
  financial_sustainability: ["Financial sustainability (%)", "Viabilité financière (%)", "pct"],
  environment: ["Environment (%)", "Environnement (%)", "pct"],
  productive_use: ["Productive use (%)", "Usages productifs (%)", "pct"],
};

function FieldBox({ k, l, value, onChange, error }: { k: string; l: L; value: Json | undefined; onChange: (v: Json | undefined) => void; error?: string }) {
  const { locale } = useI18n();
  const id = useId();
  const text = l[locale === "fr" ? 1 : 0];
  const kind = l[2] ?? "num";
  if (kind === "bool") {
    return (
      <label className="flex items-center gap-2 self-end pb-2 text-sm">
        <input type="checkbox" className="size-4 accent-emerald-600" checked={value === true} onChange={(e) => onChange(e.target.checked)} />
        {text}
      </label>
    );
  }
  return (
    <div className="flex flex-col gap-1">
      <Label htmlFor={id}>{text}</Label>
      {kind === "text" ? (
        <Input id={id} value={typeof value === "string" ? value : ""} onChange={(e) => onChange(e.target.value)} aria-invalid={!!error} />
      ) : kind === "tri" ? (
        <Select id={id} value={value === true ? "yes" : value === false ? "no" : ""} onChange={(e) => onChange(e.target.value === "yes" ? true : e.target.value === "no" ? false : null)}>
          <option value="">{locale === "fr" ? "Inconnu" : "Unknown"}</option>
          <option value="yes">{locale === "fr" ? "Oui" : "Yes"}</option>
          <option value="no">{locale === "fr" ? "Non" : "No"}</option>
        </Select>
      ) : (
        <NumberBox id={id} value={value} pct={kind === "pct"} int={kind === "int"} invalid={!!error} onChange={(v) => onChange(v === undefined ? (k === "distance_to_grid_km" ? null : undefined) : v)} />
      )}
      {error ? <p className="text-xs text-danger-700">{error}</p> : null}
    </div>
  );
}

function Group({ title, defs, obj, set, errors, prefix }: { title: string; defs: Record<string, L>; obj: Obj; set: (k: string, v: Json | undefined) => void; errors: Record<string, string>; prefix: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Object.entries(defs).map(([k, l]) => (
            <FieldBox key={k} k={k} l={l} value={obj[k]} onChange={(v) => set(k, v)} error={errors[`${prefix}.${k}`]} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default function OptimizerPage() {
  const { t, locale } = useI18n();
  const [settlement, setSettlement] = useState<Obj>({});
  const [costs, setCosts] = useState<Obj>({});
  const [weights, setWeights] = useState<Obj>({});
  const [demoLabel, setDemoLabel] = useState<string | null>(null);
  const [fromDemo, setFromDemo] = useState(false);
  const [res, setRes] = useState<CompareResult | null>(null);
  const [resDemo, setResDemo] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  async function loadDemo() {
    try {
      const d = await api<{ label: string; settlement: Obj; costs: Obj; weights: Obj }>("/api/optimizer/demo");
      setSettlement(d.settlement);
      setCosts(d.costs);
      setWeights(d.weights);
      setDemoLabel(d.label);
      setFromDemo(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- prefill once with the labelled synthetic demo
    void loadDemo();
  }, []);

  const upd = (setter: (f: (o: Obj) => Obj) => void) => (k: string, v: Json | undefined) =>
    setter((o) => {
      const n = { ...o };
      if (v === undefined) delete n[k];
      else n[k] = v;
      return n;
    });

  async function compare() {
    setBusy(true);
    setError(null);
    setErrors({});
    try {
      const r = await api<CompareResult>("/api/optimizer/compare", { method: "POST", body: { settlement, costs, weights } });
      setRes(r);
      setResDemo(fromDemo);
    } catch (e) {
      if (e instanceof ApiError) setErrors(e.fieldErrors());
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  const scatter = (res?.options ?? [])
    .filter((o) => o.feasible && typeof o.lcoe === "number" && typeof o.months_to_electrify === "number")
    .map((o) => ({ code: o.code, name: o.name, months: o.months_to_electrify as number, lcoe: o.lcoe as number }));
  const byCode = (c: string | null) => res?.options.find((o) => o.code === c);

  return (
    <>
      <PageHeader
        title={t("opt.title")}
        lead={t("opt.lead")}
        actions={
          <Button variant="gold" onClick={loadDemo}>
            {t("opt.loadDemo")}
          </Button>
        }
      />
      <div className="flex flex-col gap-5">
        {fromDemo && demoLabel ? (
          <Alert variant="warning" className="items-center">
            <DemoBadge /> <span>{demoLabel}</span>
          </Alert>
        ) : null}
        <Group
          title={t("opt.settlement")}
          defs={SETTLEMENT}
          obj={settlement}
          set={(k, v) => {
            upd(setSettlement)(k, v);
            setFromDemo(false);
          }}
          errors={errors}
          prefix="settlement"
        />
        <Group
          title={t("opt.costs")}
          defs={COSTS}
          obj={costs}
          set={(k, v) => {
            upd(setCosts)(k, v);
            setFromDemo(false);
          }}
          errors={errors}
          prefix="costs"
        />
        <Group title={t("opt.weights")} defs={WEIGHTS} obj={weights} set={upd(setWeights)} errors={errors} prefix="weights" />
        <div>
          <Button variant="accent" size="lg" onClick={compare} disabled={busy} data-testid="compare-options">
            {busy ? <Loader2 className="animate-spin" aria-hidden /> : null}
            {busy ? t("opt.comparing") : t("opt.compare")}
          </Button>
        </div>
        {error ? <ErrorBox error={error} /> : null}

        {res ? (
          <section className="flex flex-col gap-5" data-testid="optimizer-results" aria-labelledby="opt-res">
            <div className="flex flex-wrap items-center gap-2">
              <h2 id="opt-res" className="text-lg font-semibold text-navy-900">
                {t("opt.options")}: {res.settlement}
              </h2>
              <DemoBadge show={resDemo} />
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              {[
                { code: res.least_cost, title: t("opt.leastCost"), icon: Award },
                { code: res.recommended, title: t("opt.recommended"), icon: Star },
              ].map((c) => {
                const o = byCode(c.code);
                return (
                  <Card key={c.title} className="border-l-4 border-l-emerald-600">
                    <CardHeader>
                      <CardDescription className="flex items-center gap-1.5 uppercase tracking-wide">
                        <c.icon className="size-3.5 text-gold-700" aria-hidden /> {c.title}
                      </CardDescription>
                      <CardTitle className="text-base">{o ? `${o.code}. ${o.name}` : t("common.dataUnavailable")}</CardTitle>
                    </CardHeader>
                    {o ? (
                      <CardContent className="text-sm text-muted-foreground">
                        LCOE {num(o.lcoe, locale, 1)} LCY/kWh · {num(o.months_to_electrify, locale)} {t("opt.months").toLowerCase()} · {t("opt.score")} {num(o.score, locale, 1)}
                      </CardContent>
                    ) : null}
                  </Card>
                );
              })}
            </div>
            <Alert variant="info" data-testid="optimizer-explanation">
              {res.explanation}
            </Alert>
            <Card>
              <TableWrap>
                <Table className="text-xs" data-testid="options-table">
                  <thead>
                    <tr>
                      <Th>{t("opt.option")}</Th>
                      <Th>{t("opt.feasible")}</Th>
                      <Th className="text-right">{t("opt.lcoe")}</Th>
                      <Th className="text-right">{t("opt.costPerConn")}</Th>
                      <Th className="text-right">{t("opt.tier")}</Th>
                      <Th className="text-right">{t("opt.months")}</Th>
                      <Th className="text-right">{t("opt.subsidyPerConn")}</Th>
                      <Th className="text-right">{t("opt.billIncome")}</Th>
                      <Th className="text-right">{t("opt.co2")}</Th>
                      <Th className="text-right">{t("opt.score")}</Th>
                      <Th>{t("opt.pareto")}</Th>
                    </tr>
                  </thead>
                  <tbody>
                    {res.options.map((o) => (
                      <tr key={o.code} className={cn(o.code === res.recommended && "bg-emerald-50", !o.feasible && "text-muted-foreground")}>
                        <Td className="min-w-48">
                          <span className="font-semibold text-navy-900">{o.code}.</span> {o.name}
                          {o.code === res.recommended ? (
                            <Badge variant="success" className="ml-1">
                              {t("opt.recommended")}
                            </Badge>
                          ) : null}
                          {o.code === res.least_cost ? (
                            <Badge variant="navy" className="ml-1">
                              {t("opt.leastCost")}
                            </Badge>
                          ) : null}
                        </Td>
                        <Td className="min-w-40">
                          {o.feasible ? (
                            <span className="inline-flex items-center gap-1 text-emerald-700">
                              <CheckCircle2 className="size-3.5" aria-hidden /> {t("common.yes")}
                            </span>
                          ) : (
                            <span className="flex flex-col gap-0.5 text-danger-700">
                              <span className="inline-flex items-center gap-1">
                                <XCircle className="size-3.5" aria-hidden /> {t("opt.failedGates")}
                              </span>
                              {o.gates_failed.map((g) => (
                                <span key={g} className="text-[11px]">
                                  {g}
                                </span>
                              ))}
                            </span>
                          )}
                        </Td>
                        <Td className="text-right">{num(o.lcoe, locale, 1)}</Td>
                        <Td className="text-right">{num(o.cost_per_connection, locale, 0)}</Td>
                        <Td className="text-right">{num(o.service_tier, locale, 0)}</Td>
                        <Td className="text-right">{num(o.months_to_electrify, locale, 0)}</Td>
                        <Td className="text-right">{num(o.subsidy_per_connection, locale, 0)}</Td>
                        <Td className="text-right">{pct(o.bill_to_income, locale)}</Td>
                        <Td className="text-right">{num(o.co2_t_pa, locale, 1)}</Td>
                        <Td className="text-right">{num(o.score, locale, 1)}</Td>
                        <Td>{o.pareto_efficient ? t("common.yes") : t("common.no")}</Td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </TableWrap>
            </Card>
            <ChartFrame title={t("opt.scatter")} subtitle="LCY/kWh" height={300} testId="optimizer-scatter">
              <OptionsScatter data={scatter} locale={locale} xName={t("opt.months")} yName="LCOE" />
            </ChartFrame>
            <Card>
              <CardHeader>
                <CardTitle>{t("opt.method")}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">{res.method_note}</CardContent>
            </Card>
          </section>
        ) : null}
      </div>
    </>
  );
}
