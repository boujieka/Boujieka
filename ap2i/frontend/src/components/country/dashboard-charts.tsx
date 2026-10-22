"use client";

import { Chart } from "@/components/charts/echart";
import { ChartLinks } from "@/components/charts/chart-links";
import { LEVEL_COLOR, LEVEL_ORDER } from "@/components/badges";
import { label } from "@/i18n";
import { fmtNumber } from "@/lib/format";
import type { Dashboard } from "@/lib/types";
import { useI18n } from "../i18n-provider";

export function StatusChart({ iso3, byStatus }: { iso3: string; byStatus: Record<string, number> }) {
  const { d, locale } = useI18n();
  const keys = Object.keys(byStatus).sort((a, b) => byStatus[b] - byStatus[a]);
  const links = keys.map((k) => `/projects?country=${iso3}&status=${k}`);
  return (
    <>
      <Chart ariaLabel={d.countries.statusMix} horizontal categories={keys.map((k) => label(d.projectStatus, k))} links={links}
        series={[{ name: d.common.projects, data: keys.map((k) => byStatus[k]), color: "#082B50" }]} />
      <ChartLinks label={d.common.clickToDrill} items={keys.map((k, i) => ({ label: label(d.projectStatus, k), href: links[i], value: fmtNumber(byStatus[k], locale) ?? "" }))} />
    </>
  );
}

export function SectorChart({ iso3, sectors }: { iso3: string; sectors: Dashboard["by_sector"] }) {
  const { d, locale } = useI18n();
  // "UNCLASSIFIED" is not a real sector code; it cannot be filtered, so it is shown without a link.
  const links = sectors.map((s) => (s.code === "UNCLASSIFIED" ? null : `/projects?country=${iso3}&sector=${s.code}`));
  const names = sectors.map((s) => (locale === "fr" ? s.name_fr : s.name_en));
  return (
    <>
      <Chart ariaLabel={d.countries.bySector} horizontal categories={names} links={links}
        series={[
          { name: d.common.projects, data: sectors.map((s) => s.projects), color: "#082B50" },
          { name: d.countries.active, data: sectors.map((s) => s.active), color: "#087F5B", links: sectors.map((s) => (s.code === "UNCLASSIFIED" ? null : `/projects?country=${iso3}&sector=${s.code}&status=active`)) },
        ]} />
      <ChartLinks label={d.common.clickToDrill} items={sectors.map((s, i) => ({ label: names[i], href: links[i], value: fmtNumber(s.projects, locale) ?? "" }))} />
    </>
  );
}

export function AlertLevelChart({ iso3, levels }: { iso3: string; levels: Record<string, number> }) {
  const { d, locale } = useI18n();
  const keys = LEVEL_ORDER.filter((k) => k in levels);
  const links = keys.map((k) => `/performance?country=${iso3}&level=${k}`);
  return (
    <>
      <Chart ariaLabel={d.countries.alertsByLevel} horizontal categories={keys.map((k) => label(d.alertLevel, k))} links={links}
        series={keys.length ? [{ name: d.performance.level, data: keys.map((k) => levels[k]), color: "#D9A323" }] : []} />
      <ul className="mt-2 flex flex-wrap gap-3 text-sm">
        {keys.map((k, i) => (
          <li key={k}><a className="link" href={links[i]}><span className="mr-1 inline-block h-2.5 w-2.5 rounded-full" style={{ background: LEVEL_COLOR[k] }} />{label(d.alertLevel, k)}: {fmtNumber(levels[k], locale)}</a></li>
        ))}
      </ul>
    </>
  );
}
