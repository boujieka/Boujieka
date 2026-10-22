import Link from "next/link";
import { ActionButton } from "@/components/admin/action-button";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface Brief { id: number; ap2i_id: string; title: string; status: string; approval: string | null; partners: string[]; executing_agency: string | null }
interface Match { id: number; score: number; features: Record<string, unknown>; relation: string; status: string; created_at: string; review_note: string | null; a: Brief; b: Brief }
interface Merge { id: number; survivor_id: number; merged_id: number; merged_by: number | null; merged_at: string; reason: string | null; reversed_at: string | null; reversed_by: number | null; match_candidate_id: number | null }

function P({ p }: { p: Brief }) {
  return <div className="min-w-56 text-xs"><Link className="link font-mono" href={`/projects/${p.ap2i_id}`}>{p.ap2i_id}</Link><div className="text-sm">{p.title}</div><div className="text-muted">{p.status} · {p.approval ?? "—"} · {p.partners.join(", ")} · {p.executing_agency ?? "—"}</div></div>;
}

export default async function MatchesPage() {
  const { d } = await getI18n();
  const [m, merges] = await Promise.all([apiGet<Match[]>("/admin/matches?status=pending"), apiGet<Merge[]>("/admin/merges")]);
  return (
    <div className="space-y-6">
      <PageHeader title={d.admin.matches} />
      {!m.ok ? <ErrorState d={d} status={m.status} message={m.error} /> : (
        <Card>
          <CardHeader title={`${d.admin.pendingOnly} (${m.data.length})`} />
          <Table caption={d.admin.matches}>
            <THead><TR><TH>{d.admin.score}</TH><TH>A</TH><TH>B</TH><TH>{d.admin.relation}</TH><TH>{d.common.actions}</TH></TR></THead>
            <TBody>{m.data.map((x) => (
              <TR key={x.id}>
                <TD className="font-semibold">{x.score}<div className="font-mono text-xs font-normal text-muted">{Object.entries(x.features).map(([k, v]) => <div key={k}>{k}: {String(v)}</div>)}</div></TD>
                <TD><P p={x.a} /></TD><TD><P p={x.b} /></TD><TD>{x.relation}</TD>
                <TD className="space-y-1">
                  <div className="text-xs text-muted">{d.admin.accept} — {d.admin.survivor}:</div>
                  <div className="flex flex-wrap gap-1">
                    <ActionButton path={`admin/matches/${x.id}`} body={{ decision: "accept", survivor: "a" }} variant="secondary" confirm={`${d.admin.accept}: ${x.a.ap2i_id} ← ${x.b.ap2i_id}?`}>A</ActionButton>
                    <ActionButton path={`admin/matches/${x.id}`} body={{ decision: "accept", survivor: "b" }} variant="secondary" confirm={`${d.admin.accept}: ${x.b.ap2i_id} ← ${x.a.ap2i_id}?`}>B</ActionButton>
                    <ActionButton path={`admin/matches/${x.id}`} body={{ decision: "reject" }} variant="danger">{d.admin.reject}</ActionButton>
                  </div>
                </TD>
              </TR>))}
            </TBody>
          </Table>
        </Card>
      )}
      <Card>
        <CardHeader title={d.admin.merges} />
        {!merges.ok ? <ErrorState d={d} status={merges.status} message={merges.error} /> : (
          <Table caption={d.admin.merges}>
            <THead><TR><TH>ID</TH><TH>{d.admin.survivor}</TH><TH>merged</TH><TH>{d.admin.at}</TH><TH>{d.common.note}</TH><TH>{d.admin.reversed}</TH><TH /></TR></THead>
            <TBody>{merges.data.map((x) => (
              <TR key={x.id}><TD>#{x.id}</TD><TD>{x.survivor_id}</TD><TD>{x.merged_id}</TD><TD><DateV value={x.merged_at} time /></TD><TD className="text-xs"><V value={x.reason} /></TD><TD>{x.reversed_at ? <DateV value={x.reversed_at} time /> : "—"}</TD>
                <TD>{x.reversed_at ? null : <ActionButton path={`admin/merges/${x.id}/reverse`} variant="danger" confirm={`${d.admin.reverse} #${x.id}?`}>{d.admin.reverse}</ActionButton>}</TD></TR>))}
            </TBody>
          </Table>
        )}
      </Card>
    </div>
  );
}
