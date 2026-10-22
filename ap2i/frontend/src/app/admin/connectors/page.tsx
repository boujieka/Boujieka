import Link from "next/link";
import { ConnectorActions } from "@/components/admin/connector-row-actions";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, Num, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet, getMe, hasPermission } from "@/lib/api";

interface Conn {
  id: number; key: string; name: string; tier: number; enabled: boolean; status: string; status_evidence: string | null; access_method: string | null; base_url: string | null; documentation_url: string | null;
  usage_terms: string | null; update_frequency: string | null; config: Record<string, unknown> | null; schedule_cron: string | null; last_success_at: string | null; last_failure_at: string | null; last_error: string | null; notes: string | null;
  records_stored: number; records_requiring_review: number; last_run: { id: number; status: string; started_at: string; finished_at: string | null; records_retrieved: number; records_imported: number; records_review: number; records_failed: number } | null;
}

export default async function ConnectorsPage() {
  const { d } = await getI18n();
  const [r, me] = await Promise.all([apiGet<Conn[]>("/admin/connectors"), getMe()]);
  const admin = hasPermission(me, "admin:all");
  return (
    <div>
      <PageHeader title={d.admin.connectors} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.connectors}>
            <THead><TR><TH>{d.common.name}</TH><TH>{d.common.status}</TH><TH className="text-right">{d.explorer.records}</TH><TH>{d.explorer.lastSuccess} / {d.explorer.lastFailure}</TH><TH>{d.explorer.lastRun}</TH><TH>{d.admin.schedule}</TH>{admin ? <TH>{d.common.actions}</TH> : null}</TR></THead>
            <TBody>{r.data.map((c) => (
              <TR key={c.key}>
                <TD className="min-w-64">
                  <div className="font-medium">{c.name}</div>
                  <div className="font-mono text-xs text-muted">{c.key} · tier {c.tier}</div>
                  <div className="text-xs text-muted">{d.admin.accessMethod}: {c.access_method ?? d.common.na}</div>
                  {c.base_url ? <div className="text-xs break-anywhere">{c.base_url}</div> : null}
                  {c.status_evidence ? <details className="text-xs"><summary className="cursor-pointer text-navy">{d.admin.statusEvidence}</summary><p>{c.status_evidence}</p>{c.usage_terms ? <p className="mt-1 text-muted">{c.usage_terms}</p> : null}</details> : null}
                </TD>
                <TD><Badge tone={c.status === "operational" ? "emerald" : c.status === "blocked" ? "danger" : "outline"}>{c.status}</Badge><div className="mt-1 text-xs">{d.explorer.enabled}: {c.enabled ? d.common.yes : d.common.no}</div></TD>
                <TD className="text-right"><Num value={c.records_stored} />{c.records_requiring_review ? <div className="text-xs"><Link className="link" href={`/admin/review?connector=${c.key}`}>{d.admin.reviewCount}: {c.records_requiring_review}</Link></div> : null}</TD>
                <TD className="whitespace-nowrap text-xs"><DateV value={c.last_success_at} time /><br /><DateV value={c.last_failure_at} time />{c.last_error ? <div className="max-w-56 whitespace-normal text-danger break-anywhere">{c.last_error}</div> : null}</TD>
                <TD className="text-xs">{c.last_run ? <><Link className="link" href={`/admin/sync-runs/${c.last_run.id}`}>#{c.last_run.id}</Link> {c.last_run.status}<div>{c.last_run.records_retrieved}/{c.last_run.records_imported}/{c.last_run.records_review}/{c.last_run.records_failed}</div></> : <V value={null} />}</TD>
                <TD className="font-mono text-xs"><V value={c.schedule_cron} /></TD>
                {admin ? <TD><ConnectorActions k={c.key} enabled={c.enabled} schedule={c.schedule_cron} status={c.status} /></TD> : null}
              </TR>))}
            </TBody>
          </Table>
          <p className="px-4 py-2 text-xs text-muted">{d.explorer.lastRun}: {d.admin.retrieved} / {d.admin.imported} / {d.admin.reviewCount} / {d.admin.failed}</p>
        </Card>
      )}
    </div>
  );
}
