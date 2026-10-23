import { useMemo } from "react";
import type { EChartsCoreOption as EChartsOption } from "echarts/core";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { annual, commitmentsOf, moneyBy, type Money } from "../lib/agg";
import { currencyLines, escapeHtml, fmtAmount, fmtDate, fmtPct, moneyTooltip } from "../lib/format";
import { go, href, type Route } from "../lib/router";
import { hbar, stacked } from "../lib/charts";
import type { Filters } from "../lib/filters";
import { EChart } from "../components/EChart";
import { FilterBar } from "../components/FilterBar";
import { DataTable } from "../components/DataTable";
import { Card, Kpi, PageHead } from "../components/ui";

export function Finance({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = route.filters;
  const sel = useSelection(f);
  const selAll = useSelection({ ...f, y0: undefined, y1: undefined });
  const y0 = f.y0 ?? 2011, y1 = f.y1 ?? s.meta.years[1];
  const years = useMemo(() => Array.from({ length: y1 - y0 + 1 }, (_, i) => y0 + i), [y0, y1]);
  const prov = [s.meta.scope, `snapshot ${s.meta.generated_at}`, t("money.note"), `filters: ${window.location.hash}`];
  const projById = useMemo(() => new Map(s.projects.map((p) => [p.id, p])), [s]);
  const drill = route.qs.get("drill")?.split("|").filter(Boolean).slice(0, 2) ?? []; // [sector, partner]

  // Stacked annual series by partner (dated transactions, USD eq.)
  const byPartnerYear = (kind: "commitment" | "disbursement") => {
    const partners = [...new Set(selAll.agreements.map((a) => a.partner ?? "—"))];
    return partners.map((pc) => {
      const ids = new Set(selAll.agreements.filter((a) => (a.partner ?? "—") === pc).map((a) => a.id));
      const ys = annual(s.flows, ids, kind, y0, y1).years;
      return { name: names.partner(pc === "—" ? null : pc), data: years.map((y) => (ys[y].usd === null ? null : Math.round(ys[y].usd!))) };
    }).filter((g) => g.data.some((v) => v !== null));
  };
  const cByP = useMemo(() => byPartnerYear("commitment"), [selAll, years, names]); // eslint-disable-line react-hooks/exhaustive-deps
  const dByP = useMemo(() => byPartnerYear("disbursement"), [selAll, years, names]); // eslint-disable-line react-hooks/exhaustive-deps

  const bySector = moneyBy(sel.agreements, (a) => projById.get(a.project)?.sector ?? null, "UNCLASSIFIED");
  const sectorKeys = [...bySector.keys()];
  const byInstr = moneyBy(sel.agreements, (a) => a.instrument);
  const instrKeys = [...byInstr.keys()];

  // Sankey institution → sector (USD-converted commitments only)
  const sankey: EChartsOption = useMemo(() => {
    const links = new Map<string, number>();
    for (const a of sel.agreements) {
      if (a.committed_usd === null) continue;
      const src = `P:${names.partner(a.partner)}`, dst = `S:${names.sector(projById.get(a.project)?.sector ?? null)}`;
      links.set(`${src}→${dst}`, (links.get(`${src}→${dst}`) ?? 0) + Number(a.committed_usd));
    }
    const nodes = new Set<string>();
    const data = [...links.entries()].map(([k, v]) => {
      const [source, target] = k.split("→");
      nodes.add(source);
      nodes.add(target);
      return { source, target, value: Math.round(v) };
    });
    return {
      tooltip: { trigger: "item", formatter: (p: unknown) => {
        const x = p as { data: { source?: string; target?: string; value?: number }; name: string; value: number };
        return x.data.source ? `${escapeHtml(x.data.source.slice(2))} → ${escapeHtml(x.data.target!.slice(2))}<br/>${fmtAmount(x.data.value!, locale, "USD")}` : `${escapeHtml(x.name.slice(2))}<br/>${fmtAmount(x.value, locale, "USD")}`;
      } },
      series: [{ type: "sankey", data: [...nodes].map((n) => ({ name: n })), links: data, emphasis: { focus: "adjacency" },
        label: { formatter: (p: { name: string }) => p.name.slice(2) }, nodeGap: 6, lineStyle: { color: "gradient", curveness: 0.5, opacity: 0.35 } }],
    };
  }, [sel.agreements, names, projById, locale]);

  // Treemap drill-down: sector → institution → project (agreements → transactions are in the project profile)
  const tree = useMemo(() => {
    const level = drill.length;
    const groups = new Map<string, { value: number; id: string; kind: string }>();
    for (const a of sel.agreements) {
      if (a.committed_usd === null) continue;
      const p = projById.get(a.project)!;
      const sec = p.sector ?? "UNCLASSIFIED";
      if (level >= 1 && sec !== drill[0]) continue;
      if (level >= 2 && (a.partner ?? "—") !== drill[1]) continue;
      const key = level === 0 ? sec : level === 1 ? a.partner ?? "—" : p.ref;
      const label = level === 0 ? names.sector(sec === "UNCLASSIFIED" ? null : sec) : level === 1 ? names.partner(a.partner) : `${p.ref} — ${p.title.slice(0, 60)}`;
      const g = groups.get(label) ?? { value: 0, id: key, kind: level === 0 ? "sector" : level === 1 ? "partner" : "project" };
      g.value += Number(a.committed_usd);
      groups.set(label, g);
    }
    return [...groups.entries()].map(([name, g]) => ({ name, value: Math.round(g.value), id: g.id, kind: g.kind })).sort((a, b) => b.value - a.value);
  }, [sel.agreements, projById, names, drill]);
  const treemap: EChartsOption = {
    tooltip: { formatter: (p: unknown) => { const x = p as { name: string; value: number }; return `${escapeHtml(x.name)}<br/>${fmtAmount(x.value, locale, "USD")}`; } },
    series: [{ type: "treemap", data: tree, roam: false, nodeClick: false, breadcrumb: { show: false }, label: { formatter: "{b}" }, width: "100%", height: "100%" }],
  };
  const onTree = (p: { data?: unknown }) => {
    const x = p.data as { id: string; kind: string } | undefined;
    if (!x) return;
    if (x.kind === "project") go(`/project/${x.id}`, f);
    else go("/finance", f, { drill: [...drill, x.id].join("|") });
  };

  // Cumulative execution (dated disbursements / dated commitments), per currency-consistent USD equivalents
  // cumulative from the first dated transaction (not from an arbitrary year)
  const firstYear = Math.min(y0, ...s.flows.year.filter((y): y is number => y !== null));
  const cAll = annual(s.flows, selAll.agreementIds, "commitment", firstYear, y1);
  const dAll = annual(s.flows, selAll.agreementIds, "disbursement", firstYear, y1);
  let cc = 0, cd = 0;
  const cum = years.map(() => [0, 0]);
  for (let y = firstYear; y <= y1; y++) {
    cc += cAll.years[y].usd ?? 0;
    cd += dAll.years[y].usd ?? 0;
    if (y >= y0) cum[y - y0] = [Math.round(cc), Math.round(cd)];
  }
  const execOpt: EChartsOption = {
    grid: { left: 8, right: 40, top: 36, bottom: 8, containLabel: true }, legend: { top: 0 },
    tooltip: { trigger: "axis", formatter: (ps: unknown) => {
      const arr = ps as { dataIndex: number }[];
      const i = arr[0]?.dataIndex ?? 0;
      const [c, d] = cum[i];
      return `<b>${years[i]}</b><br/>${t("finance.cumCommit")}: ${fmtAmount(c, locale, "USD")}<br/>${t("finance.cumDisb")}: ${fmtAmount(d, locale, "USD")}<br/>ratio: ${fmtPct(c ? d / c : null, locale, 1)}`;
    } },
    xAxis: { type: "category", data: years.map(String) }, yAxis: { type: "value", axisLabel: { formatter: (v: number) => fmtAmount(v, locale) } },
    series: [{ type: "line", name: t("finance.cumCommit"), data: cum.map((x) => x[0]) }, { type: "line", name: t("finance.cumDisb"), data: cum.map((x) => x[1]), areaStyle: { opacity: 0.15 } }],
  };

  const costRows = sel.projects.filter((p) => p.original_cost !== null && p.revised_cost !== null);
  const additional = sel.agreements.filter((a) => a.parent);
  const undisb: Record<string, number> = {};
  for (const a of sel.agreements) if (a.undisbursed !== null && a.currency && !a.is_guarantee) undisb[a.currency] = (undisb[a.currency] ?? 0) + Number(a.undisbursed);
  const total = commitmentsOf(sel.agreements);
  const setFilter = (patch: Filters) => go("/finance", { ...f, ...patch });

  return (
    <div>
      <PageHead title={t("finance.title")} subtitle={t("money.note")} />
      <FilterBar route={route} undated={sel.undatedExcluded} />
      <div className="kpis">
        <Kpi label={t("kpi.commitmentsAll")} help={t("kpi.commitmentsHelp")} value={fmtAmount(total.usd, locale, "USD")} sub={<>{currencyLines(total.byCurrency, locale)}{Object.keys(total.unconverted).length ? <> · {t("common.notConverted")}: {currencyLines(total.unconverted, locale)}</> : null}</>} />
        <Kpi label={t("kpi.agreements")} value={sel.agreements.length} />
        <Kpi label={t("finance.undisbursed")} value={<span className="small-v">{currencyLines(undisb, locale)}</span>} />
        <Kpi label={t("finance.linked")} value={additional.length} />
      </div>
      <div className="grid-2">
        <EChart id="f1" title={t("finance.byYearPartner")} provenance={prov} option={stacked(years, cByP, locale)}
          data={{ header: ["institution", ...years.map(String)], rows: cByP.map((g) => [g.name, ...g.data]) }}
          onClick={(p) => go("/projects", { ...f, y0: years[p.dataIndex], y1: years[p.dataIndex], partner: s.ref.partners.find((x) => x.short_name === p.seriesName)?.code })} />
        <EChart id="f2" title={t("finance.byYearDisb")} provenance={prov} option={stacked(years, dByP, locale)}
          data={{ header: ["institution", ...years.map(String)], rows: dByP.map((g) => [g.name, ...g.data]) }} />
        <EChart id="f3" title={t("finance.bySector")} provenance={prov}
          option={hbar(sectorKeys.map((k) => names.sector(k === "UNCLASSIFIED" ? null : k)), [...bySector.values()].map((m) => (m.usd === null ? null : Math.round(m.usd))), locale,
            { money: true, seriesName: t("chart.commitments"), tooltip: (i) => `${escapeHtml(names.sector(sectorKeys[i] === "UNCLASSIFIED" ? null : sectorKeys[i]))}<br/>${moneyTooltip([...bySector.values()][i], locale, t)}` })}
          data={{ header: ["sector", "usd_equivalent", "by_currency", "not_converted", "agreements"], rows: moneyRows(bySector) }}
          onClick={(p) => setFilter({ sector: sectorKeys[p.dataIndex] })} height={380} />
        <EChart id="f4" title={t("finance.byInstrument")} provenance={prov}
          option={hbar(instrKeys.map((k) => names.instrument(k === "—" ? null : k)), [...byInstr.values()].map((m) => (m.usd === null ? null : Math.round(m.usd))), locale,
            { money: true, seriesName: t("chart.commitments"), tooltip: (i) => `${escapeHtml(names.instrument(instrKeys[i] === "—" ? null : instrKeys[i]))}<br/>${moneyTooltip([...byInstr.values()][i], locale, t)}` })}
          data={{ header: ["instrument", "usd_equivalent", "by_currency", "not_converted", "agreements"], rows: moneyRows(byInstr) }}
          onClick={(p) => instrKeys[p.dataIndex] !== "—" && setFilter({ instrument: instrKeys[p.dataIndex] })} />
      </div>
      <EChart id="f5" title={t("finance.sankey")} provenance={prov} option={sankey} height={520}
        data={{ header: ["institution", "sector", "usd_equivalent"], rows: ((sankey.series as { links: { source: string; target: string; value: number }[] }[])[0].links).map((l) => [l.source.slice(2), l.target.slice(2), l.value]) }} />
      <nav className="crumbs card" style={{ padding: "8px 12px", marginBottom: 6 }} aria-label={t("finance.drill")}>
          <a href={href("/finance", f)}>{names.country(f.country ?? null) === "—" ? t("filters.all") : names.country(f.country ?? null)}</a>
          {drill[0] && <> › <a href={href("/finance", f, { drill: drill[0] })}>{names.sector(drill[0] === "UNCLASSIFIED" ? null : drill[0])}</a></>}
          {drill[1] && <> › <span>{names.partner(drill[1] === "—" ? null : drill[1])}</span></>}
          <span className="muted"> › {t("common.project")} › {t("col.agreement")} › {t("profile.transactions")}</span>
      </nav>
      <EChart id="f6" title={t("finance.treemap")} provenance={prov} option={treemap} height={420} onClick={onTree}
        data={{ header: ["node", "usd_equivalent"], rows: tree.map((x) => [x.name, x.value]) }} />
      <EChart id="f7" title={t("finance.execution")} provenance={prov} option={execOpt} note={t("finance.execNote")}
        data={{ header: ["year", "cumulative_dated_commitments_usd", "cumulative_dated_disbursements_usd"], rows: years.map((y, i) => [y, ...cum[i]]) }} />
      <div className="grid-2">
        <Card title={t("finance.costs")}>
          {costRows.length ? (
            <DataTable rows={costRows} rowKey={(p) => p.id} exportName="ap2i_costs" provenance={prov} columns={[
              { key: "ref", label: t("col.ref"), value: (p) => p.ref, render: (p) => <a href={href(`/project/${p.ref}`, f)}>{p.ref}</a> },
              { key: "o", label: t("finance.original"), align: "right", value: (p) => Number(p.original_cost), render: (p) => fmtAmount(Number(p.original_cost), locale, p.cost_currency ?? "") },
              { key: "r", label: t("finance.revised"), align: "right", value: (p) => Number(p.revised_cost), render: (p) => fmtAmount(Number(p.revised_cost), locale, p.cost_currency ?? "") },
              { key: "d", label: "Δ", align: "right", value: (p) => Number(p.revised_cost) / Number(p.original_cost) - 1, render: (p) => fmtPct(Number(p.revised_cost) / Number(p.original_cost) - 1, locale, 1) },
            ]} />
          ) : <p className="muted">{t("finance.costsNA")}</p>}
        </Card>
        <Card title={t("finance.linked")} note={t("finance.linkedNote")}>
          <DataTable rows={additional} rowKey={(a) => a.id} pageSize={10} exportName="ap2i_additional_financing" provenance={prov} columns={[
            { key: "id", label: t("col.agreement"), value: (a) => a.source_identifier },
            { key: "parent", label: "Parent", value: (a) => a.parent },
            { key: "p", label: t("col.ref"), value: (a) => projById.get(a.project)?.ref ?? null, render: (a) => <a href={href(`/project/${projById.get(a.project)?.ref}`, f)}>{projById.get(a.project)?.ref}</a> },
            { key: "c", label: t("chart.commitments"), align: "right", value: (a) => (a.committed === null ? null : Number(a.committed)), render: (a) => fmtAmount(a.committed === null ? null : Number(a.committed), locale, a.currency ?? "") },
          ]} />
        </Card>
      </div>
      <Card title={t("finance.table")}>
        <DataTable rows={sel.agreements} rowKey={(a) => a.id} exportName="ap2i_agreements" provenance={prov} columns={[
          { key: "id", label: t("col.agreement"), value: (a) => a.source_identifier },
          { key: "p", label: t("col.ref"), minWidth: "17ch", value: (a) => projById.get(a.project)?.ref ?? null, render: (a) => <a className="mono" href={href(`/project/${projById.get(a.project)?.ref}`, f)}>{projById.get(a.project)?.ref}</a> },
          { key: "partner", label: t("col.partners"), value: (a) => names.partner(a.partner) },
          { key: "instr", label: t("col.instrument"), value: (a) => (a.instrument ? names.instrument(a.instrument) : a.instrument_label) },
          { key: "appr", label: t("col.approval"), value: (a) => a.approval, render: (a) => fmtDate(a.approval, locale) },
          { key: "cur", label: t("col.currency"), value: (a) => a.currency },
          { key: "c", label: t("chart.commitments"), align: "right", value: (a) => (a.committed === null ? null : Number(a.committed)),
            render: (a) => (a.committed === null ? (a.committed_basis?.startsWith("not counted") ? t("profile.notCounted") : null) : fmtAmount(Number(a.committed), locale, a.currency ?? "")) },
          { key: "usd", label: t("col.usd"), align: "right", value: (a) => (a.committed_usd === null ? null : Number(a.committed_usd)), render: (a) => fmtAmount(a.committed_usd === null ? null : Number(a.committed_usd), locale, "USD") },
          { key: "d", label: t("col.disbursed"), align: "right", value: (a) => (a.disbursed === null ? null : Number(a.disbursed)), render: (a) => fmtAmount(a.disbursed === null ? null : Number(a.disbursed), locale, a.currency ?? "") },
          { key: "u", label: t("col.undisbursed"), align: "right", value: (a) => (a.undisbursed === null ? null : Number(a.undisbursed)),
            render: (a) => (a.undisbursed === null ? null : <span title={Number(a.undisbursed) < 0 ? t("profile.overDisbursed") : undefined}>{fmtAmount(Number(a.undisbursed), locale, a.currency ?? "")}{Number(a.undisbursed) < 0 ? " ⚠" : ""}</span>) },
          { key: "basis", label: t("col.basis"), value: (a) => a.disbursed_basis,
            render: (a) => (a.disbursed_basis ? <span title={a.disbursed_basis}>{a.disbursed_basis.startsWith("sum of dated") ? t("finance.basis.tx") : t("finance.basis.api")}{a.disbursed_as_of ? ` (${fmtDate(a.disbursed_as_of, locale)})` : ""}</span> : null) },
        ]} />
      </Card>
    </div>
  );
}

function moneyRows(m: Map<string, Money>) {
  return [...m.entries()].map(([k, v]) => [k, v.usd === null ? null : Math.round(v.usd), currencyLines(v.byCurrency, "en"), currencyLines(v.unconverted, "en"), v.n]);
}
