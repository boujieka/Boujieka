import { useMemo, useRef, useState } from "react";
import type { Run, Series } from "../api";
import { useApp } from "../context";
import { formatDate, formatValue, Key } from "../i18n";
import { href } from "../router";
import { LineChart } from "../components/LineChart";
import { Alert, errorText, Loading, RunBadge, useLoad, useMessage } from "../components/ui";

const HEADLINE = ["project_irr", "project_npv", "equity_irr_incl_grant", "min_dscr_repayment", "llcr_first_repayment",
  "senior_debt", "total_funding", "payback_years"];
const TABLES: Record<string, string[]> = {
  tab_ops: ["operations_flag", "operational_grids", "connections", "consumption_kwh", "gross_production_kwh", "diesel_production_kwh"],
  tab_pl: ["revenue", "opco_fees", "diesel_cost", "admin_costs", "total_opex", "ebitda", "depreciation", "ebit", "interest", "ebt", "npat"],
  tab_cash: ["cfads", "senior_interest", "senior_principal", "debt_service", "dscr", "dscr_below_target", "senior_debt_balance",
    "refi_debt_balance", "dsra_balance", "mmra_balance", "grid_purchases", "ongoing_capex", "tax_paid", "distributions", "project_cash_flow"],
  tab_bs: ["total_assets_current", "fixed_assets", "liabilities", "net_assets", "equity", "balance_check", "cash_balance"],
};
const FLOWS = new Set(["revenue", "opco_fees", "diesel_cost", "admin_costs", "total_opex", "ebitda", "depreciation", "ebit", "interest",
  "ebt", "npat", "cfads", "senior_interest", "senior_principal", "debt_service", "grid_purchases", "ongoing_capex", "tax_paid",
  "distributions", "project_cash_flow", "consumption_kwh", "gross_production_kwh", "diesel_production_kwh"]);

const SHORT: Record<string, [string, string]> = {
  revenue: ["Recettes", "Revenue"], total_opex: ["Charges", "Opex"], ebitda: ["EBE", "EBITDA"], cfads: ["CFADS", "CFADS"],
  debt_service: ["Service dette", "Debt service"], senior_debt_balance: ["Dette senior", "Senior debt"],
  refi_debt_balance: ["Dette refinancée", "Refi debt"], dsra_balance: ["DSRA", "DSRA"],
};

export function activeWindow(series: Record<string, Series>): [number, number] {
  const n = series.year.values.length;
  const idx = [...Array(n).keys()].filter((t) => series.operations_flag?.values[t] || series.construction_flag?.values[t]
    || (series.senior_debt_balance?.values[t] ?? 0) > 1e-6);
  return idx.length ? [idx[0], idx[idx.length - 1]] : [0, n - 1];
}

