"use client";

import Link from "next/link";
import { useState } from "react";
import { UsdCompleteBadge } from "@/components/badges";
import { Chart } from "@/components/charts/echart";
import { Select } from "@/components/ui/form";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, MoneyList, Num } from "@/components/value";
import { toNumber } from "@/lib/format";
import { useI18n } from "../i18n-provider";

export interface SlimYear {
  year: number;
  approved: number | null;
  active: number | null;
  completed: number | null;
  undated: number | null;
  commitments: { by_currency: Record<string, string>; usd: string | null; usd_complete: boolean; rate_sources: string[]; transactions: number };
  disbursements: { by_currency: Record<string, string>; usd: string | null; usd_complete: boolean; rate_sources: string[]; transactions: number };
}

export function AnnualPortfolio({ iso3, years, extraQuery = "" }: { iso3: string; years: SlimYear[]; extraQuery?: string }) {
  const { d } = useI18n();
  const cats = years.map((y) => String(y.year));
  const yearLink = (y: number) => `/projects?country=${iso3}&year_from=${y}&year_to=${y}${extraQuery}`;
  const flowLink = (y: number, flow: string) => `/explorer?country=${iso3}&flow=${flow}&year=${y}`;
  const [a, setA] = useState(String(years.at(-2)?.year ?? ""));
  const [b, setB] = useState(String(years.at(-1)?.year ?? ""));
  const ya = years.find((y) => String(y.year) === a);
  const yb = years.find((y) => String(y.year) === b);
  const diff = (x: number | string | null | undefined, y: number | string | null | undefined) => {
    const nx = toNumber(x), ny = toNumber(y);
    return nx === null || ny === null ? null : ny - nx;
  };
  const currencies = [...new Set([...(ya ? Object.keys(ya.commitments.by_currency) : []), ...(yb ? Object.keys(yb.commitments.by_currency) : []), ...(ya ? Object.keys(ya.disbursements.by_currency) : []), ...(yb ? Object.keys(yb.disbursements.by_currency) : [])])].sort();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="mb-1 text-sm font-semibold text-navy">{d.countries.annualCounts}</h3>
        <Chart ariaLabel={d.countries.annualCounts} categories={cats} links={years.map((y) => yearLink(y.year))}
          series={[
            { name: d.countries.approved, data: years.map((y) => y.approved), color: "#D9A323" },
            { name: d.countries.active, data: years.map((y) => y.active), color: "#082B50" },
            { name: d.countries.completed, data: years.map((y) => y.completed), color: "#087F5B" },
          ]} />
        <p className="text-xs text-muted">{d.common.clickToDrill}</p>
      </div>
      <div>
        <h3 className="mb-1 text-sm font-semibold text-navy">{d.countries.annualFlows}</h3>
        <Chart ariaLabel={d.countries.annualFlows} categories={cats} unit="USD"
          series={[
            { name: d.countries.commitments, data: years.map((y) => toNumber(y.commitments.usd)), color: "#082B50", links: years.map((y) => flowLink(y.year, "commitment")) },
            { name: d.countries.disbursements, data: years.map((y) => toNumber(y.disbursements.usd)), color: "#087F5B", links: years.map((y) => flowLink(y.year, "disbursement")) },
          ]} />
      </div>
      <div>
        <h3 className="mb-2 text-sm font-semibold text-navy">{d.countries.annualByCurrency}</h3>
        <Table caption={d.countries.annualByCurrency}>
          <THead>
            <TR>
              <TH>{d.common.year}</TH>
              <TH className="text-right">{d.countries.approved}</TH>
              <TH className="text-right">{d.countries.active}</TH>
              <TH className="text-right">{d.countries.completed}</TH>
              <TH>{d.countries.commitments} — {d.common.perCurrency}</TH>
              <TH className="text-right">{d.countries.commitments} ({d.common.usdEquivalent})</TH>
              <TH>{d.countries.disbursements} — {d.common.perCurrency}</TH>
              <TH className="text-right">{d.countries.disbursements} ({d.common.usdEquivalent})</TH>
            </TR>
          </THead>
          <TBody>
            {years.map((y) => (
              <TR key={y.year}>
                <TD><Link className="link" href={yearLink(y.year)}>{y.year}</Link></TD>
                <TD className="text-right"><Num value={y.approved} /></TD>
                <TD className="text-right"><Num value={y.active} /></TD>
                <TD className="text-right"><Num value={y.completed} /></TD>
                <TD><Link className="no-underline hover:underline" href={flowLink(y.year, "commitment")}><MoneyList value={y.commitments.by_currency} /></Link></TD>
                <TD className="text-right"><Amount value={y.commitments.usd} currency="USD" /><div className="mt-0.5"><UsdCompleteBadge complete={y.commitments.usd_complete} /></div></TD>
                <TD><Link className="no-underline hover:underline" href={flowLink(y.year, "disbursement")}><MoneyList value={y.disbursements.by_currency} /></Link></TD>
                <TD className="text-right"><Amount value={y.disbursements.usd} currency="USD" /><div className="mt-0.5"><UsdCompleteBadge complete={y.disbursements.usd_complete} /></div></TD>
              </TR>
            ))}
          </TBody>
        </Table>
        <p className="mt-2 text-xs text-muted">
          {d.common.method}: {[...new Set(years.flatMap((y) => [...y.commitments.rate_sources, ...y.disbursements.rate_sources]))].join(" · ") || d.common.na}
        </p>
      </div>
      <div className="rounded-lg border border-line p-3">
        <h3 className="text-sm font-semibold text-navy">{d.countries.compare}</h3>
        <div className="mt-2 grid max-w-md grid-cols-2 gap-3">
          <div>
            <label htmlFor="cmp-a" className="mb-1 block text-xs font-semibold uppercase text-muted">{d.countries.compareA}</label>
            <Select id="cmp-a" value={a} onChange={(e) => setA(e.target.value)}>{cats.map((c) => <option key={c}>{c}</option>)}</Select>
          </div>
          <div>
            <label htmlFor="cmp-b" className="mb-1 block text-xs font-semibold uppercase text-muted">{d.countries.compareB}</label>
            <Select id="cmp-b" value={b} onChange={(e) => setB(e.target.value)}>{cats.map((c) => <option key={c}>{c}</option>)}</Select>
          </div>
        </div>
        {ya && yb ? (
          <div className="mt-3">
            <Table caption={d.countries.compare}>
              <THead><TR><TH /><TH className="text-right">{a}</TH><TH className="text-right">{b}</TH><TH className="text-right">{d.countries.difference}</TH></TR></THead>
              <TBody>
                {([[d.countries.approved, ya.approved, yb.approved], [d.countries.active, ya.active, yb.active], [d.countries.completed, ya.completed, yb.completed]] as const).map(([l, x, y]) => (
                  <TR key={l}><TD>{l}</TD><TD className="text-right"><Num value={x} /></TD><TD className="text-right"><Num value={y} /></TD><TD className="text-right"><Num value={diff(x, y)} /></TD></TR>
                ))}
                {currencies.flatMap((c) => [
                  <TR key={`c-${c}`}><TD>{d.countries.commitments} ({c})</TD><TD className="text-right"><Amount value={ya.commitments.by_currency[c] ?? null} currency={c} /></TD><TD className="text-right"><Amount value={yb.commitments.by_currency[c] ?? null} currency={c} /></TD><TD className="text-right"><Amount value={diff(ya.commitments.by_currency[c], yb.commitments.by_currency[c])} currency={c} /></TD></TR>,
                  <TR key={`d-${c}`}><TD>{d.countries.disbursements} ({c})</TD><TD className="text-right"><Amount value={ya.disbursements.by_currency[c] ?? null} currency={c} /></TD><TD className="text-right"><Amount value={yb.disbursements.by_currency[c] ?? null} currency={c} /></TD><TD className="text-right"><Amount value={diff(ya.disbursements.by_currency[c], yb.disbursements.by_currency[c])} currency={c} /></TD></TR>,
                ])}
                <TR><TD>{d.countries.commitments} ({d.common.usdEquivalent})</TD><TD className="text-right"><Amount value={ya.commitments.usd} currency="USD" /></TD><TD className="text-right"><Amount value={yb.commitments.usd} currency="USD" /></TD><TD className="text-right"><Amount value={diff(ya.commitments.usd, yb.commitments.usd)} currency="USD" /></TD></TR>
                <TR><TD>{d.countries.disbursements} ({d.common.usdEquivalent})</TD><TD className="text-right"><Amount value={ya.disbursements.usd} currency="USD" /></TD><TD className="text-right"><Amount value={yb.disbursements.usd} currency="USD" /></TD><TD className="text-right"><Amount value={diff(ya.disbursements.usd, yb.disbursements.usd)} currency="USD" /></TD></TR>
              </TBody>
            </Table>
            <p className="mt-1 text-xs text-muted">{d.common.perCurrency}. {!ya.commitments.usd_complete || !yb.commitments.usd_complete || !ya.disbursements.usd_complete || !yb.disbursements.usd_complete ? d.common.usdIncomplete : d.common.usdComplete}.</p>
          </div>
        ) : null}
      </div>
    </div>
  );
}
