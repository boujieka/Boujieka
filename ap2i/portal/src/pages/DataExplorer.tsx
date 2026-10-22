import { useMemo } from "react";
import type { EChartsOption } from "echarts";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { year } from "../lib/filters";
import { fmtAmount, fmtNum } from "../lib/format";
import { go, type Route } from "../lib/router";
import { EChart } from "../components/EChart";
import { FilterBar } from "../components/FilterBar";
import { DataTable } from "../components/DataTable";
import { Card, PageHead } from "../components/ui";

const DIMS = ["country", "sector", "partner", "instrument", "status", "approvalYear", "region", "txYear"] as const;
const MEASURES = ["projects", "agreements", "commitUsd", "txCommit", "txDisb"] as const;
type Dim = (typeof DIMS)[number];
type Measure = (typeof MEASURES)[number];

export function DataExplorer({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = route.filters;
  const sel = useSelection(f);
  const pick = <T extends string>(k: string, all: readonly T[], d: T | ""): T | "" => ((all as readonly string[]).includes(route.qs.get(k) ?? "") ? (route.qs.get(k) as T) : d);
  let measure = pick("measure", MEASURES, "projects") as Measure;
  let dim = pick("dim", DIMS, "sector") as Dim;
  let col = pick("col", DIMS, "") as Dim | "";
  // Transaction year only makes sense with transaction measures; project counts use the approval year.
  const txMeasure = measure === "txCommit" || measure === "txDisb";
  if (dim === "txYear" && !txMeasure) dim = "approvalYear";
  if (col === "txYear" && !txMeasure) col = "approvalYear";
  if (dim === col) col = "";
  const setQ = (patch: Record<string, string>) => go("/data", f, { measure, dim, col, ...patch });
  const projById = useMemo(() => new Map(s.projects.map((p) => [p.id, p])), [s]);

  const label = (d: Dim, k: string) => {
    if (k === "—") return "—";
    switch (d) {
      case "country": return names.country(k);
      case "sector": return names.sector(k);
      case "partner": return names.partner(k);
      case "instrument": return names.instrument(k);
      case "status": return t(`status.${k}`);
      default: return k;
    }
  };

  const cube = useMemo(() => {
    // value: number; undefined cell = no observation (shown "—"), 0 = observed zero
    const cells = new Map<string, Map<string, number>>();
    const put = (r: string, c: string, v: number) => {
      if (!cells.has(r)) cells.set(r, new Map());
      const row = cells.get(r)!;
      row.set(c, (row.get(c) ?? 0) + v);
    };
    const pKeys = (p: typeof s.projects[number], d: Dim): string[] => {
      switch (d) {
        case "country": return [p.country];
        case "sector": return [p.sector ?? "—"];
        case "partner": return p.partners.length ? p.partners : ["—"];
        case "instrument": return p.instruments.length ? p.instruments : ["—"];
        case "status": return [p.status];
        case "approvalYear": return [String(year(p.approval) ?? "—")];
        case "region": return [p.region ?? "—"];
        default: return ["—"];
      }
    };
    const aKeys = (a: typeof s.agreements[number], d: Dim): string[] => {
      const p = projById.get(a.project)!;
      if (d === "partner") return [a.partner ?? "—"];
      if (d === "instrument") return [a.instrument ?? "—"];
      if (d === "approvalYear") return [String(year(a.approval) ?? year(p.approval) ?? "—")];
      return pKeys(p, d);
    };
    if (measure === "projects") {
      for (const p of sel.projects) for (const r of pKeys(p, dim)) for (const c of col ? pKeys(p, col) : ["Σ"]) put(r, c, 1);
    } else if (measure === "agreements" || measure === "commitUsd") {
      for (const a of sel.agreements) {
        if (measure === "commitUsd" && a.committed_usd === null) continue;
        for (const r of aKeys(a, dim)) for (const c of col ? aKeys(a, col) : ["Σ"]) put(r, c, measure === "agreements" ? 1 : Number(a.committed_usd));
      }
    } else {
      const kind = measure === "txCommit" ? "commitment" : "disbursement";
      const agr = new Map(sel.agreements.map((a) => [a.id, a]));
      const fl = s.flows;
      for (let i = 0; i < fl.kind.length; i++) {
        if (fl.kind[i] !== kind || fl.usd[i] === null) continue;
        const a = agr.get(fl.agreement[i]);
        if (!a) continue;
        const y = fl.year[i];
        if ((f.y0 !== undefined && (y === null || y < f.y0)) || (f.y1 !== undefined && (y === null || y > f.y1))) continue;
        const keys = (d: Dim) => (d === "txYear" ? [String(y ?? "—")] : aKeys(a, d));
        for (const r of keys(dim)) for (const c of col ? keys(col) : ["Σ"]) put(r, c, Number(fl.usd[i]));
      }
    }
    const rows = [...cells.keys()].sort((a, b) => (dim.endsWith("Year") ? a.localeCompare(b) : [...cells.get(b)!.values()].reduce((x, y) => x + y, 0) - [...cells.get(a)!.values()].reduce((x, y) => x + y, 0)));
    const cols = [...new Set([...cells.values()].flatMap((m) => [...m.keys()]))].sort();
    return { cells, rows, cols };
  }, [sel, s, measure, dim, col, projById, f.y0, f.y1]);

  const money = measure === "commitUsd" || measure === "txCommit" || measure === "txDisb";
  const fmt = (v: number | undefined) => (v === undefined ? "—" : money ? fmtAmount(v, locale, "USD") : fmtNum(v, locale));
  const option: EChartsOption = {
    grid: { left: 8, right: 16, top: 36, bottom: 8, containLabel: true }, legend: { top: 0, type: "scroll" },
    tooltip: { trigger: "axis", valueFormatter: (v: unknown) => (v === null || v === undefined ? "—" : fmt(v as number)) },
    xAxis: { type: "category", data: cube.rows.map((r) => label(dim, r)), axisLabel: { rotate: cube.rows.length > 8 ? 35 : 0 } },
    yAxis: { type: "value", axisLabel: { formatter: (v: number) => (money ? fmtAmount(v, locale) : fmtNum(v, locale)) } },
    series: cube.cols.map((c) => ({ type: "bar", stack: "x", name: c === "Σ" ? t(`measure.${measure}`) : label(col as Dim, c),
      data: cube.rows.map((r) => cube.cells.get(r)?.get(c) ?? null) })),
  };
  type Row = { key: string };
  const tableRows: Row[] = cube.rows.map((key) => ({ key }));
  const prov = [s.meta.scope, `snapshot ${s.meta.generated_at}`, `measure=${measure} rows=${dim} cols=${col || "-"}`, t("data.missingNote"), `filters: ${window.location.hash}`];

  return (
    <div>
      <PageHead title={t("data.title")} subtitle={t("data.missingNote")} />
      <FilterBar route={route} undated={sel.undatedExcluded} />
      <Card>
        <div className="fb-row">
          <label><span>{t("data.measure")}</span>
            <select value={measure} onChange={(e) => setQ({ measure: e.target.value })} data-testid="dx-measure">{MEASURES.map((m) => <option key={m} value={m}>{t(`measure.${m}`)}</option>)}</select></label>
          <label><span>{t("data.rows")}</span>
            <select value={dim} onChange={(e) => setQ({ dim: e.target.value })} data-testid="dx-dim">{DIMS.filter((d) => d !== "txYear" || txMeasure).map((d) => <option key={d} value={d}>{t(`dim.${d}`)}</option>)}</select></label>
          <label><span>{t("data.cols")}</span>
            <select value={col} onChange={(e) => setQ({ col: e.target.value })}><option value="">—</option>{DIMS.filter((d) => d !== dim && (d !== "txYear" || txMeasure)).map((d) => <option key={d} value={d}>{t(`dim.${d}`)}</option>)}</select></label>
        </div>
        <p className="muted small">{money ? t("money.note") : ""} {measure === "commitUsd" ? `${sel.agreements.filter((a) => a.committed !== null && a.committed_usd === null).length} ${t("common.notConverted")}` : ""}</p>
      </Card>
      <EChart id="dx" title={`${t("measure." + measure)} × ${t("dim." + dim)}${col ? " × " + t("dim." + col) : ""}`} option={option} provenance={prov} height={380}
        data={{ header: [dim, ...cube.cols], rows: cube.rows.map((r) => [r, ...cube.cols.map((c) => cube.cells.get(r)?.get(c) ?? null)]) }} />
      <Card title={t("data.table")}>
        <DataTable<Row> rows={tableRows} rowKey={(r) => r.key} pageSize={50} exportName="ap2i_data_explorer" provenance={prov} testId="dx-table"
          columns={[
            { key: "k", label: t(`dim.${dim}`), value: (r) => label(dim, r.key) },
            ...cube.cols.map((c) => ({ key: `c_${c}`, label: c === "Σ" ? t(`measure.${measure}`) : label(col as Dim, c), align: "right" as const,
              value: (r: Row) => cube.cells.get(r.key)?.get(c) ?? null, render: (r: Row) => fmt(cube.cells.get(r.key)?.get(c)) })),
          ]} />
      </Card>
    </div>
  );
}
