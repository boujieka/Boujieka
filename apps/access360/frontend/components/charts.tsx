"use client";

// Charts follow the dataviz rules: one y axis per chart, thin marks, recessive grid, legend for 2+ series,
// text in ink colours (never the series colour), hover tooltips on every mark.

import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import type { ReactNode } from "react";
import { axisCompact, num, type Loc } from "@/lib/format";

export const SERIES = ["#2a78d6", "#eb6834", "#1baf7a"] as const;
const DOWN = "#e34948";
const UP = "#2a78d6";
const GRID = "#e6e9ee";
const AXIS = "#6b7684";
const INK = "#0d1b2e";
const INK2 = "#4f5b6b";

const axisProps = { stroke: GRID, tick: { fill: AXIS, fontSize: 11 }, tickLine: false } as const;
const tooltipStyle = {
  contentStyle: { borderRadius: 6, border: "1px solid #dfe3e9", fontSize: 12, color: INK, boxShadow: "0 4px 12px rgba(13,27,46,0.08)" },
  labelStyle: { color: INK, fontWeight: 600, marginBottom: 4 },
  itemStyle: { color: INK2, padding: 0 },
};
const legendProps = {
  iconType: "plainline" as const,
  iconSize: 14,
  wrapperStyle: { fontSize: 12, color: INK2, paddingTop: 4 },
  formatter: (v: string) => <span style={{ color: INK2 }}>{v}</span>,
};

export function ChartFrame({ title, subtitle, children, height = 260, testId }: { title: string; subtitle?: string; children: ReactNode; height?: number; testId?: string }) {
  return (
    <figure className="rounded-lg border border-border bg-surface p-4" data-testid={testId}>
      <figcaption className="mb-3">
        <div className="text-sm font-semibold text-navy-900">{title}</div>
        {subtitle ? <div className="text-xs text-subtle-foreground">{subtitle}</div> : null}
      </figcaption>
      <div style={{ height }} className="w-full">
        {children}
      </div>
    </figure>
  );
}

export interface SeriesDef {
  key: string;
  name: string;
}

