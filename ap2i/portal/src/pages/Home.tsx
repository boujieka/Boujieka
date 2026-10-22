import { useI18n } from "../lib/i18n";
import { useSnap, useSelection } from "../lib/context";
import { commitmentsOf } from "../lib/agg";
import { fmtAmount, fmtDate, fmtNum } from "../lib/format";
import { href } from "../lib/router";
import { Kpi } from "../components/ui";

const MODULES = ["africa", "country", "projects", "finance", "performance", "rescue", "data"] as const;
const PATHS: Record<string, string> = { africa: "/africa", country: "/country/CMR", projects: "/projects", finance: "/finance",
  performance: "/performance", rescue: "/rescue", data: "/data" };

export function Home() {
  const { t, locale } = useI18n();
  const s = useSnap();
  const sel = useSelection({});
  const c = commitmentsOf(sel.agreements);
  const withData = s.ref.countries.filter((x) => x.documented_projects > 0).length;
  return (
    <div className="home">
      <section className="hero">
        <img src={`${import.meta.env.BASE_URL}ap2i-logo.png`} alt="AP²I" width={132} height={132} />
        <div>
          <p className="kicker">AP²I — {t("app.name")}</p>
          <h1>{t("app.tagline")}</h1>
          <p className="lead">{t("home.lead")}</p>
          <a className="btn gold" href="#/africa">{t("home.explore")}</a>
          <a className="btn outline-w" href="#/country/CMR">{t("home.cameroon")}</a>
        </div>
      </section>
      <div className="kpis">
        <Kpi label={t("kpi.projects")} value={fmtNum(s.meta.counts.projects, locale)} href="#/projects" />
        <Kpi label={t("kpi.commitments")} value={fmtAmount(c.usd, locale, "USD")} sub={t("kpi.commitmentsNote", { n: s.agreements.filter((a) => a.committed !== null && a.committed_usd === null).length })} href="#/finance" />
        <Kpi label={t("kpi.agreements")} value={fmtNum(s.meta.counts.agreements, locale)} href="#/finance" />
        <Kpi label={t("kpi.alerts")} value={fmtNum(s.meta.counts.alerts, locale)} href={href("/performance", {})} />
        <Kpi label={t("metric.coverage")} value={`${withData} / ${s.ref.countries.length}`} sub={t("africa.subtitle").split(".")[0]} href="#/africa" />
      </div>
      <p className="muted small">{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)} · {t("snapshot.latestSource")} {fmtDate(s.meta.latest_source_update, locale)}</p>
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
