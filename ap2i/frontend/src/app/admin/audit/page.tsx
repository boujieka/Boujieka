import { FilterBar, one, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { qs } from "@/lib/utils";

interface Log { id: number; at: string; user_id: number | null; organization_id: number | null; action: string; entity_type: string | null; entity_id: string | null; method: string | null; path: string | null; status_code: number | null; ip_truncated: string | null; detail: unknown }

export default async function AuditPage({ searchParams }: { searchParams: SP }) {
  const { d } = await getI18n();
  const action = one((await searchParams).action);
  const r = await apiGet<Log[]>(`/admin/audit-logs${qs({ action, limit: 300 })}`);
  return (
    <div>
      <PageHeader title={d.admin.audit} />
      <FilterBar d={d} action="/admin/audit" fields={[{ name: "action", label: d.admin.action, type: "text", value: action, placeholder: "auth.login" }]} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.audit}>
            <THead><TR><TH>ID</TH><TH>{d.admin.at}</TH><TH>{d.admin.action}</TH><TH>{d.admin.user}</TH><TH>{d.admin.entity}</TH><TH>{d.admin.path}</TH><TH>HTTP</TH><TH>IP</TH><TH>{d.common.details}</TH></TR></THead>
            <TBody>{r.data.map((x) => (
              <TR key={x.id}><TD>{x.id}</TD><TD className="whitespace-nowrap"><DateV value={x.at} time /></TD><TD className="font-mono text-xs">{x.action}</TD><TD><V value={x.user_id} /></TD><TD className="text-xs">{x.entity_type ? `${x.entity_type}:${x.entity_id ?? ""}` : "—"}</TD>
                <TD className="font-mono text-xs">{x.method} {x.path}</TD><TD><V value={x.status_code} /></TD><TD className="text-xs"><V value={x.ip_truncated} /></TD><TD className="max-w-64 truncate font-mono text-xs" title={JSON.stringify(x.detail)}>{x.detail ? JSON.stringify(x.detail) : "—"}</TD></TR>))}
            </TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
