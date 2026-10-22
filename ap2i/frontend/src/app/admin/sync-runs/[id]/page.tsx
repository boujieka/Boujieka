import { notFound } from "next/navigation";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { DateV } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import type { Run } from "../page";

export default async function RunPage({ params }: { params: Promise<{ id: string }> }) {
  const id = (await params).id;
  if (!/^\d+$/.test(id)) notFound();
  const { d } = await getI18n();
  const r = await apiGet<Run>(`/admin/sync-runs/${id}`);
  if (!r.ok) return r.status === 404 ? notFound() : <ErrorState d={d} status={r.status} message={r.error} />;
  const x = r.data;
  const stats: [string, number][] = [[d.admin.retrieved, x.records_retrieved], ["new", x.records_new], ["unchanged", x.records_unchanged], [d.admin.imported, x.records_imported], [d.admin.reviewCount, x.records_review], [d.admin.failed, x.records_failed]];
  return (
    <div className="space-y-4">
      <PageHeader eyebrow={d.admin.syncRuns} title={`#${x.id} · ${x.connector} · ${x.status}`} subtitle={<><DateV value={x.started_at} time /> → <DateV value={x.finished_at} time /> · {x.trigger}</>} />
      <Card><CardHeader title={d.admin.stats} /><CardBody><dl className="grid grid-cols-2 gap-2 text-sm sm:grid-cols-6">{stats.map(([k, v]) => <div key={k}><dt className="text-xs text-muted">{k}</dt><dd className="text-lg font-semibold">{v}</dd></div>)}</dl>
        <pre className="mt-3 overflow-auto rounded bg-gray-bg p-2 text-xs">{JSON.stringify(x.params, null, 2)}</pre></CardBody></Card>
      <Card><CardHeader title={d.admin.errors} /><CardBody><pre className="max-h-96 overflow-auto rounded bg-gray-bg p-2 text-xs">{JSON.stringify(x.errors ?? [], null, 2)}</pre></CardBody></Card>
      <Card><CardHeader title={d.admin.runLog} /><CardBody><pre className="max-h-[600px] overflow-auto whitespace-pre-wrap rounded bg-gray-bg p-2 text-xs">{typeof x.log === "string" ? x.log : JSON.stringify(x.log ?? null, null, 2)}</pre></CardBody></Card>
    </div>
  );
}
