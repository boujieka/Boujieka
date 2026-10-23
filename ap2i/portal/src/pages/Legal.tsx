import type { ReactNode } from "react";
import { useI18n } from "../lib/i18n";
import { ct } from "../lib/i18n-commercial";
import { useSnap } from "../lib/context";
import { fmtDate } from "../lib/format";
import { SITE } from "../lib/site";
import { Badge, Card, ExternalLink, PageHead } from "../components/ui";

const SECTIONS = ["terms", "privacy", "data"] as const;
type Section = (typeof SECTIONS)[number];

const IATI_TERMS = "Licence set per publisher in the IATI Registry; attribution to the reporting organisation.";
const IATI_DOCS = "https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/";

/**
 * Usage terms and documentation URLs exactly as recorded in backend/app/connectors/*.py (`usage_terms`,
 * `documentation_url`). Quoted verbatim (English). Do not add a licence that the repository does not state.
 */
const SOURCE_TERMS: Record<string, { terms: string | null; docs: string | null }> = {
  worldbank_projects: { terms: "World Bank Terms of Use for Datasets; attribution to the World Bank required.", docs: "https://projects.worldbank.org/en/projects-operations/project-search" },
  worldbank_documents: { terms: "World Bank Terms of Use; publicly disclosed documents; attribution to the World Bank.", docs: "https://documents.worldbank.org/en/publication/documents-reports/api" },
  worldbank_iati: { terms: IATI_TERMS, docs: "https://iatiregistry.org/publisher/worldbank" },
  afdb_iati: { terms: IATI_TERMS, docs: "https://www.afdb.org/en/projects-and-operations" },
  afd_iati: { terms: IATI_TERMS, docs: "https://opendata.afd.fr" },
  afdb_documents: { terms: "Public AfDB documents. www.afdb.org serves an anti-bot challenge: those documents are not fetched automatically and can be added through the document upload workflow.", docs: "https://idev.afdb.org" },
  iati_generic: { terms: IATI_TERMS, docs: IATI_DOCS },
  eib_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  eu_intpa_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  ifad_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  undp_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  unicef_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  fao_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  unido_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  bmz_iati: { terms: IATI_TERMS, docs: IATI_DOCS },
  manual_upload: { terms: "Contributor certifies that each row reproduces an official document cited in source_url.", docs: null },
};

function Block({ h, children }: { h: string; children: ReactNode }) {
  return (
    <section className="legal-block" style={{ marginBottom: 14 }}>
      <h2 style={{ fontSize: "1rem", margin: "0 0 4px" }}>{h}</h2>
      {children}
    </section>
  );
}

