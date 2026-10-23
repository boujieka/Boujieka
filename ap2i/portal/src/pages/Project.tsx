import { useEffect, useMemo, useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { fetchJSON, useAsync } from "../lib/data";
import { transactionsOf } from "../lib/agg";
import { fmtAmount, fmtDate, fmtNum, fmtPct } from "../lib/format";
import { href, type Route } from "../lib/router";
import { Card, Empty, ErrorState, ExternalLink, Field, LevelBadge, Loading, NA, PageHead, Badge } from "../components/ui";
import { DataTable } from "../components/DataTable";
import { ProjectSummary } from "../components/ProjectSummary";
import { markViewed } from "../lib/follow";
import type { AlertItem } from "../lib/types";

/* eslint-disable @typescript-eslint/no-explicit-any */
type Detail = Record<string, any>;

const safeRef = (r: string) => /^[A-Z0-9][A-Z0-9_\-]{2,60}$/i.test(r);

export function Project({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const ref = route.path[1] ?? "";
  const row = s.projects.find((p) => p.ref === ref);
  const { data, error, loading, retry } = useAsync<Detail>(() => (safeRef(ref) && row ? fetchJSON<Detail>(`p/${encodeURIComponent(ref)}.json`) : Promise.reject(new Error("not found"))), [ref]);
  const [allDocs, setAllDocs] = useState(false);
  const [openAgr, setOpenAgr] = useState<number | null>(null);
  const agreements = useMemo(() => s.agreements.filter((a) => a.project === row?.id), [s, row]);
  const back = href("/projects", route.filters);
  useEffect(() => {
    if (row) markViewed(row.ref);
  }, [row]);

  if (!row) return <div><PageHead title={ref} /><Empty>{t("profile.notFound")}</Empty><a href={back}>{t("profile.back")}</a></div>;
  if (loading) return <Loading />;
  if (error || !data) return <ErrorState error={error ?? ""} retry={retry} />;
  const d = data;
  const ind = (code: string) => (d.financials?.indicators ?? []).filter((x: any) => x.code === code);
  const docs: any[] = d.documents ?? [];
  const alerts: AlertItem[] = d.alerts ?? [];

  return (
    <div className="profile">
      <a href={back} className="small">{t("profile.back")}</a>
      <PageHead title={d.title} subtitle={<><span className="mono">{d.ap2i_id}</span> · {names.country(d.country)} · {names.sector(d.sector?.code ?? null)}</>}>
        <Badge>{t(`status.${d.status}`)}</Badge>
        <Badge tone="gray">{d.verification_status}</Badge>
      </PageHead>
      <ProjectSummary p={row} agreements={agreements} />

      <div className="grid-2">
        <Card title={t("profile.identification")}>
          <dl className="fields">
            <Field label={t("col.ref")}>{d.ap2i_id}</Field>
            <Field label={t("profile.identifiers")}>{(d.identifiers ?? []).map((x: any) => `${x.scheme}: ${x.identifier}`).join(" · ")}</Field>
            <Field label={t("col.status")}>{t(`status.${d.status}`)} {d.status_source ? <span className="muted small">({d.status_source})</span> : null}</Field>
            <Field label={t("profile.agency")}>{d.executing_agency}</Field>
            <Field label={t("profile.ministry")}>{d.supervising_ministry}</Field>
            <Field label={t("col.region")}>{d.region ? (locale === "fr" ? d.region.name_fr : d.region.name_en) : null}</Field>
            <Field label={t("col.approval")}>{d.original_approval_date ? fmtDate(d.original_approval_date, locale) : null}</Field>
            <Field label={t("profile.dates")}>{[["start", d.implementation_start_date], ["end", d.original_completion_date], ["revised", d.revised_completion_date], ["actual", d.actual_completion_date]]
              .filter(([, v]) => v).map(([k, v]) => `${t(`profile.date.${k}`)} : ${fmtDate(v, locale)}`).join(" · ") || null}</Field>
          </dl>
          {d.description && <details><summary>{t("profile.description")}</summary><p className="pre">{d.description}</p></details>}
          {d.objectives && <details open><summary>{t("profile.objectives")}</summary><p className="pre">{d.objectives}</p></details>}
        </Card>

        <Card title={t("profile.financing")} note={t("money.note")}>
          <dl className="fields">
            {Object.entries(d.financials?.totals_by_currency ?? {}).map(([cur, v]: [string, any]) => (
              <Field key={cur} label={cur}>{`${t("chart.commitments")} ${fmtAmount(v.committed === null ? null : Number(v.committed), locale, cur)} · ${t("col.disbursed")} ${fmtAmount(v.disbursed === null ? null : Number(v.disbursed), locale, cur)}`}</Field>
            ))}
            {ind("disbursement_rate").map((x: any) => (
              <Field key={x.label} label={`${t("ind.disbursement_rate")} — ${x.label.split("—")[1]?.trim() ?? ""}`}>{x.value === null ? <><NA /> <span className="muted small">{(x.missing_inputs ?? []).join(", ") || x.formula}</span></> : `${fmtPct(Number(x.value), locale, 1)} (${t("common.calculated")})`}</Field>
            ))}
            {["elapsed_time_ratio", "schedule_slippage_days", "cost_overrun", "financing_gap"].flatMap((c) => ind(c)).map((x: any) => (
              <Field key={x.code} label={t(`ind.${x.code}`)}>{x.value === null ? <><NA /> <span className="muted small" lang="en">{(x.missing_inputs ?? []).join(", ")}</span></> : x.unit === "ratio" ? fmtPct(Number(x.value), locale, 1) : `${fmtNum(Number(x.value), locale)} ${x.unit === "days" ? t("profile.days") : x.unit}`}</Field>
            ))}
            {agreements.some((a) => a.disbursed !== null && a.committed !== null && Number(a.disbursed) > Number(a.committed) && !a.is_guarantee) &&
              <Field label="⚠">{t("profile.overDisbursed")}</Field>}
            <Field label={t("finance.costs")}>{d.original_estimated_cost ? `${fmtAmount(Number(d.original_estimated_cost), locale, d.cost_currency)} → ${d.revised_estimated_cost ? fmtAmount(Number(d.revised_estimated_cost), locale, d.cost_currency) : "—"}` : null}</Field>
          </dl>
        </Card>
      </div>

      <Card title={t("profile.agreements")}>
        <div className="table-wrap">
          <table>
            <thead><tr><th>{t("col.agreement")}</th><th>{t("col.partners")}</th><th>{t("col.instrument")}</th><th>{t("col.approval")}</th>
              <th className="r">{t("chart.commitments")}</th><th className="r">{t("col.usd")}</th><th className="r">{t("col.disbursed")}</th><th className="r">{t("col.undisbursed")}</th><th>{t("common.source")}</th><th /></tr></thead>
            <tbody>
              {agreements.map((a) => {
                const src = (d.agreements ?? []).find((x: any) => x.id === a.id)?.source;
                const tx = transactionsOf(s.flows, a.id);
                return [
                  <tr key={a.id}>
                    <td className="mono">{a.source_identifier}{a.parent ? <div className="small muted">↳ {a.parent}</div> : null}{a.is_guarantee ? <div><Badge tone="gold">guarantee</Badge></div> : null}</td>
                    <td>{names.partner(a.partner)}</td>
                    <td>{a.instrument ? names.instrument(a.instrument) : a.instrument_label ?? "—"}</td>
                    <td>{fmtDate(a.approval, locale)}</td>
                    <td className="r" title={a.committed_basis ?? ""}>{fmtAmount(a.committed === null ? null : Number(a.committed), locale, a.currency ?? "")}</td>
                    <td className="r" title={a.committed_usd_note ?? ""}>{a.committed_usd === null ? <span className="na">{a.committed === null ? (a.committed_basis?.startsWith("not counted") ? t("profile.notCounted") : "—") : t("common.notConverted")}</span> : fmtAmount(Number(a.committed_usd), locale, "USD")}</td>
                    <td className="r" title={`${a.disbursed_basis ?? ""} ${a.disbursed_as_of ?? ""}`}>{a.is_guarantee
                      ? <span className="small">{t("fin.guarantee")}</span>
                      : a.disbursed === null ? <span className="na small">{t("fin.notPublished")}</span>
                      : fmtAmount(Number(a.disbursed), locale, a.currency ?? "")}</td>
                    <td className="r">{fmtAmount(a.undisbursed === null ? null : Number(a.undisbursed), locale, a.currency ?? "")}</td>
                    <td>{src?.url ? <ExternalLink href={src.url}>{src.connector}</ExternalLink> : "—"}</td>
                    <td>{tx.length > 0 && <button className="btn xs ghost" onClick={() => setOpenAgr(openAgr === a.id ? null : a.id)} aria-expanded={openAgr === a.id}>{tx.length} tx</button>}</td>
                  </tr>,
                  openAgr === a.id ? (
                    <tr key={`${a.id}-tx`}><td colSpan={10}>
                      <DataTable rows={tx} rowKey={(r) => r.i} pageSize={15} exportName={`ap2i_${a.source_identifier}_transactions`}
                        provenance={[`${d.ap2i_id} / ${a.source_identifier}`, s.meta.scope]}
                        columns={[
                          { key: "kind", label: t("col.kind"), value: (r) => r.kind },
                          { key: "date", label: t("col.date"), value: (r) => r.date ?? (r.year ? String(r.year) : null) },
                          { key: "amount", label: t("col.amount"), align: "right", value: (r) => Number(r.amount), render: (r) => fmtAmount(Number(r.amount), locale, r.currency) },
                          { key: "usd", label: t("col.usd"), align: "right", value: (r) => (r.usd === null ? null : Number(r.usd)), render: (r) => (r.usd === null ? t("common.notConverted") : fmtAmount(Number(r.usd), locale, "USD")) },
                          { key: "rs", label: t("col.rateSource"), value: (r) => r.rate_source },
                        ]} />
                    </td></tr>
                  ) : null,
                ];
              })}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="grid-2">
        <Card title={t("profile.progress")}>
          {(d.implementation_progress ?? []).length ? (
            <ul className="timeline">
              {(d.implementation_progress as any[]).slice(0, 12).map((x, i) => (
                <li key={i}>
                  <b>{fmtDate(x.report_date, locale)}</b> {x.document ? <ExternalLink href={x.document.url}>{x.document.doc_type ?? x.document.title}</ExternalLink> : null}
                  {x.rating && <div className="small">{t("profile.rating")} : {x.rating}</div>}
                  <div className="small muted">{t("profile.physical")} : {x.physical_progress_pct === null ? t("common.na") : `${x.physical_progress_pct} %`} · {t("profile.financialPct")} : {x.financial_progress_pct === null ? t("common.na") : `${x.financial_progress_pct} %`}</div>
                  {x.narrative && <details><summary className="small">{t("profile.narrative")}</summary><p className="pre small">{x.narrative}</p></details>}
                </li>
              ))}
            </ul>
          ) : <NA />}
        </Card>
        <Card title={`${t("profile.operational")} · ${t("profile.amendments")} · ${t("profile.milestones")}`}>
          <dl className="fields">
            <Field label={t("profile.operational")}>{t(`op.${d.operational_status}`)}{d.commissioning_date ? ` — ${t("op.commissioned", { d: fmtDate(d.commissioning_date, locale) })}` : ""}
              {d.status_source && d.operational_status !== "unknown" ? <div className="small muted">{t("op.source")} : {d.status_source}</div> : null}</Field>
            <Field label={t("profile.amendments")}>{t("profile.amendmentsNA")}</Field>
            <Field label={t("profile.milestones")}>{(d.status_history ?? []).length ? (d.status_history as any[]).map((h) => `${fmtDate(h.effective_date ?? h.recorded_at, locale)} — ${h.status}${h.note ? ` (${h.note})` : ""}`).join(" · ") : null}</Field>
            <Field label={t("profile.expected")}>{d.expected_beneficiaries ?? d.development_results}</Field>
          </dl>
        </Card>
      </div>

      {(d.documented_evidence ?? []).length > 0 && (
        <Card title={t("ev.title")} note={t("ev.note")} id="evidence">
          <ul className="evidence">
            {(d.documented_evidence as any[]).map((e, i) => (
              <li key={i}>
                <b>{t(`ev.field.${e.field}`)}</b> : {e.value}{e.currency ? ` ${e.currency}` : ""}{e.as_of ? ` (${fmtDate(e.as_of, locale)})` : ""}
                {e.agreement ? <span className="mono small muted"> · {e.agreement}</span> : null}{" "}
                <Badge tone={e.data_nature === "officially_reported" ? "green" : "gold"}>{e.data_nature === "officially_reported" ? t("ev.official") : t("ev.secondary")}</Badge>
                <blockquote lang="en">« {e.quote} »</blockquote>
                <span className="small"><ExternalLink href={e.source_url}>{e.publisher}</ExternalLink>{e.published ? ` — ${fmtDate(e.published, locale)}` : ""}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      <Card title={t("profile.observed")}>
        {(d.results ?? []).length ? (
          <DataTable rows={d.results as any[]} rowKey={(r) => r.name + r.unit} pageSize={10} exportName={`ap2i_${d.ap2i_id}_results`} provenance={[d.ap2i_id, s.meta.scope]}
            columns={[
              { key: "name", label: t("col.title"), minWidth: "30ch", value: (r) => r.name },
              { key: "unit", label: t("profile.unit"), value: (r) => r.unit },
              { key: "b", label: t("profile.baseline"), align: "right", value: (r) => (r.baseline_value === null ? null : Number(r.baseline_value)), render: (r) => (r.baseline_value === null ? null : fmtNum(Number(r.baseline_value), locale, 2)) },
              { key: "tg", label: t("profile.target"), align: "right", value: (r) => (r.target_value === null ? null : Number(r.target_value)), render: (r) => (r.target_value === null ? null : fmtNum(Number(r.target_value), locale, 2)) },
              { key: "l", label: t("profile.latest"), align: "right", value: (r) => {
                const obs = (r.observations as any[]).filter((o) => o.period_end).sort((a, b) => (a.period_end < b.period_end ? 1 : -1));
                return obs[0] ? `${obs[0].value !== null ? fmtNum(Number(obs[0].value), locale, 2) : obs[0].value_text} (${fmtDate(obs[0].period_end, locale)})` : null; } },
            ]} />
        ) : <NA />}
      </Card>

      <Card title={t("profile.alerts")} id="alerts" note={t("perf.disclaimer")}>
        {alerts.length ? alerts.map((a) => (
          <div key={a.alert_id} className="alert-row">
            <LevelBadge level={a.level} /> <b>{t(`rule.${a.rule_code}`)}</b>
            <div className="small">{t("col.observed")} : {a.observed_value} · {t("col.threshold")} : {a.threshold} · {t("col.asOf")} {a.as_of}</div>
            <div className="small muted">{a.explanation}</div>
            <div className="small"><b>{t("perf.evidence")} :</b> {a.source} {a.source_record_ids?.length ? `(records ${a.source_record_ids.join(", ")})` : ""}</div>
          </div>
        )) : <span className="muted">{t("level.none")}</span>}
        <p className="small"><a href={href(`/rescue/${d.ap2i_id}`, {})}>{t("profile.rescue")} →</a> <span className="muted">{t("profile.rescueNote")}</span></p>
      </Card>

      <div className="grid-2">
        <Card title={`${t("profile.documents")} (${docs.length})`}>
          <ul className="doclist">
            {(allDocs ? docs : docs.slice(0, 12)).map((x) => (
              <li key={x.id}><ExternalLink href={x.url}>{x.title}</ExternalLink> <span className="small muted">{x.doc_type ?? ""} · {fmtDate(x.published_date, locale)}</span></li>
            ))}
          </ul>
          {docs.length > 12 && !allDocs && <button className="btn xs ghost" onClick={() => setAllDocs(true)}>{t("profile.showAll", { n: docs.length })}</button>}
        </Card>
        <Card title={t("profile.sources")}>
          <ul className="doclist">
            {(d.sources ?? []).map((x: any) => (
              <li key={x.record_id}><ExternalLink href={x.url}>{x.connector_name}</ExternalLink> <span className="small muted">{x.source_identifier} · {x.link_type} · retrieved {fmtDate(x.retrieved_at, locale)} · source updated {fmtDate(x.source_last_updated, locale)}</span></li>
            ))}
          </ul>
          {d.data_quality && <p className="small">{t("profile.dq")} : completeness {fmtPct(d.data_quality.completeness, locale)} · traceability {fmtPct(d.data_quality.traceability, locale)} · missing: {(d.data_quality.missing_fields ?? []).join(", ") || "—"}</p>}
          {(d.validation_issues ?? []).length > 0 && <details><summary className="small">{(d.validation_issues as any[]).length} validation notes</summary>
            <ul className="small">{(d.validation_issues as any[]).slice(0, 30).map((v, i) => <li key={i}>[{v.severity}] {v.message}</li>)}</ul></details>}
          {d.observations_note && <p className="small muted">{t("profile.observationsNote")} <a href="#/plans">{t("nav.plans")} →</a></p>}
        </Card>
      </div>
    </div>
  );
}
