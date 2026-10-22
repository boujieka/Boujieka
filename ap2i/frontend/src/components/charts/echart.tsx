"use client";

import ReactEChartsCore from "echarts-for-react/lib/core";
import { BarChart as EBar, LineChart as ELine } from "echarts/charts";
import { GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import * as echarts from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { useRouter } from "next/navigation";
import { fmtCompact, fmtNumber, type Locale } from "@/lib/format";
import { useI18n } from "../i18n-provider";

echarts.use([EBar, ELine, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer]);

export const PALETTE = ["#082B50", "#087F5B", "#D9A323", "#4F7CAC", "#8A96A3", "#A4262C", "#5BA88C"];

export interface Series {
  name: string;
  data: (number | null)[];
  color?: string;
  type?: "bar" | "line";
  stack?: string;
  /** Per-point link; falls back to the chart-level `links` for that category. */
  links?: (string | null)[];
}

export interface ChartProps {
  categories: string[];
  series: Series[];
  /** One drill-down link per category (index-aligned). */
  links?: (string | null)[];
  horizontal?: boolean;
  unit?: string;
  height?: number;
  ariaLabel: string;
}

function fmt(v: unknown, locale: Locale, unit?: string, compact = false): string {
  if (v === null || v === undefined || v === "-" || (typeof v === "number" && Number.isNaN(v))) return "—";
  const n = Number(v);
  return (compact ? fmtCompact(n, unit, locale) : fmtNumber(n, locale)) + (unit && !compact ? ` ${unit}` : "");
}

/** Bar/line chart whose elements are links to the underlying records (no decorative charts). */
export function Chart({ categories, series, links, horizontal = false, unit, height, ariaLabel }: ChartProps) {
  const { locale, d } = useI18n();
  const router = useRouter();
  const h = height ?? (horizontal ? Math.max(180, categories.length * 28 + 60) : 300);
  const valueAxis = { type: "value" as const, axisLabel: { formatter: (v: number) => fmt(v, locale, unit, true) }, splitLine: { lineStyle: { color: "#eef1f5" } } };
  const catAxis = { type: "category" as const, data: categories, axisLabel: { interval: 0, width: horizontal ? 130 : undefined, overflow: "truncate" as const, rotate: !horizontal && categories.length > 8 ? 45 : 0 } };
  const option = {
    color: PALETTE,
    animation: false,
    grid: { left: horizontal ? 140 : 60, right: 20, top: series.length > 1 ? 36 : 16, bottom: !horizontal && categories.length > 8 ? 56 : 28, containLabel: false },
    legend: series.length > 1 ? { top: 0, type: "scroll" as const } : undefined,
    tooltip: {
      trigger: "axis" as const,
      axisPointer: { type: "shadow" as const },
      valueFormatter: (v: unknown) => (v === null || v === undefined ? d.common.na : fmt(v, locale, unit)),
    },
    xAxis: horizontal ? valueAxis : catAxis,
    yAxis: horizontal ? { ...catAxis, inverse: true } : valueAxis,
    series: series.map((s) => ({
      name: s.name,
      type: s.type ?? "bar",
      stack: s.stack,
      data: s.data.map((v) => (v === null ? "-" : v)),
      itemStyle: s.color ? { color: s.color } : undefined,
      lineStyle: s.color ? { color: s.color } : undefined,
      connectNulls: false,
      barMaxWidth: 28,
      cursor: "pointer",
    })),
  };
  const onEvents = {
    click: (p: { dataIndex: number; seriesIndex: number }) => {
      const url = series[p.seriesIndex]?.links?.[p.dataIndex] ?? links?.[p.dataIndex];
      if (url) router.push(url);
    },
  };
  return (
    <div role="img" aria-label={ariaLabel} className="w-full min-w-0">
      <ReactEChartsCore echarts={echarts} option={option} onEvents={onEvents} style={{ height: h, width: "100%" }} notMerge lazyUpdate />
    </div>
  );
}
