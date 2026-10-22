import Link from "next/link";
import { LEVEL_COLOR, LEVEL_ORDER, LevelBadge, ReviewBadge } from "@/components/badges";
import { AlertReview } from "@/components/alert-review";
import { CoverageNotice } from "@/components/coverage";
import { FilterBar, one, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { Pagination } from "@/components/pagination";
import { ErrorState } from "@/components/states";
import { Alert as Notice } from "@/components/ui/alert";
import { Card, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet, getMe, hasPermission } from "@/lib/api";
import { refData } from "@/lib/refdata";
import type { Alert } from "@/lib/types";
import { qs } from "@/lib/utils";

interface AlertList { total: number; items: Alert[]; summary_by_level: Record<string, number>; disclaimer: string }
interface Rule { code: string; label: string; indicator: string; thresholds: Record<string, string> }

export const metadata = { title: "Performance" };
const LIMIT = 100;

export default async function PerformancePage({ searchParams }: { searchParams: SP }) {
  const { d, locale } = await getI18n();
  const sp = await searchParams;
  const f = { country: one(sp.country), level: one(sp.level), rule: one(sp.rule), partner: one(sp.partner), review_status: one(sp.review_status) };
  const offset = Math.max(0, Number(one(sp.offset) ?? 0) || 0);
  const [alerts, rules, ref, me] = await Promise.all([apiGet<AlertList>(`/alerts${qs({ ...f, limit: LIMIT, offset })}`), apiGet<Rule[]>("/alerts/rules"), refData(locale), getMe()]);
  const canReview = hasPermission(me, "data:review");
  const levelOpts: [string, string][] = LEVEL_ORDER.map((l) => [l, label(d.alertLevel, l)]);
  if (f.level && !levelOpts.some(([k]) => k === f.level)) levelOpts.push([f.level, f.level.split(",").map((l) => label(d.alertLevel, l)).join(" + ")]);
  return (
    <div className="space-y-6">
      <PageHeader title={d.performance.title} subtitle={d.performance.subtitle} />
      <Notice tone="warning" title={d.performance.disclaimer}>{alerts.ok ? <p className="text-xs">API: “{alerts.data.disclaimer}”</p> : null}</Notice>
      <CoverageNotice d={d} />
      <FilterBar d={d} action="/performance" fields={[
        { name: "level", label: d.performance.level, type: "select", options: levelOpts, value: f.level },
        { name: "rule", label: d.performance.rule, type: "select", options: rules.ok ? rules.data.map((r) => [r.code, r.label]) : [], value: f.rule },
        { name: "partner", label: d.common.partner, type: "select", options: ref.partners, value: f.partner },
        { name: "review_status", label: d.performance.reviewStatus, type: "select", options: Object.entries(d.reviewStatus), value: f.review_status },
        { name: "country", label: d.common.country, type: "select", options: [["CMR", locale === "fr" ? "Cameroun" : "Cameroon"]], value: f.country },
      ]} />
      {!alerts.ok ? <ErrorState d={d} status={alerts.status} message={alerts.error} /> : (
        <>
          <section aria-label={d.performance.summary} className="grid grid-cols-2 gap-3 md:grid-cols-4">
            {LEVEL_ORDER.map((l) => (
              <Link key={l} href={`/performance${qs({ ...f, level: l })}`} className="rounded-lg border border-line bg-white p-4 no-underline shadow-sm hover:border-navy" style={{ borderLeft: `6px solid ${LEVEL_COLOR[l]}` }}>
                <div className="text-xs font-semibold uppercase text-muted">{label(d.alertLevel, l)}</div>
                <div className="text-2xl font-bold text-navy tabular-nums">{alerts.data.summary_by_level[l] ?? 0}</div>
              </Link>
            ))}
          </section>
          <Card>
            <Pagination d={d} base="/performance" params={f} total={alerts.data.total} limit={LIMIT} offset={offset} />
            {alerts.data.items.length === 0 ? <p className="px-4 pb-4 text-sm text-muted">{d.performance.noAlerts}</p> : (
              <Table caption={d.performance.title}>
                <THead><TR><TH>{d.performance.level}</TH><TH>{d.common.project}</TH><TH>{d.performance.rule}</TH><TH>{d.project.observed}</TH><TH>{d.project.threshold}</TH><TH>{d.project.recommendedVerification}</TH><TH>{d.performance.reviewStatus}</TH></TR></THead>
                <TBody>{alerts.data.items.map((a) => (
                  <TR key={a.id}>
                    <TD><LevelBadge value={a.level} /><div className="mt-1 font-mono text-xs text-muted">{a.alert_id}</div><div className="text-xs"><DateV value={a.as_of} /></div></TD>
                    <TD className="min-w-56">{a.project ? <Link className="link" href={`/projects/${a.project.ap2i_id}#alerts`}>{a.project.title}</Link> : null}<div className="font-mono text-xs text-muted">{a.project?.ap2i_id}</div></TD>
                    <TD className="font-mono text-xs"><Link className="link" href={`/performance${qs({ ...f, rule: a.rule_code })}`}>{a.rule_code}</Link></TD>
                    <TD className="min-w-56 text-xs">{a.observed_value}<div className="mt-1 text-muted">{(a.source_record_ids ?? []).map((id) => <Link key={id} className="link mr-1" href={`/sources/${id}`}>#{id}</Link>)}</div></TD>
                    <TD className="min-w-40 text-xs">{a.threshold}</TD>
                    <TD className="min-w-64 text-xs">{a.recommended_verification}</TD>
                    <TD><ReviewBadge value={a.review_status} />{a.review_note ? <div className="text-xs text-muted">{a.review_note}</div> : null}{canReview ? <AlertReview id={a.id} current={a.review_status} /> : null}</TD>
                  </TR>))}
                </TBody>
              </Table>
            )}
            <Pagination d={d} base="/performance" params={f} total={alerts.data.total} limit={LIMIT} offset={offset} />
          </Card>
        </>
      )}
      <Card>
        <CardHeader title={d.performance.catalogue} />
        {rules.ok ? (
          <Table caption={d.performance.catalogue}>
            <THead><TR><TH>{d.common.code}</TH><TH>{d.common.name}</TH><TH>{d.performance.indicator}</TH><TH>{d.performance.thresholds}</TH></TR></THead>
            <TBody>{rules.data.map((r) => (
              <TR key={r.code}><TD className="font-mono text-xs"><Link className="link" href={`/performance?rule=${r.code}`}>{r.code}</Link></TD><TD>{r.label}</TD><TD className="font-mono text-xs">{r.indicator}</TD>
                <TD className="text-xs">{Object.keys(r.thresholds).length ? Object.entries(r.thresholds).map(([k, v]) => <div key={k}>{k} = <span className="font-mono">{v}</span></div>) : "—"}</TD></TR>))}
            </TBody>
          </Table>
        ) : <ErrorState d={d} status={rules.status} message={rules.error} />}
      </Card>
    </div>
  );
}
