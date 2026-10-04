import { Kpi } from "@/components/kpi";
import { SourceTable } from "@/components/source-table";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { ApiError, api } from "@/lib/api";
import { formatDate, titleCase } from "@/lib/format";
import type { DataQualityReport, SourceOut } from "@/lib/types";

function Unauthorized({ status }: { status: number }) {
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Admin · Data quality</h1>
      <Card>
        <div className="space-y-2 px-4 py-3 text-sm">
          <p>
            <strong>{status === 401 ? "Not authorized." : "Access denied."}</strong> The data-quality report is
            restricted to analyst and admin API keys.
          </p>
          <p className="text-muted">
            {status === 401
              ? "Set ABI_API_KEY (server-side environment, never NEXT_PUBLIC_) to a valid, non-revoked key and restart the frontend."
              : "The configured ABI_API_KEY does not have the analyst or admin role."}{" "}
            See docs/SECURITY.md.
          </p>
        </div>
      </Card>
    </div>
  );
}

export default async function DataQualityPage() {
  let dq: DataQualityReport, sources: SourceOut[];
  try {
    [dq, sources] = await Promise.all([api.dataQuality(), api.sources()]);
  } catch (e) {
    if (e instanceof ApiError && (e.status === 401 || e.status === 403)) return <Unauthorized status={e.status} />;
    throw e;
  }
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-lg font-semibold">Admin · Data quality</h1>
        <p className="text-xs text-muted">As of {formatDate(dq.as_of)}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4 xl:grid-cols-7">
        <Kpi label="Sources" value={dq.sources_total} />
        <Kpi label="Pending configuration" value={dq.sources_pending_configuration.length} />
        <Kpi label="Failing crawlers" value={dq.sources_failing.length} hint="Crawlers arrive in Phase 2" />
        <Kpi label="Stale sources" value={dq.sources_stale.length} />
        <Kpi label="Unverified records" value={dq.unverified_records} />
        <Kpi label="Low-confidence records" value={dq.low_confidence_records} />
        <Kpi label="Duplicate candidates" value={dq.duplicate_candidates} hint={<span title={dq.duplicate_definition}>hover for definition</span>} />
      </div>

      <div className="rounded-md border border-[var(--nature-synthetic)] px-4 py-2 text-sm">
        <strong className="text-[var(--nature-synthetic)]">Synthetic data present:</strong> {dq.synthetic_auctions} auctions and{" "}
        {dq.synthetic_securities} securities are generated development data, not real market data.
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Missing fields — completed auctions</CardTitle>
        </CardHeader>
        <Table>
          <THead>
            <tr>
              <TH>Field</TH>
              <TH className="text-right">Missing</TH>
              <TH className="text-right">Not disclosed by source</TH>
              <TH className="text-right">No source (not available)</TH>
              <TH className="text-right">Completeness</TH>
            </tr>
          </THead>
          <TBody>
            {dq.auction_missing_fields.map((m) => (
              <TR key={m.field}>
                <TD>{titleCase(m.field)}</TD>
                <TD className="num text-right">{m.missing}</TD>
                <TD className="num text-right">{m.not_disclosed}</TD>
                <TD className="num text-right">{m.missing - m.not_disclosed - m.pending}</TD>
                <TD className="num text-right">{m.total ? `${(((m.total - m.missing) / m.total) * 100).toFixed(1)}%` : "—"}</TD>
              </TR>
            ))}
          </TBody>
        </Table>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Source registry & freshness</CardTitle>
        </CardHeader>
        <SourceTable sources={sources} />
      </Card>
    </div>
  );
}
