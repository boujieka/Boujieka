import { useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { commitmentsOf, disbursementRate, maxLevel } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtPct } from "../lib/format";
import { useFollowed } from "../lib/follow";
import { href } from "../lib/router";
import type { AgreementRow, AlertItem, ProjectRow } from "../lib/types";
import { ExternalLink, Help } from "./ui";

/* eslint-disable @typescript-eslint/no-explicit-any */
type Detail = Record<string, any>;

/** Project page, top part (redesign phase 1): who / how much / does it work / when / according to whom.
 * Every value comes from the record shown below; nothing is estimated (the summary sentence is a template, not AI). */

const RATING_KEYS: Record<string, [string, string]> = { PDO: ["Objectif", "Objective"], IP: ["Mise en œuvre", "Implementation"],
  Risk: ["Risque", "Risk"], Outcome: ["Résultat", "Outcome"] };
const RATING_WORDS: Record<string, string> = { "Highly Satisfactory": "Très satisfaisant", "Moderately Satisfactory": "Moyennement satisfaisant",
  Satisfactory: "Satisfaisant", "Moderately Unsatisfactory": "Moyennement insatisfaisant", "Highly Unsatisfactory": "Très insatisfaisant",
  Unsatisfactory: "Insatisfaisant", Substantial: "Substantiel", High: "Élevé", Moderate: "Modéré", Low: "Faible" };

/** "PDO=Satisfactory|IP=Moderately Satisfactory|Risk=High" -> [["Objectif", "Satisfaisant"], ...] (published words, translated in FR). */
export function ratingParts(raw: string, fr: boolean): [string, string][] {
  return raw.replace(/^ICR( Review)?: /, "").split("|").slice(0, 3).map((part) => {
    const [k, v = ""] = part.split("=");
    const val = v.replace(/ \(IEG=.*\)/, "").trim();
    return [RATING_KEYS[k.trim()]?.[fr ? 0 : 1] ?? k.trim(), fr ? RATING_WORDS[val] ?? val : val];
  });
}

// categorical colours for lenders (fixed order, so a lender keeps its colour on every page)
const LENDER_COLORS: Record<string, string> = { WB: "#2c5d9e", AFDB: "#087f5b", AFD: "#c9822b", EIB: "#6b4fa0", EU: "#3a8fb7", IFAD: "#8a6d1f" };
const lenderColor = (code: string | null) => (code && LENDER_COLORS[code]) || "#8a96a3";

const LEVEL_TONE: Record<string, string> = { critical_attention: "tag-red", high_attention: "tag-amber", watch: "tag-blue", information: "tag-gray" };

type Pub = "published" | "not_published" | "guarantee";
const pubOf = (a: AgreementRow): Pub => (a.is_guarantee ? "guarantee" : a.disbursed === null ? "not_published" : "published");

