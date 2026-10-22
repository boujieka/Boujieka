import Link from "next/link";
import { CoverageNotice } from "@/components/coverage";
import { FilterBar, one, type SP } from "@/components/filter-bar";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, MoneyList, Num } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { qs } from "@/lib/utils";

interface Fin {
  country: string;
  by_instrument: { instrument: string; agreements: number; committed_by_currency: Record<string, string> }[];
  totals_by_currency: Record<string, { committed: string; disbursed: string; undisbursed: string; agreements_with_disbursement: number; agreements: number }>;
  distinctions: Record<string, string>;
  note: string;
}
interface Rate { base_currency: string; quote_currency: string; rate: string; period: string; period_type: string; source: string; source_url: string | null; retrieved_at: string | null }

export const metadata = { title: "Financing" };

export default async function FinancingPage({ searchParams }: { searchParams: SP }) {
  const { d } = await getI18n();
  const sp = await searchParams;
  const currency = one(sp.currency);
  const [fin, rates] = await Promise.all([apiGet<Fin>("/financing/summary?country=CMR"), apiGet<Rate[]>(`/exchange-rates${qs({ currency })}`)]);
  const allCurrencies = fin.ok ? Object.keys(fin.data.totals_by_currency).sort() : [];
  return (
    <div className="space-y-6">
      <PageHeader title={d.financing.title} subtitle={d.financing.subtitle} eyebrow="CMR" />
      <CoverageNotice d={d} />
      {!fin.ok ? <ErrorState d={d} status={fin.status} message={fin.error} /> : (
        <>
          <Card>
            <CardHeader title={d.financing.totals} description={fin.data.note} />
            <Table caption={d.financing.totals}>
              <THead><TR><TH>{d.common.currency}</TH><TH className="text-right">{d.financing.committed}</TH><TH className="text-right">{d.financing.disbursed}</TH><TH className="text-right">{d.financing.undisbursed}</TH><TH className="text-right">{d.financing.agreements}</TH><TH className="text-right">{d.financing.withDisbursement}</TH></TR></THead>
              <TBody>{Object.entries(fin.data.totals_by_currency).sort().map(([cur, t]) => (
                <TR key={cur}><TD className="font-semibold"><Link className="link" href={`/explorer?country=${fin.data.country}&currency=${cur}&flow=commitment`}>{cur}</Link></TD>
                  <TD className="text-right"><Amount value={t.committed} currency={cur} /></TD><TD className="text-right"><Link className="hover:underline" href={`/explorer?country=${fin.data.country}&currency=${cur}&flow=disbursement`}><Amount value={t.disbursed} currency={cur} /></Link></TD>
                  <TD className="text-right"><Amount value={t.undisbursed} currency={cur} /></TD><TD className="text-right"><Num value={t.agreements} /></TD><TD className="text-right"><Num value={t.agreements_with_disbursement} /></TD></TR>))}
              </TBody>
            </Table>
          </Card>
          <Card>
            <CardHeader title={d.financing.byInstrument} />
            <Table caption={d.financing.byInstrument}>
              <THead><TR><TH>{d.common.instrument}</TH><TH className="text-right">{d.financing.agreements}</TH><TH>{d.financing.committed} — {d.common.perCurrency}</TH></TR></THead>
              <TBody>{fin.data.by_instrument.map((i) => (
                <TR key={i.instrument}><TD>{i.instrument}</TD><TD className="text-right"><Num value={i.agreements} /></TD><TD><MoneyList value={i.committed_by_currency} /></TD></TR>))}
              </TBody>
            </Table>
          </Card>
          <Card>
            <CardHeader title={d.financing.distinctions} />
            <CardBody><dl className="grid gap-2 text-sm sm:grid-cols-[200px_1fr]">{Object.entries(fin.data.distinctions).map(([k, v]) => <div key={k} className="contents"><dt className="font-semibold">{k.replace(/_/g, " ")}</dt><dd>{v}</dd></div>)}</dl></CardBody>
          </Card>
        </>
      )}
      <Card>
        <CardHeader title={d.financing.rates} description={d.financing.ratesSubtitle} />
        <CardBody>
          <FilterBar d={d} action="/financing" fields={[{ name: "currency", label: d.financing.filterCurrency, type: "select", options: [...new Set([...allCurrencies, "USD", "XAF"])].sort().map((c) => [c, c]), value: currency }]} />
          {!rates.ok ? <ErrorState d={d} status={rates.status} message={rates.error} /> : (
            <Table caption={d.financing.rates}>
              <THead><TR><TH>{d.financing.base}</TH><TH>{d.financing.quote}</TH><TH className="text-right">{d.financing.rate}</TH><TH>{d.financing.period}</TH><TH>{d.financing.periodType}</TH><TH>{d.common.source}</TH><TH>{d.project.retrieved}</TH></TR></THead>
              <TBody>{rates.data.map((r, i) => (
                <TR key={i}><TD>{r.base_currency}</TD><TD>{r.quote_currency}</TD><TD className="text-right"><Num value={r.rate} digits={6} /></TD><TD>{r.period}</TD><TD>{r.period_type}</TD>
                  <TD className="min-w-56 text-xs">{r.source_url ? <a className="link" href={r.source_url} target="_blank" rel="noopener noreferrer">{r.source}</a> : r.source}</TD><TD className="whitespace-nowrap"><DateV value={r.retrieved_at} /></TD></TR>))}
              </TBody>
            </Table>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
