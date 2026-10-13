"use client";

import Link from "next/link";
import { Fragment, useCallback, useEffect, useState, type FormEvent } from "react";
import { ChevronDown, ChevronRight, Info, Loader2, Plus, RotateCcw, Trash2, X } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { Field } from "@/components/field";
import { Kpi } from "@/components/kpi";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { DecisionBadge, GateOverrideNote, GatesList, ScoreBar, ScoreBreakdown, SourcesList } from "@/components/score";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, ApiError, orgPath } from "@/lib/api";
import { date, DASH, moneyCompact, num, pct } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import { CRITERIA, DEFAULT_WEIGHTS, type PortfolioAnalysis, type PortfolioSummary, type PortfolioTotals, type Project, type RankingRow, type ScoreWeights } from "@/lib/types";
import { cn } from "@/lib/utils";

function TotalsPanel({ totals, demo }: { totals: PortfolioTotals; demo: boolean }) {
  const { t, locale } = useI18n();
  const id = demo ? "totals-demo" : "totals-real";
  return (
    <section aria-labelledby={`${id}-title`} className="flex flex-col gap-3 rounded-xl border border-border bg-surface-muted/50 p-4" data-testid={id}>
      <div className="flex flex-wrap items-center gap-2">
        <h2 id={`${id}-title`} className="text-base font-semibold text-navy-900">
          {demo ? t("pf.totalsDemo") : t("pf.totalsReal")}
        </h2>
        <DemoBadge show={demo} />
      </div>
      {totals.projects === 0 ? (
        <p className="text-sm text-muted-foreground">{t("dash.noProjects")}</p>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-3 xl:grid-cols-4">
            <Kpi label={t("pf.projects")} value={num(totals.projects, locale)} sub={t("pf.modelled", { n: num(totals.modelled, locale) })} />
            <Kpi label={t("pf.capex")} value={moneyCompact(totals.capex_usd, "USD", locale)} />
            <Kpi label={t("pf.connections")} value={num(totals.connections, locale)} />
            <Kpi label={t("pf.viabilityGap")} value={moneyCompact(totals.viability_gap_usd, "USD", locale)} />
          </div>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="text-xs text-muted-foreground">{t("score.decision")}:</span>
            <DecisionBadge decision="eligible" /> <span className="font-semibold tabular">{num(totals.eligible, locale)}</span>
            <DecisionBadge decision="review_required" /> <span className="font-semibold tabular">{num(totals.review_required, locale)}</span>
            <DecisionBadge decision="excluded" /> <span className="font-semibold tabular">{num(totals.excluded, locale)}</span>
          </div>
        </>
      )}
    </section>
  );
}

