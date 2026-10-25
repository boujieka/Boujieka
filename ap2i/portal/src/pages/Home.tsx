import { useI18n } from "../lib/i18n";
import { useNames, useSnap, useSelection } from "../lib/context";
import { commitmentsOf, maxLevel } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtNum, fmtPct } from "../lib/format";
import { href } from "../lib/router";
import { Help, LevelBadge } from "../components/ui";
import { GlobalSearch } from "../components/GlobalSearch";
import { useFollowed } from "../lib/follow";
import type { AlertItem, ProjectRow } from "../lib/types";

/** Home (redesign phase 2): search first, the state of the portfolio at a glance, then what needs attention and why.
 * Every figure is computed from the public snapshot; the alert reasons are the alert rules that fired. */

const ORDER = ["critical_attention", "high_attention", "watch", "information"];

export function Home() {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const fr = locale === "fr";
  const L = (f: string, e: string) => (fr ? f : e);
  const sel = useSelection({});
  const c = commitmentsOf(sel.agreements);
  const { followed, recent } = useFollowed();
  const byRef = new Map(s.projects.map((p) => [p.ref, p]));
  const byId = new Map(s.projects.map((p) => [p.id, p]));
  const mine = (refs: string[]) => refs.map((r) => byRef.get(r)).filter((p): p is ProjectRow => !!p);

  const active = s.projects.filter((p) => p.status === "active").length;
  const attention = s.projects.filter((p) => { const l = maxLevel(p); return l === "critical_attention" || l === "high_attention"; }).length;
  const operational = s.projects.filter((p) => p.operational_status === "operational").length;
  const notConv = s.agreements.filter((a) => a.committed !== null && a.committed_usd === null).length;
  const toWatch = href("/projects", { alert: "attention" }, { sort: "alerts" });

  // projects to watch: most severe alert first, then the number of alerts; the reason is the rule of the most severe alert
  const alertsByProject = new Map<number, AlertItem[]>();
  for (const a of s.alerts.items) {
    const pid = (a as unknown as { project?: { id: number } }).project?.id;
    if (pid !== undefined) alertsByProject.set(pid, [...(alertsByProject.get(pid) ?? []), a]);
  }
  const watch = [...alertsByProject.entries()]
    .map(([pid, list]) => ({ p: byId.get(pid), list: [...list].sort((a, b) => ORDER.indexOf(a.level) - ORDER.indexOf(b.level)) }))
    .filter((x): x is { p: ProjectRow; list: AlertItem[] } => !!x.p && (x.list[0].level === "critical_attention" || x.list[0].level === "high_attention"))
    .sort((a, b) => ORDER.indexOf(a.list[0].level) - ORDER.indexOf(b.list[0].level) || b.list.length - a.list.length)
    .slice(0, 6);

  // where the money goes: commitments (USD eq.) by sector, all years
  const bySector = new Map<string | null, number>();
  for (const a of sel.agreements) {
    if (a.committed_usd === null) continue;
    const p = byId.get(a.project);
    bySector.set(p?.sector ?? null, (bySector.get(p?.sector ?? null) ?? 0) + Number(a.committed_usd));
  }
  const sectors = [...bySector.entries()].sort((a, b) => b[1] - a[1]);
  const top = sectors.slice(0, 6);
  const sectTotal = sectors.reduce((x, y) => x + y[1], 0);
  const max = top[0]?.[1] ?? 1;

  const chips = [
    { label: L("Projets à surveiller", "Projects to watch"), to: toWatch },
    { label: L("En cours", "Active"), to: href("/projects", { status: ["active"] }) },
    { label: names.sector("ENERGY"), to: href("/projects", { sector: "ENERGY" }) },
    { label: names.sector("TRANSPORT"), to: href("/projects", { sector: "TRANSPORT" }) },
    { label: L("Carte des projets", "Project map"), to: "#/projects?view=map" },
  ];

  return (
    <div className="home home2">
      <section className="h2-hero">
        <p className="kicker">AP²I — {t("app.name")}</p>
        <h1>{L("Suivre l'investissement public financé par les bailleurs, source à l'appui", "Track donor-financed public investment, with every source")}</h1>
        <p className="h2-lead">{L(`Cameroun : ${fmtNum(s.meta.counts.projects, locale)} projets de 6 bailleurs, chaque chiffre relié à sa source officielle.`,
          `Cameroon: ${fmtNum(s.meta.counts.projects, locale)} projects from 6 lenders, every figure linked to its official source.`)}</p>
        <GlobalSearch variant="hero" />
        <nav className="h2-chips" aria-label={L("Accès rapides", "Quick links")}>
          {chips.map((x) => <a key={x.label} className="chip" href={x.to}>{x.label}</a>)}
        </nav>
      </section>

      <section className="h2-kpis" aria-label={L("Le portefeuille en chiffres", "The portfolio in figures")}>
        <a className="h2-kpi" href="#/projects"><span>{L("Projets documentés", "Documented projects")}</span><b>{fmtNum(s.meta.counts.projects, locale)}</b>
          <small>{fmtNum(active, locale)} {L("en cours", "active")}</small></a>
        <a className="h2-kpi" href="#/finance"><span>{L("Engagements, toutes années", "Commitments, all years")}<Help text={t("kpi.commitmentsHelp")} /></span><b>{fmtAmount(c.usd, locale, "USD")}</b>
          <small>{notConv ? t("kpi.notConvertedAmounts", { amounts: currencyLines(c.unconverted, locale) }) : L("équivalent USD", "USD equivalent")}</small></a>
        <a className="h2-kpi warn" href={toWatch} data-testid="home-task1"><span>{L("À surveiller", "To watch")}<Help text={t("kpi.attentionHelp")} /></span><b>{fmtNum(attention, locale)}</b>
          <small>{L("alerte critique ou élevée", "critical or high alert")}</small></a>
        <div className="h2-kpi"><span>{L("En service, documentés", "In service, documented")}<Help text={L("Projets dont le statut opérationnel est établi par une source officielle citée (opérateur, bailleur, État). Les autres restent « non documentés », pas « hors service ».", "Projects whose operational status is established by a cited official source (operator, lender, government). Others remain “not documented”, not “out of service”.")} /></span><b>{fmtNum(operational, locale)}</b>
          <small>{L("source officielle citée", "official source cited")}</small></div>
      </section>
      <p className="muted small h2-asof">{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)} · {t("snapshot.latestSource")} {fmtDate(s.meta.latest_source_update, locale)} ·{" "}
        <a href="#/about">{L("Méthode et sources", "Method and sources")}</a></p>

      <div className="h2-grid">
        <section className="card" aria-labelledby="watch-h">
          <header className="card-h"><h2 className="card-t" id="watch-h">{L("Projets à surveiller", "Projects to watch")}</h2>
            <a className="small" href={toWatch}>{L(`Voir les ${fmtNum(attention, locale)}`, `See all ${fmtNum(attention, locale)}`)} →</a></header>
          <ul className="watch">
            {watch.map(({ p, list }) => (
              <li key={p.id}>
                <a href={`#/project/${encodeURIComponent(p.ref)}`}>
                  <span className="watch-top"><LevelBadge level={list[0].level} /> <span className="small muted">{names.sector(p.sector)} · {p.partners.map((x) => names.partner(x)).join(", ")}</span></span>
                  <b>{p.title}</b>
                  <span className="small">{L("Pourquoi", "Why")} : {t(`rule.${list[0].rule_code}`)}{list.length > 1 ? L(` (+${list.length - 1} autre${list.length > 2 ? "s" : ""})`, ` (+${list.length - 1} more)`) : ""}</span>
                </a>
              </li>
            ))}
          </ul>
          <p className="note">{t("perf.disclaimer")}</p>
        </section>

        <div className="h2-side">
          {(followed.length > 0 || recent.length > 0) && (
            <section className="card">
              <header className="card-h"><h2 className="card-t">{t("home.followTitle")}</h2></header>
              <div className="card-b mine">
                {[["home.followed", mine(followed)], ["home.recent", mine(recent)]].map(([k, list]) => (list as ProjectRow[]).length ? (
                  <div key={k as string}>
                    <h3 className="small muted">{t(k as string)}</h3>
                    <ul className="ranked">
                      {(list as ProjectRow[]).slice(0, 4).map((p) => {
                        const l = maxLevel(p);
                        return <li key={p.id}><a href={`#/project/${encodeURIComponent(p.ref)}`}>{l && <LevelBadge level={l} />} <b>{p.title}</b></a></li>;
                      })}
                    </ul>
                  </div>) : null)}
              </div>
            </section>
          )}
          <section className="card" aria-labelledby="money-h">
            <header className="card-h"><h2 className="card-t" id="money-h">{L("Où va l'argent", "Where the money goes")}</h2>
              <a className="small" href="#/finance">{t("nav.finance")} →</a></header>
            <div className="card-b">
              <ul className="hbars">
                {top.map(([code, v]) => (
                  <li key={code ?? "none"}><a href={href("/projects", { sector: code ?? "UNCLASSIFIED" })}>
                    <span className="hb-l">{names.sector(code)}</span>
                    <span className="hb-b" aria-hidden><i style={{ width: `${(v / max) * 100}%` }} /></span>
                    <span className="hb-v">{fmtAmount(v, locale, "USD")} <small className="muted">{fmtPct(v / sectTotal, locale)}</small></span></a></li>
                ))}
              </ul>
              <p className="small muted">{L("Engagements en équivalent USD, toutes années, par secteur.", "Commitments in USD equivalent, all years, by sector.")}</p>
            </div>
          </section>
        </div>
      </div>

      <section className="h2-trust" aria-labelledby="trust-h">
        <div>
          <h2 id="trust-h">{L("Pourquoi faire confiance à ces chiffres ?", "Why trust these figures?")}</h2>
          <ul className="why">
            <li>{L("Chaque montant vient d'une publication officielle d'un bailleur, avec le lien vers la source.", "Every amount comes from an official lender publication, with a link to the source.")}</li>
            <li>{L("Ce qui n'est pas publié est marqué « non publié », jamais estimé ni remplacé par zéro.", "What is not published is marked “not published”, never estimated or replaced by zero.")}</li>
            <li>{L("Les alertes sont des signaux à vérifier, avec leur règle et leur seuil, pas des jugements.", "Alerts are signals to check, with their rule and threshold, not judgements.")}</li>
          </ul>
        </div>
        <div className="h2-cta">
          <p className="small">{t("home.audience")}</p>
          <a className="btn gold" href="#/contact" data-testid="hero-demo">{t("home.demo")}</a>
          <a className="btn ghost" href="#/plans">{t("nav.plans")}</a>
        </div>
      </section>
    </div>
  );
}
