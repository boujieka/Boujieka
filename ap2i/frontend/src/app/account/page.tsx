import { ApiKeys, MfaTools } from "@/components/account-tools";
import { PageHeader } from "@/components/page-header";
import { LoginRequired } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet, getMe, hasFeature } from "@/lib/api";

export const metadata = { title: "Account" };

export default async function AccountPage() {
  const { d } = await getI18n();
  const me = await getMe();
  if (!me) return <LoginRequired d={d} next="/account" />;
  const keys = await apiGet<{ id: number; name: string; prefix: string; created_at: string; revoked_at: string | null; last_used_at: string | null }[]>("/auth/api-keys");
  return (
    <div className="space-y-6">
      <PageHeader title={d.auth.accountTitle} subtitle={`${me.full_name} · ${me.email}`} />
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title={d.common.details} />
          <CardBody>
            <dl className="divide-y divide-line text-sm">
              <div className="grid grid-cols-2 py-1.5"><dt className="text-muted">{d.auth.emailVerified}</dt><dd>{me.email_verified ? d.common.yes : d.common.no}</dd></div>
              <div className="grid grid-cols-2 py-1.5"><dt className="text-muted">{d.auth.organization}</dt><dd>{me.organization?.name ?? d.common.na}</dd></div>
              <div className="grid grid-cols-2 py-1.5"><dt className="text-muted">{d.auth.roles}</dt><dd className="flex flex-wrap gap-1">{me.roles.map((r) => <Badge key={r} tone="navy">{r}</Badge>)}</dd></div>
              <div className="grid grid-cols-2 py-1.5"><dt className="text-muted">{d.auth.features}</dt><dd className="flex flex-wrap gap-1">{(me.features ?? []).map((f) => <Badge key={f} tone="outline">{label(d.pricing.feature, f)}</Badge>)}</dd></div>
              <div className="grid grid-cols-2 py-1.5"><dt className="text-muted">{d.auth.permissions}</dt><dd className="flex flex-wrap gap-1">{(me.permissions ?? []).map((p) => <Badge key={p} tone="outline">{p}</Badge>)}</dd></div>
            </dl>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={d.auth.mfa} description={me.mfa_enabled ? d.auth.mfaEnabled : d.auth.mfaDisabled} />
          <CardBody><MfaTools enabled={me.mfa_enabled} /></CardBody>
        </Card>
      </div>
      <Card>
        <CardHeader title={d.auth.apiKeys} />
        <CardBody><ApiKeys keys={keys.ok ? keys.data : []} canCreate={hasFeature(me, "api_access")} /></CardBody>
      </Card>
    </div>
  );
}
