import Link from "next/link";
import { NatureBadge } from "@/components/badges";
import { CoverageNotice } from "@/components/coverage";
import { FilterBar, one, YEARS, type SP } from "@/components/filter-bar";
import { Kpi, PageHeader } from "@/components/page-header";
import { Pagination } from "@/components/pagination";
import { ErrorState } from "@/components/states";
import { Badge } from "@/components/ui/badge";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, Num, Pct, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet } from "@/lib/api";
import { refData } from "@/lib/refdata";
import type { DataQuality } from "@/lib/types";
import { qs } from "@/lib/utils";

interface Tx { id: number; flow: string; amount: string | null; currency: string | null; value_date: string | null; agreement: string | null; partner_id: number | null; project: { id: number; ap2i_id: string; title: string }; source_record_id: number | null; data_nature: string | null }

export const metadata = { title: "Data Explorer" };
const LIMIT = 100;

export default async function ExplorerPage({ searchParams }: { searchParams: SP }) {
  const { d, locale } = await getI18n();
  const sp = await searchParams;
  const f = { flow: one(sp.flow) ?? "disbursement", country: one(sp.country), partner: one(sp.partner), year: one(sp.year), currency: one(sp.currency) };
  const offset = Math.max(0, Number(one(sp.offset) ?? 0) || 0);
  const [tx, dq, ref] = await Promise.all([apiGet<{ total: number; items: Tx[] }>(`/explorer/transactions${qs({ ...f, limit: LIMIT, offset })}`), apiGet<DataQuality>(`/data-quality${qs({ country: f.country })}`), refData(locale)]);
  const flowLabel = (x: string) => (x === "commitment" ? d.explorer.flowCommitment : x === "expenditure" ? d.explorer.flowExpenditure : d.explorer.flowDisbursement);
  return (
    <div className="space-y-6">
      <PageHeader title={d.explorer.title} subtitle={d.explorer.subtitle} />
      <CoverageNotice d={d} />
      <section aria-labelledby="tx-title">
        <h2 id="tx-title" className="mb-2 text-lg font-semibold text-navy">{d.explorer.transactions}</h2>
        <FilterBar d={d} action="/explorer" fields={[
          { name: "flow", label: d.explorer.flow, type: "select", options: [["commitment", d.explorer.flowCommitment], ["disbursement", d.explorer.flowDisbursement], ["expenditure", d.explorer.flowExpenditure]], value: f.flow, allLabel: d.explorer.flowDisbursement },
          { name: "country", label: d.common.country, type: "select", options: [["CMR", locale === "fr" ? "Cameroun" : "Cameroon"]], value: f.country },
          { name: "partner", label: d.common.partner, type: "select", options: ref.partners, value: f.partner },
          { name: "year", label: d.common.year, type: "select", options: YEARS.map((y) => [y, y]), value: f.year },
          { name: "currency", label: d.common.currency, type: "select", options: ["EUR", "USD", "XAF", "XDR"].map((c) => [c, c]), value: f.currency },
        ]} />
        {!tx.ok ? <ErrorState d={d} status={tx.status} message={tx.error} /> : (
          <Card>
            <Pagination d={d} base="/explorer" params={f} total={tx.data.total} limit={LIMIT} offset={offset} />
            <Table caption={d.explorer.transactions}>
              <THead><TR><TH>{d.explorer.valueDate}</TH><TH>{d.explorer.flow}</TH><TH className="text-right">{d.common.amount}</TH><TH>{d.common.project}</TH><TH>{d.explorer.agreement}</TH><TH>{d.common.partner}</TH><TH>{d.common.dataNature}</TH><TH>{d.common.source}</TH></TR></THead>
              <TBody>{tx.data.items.map((t) => (
                <TR key={`${t.flow}-${t.id}`}>
                  <TD className="whitespace-nowrap"><DateV value={t.value_date} /></TD><TD>{flowLabel(t.flow)}</TD><TD className="text-right"><Amount value={t.amount} currency={t.currency} /></TD>
                  <TD className="min-w-56"><Link className="link font-mono text-xs" href={`/projects/${t.project.ap2i_id}`}>{t.project.ap2i_id}</Link><div className="text-xs">{t.project.title}</div></TD>
                  <TD className="font-mono text-xs"><V value={t.agreement} /></TD>
                  <TD><V value={t.partner_id ? ref.partnerById.get(t.partner_id)?.short_name ?? `#${t.partner_id}` : null} /></TD>
                  <TD><NatureBadge value={t.data_nature} /></TD>
                  <TD>{t.source_record_id ? <Link className="link font-mono text-xs" href={`/sources/${t.source_record_id}`}>#{t.source_record_id}</Link> : <V value={null} />}</TD>
                </TR>))}
              </TBody>
            </Table>
            <Pagination d={d} base="/explorer" params={f} total={tx.data.total} limit={LIMIT} offset={offset} />
          </Card>
        )}
      </section>

      <section id="quality" aria-labelledby="dq-title" className="space-y-4">
        <h2 id="dq-title" className="text-lg font-semibold text-navy">{d.explorer.quality}</h2>
        {!dq.ok ? <ErrorState d={d} status={dq.status} message={dq.error} /> : (
          <>
            <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
              <Kpi label={d.common.projects} value={dq.data.projects} href="/projects" />
              <Kpi label={d.explorer.review} value={dq.data.records_requiring_review} href="/admin/review" />
              <Kpi label={d.explorer.duplicates} value={dq.data.potential_duplicates} href="/admin/matches" />
              <Kpi label={d.explorer.failedImports} value={dq.data.failed_imports} href="/admin/sync-runs" />
              <Kpi label={d.explorer.outdated} value={dq.data.outdated_observations} />
              <Kpi label={label(d.verificationStatus, "verified")} value={dq.data.verified_records} href="/projects?verification=verified" />
            </div>
            <div className="grid gap-4 lg:grid-cols-3">
              <Card>
                <CardHeader title={d.explorer.verification} />
                <CardBody><ul className="space-y-1 text-sm">{Object.entries(dq.data.verification).map(([k, v]) => <li key={k} className="flex justify-between"><Link className="link" href={`/projects?verification=${k}`}>{label(d.verificationStatus, k)}</Link><span className="tabular-nums">{v}</span></li>)}</ul></CardBody>
              </Card>
              <Card>
                <CardHeader title={d.countries.quality} />
                <CardBody><ul className="space-y-1 text-sm">{Object.entries(dq.data.average_scores).map(([k, v]) => <li key={k} className="flex justify-between"><span>{label(d.project.scores, k)}</span><Pct value={v} digits={0} /></li>)}</ul></CardBody>
              </Card>
              <Card>
                <CardHeader title={d.explorer.missingInfo} />
                <CardBody><ul className="space-y-1 text-sm">{Object.entries(dq.data.missing_information).map(([k, v]) => <li key={k} className="flex justify-between"><span>{k}</span><span className="tabular-nums">{v}</span></li>)}</ul></CardBody>
              </Card>
            </div>
            <Card>
              <CardHeader title={d.explorer.connectors} />
              <Table caption={d.explorer.connectors}>
                <THead><TR><TH>{d.common.name}</TH><TH>{d.explorer.tier}</TH><TH>{d.explorer.enabled}</TH><TH>{d.common.status}</TH><TH className="text-right">{d.explorer.records}</TH><TH>{d.explorer.lastSuccess}</TH><TH>{d.explorer.lastFailure}</TH><TH>{d.explorer.lastRun}</TH></TR></THead>
                <TBody>{dq.data.connectors.map((c) => (
                  <TR key={c.key}>
                    <TD className="min-w-56">{c.name}<div className="font-mono text-xs text-muted">{c.key}</div>{c.last_error ? <div className="text-xs text-danger break-anywhere">{d.explorer.lastError}: {c.last_error}</div> : null}</TD>
                    <TD>{c.tier}</TD><TD>{c.enabled ? d.common.yes : d.common.no}</TD>
                    <TD><Badge tone={c.status === "operational" ? "emerald" : c.status === "blocked" ? "danger" : "outline"}>{c.status}</Badge></TD>
                    <TD className="text-right"><Num value={c.records_stored} /></TD>
                    <TD className="whitespace-nowrap"><DateV value={c.last_success_at} time /></TD><TD className="whitespace-nowrap"><DateV value={c.last_failure_at} time /></TD>
                    <TD className="text-xs">{c.last_run ? <>#{c.last_run.id} {c.last_run.status} · {c.last_run.retrieved}/{c.last_run.imported}/{c.last_run.review}/{c.last_run.failed}</> : <V value={null} />}</TD>
                  </TR>))}
                </TBody>
              </Table>
              <p className="px-4 pb-3 text-xs text-muted">{d.explorer.lastRun}: {d.admin.retrieved} / {d.admin.imported} / {d.admin.reviewCount} / {d.admin.failed}</p>
            </Card>
          </>
        )}
      </section>
    </div>
  );
}
