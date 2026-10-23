import { useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { commitmentsOf, disbursementRate, elapsedRatio, maxLevel } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtPct } from "../lib/format";
import { useFollowed } from "../lib/follow";
import type { AgreementRow, ProjectRow } from "../lib/types";
import { Help, LevelBadge } from "./ui";

/** "At a glance" block of a project: key facts and one plain-language sentence built only from the data shown below
 * (template, no AI): nothing is stated that is not in the record. */
const RATING_KEYS: Record<string, [string, string]> = { PDO: ["Objectif", "Objective"], IP: ["Mise en œuvre", "Implementation"],
  Risk: ["Risque", "Risk"], Outcome: ["Résultat", "Outcome"] };
const RATING_WORDS: Record<string, string> = { "Highly Satisfactory": "Très satisfaisant", "Moderately Satisfactory": "Moyennement satisfaisant",
  Satisfactory: "Satisfaisant", "Moderately Unsatisfactory": "Moyennement insatisfaisant", "Highly Unsatisfactory": "Très insatisfaisant",
  Unsatisfactory: "Insatisfaisant", Substantial: "Substantiel", High: "Élevé", Moderate: "Modéré", Low: "Faible" };

/** "PDO=Satisfactory|IP=Moderately Satisfactory|Risk=High" -> readable labels (words kept as published, translated in FR). */
function ratingLabel(raw: string, fr: boolean): string {
  return raw.replace(/^ICR( Review)?: /, "").split("|").slice(0, 2).map((part) => {
    const [k, v = ""] = part.split("=");
    const key = RATING_KEYS[k.trim()]?.[fr ? 0 : 1] ?? k.trim();
    const val = v.replace(/ \(IEG=.*\)/, "").trim();
    return `${key} : ${fr ? RATING_WORDS[val] ?? val : val}`;
  }).join(" · ");
}