/** Multi series line chart sharing one unit (one axis). */
export function LinesChart({
  data,
  xKey,
  series,
  locale,
  valueFormat,
  refLine,
  yDomain,
}: {
  data: Record<string, unknown>[];
  xKey: string;
  series: SeriesDef[];
  locale: Loc;
  valueFormat: (v: number) => string;
  refLine?: { y: number; label: string };
  yDomain?: [number | "auto" | "dataMin", number | "auto" | "dataMax"];
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: 4 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey={xKey} {...axisProps} minTickGap={16} />
        <YAxis {...axisProps} axisLine={false} width={56} tickFormatter={axisCompact(locale)} domain={yDomain ?? ["auto", "auto"]} />
        <Tooltip {...tooltipStyle} formatter={(v) => (typeof v === "number" ? valueFormat(v) : String(v ?? "–"))} />
        {series.length > 1 ? <Legend {...legendProps} /> : null}
        {refLine ? (
          <ReferenceLine
            y={refLine.y}
            stroke="#a12b2b"
            strokeDasharray="4 3"
            strokeWidth={1}
            label={{ value: refLine.label, position: "insideTopRight", fill: INK2, fontSize: 11 }}
          />
        ) : null}
        {series.map((s, i) => (
          <Line key={s.key} type="monotone" dataKey={s.key} name={s.name} stroke={SERIES[i % SERIES.length]} strokeWidth={2} dot={false} activeDot={{ r: 4 }} connectNulls={false} isAnimationActive={false} />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

/** Single series vertical bar chart. */
export function BarsChart({ data, xKey, yKey, name, locale, valueFormat }: { data: Record<string, unknown>[]; xKey: string; yKey: string; name: string; locale: Loc; valueFormat: (v: number) => string }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: 4 }} barCategoryGap={2}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey={xKey} {...axisProps} minTickGap={8} />
        <YAxis {...axisProps} axisLine={false} width={56} tickFormatter={axisCompact(locale)} />
        <Tooltip {...tooltipStyle} cursor={{ fill: "rgba(13,27,46,0.04)" }} formatter={(v) => (typeof v === "number" ? valueFormat(v) : String(v ?? "–"))} />
        <Bar dataKey={yKey} name={name} fill={SERIES[0]} radius={[4, 4, 0, 0]} maxBarSize={28} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

/** Horizontal single series bar chart for categories (e.g. projects by country). */
export function HBarsChart({ data, catKey, valKey, name, locale }: { data: Record<string, unknown>[]; catKey: string; valKey: string; name: string; locale: Loc }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} layout="vertical" margin={{ top: 0, right: 28, bottom: 0, left: 4 }}>
        <CartesianGrid stroke={GRID} horizontal={false} />
        <XAxis type="number" {...axisProps} allowDecimals={false} />
        <YAxis type="category" dataKey={catKey} {...axisProps} axisLine={false} width={170} />
        <Tooltip {...tooltipStyle} cursor={{ fill: "rgba(13,27,46,0.04)" }} formatter={(v) => (typeof v === "number" ? num(v, locale) : String(v))} />
        <Bar dataKey={valKey} name={name} fill={SERIES[0]} radius={[0, 4, 4, 0]} maxBarSize={18} isAnimationActive={false}>
          <LabelList dataKey={valKey} position="right" fill={INK2} fontSize={11} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export interface TornadoDatum {
  label: string;
  base: number;
  down: [number, number] | null;
  up: [number, number] | null;
  low: number | null;
  high: number | null;
}

/** Tornado: bars from the base case to the lowest and highest case values of each driver. */
export function TornadoChart({ data, base, locale, valueFormat, downName, upName, baseName }: { data: TornadoDatum[]; base: number; locale: Loc; valueFormat: (v: number) => string; downName: string; upName: string; baseName: string }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 16, bottom: 0, left: 4 }} barGap={-14} barCategoryGap={4}>
        <CartesianGrid stroke={GRID} horizontal={false} />
        <XAxis type="number" {...axisProps} tickFormatter={axisCompact(locale)} domain={["auto", "auto"]} />
        <YAxis type="category" dataKey="label" {...axisProps} axisLine={false} width={128} />
        <Tooltip
          {...tooltipStyle}
          cursor={{ fill: "rgba(13,27,46,0.04)" }}
          formatter={(v, n) => {
            if (Array.isArray(v)) {
              const end = n === downName ? Math.min(...(v as number[])) : Math.max(...(v as number[]));
              return [valueFormat(end), n];
            }
            return [String(v), n];
          }}
        />
        <Legend {...legendProps} iconType="square" />
        <ReferenceLine x={base} stroke={INK} strokeWidth={1} label={{ value: baseName, position: "top", fill: INK2, fontSize: 11 }} />
        <Bar dataKey="down" name={downName} fill={DOWN} barSize={14} radius={2} isAnimationActive={false} />
        <Bar dataKey="up" name={upName} fill={UP} barSize={14} radius={2} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

/** Scatter of options: x = months to electrify, y = LCOE. Direct labels with the option code. */
export function OptionsScatter({ data, locale, xName, yName }: { data: { code: string; months: number; lcoe: number; name: string }[]; locale: Loc; xName: string; yName: string }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ScatterChart margin={{ top: 16, right: 24, bottom: 16, left: 4 }}>
        <CartesianGrid stroke={GRID} />
        <XAxis type="number" dataKey="months" name={xName} {...axisProps} label={{ value: xName, position: "insideBottom", offset: -8, fill: INK2, fontSize: 11 }} domain={[0, "auto"]} />
        <YAxis type="number" dataKey="lcoe" name={yName} {...axisProps} axisLine={false} width={56} tickFormatter={axisCompact(locale)} domain={[0, "auto"]} />
        <ZAxis range={[80, 80]} />
        <Tooltip
          {...tooltipStyle}
          cursor={{ strokeDasharray: "3 3", stroke: AXIS }}
          formatter={(v, n) => [typeof v === "number" ? num(v, locale, n === yName ? 1 : 0) : String(v), n]}
          labelFormatter={() => ""}
        />
        <Scatter data={data} fill={SERIES[0]} stroke="#ffffff" strokeWidth={2} isAnimationActive={false}>
          <LabelList dataKey="code" position="top" fill={INK} fontSize={11} fontWeight={600} />
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  );
}
