import { useI18n } from "../lib/i18n";
import { useSnap, useSelection } from "../lib/context";
import { commitmentsOf, maxLevel } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtNum } from "../lib/format";
import { href } from "../lib/router";
import { Kpi, LevelBadge } from "../components/ui";
import { useFollowed } from "../lib/follow";

const MODULES = ["africa", "country", "projects", "finance", "performance", "rescue", "data"] as const;
const PATHS: Record<string, string> = { africa: "/africa", country: "/country/CMR", projects: "/projects", finance: "/finance",
  performance: "/performance", rescue: "/rescue", data: "/data" };

export function Home() {
  const { t, locale } = useI18n();
  const s = useSnap();
  const sel = useSelection({});
  const c = commitmentsOf(sel.agreements);
  const withData = s.ref.countries.filter((x) => x.documented_projects > 0).length;
  const attention = s.projects.filter((p) => { const l = maxLevel(p); return l === "critical_attention" || l === "high_attention"; }).length;
  const { followed, recent } = useFollowed();
  const byRef = new Map(s.projects.map((p) => [p.ref, p]));
  const mine = (refs: string[]) => refs.map((r) => byRef.get(r)).filter((p): p is NonNullable<typeof p> => !!p);
  const notConv = s.agreements.filter((a) => a.committed !== null && a.committed_usd === null).length;
  const tasks = [
    { k: "task1", to: href("/projects", { alert: "attention" }, { sort: "alerts" }) },
    { k: "task2", to: "#/finance" },
    { k: "task3", to: "#/projects" },
    { k: "task4", to: "#/about" },
  ];
  const audiences = [
    { k: "for1", to: href("/performance", { country: "CMR" }) },
    { k: "for2", to: "#/finance" },
    { k: "for3", to: href("/projects", { status: ["active", "pipeline"] }) },
    { k: "for4", to: "#/projects?view=cards" },
  ];
  return (
    <div className="home">
      <section className="hero">
        <img src={`${import.meta.env.BASE_URL}ap2i-logo.png`} alt="AP²I" width={132} height={132} />
        <div>
          <p className="kicker">AP²I — {t("app.name")}</p>
          <h1>{t("app.tagline")}</h1>
          <p className="lead">{t("home.lead")}</p>
          <p className="lead small">{t("home.audience")}</p>
          <a className="btn gold" href="#/contact" data-testid="hero-demo">{t("home.demo")}</a>
          <a className="btn outline-w" href="#/country/CMR">{t("home.explore")}</a>
        </div>
      </section>

      <h2>{t("home.tasksTitle")}</h2>
      <div className="modules tasks">
        {tasks.map((x) => (
          <a key={x.k} className="module" href={x.to} data-testid={`home-${x.k}`}>
            <b>{t(`home.${x.k}`)}</b><span>{t(`home.${x.k}d`)}</span>
          </a>
        ))}
      </div>

      {(followed.length > 0 || recent.length > 0) && (
        <section className="card">
          <header className="card-h"><h2 className="card-t">{t("home.followTitle")}</h2></header>
          <div className="card-b grid-2 mine">
            {[["home.followed", mine(followed)], ["home.recent", mine(recent)]].map(([k, list]) => (
              <div key={k as string}>
                <h3 className="small muted">{t(k as string)}</h3>
                {(list as typeof s.projects).length ? (
                  <ul className="ranked">
                    {(list as typeof s.projects).slice(0, 6).map((p) => {
                      const l = maxLevel(p);
                      return <li key={p.id}><a href={`#/project/${encodeURIComponent(p.ref)}`}>{l && <LevelBadge level={l} />} <b>{p.title}</b></a></li>;
                    })}
                  </ul>
                ) : <p className="small muted">{t("home.followHint")}</p>}
              </div>
            ))}
          </div>
        </section>
      )}

      <div className="kpis">
        <Kpi label={t("kpi.projects")} value={fmtNum(s.meta.counts.projects, locale)} href="#/projects" />
        <Kpi label={t("kpi.commitmentsAll")} value={fmtAmount(c.usd, locale, "USD")} help={t("kpi.commitmentsHelp")}
          sub={notConv ? t("kpi.notConvertedAmounts", { amounts: currencyLines(c.unconverted, locale) }) : undefined} href="#/finance" />
        <Kpi label={t("kpi.attention")} value={fmtNum(attention, locale)} help={t("kpi.attentionHelp")} href={href("/projects", { alert: "attention" }, { sort: "alerts" })} />
        <Kpi label={t("kpi.agreements")} value={fmtNum(s.meta.counts.agreements, locale)} href="#/finance" />
        <Kpi label={t("kpi.countriesDocumented")} value={`${withData} / ${s.ref.countries.length}`} href="#/africa" />
      </div>
      <p className="muted small">{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)} · {t("snapshot.latestSource")} {fmtDate(s.meta.latest_source_update, locale)}</p>

      <div className="grid-2 home-2">
        <section className="card">
          <header className="card-h"><h2 className="card-t">{t("home.forTitle")}</h2></header>
          <div className="card-b audiences">
            {audiences.map((x) => (
              <a key={x.k} href={x.to} className="aud"><b>{t(`home.${x.k}`)}</b><span className="small muted">{t(`home.${x.k}d`)}</span></a>
            ))}
          </div>
        </section>
        <section className="card">
          <header className="card-h"><h2 className="card-t">{t("home.why")}</h2></header>
          <div className="card-b">
            <ul className="why">
              <li>{t("home.why1")}</li><li>{t("home.why2")}</li><li>{t("home.why3")}</li>
            </ul>
            <a className="btn sm" href="#/plans">{t("nav.plans")} →</a> <a className="btn sm ghost" href="#/about">{t("nav.about")}</a>
          </div>
        </section>
      </div>

      <h2>{t("home.modules")}</h2>
      <div className="modules">
        {MODULES.map((m) => (
          <a key={m} className="module" href={`#${PATHS[m]}`}>
            <b>{t(`nav.${m}`)}</b>
            <span>{t(`home.m.${m}`)}</span>
          </a>
        ))}
      </div>
    </div>
  );
}