function WeightsEditor({ draft, setDraft, onApply, onReset, busy }: { draft: ScoreWeights; setDraft: (w: ScoreWeights) => void; onApply: () => void; onReset: () => void; busy: boolean }) {
  const { t, locale } = useI18n();
  const sum = CRITERIA.reduce((a, c) => a + draft[c], 0);
  return (
    <Card data-testid="weights-editor">
      <CardHeader>
        <CardTitle>{t("pf.weights")}</CardTitle>
        <CardDescription className="flex items-start gap-1.5">
          <Info className="mt-0.5 size-3.5 shrink-0" aria-hidden /> {t("pf.weightsNote")}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="grid gap-x-6 gap-y-4 sm:grid-cols-2 xl:grid-cols-3">
          {CRITERIA.map((c) => {
            const id = `w-${c}`;
            return (
              <div key={c} className="flex flex-col gap-1">
                <div className="flex items-baseline justify-between gap-2">
                  <label htmlFor={id} className="text-xs font-medium text-muted-foreground">
                    {t(`score.crit.${c}` as DictKey)}
                  </label>
                  <span className="text-xs tabular text-navy-900">{num(Math.round(draft[c] * 100), locale, 0)}</span>
                </div>
                <input
                  id={id}
                  type="range"
                  min={0}
                  max={50}
                  step={1}
                  value={Math.round(draft[c] * 100)}
                  onChange={(e) => setDraft({ ...draft, [c]: Number(e.target.value) / 100 })}
                  className="w-full accent-[var(--emerald-600)]"
                  data-testid={`weight-${c}`}
                />
                <span className="text-xs text-subtle-foreground">{t("pf.share", { v: sum > 0 ? pct(draft[c] / sum, locale) : DASH })}</span>
              </div>
            );
          })}
        </div>
        <div className="flex flex-wrap gap-2">
          <Button type="button" onClick={onApply} disabled={busy || sum <= 0} data-testid="apply-weights">
            {busy ? <Loader2 className="animate-spin" aria-hidden /> : null}
            {t("pf.apply")}
          </Button>
          <Button type="button" variant="outline" onClick={onReset} disabled={busy}>
            <RotateCcw aria-hidden /> {t("pf.reset")}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function RankingTable({ rows, onRemove, canEdit }: { rows: RankingRow[]; onRemove: (r: RankingRow) => void; canEdit: boolean }) {
  const { t, locale } = useI18n();
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const COLS = 12;
  return (
    <TableWrap>
      <Table data-testid="ranking-table">
        <thead>
          <tr>
            <Th className="w-8">
              <span className="sr-only">{t("pf.details")}</span>
            </Th>
            <Th>{t("pf.rank")}</Th>
            <Th>{t("common.project")}</Th>
            <Th>{t("pf.score")}</Th>
            <Th>{t("score.decision")}</Th>
            <Th>{t("common.country")}</Th>
            <Th>{t("common.stage")}</Th>
            <Th>{t("pf.modelStatus")}</Th>
            <Th className="text-right">{t("pf.capex")}</Th>
            <Th className="text-right">{t("pf.connections")}</Th>
            <Th className="text-right">{t("pf.viabilityGap")}</Th>
            <Th>
              <span className="sr-only">{t("common.actions")}</span>
            </Th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => {
            const isOpen = !!open[r.project_id];
            const excluded = r.decision === "excluded";
            return (
              <Fragment key={r.project_id}>
                <tr data-testid="ranking-row" data-decision={r.decision} data-project={r.project_name} className={cn(excluded && "bg-danger-100/30")}>
                  <Td>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="size-7"
                      aria-expanded={isOpen}
                      aria-label={t("pf.showDetails", { name: r.project_name })}
                      data-testid="expand-row"
                      onClick={() => setOpen({ ...open, [r.project_id]: !isOpen })}
                    >
                      {isOpen ? <ChevronDown aria-hidden /> : <ChevronRight aria-hidden />}
                    </Button>
                  </Td>
                  <Td className="whitespace-nowrap" data-testid="rank">
                    {r.rank === null ? <span className="text-xs italic text-subtle-foreground">{t("score.noRank")}</span> : <span className="text-base font-semibold tabular text-navy-900">{r.rank}</span>}
                  </Td>
                  <Td className="min-w-48">
                    <Link href={`/app/projects/${r.project_id}?tab=score`} className="font-medium text-navy-800 underline-offset-4 hover:underline">
                      {r.project_name}
                    </Link>
                    {r.is_demo ? (
                      <div className="mt-1">
                        <DemoBadge />
                      </div>
                    ) : null}
                  </Td>
                  <Td>
                    <ScoreBar score={r.score} decision={r.decision} />
                    {r.score_is_partial ? <div className="mt-0.5 text-xs text-subtle-foreground">{t("score.partial", { n: r.missing_criteria.length })}</div> : null}
                  </Td>
                  <Td>
                    <div className="flex flex-col items-start gap-1">
                      <DecisionBadge decision={r.decision} />
                      {excluded ? <GateOverrideNote /> : null}
                    </div>
                  </Td>
                  <Td className="whitespace-nowrap">{r.country}</Td>
                  <Td className="whitespace-nowrap">{t(`stage.${r.stage}` as DictKey)}</Td>
                  <Td>
                    <StatusBadge status={r.run_status} />
                  </Td>
                  <Td className="text-right whitespace-nowrap">{moneyCompact(r.capex_usd, "USD", locale)}</Td>
                  <Td className="text-right whitespace-nowrap">{num(r.connections, locale)}</Td>
                  <Td className="text-right whitespace-nowrap">{moneyCompact(r.viability_gap_usd, "USD", locale)}</Td>
                  <Td>
                    {canEdit ? (
                      <Button type="button" variant="ghost" size="icon" className="size-7 text-muted-foreground" aria-label={`${t("pf.remove")}: ${r.project_name}`} onClick={() => onRemove(r)}>
                        <X aria-hidden />
                      </Button>
                    ) : null}
                  </Td>
                </tr>
                {isOpen ? (
                  <tr data-testid="ranking-detail">
                    <td colSpan={COLS} className="border-b border-border bg-surface-muted/40 px-4 py-4">
                      <p className={cn("mb-4 text-sm", excluded ? "font-medium text-danger-700" : "text-foreground")}>{r.decision_explanation}</p>
                      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)_minmax(0,1fr)]">
                        <div>
                          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("score.breakdown")}</h3>
                          <ScoreBreakdown parts={r.parts} compact />
                        </div>
                        <div>
                          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("score.gatesTitle")}</h3>
                          <GatesList gates={r.gates} />
                        </div>
                        <div>
                          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("score.sources")}</h3>
                          <SourcesList sources={r.sources} />
                          <p className="mt-3 text-xs text-subtle-foreground">{t("score.serverText")}</p>
                        </div>
                      </div>
                    </td>
                  </tr>
                ) : null}
              </Fragment>
            );
          })}
        </tbody>
      </Table>
    </TableWrap>
  );
}

