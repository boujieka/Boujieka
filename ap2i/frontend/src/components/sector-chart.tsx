"use client";

import { Chart } from "@/components/charts/echart";
import { toNumber } from "@/lib/format";
import { useI18n } from "./i18n-provider";

export function SectorAnnualChart({ code, country, annual }: { code: string; country: string; annual: { year: number; approved: number | null; active: number | null; commitments_usd: string | null; disbursements_usd: string | null; usd_complete: boolean }[] }) {
  const { d } = useI18n();
  const cats = annual.map((a) => String(a.year));
  const links = annual.map((a) => `/projects?country=${country}&sector=${code}&year_from=${a.year}&year_to=${a.year}`);
  return (
    <div className="space-y-4">
      <Chart ariaLabel={d.countries.annualCounts} categories={cats} links={links} series={[
        { name: d.countries.approved, data: annual.map((a) => a.approved), color: "#D9A323" },
        { name: d.countries.active, data: annual.map((a) => a.active), color: "#082B50" },
      ]} />
      <Chart ariaLabel={d.sectors.annual} categories={cats} unit="USD" links={links} series={[
        { name: d.countries.commitments, data: annual.map((a) => toNumber(a.commitments_usd)), color: "#082B50" },
        { name: d.countries.disbursements, data: annual.map((a) => toNumber(a.disbursements_usd)), color: "#087F5B" },
      ]} />
    </div>
  );
}
