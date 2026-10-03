import Link from "next/link";

import { NatureBadge } from "@/components/provenance";
import { Badge } from "@/components/ui/badge";
import { INSTRUMENT_LABEL, formatAmount, formatDate, formatPct, formatTenor, titleCase } from "@/lib/format";
import type { DataNature, Opportunity, PassportFact } from "@/lib/types";

/** Render a passport value for reading; the exact stored value stays in the tooltip. */
function factValue(f: PassportFact): string {
  if (f.value === null) return "Not available";
  if (f.unit === "%") return formatPct(f.value) ?? f.value;
  if (f.unit && /^[A-Z]{3}$/.test(f.unit)) return formatAmount(f.value, f.unit) ?? f.value;
  return `${f.value}${f.unit ? ` ${f.unit}` : ""}`;
}

export const SIGNAL_TYPE_LABEL: Record<string, string> = {
  upcoming_auction: "Upcoming auction",
  yield_move: "Yield movement",
  high_demand: "High demand",
  low_demand: "Low demand",
  high_yield: "Higher historical yield",
  curve_inversion: "Curve inversion",
  refinancing_concentration: "Refinancing concentration",
  auction_cancelled: "Cancelled",
  auction_postponed: "Postponed",
};

const NATURES = new Set(["FACT", "CALCULATION", "ESTIMATE", "AI_INTERPRETATION", "SYNTHETIC"]);

function Passport({ o }: { o: Opportunity }) {
  const p = o.evidence;
  return (
    <details className="mt-3 rounded-sm border border-border bg-surface-2/40">
      <summary className="cursor-pointer px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-muted">
        Signal passport — why this signal exists
      </summary>
      <div className="space-y-3 px-3 pb-3 text-[13px]">
        <section>
          <h4 className="mb-1 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide text-muted">
            1 · Published facts used
          </h4>
          <ul className="space-y-1">
            {p.facts.map((f, i) => (
              <li key={i} className="flex flex-wrap items-baseline gap-x-2">
                {NATURES.has(f.data_nature) && <NatureBadge nature={f.data_nature as DataNature} />}
                <span className="text-muted">{f.label}:</span>
                <span className="num font-medium" title={f.value !== null ? `Exact value: ${f.value} ${f.unit ?? ""}` : undefined}>
                  {factValue(f)}
                </span>
                {f.auction_id && (
                  <Link href={`/auctions/${f.auction_id}`} className="text-xs text-accent hover:underline">
                    auction {formatDate(f.auction_date ?? null)}
                  </Link>
                )}
                {f.source && <span className="text-xs text-muted">· {f.source}</span>}
                {f.source_url && (
                  <a href={f.source_url} className="text-xs text-accent underline" rel="noopener noreferrer" target="_blank">
                    document
                  </a>
                )}
              </li>
            ))}
          </ul>
        </section>
        {p.calculation && (
          <section>
            <h4 className="mb-1 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide text-muted">
              2 · Calculation <NatureBadge nature="CALCULATION" />
            </h4>
            <p className="font-mono text-xs">{p.calculation.formula}</p>
            {p.calculation.inputs && (
              <p className="mt-1 font-mono text-xs text-muted break-words">
                {Object.entries(p.calculation.inputs)
                  .map(([k, v]) => `${k} = ${Array.isArray(v) ? `[${v.length} auctions]` : String(v)}`)
                  .join(" · ")}
              </p>
            )}
            <p className="mt-1">
              Result: <span className="num font-semibold">{String(p.calculation.result)}</span> {p.calculation.unit}
            </p>
          </section>
        )}
        <section>
          <h4 className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-muted">3 · Rule that fired</h4>
          <p>{p.rule.description}</p>
        </section>
        <section>
          <h4 className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-muted">4 · What would invalidate it</h4>
          <p>{p.invalidated_if}</p>
        </section>
        {p.caveats.length > 0 && (
          <section>
            <h4 className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-muted">5 · Caveats</h4>
            <ul className="list-disc pl-5 text-muted">
              {p.caveats.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
          </section>
        )}
        <p className="text-[11px] text-subtle">
          Rules {p.rules_version} · computed as of {formatDate(p.as_of ?? null)}
        </p>
      </div>
    </details>
  );
}

export function SignalCard({ o }: { o: Opportunity }) {
  const s = o.security;
  const isUpcoming = o.opportunity_type === "upcoming_auction";
  return (
    <article className="rounded-md border border-border bg-surface p-3">
      <header className="flex flex-wrap items-center gap-2">
        <Badge variant={o.opportunity_type.includes("low") || o.opportunity_type.startsWith("auction_") ? "warning" : "neutral"}>
          {SIGNAL_TYPE_LABEL[o.opportunity_type] ?? titleCase(o.opportunity_type)}
        </Badge>
        <h3 className="text-sm font-semibold">{o.label}</h3>
        {o.matches_criteria === true && <Badge variant="good">✓ Matches your criteria</Badge>}
        {o.matches_criteria === false && (
          <Badge variant="neutral" title={o.criteria_unmet.join(", ")}>
            Outside criteria
          </Badge>
        )}
        {o.is_synthetic && <Badge variant="synthetic">SYNTHETIC</Badge>}
      </header>

      <dl className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-[13px] sm:grid-cols-4">
        <div>
          <dt className="text-[11px] text-muted">Country</dt>
          <dd>
            <Link href={`/countries/${o.country_iso3}`} className="hover:underline">
              {o.country_name}
            </Link>
          </dd>
        </div>
        <div>
          <dt className="text-[11px] text-muted">Instrument</dt>
          <dd>
            {s ? (
              <Link href={`/securities/${s.security_id}`} className="hover:underline">
                {INSTRUMENT_LABEL[s.instrument_type]} {formatTenor(s.tenor_days)}
              </Link>
            ) : (
              <span className="text-subtle italic">Country-level</span>
            )}
            {o.currency && <span className="ml-1 text-xs text-muted">{o.currency}</span>}
          </dd>
        </div>
        <div>
          <dt className="text-[11px] text-muted">{isUpcoming ? "Auction date" : "Date"}</dt>
          <dd className="num">
            {o.auction_id ? (
              <Link href={`/auctions/${o.auction_id}`} className="text-accent hover:underline">
                {formatDate(o.auction_date)}
              </Link>
            ) : (
              formatDate(o.auction_date) ?? <span className="text-subtle italic">—</span>
            )}
          </dd>
        </div>
        <div>
          <dt className="text-[11px] text-muted" title={isUpcoming ? "Last published result for the same tenor — not a forecast" : undefined}>
            {isUpcoming ? "Ref. yield (previous auction)" : "Yield"}
          </dt>
          <dd className="num font-semibold">{formatPct(o.yield_pct) ?? <span className="font-normal text-subtle italic">n/a</span>}</dd>
        </div>
      </dl>

      {o.explanation && <p className="mt-2 text-[13px] text-muted">{o.explanation}</p>}

      <div className="mt-2 flex flex-wrap items-center gap-1.5 text-[11px]">
        {o.strength && (
          <span className="text-muted" title={o.strength_definition}>
            Signal intensity <span className="num font-semibold text-foreground">{Number(o.strength).toFixed(2)}×</span> threshold
          </span>
        )}
        {o.risk_flags.map((f) => (
          <Badge key={f} variant={f === "synthetic_data" ? "synthetic" : "warning"}>
            {f.replace(/_/g, " ")}
          </Badge>
        ))}
        {o.matches_criteria === false && <span className="text-muted">· {o.criteria_unmet.join(", ")}</span>}
      </div>

      <Passport o={o} />
    </article>
  );
}
