import Link from "next/link";
import { CoverageNotice } from "@/components/coverage";
import { one, type SP } from "@/components/filter-bar";
import { Kpi, PageHeader } from "@/components/page-header";
import { ReportButton } from "@/components/report-button";
import { CreatePlan } from "@/components/rescue/create-plan";
import { ErrorState, LoginRequired, UpgradeRequired } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, Pct } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet, getMe, hasFeature } from "@/lib/api";

interface Dash { plans: number; actions: number; by_approval: Record<string, number>; by_implementation: Record<string, number>; by_priority: Record<string, number>; overdue_action_ids: number[] }
interface PlanRow { id: number; title: string; status: string; project_id: number; updated_at: string; summary: { actions: number; approved: number; done: number; completion_rate: number | null } }

export const metadata = { title: "Project Rescue" };

export default async function RescuePage({ searchParams }: { searchParams: SP }) {
  const { d } = await getI18n();
  const project = one((await searchParams).project);
  const me = await getMe();
  const header = <PageHeader title={d.rescue.title} subtitle={d.rescue.subtitle} />;
  if (!me) return <div>{header}<LoginRequired d={d} next={`/rescue${project ? `?project=${encodeURIComponent(project)}` : ""}`} /></div>;
  if (!hasFeature(me, "project_rescue")) return <div>{header}<UpgradeRequired d={d} /></div>;
  const [dash, plans] = await Promise.all([apiGet<Dash>("/rescue/dashboard"), apiGet<PlanRow[]>("/rescue/plans")]);
  if (!dash.ok && dash.status === 403) return <div>{header}<UpgradeRequired d={d} detail={dash.error} /></div>;
  const groups: [string, Record<string, number>, Record<string, string>][] = dash.ok
    ? [[d.rescue.byApproval, dash.data.by_approval, d.rescue.approvalStatus], [d.rescue.byImplementation, dash.data.by_implementation, d.rescue.implStatus], [d.rescue.byPriority, dash.data.by_priority, {}]]
    : [];
  return (
    <div className="space-y-6">
      {header}
      <CoverageNotice d={d} />
      {!dash.ok ? <ErrorState d={d} status={dash.status} message={dash.error} /> : (
        <>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <Kpi label={d.rescue.plans} value={dash.data.plans} />
            <Kpi label={d.rescue.actions} value={dash.data.actions} />
            <Kpi label={d.rescue.overdue} value={dash.data.overdue_action_ids.length} />
            <div className="flex items-center"><ReportButton request={{ report_type: "project_rescue", format: "pdf", country: "CMR" }} label={d.rescue.downloadReport} busyLabel={d.reports.generating} variant="outline" /></div>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {groups.map(([t, m, labels]) => (
              <Card key={t}><CardHeader title={t} /><CardBody>{Object.keys(m).length ? <ul className="space-y-1 text-sm">{Object.entries(m).map(([k, v]) => <li key={k} className="flex justify-between"><span>{label(labels, k)}</span><span className="tabular-nums">{v}</span></li>)}</ul> : <p className="text-sm text-muted">{d.common.none}</p>}</CardBody></Card>
            ))}
          </div>
        </>
      )}
      <div className="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
        <Card>
          <CardHeader title={d.rescue.plans} />
          {!plans.ok ? <CardBody><ErrorState d={d} status={plans.status} message={plans.error} /></CardBody> : plans.data.length === 0 ? <CardBody><p className="text-sm text-muted">{d.rescue.noPlans}</p></CardBody> : (
            <Table caption={d.rescue.plans}>
              <THead><TR><TH>{d.rescue.plan}</TH><TH>{d.common.status}</TH><TH className="text-right">{d.rescue.actions}</TH><TH className="text-right">{d.rescue.approvedCount}</TH><TH className="text-right">{d.rescue.completion}</TH><TH>{d.common.lastUpdate}</TH></TR></THead>
              <TBody>{plans.data.map((p) => (
                <TR key={p.id}><TD className="min-w-56"><Link className="link" href={`/rescue/plans/${p.id}`}>{p.title}</Link></TD><TD><Badge tone="navy">{p.status}</Badge></TD><TD className="text-right">{p.summary.actions}</TD><TD className="text-right">{p.summary.approved}</TD><TD className="text-right"><Pct value={p.summary.completion_rate} digits={0} /></TD><TD><DateV value={p.updated_at} /></TD></TR>))}
              </TBody>
            </Table>
          )}
        </Card>
        <Card>
          <CardHeader title={d.rescue.createTitle} />
          <CardBody><CreatePlan initialProject={project} hasOrg={!!me.organization} /></CardBody>
        </Card>
      </div>
    </div>
  );
}
