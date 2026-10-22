import { useEffect, useRef, useState } from "react";
import type { ECharts, EChartsOption } from "echarts";
import { useI18n } from "../lib/i18n";
import { downloadCSV, type Cell } from "../lib/exporters";
import { Card } from "./ui";

export const PALETTE = ["#082B50", "#087F5B", "#D9A323", "#4C78A8", "#B5523B", "#6F4E9C", "#3A9BB4", "#8C8C3A", "#C27BA0", "#5C6B7A"];

export interface ChartData {
  header: string[];
  rows: Cell[][];
}

/** ECharts card with tooltip/legend from the option, click handler, PNG and CSV export of the underlying rows. */
export function EChart({ title, option, data, onClick, height = 320, note, id, provenance }: {
  title: string; option: EChartsOption; data: ChartData; onClick?: (p: { name: string; seriesName?: string; data?: unknown; dataIndex: number }) => void;
  height?: number; note?: React.ReactNode; id?: string; provenance: string[];
}) {
  const { t } = useI18n();
  const el = useRef<HTMLDivElement>(null);
  const chart = useRef<ECharts | null>(null);
  const clickRef = useRef(onClick);
  clickRef.current = onClick;
  const optRef = useRef(option);
  optRef.current = option;
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let disposed = false;
    let ro: ResizeObserver | null = null;
    import("echarts").then((echarts) => {
      if (disposed || !el.current) return;
      chart.current = echarts.init(el.current, undefined, { renderer: "canvas" });
      (el.current as unknown as { __chart?: ECharts }).__chart = chart.current; // used by the end-to-end tests
      chart.current.on("click", (p) => clickRef.current?.(p as never));
      ro = new ResizeObserver(() => chart.current?.resize());
      ro.observe(el.current);
      chart.current.setOption({ color: PALETTE, textStyle: { fontFamily: "Inter, system-ui, sans-serif" }, ...optRef.current }, true);
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
    chart.current?.setOption({ color: PALETTE, textStyle: { fontFamily: "Inter, system-ui, sans-serif" }, ...option }, true);
  }, [option]);

  const png = () => {
    const url = chart.current?.getDataURL({ type: "png", pixelRatio: 2, backgroundColor: "#ffffff" });
    if (!url) return;
    const a = document.createElement("a");
    a.href = url;
    a.download = `${(id ?? title).replace(/[^\w-]+/g, "_").slice(0, 60)}.png`;
    a.click();
  };
  const csv = () => downloadCSV(`${(id ?? title).replace(/[^\w-]+/g, "_").slice(0, 60)}`, data.header, data.rows, [title, ...provenance]);

  return (
    <Card title={title} id={id} note={note} className="chart-card"
      actions={<>
        <button className="btn xs ghost" onClick={png} aria-label={`${t("common.exportPng")} — ${title}`}>{t("common.exportPng")}</button>
        <button className="btn xs ghost" onClick={csv} aria-label={`${t("common.exportCsv")} — ${title}`}>{t("common.exportCsv")}</button>
      </>}>
      {err ? <p className="muted">{err}</p> : null}
      <div ref={el} className="chart" style={{ height }} role="img" aria-label={title} data-testid={id ? `chart-${id}` : undefined} />
    </Card>
  );
}
