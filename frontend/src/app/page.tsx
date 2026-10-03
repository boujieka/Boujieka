import Link from "next/link";

import { AuctionTable } from "@/components/auction-table";
import { Kpi } from "@/components/kpi";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { addDays, formatAmount, formatDate } from "@/lib/format";

export default async function HomePage() {
  const summary = await api.summary();
  const today = summary.as_of;
  const [upcoming, results] = await Promise.all([
    api.auctions({ date_from: today, date_to: addDays(today, 7), order: "asc", limit: 50 }),
    api.auctions({ status: ["completed"], date_to: today, date_from: addDays(today, -6), order: "desc", limit: 50 }),
  ]);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-lg font-semibold">Market overview</h1>
        <p className="text-xs text-muted">As of {formatDate(today)}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <Kpi label="Upcoming auctions (7d)" value={summary.upcoming_auctions_7d} hint={`${summary.upcoming_auctions_30d} in next 30 days`} href="/auctions" />
        <Kpi label="Countries monitored" value={summary.countries_monitored} href="/countries" />
        <Kpi label="New results (7d)" value={summary.results_last_7d} />
        <Kpi
          label="Announced issuance (30d)"
          value={
            summary.announced_issuance_by_currency.length ? (
              <span className="flex flex-col text-base">
                {summary.announced_issuance_by_currency.map((r) => (
                  <span key={r.currency} className="num">
                    {formatAmount(r.amount, r.currency)}
                  </span>
                ))}
              </span>
            ) : (
              "—"
            )
          }
          hint="Offered amounts, per currency (never summed across currencies)"
        />
        <Kpi
          label="New opportunities"
          value={<span className="text-base text-subtle italic">Not available</span>}
          hint="Opportunity Engine arrives in Phase 4"
        />
        <Kpi
          label="Alerts"
          value={summary.cancelled_or_postponed}
          hint="Upcoming auctions cancelled or postponed"
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Auctions in the next 7 days</CardTitle>
          <Link href="/auctions" className="text-xs text-accent hover:underline">
            Full calendar →
          </Link>
        </CardHeader>
        <AuctionTable auctions={upcoming.items} showResults={false} caption="Auctions in the next 7 days" />
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Results published in the last 7 days</CardTitle>
        </CardHeader>
        <AuctionTable auctions={results.items} caption="Recent auction results" />
      </Card>

      {summary.sources_pending_configuration > 0 && (
        <Card>
          <CardContent className="text-sm text-muted">
            {summary.sources_pending_configuration} official sources are registered but not yet configured — no live
            data is being collected from them. See{" "}
            <Link href="/admin/data-quality" className="text-accent underline">
              data quality
            </Link>
            .
          </CardContent>
        </Card>
      )}
    </div>
  );
}