export function RunPage({ id }: { id: string }) {
  const { api, t, lang, labels, notify, compareRuns, setCompareRuns } = useApp();
  const msg = useMessage();
  const [run] = useLoad(() => api.getRun(id), [api, id]);
  const [version] = useLoad(() => (run ? api.version(run.version_id) : Promise.resolve(undefined)), [api, run?.version_id]);
  const [tab, setTab] = useState("tab_pl");
  const [allYears, setAllYears] = useState(false);
  const [busy, setBusy] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  const res = run?.result;
  const win = useMemo(() => (res?.series?.year ? activeWindow(res.series) : [0, 0]), [res]);
  if (!run || !version) return <Loading />;
  const r: Run = run;
  const kpis = res?.kpis ?? {};
  const series = res?.series ?? {};
  const [a, b] = allYears ? [0, (series.year?.values.length ?? 1) - 1] : win;
  const years = (series.year?.values.slice(a, b + 1) ?? []) as number[];
  const sl = (k: string) => (series[k]?.values ?? []).slice(a, b + 1);
  const short = (k: string) => SHORT[k]?.[lang === "fr" ? 0 : 1] ?? k;
  const sLabel = (k: string) => labels.series[k] ?? series[k]?.label ?? k;
  const kLabel = (k: string) => labels.kpis[k] ?? (k.startsWith("lot_") ? kpis[k]?.label : undefined) ?? kpis[k]?.label ?? k;
  const unitLabel = (u: string) => labels.units[u] ?? u;
  const target = version.assumptions?.debt?.target_dscr as number | undefined;

  async function download(kind: string, fn: () => Promise<void>) {
    setBusy(kind);
    try { await fn(); } catch (err) { notify(errorText(err), "error"); } finally { setBusy(""); }
  }

  return (
    <section>
      <p className="small"><a href={href("versions", version.id)}>← {version.scenario} · v{version.version}</a></p>
      <div className="row">
        <h1 className="grow">{t("results")} — {version.scenario} v{version.version}</h1>
        <RunBadge status={r.status} />
      </div>
      <p className="small muted">{formatDate(r.created_at, lang)} · {t("engineVersion")} {r.engine_version} · {r.duration_ms} ms
        · <span className="mono">{r.inputs_hash.slice(0, 12)}</span>
        {res?.options?.length ? ` · ${t("options")} : ${res.options.join(", ")}` : ""}</p>

      {r.status === "failed" ? <Alert kind="critical">{msg(r.error)}</Alert> : <>
        <div className="kpis">
          {HEADLINE.filter((k) => kpis[k]).map((k) => (
            <div className="kpi" key={k}>
              <div className="l">{kLabel(k)}</div>
              <div className="v">{formatValue(kpis[k].value, kpis[k].unit, lang)}</div>
              <div className="s">{kpis[k].derived ? t("derived") : kpis[k].source}</div>
            </div>
          ))}
        </div>

        <h2>{t("alerts")}</h2>
        {!res!.failed_checks.length && !res!.warnings.length ? <p className="muted">{t("none")}</p> : <>
          {res!.failed_checks.map((c) => <Alert key={c} kind="critical">{t("checks")} : {labels.checks[c] ?? c}</Alert>)}
          {res!.warnings.filter((w) => !w.startsWith("Workbook checks not passed")).map((w) => <Alert key={w} kind="warning">{msg(w)}</Alert>)}
        </>}

        <div className="card no-print">
          <h2 style={{ marginTop: 0 }}>{t("exports")}</h2>
          <div className="row">
            <button onClick={() => download("pdf", () => api.exportPdf(r.id, lang))} disabled={!!busy}>{busy === "pdf" ? t("downloading") : t("exportPdf")}</button>
            <button onClick={() => download("xlsx", () => api.exportXlsx(r.id, lang))} disabled={!!busy}>{busy === "xlsx" ? t("downloading") : t("exportXlsx")}</button>
            <button onClick={() => download("csv", () => api.exportCsv(r.id))} disabled={!!busy}>{busy === "csv" ? t("downloading") : t("exportCsv")}</button>
            {compareRuns.includes(r.id) ? <span className="small muted">{t("inCompare")}</span>
              : <button disabled={compareRuns.length >= 4} onClick={() => setCompareRuns([...compareRuns, r.id])}>{t("addToCompare")}</button>}
          </div>
          {r.status === "reconciled-engine" && <>
            <h3>{t("exportCb")}</h3>
            <p className="small muted">{t("exportCbNote")}</p>
            <input ref={fileRef} type="file" accept=".xlsm,.xlsx" hidden onChange={(e) => {
              const f = e.target.files?.[0];
              e.target.value = "";
              if (f) download("cb", () => api.exportCrossBoundary(r.id, f));
            }} />
            <button onClick={() => fileRef.current?.click()} disabled={!!busy}>{busy === "cb" ? t("downloading") : t("chooseFile")}</button>
          </>}
        </div>

        <div className="row"><h2 className="grow">{t("charts")}</h2>
          <label className="row small"><input type="checkbox" checked={allYears} onChange={(e) => setAllYears(e.target.checked)} />{t("allYears")}</label>
        </div>
        <p className="small muted">{t("amountsNote")}</p>
        <div className="charts">
          <LineChart title={t("chart_pl")} years={years} unit="currency" lang={lang} tableLabel={[t("showTable"), t("hideTable")]}
            series={["revenue", "total_opex", "ebitda"].map((k) => ({ key: k, label: short(k), values: k === "total_opex" ? sl(k).map((v) => (v === null ? null : -v)) : sl(k) }))} />
          <LineChart title={t("chart_ds")} years={years} unit="currency" lang={lang} tableLabel={[t("showTable"), t("hideTable")]}
            series={["cfads", "debt_service"].map((k) => ({ key: k, label: short(k), values: sl(k) }))} />
          <LineChart title={t("chart_debt")} years={years} unit="currency" lang={lang} tableLabel={[t("showTable"), t("hideTable")]}
            series={["senior_debt_balance", "refi_debt_balance", "dsra_balance"].map((k) => ({ key: k, label: short(k), values: sl(k) }))} />
          <LineChart title={t("chart_dscr")} years={years} unit="x" lang={lang} tableLabel={[t("showTable"), t("hideTable")]}
            reference={target ? { value: target, label: t("target") } : undefined}
            series={[{ key: "dscr", label: "DSCR", values: sl("dscr") }]} />
        </div>

        <h2>{t("financials")}</h2>
        <div className="tabs" role="tablist">
          {Object.keys(TABLES).map((k) => (
            <button key={k} role="tab" aria-selected={tab === k} onClick={() => setTab(k)}>{t(k as Key)}</button>
          ))}
        </div>
        <div className="card scroll-x" role="tabpanel">
          <table className="data">
            <thead><tr><th scope="col">{t("year")}</th><th scope="col" className="num">{t("total")}</th>
              {years.map((y) => <th key={y} scope="col" className="num">{y}</th>)}</tr></thead>
            <tbody>{TABLES[tab].filter((k) => series[k]).map((k) => (
              <tr key={k}>
                <th scope="row" style={{ fontWeight: 400 }}>{sLabel(k)}<div className="small muted">{unitLabel(series[k].unit)} · <span className="mono">{series[k].source}</span></div></th>
                <td className="num">{FLOWS.has(k) ? formatValue(series[k].values.reduce<number>((s, v) => s + (v ?? 0), 0), series[k].unit, lang) : ""}</td>
                {sl(k).map((v, i) => <td key={i} className="num">{formatValue(v, series[k].unit, lang)}</td>)}
              </tr>
            ))}</tbody>
          </table>
        </div>

        <h2>{t("indicators")}</h2>
        <div className="card scroll-x">
          <table className="data">
            <thead><tr><th scope="col">{t("indicators")}</th><th scope="col" className="num">{t("value")}</th><th scope="col">{t("unit")}</th><th scope="col">{t("source")}</th></tr></thead>
            <tbody>{Object.entries(kpis).map(([k, i]) => (
              <tr key={k}>
                <th scope="row" style={{ fontWeight: 400 }}>{kLabel(k)}</th>
                <td className="num">{formatValue(i.value, i.unit, lang)}</td>
                <td className="small">{unitLabel(i.unit)}</td>
                <td className="small">{i.source.startsWith("derived") ? t("derived") : <span className="mono">{i.source}</span>}
                  {i.derived && !i.source.startsWith("derived") && <> · {t("derived")}</>}{i.experimental && <> · <strong>{t("experimental")}</strong></>}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>

        <h2>{t("checks")}</h2>
        <div className="card">
          <table className="data">
            <tbody>{Object.entries(res!.checks).map(([k, v]) => {
              const bad = res!.failed_checks.includes(k);
              return (
                <tr key={k}>
                  <th scope="row" style={{ fontWeight: 400 }}>{labels.checks[k] ?? k}</th>
                  <td className="num mono">{formatValue(v, "", lang)}</td>
                  <td>{bad ? <span className="badge bad"><span aria-hidden="true">✕</span>{t("failed")}</span>
                    : <span className="badge good"><span aria-hidden="true">✓</span>{t("ok")}</span>}</td>
                </tr>
              );
            })}</tbody>
          </table>
        </div>
      </>}
    </section>
  );
}
