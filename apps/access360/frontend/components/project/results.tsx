"use client";

import { useEffect, useMemo, useState } from "react";
import { CheckCircle2, Loader2, Play, XCircle, AlertTriangle } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { BarsChart, ChartFrame, LinesChart } from "@/components/charts";
import { Kpi } from "@/components/kpi";
import { ErrorBox, Loading } from "@/components/page";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, orgPath } from "@/lib/api";
import { dateTime, money, ratio } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { ANNUAL_COLS, fmtMetric, label, RESULT_KPIS, SOURCES, USES } from "@/lib/metrics";
import { useSession } from "@/lib/session";
import type { Check, Project, RunDetail, RunSummary } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Text of a check row. Defensive: some backend rows carry the text in another field (see README, known issues). */
export function checkText(c: Check): { label: string; detail: string; passed: boolean } {
  const lbl = typeof c.label === "string" ? c.label : typeof c.passed === "string" ? c.passed : c.code;
  const detail = typeof c.detail === "string" ? c.detail : "";
  const passed = c.passed === true;
  return { label: lbl, detail, passed };
}

export function projectCurrency(p: Project): string {
  return typeof p.inputs?.currency === "string" && p.inputs.currency ? p.inputs.currency : "LCY";
}

function ChecksList({ items, kind }: { items: Check[]; kind: "checks" | "warnings" }) {
  const { t } = useI18n();
  if (!items.length) return <p className="text-sm text-muted-foreground">{t("common.none")}</p>;
  const nPassed = items.filter((c) => c.passed === true).length;
  return (
    <>
    {kind === "checks" ? (
      <p className={cn("mb-2 text-sm font-medium", nPassed === items.length ? "text-emerald-700" : "text-danger-700")} data-testid="checks-summary">
        {nPassed} / {items.length} {t("results.passed").toLowerCase()}
      </p>
    ) : null}
    <ul className="flex max-h-80 flex-col divide-y divide-border overflow-y-auto pr-1" data-testid={`${kind}-list`} tabIndex={0}>
      {[...items].sort((a, b) => Number(a.passed === true) - Number(b.passed === true)).map((c, i) => {
        const x = checkText(c);
        return (
          <li key={`${c.code}-${i}`} className="flex items-start gap-2 py-1.5 text-sm">
            {kind === "warnings" ? (
              <AlertTriangle className="mt-0.5 size-4 shrink-0 text-gold-700" aria-label={t("status.warning")} />
            ) : x.passed ? (
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-700" aria-label={t("results.passed")} />
            ) : (
              <XCircle className="mt-0.5 size-4 shrink-0 text-danger-700" aria-label={t("results.failed")} />
            )}
            <span className="min-w-0">
              <span className="text-foreground">{x.label}</span>
              {c.code.startsWith("R_") ? (
                <span className="ml-1.5 rounded bg-navy-50 px-1 py-px text-[10px] font-medium uppercase tracking-wide text-navy-700" title={t("results.recompute")}>
                  {t("results.recomputeShort")}
                </span>
              ) : null}
              {x.detail ? <span className="block text-xs text-subtle-foreground">{x.detail}</span> : null}
            </span>
            {kind === "checks" ? <span className={cn("ml-auto shrink-0 text-xs font-medium", x.passed ? "text-emerald-700" : "text-danger-700")}>{x.passed ? t("results.passed") : t("results.failed")}</span> : null}
          </li>
        );
      })}
    </ul>
    </>
  );
}

