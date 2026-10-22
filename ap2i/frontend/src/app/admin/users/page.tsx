import { RolesEditor } from "@/components/admin/forms";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface U { id: number; email: string; full_name: string; organization_id: number | null; is_active: boolean; email_verified_at: string | null; mfa_enabled: boolean; last_login_at: string | null; created_at: string; roles: string[] }

// The API exposes no role catalogue endpoint; these codes mirror backend app/reference/catalog.py ROLES.
const KNOWN_ROLES = ["public_visitor", "registered_user", "professional_subscriber", "government_analyst", "government_administrator", "dfi_analyst", "institutional_administrator", "data_contributor", "data_reviewer", "ap2i_super_admin"];

export default async function UsersPage() {
  const { d } = await getI18n();
  const r = await apiGet<U[]>("/admin/users");
  const roles = r.ok ? [...new Set([...KNOWN_ROLES, ...r.data.flatMap((u) => u.roles)])] : KNOWN_ROLES;
  return (
    <div>
      <PageHeader title={d.admin.users} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.admin.users}>
            <THead><TR><TH>ID</TH><TH>{d.auth.email}</TH><TH>{d.auth.organization}</TH><TH>{d.auth.emailVerified}</TH><TH>MFA</TH><TH>{d.admin.lastLogin}</TH><TH>{d.auth.roles}</TH></TR></THead>
            <TBody>{r.data.map((u) => (
              <TR key={u.id}><TD>{u.id}</TD><TD className="min-w-48">{u.email}<div className="text-xs text-muted">{u.full_name}</div></TD><TD><V value={u.organization_id} /></TD><TD><DateV value={u.email_verified_at} /></TD><TD>{u.mfa_enabled ? d.common.yes : d.common.no}</TD><TD><DateV value={u.last_login_at} time /></TD>
                <TD><RolesEditor userId={u.id} roles={u.roles} active={u.is_active} allRoles={roles} /></TD></TR>))}
            </TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
