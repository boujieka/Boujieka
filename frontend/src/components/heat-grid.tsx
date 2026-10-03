import Link from "next/link";

import { formatDate, formatPct, formatTenor } from "@/lib/format";
import type { HeatCell, HeatGrid as HeatGridData } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Diverging bins on demand z-score. Colour is never the only cue: the arrow and value are printed. */
function demandStyle(z: number | null): { bg: string; arrow: string; word: string } {
  if (z === null) return { bg: "transparent", arrow: "·", word: "insufficient history" };
  if (z >= 1.5) return { bg: "var(--div-pos-2)", arrow: "▲▲", word: "well above own history" };
  if (z >= 0.5) return { bg: "var(--div-pos-1)", arrow: "▲", word: "above own history" };
  if (z > -0.5) return { bg: "var(--div-mid)", arrow: "–", word: "in line with own history" };
  if (z > -1.5) return { bg: "var(--div-neg-1)", arrow: "▼", word: "below own history" };
  return { bg: "var(--div-neg-2)", arrow: "▼▼", word: "well below own history" };
}

function Cell({ cell }: { cell: HeatCell | undefined }) {
  if (!cell) {
    return <td className="border border-border px-2 py-1.5 text-center text-xs text-subtle">—</td>;
  }
  const z = cell.demand_z === null ? null : Number(cell.demand_z);
  const s = demandStyle(z);
  const title = [
    `${formatTenor(cell.tenor_days)} · auction ${formatDate(cell.auction_date)}`,
    `WA yield ${formatPct(cell.weighted_average_yield) ?? "n/a"}`,
    `Bid-to-cover ${cell.bid_to_cover ? Number(cell.bid_to_cover).toFixed(2) + "×" : "n/a"}`,
    z === null ? `Demand: ${s.word}` : `Demand z = ${z.toFixed(2)} (${s.word}, n=${cell.demand_peer_count})`,
  ].join("\n");
  return (
    <td className="border border-border p-0" style={{ background: s.bg }}>
      <Link
        href={`/auctions/${cell.auction_id}`}
        title={title}
        className="block px-2 py-1.5 text-center leading-tight hover:outline-2 hover:outline-accent focus-visible:outline-2 focus-visible:outline-accent"
      >
        <span className="num block text-[13px] font-semibold">{formatPct(cell.weighted_average_yield, 2) ?? "—"}</span>
        <span className="num block text-[11px] text-muted">
          <span aria-hidden>{s.arrow}</span> {z === null ? "n/a" : `z ${z > 0 ? "+" : ""}${z.toFixed(1)}`}
        </span>
        <span className="sr-only">{s.word}</span>
      </Link>
    </td>
  );
}

export function HeatGrid({ grid, selected }: { grid: HeatGridData; selected?: string }) {
  return (
    <div>
      {/* `relative` contains the absolutely positioned sr-only labels inside the scroller. */}
      <div className="relative overflow-x-auto">
        <table className="w-full min-w-[640px] border-collapse text-[13px]">
          <caption className="sr-only">
            Latest auction yield and demand versus own history by country and tenor
          </caption>
          <thead>
            <tr>
              <th scope="col" className="px-2 py-1.5 text-left text-[11px] font-semibold uppercase tracking-wide text-muted">
                Country
              </th>
              {grid.buckets.map((b) => (
                <th key={b} scope="col" className="px-2 py-1.5 text-center text-[11px] font-semibold uppercase tracking-wide text-muted">
                  {b}
                </th>
              ))}
              <th scope="col" className="px-2 py-1.5 text-right text-[11px] font-semibold uppercase tracking-wide text-muted">
                Signals
              </th>
            </tr>
          </thead>
          <tbody>
            {grid.rows.map((row) => {
              const byBucket = new Map(row.cells.map((c) => [c.bucket, c]));
              const isSel = selected === row.country_iso3;
              return (
                <tr key={row.country_iso3} className={cn(isSel && "outline-2 outline-accent")}>
                  <th scope="row" className="px-2 py-1.5 text-left font-normal whitespace-nowrap">
                    <Link
                      href={isSel ? "/radar" : `/radar?country=${row.country_iso3}`}
                      className={cn("hover:underline", isSel ? "font-semibold text-accent" : "text-foreground")}
                      aria-current={isSel ? "true" : undefined}
                    >
                      {row.country_name}
                    </Link>
                    <span className="ml-1 text-xs text-muted">{row.currency}</span>
                  </th>
                  {grid.buckets.map((b) => (
                    <Cell key={b} cell={byBucket.get(b)} />
                  ))}
                  <td className="num px-2 py-1.5 text-right font-semibold">{row.active_opportunities}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-muted" aria-label="Legend">
        <span className="font-semibold uppercase tracking-wide">Demand vs own history (z)</span>
        {[
          ["var(--div-neg-2)", "▼▼ ≤ −1.5"],
          ["var(--div-neg-1)", "▼ −1.5…−0.5"],
          ["var(--div-mid)", "– in line"],
          ["var(--div-pos-1)", "▲ 0.5…1.5"],
          ["var(--div-pos-2)", "▲▲ ≥ 1.5"],
        ].map(([bg, text]) => (
          <span key={text} className="inline-flex items-center gap-1">
            <span className="inline-block h-3 w-4 rounded-sm border border-border" style={{ background: bg }} />
            {text}
          </span>
        ))}
      </div>
      <p className="mt-1 text-[11px] text-muted">{grid.caveat}</p>
    </div>
  );
}
