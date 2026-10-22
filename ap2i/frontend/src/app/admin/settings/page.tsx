import { SettingForm } from "@/components/admin/forms";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

export default async function SettingsPage() {
  const { d } = await getI18n();
  const r = await apiGet<{ stored: Record<string, unknown>; runtime: Record<string, unknown> }>("/admin/settings");
  return (
    <div className="space-y-4">
      <PageHeader title={d.admin.settings} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <>
          <Card><CardHeader title={d.admin.runtime} /><CardBody><dl className="grid gap-2 text-sm sm:grid-cols-2">{Object.entries(r.data.runtime).map(([k, v]) => <div key={k} className="flex justify-between gap-2"><dt className="font-mono text-xs">{k}</dt><dd className="text-right font-mono text-xs break-anywhere">{JSON.stringify(v)}</dd></div>)}</dl></CardBody></Card>
          <Card><CardHeader title={d.admin.stored} /><CardBody className="grid gap-4 md:grid-cols-2">{["ai", "rescue", "reports", "ui"].map((g) => <SettingForm key={g} group={g} initial={r.data.stored[g] ?? {}} />)}</CardBody></Card>
        </>
      )}
    </div>
  );
}
