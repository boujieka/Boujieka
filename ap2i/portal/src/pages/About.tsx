import { useI18n } from "../lib/i18n";
import { useSnap } from "../lib/context";
import { fmtDate, fmtNum } from "../lib/format";
import { Badge, Card, PageHead } from "../components/ui";
import { GLOSSARY } from "../lib/i18n-ux";

export function About() {
  const { t, locale } = useI18n();
  const s = useSnap();
  const m = s.meta;
  const meth = s.ref.methodology as Record<string, unknown>;
  const text = (v: unknown): string => (typeof v === "string" ? v : Array.isArray(v) ? v.map(text).join(" ") : v && typeof v === "object" ? Object.values(v).map(text).join(" ") : "");
  return (
    <div>
      <PageHead title={t("about.title")} subtitle={m.scope} />
      <div className="grid-2">
        <Card title={t("about.reconciliation")}>
          {m.reconciliation.map((r, i) => (
            <p key={i}><Badge tone={r.ok ? "green" : "gold"}>{r.ok ? "OK" : "!"}</Badge> {r.country} — {r.check ?? r.method}</p>
          ))}
          <p className="small">{t("about.recOk")}</p>
          <p className="small muted">{t("about.checksum")} : <span className="mono wrap">{m.checksum}</span></p>
        </Card>
        <Card title={t("about.files")}>
          <dl className="dl">
            <div><dt>{t("snapshot.asOf")}</dt><dd>{fmtDate(m.generated_at, locale)}</dd></div>
            <div><dt>{t("snapshot.latestSource")}</dt><dd>{fmtDate(m.latest_source_update, locale)}</dd></div>
            <div><dt>{t("kpi.projects")}</dt><dd>{fmtNum(m.counts.projects, locale)}</dd></div>
            <div><dt>{t("kpi.agreements")}</dt><dd>{fmtNum(m.counts.agreements, locale)}</dd></div>
            <div><dt>{t("money.transactions")}</dt><dd>{fmtNum(m.counts.transactions, locale)}</dd></div>
            <div><dt>{t("kpi.alerts")}</dt><dd>{fmtNum(m.counts.alerts, locale)}</dd></div>
          </dl>
          <p className="small muted">{t("money.note")} {s.ref.rate_sources.join(" · ")}</p>
        </Card>
      </div>
      <Card title={t("about.coverageTitle")}>
        <ul>
          <li>{t("about.cov1")}</li><li>{t("about.cov2")}</li><li>{t("about.cov3")}</li>
        </ul>
        <p className="small">{t("about.cadence")}</p>
      </Card>
      <Card title={t("about.measuresTitle")}>
        <dl className="glossary">
          {["m1", "m2", "m3"].map((k) => <div key={k}><dt>{t(`about.${k}`)}</dt><dd>{t(`about.${k}d`)}</dd></div>)}
        </dl>
        <p className="small muted">{t("money.note")}</p>
      </Card>
      <Card title={t("about.glossary")} id="glossary">
        <dl className="glossary">
          {GLOSSARY.map((k) => <div key={k}><dt>{t(`g.${k}`)}</dt><dd>{t(`g.${k}D`)}</dd></div>)}
        </dl>
      </Card>
      <Card title={t("about.connectors")}>
        <div className="table-wrap">
          <table>
            <thead><tr><th scope="col">{t("about.connector")}</th><th scope="col">{t("about.status")}</th><th scope="col">{t("about.lastSuccess")}</th></tr></thead>
            <tbody>{m.connectors.map((c) => <tr key={c.key}><td>{c.name}</td><td>{c.status}</td><td>{fmtDate(c.last_success, locale)}</td></tr>)}</tbody>
          </table>
        </div>
      </Card>
      <Card title={t("about.limits")}>
        <ul className="small">
          <li>{s.dataQuality.coverage_warning}</li>
          {Object.entries(s.dataQuality.missing_information).slice(0, 8).map(([k, v]) => <li key={k}>{k} : {fmtNum(v, locale)} / {fmtNum(s.dataQuality.projects, locale)}</li>)}
          <li>{locale === "fr" ? "Ce portail est une copie publique en lecture seule : comptes, plans officiels Project Rescue et données privées des organisations ne sont disponibles que dans l'application AP²I." : "This portal is a public read-only copy: accounts, official Project Rescue plans and organisations' private data are only available in the AP²I application."}</li>
        </ul>
      </Card>
      <Card title={t("about.methodology")}>
        {Object.entries(meth).map(([k, v]) => <details key={k}><summary>{k.replace(/_/g, " ")}</summary><p className="small pre">{text(v)}</p></details>)}
      </Card>
    </div>
  );
}
