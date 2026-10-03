import Link from "next/link";

import { AuctionTable } from "@/components/auction-table";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { INSTRUMENT_LABEL, addDays, todayIso } from "@/lib/format";
import type { InstrumentType } from "@/lib/types";

type SP = Record<string, string | string[] | undefined>;

const PAGE_SIZE = 50;
const MATURITY_BUCKETS: Record<string, { label: string; min?: number; max?: number }> = {
  "": { label: "Any maturity" },
  short: { label: "≤ 1 year", max: 366 },
  medium: { label: "1–5 years", min: 367, max: 5 * 365 },
  long: { label: "> 5 years", min: 5 * 365 + 1 },
};

function one(v: string | string[] | undefined): string {
  return Array.isArray(v) ? (v[0] ?? "") : (v ?? "");
}

const fieldCls =
  "h-8 rounded-sm border border-border-strong bg-surface px-2 text-[13px] focus:outline-2 focus:outline-accent";

export default async function AuctionCalendarPage({ searchParams }: { searchParams: Promise<SP> }) {
  const sp = await searchParams;
  const today = todayIso();
  const f = {
    country: one(sp.country),
    currency: one(sp.currency),
    instrument_type: one(sp.instrument_type),
    status: one(sp.status),
    maturity: one(sp.maturity),
    date_from: one(sp.date_from) || today,
    date_to: one(sp.date_to) || addDays(today, 30),
  };
  const page = Math.max(0, Number(one(sp.page)) || 0);
  const bucket = MATURITY_BUCKETS[f.maturity] ?? MATURITY_BUCKETS[""];

  const [countries, data] = await Promise.all([
    api.countries(),
    api.auctions({
      country: f.country,
      currency: f.currency,
      instrument_type: f.instrument_type ? [f.instrument_type] : undefined,
      status: f.status ? [f.status] : undefined,
      date_from: f.date_from,
      date_to: f.date_to,
      min_tenor_days: bucket.min,
      max_tenor_days: bucket.max,
      order: "asc",
      limit: PAGE_SIZE,
      offset: page * PAGE_SIZE,
    }),
  ]);
  const currencies = [...new Set(countries.map((c) => c.currency))].sort();
  const pageHref = (p: number) => {
    const qs = new URLSearchParams(Object.entries({ ...f, page: String(p) }).filter(([, v]) => v));
    return `/auctions?${qs}`;
  };

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Auction calendar</h1>

      <form method="get" className="flex flex-wrap items-end gap-3 rounded-md border border-border bg-surface p-3" aria-label="Filter auctions">
        <label className="flex flex-col gap-1 text-xs text-muted">
          Country
          <select name="country" defaultValue={f.country} className={fieldCls}>
            <option value="">All countries</option>
            {countries.map((c) => (
              <option key={c.iso3} value={c.iso3}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Currency
          <select name="currency" defaultValue={f.currency} className={fieldCls}>
            <option value="">All</option>
            {currencies.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Instrument
          <select name="instrument_type" defaultValue={f.instrument_type} className={fieldCls}>
            <option value="">All</option>
            {(Object.keys(INSTRUMENT_LABEL) as InstrumentType[]).map((k) => (
              <option key={k} value={k}>
                {INSTRUMENT_LABEL[k]}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Maturity
          <select name="maturity" defaultValue={f.maturity} className={fieldCls}>
            {Object.entries(MATURITY_BUCKETS).map(([k, b]) => (
              <option key={k} value={k}>
                {b.label}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          Status
          <select name="status" defaultValue={f.status} className={fieldCls}>
            <option value="">All</option>
            <option value="announced">Announced</option>
            <option value="completed">Completed</option>
            <option value="postponed">Postponed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          From
          <input type="date" name="date_from" defaultValue={f.date_from} className={fieldCls} />
        </label>
        <label className="flex flex-col gap-1 text-xs text-muted">
          To
          <input type="date" name="date_to" defaultValue={f.date_to} className={fieldCls} />
        </label>
        <button type="submit" className="h-8 rounded-sm bg-accent px-3 text-[13px] font-medium text-accent-foreground">
          Apply
        </button>
        <Link href="/auctions" className="h-8 px-1 text-[13px] leading-8 text-muted hover:text-foreground">
          Reset
        </Link>
      </form>
      <p className="text-xs text-muted">
        Investor-eligibility filtering needs verified subscription-route data and is planned for Phase 6.
      </p>

      <Card>
        <CardHeader>
          <CardTitle>
            {data.total} auction{data.total === 1 ? "" : "s"}
          </CardTitle>
          {data.total > PAGE_SIZE && (
            <nav aria-label="Pagination" className="flex gap-3 text-xs">
              {page > 0 && (
                <Link href={pageHref(page - 1)} className="text-accent">
                  ← Previous
                </Link>
              )}
              <span className="text-muted">
                Page {page + 1} of {Math.ceil(data.total / PAGE_SIZE)}
              </span>
              {(page + 1) * PAGE_SIZE < data.total && (
                <Link href={pageHref(page + 1)} className="text-accent">
                  Next →
                </Link>
              )}
            </nav>
          )}
        </CardHeader>
        <AuctionTable auctions={data.items} caption="Auction calendar" />
      </Card>
    </div>
  );
}
