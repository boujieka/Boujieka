import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody } from "@/components/ui/card";
import { V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface Sys { database: boolean; redis: boolean | null; postgis_version: string | null; running_syncs: number; failed_runs_7d: number }

export default async function SystemPage() {
  const { d } = await getI18n();
  const r = await apiGet<Sys>("/admin/system");
  const ok = (b: boolean | null) => (b === null ? <V value={null} /> : <Badge tone={b ? "emerald" : "danger"}>{b ? "OK" : "KO"}</Badge>);
  return (
    <div>
      <PageHeader title={d.admin.system} />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card><CardBody>
          <dl className="grid gap-3 text-sm sm:grid-cols-2">
            <div className="flex justify-between"><dt>{d.admin.database}</dt><dd>{ok(r.data.database)}</dd></div>
            <div className="flex justify-between"><dt>{d.admin.redis}</dt><dd>{ok(r.data.redis)}</dd></div>
            <div className="flex justify-between"><dt>{d.admin.postgis}</dt><dd><V value={r.data.postgis_version} /></dd></div>
            <div className="flex justify-between"><dt>{d.admin.runningSyncs}</dt><dd>{r.data.running_syncs}</dd></div>
            <div className="flex justify-between"><dt>{d.admin.failedRuns}</dt><dd>{r.data.failed_runs_7d}</dd></div>
          </dl>
        </CardBody></Card>
      )}
    </div>
  );
}
