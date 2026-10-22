"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Amount, DateV, MoneyList, Num } from "@/components/value";
import type { OverviewCountry } from "@/lib/types";
import { useI18n } from "../i18n-provider";

/** Figures for one country exactly as /africa/overview returns them (null → Not available). */
export function CountryFigures({ c }: { c: OverviewCountry }) {
  const { d, locale } = useI18n();
  const name = locale === "fr" ? c.name_fr : c.name_en;
  const rows: [string, React.ReactNode][] = [
    [d.africa.documented, <Num key="a" value={c.documented_projects} />],
    [d.africa.commitmentsUsd, <span key="b"><Amount value={c.commitments_usd} currency="USD" />{c.commitments_usd_note ? <span className="block text-xs text-muted">{c.commitments_usd_note}</span> : null}</span>],
    [d.africa.commitmentsByCurrency, <MoneyList key="c" value={c.commitments_by_currency} />],
    [d.africa.disbursementsByCurrency, <MoneyList key="d" value={c.disbursements_by_currency ?? null} />],
    [d.africa.underImplementation, <Num key="e" value={c.under_implementation} />],
    [d.africa.completed, <Num key="f" value={c.completed} />],
    [d.africa.operational, <span key="g"><Num value={c.operational} />{c.operational_unknown ? <span className="block text-xs text-muted">{d.africa.operationalUnknown}: {c.operational_unknown}</span> : null}</span>],
    [d.africa.attention, <Num key="h" value={c.requiring_attention} />],
    [d.africa.coverage, <span key="i">{c.data_coverage}</span>],
    [d.africa.lastUpdate, <DateV key="j" value={c.last_update} time />],
  ];
  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        <h3 className="text-lg font-semibold text-navy">{name}</h3>
        <Badge tone={c.has_data ? "emerald" : "outline"}>{c.has_data ? c.iso3 : d.africa.noDataState}</Badge>
      </div>
      <dl className="mt-2 divide-y divide-line text-sm">
        {rows.map(([k, v]) => (
          <div key={k} className="grid grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)] gap-2 py-1.5">
            <dt className="text-muted">{k}</dt>
            <dd className="min-w-0 break-anywhere">{v}</dd>
          </div>
        ))}
      </dl>
      <Link href={`/countries/${c.iso3}`} className="link mt-2 inline-block text-sm">{d.africa.openCountry} →</Link>
    </div>
  );
}