export function Legal({ section }: { section: string }) {
  const { locale } = useI18n();
  const c = (k: string, v?: Record<string, string | number>) => ct(locale, k, v);
  const s = useSnap();
  const current: Section = (SECTIONS as readonly string[]).includes(section) ? (section as Section) : "terms";
  const date = fmtDate(s.meta.generated_at, locale);
  const pub = SITE.publisher;
  const todo = <span className="badge b-gold" data-testid="publisher-todo">{c("com.publisher.todo")}</span>;
  const contactNode = pub?.email ? <a href={`mailto:${pub.email}`}>{pub.email}</a> : <span>{c("com.contactAddr")} : <em>{c("com.contactAddr.todo")}</em></span>;
  const withContact = (key: string) => {
    const [before, after = ""] = c(key, { contact: "\u0000" }).split("\u0000");
    return <p>{before}{contactNode}{after}</p>;
  };

  return (
    <div>
      <PageHead title={c("com.legal.title")} subtitle={c("com.legal.subtitle")} />
      <nav className="seg" role="tablist" aria-label={c("com.legal.title")} style={{ marginBottom: 12 }}>
        {SECTIONS.map((k) => (
          <a key={k} role="tab" aria-selected={current === k} aria-controls={`legal-${k}`} id={`legal-tab-${k}`}
            className={`btn xs ${current === k ? "" : "ghost"}`} href={`#/legal/${k}`} data-testid={`legal-tab-${k}`}>
            {c(`com.legal.tab.${k}`)}
          </a>
        ))}
      </nav>

      <Card title={c("com.legal.identity")}>
        <dl className="dl">
          <div><dt>{c("com.publisher")}</dt><dd>{pub ? `${pub.name} (${pub.country})` : todo}</dd></div>
          <div><dt>{c("com.contactAddr")}</dt><dd>{pub?.email ? <a href={`mailto:${pub.email}`}>{pub.email}</a> : <em>{c("com.contactAddr.todo")}</em>}</dd></div>
          <div><dt>{c("com.hosting")}</dt><dd>{c("com.hosting.value")}</dd></div>
        </dl>
        <p className="small muted">{c("com.draftNote")}</p>
      </Card>

      <div role="tabpanel" id={`legal-${current}`} aria-labelledby={`legal-tab-${current}`} data-testid={`legal-${current}`}>
        {current === "terms" && (
          <Card title={c("com.legal.tab.terms")}>
            <Block h={c("com.terms.service.h")}><p>{c("com.terms.service.p")}</p></Block>
            <Block h={c("com.terms.calc.h")}><p>{c("com.terms.calc.p")}</p></Block>
            <Block h={c("com.terms.alerts.h")}><p>{c("com.terms.alerts.p")}</p></Block>
            <Block h={c("com.terms.warranty.h")}><p>{c("com.terms.warranty.p")}</p></Block>
            <Block h={c("com.terms.use.h")}>
              <ul>
                {["l1", "l2", "l3", "l4"].map((k) => <li key={k}>{c(`com.terms.use.${k}`)}</li>)}
                <li>{c("com.terms.use.l5")} <a href="#/legal/data">{c("com.legal.tab.data")}</a></li>
              </ul>
            </Block>
            <Block h={c("com.terms.update.h")}>
              <p>{SITE.refreshCadence === "manual"
                ? c("com.terms.update.manual", { date })
                : c("com.terms.update.scheduled", { cadence: c(`com.cadence.${SITE.refreshCadence}`), date })}</p>
            </Block>
            <Block h={c("com.terms.report.h")}>{withContact("com.terms.report.p")}</Block>
          </Card>
        )}

        {current === "privacy" && (
          <Card title={c("com.legal.tab.privacy")}>
            <Block h={c("com.privacy.collect.h")}><p>{c("com.privacy.collect.p")}</p></Block>
            <Block h={c("com.privacy.controller.h")}><p>{pub ? `${pub.name} (${pub.country})` : todo}</p></Block>
            <Block h={c("com.privacy.processor.h")}>
              <p>{c("com.privacy.processor.p")} <ExternalLink href="https://www.netlify.com/privacy/">{c("com.privacy.processor.link")}</ExternalLink></p>
            </Block>
            <Block h={c("com.privacy.purpose.h")}><p>{c("com.privacy.purpose.p")}</p></Block>
            <Block h={c("com.privacy.retention.h")}>
              <p>{c("com.privacy.retention.p")} <Badge tone="gold">{c("com.privacy.retention.todo")}</Badge></p>
            </Block>
            <Block h={c("com.privacy.rights.h")}>{withContact("com.privacy.rights.p")}</Block>
            <Block h={c("com.privacy.storage.h")}><p>{c("com.privacy.storage.p")}</p></Block>
            <Block h={c("com.privacy.cookies.h")}><p>{c("com.privacy.cookies.p")}</p></Block>
          </Card>
        )}

        {current === "data" && (
          <>
            <Card title={c("com.legal.tab.data")} note={c("com.data.iatiMirror")}>
              <p className="small">{c("com.data.intro")}</p>
              <div className="table-wrap">
                <table data-testid="legal-sources">
                  <thead>
                    <tr>
                      <th scope="col">{c("com.data.col.source")}</th>
                      <th scope="col">{c("com.data.col.status")}</th>
                      <th scope="col">{c("com.data.col.sync")}</th>
                      <th scope="col">{c("com.data.col.terms")}</th>
                      <th scope="col">{c("com.data.col.check")}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {s.meta.connectors.map((cn) => {
                      const info = SOURCE_TERMS[cn.key];
                      return (
                        <tr key={cn.key}>
                          <td>{cn.name}<br /><span className="small muted">{cn.key}</span></td>
                          <td>{cn.status}</td>
                          <td>{fmtDate(cn.last_success, locale)}</td>
                          <td style={{ minWidth: 200 }}>
                            {info?.terms
                              ? <><q lang="en">{info.terms}</q>{locale !== "en" && <span className="small muted"> ({c("com.data.original")})</span>}</>
                              : <span className="muted">{c("com.data.noTerms")}</span>}
                          </td>
                          <td>{info?.docs ? <ExternalLink href={info.docs}>{c("com.data.checkLink")}</ExternalLink> : <span className="muted">—</span>}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </Card>

            <Card title={c("com.data.other.h")}>
              <dl className="dl">
                <div><dt>{c("com.data.maps")}</dt><dd>{c("com.data.maps.value")}</dd></div>
                <div><dt>{c("com.data.fx")}</dt><dd>{c("com.data.fx.value")}{s.ref.rate_sources.length > 0 && <span className="small muted"> — {s.ref.rate_sources.join(" · ")}</span>}</dd></div>
              </dl>
            </Card>

            <div className="grid-2">
              <Card title={c("com.data.calc.h")}>
                <p>{c("com.data.calc.p")}</p>
                {!pub && <p>{todo}</p>}
              </Card>
              <Card title={c("com.data.cite.h")}>
                <p>{c("com.data.cite.p", { date, source: c("com.data.cite.source") })}</p>
              </Card>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
