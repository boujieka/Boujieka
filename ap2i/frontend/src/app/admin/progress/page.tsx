import Link from "next/link";
import { ActionButton } from "@/components/admin/action-button";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface Candidate {
  id: number;
  value_numeric: string | null;
  value_text: string | null;
  value_date: string | null;
  source_field: string | null;
  source_record_id: number | null;
  project: { id: number; ap2i_id: string; title: string; physical_progress_pct: string | null };
}

export default async function ProgressCandidatesPage() {
  const { d } = await getI18n();
  const c = await apiGet<Candidate[]>("/admin/progress-candidates");
  return (
    <div className="space-y-6">
      <PageHeader title={d.admin.progress} subtitle={d.admin.progressIntro} />
      {!c.ok ? <ErrorState d={d} status={c.status} message={c.error} /> : (
        <Card>
          <CardHeader title={`${d.admin.pendingOnly} (${c.data.length})`} />
          <Table caption={d.admin.progress}>
            <THead><TR><TH>AP²I</TH><TH>%</TH><TH>{d.admin.progressSentence}</TH><TH>{d.admin.at}</TH><TH>{d.common.actions}</TH></TR></THead>
            <TBody>{c.data.map((x) => (
              <TR key={x.id}>
                <TD className="min-w-48 text-xs"><Link className="link font-mono" href={`/projects/${x.project.ap2i_id}`}>{x.project.ap2i_id}</Link><div className="text-sm">{x.project.title}</div></TD>
                <TD className="font-semibold"><V value={x.value_numeric} /></TD>
                <TD className="text-xs">
                  <V value={x.value_text} />
                  <div className="text-muted">{x.source_field} · {x.source_record_id ? <Link className="link" href={`/sources/${x.source_record_id}`}>#{x.source_record_id}</Link> : null}</div>
                </TD>
                <TD><DateV value={x.value_date} /></TD>
                <TD className="flex flex-wrap gap-1">
                  <ActionButton path={`admin/progress-candidates/${x.id}`} body={{ decision: "accept" }} variant="secondary" confirm={`${d.admin.accept}: ${x.value_numeric}% → ${x.project.ap2i_id}?`}>{d.admin.accept}</ActionButton>
                  <ActionButton path={`admin/progress-candidates/${x.id}`} body={{ decision: "reject" }} variant="danger">{d.admin.reject}</ActionButton>
                </TD>
              </TR>))}
            </TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
