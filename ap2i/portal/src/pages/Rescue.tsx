import { useEffect, useMemo, useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { fetchJSON, useAsync } from "../lib/data";
import { disbursementRate, elapsedRatio, maxLevel, slippageDays } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtPct } from "../lib/format";
import { downloadCSV } from "../lib/exporters";
import { go, href, type Route } from "../lib/router";
import { Card, Empty, ErrorState, ExternalLink, LevelBadge, Loading, NA, PageHead } from "../components/ui";
import type { AlertItem } from "../lib/types";

/* eslint-disable @typescript-eslint/no-explicit-any */
interface Action { id: string; text: string; owner: string; deadline: string; priority: "high" | "medium" | "low"; status: "todo" | "in_progress" | "done" | "blocked"; rule?: string }
const KEY = (ref: string) => `ap2i.portal.rescueDraft.${ref}`;

function loadDraft(ref: string): Action[] {
  try {
    const v = JSON.parse(localStorage.getItem(KEY(ref)) ?? "[]");
    return Array.isArray(v) ? v.slice(0, 100) : [];
  } catch {
    return [];
  }
}

export function Rescue({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const ref = route.path[1];
  const [onlyAlerts, setOnlyAlerts] = useState(true);
  const [sector, setSector] = useState("");
  const candidates = useMemo(() => s.projects.filter((p) => (!onlyAlerts || maxLevel(p) !== null) && (!sector || p.sector === sector))
    .sort((a, b) => (["critical_attention", "high_attention", "watch", "information"].indexOf(maxLevel(a) ?? "z") - ["critical_attention", "high_attention", "watch", "information"].indexOf(maxLevel(b) ?? "z")) || a.ref.localeCompare(b.ref)), [s, onlyAlerts, sector]);
  const p = s.projects.find((x) => x.ref === ref);
  return (
    <div>
      <PageHead title={t("rescue.title")} subtitle={t("rescue.noAI")}>
        <label className="inline"><input type="checkbox" checked={onlyAlerts} onChange={(e) => setOnlyAlerts(e.target.checked)} /> {t("rescue.onlyAlerts")}</label>
        <select aria-label={t("filters.sector")} value={sector} onChange={(e) => setSector(e.target.value)}>
          <option value="">{t("rescue.allSectors")}</option>
          {s.ref.sectors.filter((x) => s.projects.some((p) => p.sector === x.code)).map((x) => <option key={x.code} value={x.code}>{names.sector(x.code)}</option>)}
        </select>
        <select aria-label={t("rescue.select")} value={ref ?? ""} onChange={(e) => go(`/rescue/${e.target.value}`, {})} data-testid="rescue-select">
          <option value="">{t("rescue.select")}…</option>
          {candidates.map((x) => <option key={x.id} value={x.ref}>{x.ref} — {x.title.slice(0, 70)}</option>)}
        </select>
      </PageHead>
      {!p ? (
        <Card title={t("rescue.topTitle")} note={t("rescue.topHint")}>
          {candidates.length ? (
            <ol className="ranked">
              {candidates.slice(0, 15).map((x) => {
                const l = maxLevel(x);
                return (
                  <li key={x.id}>
                    <a href={`#/rescue/${encodeURIComponent(x.ref)}`} data-testid="rescue-top">
                      {l && <LevelBadge level={l} />} <b>{x.title}</b>
                      <span className="small muted"> — {names.sector(x.sector)} · {x.partners.map((c) => names.partner(c)).join(", ")} · <span className="mono">{x.ref}</span></span>
                    </a>
                  </li>
                );
              })}
            </ol>
          ) : <Empty>{t("rescue.empty")}</Empty>}
        </Card>
      ) : <RescueProject key={p.ref} refId={p.ref} names={names} />}
    </div>
  );
}

function RescueProject({ refId, names }: { refId: string; names: ReturnType<typeof useNames> }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const p = s.projects.find((x) => x.ref === refId)!;
  const { data, error, loading, retry } = useAsync<any>(() => fetchJSON(`p/${encodeURIComponent(refId)}.json`), [refId]);
  const [actions, setActions] = useState<Action[]>(() => loadDraft(refId));
  const [draft, setDraft] = useState<Action>({ id: "", text: "", owner: "", deadline: "", priority: "medium", status: "todo" });
  useEffect(() => {
    try {
      localStorage.setItem(KEY(refId), JSON.stringify(actions));
    } catch { /* private mode: draft kept in memory only */ }
  }, [actions, refId]);
  if (loading) return <Loading />;
  if (error) return <ErrorState error={error} retry={retry} />;
  const agreements = s.agreements.filter((a) => a.project === p.id);
  const alerts: AlertItem[] = data.alerts ?? [];
  const rate = disbursementRate(agreements);
  const elapsed = elapsedRatio(p, new Date(s.meta.generated_at));
  const slip = slippageDays(p);
  const undisb: Record<string, number> = {};
  for (const a of agreements) if (a.undisbursed !== null && a.currency && !a.is_guarantee) undisb[a.currency] = (undisb[a.currency] ?? 0) + Number(a.undisbursed);
  const ratings = (data.implementation_progress ?? []).filter((x: any) => x.rating).slice(0, 6);
  const events = [
    ["approval", p.approval], ["start", p.start], ["planned end", p.planned_end], ["revised end", p.revised_end], ["actual end", p.actual_end],
    ...agreements.flatMap((a) => [[`${a.source_identifier} approval`, a.approval], [`${a.source_identifier} closing`, a.closing_current]]),
    ...ratings.map((x: any) => [`ISR/ICR ${x.rating.split("|")[0]}`, x.report_date]),
  ].filter(([, d]) => d).sort((a, b) => String(a[1]).localeCompare(String(b[1])));
  const done = actions.filter((a) => a.status === "done").length;
  const add = () => {
    if (!draft.text.trim()) return;
    setActions((xs) => [...xs, { ...draft, id: Math.random().toString(36).slice(2), text: draft.text.trim().slice(0, 500), owner: draft.owner.trim().slice(0, 200) }]);
    setDraft({ id: "", text: "", owner: "", deadline: "", priority: "medium", status: "todo" });
  };
  const exportPlan = () => downloadCSV(`ap2i_rescue_draft_${refId}`, ["action", "responsible_institution", "deadline", "priority", "status", "linked_alert_rule"],
    actions.map((a) => [a.text, a.owner, a.deadline, a.priority, a.status, a.rule ?? ""]),
    [`AP²I Project Rescue — LOCAL DRAFT for ${refId} (not official; requires human approval in the AP²I application)`, `exported ${new Date().toISOString()}`]);

  return (
    <>
      <div className="grid-2">
        <Card title={t("rescue.overview")}>
          <p><a href={href(`/project/${p.ref}`, {})}><b>{p.ref}</b></a> — {p.title}</p>
          <p className="small muted">{names.sector(p.sector)} · {t(`status.${p.status}`)} · {p.partners.map((c) => names.partner(c)).join(", ")}</p>
          <dl className="dl">
            <div><dt>{t("col.alerts")}</dt><dd>{alerts.length ? alerts.map((a) => <span key={a.alert_id}><LevelBadge level={a.level} /> </span>) : t("level.none")}</dd></div>
            <div><dt>{t("col.rate")}</dt><dd>{rate.value !== null ? fmtPct(rate.value, locale)
              : rate.partial ? t("fin.partial", { p: fmtPct(rate.partial.value, locale), n: String(rate.partial.published), t: String(rate.partial.total) }) : <NA />}</dd></div>
            <div><dt>{locale === "fr" ? "Temps écoulé" : "Time elapsed"}</dt><dd>{elapsed === null ? <NA /> : fmtPct(elapsed, locale)}</dd></div>
            <div><dt>{locale === "fr" ? "Glissement de la fin" : "End-date slippage"}</dt><dd>{slip === null ? <NA /> : `${slip} j`}</dd></div>
            <div><dt>{t("profile.physical")}</dt><dd>{p.physical_progress === null ? <NA /> : `${p.physical_progress} %`}</dd></div>
          </dl>
        </Card>
        <Card title={t("rescue.gaps")}>
          <dl className="dl">
            {agreements.map((a) => (
              <div key={a.id}><dt>{a.source_identifier} ({names.partner(a.partner)})</dt>
                <dd>{fmtAmount(a.committed === null ? null : Number(a.committed), locale, a.currency ?? "")} → {t("col.disbursed")} {a.is_guarantee ? t("fin.guarantee") : a.disbursed === null ? t("fin.notPublished") : fmtAmount(Number(a.disbursed), locale, a.currency ?? "")}{a.disbursed_as_of ? ` (${fmtDate(a.disbursed_as_of, locale)})` : ""}</dd></div>
            ))}
            <div><dt>{t("col.undisbursed")}</dt><dd>{currencyLines(undisb, locale)}</dd></div>
          </dl>
        </Card>
      </div>
      <div className="grid-2">
        <Card title={t("rescue.timeline")}>
          <ul className="timeline">{events.map(([l, d], i) => <li key={i}><b>{fmtDate(d as string, locale)}</b> — {l as string}</li>)}</ul>
        </Card>
        <Card title={t("rescue.bottlenecks")} note={t("perf.disclaimer")}>
          {alerts.map((a) => (
            <div key={a.alert_id} className="alert-row">
              <LevelBadge level={a.level} /> <b>{t(`rule.${a.rule_code}`)}</b>
              <div className="small">{a.observed_value}</div>
              <div className="small muted">{a.recommended_verification}</div>
              <div className="small"><b>{t("perf.evidence")} :</b> {a.source}</div>
              <button className="btn xs ghost" onClick={() => setDraft((d) => ({ ...d, text: a.recommended_verification.slice(0, 500), rule: a.rule_code }))}>+ {t("rescue.addAction")}</button>
            </div>
          ))}
          {ratings.map((x: any, i: number) => <div key={i} className="small">{fmtDate(x.report_date, locale)} — {x.rating} {x.document && <ExternalLink href={x.document.url}>{x.document.doc_type}</ExternalLink>}</div>)}
          {!alerts.length && !ratings.length && <span className="muted">{t("level.none")}</span>}
        </Card>
      </div>
      <Card title={t("rescue.diagnostic")}>
        <ol className="small">
          <li>{t("rule.LOW_DISBURSEMENT")} : {rate.value === null || elapsed === null ? t("common.na") : `${fmtPct(rate.value, locale)} / ${fmtPct(elapsed, locale)}`}</li>
          <li>{t("rule.SCHEDULE_EXTENSION")} : {slip === null ? t("common.na") : `${slip} j`}</li>
          <li>{t("rule.UNSATISFACTORY_RATING")} : {ratings[0]?.rating ?? t("common.na")}</li>
          <li>{t("rule.COMPLETED_NOT_OPERATIONAL")} : {t(`op.${p.operational_status}`)}</li>
          <li>{t("profile.amendments")} : {t("profile.amendmentsNA")}</li>
        </ol>
      </Card>
      <Card title={t("rescue.plan")} note={t("rescue.planNote")} actions={<button className="btn xs ghost" onClick={exportPlan} disabled={!actions.length}>{t("rescue.export")}</button>}>
        <div className="progress" aria-label={t("rescue.progress")}><div style={{ width: `${actions.length ? (done / actions.length) * 100 : 0}%` }} /><span>{t("rescue.progress")} : {done}/{actions.length}</span></div>
        <div className="table-wrap">
          <table>
            <thead><tr><th>{t("rescue.action")}</th><th>{t("rescue.owner")}</th><th>{t("rescue.deadline")}</th><th>{t("rescue.priority")}</th><th>{t("rescue.statusCol")}</th><th /></tr></thead>
            <tbody>
              {actions.map((a) => (
                <tr key={a.id}>
                  <td>{a.text}{a.rule ? <div className="small muted">{t(`rule.${a.rule}`)}</div> : null}</td>
                  <td>{a.owner || "—"}</td>
                  <td>{a.deadline || "—"}</td>
                  <td>{t(`prio.${a.priority}`)}</td>
                  <td><select value={a.status} onChange={(e) => setActions((xs) => xs.map((x) => (x.id === a.id ? { ...x, status: e.target.value as Action["status"] } : x)))} aria-label={t("rescue.statusCol")}>
                    {(["todo", "in_progress", "done", "blocked"] as const).map((st) => <option key={st} value={st}>{t(`astatus.${st}`)}</option>)}
                  </select></td>
                  <td><button className="btn xs ghost" onClick={() => setActions((xs) => xs.filter((x) => x.id !== a.id))}>{t("rescue.delete")}</button></td>
                </tr>
              ))}
              <tr className="add-row">
                <td><textarea rows={2} maxLength={500} value={draft.text} onChange={(e) => setDraft({ ...draft, text: e.target.value })} aria-label={t("rescue.action")} data-testid="rescue-action" /></td>
                <td><input maxLength={200} value={draft.owner} onChange={(e) => setDraft({ ...draft, owner: e.target.value })} aria-label={t("rescue.owner")} /></td>
                <td><input type="date" value={draft.deadline} onChange={(e) => setDraft({ ...draft, deadline: e.target.value })} aria-label={t("rescue.deadline")} /></td>
                <td><select value={draft.priority} onChange={(e) => setDraft({ ...draft, priority: e.target.value as Action["priority"] })} aria-label={t("rescue.priority")}>
                  {(["high", "medium", "low"] as const).map((x) => <option key={x} value={x}>{t(`prio.${x}`)}</option>)}</select></td>
                <td />
                <td><button className="btn xs" onClick={add} data-testid="rescue-add">{t("rescue.addAction")}</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </>
  );
}
