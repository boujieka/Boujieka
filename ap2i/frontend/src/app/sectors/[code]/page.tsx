import Link from "next/link";
import { notFound } from "next/navigation";
import { StatusBadge, UsdCompleteBadge, VerificationBadge } from "@/components/badges";
import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { SectorAnnualChart } from "@/components/sector-chart";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, Num } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet } from "@/lib/api";
import type { ProjectSummary, SectorRef } from "@/lib/types";

interface Summary {
  sector: SectorRef; country: string; projects: number; by_status: Record<string, number>;
  indicators: { code: string; name_en: string; name_fr: string; unit: string; kind: string }[];
  indicator_observations_linked: number; indicator_note: string;
  annual: { year: number; approved: number | null; active: number | null; commitments_usd: string | null; disbursements_usd: string | null; usd_complete: boolean }[];
  project_list: ProjectSummary[];
}

export default async function SectorPage({ params, searchParams }: { params: Promise<{ code: string }>; searchParams: Promise<{ country?: string }> }) {
  const code = (await params).code.toUpperCase();
  const country = ((await searchParams).country ?? "CMR").toUpperCase();
  if (!/^[A-Z_]+$/.test(code) || !/^[A-Z]{3}$/.test(country)) notFound();
  const { d, locale } = await getI18n();
  const r = await apiGet<Summary>(`/sectors/${code}/summary?country=${country}`);
  if (!r.ok && r.status === 404) notFound();
  if (!r.ok) return <ErrorState d={d} status={r.status} message={r.error} />;
  const s = r.data;
  return (
    <div className="space-y-6">
      <PageHeader eyebrow={`${d.common.sector} · ${s.country}`} title={locale === "fr" ? s.sector.name_fr : s.sector.name_en}
        subtitle={<><Link className="link" href={`/projects?country=${s.country}&sector=${code}`}>{s.projects} {d.common.projects.toLowerCase()}</Link></>} />
      <CoverageNotice d={d} />
      <div className="flex flex-wrap gap-2">
        {Object.entries(s.by_status).map(([k, v]) => <Link key={k} href={`/projects?country=${s.country}&sector=${code}&status=${k}`} className="no-underline"><Badge tone="navy">{label(d.projectStatus, k)}: {v}</Badge></Link>)}
      </div>
      <Card>
        <CardHeader title={d.sectors.indicators} description={s.indicator_note} />
        <Table caption={d.sectors.indicators}>
          <THead><TR><TH>{d.common.name}</TH><TH>{d.sectors.unit}</TH><TH>{d.sectors.kind}</TH><TH>{d.common.value}</TH></TR></THead>
          <TBody>{s.indicators.map((i) => (
            <TR key={i.code}><TD>{locale === "fr" ? i.name_fr : i.name_en}</TD><TD>{i.unit}</TD><TD>{i.kind}</TD>
              <TD>{s.indicator_observations_linked === 0 ? <span className="italic text-muted">{d.sectors.noObservations}</span> : <Num value={s.indicator_observations_linked} />}</TD></TR>))}
          </TBody>
        </Table>
      </Card>
      <Card>
        <CardHeader title={d.sectors.annual} description={d.common.clickToDrill} />
        <CardBody>
          <SectorAnnualChart code={code} country={s.country} annual={s.annual} />
          <Table caption={d.sectors.annual}>
            <THead><TR><TH>{d.common.year}</TH><TH className="text-right">{d.countries.approved}</TH><TH className="text-right">{d.countries.active}</TH><TH className="text-right">{d.countries.commitments} (USD)</TH><TH className="text-right">{d.countries.disbursements} (USD)</TH><TH /></TR></THead>
            <TBody>{s.annual.map((a) => (
              <TR key={a.year}><TD><Link className="link" href={`/projects?country=${s.country}&sector=${code}&year_from=${a.year}&year_to=${a.year}`}>{a.year}</Link></TD><TD className="text-right"><Num value={a.approved} /></TD><TD className="text-right"><Num value={a.active} /></TD>
                <TD className="text-right"><Amount value={a.commitments_usd} currency="USD" /></TD><TD className="text-right"><Amount value={a.disbursements_usd} currency="USD" /></TD><TD><UsdCompleteBadge complete={a.usd_complete} /></TD></TR>))}
            </TBody>
          </Table>
          <Alert tone="info" className="mt-2">{d.common.perCurrency}: <Link className="link" href={`/countries/${s.country}`}>{d.countries.dashboard}</Link></Alert>
        </CardBody>
      </Card>
      <Card>
        <CardHeader title={d.sectors.projectList} />
        <Table caption={d.sectors.projectList}>
          <THead><TR><TH>{d.projects.id}</TH><TH>{d.projects.titleCol}</TH><TH>{d.projects.partners}</TH><TH>{d.common.status}</TH><TH>{d.common.verification}</TH><TH>{d.projects.approval}</TH></TR></THead>
          <TBody>{s.project_list.map((p) => (
            <TR key={p.id}><TD className="font-mono text-xs"><Link className="link" href={`/projects/${p.ap2i_id}`}>{p.ap2i_id}</Link></TD><TD className="min-w-56">{p.title}</TD><TD>{p.partners.join(", ")}</TD><TD><StatusBadge value={p.status} /></TD><TD><VerificationBadge value={p.verification_status} /></TD><TD className="whitespace-nowrap"><DateV value={p.original_approval_date} /></TD></TR>))}
          </TBody>
        </Table>
      </Card>
    </div>
  );
}
