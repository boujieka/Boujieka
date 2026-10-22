import Link from "next/link";
import { notFound } from "next/navigation";
import { AnnualPortfolio, type SlimYear } from "@/components/country/annual-portfolio";
import { AlertLevelChart, SectorChart, StatusChart } from "@/components/country/dashboard-charts";
import { CoverageNotice } from "@/components/coverage";
import { Kpi, PageHeader } from "@/components/page-header";
import { ReportButton } from "@/components/report-button";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, MoneyList, Num, Pct } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet, getMe, hasFeature } from "@/lib/api";
import { fmtNumber } from "@/lib/format";
import type { CountryDetail, Dashboard, Portfolio } from "@/lib/types";

export async function generateMetadata({ params }: { params: Promise<{ iso3: string }> }) {
  return { title: (await params).iso3.toUpperCase() };
}

export default async function CountryPage({ params }: { params: Promise<{ iso3: string }> }) {
  const iso3 = (await params).iso3.toUpperCase();
  if (!/^[A-Z]{3}$/.test(iso3)) notFound();
  const { d, locale } = await getI18n();
  const [detail, dash, me] = await Promise.all([apiGet<CountryDetail>(`/countries/${iso3}`), apiGet<Dashboard>(`/countries/${iso3}/dashboard`), getMe()]);
  if (!detail.ok && detail.status === 404) notFound();
  if (!detail.ok) return <ErrorState d={d} status={detail.status} message={detail.error} />;
  const c = detail.data;
  const name = locale === "fr" ? c.name_fr : c.name_en;
  const hasData = dash.ok && dash.data.documented_projects > 0;
  const pf = dash.ok ? await apiGet<Portfolio>(`/countries/${iso3}/portfolio?year_from=2011&year_to=2026`) : null;
  const years: SlimYear[] = pf?.ok
    ? pf.data.years.map((y) => ({
        year: y.year, approved: y.counts.approved, active: y.counts.active, completed: y.counts.completed, undated: y.counts.undated_projects_excluded ?? null,
        commitments: { by_currency: y.commitments.by_currency, usd: y.commitments.usd_equivalent, usd_complete: y.commitments.usd_complete, rate_sources: y.commitments.rate_sources, transactions: y.commitments.transactions },
        disbursements: { by_currency: y.disbursements.by_currency, usd: y.disbursements.usd_equivalent, usd_complete: y.disbursements.usd_complete, rate_sources: y.disbursements.rate_sources, transactions: y.disbursements.transactions },
      }))
    : [];
  const canExport = hasFeature(me, "exports");

  return (
    <div className="space-y-6">
      <PageHeader eyebrow={d.countries.dashboard} title={name} subtitle={`${c.iso3} · ${c.region ?? ""} · ${c.currency ?? ""}`}
        actions={hasData ? (
          me && canExport ? <ReportButton request={{ report_type: "annual_portfolio", format: "xlsx", country: iso3, year_from: 2011, year_to: 2026 }} label={d.countries.downloadExcel} busyLabel={d.reports.generating} />
            : <p className="max-w-xs text-xs text-muted">{d.countries.downloadNeedsLogin} {!me ? <Link className="link" href={`/login?next=/countries/${iso3}`}>{d.nav.login}</Link> : <Link className="link" href="/pricing">{d.common.seePricing}</Link>}</p>
        ) : null} />
      <CoverageNotice d={d} apiText={dash.ok ? dash.data.coverage_warning : null} />

      {!dash.ok ? <ErrorState d={d} status={dash.status} message={dash.error} /> : !hasData ? (
        <Alert tone="info" title={d.countries.noRecords}><p>{d.countries.noRecordsText}</p>{pf?.ok && pf.data.coverage_note ? <p className="mt-1 text-xs">API: “{pf.data.coverage_note}”</p> : null}</Alert>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <Kpi label={d.africa.documented} value={fmtNumber(dash.data.documented_projects, locale)} href={`/projects?country=${iso3}`} />
            <Kpi label={d.africa.underImplementation} value={fmtNumber(dash.data.by_status.active ?? null, locale) ?? d.common.na} href={`/projects?country=${iso3}&status=active`} />
            <Kpi label={d.countries.alertsByLevel} value={fmtNumber(Object.values(dash.data.alerts_by_level).reduce((a, b) => a + b, 0), locale)} href={`/performance?country=${iso3}`} />
            <Kpi label={d.countries.agreements} value={fmtNumber(dash.data.by_partner.reduce((a, p) => a + p.agreements, 0), locale)} href={`/explorer?country=${iso3}&flow=commitment`} />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <Card><CardHeader title={d.countries.statusMix} /><CardBody><StatusChart iso3={iso3} byStatus={dash.data.by_status} /></CardBody></Card>
            <Card><CardHeader title={d.countries.alertsByLevel} /><CardBody><AlertLevelChart iso3={iso3} levels={dash.data.alerts_by_level} /></CardBody></Card>
          </div>

          <Card><CardHeader title={d.countries.bySector} description={d.common.clickToDrill} /><CardBody><SectorChart iso3={iso3} sectors={dash.data.by_sector} />
            <div className="mt-3">
              <Table caption={d.countries.bySector}>
                <THead><TR><TH>{d.common.sector}</TH><TH className="text-right">{d.countries.projectsCount}</TH><TH className="text-right">{d.countries.active}</TH><TH className="text-right">{d.countries.committedUsd}</TH></TR></THead>
                <TBody>{dash.data.by_sector.map((s) => (
                  <TR key={s.code}>
                    <TD>{s.code === "UNCLASSIFIED" ? (locale === "fr" ? s.name_fr : s.name_en) : <Link className="link" href={`/sectors/${s.code}`}>{locale === "fr" ? s.name_fr : s.name_en}</Link>}</TD>
                    <TD className="text-right">{s.code === "UNCLASSIFIED" ? <Num value={s.projects} /> : <Link className="link" href={`/projects?country=${iso3}&sector=${s.code}`}><Num value={s.projects} /></Link>}</TD>
                    <TD className="text-right"><Num value={s.active} /></TD>
                    <TD className="text-right"><Amount value={s.committed_usd} currency="USD" /></TD>
                  </TR>))}
                </TBody>
              </Table>
              <p className="mt-1 text-xs text-muted">{d.common.method}: {dash.data.usd_method}</p>
            </div>
          </CardBody></Card>

          <Card>
            <CardHeader title={d.countries.byPartner} />
            <Table caption={d.countries.byPartner}>
              <THead><TR><TH>{d.common.partner}</TH><TH className="text-right">{d.countries.agreements}</TH><TH>{d.countries.committed} — {d.common.perCurrency}</TH><TH>{d.countries.disbursed} — {d.common.perCurrency}</TH><TH className="text-right">{d.countries.committedUsd}</TH></TR></THead>
              <TBody>{dash.data.by_partner.map((p) => (
                <TR key={p.partner}>
                  <TD>{p.code ? <Link className="link" href={`/projects?country=${iso3}&partner=${p.code}`}>{p.partner}</Link> : p.partner}</TD>
                  <TD className="text-right"><Num value={p.agreements} /></TD>
                  <TD><MoneyList value={p.committed_by_currency} /></TD>
                  <TD>{p.code ? <Link className="no-underline hover:underline" href={`/explorer?country=${iso3}&partner=${p.code}&flow=disbursement`}><MoneyList value={p.disbursed_by_currency} /></Link> : <MoneyList value={p.disbursed_by_currency} />}</TD>
                  <TD className="text-right"><Amount value={p.committed_usd} currency="USD" /></TD>
                </TR>))}
              </TBody>
            </Table>
            <p className="px-4 pb-3 text-xs text-muted">{d.common.method}: {dash.data.usd_method}</p>
          </Card>

          <div className="grid gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader title={d.countries.dataGaps} />
              <Table caption={d.countries.dataGaps}>
                <THead><TR><TH>{d.common.name}</TH><TH className="text-right">{d.common.projects}</TH><TH className="text-right">%</TH></TR></THead>
                <TBody>{Object.entries(dash.data.data_gaps).map(([k, v]) => (
                  <TR key={k}><TD>{k}</TD><TD className="text-right"><Num value={v} /></TD><TD className="text-right"><Pct value={v / dash.data.documented_projects} digits={0} /></TD></TR>))}
                </TBody>
              </Table>
              <p className="px-4 pb-3 text-xs"><Link className="link" href="/explorer#quality">{d.explorer.quality} →</Link></p>
            </Card>
            <Card>
              <CardHeader title={d.countries.quality} />
              <CardBody>
                <dl className="space-y-2 text-sm">{Object.entries(dash.data.average_quality).map(([k, v]) => (
                  <div key={k}>
                    <div className="flex justify-between"><dt>{label(d.project.scores, k)}</dt><dd><Pct value={v} digits={0} /></dd></div>
                    {v !== null ? <div className="mt-1 h-2 rounded bg-gray-bg"><div className="h-2 rounded bg-emerald" style={{ width: `${Math.round(v * 100)}%` }} /></div> : null}
                  </div>))}
                </dl>
              </CardBody>
            </Card>
          </div>

          <Card>
            <CardHeader title={d.countries.annualTitle} description={pf?.ok ? pf.data.coverage_note : undefined} />
            <CardBody>{pf && !pf.ok ? <ErrorState d={d} status={pf.status} message={pf.error} /> : pf?.ok && (pf.data.has_data === false || years.length === 0) ? <Alert tone="info" title={d.countries.noRecords}><p>{pf.data.coverage_note}</p></Alert> : <AnnualPortfolio iso3={iso3} years={years} />}</CardBody>
          </Card>
        </>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title={d.countries.adminDivisions} />
          {c.admin_divisions.length ? (
            <Table caption={d.countries.adminDivisions}>
              <THead><TR><TH>{d.common.code}</TH><TH>{d.common.name}</TH><TH>{d.common.type}</TH></TR></THead>
              <TBody>{c.admin_divisions.map((r) => (
                <TR key={r.code}><TD className="font-mono text-xs">{hasData ? <Link className="link" href={`/projects?country=${iso3}&region=${r.code}`}>{r.code}</Link> : r.code}</TD><TD>{locale === "fr" ? r.name_fr : r.name_en}</TD><TD>{r.division_type}</TD></TR>))}
              </TBody>
            </Table>
          ) : <CardBody><p className="text-sm italic text-muted">{d.common.na}</p></CardBody>}
        </Card>
        <Card>
          <CardHeader title={d.countries.dataSources} />
          {c.data_sources.length ? (
            <Table caption={d.countries.dataSources}>
              <THead><TR><TH>{d.common.name}</TH><TH>{d.countries.institution}</TH><TH>{d.countries.accessMethod}</TH><TH>{d.countries.reachability}</TH></TR></THead>
              <TBody>{c.data_sources.map((s) => (
                <TR key={s.name + s.institution}>
                  <TD>{s.url ? <a className="link" href={s.url} target="_blank" rel="noopener noreferrer">{s.name}</a> : s.name}<div className="text-xs text-muted">{s.category}</div></TD>
                  <TD>{s.institution}</TD><TD className="text-xs">{s.access_method}</TD>
                  <TD><Badge tone="outline">{s.reachability}</Badge><div className="text-xs"><DateV value={s.last_checked_at} /></div></TD>
                </TR>))}
              </TBody>
            </Table>
          ) : <CardBody><p className="text-sm italic text-muted">{d.common.na}</p></CardBody>}
        </Card>
      </div>
      <Card>
        <CardBody className="grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-4">
          <div><span className="text-muted">{d.countries.subregion}: </span>{c.subregion ?? d.common.na}</div>
          <div><span className="text-muted">{d.countries.languages}: </span>{c.official_languages?.join(", ") || d.common.na}</div>
          <div><span className="text-muted">{d.countries.referenceStatus}: </span><Badge tone="outline">{c.reference_status ?? d.common.na}</Badge></div>
          <div className="text-xs text-muted sm:col-span-2 lg:col-span-4">{c.reference_note}</div>
        </CardBody>
      </Card>
    </div>
  );
}
