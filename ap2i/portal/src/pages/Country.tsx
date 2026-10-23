import { useMemo } from "react";
import type { EChartsCoreOption as EChartsOption } from "echarts/core";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { annual, commitmentsOf, completionYear, countBy, disbursedByCurrency, maxLevel, moneyBy, yearFlags, type Money } from "../lib/agg";
import { currencyLines, escapeHtml, fmtAmount, fmtDate, fmtNum, fmtPct, moneyTooltip } from "../lib/format";
import { go, href, type Route } from "../lib/router";
import { donut, hbar, moneyLine } from "../lib/charts";
import { LEVELS, type Filters } from "../lib/filters";
import { EChart } from "../components/EChart";
import { FilterBar } from "../components/FilterBar";
import { Card, Empty, Kpi, PageHead } from "../components/ui";

export function Country({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const iso3 = (route.path[1] ?? "CMR").toUpperCase();
  const f: Filters = useMemo(() => ({ ...route.filters, country: iso3 }), [route.filters, iso3]);
  const fNoYears: Filters = useMemo(() => ({ ...f, y0: undefined, y1: undefined }), [f]);
  const sel = useSelection(f);
  const selAll = useSelection(fNoYears); // annual series: transaction years over all projects matching the other filters
  const country = s.ref.countries.find((c) => c.iso3 === iso3);
  const y0 = f.y0 ?? 2011, y1 = f.y1 ?? s.meta.years[1];
  const years = useMemo(() => Array.from({ length: y1 - y0 + 1 }, (_, i) => y0 + i), [y0, y1]);
  const prov = useMemo(() => [s.meta.scope, `snapshot ${s.meta.generated_at}`, t("money.note"), `filters: ${window.location.hash}`], [s, t]);
  const toProjects = (patch: Filters) => go("/projects", { ...f, ...patch });

  const series = useMemo(() => {
    const c = annual(s.flows, selAll.agreementIds, "commitment", y0, y1);
    const d = annual(s.flows, selAll.agreementIds, "disbursement", y0, y1);
    return { c, d };
  }, [s, selAll, y0, y1]);

  if (!country) return <Empty />;
  if (!country.documented_projects) {
    return (<div><PageHead title={names.country(iso3)} /><Card><p>{t("country.noData")}</p></Card></div>);
  }

  const ps = sel.projects;
  const money = commitmentsOf(sel.agreements);
  const unconvertedN = sel.agreements.filter((a) => a.committed !== null && a.committed_usd === null).length;
  const attentionPs = ps.filter((p) => { const l = maxLevel(p); return l === "critical_attention" || l === "high_attention"; });
  const attention = attentionPs.length;
  // of which: flagged only because the closing date has passed while the source still says "active"
  const seriousRules = new Map<number, Set<string>>();
  for (const a of s.alerts.items) if (a.level === "critical_attention" || a.level === "high_attention")
    seriousRules.set(a.project.id, (seriousRules.get(a.project.id) ?? new Set()).add(a.rule_code));
  const stale = attentionPs.filter((p) => { const r = seriousRules.get(p.id); return r && r.size === 1 && r.has("CLOSING_DATE_PASSED"); }).length;
  const lastSync = s.africa.countries.find((x) => x.iso3 === iso3)?.last_update ?? null;
  const cYears = years.map((y) => series.c.years[y]);
  const dYears = years.map((y) => series.d.years[y]);
  const flags = yearFlags(years, [cYears, dYears], s.meta.generated_at);
  const flagNote = [flags.some((x) => x.partial) ? t("chart.partialYear", { y: s.meta.generated_at.slice(0, 4), d: fmtDate(s.meta.generated_at, locale) }) : "",
    flags.some((x) => x.incomplete) ? t("chart.incompleteYear") : ""].filter(Boolean).join(" ");

  // Chart data -------------------------------------------------------------------------------------
  const bySector = countBy(ps, (p) => p.sector ?? "UNCLASSIFIED");
  const sectorCodes = [...bySector.keys()];
  const byPartner = moneyBy(sel.agreements, (a) => a.partner);
  const partnerCodes = [...byPartner.keys()];
  const byInstr = countBy(sel.agreements, (a) => a.instrument ?? "—");
  const instrCodes = [...byInstr.keys()];
  const byStatus = countBy(ps, (p) => p.status);
  const statusCodes = [...byStatus.keys()];
  const byLevel = LEVELS.map((l) => ({ l, n: ps.filter((p) => maxLevel(p) === l).length }));
  const compl: Record<number, { actual: number; proxy: number }> = {};
  for (const y of years) compl[y] = { actual: 0, proxy: 0 };
  for (const p of ps) {
    const c = completionYear(p);
    if (c && compl[c.year]) compl[c.year][c.basis === "actual" ? "actual" : "proxy"]++;
  }
  const missing: [string, number][] = [
    ["Physical progress", ps.filter((p) => p.physical_progress === null).length],
    ["Estimated cost", ps.filter((p) => p.original_cost === null).length],
    ["Operational status", ps.filter((p) => p.operational_status === "unknown").length],
    ["Region", ps.filter((p) => !p.region).length],
    ["Approval date", ps.filter((p) => !p.approval).length],
    ["Executing agency", ps.filter((p) => !p.agency).length],
    ["Planned completion date", ps.filter((p) => !p.planned_end).length],
    ["Start date", ps.filter((p) => !p.start).length],
    ["Sector", ps.filter((p) => !p.sector).length],
    ["Coordinates", ps.filter((p) => !p.locations.length).length],
  ];
  missing.sort((a, b) => b[1] - a[1]);
  const fieldLabel = (k: string) => (locale === "fr" ? ({ "Physical progress": "Avancement physique", "Estimated cost": "Coût estimé",
    "Operational status": "Statut opérationnel", Region: "Région", "Approval date": "Date d'approbation", "Executing agency": "Agence d'exécution",
    "Planned completion date": "Date de fin prévue", "Start date": "Date de démarrage", Sector: "Secteur", Coordinates: "Coordonnées" } as Record<string, string>)[k] ?? k : k);

  const moneyRows = (m: Money[], label: string) => years.map((y, i) => [y, label, m[i].usd === null ? null : Math.round(m[i].usd!),
    currencyLines(m[i].byCurrency, "en"), currencyLines(m[i].unconverted, "en"), m[i].n]);
  const moneyHeader = ["year", "measure", "usd_equivalent", "by_currency", "not_converted", "transactions"];

  const c8: EChartsOption = moneyLine(years, [{ name: t("chart.commitments"), data: cYears }, { name: t("chart.disbursements"), data: dYears }], locale, t, "bar", flags);
  const c9: EChartsOption = {
    grid: { left: 8, right: 16, top: 36, bottom: 8, containLabel: true }, legend: { top: 0 }, tooltip: { trigger: "axis" },
    xAxis: { type: "category", data: years.map(String) }, yAxis: { type: "value", minInterval: 1 },
    series: [
      { type: "bar", stack: "c", name: t("chart.actual"), data: years.map((y) => compl[y].actual) },
      { type: "bar", stack: "c", name: t("chart.closingProxy"), data: years.map((y) => compl[y].proxy) },
    ],
  };

  return (
    <div>
      <PageHead title={`${t("country.title")} — ${names.country(iso3)}`} subtitle={`${iso3} · ${names.region(country.region)} · ${country.currency}`}>
        <select aria-label={t("country.choose")} value={iso3} onChange={(e) => go(`/country/${e.target.value}`, route.filters)}>
          {s.ref.countries.map((c) => <option key={c.iso3} value={c.iso3}>{names.country(c.iso3)}{c.documented_projects ? "" : " —"}</option>)}
        </select>
      </PageHead>
      <FilterBar route={route} undated={sel.undatedExcluded} hide={["country"]} />
      <div className="kpis">
        <Kpi label={t("kpi.projects")} value={fmtNum(ps.length, locale)} href={href("/projects", f)} />
        <Kpi label={t("kpi.commitmentsAll")} value={fmtAmount(money.usd, locale, "USD")} help={t("kpi.commitmentsHelp")}
          sub={unconvertedN ? t("kpi.notConvertedAmounts", { amounts: currencyLines(money.unconverted, locale) }) : undefined} href={href("/finance", f)} />
        <Kpi label={t("kpi.disbursed")} help={t("kpi.disbursedHelp")} value={<span className="small-v">{currencyLines(disbursedByCurrency(sel.agreements), locale)}</span>} />
        <Kpi label={t("kpi.active")} value={fmtNum(ps.filter((p) => p.status === "active").length, locale)} href={href("/projects", { ...f, status: ["active"] })} />
        <Kpi label={t("kpi.attention")} value={fmtNum(attention, locale)} help={t("kpi.attentionHelp")}
          sub={stale ? t("attention.stale", { n: stale }) : undefined} href={href("/projects", { ...f, alert: "attention" }, { sort: "alerts" })} />
        <Kpi label={t("kpi.lastSync")} value={<span className="small-v">{fmtDate(lastSync, locale)}</span>} />
      </div>
      <p className="muted small">{t("chart.clickHint")} {t("money.note")}</p>
      <div className="grid-2">
        <EChart id="c1" title={t("chart.c1")} provenance={prov}
          option={moneyLine(years, [{ name: t("chart.commitments"), data: cYears }], locale, t, "line", flags)}
          data={{ header: moneyHeader, rows: moneyRows(cYears, "commitment") }}
          onClick={(p) => toProjects({ y0: years[p.dataIndex], y1: years[p.dataIndex] })}
          note={[series.c.undated ? t("chart.undated", { n: series.c.undated }) : "", flagNote].filter(Boolean).join(" ") || undefined} />
        <EChart id="c2" title={t("chart.c2")} provenance={prov}
          option={moneyLine(years, [{ name: t("chart.disbursements"), data: dYears }], locale, t, "line", flags)}
          data={{ header: moneyHeader, rows: moneyRows(dYears, "disbursement") }}
          note={[series.d.undated ? t("chart.undated", { n: series.d.undated }) : "", flagNote].filter(Boolean).join(" ") || undefined} />
        <EChart id="c3" title={t("chart.c3")} provenance={prov}
          option={hbar(sectorCodes.map((c) => names.sector(c === "UNCLASSIFIED" ? null : c)), [...bySector.values()], locale, { seriesName: t("common.projects") })}
          data={{ header: ["sector_code", "sector", "projects"], rows: sectorCodes.map((c) => [c, names.sector(c === "UNCLASSIFIED" ? null : c), bySector.get(c)!]) }}
          onClick={(p) => go(`/country/${iso3}`, { ...route.filters, sector: sectorCodes[p.dataIndex] })} height={360} />
        <EChart id="c4" title={t("chart.c4")} provenance={prov}
          option={hbar(partnerCodes.map((c) => names.partner(c === "—" ? null : c)), [...byPartner.values()].map((m) => (m.usd === null ? null : Math.round(m.usd))), locale, {
            money: true, seriesName: t("chart.commitments"), tooltip: (i) => `${escapeHtml(names.partner(partnerCodes[i] === "—" ? null : partnerCodes[i]))}<br/>${moneyTooltip([...byPartner.values()][i], locale, t)}` })}
          data={{ header: ["partner", "usd_equivalent", "by_currency", "not_converted", "agreements"], rows: partnerCodes.map((c) => {
            const m = byPartner.get(c)!; return [c, m.usd === null ? null : Math.round(m.usd), currencyLines(m.byCurrency, "en"), currencyLines(m.unconverted, "en"), m.n]; }) }}
          onClick={(p) => partnerCodes[p.dataIndex] !== "—" && go(`/country/${iso3}`, { ...route.filters, partner: partnerCodes[p.dataIndex] })} />
        <EChart id="c5" title={t("chart.c5")} provenance={prov}
          option={donut(instrCodes.map((c) => ({ name: names.instrument(c === "—" ? null : c), value: byInstr.get(c)! })), locale)}
          data={{ header: ["instrument", "agreements"], rows: instrCodes.map((c) => [c, byInstr.get(c)!]) }}
          onClick={(p) => instrCodes[p.dataIndex] !== "—" && go(`/country/${iso3}`, { ...route.filters, instrument: instrCodes[p.dataIndex] })}
          note={t("chart.agreements")} />
        <EChart id="c6" title={t("chart.c6")} provenance={prov}
          option={donut(statusCodes.map((c) => ({ name: t(`status.${c}`), value: byStatus.get(c)! })), locale)}
          data={{ header: ["status", "projects"], rows: statusCodes.map((c) => [c, byStatus.get(c)!]) }}
          onClick={(p) => toProjects({ status: [statusCodes[p.dataIndex]] })} />
        <EChart id="c7" title={t("chart.c7")} provenance={prov}
          option={hbar(byLevel.map((x) => t(`level.${x.l}`)), byLevel.map((x) => x.n), locale, { seriesName: t("common.projects") })}
          data={{ header: ["highest_alert_level", "projects"], rows: byLevel.map((x) => [x.l, x.n]) }}
          onClick={(p) => toProjects({ alert: byLevel[p.dataIndex].l })} note={t("attention.def")} />
        <EChart id="c8" title={t("chart.c8")} provenance={prov} option={c8} note={flagNote || undefined}
          data={{ header: moneyHeader, rows: [...moneyRows(cYears, "commitment"), ...moneyRows(dYears, "disbursement")] }}
          onClick={(p) => toProjects({ y0: years[p.dataIndex], y1: years[p.dataIndex] })} />
        <EChart id="c9" title={t("chart.c9")} provenance={prov} option={c9} note={t("chart.c9note")}
          data={{ header: ["year", "completed_actual_date", "closed_closing_date_proxy"], rows: years.map((y) => [y, compl[y].actual, compl[y].proxy]) }} />
        <EChart id="c10" title={t("chart.c10")} provenance={prov}
          option={hbar(missing.map(([k]) => fieldLabel(k)), missing.map(([, n]) => n), locale, { seriesName: t("chart.missing"),
            tooltip: (i) => `${escapeHtml(fieldLabel(missing[i][0]))}<br/>${fmtNum(missing[i][1], locale)} / ${fmtNum(ps.length, locale)} (${fmtPct(ps.length ? missing[i][1] / ps.length : null, locale)})` })}
          data={{ header: ["field", "projects_missing", "projects_total"], rows: missing.map(([k, n]) => [k, n, ps.length]) }} height={360} />
      </div>
    </div>
  );
}
