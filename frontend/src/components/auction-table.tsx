import Link from "next/link";

import { Field } from "@/components/provenance";
import { Badge } from "@/components/ui/badge";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import {
  INSTRUMENT_LABEL,
  formatAmount,
  formatDate,
  formatPct,
  formatRatio,
  formatTenor,
} from "@/lib/format";
import type { Auction, AuctionStatus } from "@/lib/types";

const STATUS_VARIANT: Record<AuctionStatus, "neutral" | "good" | "warning" | "critical"> = {
  announced: "neutral",
  completed: "good",
  postponed: "warning",
  cancelled: "critical",
};

export function StatusBadge({ status }: { status: AuctionStatus }) {
  return <Badge variant={STATUS_VARIANT[status]}>{status}</Badge>;
}

export function AuctionTable({
  auctions,
  showResults = true,
  caption,
}: {
  auctions: Auction[];
  showResults?: boolean;
  caption?: string;
}) {
  if (auctions.length === 0) {
    return <p className="px-4 py-6 text-sm text-muted">No auctions match.</p>;
  }
  return (
    <Table>
      {caption && <caption className="sr-only">{caption}</caption>}
      <THead>
        <tr>
          <TH>Date</TH>
          <TH>Country</TH>
          <TH>Instrument</TH>
          <TH>Tenor</TH>
          <TH>Status</TH>
          <TH className="text-right">Offered</TH>
          {showResults && (
            <>
              <TH className="text-right">Submitted</TH>
              <TH className="text-right">WA yield</TH>
              <TH className="text-right" title="Calculated: submitted / offered">
                Bid/cover <span className="font-normal normal-case">(calc)</span>
              </TH>
            </>
          )}
          <TH>Data</TH>
        </tr>
      </THead>
      <TBody>
        {auctions.map((a) => (
          <TR key={a.auction_id}>
            <TD className="num">
              <Link href={`/auctions/${a.auction_id}`} className="text-accent hover:underline">
                {formatDate(a.auction_date)}
              </Link>
            </TD>
            <TD>
              <Link href={`/countries/${a.security.country_iso3}`} className="hover:underline">
                {a.security.country_name}
              </Link>
            </TD>
            <TD>
              <Link href={`/securities/${a.security.security_id}`} className="hover:underline">
                {INSTRUMENT_LABEL[a.security.instrument_type]}
              </Link>
              {a.auction_type !== "primary_auction" && (
                <span className="ml-1 text-xs text-muted">({a.auction_type.replace("_", " ")})</span>
              )}
            </TD>
            <TD className="num">{formatTenor(a.security.tenor_days)}</TD>
            <TD>
              <StatusBadge status={a.status} />
            </TD>
            <TD className="num text-right">
              <Field
                value={formatAmount(a.official.amount_offered, a.security.currency)}
                status={a.field_status.amount_offered}
              />
            </TD>
            {showResults && (
              <>
                <TD className="num text-right">
                  <Field
                    value={formatAmount(a.official.amount_submitted, a.security.currency)}
                    status={a.field_status.amount_submitted}
                  />
                </TD>
                <TD className="num text-right">
                  <Field
                    value={formatPct(a.official.weighted_average_yield)}
                    status={a.field_status.weighted_average_yield}
                  />
                </TD>
                <TD className="num text-right">
                  <Field
                    value={formatRatio(a.calculated.bid_to_cover)}
                    status={a.field_status.amount_submitted}
                  />
                </TD>
              </>
            )}
            <TD>
              {a.provenance.is_synthetic ? (
                <Badge variant="synthetic">SYNTHETIC</Badge>
              ) : (
                <Badge variant="fact">{a.provenance.verification_status}</Badge>
              )}
            </TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
