import Link from "next/link";
import { notFound } from "next/navigation";
import { PageHeader } from "@/components/page-header";
import { ReportButton } from "@/components/report-button";
import { ActionCard } from "@/components/rescue/action-card";
import { ErrorState, LoginRequired, UpgradeRequired } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { DateV, Pct } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet, getMe, hasFeature } from "@/lib/api";
import type { RescuePlan } from "@/lib/types";

function DiagValue({ v }: { v: unknown }) {
  if (v === null || v === undefined) return <span className="italic text-muted">—</span>;
  if (typeof v === "string" || typeof v === "number" || typeof v === "boolean") return <span className="whitespace-pre-line">{String(v)}</span>;
  return <pre className="max-h-64 overflow-auto rounded bg-gray-bg p-2 text-xs">{JSON.stringify(v, null, 2)}</pre>;
}

export default async function PlanPage({ params }: { params: Promise<{ id: string }> }) {
  const id = (await params).id;
  if (!/^\d+$/.test(id)) notFound();
  const { d } = await getI18n();
  const me = await getMe();
  if (!me) return <LoginRequired d={d} next={`/rescue/plans/${id}`} />;
  if (!hasFeature(me, "project_rescue")) return <UpgradeRequired d={d} />;
  const r = await apiGet<RescuePlan>(`/rescue/plans/${id}`);
  if (!r.ok && r.status === 404) notFound();
  if (!r.ok) return <ErrorState d={d} status={r.status} message={r.error} />;
  const p = r.data;
  return (
    <div className="space-y-6">
      <PageHeader eyebrow={`${d.rescue.plan} #${p.id}`} title={p.title}
        subtitle={<><Link className="link" href={`/projects/${p.project.ap2i_id}`}>{p.project.ap2i_id}</Link> · {p.project.title}</>}
        actions={<ReportButton request={{ report_type: "project_rescue", format: "pdf", country: p.project.ap2i_id.split("-")[1] }} label={d.rescue.downloadReport} busyLabel={d.reports.generating} variant="outline" />} />
      <div className="flex flex-wrap gap-2 text-sm">
        <Badge tone="navy">{p.status}</Badge>{p.private ? <Badge tone="gold">private</Badge> : null}
        <span className="text-muted">{d.rescue.actions}: {p.summary.actions} · {d.rescue.approvedCount}: {p.summary.approved} · {d.rescue.doneCount}: {p.summary.done} · {d.rescue.completion}: <Pct value={p.summary.completion_rate} digits={0} /></span>
        <span className="text-muted">· <DateV value={p.updated_at} time /></span>
      </div>
      <Card>
        <CardHeader title={d.rescue.diagnosis} />
        <CardBody>
          {p.diagnosis ? <dl className="grid gap-2 text-sm sm:grid-cols-[200px_1fr]">{Object.entries(p.diagnosis).map(([k, v]) => <div key={k} className="contents"><dt className="font-semibold text-muted">{k}</dt><dd className="min-w-0 break-anywhere"><DiagValue v={v} /></dd></div>)}</dl> : <p className="text-sm italic text-muted">{d.common.na}</p>}
        </CardBody>
      </Card>
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-navy">{d.rescue.actions}</h2>
        {p.actions.length === 0 ? <p className="text-sm text-muted">{d.rescue.noActions}</p> : p.actions.map((a) => <ActionCard key={a.id} a={a} />)}
      </section>
    </div>
  );
}
