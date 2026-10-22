import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { ReportForm } from "@/components/report-form";
import { ErrorState, LoginRequired } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV, Num } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet, getMe } from "@/lib/api";
import { refData } from "@/lib/refdata";
import type { Country } from "@/lib/types";

interface Rep { report_uid: string; report_type: string; title: string; fmt: string; period: string | null; generated_at: string; sha256: string; size_bytes: number | null }

export const metadata = { title: "Reports" };

export default async function ReportsPage() {
  const { d, locale } = await getI18n();
  const me = await getMe();
  const [types, ref, countries, mine] = await Promise.all([
    apiGet<{ code: string; title: string }[]>("/reports/types"), refData(locale), apiGet<Country[]>("/countries"), me ? apiGet<Rep[]>("/reports") : Promise.resolve(null),
  ]);
  return (
    <div className="space-y-6">
      <PageHeader title={d.reports.title} subtitle={d.reports.subtitle} />
      <CoverageNotice d={d} />
      <Card>
        <CardHeader title={d.reports.type} />
        <CardBody>
          {types.ok ? <ul className="mb-4 grid gap-1 text-sm sm:grid-cols-2 lg:grid-cols-3">{types.data.map((t) => <li key={t.code}>• {t.title} <span className="font-mono text-xs text-muted">({t.code})</span></li>)}</ul> : <ErrorState d={d} status={types.status} message={types.error} />}
          {!me ? <LoginRequired d={d} next="/reports" /> : types.ok ? (
            <ReportForm types={types.data} sectors={ref.sectors} partners={ref.partners}
              countries={countries.ok ? countries.data.map((c) => [c.iso3, locale === "fr" ? c.name_fr : c.name_en]) : [["CMR", "Cameroon"]]} />
          ) : null}
        </CardBody>
      </Card>
      {mine ? (
        <Card>
          <CardHeader title={d.reports.mine} />
          {!mine.ok ? <CardBody><ErrorState d={d} status={mine.status} message={mine.error} /></CardBody> : mine.data.length === 0 ? <CardBody><p className="text-sm text-muted">{d.reports.noReports}</p></CardBody> : (
            <Table caption={d.reports.mine}>
              <THead><TR><TH>ID</TH><TH>{d.common.name}</TH><TH>{d.reports.format}</TH><TH>{d.reports.period}</TH><TH>{d.reports.generated}</TH><TH className="text-right">{d.reports.size}</TH><TH>SHA-256</TH></TR></THead>
              <TBody>{mine.data.map((r) => (
                <TR key={r.report_uid}><TD className="font-mono text-xs">{r.report_uid}</TD><TD>{r.title}</TD><TD>{r.fmt}</TD><TD>{r.period}</TD><TD><DateV value={r.generated_at} time /></TD><TD className="text-right"><Num value={r.size_bytes} /></TD><TD className="max-w-40 truncate font-mono text-xs" title={r.sha256}>{r.sha256}</TD></TR>))}
              </TBody>
            </Table>
          )}
        </Card>
      ) : null}
    </div>
  );
}
