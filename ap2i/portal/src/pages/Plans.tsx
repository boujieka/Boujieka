import { useI18n } from "../lib/i18n";
import { ct } from "../lib/i18n-commercial";
import { useSnap } from "../lib/context";
import { fmtDate } from "../lib/format";
import { Badge, Card, PageHead } from "../components/ui";

/**
 * Mirror of the plan catalogue in backend/app/reference/catalog.py (PLANS). Prices are NULL there ("on request"),
 * so no price is shown here. Keep this list in sync with the catalogue — never add a feature that is not in it.
 */
export const PLANS: { code: string; name_fr: string; name_en: string; billing_period: "month" | "year" | null; features: string[] }[] = [
  { code: "public", name_fr: "Public", name_en: "Public", billing_period: null,
    features: ["basic_search", "country_summaries", "public_dashboards"] },
  { code: "professional", name_fr: "Professionnel", name_en: "Professional", billing_period: "month",
    features: ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
      "project_details", "custom_filters", "exports", "saved_searches"] },
  { code: "institutional", name_fr: "Institutionnel", name_en: "Institutional", billing_period: "year",
    features: ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
      "project_details", "custom_filters", "exports", "saved_searches", "private_portfolios",
      "project_rescue", "team_collaboration", "advanced_reports", "institutional_imports"] },
  { code: "enterprise", name_fr: "Entreprise", name_en: "Enterprise", billing_period: "year",
    features: ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
      "project_details", "custom_filters", "exports", "saved_searches", "private_portfolios",
      "project_rescue", "team_collaboration", "advanced_reports", "institutional_imports",
      "api_access", "custom_integrations", "dedicated_workspace"] },
];

export function planName(code: string, locale: "fr" | "en"): string | null {
  const p = PLANS.find((x) => x.code === code);
  return p ? (locale === "fr" ? p.name_fr : p.name_en) : null;
}

export function Plans() {
  const { locale } = useI18n();
  const c = (k: string, v?: Record<string, string | number>) => ct(locale, k, v);
  const s = useSnap();
  const features = [...new Set(PLANS.flatMap((p) => p.features))];
  const name = (p: (typeof PLANS)[number]) => (locale === "fr" ? p.name_fr : p.name_en);

  return (
    <div>
      <PageHead title={c("com.plans.title")} subtitle={c("com.plans.subtitle")}>
        <a className="btn gold" href="#/contact">{c("com.plans.request")}</a>
      </PageHead>

      <div className="grid-2">
        <Card title={c("com.plans.portal.title")}>
          <ul className="small">
            <li>{c("com.plans.portal.b1", { date: fmtDate(s.meta.generated_at, locale) })}</li>
            <li>{c("com.plans.portal.b2")}</li>
            <li>{c("com.plans.portal.b3")}</li>
          </ul>
        </Card>
        <Card title={c("com.plans.app.title")}>
          <ul className="small">
            <li>{c("com.plans.app.b1")}</li>
            <li>{c("com.plans.app.b2")}</li>
            <li>{c("com.plans.app.b3")}</li>
          </ul>
        </Card>
      </div>

      <div className="cards plan-cards" role="list">
        {PLANS.map((p, i) => {
          const prev = i > 0 ? PLANS[i - 1] : null;
          const added = prev ? p.features.filter((f) => !prev.features.includes(f)) : p.features;
          const isPublic = p.code === "public";
          return (
            <article key={p.code} className="pcard plan-card" role="listitem" aria-labelledby={`plan-${p.code}`} data-testid={`plan-${p.code}`}>
              <h2 id={`plan-${p.code}`} className="plan-name">{name(p)}</h2>
              <p className="small muted" style={{ margin: 0 }}>
                <Badge tone={isPublic ? "green" : "navy"}>{isPublic ? c("com.plans.where.portal") : c("com.plans.where.app")}</Badge>
              </p>
              <p className="plan-price" style={{ margin: "4px 0", fontWeight: 700 }}>
                {isPublic ? c("com.plans.free") : c("com.plans.onRequest")}
                {p.billing_period && <span className="small muted" style={{ fontWeight: 400 }}> · {c(`com.plans.billing.${p.billing_period}`)}</span>}
              </p>
              {prev && <p className="small muted" style={{ margin: 0 }}>{c("com.plans.includes", { plan: name(prev) })}</p>}
              <ul className="small" style={{ paddingLeft: "1.1rem", margin: "4px 0" }}>
                {added.map((f) => <li key={f}>{c(`com.feat.${f}`)}</li>)}
              </ul>
              <div className="pcard-f">
                {isPublic
                  ? <span className="small">{c("com.plans.here")}</span>
                  : <a className="btn sm" href={`#/contact?plan=${encodeURIComponent(p.code)}`} data-testid={`plan-cta-${p.code}`}>{c("com.plans.request")}</a>}
              </div>
            </article>
          );
        })}
      </div>
      <p className="small muted">{c("com.plans.priceNote")}</p>

      <Card title={c("com.plans.compare")}>
        <div className="table-wrap">
          <table data-testid="plans-compare">
            <caption className="small muted" style={{ textAlign: "left", paddingBottom: 6 }}>{c("com.plans.compare")}</caption>
            <thead>
              <tr>
                <th scope="col">{c("com.plans.feature")}</th>
                {PLANS.map((p) => <th scope="col" key={p.code} style={{ textAlign: "center" }}>{name(p)}</th>)}
              </tr>
            </thead>
            <tbody>
              {features.map((f) => (
                <tr key={f}>
                  <th scope="row" style={{ background: "transparent", color: "inherit", fontWeight: 400, whiteSpace: "normal" }}>{c(`com.feat.${f}`)}</th>
                  {PLANS.map((p) => (
                    <td key={p.code} style={{ textAlign: "center" }}>
                      {p.features.includes(f)
                        ? <span role="img" aria-label={c("com.yes")}>✓</span>
                        : <span role="img" aria-label={c("com.no")} className="muted">—</span>}
                    </td>
                  ))}
                </tr>
              ))}
              <tr>
                <th scope="row" style={{ background: "transparent", color: "inherit", whiteSpace: "normal" }}>{c("com.plans.price")}</th>
                {PLANS.map((p) => <td key={p.code} style={{ textAlign: "center" }}>{p.code === "public" ? c("com.plans.free") : c("com.plans.onRequest")}</td>)}
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
