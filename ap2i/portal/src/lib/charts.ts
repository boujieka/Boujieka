import type { EChartsOption } from "echarts";
import type { Money } from "./agg";
import { escapeHtml, fmtAmount, fmtNum, moneyTooltip, type Locale } from "./format";

const axisLabel = (locale: Locale) => ({ formatter: (v: number) => fmtAmount(v, locale) });
const grid = { left: 8, right: 16, top: 36, bottom: 8, containLabel: true };

export function hbar(names: string[], values: (number | null)[], locale: Locale, opts: { money?: boolean; seriesName: string; tooltip?: (i: number) => string }): EChartsOption {
  return {
    grid,
    tooltip: { trigger: "item", formatter: (p: unknown) => {
      const i = (p as { dataIndex: number }).dataIndex;
      return opts.tooltip ? opts.tooltip(i) : `${escapeHtml(names[i])}<br/>${opts.money ? fmtAmount(values[i], locale, "USD") : fmtNum(values[i], locale)}`;
    } },
    xAxis: { type: "value", axisLabel: opts.money ? axisLabel(locale) : undefined },
    yAxis: { type: "category", data: names, inverse: true, axisLabel: { width: 150, overflow: "truncate" } },
    series: [{ type: "bar", name: opts.seriesName, data: values, barMaxWidth: 22 }],
  };
}

export function moneyLine(years: number[], series: { name: string; data: Money[] }[], locale: Locale, t: (k: string) => string, type: "line" | "bar" = "line"): EChartsOption {
  return {
    grid,
    legend: { top: 0 },
    tooltip: { trigger: "axis", formatter: (ps: unknown) => {
      const arr = ps as { seriesIndex: number; dataIndex: number; seriesName: string }[];
      const y = years[arr[0]?.dataIndex ?? 0];
      return `<b>${y}</b><br/>` + arr.map((p) => `<u>${escapeHtml(p.seriesName)}</u><br/>${moneyTooltip(series[p.seriesIndex].data[p.dataIndex], locale, t)}`).join("<br/>");
    } },
    xAxis: { type: "category", data: years.map(String) },
    yAxis: { type: "value", axisLabel: axisLabel(locale) },
    series: series.map((s) => ({
      type, name: s.name, smooth: false, barMaxWidth: 26,
      // a year without any transaction is a gap (null), not a zero
      data: s.data.map((m) => (m.usd === null ? null : Math.round(m.usd))),
      connectNulls: false,
    })),
  };
}

export function stacked(years: number[], groups: { name: string; data: (number | null)[] }[], locale: Locale): EChartsOption {
  return {
    grid,
    legend: { top: 0, type: "scroll" },
    tooltip: { trigger: "axis", valueFormatter: (v: unknown) => (v === null || v === undefined ? "—" : fmtAmount(v as number, locale, "USD")) },
    xAxis: { type: "category", data: years.map(String) },
    yAxis: { type: "value", axisLabel: axisLabel(locale) },
    series: groups.map((g) => ({ type: "bar", stack: "s", name: g.name, data: g.data, barMaxWidth: 28, emphasis: { focus: "series" } })),
  };
}

export function donut(items: { name: string; value: number }[], locale: Locale, money = false): EChartsOption {
  return {
    tooltip: { trigger: "item", formatter: (p: unknown) => {
      const x = p as { name: string; value: number; percent: number };
      return `${escapeHtml(x.name)}<br/>${money ? fmtAmount(x.value, locale, "USD") : fmtNum(x.value, locale)} (${fmtNum(x.percent, locale, 1)} %)`;
    } },
    legend: { type: "scroll", bottom: 0 },
    series: [{ type: "pie", radius: ["42%", "70%"], center: ["50%", "45%"], data: items, label: { show: false }, avoidLabelOverlap: true }],
  };
}
