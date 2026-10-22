import { useMemo } from "react";
import type { EChartsOption } from "echarts";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { countBy, disbursementRate, elapsedRatio, maxLevel, slippageDays } from "../lib/agg";
import { escapeHtml, fmtNum, fmtPct } from "../lib/format";
import { go, href, type Route } from "../lib/router";
import { donut, hbar } from "../lib/charts";
import { LEVELS } from "../lib/filters";
import { EChart } from "../components/EChart";
import { FilterBar } from "../components/FilterBar";
import { DataTable } from "../components/DataTable";
import { Card, LevelBadge, PageHead } from "../components/ui";
import type { AgreementRow, AlertItem } from "../lib/types";

const SEV: Record<string, number> = { critical_attention: 4, high_attention: 3, watch: 2, information: 1 };
const SEV_COLOR: Record<number, string> = { 0: "#9aa7b4", 1: "#087F5B", 2: "#4C78A8", 3: "#D9A323", 4: "#B42318" };

export function Performance({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = route.filters;
  const sel = useSelection(f);
  const today = useMemo(() => new Date(s.meta.generated_at), [s]);
  const prov = [s.meta.scope, `snapshot ${s.meta.generated_at}`, `filters: ${window.location.hash}`, t("perf.disclaimer")];
  const agrByProject = useMemo(() => {
    const m = new Map<number, AgreementRow[]>();
    for (const a of s.agreements) m.set(a.project, [...(m.get(a.project) ?? []), a]);
    return m;
  }, [s]);
  const ps = sel.projects;

  const byStatus = countBy(ps, (p) => p.status);
  const stCodes = [...byStatus.keys()];
  const slip = ps.map((p) => ({ p, d: slippageDays(p) })).filter((x) => x.d !== null) as { p: typeof ps[number]; d: number }[];
  const bins = [[-Infinity, 0, "≤ 0"], [1, 180, "1–180"], [181, 365, "181–365"], [366, 730, "1–2 ans"], [731, Infinity, "> 2 ans"]] as const;
  const slipBins = bins.map(([a, b, l]) => ({ l: locale === "en" ? l.replace("ans", "yrs") : l, n: slip.filter((x) => x.d >= a && x.d <= b).length }));
  const rates = ps.map((p) => ({ p, r: disbursementRate(agrByProject.get(p.id) ?? []) }));
  const EDGES = [0, 0.2, 0.4, 0.6, 0.8];
  const rateBins = EDGES.map((lo, i) => {
    const hi = i === EDGES.length - 1 ? Infinity : EDGES[i + 1];
    return { l: i === EDGES.length - 1 ? "≥ 80 %" : `${lo * 100}–${hi * 100} %`, n: rates.filter((x) => x.r.value !== null && x.r.value >= lo && x.r.value < hi).length };
  });
  const rateNA = rates.filter((x) => x.r.value === null).length;
  const phys = ps.filter((p) => p.physical_progress !== null);
  const byOp = countBy(ps, (p) => p.operational_status);
  const opCodes = [...byOp.keys()];
  const cnotop = ps.filter((p) => (p.status === "completed" || p.status === "closed") && p.operational_status !== "operational");
  const alerts = useMemo(() => s.alerts.items.filter((a) => sel.ids.has(a.project.id) && (!f.alert || f.alert === "any" || a.level === f.alert)), [s, sel, f.alert]);
  const byRule = countBy(alerts, (a) => a.rule_code);
  const ruleCodes = [...byRule.keys()];

  // Risk matrix: documented indicators only (disbursement rate AND elapsed share both available)
  const points = ps.map((p) => {
    const r = rates.find((x) => x.p.id === p.id)!.r.value;
    const e = elapsedRatio(p, today);
    const l = maxLevel(p);
    return { p, r, e, sev: l ? SEV[l] : 0 };
  }).filter((x) => x.r !== null && x.e !== null);
  const matrix: EChartsOption = {
    grid: { left: 8, right: 24, top: 30, bottom: 30, containLabel: true },
    tooltip: { trigger: "item", formatter: (p: unknown) => {
      const x = points[(p as { dataIndex: number }).dataIndex];
      return `<b>${escapeHtml(x.p.ref)}</b><br/>${escapeHtml(x.p.title.slice(0, 90))}<br/>${escapeHtml(t("col.rate"))}: ${fmtPct(x.r, locale)}<br/>elapsed: ${fmtPct(x.e, locale)}`;
    } },
    xAxis: { type: "value", name: locale === "fr" ? "Temps écoulé" : "Time elapsed", nameLocation: "middle", nameGap: 22, min: 0, max: 1, axisLabel: { formatter: (v: number) => `${Math.round(v * 100)} %` } },
    yAxis: { type: "value", name: t("col.rate"), min: 0, max: (v: { max: number }) => Math.max(1, Math.ceil(v.max * 10) / 10), axisLabel: { formatter: (v: number) => `${Math.round(v * 100)} %` } },
    series: [{
      type: "scatter", data: points.map((x) => ({ value: [Math.min(1, x.e!), x.r], itemStyle: { color: SEV_COLOR[x.sev], opacity: 0.8 } })),
      symbolSize: (_: unknown, p: { dataIndex: number }) => 7 + points[p.dataIndex].sev * 4,
      markArea: { silent: true, itemStyle: { color: "rgba(180,35,24,0.06)" }, data: [[{ xAxis: 0.5, yAxis: 0 }, { xAxis: 1, yAxis: 0.3 }]] },
    }],
  };

  return (
    <div>
      <PageHead title={t("perf.title")} subtitle={t("perf.disclaimer")} />
      <FilterBar route={route} undated={sel.undatedExcluded} />
      <div className="grid-2">
        <EChart id="p1" title={t("perf.status")} provenance={prov} option={donut(stCodes.map((c) => ({ name: t(`status.${c}`), value: byStatus.get(c)! })), locale)}
          data={{ header: ["status", "projects"], rows: stCodes.map((c) => [c, byStatus.get(c)!]) }} onClick={(p) => go("/projects", { ...f, status: [stCodes[p.dataIndex]] })} />
        <EChart id="p2" title={t("perf.matrix")} provenance={prov} option={matrix} height={360}
          note={t("perf.matrixNote", { n: points.length })}
          data={{ header: ["project", "disbursement_rate", "elapsed_share", "max_alert_severity"], rows: points.map((x) => [x.p.ref, x.r, x.e, x.sev]) }}
          onClick={(p) => go(`/project/${points[p.dataIndex].p.ref}`, f)} />
        <EChart id="p3" title={t("perf.delays")} provenance={prov} option={hbar(slipBins.map((b) => b.l), slipBins.map((b) => b.n), locale, { seriesName: t("common.projects") })}
          note={`${slip.length} / ${ps.length} ${t("common.projects")} — ${locale === "fr" ? "fin révisée − fin initiale, quand les deux dates sont publiées" : "revised − original end, when both dates are published"}`}
          data={{ header: ["project", "slippage_days"], rows: slip.map((x) => [x.p.ref, x.d]) }} />
        <EChart id="p4" title={t("perf.execution")} provenance={prov} option={hbar(rateBins.map((b) => b.l), rateBins.map((b) => b.n), locale, { seriesName: t("common.projects") })}
          note={`${t("common.na")} : ${rateNA} ${t("common.projects")} (${locale === "fr" ? "montants manquants, plusieurs devises ou garantie" : "missing amounts, several currencies or guarantee"})`}
          data={{ header: ["project", "disbursement_rate", "reason_if_missing"], rows: rates.map((x) => [x.p.ref, x.r.value, x.r.reason]) }} />
        <EChart id="p5" title={t("perf.operational")} provenance={prov} option={donut(opCodes.map((c) => ({ name: t(`op.${c}`), value: byOp.get(c)! })), locale)}
          note={`${t("perf.cnotop")} : ${cnotop.length}`}
          data={{ header: ["operational_status", "projects"], rows: opCodes.map((c) => [c, byOp.get(c)!]) }} />
        <EChart id="p6" title={t("perf.rules")} provenance={prov} option={hbar(ruleCodes.map((c) => t(`rule.${c}`)), ruleCodes.map((c) => byRule.get(c)!), locale, { seriesName: t("col.alerts") })}
          data={{ header: ["rule", "alerts"], rows: ruleCodes.map((c) => [c, byRule.get(c)!]) }} height={360} />
      </div>
      <div className="grid-2">
        <Card title={t("perf.physical")}>
          {phys.length ? <ul>{phys.map((p) => <li key={p.id}><a href={href(`/project/${p.ref}`, f)}>{p.ref}</a> — {p.physical_progress} %</li>)}</ul> : <p className="muted">{t("perf.physicalNA")}</p>}
        </Card>
        <Card title={t("perf.availability")}>
          <dl className="dl">
            <div><dt>{t("col.rate")}</dt><dd>{fmtNum(ps.length - rateNA, locale)} / {fmtNum(ps.length, locale)}</dd></div>
            <div><dt>{t("perf.delays")}</dt><dd>{fmtNum(slip.length, locale)} / {fmtNum(ps.length, locale)}</dd></div>
            <div><dt>{t("perf.physical")}</dt><dd>{fmtNum(phys.length, locale)} / {fmtNum(ps.length, locale)}</dd></div>
            <div><dt>{t("profile.operational")}</dt><dd>{fmtNum(ps.filter((p) => p.operational_status !== "unknown").length, locale)} / {fmtNum(ps.length, locale)}</dd></div>
            <div><dt>{t("profile.rating")}</dt><dd>{fmtNum(ps.filter((p) => p.latest_rating).length, locale)} / {fmtNum(ps.length, locale)}</dd></div>
            <div><dt>{t("profile.amendments")}</dt><dd>{t("common.na")}</dd></div>
          </dl>
        </Card>
      </div>
      <Card title={`${t("perf.alertList")} (${alerts.length})`}>
        <div className="seg" style={{ marginBottom: 8 }}>
          {LEVELS.map((l) => <a key={l} className={`btn xs ${f.alert === l ? "" : "ghost"}`} href={href("/performance", { ...f, alert: f.alert === l ? undefined : l })}>{t(`level.${l}`)} ({alerts.filter((a) => a.level === l).length})</a>)}
        </div>
        <DataTable<AlertItem> rows={alerts} rowKey={(a) => a.alert_id} exportName="ap2i_alerts" provenance={prov} testId="alerts-table" columns={[
          { key: "level", label: t("col.level"), value: (a) => SEV[a.level], render: (a) => <LevelBadge level={a.level} /> },
          { key: "rule", label: t("col.rule"), value: (a) => t(`rule.${a.rule_code}`) },
          { key: "project", label: t("common.project"), value: (a) => a.project.ap2i_id, render: (a) => <a href={href(`/project/${a.project.ap2i_id}`, f)} title={a.project.title}>{a.project.ap2i_id}</a> },
          { key: "obs", label: t("col.observed"), value: (a) => a.observed_value },
          { key: "thr", label: t("col.threshold"), value: (a) => a.threshold },
          { key: "src", label: t("perf.evidence"), value: (a) => a.source },
          { key: "asof", label: t("col.asOf"), value: (a) => a.as_of },
          { key: "partner", label: t("col.partners"), value: (a) => (s.projects.find((p) => p.id === a.project.id)?.partners ?? []).map((c) => names.partner(c)).join(", ") },
        ]} />
      </Card>
    </div>
  );
}
