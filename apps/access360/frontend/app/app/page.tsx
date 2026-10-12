"use client";

import { AlertTriangle, CalendarClock, Info, XCircle } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { ChartFrame, HBarsChart } from "@/components/charts";
import { Kpi } from "@/components/kpi";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { orgPath } from "@/lib/api";
import { date, moneyCompact, num } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { DashAgg, Dashboard } from "@/lib/types";

const STATUSES = ["validated", "warning", "failed_checks", "incomplete_inputs"] as const;

function Panel({ agg, demo, testId }: { agg: DashAgg; demo: boolean; testId: string }) {
  const { t, locale } = useI18n();
  const countries = Object.entries(agg.country_counts)
    .map(([country, n]) => ({ country, n }))
    .sort((a, b) => b.n - a.n);
  return (
    <section aria-labelledby={`${testId}-title`} className="flex flex-col gap-4 rounded-xl border border-border bg-surface-muted/50 p-4 sm:p-5" data-testid={testId}>
      <div className="flex flex-wrap items-center gap-2">
        <h2 id={`${testId}-title`} className="text-base font-semibold text-navy-900">
          {demo ? t("dash.demo") : t("dash.real")}
        </h2>
        <DemoBadge show={demo} />
      </div>
      {agg.projects === 0 ? (
        <p className="text-sm text-muted-foreground">{t("dash.noProjects")}</p>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-3">
            <Kpi label={t("dash.activeProjects")} value={num(agg.projects, locale)} sub={`${num(agg.projects_modelled, locale)} ${t("dash.modelled")}`} />
            <Kpi label={t("dash.pipelineCapex")} value={moneyCompact(agg.pipeline_capex_usd, "USD", locale)} />
            <Kpi label={t("dash.plannedConnections")} value={num(agg.planned_connections, locale)} />
            <Kpi label={t("dash.viabilityGap")} value={moneyCompact(agg.viability_gap_usd, "USD", locale)} />
          </div>
          <p className="text-xs text-subtle-foreground">{t("dash.usableNote")}</p>
          <Card>
            <CardHeader>
              <CardTitle>{t("dash.readiness")}</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="grid grid-cols-2 gap-2">
                {STATUSES.map((s) => (
                  <li key={s} className="flex items-center justify-between gap-2 rounded-md border border-border px-3 py-2">
                    <StatusBadge status={s} />
                    <span className="text-sm font-semibold tabular text-navy-900">{num(agg.status_counts[s] ?? 0, locale)}</span>
                  </li>
                ))}
                <li className="flex items-center justify-between gap-2 rounded-md border border-border px-3 py-2">
                  <StatusBadge status={null} />
                  <span className="text-sm font-semibold tabular text-navy-900">{num(agg.projects - agg.projects_modelled, locale)}</span>
                </li>
              </ul>
            </CardContent>
          </Card>
          <ChartFrame title={t("dash.countries")} height={Math.max(80, countries.length * 34 + 30)}>
            <HBarsChart data={countries} catKey="country" valKey="n" name={t("nav.projects")} locale={locale} />
          </ChartFrame>
        </>
      )}
    </section>
  );
}

const ALERT_ICON = { info: Info, warning: AlertTriangle, critical: XCircle } as const;

export default function DashboardPage() {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const dash = useApi<Dashboard>(org ? orgPath(org.id, "/dashboard") : null);

  return (
    <>
      <PageHeader title={t("dash.title")} lead={t("dash.separateNote")} />
      {dash.loading && !dash.data ? <Loading /> : null}
      {dash.error ? <ErrorBox error={dash.error} onRetry={dash.reload} /> : null}
      {dash.data ? (
        <div className="flex flex-col gap-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Panel agg={dash.data.real} demo={false} testId="panel-real" />
            <Panel agg={dash.data.demo} demo testId="panel-demo" />
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CalendarClock className="size-4 text-emerald-700" aria-hidden /> {t("dash.milestones")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {dash.data.milestones.length === 0 ? (
                  <p className="text-sm text-muted-foreground">{t("dash.noMilestones")}</p>
                ) : (
                  <TableWrap>
                    <Table>
                      <thead>
                        <tr>
                          <Th>{t("ms.due")}</Th>
                          <Th>{t("ms.title")}</Th>
                          <Th>{t("common.project")}</Th>
                          <Th>{t("common.status")}</Th>
                        </tr>
                      </thead>
                      <tbody>
                        {dash.data.milestones.map((m, i) => (
                          <tr key={i}>
                            <Td className="whitespace-nowrap">
                              {date(m.due_date, locale)}
                              {m.due_soon ? (
                                <Badge variant="gold" className="ml-2" title={t("dash.dueSoon")}>
                                  60d
                                </Badge>
                              ) : null}
                            </Td>
                            <Td>{m.title}</Td>
                            <Td className="text-muted-foreground">{m.project}</Td>
                            <Td>{t(`ms.status.${m.status}` as DictKey)}</Td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  </TableWrap>
                )}
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>{t("dash.alerts")}</CardTitle>
              </CardHeader>
              <CardContent>
                {dash.data.alerts.length === 0 ? (
                  <p className="text-sm text-muted-foreground">{t("dash.noAlerts")}</p>
                ) : (
                  <ul className="flex flex-col divide-y divide-border">
                    {dash.data.alerts.map((a, i) => {
                      const Icon = ALERT_ICON[a.level] ?? Info;
                      return (
                        <li key={i} className="flex items-start gap-2 py-2 text-sm">
                          <Icon
                            className={a.level === "critical" ? "mt-0.5 size-4 shrink-0 text-danger-700" : a.level === "warning" ? "mt-0.5 size-4 shrink-0 text-gold-700" : "mt-0.5 size-4 shrink-0 text-navy-700"}
                            aria-label={a.level}
                          />
                          <span>
                            <span className="font-medium text-navy-900">{a.project}</span>
                            <span className="text-muted-foreground"> · {a.text}</span>
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      ) : null}
    </>
  );
}
