/**
 * Aperçu produit du hero — mini « fiche de pré-faisabilité » en SVG.
 * Montre le cœur d'ATEN : courbe charge vs productible, part servie par le
 * solaire+stockage, et les trois sorties clés. Chiffres ILLUSTRATIFS (étiquetés).
 * Rendu serveur, autonome, sans dépendance.
 */

const NAVY = "#0a1e3f";
const GOLD = "#c9a227";
const VERT = "#1fa36a";

// Profil journalier stylisé (24 h) — charge industrielle + productible solaire.
const HOURS = Array.from({ length: 24 }, (_, h) => h);
const load = HOURS.map((h) => 0.62 + 0.28 * Math.exp(-((h - 13) ** 2) / 40) + 0.05 * Math.sin(h));
const solar = HOURS.map((h) => {
  const x = (h - 6) / 12;
  return x > 0 && x < 1 ? Math.sin(Math.PI * x) : 0;
});

function path(series: number[], W: number, H: number, pad: number, max: number) {
  const x = (i: number) => pad + (i / 23) * (W - 2 * pad);
  const y = (v: number) => H - pad - (v / max) * (H - 2 * pad);
  return series.map((v, i) => `${i === 0 ? "M" : "L"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
}

export function HeroPreview() {
  const W = 320;
  const H = 150;
  const pad = 16;
  const max = 1.05;
  // Aire du solaire réellement utilisé = min(charge, solaire).
  const served = HOURS.map((h) => Math.min(load[h], solar[h]));
  const areaPath =
    path(served, W, H, pad, max) +
    ` L${(pad + (W - 2 * pad)).toFixed(1)},${(H - pad).toFixed(1)} L${pad},${(H - pad).toFixed(1)} Z`;

  return (
    <div className="w-full rounded-2xl border border-white/12 bg-white p-4 shadow-2xl">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold text-navy-800">Aperçu de pré-faisabilité</div>
        <span className="rounded-full bg-navy-50 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-navy-400">
          Exemple illustratif
        </span>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className="mt-3 w-full" role="img" aria-label="Charge horaire et productible solaire sur une journée">
        <line x1={pad} y1={H - pad} x2={W - pad} y2={H - pad} stroke="#e1e8f2" />
        <path d={areaPath} fill={GOLD} fillOpacity={0.16} />
        <path d={path(solar, W, H, pad, max)} fill="none" stroke={GOLD} strokeWidth={2.5} />
        <path d={path(load, W, H, pad, max)} fill="none" stroke={NAVY} strokeWidth={2.5} />
        {[0, 6, 12, 18].map((h) => (
          <text key={h} x={pad + (h / 23) * (W - 2 * pad)} y={H - 4} fontSize={8} fill="#93a6c6" textAnchor="middle">
            {h}h
          </text>
        ))}
      </svg>

      <div className="mt-1 flex gap-4 text-[11px] text-navy-500">
        <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-sm" style={{ background: NAVY }} /> Charge</span>
        <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-sm" style={{ background: GOLD }} /> Productible solaire</span>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 border-t border-navy-50 pt-3">
        <Metric label="Couverture" value="95 %" tone={VERT} />
        <Metric label="CO₂ évité" value="≈ 420 t/an" tone={VERT} />
        <Metric label="PPA vs réseau" value="−18 %" tone={GOLD} />
      </div>
    </div>
  );
}

function Metric({ label, value, tone }: { label: string; value: string; tone: string }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wide text-navy-400">{label}</div>
      <div className="text-base font-semibold tabular-nums" style={{ color: tone }}>{value}</div>
    </div>
  );
}
