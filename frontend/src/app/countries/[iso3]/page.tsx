import { notFound } from "next/navigation";

import { AuctionTable } from "@/components/auction-table";
import { MAX_SERIES, TimeSeriesChart, YieldCurveChart, type TimeSeries } from "@/components/charts";
import { Field, ProvenancePanel } from "@/components/provenance";
import { SourceTable } from "@/components/source-table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { ApiError, api } from "@/lib/api";
import { INSTRUMENT_LABEL, formatDate, formatPct, formatTenor, todayIso } from "@/lib/format";
import type { CountryDetail } from "@/lib/types";

export default async function CountryPage({ params }: { params: Promise<{ iso3: string }> }) {
  const { iso3 } = await params;
  let country: CountryDetail;
  try {
    country = await api.country(iso3);
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    throw e;
  }
  const today = todayIso();
  const [curve, upcoming, history] = await Promise.all([
    api.yieldCurve(country.iso3),
    api.auctions({ country: country.iso3, date_from: today, order: "asc", limit: 50 }),
    api.auctions({ country: country.iso3, status: ["completed"], date_to: today, order: "desc", limit: 500 }),
  ]);

  // Yield history per tenor: one series per original tenor, shortest first, capped (never cycled colours).
  const byTenor = new Map<number, TimeSeries>();
  for (const a of [...history.items].reverse()) {
    const t = a.security.tenor_days;
    if (t === null || a.official.weighted_average_yield === null) continue;
    const s = byTenor.get(t) ?? {
      key: `t${t}`,
      label: `${INSTRUMENT_LABEL[a.security.instrument_type]} ${formatTenor(t)}`,
      points: [],
    };
    s.points.push({ date: a.auction_date, value: Number(a.official.weighted_average_yield) });
    byTenor.set(t, s);
  }
  const series = [...byTenor.entries()].sort(([a], [b]) => a - b).map(([, s]) => s);

  const structure: [string, string, string | null][] = [
    ["Currency", "currency", country.currency],
    ["Monetary zone", "monetary_zone", country.monetary_zone === "NONE" ? "None (own central bank)" : country.monetary_zone],
    ["Central bank", "central_bank", country.central_bank],
    ["Debt management", "debt_management_office", country.debt_management_office],
    ["Primary market", "primary_market_structure", country.primary_market_structure],
    ["Secondary market", "secondary_market_structure", country.secondary_market_structure],
    ["Tax notes", "tax_notes", country.tax_notes],
    ["Capital controls", "capital_controls", country.capital_controls],
    ["Market access", "market_access_notes", country.market_access_notes],
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-lg font-semibold">
          {country.name} <span className="text-sm font-normal text-muted">{country.iso3} · {country.currency}</span>
        </h1>
        <p className="text-xs text-muted">
          {country.upcoming_auction_count} upcoming · {country.completed_auction_count} completed ·{" "}
          {country.security_count} securities
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Primary-auction yield curve</CardTitle>
            <span className="text-xs text-muted">last {curve.lookback_days} days</span>
          </CardHeader>
          <CardContent>
            {curve.points.length ? (
              <>
                <YieldCurveChart
                  ariaLabel={`Latest auction yield by tenor for ${country.name}`}
                  points={curve.points.map((p) => ({
                    years: p.tenor_days / 365,
                    value: Number(p.weighted_average_yield),
                    label: `${INSTRUMENT_LABEL[p.instrument_type]} ${formatTenor(p.tenor_days)}`,
                    date: formatDate(p.auction_date) ?? "",
                  }))}
                />
                <details className="mt-2 text-xs">
                  <summary className="cursor-pointer text-muted">Table view & method</summary>
                  <Table>
                    <THead>
                      <tr>
                        <TH>Tenor</TH>
                        <TH className="text-right">WA yield</TH>
                        <TH>Auction</TH>
                      </tr>
                    </THead>
                    <TBody>
                      {curve.points.map((p) => (
                        <TR key={p.tenor_days}>
                          <TD>{formatTenor(p.tenor_days)}</TD>
                          <TD className="num text-right">{formatPct(p.weighted_average_yield)}</TD>
                          <TD>{formatDate(p.auction_date)}</TD>
                        </TR>
                      ))}
                    </TBody>
                  </Table>
                  <p className="mt-2 text-muted">{curve.method}</p>
                  <p className="text-muted">{curve.caveat}</p>
                </details>
              </>
            ) : (
              <p className="text-sm text-muted">No completed auctions in the lookback window.</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Auction yield history by tenor</CardTitle>
            {series.length > MAX_SERIES && (
              <span className="text-xs text-muted">showing {MAX_SERIES} shortest of {series.length} tenors</span>
            )}
          </CardHeader>
          <CardContent>
            {series.length ? (
              <TimeSeriesChart series={series} unit="%" ariaLabel={`Weighted-average auction yield over time for ${country.name}`} />
            ) : (
              <p className="text-sm text-muted">No completed auctions.</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upcoming auctions</CardTitle>
        </CardHeader>
        <AuctionTable auctions={upcoming.items} showResults={false} caption={`Upcoming auctions in ${country.name}`} />
      </Card>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Debt-market structure</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-1 gap-x-4 gap-y-2 text-[13px] sm:grid-cols-[160px_1fr]">
              {structure.map(([label, key, value]) => (
                <div key={key} className="contents">
                  <dt className="text-muted">{label}</dt>
                  <dd>
                    <Field value={value} status={country.field_status[key]} />
                  </dd>
                </div>
              ))}
            </dl>
            <p className="mt-3 text-xs text-muted">
              Primary dealers and the subscription process will be shown here once verified subscription-route data
              exists (Phase 6).
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Reference-data provenance</CardTitle>
          </CardHeader>
          <CardContent>
            <ProvenancePanel p={country.provenance} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Official sources</CardTitle>
        </CardHeader>
        <SourceTable sources={country.sources} />
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Recent auction results</CardTitle>
          <span className="text-xs text-muted">latest 25 of {history.total}</span>
        </CardHeader>
        <AuctionTable auctions={history.items.slice(0, 25)} caption={`Recent auction results for ${country.name}`} />
      </Card>
    </div>
  );
}
