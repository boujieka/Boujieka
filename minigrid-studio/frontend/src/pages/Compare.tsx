import { useMemo } from "react";
import type { Comparison } from "../api";
import { useApp } from "../context";
import { formatValue } from "../i18n";
import { href } from "../router";
import { LineChart } from "../components/LineChart";
import { Loading, RunBadge, StatusBadge, useLoad } from "../components/ui";

const CHARTS = ["revenue", "cfads", "dscr", "senior_debt_balance"];

export function ComparePage() {
  const { api, t, lang, labels, compareRuns, setCompareRuns } = useApp();
  const [data, , loading] = useLoad<Comparison | undefined>(
    () => (compareRuns.length >= 2 ? api.compare(compareRuns, lang) : Promise.resolve(undefined)), [api, compareRuns.join(","), lang]);

  const win = useMemo(() => {
    if (!data) return [0, 0];
    const n = data.years.length;
    const active = [...Array(n).keys()].filter((i) => Object.values(data.series).some((s) => s.values.some((v) => (v[i] ?? 0) !== 0)));
    return active.length ? [active[0], active[active.length - 1]] : [0, n - 1];
  }, [data]);

  // unique names: project shown when runs come from several projects, #n when the same version appears twice
  const name = (i: number) => {
    if (!data) return "";
    const r = data.runs[i];
    const multi = new Set(data.runs.map((x) => x.project)).size > 1;
    const base = `${multi ? `${r.project} · ` : ""}${r.scenario} v${r.version}`;
    const same = data.runs.filter((x) => x.project === r.project && x.scenario === r.scenario && x.version === r.version).length > 1;
    return same ? `${base} #${i + 1}` : base;
  };
  return (
    <section>
      <div className="row"><h1 className="grow">{t("compareTitle")}</h1>
        {compareRuns.length > 0 && <button onClick={() => setCompareRuns([])}>{t("clear")}</button>}</div>
      <p className="small muted">{t("compareHelp")}</p>
      {compareRuns.length < 2 ? <p className="muted">{compareRuns.length} / 2</p> : loading && !data ? <Loading /> : data && <>
        <div className="card scroll-x">
          <table className="data">
            <thead><tr><th scope="col" />
              {data.runs.map((r, i) => (
                <th key={r.run_id} scope="col">
                  <a href={href("runs", r.run_id)}>{r.project} — {r.scenario} v{r.version}</a>{i === 0 && <span className="badge" style={{ marginLeft: 6 }}>{t("base")}</span>}
                  <div className="row small" style={{ marginTop: 4 }}><RunBadge status={r.status} /><StatusBadge status={r.version_status} /></div>
                  <button className="link small" onClick={() => setCompareRuns(compareRuns.filter((x) => x !== r.run_id))}>{t("remove")}</button>
                </th>))}
            </tr></thead>
            <tbody>{Object.entries(data.kpis).map(([k, row]) => (
              <tr key={k}>
                <th scope="row" style={{ fontWeight: 400 }}>{row.label}<div className="small muted mono">{row.source.startsWith("derived") ? t("derived") : row.source}</div></th>
                {row.values.map((v, i) => (
                  <td key={i} className="num">
                    {formatValue(v, row.unit, lang)}
                    {i > 0 && row.deltas[i] !== null && row.deltas[i] !== 0 && (
                      <div className="small muted">{t("delta")} {row.deltas[i]! > 0 ? "+" : ""}{row.unit.startsWith("%")
                        ? `${formatValue(row.deltas[i]! * 100, "", lang)} pt` : formatValue(row.deltas[i], row.unit, lang)}</div>
                    )}
                  </td>
                ))}
              </tr>
            ))}</tbody>
          </table>
        </div>

        <h2>{t("charts")}</h2>
        <div className="charts">
          {CHARTS.filter((k) => data.series[k]).map((k) => (
            <LineChart key={k} title={labels.series[k] ?? data.series[k].label} unit={data.series[k].unit} lang={lang}
              years={data.years.slice(win[0], win[1] + 1)} tableLabel={[t("showTable"), t("hideTable")]}
              series={data.series[k].values.map((vals, i) => ({ key: `${i}`, label: name(i), values: vals.slice(win[0], win[1] + 1) }))} />
          ))}
        </div>

        <h2>{t("assumptionDiffs")}</h2>
        {data.assumption_diffs.length === 0 ? <p className="muted">{t("noDiffs")}</p> : (
          <div className="card scroll-x">
            <table className="data">
              <thead><tr><th scope="col" />{data.runs.map((_r, i) => <th key={i} scope="col" className="num">{name(i)}</th>)}</tr></thead>
              <tbody>{data.assumption_diffs.map((d) => (
                <tr key={d.path}>
                  <th scope="row" style={{ fontWeight: 400 }}>{d.label}<div className="small muted mono">{d.path}</div></th>
                  {d.values.map((v, i) => <td key={i} className="num">{v === null || v === undefined ? "—" : String(v)}</td>)}
                </tr>
              ))}</tbody>
            </table>
          </div>
        )}
      </>}
    </section>
  );
}