export function ProjectSummary({ p, agreements }: { p: ProjectRow; agreements: AgreementRow[] }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const { isFollowed, toggle } = useFollowed();
  const [copied, setCopied] = useState(false);
  const money = commitmentsOf(agreements);
  const rate = disbursementRate(agreements);
  const allGuarantees = agreements.length > 0 && agreements.every((a) => a.is_guarantee);
  const elapsed = elapsedRatio(p, new Date(s.meta.generated_at));
  const level = maxLevel(p);
  const nAlerts = Object.values(p.alerts).reduce((a, b) => a + (b ?? 0), 0);
  const partners = [...new Set(agreements.map((a) => names.partner(a.partner)))].join(", ") || t("common.na");
  const fr = locale === "fr";

  const disbText = allGuarantees ? t("fin.guarantee")
    : rate.value !== null ? `${fmtPct(rate.value, locale)} ${fr ? "décaissé" : "disbursed"}`
    : t("fin.notPublished");
  const sentence = fr
    ? `Projet ${t(`status.${p.status}`).toLowerCase()} du secteur « ${names.sector(p.sector)} », financé par ${partners}` +
      `${money.usd !== null ? ` pour ${fmtAmount(money.usd, locale, "USD")} (éq.)` : ""}.` +
      `${p.approval ? ` Approuvé le ${fmtDate(p.approval, locale)}` : ""}${p.current_end ? `${p.approval ? "," : ""} fin prévue le ${fmtDate(p.current_end, locale)}` : ""}${p.approval || p.current_end ? "." : ""}` +
      ` Décaissement : ${disbText.toLowerCase()}.` +
      ` ${nAlerts ? `${nAlerts} alerte(s), la plus grave : ${t(`level.${level}`).toLowerCase()}.` : "Aucune alerte."}` +
      `${p.operational_status !== "unknown" ? ` Statut opérationnel : ${t(`op.${p.operational_status}`).toLowerCase()}.` : ""}`
    : `${t(`status.${p.status}`)} ${names.sector(p.sector)} project financed by ${partners}` +
      `${money.usd !== null ? ` for ${fmtAmount(money.usd, locale, "USD")} (eq.)` : ""}.` +
      `${p.approval ? ` Approved on ${fmtDate(p.approval, locale)}` : ""}${p.current_end ? `${p.approval ? "," : ""} planned end ${fmtDate(p.current_end, locale)}` : ""}${p.approval || p.current_end ? "." : ""}` +
      ` Disbursement: ${disbText.toLowerCase()}.` +
      ` ${nAlerts ? `${nAlerts} alert(s), most severe: ${t(`level.${level}`).toLowerCase()}.` : "No alert."}` +
      `${p.operational_status !== "unknown" ? ` Operational status: ${t(`op.${p.operational_status}`).toLowerCase()}.` : ""}`;

  const share = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt(t("filters.share"), window.location.href);
    }
  };

  return (
    <section className="summary card" aria-label={t("sum.title")}>
      <div className="summary-top">
        <p className="summary-text">{sentence} <span className="small muted">({t("sum.generated")})</span></p>
        <div className="summary-actions">
          <button className={`btn xs ${isFollowed(p.ref) ? "gold" : "ghost"}`} onClick={() => toggle(p.ref)} aria-pressed={isFollowed(p.ref)} data-testid="follow">
            {isFollowed(p.ref) ? `★ ${t("sum.following")}` : `☆ ${t("sum.follow")}`}
          </button>
          <button className="btn xs ghost" onClick={() => window.print()}>{t("sum.print")}</button>
          <button className="btn xs ghost" onClick={share}>{copied ? t("filters.copied") : t("filters.share")}</button>
        </div>
      </div>
      <div className="kpis summary-kpis">
        <div className="kpi"><span className="kpi-l">{t("sum.committed")}<Help text={t("kpi.commitmentsHelp")} /></span>
          <b className="kpi-v">{fmtAmount(money.usd, locale, "USD")}</b><span className="kpi-s">{currencyLines(money.byCurrency, locale)}</span></div>
        <div className="kpi"><span className="kpi-l">{t("sum.disbursed")}</span>
          <b className="kpi-v small-v">{disbText}</b>
          {rate.value === null && !allGuarantees && rate.reason === "multiple_currencies" ? <span className="kpi-s">{fr ? "plusieurs devises : voir les accords" : "several currencies: see agreements"}</span> : null}</div>
        <div className="kpi"><span className="kpi-l">{t("sum.schedule")}</span>
          <b className="kpi-v small-v">{fmtDate(p.approval, locale)} → {fmtDate(p.current_end, locale)}</b>
          <span className="kpi-s">{elapsed !== null ? `${fmtPct(Math.min(elapsed, 1), locale)} ${fr ? "du calendrier écoulé" : "of schedule elapsed"}` : t("common.na")}</span></div>
        <div className="kpi"><span className="kpi-l">{t("profile.operational")}</span>
          <b className="kpi-v small-v">{t(`op.${p.operational_status}`)}</b>
          {p.commissioning ? <span className="kpi-s">{t("op.commissioned", { d: fmtDate(p.commissioning, locale) })}</span> : null}</div>
        <div className="kpi"><span className="kpi-l">{t("profile.rating")}</span>
          <b className="kpi-v small-v">{p.latest_rating ? ratingLabel(p.latest_rating.rating, fr) : t("common.na")}</b>
          {p.latest_rating?.date ? <span className="kpi-s">{fmtDate(p.latest_rating.date, locale)}</span> : null}</div>
        <div className="kpi"><span className="kpi-l">{t("col.alerts")}</span>
          <b className="kpi-v small-v">{level ? <LevelBadge level={level} /> : t("level.none")}</b>
          {nAlerts ? <button className="linklike kpi-s" onClick={() => document.getElementById("alerts")?.scrollIntoView({ behavior: "smooth" })}>{nAlerts} → {t("sum.seeAlerts")}</button> : null}</div>
      </div>
    </section>
  );
}
