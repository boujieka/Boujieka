import Link from "next/link";
import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import type { Country } from "@/lib/types";

export const metadata = { title: "Countries" };

export default async function CountriesPage() {
  const { d, locale } = await getI18n();
  const r = await apiGet<Country[]>("/countries");
  return (
    <div>
      <PageHeader title={d.countries.title} subtitle={d.countries.subtitle} />
      <CoverageNotice d={d} className="mb-4" />
      {!r.ok ? <ErrorState d={d} status={r.status} message={r.error} /> : (
        <Card>
          <Table caption={d.countries.title}>
            <THead><TR><TH>{d.common.country}</TH><TH>ISO</TH><TH>{d.countries.region}</TH><TH>{d.countries.currency}</TH><TH className="text-right">{d.africa.documented}</TH><TH>{d.africa.coverage}</TH></TR></THead>
            <TBody>
              {r.data.map((c) => (
                <TR key={c.iso3}>
                  <TD><Link className="link" href={`/countries/${c.iso3}`}>{locale === "fr" ? c.name_fr : c.name_en}</Link></TD>
                  <TD className="font-mono text-xs">{c.iso3}</TD>
                  <TD>{c.region}</TD>
                  <TD>{c.currency}</TD>
                  <TD className="text-right tabular-nums">{c.documented_projects > 0 ? <Link className="link" href={`/projects?country=${c.iso3}`}>{c.documented_projects}</Link> : <span className="italic text-muted">{d.common.na}</span>}</TD>
                  <TD>{c.documented_projects > 0 ? <Badge tone="emerald">{d.coverage.short}</Badge> : <Badge tone="outline">{d.countries.noRecords}</Badge>}</TD>
                </TR>
              ))}
            </TBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
