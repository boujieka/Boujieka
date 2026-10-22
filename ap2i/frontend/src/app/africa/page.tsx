import Link from "next/link";
import { AfricaMap } from "@/components/africa/africa-map";
import { CoverageNotice } from "@/components/coverage";
import { FilterBar, one, YEARS, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, MoneyList, Num } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { refData, statusOptions, verificationOptions } from "@/lib/refdata";
import type { Country, Overview } from "@/lib/types";
import { qs } from "@/lib/utils";

export const metadata = { title: "Africa" };

export default async function AfricaPage({ searchParams }: { searchParams: SP }) {
  const { d, locale } = await getI18n();
  const sp = await searchParams;
  const f = { year: one(sp.year), sector: one(sp.sector), partner: one(sp.partner), instrument: one(sp.instrument), status: one(sp.status), verification: one(sp.verification) };
  const [ov, countries, ref] = await Promise.all([apiGet<Overview>(`/africa/overview${qs(f)}`), apiGet<Country[]>("/countries"), refData(locale)]);
  const region = new Map(countries.ok ? countries.data.map((c) => [c.iso3, c.region]) : []);
  return (
    <div>
      <PageHeader title={d.africa.title} subtitle={d.africa.subtitle} />
      <CoverageNotice d={d} className="mb-4" />
      <FilterBar d={d} action="/africa" fields={[
        { name: "year", label: d.common.year, type: "select", options: YEARS.map((y) => [y, y]), value: f.year },
        { name: "sector", label: d.common.sector, type: "select", options: ref.sectors, value: f.sector },
        { name: "partner", label: d.common.partner, type: "select", options: ref.partners, value: f.partner },
        { name: "instrument", label: d.common.instrument, type: "select", options: ref.instruments, value: f.instrument },
        { name: "status", label: d.common.status, type: "select", options: statusOptions(d), value: f.status },
        { name: "verification", label: d.common.verification, type: "select", options: verificationOptions(d), value: f.verification },
      ]} />
      {!ov.ok ? <ErrorState d={d} status={ov.status} message={ov.error} /> : (
        <>
          <AfricaMap countries={ov.data.countries} />
          <Card className="mt-6">
            <CardHeader title={d.africa.tableTitle} />
            <Table caption={d.africa.tableTitle}>
              <THead>
                <TR>
                  <TH>{d.common.country}</TH>
                  <TH>{d.africa.region}</TH>
                  <TH className="text-right">{d.africa.documented}</TH>
                  <TH className="text-right">{d.africa.commitmentsUsd}</TH>
                  <TH>{d.africa.commitmentsByCurrency}</TH>
                  <TH>{d.africa.disbursementsByCurrency}</TH>
                  <TH className="text-right">{d.africa.underImplementation}</TH>
                  <TH className="text-right">{d.africa.completed}</TH>
                  <TH className="text-right">{d.africa.operational}</TH>
                  <TH className="text-right">{d.africa.attention}</TH>
                  <TH>{d.africa.coverage}</TH>
                  <TH>{d.africa.lastUpdate}</TH>
                </TR>
              </THead>
              <TBody>
                {[...ov.data.countries].sort((a, b) => (locale === "fr" ? a.name_fr.localeCompare(b.name_fr, "fr") : a.name_en.localeCompare(b.name_en, "en"))).map((c) => (
                  <TR key={c.iso3} className={c.has_data ? "" : "text-muted"}>
                    <TD className="whitespace-nowrap">
                      <Link className="link" href={`/countries/${c.iso3}`}>{locale === "fr" ? c.name_fr : c.name_en}</Link>
                      {!c.has_data ? <Badge tone="outline" className="ml-2">{d.africa.legendNoData}</Badge> : null}
                    </TD>
                    <TD className="whitespace-nowrap">{region.get(c.iso3) ?? ""}</TD>
                    <TD className="text-right">{c.has_data ? <Link className="link" href={`/projects?country=${c.iso3}`}><Num value={c.documented_projects} /></Link> : <Num value={c.documented_projects} />}</TD>
                    <TD className="text-right"><Amount value={c.commitments_usd} currency="USD" /></TD>
                    <TD><MoneyList value={c.commitments_by_currency} /></TD>
                    <TD><MoneyList value={c.disbursements_by_currency ?? null} /></TD>
                    <TD className="text-right">{c.has_data ? <Link className="link" href={`/projects?country=${c.iso3}&status=active`}><Num value={c.under_implementation} /></Link> : <Num value={c.under_implementation} />}</TD>
                    <TD className="text-right">{c.has_data ? <Link className="link" href={`/projects?country=${c.iso3}&status=completed,closed`}><Num value={c.completed} /></Link> : <Num value={c.completed} />}</TD>
                    <TD className="text-right"><Num value={c.operational} /></TD>
                    <TD className="text-right">{c.has_data ? <Link className="link" href={`/performance?country=${c.iso3}&level=high_attention,critical_attention`}><Num value={c.requiring_attention} /></Link> : <Num value={c.requiring_attention} />}</TD>
                    <TD className="min-w-40 text-xs">{c.data_coverage}</TD>
                    <TD className="whitespace-nowrap"><DateV value={c.last_update} /></TD>
                  </TR>
                ))}
              </TBody>
            </Table>
          </Card>
        </>
      )}
    </div>
  );
}
