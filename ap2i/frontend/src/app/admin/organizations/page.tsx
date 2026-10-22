import { OrgForm } from "@/components/admin/forms";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface O { id: number; name: string; short_name: string | null; org_type: string; is_tenant: boolean; iati_ref: string | null; created_at: string }

export default async function OrgsPage() {
  const { d } = await getI18n();
  const r = await apiGet<O[]>("/admin/organizations");
  return (
    <div className="space-y-4">
      <PageHeader title={d.admin.organizations} />
      <Card><CardHeader title={d.admin.createOrg} /><CardBody><OrgForm /></CardBody></Card>
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.organizations}>
            <THead><TR><TH>ID</TH><TH>{d.common.name}</TH><TH>{d.admin.shortName}</TH><TH>{d.admin.orgType}</TH><TH>{d.admin.isTenant}</TH><TH>IATI</TH><TH>{d.auth.created}</TH></TR></THead>
            <TBody>{r.data.map((o) => <TR key={o.id}><TD>{o.id}</TD><TD>{o.name}</TD><TD><V value={o.short_name} /></TD><TD>{o.org_type}</TD><TD>{o.is_tenant ? d.common.yes : d.common.no}</TD><TD><V value={o.iati_ref} /></TD><TD><DateV value={o.created_at} /></TD></TR>)}</TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
