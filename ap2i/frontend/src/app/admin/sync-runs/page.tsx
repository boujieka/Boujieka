import Link from "next/link";
import { FilterBar, one, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { qs } from "@/lib/utils";

export interface Run { id: number; trigger: string; status: string; started_at: string; finished_at: string | null; params: unknown; records_retrieved: number; records_new: number; records_unchanged: number; records_imported: number; records_review: number; records_failed: number; connector: string; errors?: unknown; log?: unknown }

export default async function SyncRunsPage({ searchParams }: { searchParams: SP }) {
  const { d } = await getI18n();
  const connector = one((await searchParams).connector);
  const r = await apiGet<Run[]>(`/admin/sync-runs${qs({ connector, limit: 200 })}`);
  const keys = r.ok ? [...new Set(r.data.map((x) => x.connector))].sort() : [];
  return (
    <div>
      <PageHeader title={d.admin.syncRuns} />
      <FilterBar d={d} action="/admin/sync-runs" fields={[{ name: "connector", label: d.project.connector, type: "select", options: keys.map((k) => [k, k]), value: connector }]} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.syncRuns}>
            <THead><TR><TH>ID</TH><TH>{d.project.connector}</TH><TH>{d.common.status}</TH><TH>{d.admin.trigger}</TH><TH>{d.admin.started}</TH><TH>{d.admin.finished}</TH><TH className="text-right">{d.admin.retrieved}</TH><TH className="text-right">{d.admin.imported}</TH><TH className="text-right">{d.admin.reviewCount}</TH><TH className="text-right">{d.admin.failed}</TH></TR></THead>
            <TBody>{r.data.map((x) => (
              <TR key={x.id}><TD><Link className="link" href={`/admin/sync-runs/${x.id}`}>#{x.id}</Link></TD><TD className="font-mono text-xs">{x.connector}</TD><TD><Badge tone={x.status === "success" ? "emerald" : x.status === "failed" ? "danger" : "gold"}>{x.status}</Badge></TD><TD>{x.trigger}</TD>
                <TD className="whitespace-nowrap"><DateV value={x.started_at} time /></TD><TD className="whitespace-nowrap"><DateV value={x.finished_at} time /></TD><TD className="text-right">{x.records_retrieved}</TD><TD className="text-right">{x.records_imported}</TD><TD className="text-right">{x.records_review}</TD><TD className="text-right">{x.records_failed}</TD></TR>))}
            </TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
