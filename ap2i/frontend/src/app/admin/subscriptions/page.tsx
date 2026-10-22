import { GrantForm } from "@/components/admin/forms";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface S { id: number; user_id: number | null; organization_id: number | null; status: string; starts_on: string | null; ends_on: string | null; seats: number | null; created_at: string; plan: string }

export default async function SubsPage() {
  const { d } = await getI18n();
  const [r, plans] = await Promise.all([apiGet<S[]>("/admin/subscriptions"), apiGet<{ code: string }[]>("/plans")]);
  return (
    <div className="space-y-4">
      <PageHeader title={d.admin.subscriptions} />
      <Card><CardHeader title={d.admin.grant} /><CardBody><GrantForm plans={plans.ok ? plans.data.map((p) => p.code) : []} /></CardBody></Card>
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.subscriptions}>
            <THead><TR><TH>ID</TH><TH>Plan</TH><TH>{d.common.status}</TH><TH>{d.admin.userId}</TH><TH>{d.admin.orgId}</TH><TH>{d.common.from}</TH><TH>{d.admin.endsOn}</TH><TH>{d.admin.seats}</TH></TR></THead>
            <TBody>{r.data.map((s) => <TR key={s.id}><TD>{s.id}</TD><TD>{s.plan}</TD><TD><Badge tone={s.status === "active" ? "emerald" : "gold"}>{s.status}</Badge></TD><TD><V value={s.user_id} /></TD><TD><V value={s.organization_id} /></TD><TD><DateV value={s.starts_on} /></TD><TD><DateV value={s.ends_on} /></TD><TD><V value={s.seats} /></TD></TR>)}</TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
