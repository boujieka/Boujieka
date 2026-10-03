"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

// Fixed categorical order (validated reference palette). Never cycled: callers cap at 5 series.
const SERIES = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)", "var(--series-5)"];
export const MAX_SERIES = SERIES.length;

const axisProps = {
  stroke: "var(--axis)",
  tick: { fill: "var(--subtle)", fontSize: 11 },
  tickLine: false,
} as const;

const tooltipStyle = {
  contentStyle: {
    background: "var(--surface)",
    border: "1px solid var(--border-strong)",
    borderRadius: 4,
    fontSize: 12,
    color: "var(--foreground)",
  },
  labelStyle: { color: "var(--muted)", marginBottom: 4 },
  itemStyle: { color: "var(--foreground)", padding: 0 },
};

const fmtDate = (t: number) =>
  new Date(t).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "2-digit", timeZone: "UTC" });

export interface TimeSeries {
  key: string;
  label: string;
  points: { date: string; value: number }[];
}

/** One measure over time, one or more series, one y-axis. */
export function TimeSeriesChart({
  series,
  unit,
  height = 260,
  ariaLabel,
}: {
  series: TimeSeries[];
  unit: string;
  height?: number;
  ariaLabel: string;
}) {
  const shown = series.slice(0, MAX_SERIES);
  // Merge into one row per date so the shared tooltip lists every series at that date.
  const rows = new Map<number, Record<string, number>>();
  for (const s of shown) {
    for (const p of s.points) {
      const t = Date.parse(`${p.date}T00:00:00Z`);
      const row = rows.get(t) ?? { t };
      row[s.key] = p.value;
      rows.set(t, row);
    }
  }
  const data = [...rows.values()].sort((a, b) => a.t - b.t);

  return (
    <div role="img" aria-label={ariaLabel} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid stroke="var(--grid)" vertical={false} />
          <XAxis
            dataKey="t"
            type="number"
            scale="time"
            domain={["dataMin", "dataMax"]}
            tickFormatter={fmtDate}
            {...axisProps}
          />
          <YAxis
            domain={["auto", "auto"]}
            width={56}
            tickFormatter={(v: number) => `${v.toFixed(2)}${unit}`}
            {...axisProps}
          />
          <Tooltip
            {...tooltipStyle}
            labelFormatter={(t) => fmtDate(Number(t))}
            formatter={(v, name) => [`${Number(v).toFixed(3)}${unit}`, name]}
            cursor={{ stroke: "var(--border-strong)" }}
          />
          {shown.length > 1 && (
            <Legend iconType="plainline" itemSorter={null} wrapperStyle={{ fontSize: 12, color: "var(--muted)" }} />
          )}
          {shown.map((s, i) => (
            <Line
              key={s.key}
              dataKey={s.key}
              name={s.label}
              stroke={SERIES[i]}
              strokeWidth={2}
              dot={{ r: 2.5, fill: SERIES[i], strokeWidth: 0 }}
              activeDot={{ r: 5, stroke: "var(--surface)", strokeWidth: 2 }}
              connectNulls
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Single-series bars over discrete dates (e.g. calculated bid-to-cover per auction). */
export function DateBarChart({
  points,
  label,
  unit,
  height = 200,
  ariaLabel,
}: {
  points: { date: string; value: number }[];
  label: string;
  unit: string;
  height?: number;
  ariaLabel: string;
}) {
  const data = points.map((p) => ({ d: p.date, v: p.value }));
  return (
    <div role="img" aria-label={ariaLabel} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }} barCategoryGap={2}>
          <CartesianGrid stroke="var(--grid)" vertical={false} />
          <XAxis dataKey="d" tickFormatter={(d: string) => fmtDate(Date.parse(`${d}T00:00:00Z`))} {...axisProps} />
          <YAxis width={56} tickFormatter={(v: number) => `${v.toFixed(1)}${unit}`} {...axisProps} />
          <Tooltip
            {...tooltipStyle}
            labelFormatter={(d) => fmtDate(Date.parse(`${d}T00:00:00Z`))}
            formatter={(v) => [`${Number(v).toFixed(2)}${unit}`, label]}
            cursor={{ fill: "var(--surface-2)" }}
          />
          <Bar dataKey="v" name={label} fill="var(--series-1)" radius={[4, 4, 0, 0]} maxBarSize={28} isAnimationActive={false} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

/** Auction yield by tenor (in years). Observed points joined by a line; no curve fitting. */
export function YieldCurveChart({
  points,
  height = 260,
  ariaLabel,
}: {
  points: { years: number; value: number; label: string; date: string }[];
  height?: number;
  ariaLabel: string;
}) {
  return (
    <div role="img" aria-label={ariaLabel} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={points} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid stroke="var(--grid)" vertical={false} />
          <XAxis
            dataKey="years"
            type="number"
            domain={[0, "dataMax"]}
            tickFormatter={(v: number) => (v < 1 ? `${Math.round(v * 12)}M` : `${v}Y`)}
            {...axisProps}
          />
          <YAxis domain={["auto", "auto"]} width={56} tickFormatter={(v: number) => `${v.toFixed(2)}%`} {...axisProps} />
          <Tooltip
            {...tooltipStyle}
            labelFormatter={(_, payload) => {
              const p = payload?.[0]?.payload as { label: string; date: string } | undefined;
              return p ? `${p.label} · auction ${p.date}` : "";
            }}
            formatter={(v) => [`${Number(v).toFixed(3)}%`, "WA yield"]}
            cursor={{ stroke: "var(--border-strong)" }}
          />
          <Line
            dataKey="value"
            name="WA yield"
            stroke="var(--series-1)"
            strokeWidth={2}
            dot={{ r: 4, fill: "var(--series-1)", stroke: "var(--surface)", strokeWidth: 2 }}
            activeDot={{ r: 6, stroke: "var(--surface)", strokeWidth: 2 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
