import Link from "next/link";
import { notFound } from "next/navigation";

import { AuctionTable, StatusBadge } from "@/components/auction-table";
import { Field, NatureBadge, ProvenancePanel } from "@/components/provenance";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ApiError, api } from "@/lib/api";
import {
  INSTRUMENT_LABEL,
  formatAmount,
  formatBps,
  formatDate,
  formatPct,
  formatRatio,
  formatShare,
  formatTenor,
  titleCase,
} from "@/lib/format";
import type { AuctionDetail } from "@/lib/types";

function Row({ label, children, title }: { label: string; children: React.ReactNode; title?: string }) {
  return (
    <div className="flex justify-between gap-4 border-b border-border py-1.5 last:border-0" title={title}>
      <dt className="text-muted">{label}</dt>
      <dd className="num text-right">{children}</dd>
    </div>
  );
}

export default async function AuctionPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let a: AuctionDetail;
  try {
    a = await api.auction(Number(id));
  } catch (e) {
    if (e instanceof ApiError && (e.status === 404 || e.status === 422)) notFound();
    throw e;
  }
  const o = a.official;
  const fs = a.field_status;
  const cur = a.security.currency;

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs text-muted">
          <Link href={`/countries/${a.security.country_iso3}`} className="hover:underline">
            {a.security.country_name}
          </Link>{" "}
          · {INSTRUMENT_LABEL[a.security.instrument_type]} · {formatTenor(a.security.tenor_days)}
        </p>
        <h1 className="mt-1 flex flex-wrap items-center gap-2 text-lg font-semibold">
          Auction of {formatDate(a.auction_date)} <StatusBadge status={a.status} />
        </h1>
        <p className="mt-1 text-sm">
          <Link href={`/securities/${a.security.security_id}`} className="text-accent hover:underline">
            {a.security.security_name}
          </Link>
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Official result</CardTitle>
            <NatureBadge nature={a.provenance.data_nature} />
          </CardHeader>
          <CardContent>
            <dl className="text-[13px]">
              <Row label="Auction type">{titleCase(a.auction_type)}</Row>
              <Row label="Announced"><Field value={formatDate(a.announcement_date)} /></Row>
              <Row label="Settlement"><Field value={formatDate(a.settlement_date)} /></Row>
              <Row label="Offered"><Field value={formatAmount(o.amount_offered, cur)} status={fs.amount_offered} /></Row>
              <Row label="Submitted"><Field value={formatAmount(o.amount_submitted, cur)} status={fs.amount_submitted} /></Row>
              <Row label="Allocated"><Field value={formatAmount(o.amount_allocated, cur)} status={fs.amount_allocated} /></Row>
              <Row label="Weighted avg. yield"><Field value={formatPct(o.weighted_average_yield)} status={fs.weighted_average_yield} /></Row>
              <Row label="Cut-off (accepted) yield"><Field value={formatPct(o.cutoff_yield)} status={fs.cutoff_yield} /></Row>
              <Row label="Bid range">
                <Field
                  value={o.minimum_bid && o.maximum_bid ? `${formatPct(o.minimum_bid)} – ${formatPct(o.maximum_bid)}` : null}
                  status={fs.minimum_bid}
                />
              </Row>
              <Row label="Average price"><Field value={o.average_price} status={fs.average_price} /></Row>
              <Row label="Reported bid-to-cover"><Field value={formatRatio(o.reported_bid_to_cover)} status={fs.reported_bid_to_cover} /></Row>
              <Row label="Bidders (successful)">
                <Field
                  value={o.number_of_bidders !== null ? `${o.number_of_bidders} (${o.number_of_successful_bidders ?? "?"})` : null}
                  status={fs.number_of_bidders}
                />
              </Row>
              <Row label="Yield convention"><Field value={o.yield_convention} status={fs.yield_convention} /></Row>
            </dl>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Calculated</CardTitle>
            <NatureBadge nature="CALCULATION" />
          </CardHeader>
          <CardContent>
            <dl className="text-[13px]">
              <Row label="Bid-to-cover" title={a.calculated.bid_to_cover_definition}>
                <Field value={formatRatio(a.calculated.bid_to_cover)} status={fs.amount_submitted} />
              </Row>
              <Row label="Allocation rate" title={a.calculated.allocation_rate_definition}>
                <Field value={formatShare(a.calculated.allocation_rate)} status={fs.amount_allocated} />
              </Row>
              <Row label="Acceptance rate" title={a.calculated.acceptance_rate_definition}>
                <Field value={formatShare(a.calculated.acceptance_rate)} status={fs.amount_allocated} />
              </Row>
              <Row label="Yield change vs previous" title={a.comparison.yield_change_definition}>
                <Field value={formatBps(a.comparison.yield_change_bps)} />
              </Row>
              <Row label={`Peer avg. bid-to-cover (n=${a.comparison.peer_count})`}>
                <Field value={formatRatio(a.comparison.peer_average_bid_to_cover)} />
              </Row>
            </dl>
            <ul className="mt-3 space-y-1 text-xs text-muted">
              <li>Bid-to-cover = {a.calculated.bid_to_cover_definition}</li>
              <li>Allocation = {a.calculated.allocation_rate_definition}</li>
              <li>Acceptance = {a.calculated.acceptance_rate_definition}</li>
              <li>Peers: {a.comparison.peer_definition}</li>
            </ul>
            {a.comparison.caveat && (
              <p className="mt-2 text-xs text-warning">
                <span aria-hidden>⚠ </span>
                {a.comparison.caveat}
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Source & provenance</CardTitle>
          </CardHeader>
          <CardContent>
            <ProvenancePanel p={a.provenance} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Historical comparison — previous comparable auctions</CardTitle>
        </CardHeader>
        <AuctionTable auctions={a.peers} caption="Previous comparable auctions" />
      </Card>
    </div>
  );
}
