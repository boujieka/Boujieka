/**
 * Graphiques légers en SVG inline (rendus côté serveur, aucune dépendance).
 * Charte : navy (structure), or (solaire), vert (renouvelable/climat).
 */

const NAVY = "#0A1E3F";
const GOLD = "#C9A227";
const VERT = "#1FA36A";

/** Profil journalier moyen : charge (navy) vs productible normalisé (or). */
export function DailyProfileChart({
  load,
  yieldPerKwp,
}: {
  load: number[];
  yieldPerKwp: number[];
}) {
  // Moyenne par heure de la journée sur l'année.
  const avg = (arr: number[]) => {
    const buckets = new Array(24).fill(0);
    const counts = new Array(24).fill(0);
    for (let h = 0; h < arr.length; h++) {
      buckets[h % 24] += arr[h];
      counts[h % 24]++;
    }
    return buckets.map((b, i) => (counts[i] ? b / counts[i] : 0));
  };
  const loadDay = avg(load);
  const yieldDay = avg(yieldPerKwp);
  const maxLoad = Math.max(...loadDay, 1e-9);
  const maxYield = Math.max(...yieldDay, 1e-9);

  const W = 520;
  const H = 200;
  const pad = 28;
  const x = (i: number) => pad + (i / 23) * (W - 2 * pad);
  const yL = (v: number) => H - pad - (v / maxLoad) * (H - 2 * pad);
  const yY = (v: number) => H - pad - (v / maxYield) * (H - 2 * pad);

  const path = (day: number[], y: (v: number) => number) =>
    day.map((v, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Profil journalier moyen">
      <line x1={pad} y1={H - pad} x2={W - pad} y2={H - pad} stroke="#C9D3E6" />
      <path d={path(yieldDay, yY)} fill="none" stroke={GOLD} strokeWidth={2.5} />
      <path d={path(loadDay, yL)} fill="none" stroke={NAVY} strokeWidth={2.5} />
      {[0, 6, 12, 18, 23].map((i) => (
        <text key={i} x={x(i)} y={H - 8} fontSize={10} fill="#5D77A3" textAnchor="middle">
          {i}h
        </text>
      ))}
      <g fontSize={11}>
        <rect x={pad} y={8} width={10} height={10} fill={NAVY} />
        <text x={pad + 14} y={17} fill={NAVY}>Charge</text>
        <rect x={pad + 80} y={8} width={10} height={10} fill={GOLD} />
        <text x={pad + 94} y={17} fill={NAVY}>Productible solaire</text>
      </g>
    </svg>
  );
}

/** Donut du taux de couverture (vert = couvert, gris = déficit résiduel). */
export function CoverageDonut({ coverage }: { coverage: number }) {
  const r = 52;
  const c = 2 * Math.PI * r;
  const filled = Math.max(0, Math.min(1, coverage)) * c;
  return (
    <svg viewBox="0 0 140 140" className="h-40 w-40" role="img" aria-label="Taux de couverture">
      <circle cx={70} cy={70} r={r} fill="none" stroke="#E7F7EF" strokeWidth={16} />
      <circle
        cx={70}
        cy={70}
        r={r}
        fill="none"
        stroke={VERT}
        strokeWidth={16}
        strokeDasharray={`${filled} ${c - filled}`}
        strokeLinecap="round"
        transform="rotate(-90 70 70)"
      />
      <text x={70} y={68} textAnchor="middle" fontSize={22} fontWeight={700} fill={NAVY}>
        {(coverage * 100).toFixed(0)}%
      </text>
      <text x={70} y={88} textAnchor="middle" fontSize={10} fill="#5D77A3">
        couverture
      </text>
    </svg>
  );
}

/** Barres horizontales de sous-scores (0–1). */
export function ScoreBars({
  scores,
}: {
  scores: { label: string; value: number; tone?: "navy" | "gold" | "vert" }[];
}) {
  const color = (t?: string) => (t === "gold" ? GOLD : t === "navy" ? NAVY : VERT);
  return (
    <div className="space-y-2">
      {scores.map((s) => (
        <div key={s.label}>
          <div className="mb-0.5 flex justify-between text-xs text-navy-600">
            <span>{s.label}</span>
            <span className="font-medium">{(s.value * 100).toFixed(0)}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-navy-50">
            <div
              className="h-2 rounded-full"
              style={{ width: `${Math.max(0, Math.min(1, s.value)) * 100}%`, background: color(s.tone) }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