export function ProjectHero({ p, d, agreements }: { p: ProjectRow; d: Detail; agreements: AgreementRow[] }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const fr = locale === "fr";
  const L = (f: string, e: string) => (fr ? f : e);
  const { isFollowed, toggle } = useFollowed();
  const [copied, setCopied] = useState(false);

  const money = commitmentsOf(agreements);
  const rate = disbursementRate(agreements);
  const counted = agreements.filter((a) => a.committed !== null && Number(a.committed) > 0);
  const lenders = [...new Set(counted.map((a) => a.partner))];
  const partnerNames = lenders.map((c) => names.partner(c)).join(", ") || t("common.na");
  const alerts: AlertItem[] = d.alerts ?? [];
  const level = maxLevel(p);
  const order = ["critical_attention", "high_attention", "watch", "information"];
  const topAlert = [...alerts].sort((a, b) => order.indexOf(a.level) - order.indexOf(b.level))[0];
  const nonGuar = counted.filter((a) => !a.is_guarantee);
  const nPublished = nonGuar.filter((a) => a.disbursed !== null).length;
  const allGuarantees = counted.length > 0 && nonGuar.length === 0;
  const disbByCur: Record<string, number> = {};
  for (const a of nonGuar) if (a.disbursed !== null && a.currency) disbByCur[a.currency] = (disbByCur[a.currency] ?? 0) + Number(a.disbursed);
  const physical = d.physical_progress_pct !== null && d.physical_progress_pct !== undefined ? Number(d.physical_progress_pct) : null;

  // ---- summary sentence (template) ----
  const disbText = allGuarantees ? t("fin.guarantee")
    : rate.value !== null ? `${fmtPct(rate.value, locale)} ${L("décaissé", "disbursed")}`
    : rate.partial ? t("fin.partial", { p: fmtPct(rate.partial.value, locale), n: String(rate.partial.published), t: String(rate.partial.total) })
    : t("fin.notPublished");
  const sentence = fr
    ? `Projet ${t(`status.${p.status}`).toLowerCase()} du secteur « ${names.sector(p.sector)} », financé par ${partnerNames}` +
      `${money.usd !== null ? ` pour ${fmtAmount(money.usd, locale, "USD")} (éq.)` : ""}.` +
      ` Décaissement : ${disbText.toLowerCase()}.` +
      `${p.operational_status !== "unknown" ? ` Statut opérationnel : ${t(`op.${p.operational_status}`).toLowerCase()}${p.commissioning ? ` depuis le ${fmtDate(p.commissioning, locale)}` : ""}.` : ""}` +
      ` ${alerts.length ? `${alerts.length} alerte(s), la plus grave : ${t(`level.${level}`).toLowerCase()}.` : "Aucune alerte."}`
    : `${t(`status.${p.status}`)} ${names.sector(p.sector)} project financed by ${partnerNames}` +
      `${money.usd !== null ? ` for ${fmtAmount(money.usd, locale, "USD")} (eq.)` : ""}.` +
      ` Disbursement: ${disbText.toLowerCase()}.` +
      `${p.operational_status !== "unknown" ? ` Operational status: ${t(`op.${p.operational_status}`).toLowerCase()}${p.commissioning ? ` since ${fmtDate(p.commissioning, locale)}` : ""}.` : ""}` +
      ` ${alerts.length ? `${alerts.length} alert(s), most severe: ${t(`level.${level}`).toLowerCase()}.` : "No alert."}`;

  const share = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt(t("filters.share"), window.location.href);
    }
  };
  const toAlerts = () => document.getElementById("alerts")?.scrollIntoView({ behavior: "smooth" });

  // ---- commitments share by lender (USD eq.) ----
  const usdBy: { code: string | null; usd: number }[] = [];
  for (const a of counted) {
    if (a.committed_usd === null) continue;
    const x = usdBy.find((y) => y.code === a.partner);
    if (x) x.usd += Number(a.committed_usd); else usdBy.push({ code: a.partner, usd: Number(a.committed_usd) });
  }
  usdBy.sort((a, b) => b.usd - a.usd);
  const usdTotal = usdBy.reduce((x, y) => x + y.usd, 0);
  const rows = [...counted].sort((a, b) => Number(b.committed_usd ?? 0) - Number(a.committed_usd ?? 0));

  // ---- timeline ----
  const asOf = s.meta.generated_at.slice(0, 10);
  const rating = p.latest_rating;
  const events: { date: string; label: string; kind: "done" | "plan" | "now" | "report" }[] = [];
  const add = (date: string | null | undefined, label: string, kind: "done" | "plan" | "now" | "report") => { if (date) events.push({ date: date.slice(0, 10), label, kind }); };
  add(p.approval, L("Approbation", "Approval"), "done");
  add(p.start, L("Démarrage", "Start"), "done");
  add(p.planned_end, L("Fin prévue (initiale)", "Planned end (original)"), p.planned_end && p.planned_end <= asOf ? "done" : "plan");
  if (p.revised_end && p.revised_end !== p.planned_end) add(p.revised_end, L("Fin révisée", "Revised end"), p.revised_end <= asOf ? "done" : "plan");
  if (p.actual_end && (p.status === "completed" || p.status === "closed")) add(p.actual_end, L("Achèvement", "Completion"), "done");
  add(rating?.date, L("Dernier rapport de supervision", "Latest supervision report"), "report");
  if (physical !== null) add(d.physical_progress_date, L(`Avancement physique ${fmtPct(physical / 100, locale, 1)}`, `Physical progress ${fmtPct(physical / 100, locale, 1)}`), "report");
  add(p.commissioning, L("Mise en service", "Commissioning"), "done");
  add(asOf, L("Données au", "Data as of"), "now");
  events.sort((a, b) => a.date.localeCompare(b.date));
  const t0 = Date.parse(events[0]?.date ?? asOf), t1 = Date.parse(events[events.length - 1]?.date ?? asOf);
  const pos = (date: string) => (t1 > t0 ? ((Date.parse(date) - t0) / (t1 - t0)) * 100 : 0);
  // dot positions on the track: proportional to dates, nudged apart so that close events stay readable
  const GAP = 5;
  const dotPos = events.map((e) => pos(e.date));
  for (let i = 1; i < dotPos.length; i++) dotPos[i] = Math.max(dotPos[i], dotPos[i - 1] + GAP);
  const over = (dotPos[dotPos.length - 1] ?? 0) - 100;
  if (over > 0) for (let i = dotPos.length - 1, cap = 100; i >= 0; i--, cap -= GAP) dotPos[i] = Math.min(dotPos[i], cap);
  const planEnd = p.current_end;

  const pubTag = (a: AgreementRow) => {
    const k = pubOf(a);
    return <span className={`tag ${k === "published" ? "tag-green" : k === "guarantee" ? "tag-blue" : "tag-gray"}`}>
      {k === "published" ? L("Publié", "Published") : k === "guarantee" ? L("Garantie", "Guarantee") : L("Non publié", "Not published")}</span>;
  };

  return (
    <>
      <header className="ph">
        <nav className="crumbs small" aria-label={L("Fil d'Ariane", "Breadcrumb")}>
          <a href={href("/projects", {})}>{t("nav.projects")}</a>{p.sector ? <> › <a href={href("/projects", { sector: p.sector })}>{names.sector(p.sector)}</a></> : null}
        </nav>
        <h1>{d.title}</h1>
        <div className="ph-tags">
          <span className="tag tag-navy">{t(`status.${p.status}`)}</span>
          {p.operational_status !== "unknown" && <span className={`tag ${p.operational_status === "operational" ? "tag-green" : "tag-amber"}`}>{t(`op.${p.operational_status}`)}</span>}
          {topAlert && <button type="button" className={`tag tag-btn ${LEVEL_TONE[topAlert.level] ?? "tag-gray"}`} onClick={toAlerts}>
            {t(`level.${topAlert.level}`)} : {t(`rule.${topAlert.rule_code}`)}{alerts.length > 1 ? ` (+${alerts.length - 1})` : ""}</button>}
          <span className="tag tag-outline">{d.verification_status === "verified" ? L("Vérifié", "Verified") : L("Déclaré par les bailleurs", "Reported by lenders")}
            <Help text={L("Les chiffres viennent des publications officielles des bailleurs et des opérateurs. AP²I ne les a pas vérifiés sur le terrain.",
              "Figures come from official lender and operator publications. AP²I has not verified them on site.")} /></span>
        </div>
        <p className="ph-meta">{names.country(d.country)} · {L("Financé par", "Financed by")} {partnerNames}{d.executing_agency ? ` · ${L("Exécution", "Executing agency")} : ${d.executing_agency}` : ""}
          {" · "}<span className="mono small">{d.ap2i_id}</span></p>
        <div className="ph-actions">
          <button className={`btn xs ${isFollowed(p.ref) ? "gold" : "ghost"}`} onClick={() => toggle(p.ref)} aria-pressed={isFollowed(p.ref)} data-testid="follow">
            {isFollowed(p.ref) ? `★ ${t("sum.following")}` : `☆ ${t("sum.follow")}`}
          </button>
          <button className="btn xs ghost" onClick={() => window.print()}>{t("sum.print")}</button>
          <button className="btn xs ghost" onClick={share}>{copied ? t("filters.copied") : t("filters.share")}</button>
        </div>
      </header>

      <section className="card ph-brief summary" aria-label={t("sum.title")}>
        <h2 className="sr-only">{t("sum.title")}</h2>
        <p className="summary-text"><b>{L("En bref", "In brief")} — </b>{sentence} <span className="small muted">({t("sum.generated")})</span></p>
      </section>

      <section className="facts" aria-label={L("Chiffres clés", "Key facts")}>
        <div className="fact">
          <span className="fact-l">{L("Financement engagé", "Committed financing")}<Help text={t("kpi.commitmentsHelp")} /></span>
          <b className="fact-v">{fmtAmount(money.usd, locale, "USD")}</b>
          <span className="fact-s">{L("équivalent", "equivalent")} · {lenders.length} {L(lenders.length > 1 ? "bailleurs" : "bailleur", lenders.length > 1 ? "lenders" : "lender")}</span>
          <span className="fact-s">{currencyLines(money.byCurrency, locale)}</span>
        </div>
        <div className="fact">
          <span className="fact-l">{L("Décaissé", "Disbursed")}{rate.partial ? <Help text={t("fin.partialHelp")} /> : null}</span>
          {allGuarantees ? <b className="fact-v sm">{t("fin.guarantee")}</b>
            : rate.value !== null ? <>
              <b className="fact-v">{fmtPct(rate.value, locale)}</b>
              <span className="bar" aria-hidden><i style={{ width: `${Math.min(rate.value, 1) * 100}%` }} /></span>
              <span className="fact-s">{Object.entries(disbByCur).map(([c, v]) => fmtAmount(v, locale, c)).join(" · ")}</span></>
            : Object.keys(disbByCur).length ? <>
              <b className="fact-v">{Object.entries(disbByCur).map(([c, v]) => fmtAmount(v, locale, c)).join(" · ")}</b>
              <span className="fact-s">{L(`${nPublished} accord(s) sur ${nonGuar.length} publient leurs décaissements`, `${nPublished} of ${nonGuar.length} agreement(s) publish disbursements`)}</span></>
            : <b className="fact-v sm">{t("fin.notPublished")}</b>}
        </div>
        <div className="fact">
          <span className="fact-l">{L("En service ?", "In service?")}</span>
          <b className={`fact-v sm ${p.operational_status === "operational" ? "ok" : ""}`}>{t(`op.${p.operational_status}`)}</b>
          {p.commissioning ? <span className="fact-s">{L("Mise en service le", "Commissioned on")} {fmtDate(p.commissioning, locale)}</span>
            : <span className="fact-s">{L("Aucune source publique trouvée", "No public source found")}</span>}
        </div>
        <div className="fact">
          <span className="fact-l">{L("Avancement physique", "Physical progress")}</span>
          {physical !== null ? <>
            <b className="fact-v">{fmtPct(physical / 100, locale, 1)}</b>
            <span className="bar" aria-hidden><i style={{ width: `${Math.min(physical, 100)}%` }} /></span>
            <span className="fact-s">{L("au", "as of")} {fmtDate(d.physical_progress_date, locale)}</span></>
            : <><b className="fact-v sm">{t("op.unknown")}</b><span className="fact-s">{L("Non publié par les sources", "Not published by the sources")}</span></>}
        </div>
      </section>

      <section className="card" aria-labelledby="who-funds">
        <header className="card-h"><h2 className="card-t" id="who-funds">{L("Qui finance quoi", "Who finances what")}</h2></header>
        <div className="card-b">
          {usdTotal > 0 && <>
            <div className="stack" role="img" aria-label={usdBy.map((x) => `${names.partner(x.code)} ${fmtPct(x.usd / usdTotal, locale)}`).join(", ")}>
              {usdBy.map((x) => <i key={x.code ?? "?"} style={{ width: `${(x.usd / usdTotal) * 100}%`, background: lenderColor(x.code) }} title={`${names.partner(x.code)} ${fmtPct(x.usd / usdTotal, locale)}`} />)}
            </div>
            <ul className="stack-legend small">
              {usdBy.map((x) => <li key={x.code ?? "?"}><i style={{ background: lenderColor(x.code) }} />{names.partner(x.code)} <b>{fmtPct(x.usd / usdTotal, locale)}</b></li>)}
            </ul>
          </>}
          <div className="table-wrap">
            <table className="dt-table lenders">
              <thead><tr><th>{L("Bailleur", "Lender")}</th><th>{t("col.instrument")}</th><th className="r">{L("Engagé", "Committed")}</th>
                <th className="r">{L("Éq. USD", "USD eq.")}</th><th className="r">{L("Décaissé", "Disbursed")}</th><th>{L("Décaissements", "Disbursements")}</th></tr></thead>
              <tbody>
                {rows.map((a) => {
                  const r = !a.is_guarantee && a.disbursed !== null && a.committed !== null && Number(a.committed) > 0 ? Number(a.disbursed) / Number(a.committed) : null;
                  return (
                    <tr key={a.id}>
                      <td data-label={L("Bailleur", "Lender")}><span className="dot" style={{ background: lenderColor(a.partner) }} aria-hidden /><b>{names.partner(a.partner)}</b>
                        <div className="mono small muted">{a.source_identifier}</div></td>
                      <td data-label={t("col.instrument")}>{a.instrument ? names.instrument(a.instrument) : a.instrument_label ?? "—"}</td>
                      <td data-label={L("Engagé", "Committed")} className="r">{fmtAmount(a.committed === null ? null : Number(a.committed), locale, a.currency ?? "")}</td>
                      <td data-label={L("Éq. USD", "USD eq.")} className="r">{a.committed_usd === null ? <span className="na">{t("common.notConverted")}</span> : fmtAmount(Number(a.committed_usd), locale, "USD")}</td>
                      <td data-label={L("Décaissé", "Disbursed")} className="r">{a.is_guarantee ? "—" : a.disbursed === null ? <span className="na">—</span> : <>
                        {fmtAmount(Number(a.disbursed), locale, a.currency ?? "")}{r !== null && <div className="small muted">{fmtPct(r, locale)}</div>}</>}</td>
                      <td data-label={L("Décaissements", "Disbursements")}>{pubTag(a)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {nonGuar.length > nPublished && <p className="small muted note-inline">{L(
            "« Non publié » : le bailleur ne publie pas ses décaissements pour cet accord. Ce n'est pas un zéro, et AP²I ne l'estime pas.",
            "“Not published”: the lender does not publish disbursements for this agreement. This is not a zero, and AP²I does not estimate it.")}</p>}
          {counted.some((a) => a.is_guarantee) && <p className="small muted note-inline">{L(
            "« Garantie » : l'instrument couvre un risque ; il ne donne lieu à décaissement que s'il est appelé.",
            "“Guarantee”: the instrument covers a risk; it is disbursed only if called.")}</p>}
        </div>
      </section>

      <section className="card" aria-labelledby="tl-h">
        <header className="card-h"><h2 className="card-t" id="tl-h">{L("Calendrier", "Timeline")}</h2></header>
        <div className="card-b">
          <div className="tl-track" aria-hidden>
            {planEnd && Date.parse(planEnd) >= t0 && <span className="tl-plan" style={{ left: 0, width: `${Math.min(pos(planEnd.slice(0, 10)), 100)}%` }} />}
            {events.map((e, i) => <span key={i} className={`tl-dot tl-${e.kind}`} style={{ left: `${dotPos[i]}%` }}><b>{i + 1}</b></span>)}
          </div>
          <ol className="tl-list">
            {events.map((e, i) => (
              <li key={i} className={`tl-${e.kind}`}><span className="tl-n" aria-hidden>{i + 1}</span>
                <span className="tl-date">{fmtDate(e.date, locale)}</span> <span>{e.label}</span>
                {e.kind === "report" && rating && e.date === rating.date?.slice(0, 10) && <span className="small muted"> — {ratingParts(rating.rating, fr).map(([k, v]) => `${k} : ${v}`).join(" · ")}</span>}
              </li>
            ))}
          </ol>
        </div>
      </section>
    </>
  );
}

/** Side column: sources and reliability, latest supervision rating, key documents. */
export function ProjectSide({ p, d }: { p: ProjectRow; d: Detail }) {
  const { locale } = useI18n();
  const fr = locale === "fr";
  const L = (f: string, e: string) => (fr ? f : e);
  const sources: any[] = d.sources ?? [];
  const byConnector = new Map<string, { name: string; url: string | null; retrieved: string | null; updated: string | null; n: number }>();
  for (const x of sources) {
    const k = x.connector_name ?? "?";
    const cur = byConnector.get(k);
    if (!cur) byConnector.set(k, { name: k, url: x.url, retrieved: x.retrieved_at, updated: x.source_last_updated, n: 1 });
    else {
      cur.n += 1;
      if ((x.retrieved_at ?? "") > (cur.retrieved ?? "")) cur.retrieved = x.retrieved_at;
      if ((x.source_last_updated ?? "") > (cur.updated ?? "")) cur.updated = x.source_last_updated;
    }
  }
  const docs: any[] = (d.documents ?? []).slice(0, 4);
  const evidenceN = (d.documented_evidence ?? []).length;
  const dq = d.data_quality;
  return (
    <aside className="pside" aria-label={L("Sources et fiabilité", "Sources and reliability")}>
      <section className="card">
        <header className="card-h"><h2 className="card-t">{L("Sources et fiabilité", "Sources and reliability")}</h2></header>
        <div className="card-b">
          <ul className="srcs">
            {[...byConnector.values()].map((x) => (
              <li key={x.name}><ExternalLink href={x.url}>{x.name}</ExternalLink>
                <span className="small muted">{x.n} {L(x.n > 1 ? "enregistrements" : "enregistrement", x.n > 1 ? "records" : "record")}
                  {x.updated ? ` · ${L("mis à jour par la source", "updated by source")} ${fmtDate(x.updated, locale)}` : ""}
                  {x.retrieved ? ` · ${L("collecté", "retrieved")} ${fmtDate(x.retrieved, locale)}` : ""}</span></li>
            ))}
          </ul>
          {evidenceN > 0 && <p className="small"><a href="#evidence" onClick={(e) => { e.preventDefault(); document.getElementById("evidence")?.scrollIntoView({ behavior: "smooth" }); }}>
            {evidenceN} {L("faits documentés avec citation", "documented facts with quotes")} →</a></p>}
          {dq && <dl className="dl small">
            <div><dt>{L("Complétude", "Completeness")}</dt><dd>{fmtPct(dq.completeness, locale)}</dd></div>
            <div><dt>{L("Traçabilité", "Traceability")}</dt><dd>{fmtPct(dq.traceability, locale)}</dd></div>
          </dl>}
        </div>
      </section>
      {p.latest_rating && (
        <section className="card">
          <header className="card-h"><h2 className="card-t">{L("Dernière notation du bailleur", "Latest lender rating")}</h2></header>
          <div className="card-b">
            <dl className="dl small">{ratingParts(p.latest_rating.rating, fr).map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
            <p className="small muted">{fmtDate(p.latest_rating.date, locale)}</p>
          </div>
        </section>
      )}
      {docs.length > 0 && (
        <section className="card">
          <header className="card-h"><h2 className="card-t">{L("Documents clés", "Key documents")}</h2></header>
          <div className="card-b">
            <ul className="doclist">{docs.map((x) => <li key={x.id}><ExternalLink href={x.url}>{x.doc_type ?? x.title}</ExternalLink> <span className="small muted">{fmtDate(x.published_date, locale)}</span></li>)}</ul>
            <p className="small"><a href="#docs" onClick={(e) => { e.preventDefault(); document.getElementById("docs")?.scrollIntoView({ behavior: "smooth" }); }}>
              {L("Tous les documents", "All documents")} ({(d.documents ?? []).length}) →</a></p>
          </div>
        </section>
      )}
    </aside>
  );
}
