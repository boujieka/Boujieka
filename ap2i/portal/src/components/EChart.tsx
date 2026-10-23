import { useEffect, useRef, useState } from "react";
import type { ECharts, EChartsCoreOption as EChartsOption } from "echarts/core";
import { useI18n } from "../lib/i18n";
import { downloadCSV, type Cell } from "../lib/exporters";
import { Card } from "./ui";

export const PALETTE = ["#082B50", "#087F5B", "#D9A323", "#4C78A8", "#B5523B", "#6F4E9C", "#3A9BB4", "#8C8C3A", "#C27BA0", "#5C6B7A"];

export interface ChartData {
  header: string[];
  rows: Cell[][];
}

let echartsPromise: Promise<typeof import("echarts/core")> | null = null;
function loadECharts() {
  echartsPromise ??= import("../lib/echarts-setup").then((m) => m.default);
  return echartsPromise;
}

// Cheap change detection: formatter functions are ignored by JSON, data and labels are not.
const signature = (o: unknown, locale: string) => {
  try {
    return locale + JSON.stringify(o);
  } catch {
    return String(Math.random());
  }
};

/** ECharts card: tooltip/legend from the option, click handler, PNG (with source caption) and CSV export of the
 * underlying rows, and an accessible data table alternative. */
export function EChart({ title, option, data, onClick, height = 320, note, id, provenance }: {
  title: string; option: EChartsOption; data: ChartData; onClick?: (p: { name: string; seriesName?: string; data?: unknown; dataIndex: number }) => void;
  height?: number; note?: React.ReactNode; id?: string; provenance: string[];
}) {
  const { t, locale } = useI18n();
  const el = useRef<HTMLDivElement>(null);
  const chart = useRef<ECharts | null>(null);
  const clickRef = useRef(onClick);
  clickRef.current = onClick;
  const optRef = useRef(option);
  optRef.current = option;
  const lastSig = useRef("");
  const [err, setErr] = useState<string | null>(null);
  const base = { color: PALETTE, textStyle: { fontFamily: "Inter, system-ui, sans-serif" }, aria: { enabled: true, label: { description: title } } };

  useEffect(() => {
    let disposed = false;
    let ro: ResizeObserver | null = null;
    loadECharts().then((echarts) => {
      if (disposed || !el.current) return;
      chart.current = echarts.init(el.current, undefined, { renderer: "canvas" });
      (el.current as unknown as { __chart?: ECharts }).__chart = chart.current; // used by the end-to-end tests
      chart.current.on("click", (p) => clickRef.current?.(p as never));
      ro = new ResizeObserver(() => chart.current?.resize());
      ro.observe(el.current);
      lastSig.current = signature(optRef.current, locale);
      chart.current.setOption({ ...base, ...optRef.current }, true);
    }).catch((e) => setErr(String(e)));
    return () => {
      disposed = true;
      ro?.disconnect();
      chart.current?.dispose();
      chart.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const sig = signature(option, locale);
    if (!chart.current || sig === lastSig.current) return; // same data and labels: no redraw
    lastSig.current = sig;
    chart.current.setOption({ ...base, ...option }, true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [option, locale]);

  const fileBase = (id ?? title).replace(/[^\w-]+/g, "_").slice(0, 60);
  const png = () => {
    const c = chart.current;
    if (!c) return;
    // caption with source and date, only in the exported image
    c.setOption({ title: { text: title, subtext: `AP²I — ${provenance.slice(0, 2).join(" · ")}`.slice(0, 220), left: 8, top: 0,
      textStyle: { fontSize: 12 }, subtextStyle: { fontSize: 9 } }, grid: { top: 70 } });
    const url = c.getDataURL({ type: "png", pixelRatio: 2, backgroundColor: "#ffffff" });
    c.setOption({ ...base, ...optRef.current }, true);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${fileBase}.png`;
    a.click();
  };
  const csv = () => downloadCSV(fileBase, data.header, data.rows, [title, ...provenance]);

  return (
    <Card title={title} id={id} note={note} className="chart-card"
      actions={<>
        <button className="btn xs ghost" onClick={png} aria-label={`${t("common.exportPng")} — ${title}`}>{t("common.exportPng")}</button>
        <button className="btn xs ghost" onClick={csv} aria-label={`${t("common.exportCsv")} — ${title}`}>{t("common.exportCsv")}</button>
      </>}>
      {err ? <p className="muted">{err}</p> : null}
      <div ref={el} className="chart" style={{ height }} role="img" aria-label={title} data-testid={id ? `chart-${id}` : undefined} />
      <details className="chart-data">
        <summary>{t("common.showData")}</summary>
        <div className="table-wrap">
          <table>
            <caption className="sr-only">{title}</caption>
            <thead><tr>{data.header.map((h) => <th key={h} scope="col">{h}</th>)}</tr></thead>
            <tbody>{data.rows.slice(0, 200).map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{c === null || c === undefined ? "—" : String(c)}</td>)}</tr>)}</tbody>
          </table>
        </div>
      </details>
    </Card>
  );
}
