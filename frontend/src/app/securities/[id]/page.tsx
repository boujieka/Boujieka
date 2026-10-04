import Link from "next/link";
import { notFound } from "next/navigation";

import { AuctionTable } from "@/components/auction-table";
import { DateBarChart, TimeSeriesChart } from "@/components/charts";
import { Field, NatureBadge, ProvenancePanel } from "@/components/provenance";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ApiError, api } from "@/lib/api";
import { INSTRUMENT_LABEL, formatAmount, formatDate, formatPct, formatTenor, titleCase } from "@/lib/format";
import type { SecurityDetail } from "@/lib/types";

export default async function SecurityPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let s: SecurityDetail;
  try {
    s = await api.security(Number(id));
  } catch (e) {
    if (e instanceof ApiError && (e.status === 404 || e.status === 422)) notFound();
    throw e;
  }
  const completed = s.auctions.filter((a) => a.status === "completed");
  const yields = completed
    .filter((a) => a.official.weighted_average_yield !== null)
    .map((a) => ({ date: a.auction_date, value: Number(a.official.weighted_average_yield) }));
  const covers = completed
    .filter((a) => a.calculated.bid_to_cover !== null)
    .map((a) => ({ date: a.auction_date, value: Number(a.calculated.bid_to_cover) }));

  const details: [string, string, string | null][] = [
    ["Instrument", "instrument_type", INSTRUMENT_LABEL[s.instrument_type]],
    ["ISIN", "isin", s.isin],
    ["Local code", "local_code", s.local_code],
    ["Currency", "currency", s.currency],
    ["Original tenor", "tenor_days", formatTenor(s.tenor_days)],
    ["Issue date", "issue_date", formatDate(s.issue_date)],
    ["Maturity", "maturity_date", formatDate(s.maturity_date)],
    ["Coupon", "coupon_rate", formatPct(s.coupon_rate, 3)],
    ["Coupon frequency", "coupon_frequency", s.coupon_frequency ? titleCase(s.coupon_frequency) : null],
    ["Face value", "face_value", formatAmount(s.face_value, s.currency)],
    ["Minimum denomination", "minimum_denomination", formatAmount(s.minimum_denomination, s.currency)],
    ["Amortisation", "amortization", s.amortization],
    ["Indexation", "indexation", s.indexation],
    ["Green / social / sustainability", "green_social_sustainability_flag", s.green_social_sustainability_flag],
    ["Listing", "listing_status", s.listing_status],
  ];

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs text-muted">
          <Link href={`/countries/${s.country_iso3}`} className="hover:underline">
            {s.country_name}
          </Link>
        </p>
        <h1 className="mt-1 text-lg font-semibold">{s.security_name}</h1>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Instrument details</CardTitle>
            <NatureBadge nature={s.provenance.data_nature} />
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-[13px]">
              {details.map(([label, key, value]) => (
                <div key={key} className="contents">
                  <dt className="text-muted">{label}</dt>
                  <dd className="num">
                    <Field value={value} status={s.field_status[key]} />
                  </dd>
                </div>
              ))}
            </dl>
          </CardContent>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Weighted-average auction yield</CardTitle>
            <NatureBadge nature={s.provenance.data_nature} />
          </CardHeader>
          <CardContent>
            {yields.length > 1 ? (
              <TimeSeriesChart series={[{ key: "way", label: "WA yield", points: yields }]} unit="%" ariaLabel="Weighted-average yield at each auction" />
            ) : yields.length === 1 ? (
              <p className="text-sm">
                Single auction: <span className="num font-semibold">{formatPct(String(yields[0].value))}</span> on{" "}
                {formatDate(yields[0].date)}. A history chart needs at least two auctions (bills are usually issued once).
              </p>
            ) : (
              <p className="text-sm text-muted">No published results yet.</p>
            )}
          </CardContent>
        </Card>
      </div>

      {covers.length > 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Bid-to-cover per auction</CardTitle>
            <NatureBadge nature="CALCULATION" />
          </CardHeader>
          <CardContent>
            <DateBarChart points={covers} label="Bid-to-cover" unit="×" ariaLabel="Calculated bid-to-cover at each auction" />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Auction history</CardTitle>
        </CardHeader>
        <AuctionTable auctions={[...s.auctions].reverse()} caption="Auction history" />
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Source & provenance</CardTitle>
        </CardHeader>
        <CardContent>
          <ProvenancePanel p={s.provenance} />
          <p className="mt-3 text-xs text-muted">Source documents will be linked here once document ingestion (Phase 2) is live.</p>
        </CardContent>
      </Card>
    </div>
  );
}