export default function PortfolioPage() {
  const { org, canEdit, isAdmin } = useSession();
  const { t, locale } = useI18n();
  const list = useApi<PortfolioSummary[]>(org ? orgPath(org.id, "/portfolios") : null);
  const projects = useApi<Project[]>(org ? orgPath(org.id, "/projects") : null);
  const [selected, setSelected] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<PortfolioAnalysis | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draft, setDraft] = useState<ScoreWeights>(DEFAULT_WEIGHTS);
  const [applied, setApplied] = useState<ScoreWeights>(DEFAULT_WEIGHTS);
  const [form, setForm] = useState({ name: "", description: "" });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [toAdd, setToAdd] = useState("");
  const [busy, setBusy] = useState(false);

  const current = selected && list.data?.some((p) => p.id === selected) ? selected : (list.data?.[0]?.id ?? null);

  const run = useCallback(
    async (fid: string, w: ScoreWeights) => {
      if (!org) return;
      setRunning(true);
      setError(null);
      try {
        setAnalysis(await api<PortfolioAnalysis>(orgPath(org.id, `/portfolios/${fid}/analysis`), { method: "POST", body: { weights: w } }));
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
      } finally {
        setRunning(false);
      }
    },
    [org],
  );

  useEffect(() => {
    if (!current) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- clear when no portfolio is selected
      setAnalysis(null);
      return;
    }
    run(current, applied);
  }, [current, applied, run]);

  async function create(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    setBusy(true);
    setFormErrors({});
    setError(null);
    try {
      const f = await api<{ id: string }>(orgPath(org.id, "/portfolios"), { method: "POST", body: form });
      setForm({ name: "", description: "" });
      setSelected(f.id);
      list.reload();
    } catch (err) {
      if (err instanceof ApiError) setFormErrors(err.fieldErrors());
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  async function remove(p: PortfolioSummary) {
    if (!org || !window.confirm(t("pf.confirmDelete", { name: p.name }))) return;
    setError(null);
    try {
      await api(orgPath(org.id, `/portfolios/${p.id}`), { method: "DELETE" });
      if (selected === p.id) setSelected(null);
      list.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  async function addProject(e: FormEvent) {
    e.preventDefault();
    if (!org || !current || !toAdd) return;
    setBusy(true);
    setError(null);
    try {
      await api(orgPath(org.id, `/portfolios/${current}/projects`), { method: "POST", body: { project_id: toAdd } });
      setToAdd("");
      await run(current, applied);
      list.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  async function removeProject(r: RankingRow) {
    if (!org || !current) return;
    setError(null);
    try {
      await api(orgPath(org.id, `/portfolios/${current}/projects/${r.project_id}`), { method: "DELETE" });
      await run(current, applied);
      list.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  const members = new Set((analysis?.portfolio.id === current ? analysis?.ranking : [])?.map((r) => r.project_id));
  const candidates = (projects.data ?? []).filter((p) => !members.has(p.id));
  const shown = analysis && analysis.portfolio.id === current ? analysis : null;

  return (
    <>
      <PageHeader title={t("pf.title")} lead={t("pf.lead")} />
      {error ? (
        <Alert variant="danger" className="mb-4" data-testid="portfolio-error">
          {error}
        </Alert>
      ) : null}
      <div className="grid items-start gap-6 xl:grid-cols-[300px_minmax(0,1fr)]">
        <Card>
          <CardHeader>
            <CardTitle>{t("pf.list")}</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {list.loading && !list.data ? <Loading /> : null}
            {list.error ? <ErrorBox error={list.error} onRetry={list.reload} /> : null}
            {list.data && list.data.length === 0 ? <p className="text-sm text-muted-foreground">{t("pf.none")}</p> : null}
            {list.data && list.data.length > 0 ? (
              <ul className="flex flex-col gap-1" data-testid="portfolio-list">
                {list.data.map((p) => (
                  <li key={p.id} className={cn("flex items-start gap-1 rounded-md border px-2 py-1.5", p.id === current ? "border-emerald-600 bg-emerald-50" : "border-transparent hover:bg-surface-muted")}>
                    <button type="button" className="min-w-0 flex-1 text-left" onClick={() => setSelected(p.id)} aria-current={p.id === current ? "true" : undefined}>
                      <span className="block truncate text-sm font-medium text-navy-900">{p.name}</span>
                      <span className="block text-xs text-muted-foreground">
                        {t("pf.count", { n: num(p.projects, locale) })} · {date(p.created_at, locale)}
                      </span>
                    </button>
                    {isAdmin ? (
                      <Button type="button" variant="ghost" size="icon" className="size-7 shrink-0 text-muted-foreground hover:text-danger-700" aria-label={`${t("pf.delete")}: ${p.name}`} onClick={() => remove(p)}>
                        <Trash2 aria-hidden />
                      </Button>
                    ) : null}
                  </li>
                ))}
              </ul>
            ) : null}
            {canEdit ? (
              <form onSubmit={create} className="flex flex-col gap-3 border-t border-border pt-4" data-testid="create-portfolio">
                <Field label={t("pf.name")} error={formErrors.name}>
                  {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} required maxLength={200} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />}
                </Field>
                <Field label={`${t("pf.description")} (${t("common.optional")})`} error={formErrors.description}>
                  {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} maxLength={2000} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />}
                </Field>
                <Button type="submit" disabled={busy || !form.name.trim()}>
                  <Plus aria-hidden /> {t("pf.create")}
                </Button>
              </form>
            ) : null}
          </CardContent>
        </Card>

        <div className="flex min-w-0 flex-col gap-6">
          {!current ? null : (
            <>
              <Card>
                <CardHeader>
                  <div className="flex flex-wrap items-center gap-2">
                    <CardTitle className="text-base text-navy-900" data-testid="portfolio-name">
                      {shown?.portfolio.name ?? list.data?.find((p) => p.id === current)?.name}
                    </CardTitle>
                    {running ? (
                      <Badge variant="neutral">
                        <Loader2 className="animate-spin" aria-hidden /> {t("pf.running")}
                      </Badge>
                    ) : null}
                  </div>
                  {shown?.portfolio.description ? <CardDescription>{shown.portfolio.description}</CardDescription> : null}
                </CardHeader>
                <CardContent>
                  {canEdit ? (
                    <form onSubmit={addProject} className="flex flex-col gap-2 sm:flex-row sm:items-end">
                      <Field label={t("pf.addProject")} className="flex-1">
                        {(id, d) => (
                          <Select id={id} aria-describedby={d} value={toAdd} onChange={(e) => setToAdd(e.target.value)} data-testid="add-project-select" disabled={candidates.length === 0}>
                            <option value="">{candidates.length === 0 ? t("pf.noMore") : t("pf.chooseProject")}</option>
                            {candidates.map((p) => (
                              <option key={p.id} value={p.id}>
                                {p.name} ({p.country})
                              </option>
                            ))}
                          </Select>
                        )}
                      </Field>
                      <Button type="submit" variant="accent" disabled={busy || !toAdd} data-testid="add-project">
                        <Plus aria-hidden /> {t("pf.add")}
                      </Button>
                    </form>
                  ) : (
                    <p className="text-xs text-muted-foreground">{t("common.notAllowed")}</p>
                  )}
                </CardContent>
              </Card>

              {shown ? (
                <>
                  <div className="grid items-start gap-4 2xl:grid-cols-2">
                    <TotalsPanel totals={shown.totals_real} demo={false} />
                    <TotalsPanel totals={shown.totals_demo} demo />
                  </div>
                  <p className="-mt-3 text-xs text-subtle-foreground">{t("pf.totalsNote")}</p>
                  <WeightsEditor
                    draft={draft}
                    setDraft={setDraft}
                    busy={running}
                    onApply={() => setApplied({ ...draft })}
                    onReset={() => {
                      setDraft(DEFAULT_WEIGHTS);
                      setApplied({ ...DEFAULT_WEIGHTS });
                    }}
                  />
                  <Card>
                    <CardHeader>
                      <CardTitle>{t("pf.ranking")}</CardTitle>
                      <CardDescription>{t("pf.rankingLead")}</CardDescription>
                    </CardHeader>
                    <CardContent className="px-0 pb-2">
                      {shown.ranking.length === 0 ? (
                        <p className="px-5 pb-3 text-sm text-muted-foreground">{t("pf.empty")}</p>
                      ) : (
                        <RankingTable rows={shown.ranking} onRemove={removeProject} canEdit={canEdit} />
                      )}
                      <p className="px-5 pt-3 text-xs text-subtle-foreground">
                        {t("score.gateRule")} {t("score.assumptionsNote")}
                      </p>
                    </CardContent>
                  </Card>
                </>
              ) : running ? (
                <Loading />
              ) : null}
            </>
          )}
        </div>
      </div>
    </>
  );
}
