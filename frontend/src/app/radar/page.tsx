import Link from "next/link";

import { CategoryBarChart } from "@/components/charts";
import { HeatGrid } from "@/components/heat-grid";
import { NatureBadge } from "@/components/provenance";
import { SIGNAL_TYPE_LABEL, SignalCard } from "@/components/signal-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { api } from "@/lib/api";
import { formatAmount, formatDate } from "@/lib/format";
import { cn } from "@/lib/utils";

type SP = Record<string, string | string[] | undefined>;

const one = (v: string | string[] | undefined) => (Array.isArray(v) ? (v[0] ?? "") : (v ?? ""));

const fieldCls =
  "h-8 rounded-sm border border-border-strong bg-surface px-2 text-[13px] focus:outline-2 focus:outline-accent";

const CRITERIA_KEYS = ["min_yield", "min_tenor_days", "max_tenor_days", "currency", "matching_only", "sort"] as const;

export default async function RadarPage({ searchParams }: { searchParams: Promise<SP> }) {
  const sp = await searchParams;
  const f = {
    country: one(sp.country).toUpperCase(),
    type: one(sp.type),
    min_yield: one(sp.min_yield),
    min_tenor_days: one(sp.min_tenor_days),
    max_tenor_days: one(sp.max_tenor_days),
    currency: one(sp.currency).toUpperCase(),
    matching_only: one(sp.matching_only),
    sort: one(sp.sort) || "date",
  };

  const [grid, page, wall] = await Promise.all([
    api.heatGrid(),
    api.opportunities({
      country: f.country,
      opportunity_type: f.type ? [f.type] : undefined,
      min_yield: f.min_yield,
      min_tenor_days: f.min_tenor_days,
      max_tenor_days: f.max_tenor_days,
      currency: f.currency,
      matching_only: f.matching_only === "1" ? true : undefined,
      sort: f.sort,
      limit: 200,
    }),
    f.country ? api.maturityWall(f.country).catch(() => null) : Promise.resolve(null),
  ]);

  const selectedRow = grid.rows.find((r) => r.country_iso3 === f.country);
  const currencies = [...new Set(grid.rows.map((r) => r.currency))].sort();
  const totalAll = grid.rows.reduce((n, r) => n + r.active_opportunities, 0);
  const matching = page.items.filter((o) => o.matches_criteria === true).length;
  const hasCriteria = Object.keys(page.criteria).length > 0;

  const href = (patch: Record<string, string>) => {
    const qs = new URLSearchParams(Object.entries({ ...f, ...patch }).filter(([k, v]) => v && !(k === "sort" && v === "date")));
    const s = qs.toString();
    return s ? `/radar?${s}` : "/radar";
  };

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-lg font-semibold">Opportunity Radar</h1>
        <p className="mt-1 max-w-3xl text-sm text-muted">
          Rule-based signals detected in published auction data. Choose a country on the grid or below. Each signal
          carries a <strong>passport</strong>: the published facts, the calculation, the rule that fired and what
          would invalidate it.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Pan-African sovereign heat grid</CardTitle>
          <span className="text-xs text-muted">Latest auction per tenor · as of {formatDate(grid.as_of)}</span>
        </CardHeader>
        <CardContent>
          <HeatGrid grid={grid} selected={f.country || undefined} />
        </CardContent>
      </Card>

      <nav aria-label="Choose a country" className="flex flex-wrap gap-2">
        {[{ iso3: "", name: "All countries", n: totalAll }, ...grid.rows.map((r) => ({ iso3: r.country_iso3, name: r.country_name, n: r.active_opportunities }))].map(
          (c) => {
            const active = f.country === c.iso3;
            return (
              <Link
                key={c.iso3 || "all"}
                href={href({ country: c.iso3, type: "" })}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "inline-flex items-center gap-2 rounded-sm border px-3 py-1.5 text-[13px]",
                  active ? "border-accent bg-accent text-accent-foreground" : "border-border-strong bg-surface hover:border-accent",
                )}
              >
                {c.name}
                <span className={cn("num text-xs", active ? "opacity-90" : "text-muted")}>{c.n}</span>
              </Link>
            );
          },
        )}
      </nav>

      <form method="get" aria-label="Your criteria" className="flex flex-wrap items-end gap-3 rounded-md border border-border bg-surface p-3">
        {f.country && <input type="hidden" name="country" value={f.country} />}
        {f.type && <input type="hidden" name="type" value={f.type} />}
        <span className="w-full text-[11px] font-semibold uppercase tracking-wide text-muted sm:w-auto sm:self-center">Your criteria</span>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Min. yield (%)
          <input name="min_yield" type="number" step="0.25" min="0" defaultValue={f.min_yield} className={cn(fieldCls, "w-24")} />
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Min. tenor (days)
          <input name="min_tenor_days" type="number" min="0" defaultValue={f.min_tenor_days} className={cn(fieldCls, "w-28")} />
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Max. tenor (days)
          <input name="max_tenor_days" type="number" min="0" defaultValue={f.max_tenor_days} className={cn(fieldCls, "w-28")} />
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Currency
          <select name="currency" defaultValue={f.currency} className={fieldCls}>
            <option value="">Any</option>
            {currencies.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Order
          <select name="sort" defaultValue={f.sort} className={fieldCls}>
            <option value="date">Soonest date</option>
            <option value="strength">Signal intensity</option>
          </select>
        </label>
        <label className="flex h-8 items-center gap-2 text-[13px]">
          <input type="checkbox" name="matching_only" value="1" defaultChecked={f.matching_only === "1"} />
          Only matching
        </label>
        <button type="submit" className="h-8 rounded-sm bg-accent px-3 text-[13px] font-medium text-accent-foreground">
          Apply
        </button>
        <Link href={href(Object.fromEntries(CRITERIA_KEYS.map((k) => [k, ""])))} className="h-8 px-1 text-[13px] leading-8 text-muted hover:text-foreground">
          Clear criteria
        </Link>
      </form>

      <div className="grid gap-4 lg:grid-cols-3">
        <section className="space-y-3 lg:col-span-2" aria-label="Signals">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-sm font-semibold">
              {page.total} signal{page.total === 1 ? "" : "s"}
              {selectedRow ? ` · ${selectedRow.country_name}` : ""}
              {hasCriteria && <span className="font-normal text-muted"> · {matching} match your criteria</span>}
            </h2>
            <div className="flex flex-wrap gap-1.5" role="group" aria-label="Filter by signal type">
              <Link href={href({ type: "" })} className={cn("rounded-sm border px-2 py-0.5 text-xs", !f.type ? "border-accent text-accent" : "border-border text-muted hover:text-foreground")}>
                All types
              </Link>
              {Object.entries(page.by_type)
                .sort((a, b) => b[1] - a[1])
                .map(([t, n]) => (
                  <Link
                    key={t}
                    href={href({ type: f.type === t ? "" : t })}
                    className={cn("rounded-sm border px-2 py-0.5 text-xs", f.type === t ? "border-accent text-accent" : "border-border text-muted hover:text-foreground")}
                  >
                    {SIGNAL_TYPE_LABEL[t] ?? t} <span className="num">{n}</span>
                  </Link>
                ))}
            </div>
          </div>
          {page.items.length === 0 ? (
            <p className="rounded-md border border-border bg-surface p-4 text-sm text-muted">No signals match these filters.</p>
          ) : (
            page.items.map((o) => <SignalCard key={o.opportunity_id} o={o} />)
          )}
        </section>

        <aside className="space-y-4" aria-label="Country context">
          {selectedRow && wall ? (
            <>
              <Card>
                <CardHeader>
                  <CardTitle>Refinancing wall · {selectedRow.country_name}</CardTitle>
                  <NatureBadge nature={wall.data_nature} />
                </CardHeader>
                <CardContent>
                  {Number(wall.total) > 0 ? (
                    <>
                      <CategoryBarChart
                        ariaLabel={`Tracked securities maturing per month in ${selectedRow.country_name}`}
                        label={`Maturing (${wall.currency})`}
                        points={wall.months.map((m) => ({ name: m.month.slice(2), value: Number(m.amount) }))}
                      />
                      <details className="mt-2 text-xs">
                        <summary className="cursor-pointer text-muted">Table view</summary>
                        <Table>
                          <THead>
                            <tr>
                              <TH>Month</TH>
                              <TH className="text-right">Maturing</TH>
                              <TH className="text-right">Share</TH>
                            </tr>
                          </THead>
                          <TBody>
                            {wall.months.map((m) => (
                              <TR key={m.month}>
                                <TD>{m.month}</TD>
                                <TD className="num text-right">{formatAmount(m.amount, wall.currency)}</TD>
                                <TD className="num text-right">{m.share_pct ? `${Number(m.share_pct).toFixed(1)}%` : "—"}</TD>
                              </TR>
                            ))}
                          </TBody>
                        </Table>
                      </details>
                      <p className="mt-2 text-[11px] text-muted">
                        Total next 12 months: <span className="num">{formatAmount(wall.total, wall.currency)}</span>. {wall.caveat}
                      </p>
                    </>
                  ) : (
                    <p className="text-sm text-muted">No tracked maturities in the next 12 months.</p>
                  )}
                </CardContent>
              </Card>
              <Link href={`/countries/${selectedRow.country_iso3}`} className="block rounded-md border border-border bg-surface px-4 py-3 text-sm text-accent hover:border-accent">
                Full country profile, yield curve & sources →
              </Link>
            </>
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Signals by country</CardTitle>
              </CardHeader>
              <Table>
                <TBody>
                  {grid.rows
                    .slice()
                    .sort((a, b) => b.active_opportunities - a.active_opportunities)
                    .map((r) => (
                      <TR key={r.country_iso3}>
                        <TD>
                          <Link href={href({ country: r.country_iso3, type: "" })} className="text-accent hover:underline">
                            {r.country_name}
                          </Link>
                        </TD>
                        <TD className="num text-right font-semibold">{r.active_opportunities}</TD>
                      </TR>
                    ))}
                </TBody>
              </Table>
              <p className="px-4 py-2 text-[11px] text-muted">A count of rule hits, not a ranking of countries.</p>
            </Card>
          )}
          <Card>
            <CardContent className="text-[12px] text-muted">
              <p className="font-semibold text-foreground">How to read this</p>
              <p className="mt-1">{page.disclaimer}</p>
              <p className="mt-2">{grid.method}</p>
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}
