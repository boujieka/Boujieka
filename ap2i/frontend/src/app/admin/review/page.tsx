import Link from "next/link";
import { ActionButton } from "@/components/admin/action-button";
import { FilterBar, one, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV } from "@/components/value";
import { VerificationBadge } from "@/components/badges";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { qs } from "@/lib/utils";

interface Rec { id: number; source_identifier: string; record_type: string; country_iso3: string | null; source_url: string | null; retrieved_at: string; processing_status: string; processing_note: string | null; verification_status: string; connector: string; issues: { id: number; rule: string; severity: string; message: string; status: string }[] }

export default async function ReviewPage({ searchParams }: { searchParams: SP }) {
  const { d } = await getI18n();
  const sp = await searchParams;
  const f = { status: one(sp.status) ?? "review", connector: one(sp.connector) };
  const r = await apiGet<{ total: number; items: Rec[] }>(`/admin/review/records${qs({ ...f, limit: 200 })}`);
  return (
    <div>
      <PageHeader title={d.admin.review} subtitle={r.ok ? `${r.data.total} ${d.common.results}` : undefined} />
      <FilterBar d={d} action="/admin/review" fields={[
        { name: "status", label: d.common.status, type: "select", options: [["imported", "imported"], ["rejected", "rejected"], ["failed", "failed"]], value: f.status === "review" ? undefined : f.status, allLabel: "review" },
        { name: "connector", label: d.project.connector, type: "text", value: f.connector },
      ]} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          {r.data.items.length === 0 ? <p className="p-4 text-sm text-muted">{d.common.none}</p> : (
            <Table caption={d.admin.review}>
              <THead><TR><TH>{d.project.sourceRecord}</TH><TH>{d.project.connector}</TH><TH>{d.admin.issues}</TH><TH>{d.common.verification}</TH><TH>{d.common.actions}</TH></TR></THead>
              <TBody>{r.data.items.map((x) => (
                <TR key={x.id}>
                  <TD className="min-w-56"><Link className="link font-mono text-xs" href={`/sources/${x.id}`}>#{x.id} {x.source_identifier}</Link><div className="text-xs text-muted">{x.record_type} · {x.country_iso3} · <DateV value={x.retrieved_at} /></div>{x.processing_note ? <div className="text-xs">{x.processing_note}</div> : null}</TD>
                  <TD className="font-mono text-xs">{x.connector}</TD>
                  <TD className="min-w-64 text-xs">{x.issues.length ? <ul className="space-y-1">{x.issues.map((i) => <li key={i.id}><Badge tone={i.severity === "error" ? "danger" : "gold"}>{i.severity}</Badge> {i.rule}: {i.message} <span className="text-muted">({i.status})</span></li>)}</ul> : "—"}</TD>
                  <TD><VerificationBadge value={x.verification_status} /></TD>
                  <TD className="space-x-1 whitespace-nowrap"><ActionButton path={`admin/review/records/${x.id}`} body={{ decision: "verified" }} variant="secondary">{d.admin.verify}</ActionButton><ActionButton path={`admin/review/records/${x.id}`} body={{ decision: "rejected" }} variant="danger">{d.admin.reject}</ActionButton></TD>
                </TR>))}
              </TBody>
            </Table>
          )}
        </Card>
      )}
    </div>
  );
}
