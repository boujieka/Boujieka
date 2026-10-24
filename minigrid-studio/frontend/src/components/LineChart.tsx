import { useMemo, useState } from "react";
import { formatShort, formatValue, Lang } from "../i18n";

export interface ChartSeries { key: string; label: string; values: (number | null)[] }

const COLORS = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)"];
const W = 640, H = 250, M = { l: 52, r: 96, t: 10, b: 26 };

export function niceTicks(lo: number, hi: number, n = 5): number[] {
  if (!Number.isFinite(lo) || !Number.isFinite(hi)) return [0, 1];
  if (hi === lo) hi = lo + 1;
  const raw = (hi - lo) / n;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((s) => s * mag).find((s) => s >= raw) ?? 10 * mag;
  const ticks = [Math.floor(lo / step) * step];
  while (ticks[ticks.length - 1] < hi - 1e-12) ticks.push(+(ticks[ticks.length - 1] + step).toPrecision(12));
  if (ticks.length === 1) ticks.push(ticks[0] + step);
  return ticks.map((v) => +v.toPrecision(12));
}

/** One-axis line chart: hover/keyboard crosshair with tooltip, legend, direct end labels, data table. */
export function LineChart(props: {
  title: string; years: number[]; series: ChartSeries[]; unit: string; lang: Lang;
  reference?: { value: number; label: string }; tableLabel: [string, string];
  /** values above the cap are drawn at the cap and labelled "off scale" (the data table keeps the real value) */
  cap?: number; offScaleLabel?: string;
}) {
  const { title, years, unit, lang, reference, cap } = props;
  const series = useMemo(() => (cap === undefined ? props.series : props.series.map((s) => ({
    ...s, values: s.values.map((v) => (v !== null && v > cap ? cap : v)),
  }))), [props.series, cap]);
  const offScale = cap === undefined ? [] : props.series.flatMap((s) => s.values.map((v, i) => ({ v, i })).filter((p) => p.v !== null && p.v > cap));
  const [hover, setHover] = useState<number | null>(null);
  const [showTable, setShowTable] = useState(false);
  const n = years.length;
  const pw = W - M.l - M.r, ph = H - M.t - M.b;

  const { ticks, x, y } = useMemo(() => {
    const vals = series.flatMap((s) => s.values.filter((v): v is number => v !== null && Number.isFinite(v)));
    if (reference) vals.push(reference.value);
    const lo = Math.min(0, ...vals), hi = Math.max(0, ...vals);
    const tk = niceTicks(lo, hi);
    const [a, b] = [tk[0], tk[tk.length - 1]];
    return {
      ticks: tk,
      x: (i: number) => M.l + (pw * i) / Math.max(n - 1, 1),
      y: (v: number) => M.t + ph - (ph * (v - a)) / (b - a || 1),
    };
  }, [series, reference, n, pw, ph]);

  const paths = series.map((s) => {
    let d = "";
    let pen = false;
    s.values.forEach((v, i) => {
      if (v === null || !Number.isFinite(v)) { pen = false; return; }
      d += `${pen ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`;
      pen = true;
    });
    return d;
  });

  // direct labels at line ends, nudged apart (identity is never colour alone)
  const endLabels: { y: number; label: string; color: string; key: string }[] = [];
  if (series.length <= 4) {
    series.forEach((s, k) => {
      const last = s.values.map((v, i) => (v === null ? -1 : i)).filter((i) => i >= 0).pop();
      if (last === undefined) return;
      let ly = y(s.values[last] as number);
      while (endLabels.some((o) => Math.abs(o.y - ly) < 12)) ly += 12;
      endLabels.push({ y: ly, label: s.label, color: COLORS[k % COLORS.length], key: s.key });
    });
  }

  const step = Math.max(1, Math.round(n / 10));
  const move = (clientX: number, rect: DOMRect) => {
    const px = ((clientX - rect.left) / rect.width) * W;
    const i = Math.round(((px - M.l) / pw) * (n - 1));
    setHover(Math.min(n - 1, Math.max(0, i)));
  };

  return (
    <figure className="chart" style={{ margin: 0 }}>
      <h3>{title}</h3>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={title} tabIndex={0}
        onMouseMove={(e) => move(e.clientX, (e.currentTarget as SVGSVGElement).getBoundingClientRect())}
        onMouseLeave={() => setHover(null)}
        onFocus={() => setHover((h) => h ?? 0)} onBlur={() => setHover(null)}
        onKeyDown={(e) => {
          if (e.key === "ArrowRight") setHover((h) => Math.min(n - 1, (h ?? -1) + 1));
          if (e.key === "ArrowLeft") setHover((h) => Math.max(0, (h ?? 1) - 1));
        }}>
        {ticks.map((tv) => (
          <g key={tv}>
            <line x1={M.l} x2={M.l + pw} y1={y(tv)} y2={y(tv)} stroke={tv === 0 ? "var(--axis)" : "var(--border)"} strokeWidth={tv === 0 ? 1 : 0.6} />
            <text x={M.l - 6} y={y(tv) + 3.5} textAnchor="end" fontSize="10" fill="var(--muted)">
              {unit.startsWith("%") ? formatValue(tv, unit, lang) : formatShort(tv, lang)}
            </text>
          </g>
        ))}
        {years.map((yr, i) => (i % step === 0 ? (
          <text key={yr} x={x(i)} y={H - 8} textAnchor="middle" fontSize="10" fill="var(--muted)">{yr}</text>
        ) : null))}
        {reference && (
          <g>
            <line x1={M.l} x2={M.l + pw} y1={y(reference.value)} y2={y(reference.value)} stroke="var(--ink-2)" strokeDasharray="4 3" strokeWidth={1} />
            <text x={M.l + pw + 6} y={y(reference.value) + 3.5} fontSize="10" fill="var(--ink-2)">
              {reference.label} {formatValue(reference.value, unit, lang)}
            </text>
          </g>
        )}
        {offScale.map((p) => (
          <text key={`o${p.i}`} x={x(p.i)} y={M.t + 8} textAnchor="middle" fontSize="9" fill="var(--ink-2)">
            {props.offScaleLabel} {formatValue(p.v, unit, lang)}
          </text>
        ))}
        {paths.map((d, k) => (
          <path key={series[k].key} d={d} fill="none" stroke={COLORS[k % COLORS.length]} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" />
        ))}
        {endLabels.map((l) => (
          <g key={l.key}>
            <rect x={M.l + pw + 6} y={l.y - 1.5} width={8} height={3} rx={1.5} fill={l.color} />
            <text x={M.l + pw + 18} y={l.y + 3.5} fontSize="10" fill="var(--ink)">{l.label.length > 14 ? `${l.label.slice(0, 13)}…` : l.label}</text>
          </g>
        ))}
        {hover !== null && (
          <g pointerEvents="none">
            <line x1={x(hover)} x2={x(hover)} y1={M.t} y2={M.t + ph} stroke="var(--axis)" strokeWidth={1} />
            {series.map((s, k) => (s.values[hover] === null || s.values[hover] === undefined ? null : (
              <circle key={s.key} cx={x(hover)} cy={y(s.values[hover] as number)} r={4} fill={COLORS[k % COLORS.length]} stroke="var(--chart-surface)" strokeWidth={2} />
            )))}
          </g>
        )}
      </svg>
      {hover !== null && (
        <div className="tip" role="status" style={{
          left: `${(x(hover) / W) * 100}%`, top: 34,
          transform: x(hover) > W * 0.6 ? "translateX(calc(-100% - 12px))" : "translateX(12px)",
        }}>
          <strong>{years[hover]}</strong>
          {props.series.map((s, k) => (
            <div key={s.key}><i style={{ background: COLORS[k % COLORS.length] }} />{s.label} : {formatValue(s.values[hover], unit, lang)}</div>
          ))}
        </div>
      )}
      {series.length > 1 && (
        <div className="legend">
          {series.map((s, k) => <span key={s.key}><i style={{ background: COLORS[k % COLORS.length] }} />{s.label}</span>)}
        </div>
      )}
      <button className="link small no-print" style={{ marginTop: 6 }} onClick={() => setShowTable(!showTable)} aria-expanded={showTable}>
        {showTable ? props.tableLabel[1] : props.tableLabel[0]}
      </button>
      {showTable && (
        <div className="scroll-x" style={{ marginTop: 6 }}>
          <table className="data">
            <thead><tr><th scope="col" /> {years.map((yr) => <th key={yr} className="num" scope="col">{yr}</th>)}</tr></thead>
            <tbody>{props.series.map((s) => (
              <tr key={s.key}><th scope="row">{s.label}</th>{s.values.map((v, i) => <td key={i} className="num">{formatValue(v, unit, lang)}</td>)}</tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </figure>
  );
}
