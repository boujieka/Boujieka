import Link from "next/link";
import { StatusBadge, VerificationBadge } from "@/components/badges";
import { CoverageNotice } from "@/components/coverage";
import { FilterBar, one, YEARS, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { Pagination } from "@/components/pagination";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { buttonClass } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, MoneyList } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet, getMe } from "@/lib/api";
import { refData, statusOptions, verificationOptions } from "@/lib/refdata";
import type { Country, CountryDetail, ProjectList } from "@/lib/types";
import { qs } from "@/lib/utils";

export const metadata = { title: "Projects" };
const LIMIT = 50;

export default async function ProjectsPage({ searchParams }: { searchParams: SP }) {
  const { d, locale } = await getI18n();
  const sp = await searchParams;
  const f = {
    country: one(sp.country), sector: one(sp.sector), partner: one(sp.partner), status: one(sp.status), year_from: one(sp.year_from), year_to: one(sp.year_to),
    q: one(sp.q), region: one(sp.region), verification: one(sp.verification), has_alerts: one(sp.has_alerts), sort: one(sp.sort),
  };
  const offset = Math.max(0, Number(one(sp.offset) ?? 0) || 0);
  const [list, countries, ref, me, cd] = await Promise.all([
    apiGet<ProjectList>(`/projects${qs({ ...f, limit: LIMIT, offset })}`),
    apiGet<Country[]>("/countries"),
    refData(locale),
    getMe(),
    apiGet<CountryDetail>(`/countries/${f.country ?? "CMR"}`),
  ]);
  const countryOpts: [string, string][] = countries.ok ? countries.data.filter((c) => c.documented_projects > 0).map((c) => [c.iso3, locale === "fr" ? c.name_fr : c.name_en]) : [];
  const regionOpts: [string, string][] = cd.ok ? cd.data.admin_divisions.map((r) => [r.code, locale === "fr" ? r.name_fr : r.name_en]) : [];
  const statusOpts = statusOptions(d);
  if (f.status && !statusOpts.some(([k]) => k === f.status)) statusOpts.push([f.status, f.status.split(",").map((s) => d.projectStatus[s as keyof typeof d.projectStatus] ?? s).join(" + ")]);
  const exportHref = `/api/proxy/projects/export.csv${qs({ country: f.country, sector: f.sector, partner: f.partner, status: f.status, year_from: f.year_from, year_to: f.year_to, q: f.q })}`;

  return (
    <div>
      <PageHeader title={d.projects.title} subtitle={d.projects.subtitle}
        actions={me ? <a href={exportHref} className={buttonClass("secondary")} download>{d.projects.exportCsv}</a> : <Link href="/login?next=/projects" className={buttonClass("outline")}>{d.projects.exportNeedsLogin}</Link>} />
      <CoverageNotice d={d} className="mb-4" />
      <FilterBar d={d} action="/projects" fields={[
        { name: "q", label: d.projects.q, type: "text", value: f.q },
        { name: "country", label: d.common.country, type: "select", options: countryOpts, value: f.country },
        { name: "sector", label: d.common.sector, type: "select", options: ref.sectors, value: f.sector },
        { name: "partner", label: d.common.partner, type: "select", options: ref.partners, value: f.partner },
        { name: "status", label: d.common.status, type: "select", options: statusOpts, value: f.status },
        { name: "verification", label: d.common.verification, type: "select", options: verificationOptions(d), value: f.verification },
        { name: "year_from", label: d.projects.yearFrom, type: "select", options: YEARS.map((y) => [y, y]), value: f.year_from, allLabel: d.common.any },
        { name: "year_to", label: d.projects.yearTo, type: "select", options: YEARS.map((y) => [y, y]), value: f.year_to, allLabel: d.common.any },
        { name: "region", label: d.projects.region, type: "select", options: regionOpts, value: f.region },
        { name: "sort", label: d.projects.sort, type: "select", options: [["approval", d.projects.sortApproval], ["title", d.projects.sortTitle], ["updated", d.projects.sortUpdated]], value: f.sort, allLabel: d.projects.sortId },
        { name: "has_alerts", label: d.projects.hasAlerts, type: "checkbox", value: f.has_alerts },
      ]} />
      {!list.ok ? <ErrorState d={d} status={list.status} message={list.error} /> : (
        <Card>
          <Pagination d={d} base="/projects" params={f} total={list.data.total} limit={LIMIT} offset={offset} />
          {list.data.items.length === 0 ? <p className="px-4 pb-4 text-sm text-muted">{d.projects.noResults}</p> : (
            <Table caption={d.projects.title}>
              <THead>
                <TR><TH>{d.projects.id}</TH><TH>{d.projects.titleCol}</TH><TH>{d.common.sector}</TH><TH>{d.projects.partners}</TH><TH>{d.common.status}</TH><TH>{d.common.verification}</TH><TH>{d.projects.approval}</TH><TH>{d.projects.committed}</TH><TH className="text-right">{d.projects.alerts}</TH></TR>
              </THead>
              <TBody>
                {list.data.items.map((p) => (
                  <TR key={p.id}>
                    <TD className="whitespace-nowrap font-mono text-xs"><Link className="link" href={`/projects/${p.ap2i_id}`}>{p.ap2i_id}</Link></TD>
                    <TD className="min-w-56"><Link className="hover:underline" href={`/projects/${p.ap2i_id}`}>{p.title}</Link>{p.private ? <Badge tone="gold" className="ml-1">private</Badge> : null}</TD>
                    <TD>{p.sector ? (locale === "fr" ? p.sector.name_fr : p.sector.name_en) : <span className="italic text-muted">{d.common.na}</span>}</TD>
                    <TD className="whitespace-nowrap">{p.partners.join(", ") || <span className="italic text-muted">{d.common.na}</span>}</TD>
                    <TD><StatusBadge value={p.status} /></TD>
                    <TD><VerificationBadge value={p.verification_status} /></TD>
                    <TD className="whitespace-nowrap"><DateV value={p.original_approval_date} /></TD>
                    <TD><MoneyList value={p.committed_by_currency} /></TD>
                    <TD className="text-right">{p.active_alerts ? <Link className="link" href={`/projects/${p.ap2i_id}#alerts`}>{p.active_alerts}</Link> : <span className="text-muted">0</span>}</TD>
                  </TR>
                ))}
              </TBody>
            </Table>
          )}
          <Pagination d={d} base="/projects" params={f} total={list.data.total} limit={LIMIT} offset={offset} />
        </Card>
      )}
    </div>
  );
}