export function RunView({ run, project }: { run: RunDetail; project: Project }) {
  const { t, locale } = useI18n();
  const ccy = projectCurrency(project);
  const fmtL = (v: number) => money(v, ccy, locale);
  const years = useMemo(() => run.annual.year ?? [], [run]);

  const annualRows = useMemo(
    () =>
      years.map((y, i) => ({
        year: y,
        revenue: run.annual.revenue?.[i] ?? null,
        ebitda: run.annual.ebitda?.[i] ?? null,
        cfads: run.annual.cfads?.[i] ?? null,
        debt_service: run.annual.debt_service?.[i] ?? null,
        dscr: run.annual.dscr?.[i] ?? null,
      })),
    [run, years],
  );
  const quarterly = useMemo(() => {
    const dates = run.quarterly.date ?? [];
    const cash = (run.quarterly.cash as (number | null)[] | undefined) ?? [];
    const debt = (run.quarterly.debt_balance as (number | null)[] | undefined) ?? [];
    return dates.map((dt, i) => ({ date: dt.slice(0, 7), cash: cash[i] ?? null, debt_balance: debt[i] ?? null }));
  }, [run]);

  const fin = project.inputs?.financing;
  const lockup = run.inputs_version === project.inputs_version && fin && typeof fin === "object" && !Array.isArray(fin) && typeof fin.lockup_dscr === "number" ? fin.lockup_dscr : null;
  const hasDebt = annualRows.some((r) => (r.debt_service ?? 0) !== 0);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center gap-2 text-xs text-subtle-foreground">
        <StatusBadge status={run.status} />
        <DemoBadge show={run.is_demo} />
        <span>{dateTime(run.created_at, locale)}</span>
        <span>
          · {t("results.engine")} {run.engine_version}
        </span>
        <span className="break-all">
          · {t("results.inputsHash")} <span className="font-mono">{run.inputs_sha256.slice(0, 16)}…</span>
        </span>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>{t("results.checks")}</CardTitle>
          </CardHeader>
          <CardContent>
            <ChecksList items={run.checks} kind="checks" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{t("results.warnings")}</CardTitle>
          </CardHeader>
          <CardContent>
            <ChecksList items={run.warnings} kind="warnings" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{t("results.missing")}</CardTitle>
          </CardHeader>
          <CardContent>
            {run.missing_inputs.length ? (
              <ul className="list-disc pl-5 text-sm">
                {run.missing_inputs.map((m) => (
                  <li key={m} className="font-mono text-xs">
                    {m}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-muted-foreground">{t("common.none")}</p>
            )}
          </CardContent>
        </Card>
      </div>

      <section aria-labelledby="kpis-title">
        <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="kpis-title" className="text-base font-semibold text-navy-900">
            {t("results.kpis")}
          </h2>
          <span className="text-xs text-subtle-foreground">{t("results.currency", { ccy })}</span>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5" data-testid="kpi-grid">
          {RESULT_KPIS.map((m) => (
            <Kpi key={m.key} testId={`kpi-${m.key}`} label={label(m, locale)} value={fmtMetric(m.kind, run.metrics[m.key], ccy, locale)} />
          ))}
        </div>
      </section>

      <div className="grid gap-4 lg:grid-cols-2">
        <ChartFrame title={t("results.revenueChart")} subtitle={ccy} testId="chart-revenue">
          <LinesChart
            data={annualRows}
            xKey="year"
            locale={locale}
            valueFormat={fmtL}
            series={[
              { key: "revenue", name: locale === "fr" ? "Chiffre d'affaires" : "Revenue" },
              { key: "ebitda", name: "EBITDA" },
              { key: "cfads", name: "CFADS" },
            ]}
          />
        </ChartFrame>
        <ChartFrame title={t("results.debtServiceChart")} subtitle={ccy} testId="chart-debt-service">
          {hasDebt ? <BarsChart data={annualRows} xKey="year" yKey="debt_service" name={t("results.debtServiceChart")} locale={locale} valueFormat={fmtL} /> : <p className="text-sm text-muted-foreground">{t("common.dataUnavailable")}</p>}
        </ChartFrame>
        <ChartFrame title={t("results.dscrChart")} subtitle={lockup !== null ? `${t("results.lockup")} ${ratio(lockup, locale)}` : t("results.lockupUnknown")} testId="chart-dscr">
          <LinesChart
            data={annualRows}
            xKey="year"
            locale={locale}
            valueFormat={(v) => ratio(v, locale)}
            series={[{ key: "dscr", name: "DSCR" }]}
            refLine={lockup !== null ? { y: lockup, label: `${t("results.lockup")} ${ratio(lockup, locale)}` } : undefined}
          />
        </ChartFrame>
        <ChartFrame title={t("results.cashDebtChart")} subtitle={ccy} testId="chart-cash-debt">
          <LinesChart
            data={quarterly}
            xKey="date"
            locale={locale}
            valueFormat={fmtL}
            series={[
              { key: "cash", name: t("results.cash") },
              { key: "debt_balance", name: t("results.debtBalance") },
            ]}
          />
        </ChartFrame>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]">
        <Card>
          <CardHeader>
            <CardTitle>{t("results.sourcesUses")}</CardTitle>
          </CardHeader>
          <CardContent>
            <Table data-testid="sources-uses">
              <tbody>
                {[SOURCES, USES].map((group, gi) =>
                  group.map(([k, en, fr]) => {
                    const total = k.endsWith("_total");
                    return (
                      <tr key={k} className={cn(total && "font-semibold", total && gi === 0 && "border-b-2 border-border-strong")}>
                        <Td className={cn(!total && "pl-5")}>{locale === "fr" ? fr : en}</Td>
                        <Td className="text-right whitespace-nowrap">{money(run.sources_uses[k], ccy, locale)}</Td>
                      </tr>
                    );
                  }),
                )}
              </tbody>
            </Table>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{t("results.annualTable")}</CardTitle>
          </CardHeader>
          <CardContent>
            <TableWrap className="max-h-96">
              <Table className="text-xs">
                <thead className="sticky top-0 bg-surface">
                  <tr>
                    <Th>{t("results.year")}</Th>
                    {ANNUAL_COLS.map(([k, en, fr]) => (
                      <Th key={k} className="text-right">
                        {locale === "fr" ? fr : en}
                      </Th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {years.map((y, i) => (
                    <tr key={String(y)}>
                      <Td>{String(y)}</Td>
                      {ANNUAL_COLS.map(([k, , , kind]) => (
                        <Td key={k} className="text-right whitespace-nowrap">
                          {fmtMetric(kind === "lcy" ? "lcy" : kind === "ratio" ? "ratio" : "num", run.annual[k]?.[i], ccy, locale).replace(` ${ccy}`, "")}
                        </Td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </Table>
            </TableWrap>
            <p className="mt-2 text-xs text-subtle-foreground">{t("results.currency", { ccy })}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export function ResultsTab({ project, onRun }: { project: Project; onRun: () => void }) {
  const { org, canEdit } = useSession();
  const { t, locale } = useI18n();
  const base = org ? orgPath(org.id, `/projects/${project.id}`) : null;
  const runs = useApi<RunSummary[]>(base ? `${base}/runs` : null);
  const [selected, setSelected] = useState<string | null>(project.latest_run?.id ?? null);
  const [detail, setDetail] = useState<RunDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!base || !selected || detail?.id === selected) return;
    let alive = true;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetch lifecycle
    setLoading(true);
    api<RunDetail>(`${base}/runs/${selected}`)
      .then((r) => alive && (setDetail(r), setError(null)))
      .catch((e: unknown) => alive && setError(e instanceof Error ? e.message : String(e)))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [base, selected, detail?.id]);

  async function runModel() {
    if (!base) return;
    setRunning(true);
    setError(null);
    try {
      const r = await api<RunDetail>(`${base}/runs`, { method: "POST" });
      setDetail(r);
      setSelected(r.id);
      runs.reload();
      onRun();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={runModel} disabled={!canEdit || running || !project.has_inputs} variant="accent" data-testid="run-model">
          {running ? <Loader2 className="animate-spin" aria-hidden /> : <Play aria-hidden />}
          {running ? t("results.running") : t("results.run")}
        </Button>
        {!project.has_inputs ? <span className="text-sm text-muted-foreground">{t("results.noRun")}</span> : null}
        {project.latest_run && project.latest_run.inputs_version !== project.inputs_version ? <Alert variant="warning">{t("overview.inputsChanged")}</Alert> : null}
      </div>
      {error ? <ErrorBox error={error} /> : null}
      {loading && !detail ? <Loading /> : null}
      {!selected && !running ? <p className="text-sm text-muted-foreground">{t("results.noRun")}</p> : null}
      {detail ? <RunView run={detail} project={project} /> : null}

      {runs.data && runs.data.length > 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>{t("results.history")}</CardTitle>
          </CardHeader>
          <CardContent>
            <TableWrap>
              <Table>
                <thead>
                  <tr>
                    <Th>{t("common.date")}</Th>
                    <Th>{t("common.status")}</Th>
                    <Th>{t("results.engine")}</Th>
                    <Th className="text-right">Inputs v.</Th>
                    <Th className="text-right">Project IRR</Th>
                    <Th className="text-right">Min DSCR</Th>
                    <Th>
                      <span className="sr-only">{t("common.actions")}</span>
                    </Th>
                  </tr>
                </thead>
                <tbody>
                  {runs.data.map((r) => (
                    <tr key={r.id} className={cn(r.id === selected && "bg-navy-50")}>
                      <Td className="whitespace-nowrap">{dateTime(r.created_at, locale)}</Td>
                      <Td>
                        <span className="flex flex-wrap gap-1">
                          <StatusBadge status={r.status} />
                          {r.is_demo ? <DemoBadge /> : null}
                        </span>
                      </Td>
                      <Td>{r.engine_version}</Td>
                      <Td className="text-right">{r.inputs_version}</Td>
                      <Td className="text-right">{fmtMetric("pct", r.key.project_irr_post_subsidy, "", locale)}</Td>
                      <Td className="text-right">{fmtMetric("ratio", r.key.dscr_min, "", locale)}</Td>
                      <Td>
                        <Button size="sm" variant="ghost" onClick={() => setSelected(r.id)} disabled={r.id === selected}>
                          {t("results.view")}
                        </Button>
                      </Td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </TableWrap>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
