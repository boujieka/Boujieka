import Image from "next/image";
import Link from "next/link";
import { CoverageNotice } from "@/components/coverage";
import { Kpi } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { buttonClass } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import { fmtNumber } from "@/lib/format";
import type { Country, DataQuality } from "@/lib/types";

export default async function HomePage() {
  const { d, locale } = await getI18n();
  const [countries, dq, alerts] = await Promise.all([
    apiGet<Country[]>("/countries"),
    apiGet<DataQuality>("/data-quality"),
    apiGet<{ total: number; summary_by_level: Record<string, number> }>("/alerts?limit=1"),
  ]);
  const projects = countries.ok ? countries.data.reduce((s, c) => s + (c.documented_projects ?? 0), 0) : null;
  const withData = countries.ok ? countries.data.filter((c) => c.documented_projects > 0).length : null;
  const connectors = dq.ok ? dq.data.connectors.filter((c) => c.enabled && c.status === "operational") : null;
  const pillars = [
    { t: d.home.pillar1, x: d.home.pillar1Text, href: "/countries/CMR" },
    { t: d.home.pillar2, x: d.home.pillar2Text, href: "/performance" },
    { t: d.home.pillar3, x: d.home.pillar3Text, href: "/rescue" },
  ];
  const n = (v: number | null) => (v === null ? d.common.na : fmtNumber(v, locale));
  return (
    <div className="space-y-8">
      <section className="overflow-hidden rounded-xl bg-navy text-white shadow">
        <div className="grid items-center gap-6 p-6 sm:p-10 md:grid-cols-[auto_1fr]">
          <Image src="/ap2i-logo.png" alt="AP²I logo" width={160} height={160} className="h-28 w-28 rounded-lg bg-white object-contain p-1 sm:h-40 sm:w-40" priority />
          <div className="min-w-0">
            <p className="text-sm font-semibold uppercase tracking-widest text-gold">AP²I — {d.meta.name}</p>
            <h1 className="mt-2 text-2xl font-bold sm:text-4xl">{d.meta.tagline}</h1>
            <p className="mt-3 max-w-2xl text-white/85">{d.home.heroText}</p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link href="/africa" className={buttonClass("secondary")}>{d.home.exploreMap}</Link>
              <Link href="/countries/CMR" className={buttonClass("outline")}>{d.home.exploreCameroon}</Link>
            </div>
          </div>
        </div>
      </section>

      <CoverageNotice d={d} />

      <section aria-labelledby="kpi-title">
        <h2 id="kpi-title" className="mb-3 text-lg font-semibold text-navy">{d.home.kpiTitle}</h2>
        {!countries.ok ? <ErrorState d={d} status={countries.status} message={countries.error} /> : null}
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
          <Kpi label={d.home.kpiProjects} value={n(projects)} href="/projects" />
          <Kpi label={d.home.kpiConnectors} value={n(connectors ? connectors.length : null)} href="/explorer#quality" />
          <Kpi label={d.home.kpiCountries} value={n(countries.ok ? countries.data.length : null)} href="/countries" />
          <Kpi label={d.home.kpiCountriesWithData} value={n(withData)} href="/africa" />
          <Kpi label={d.home.kpiAlerts} value={n(alerts.ok ? alerts.data.total : null)} href="/performance" />
        </div>
        {connectors && connectors.length ? (
          <div className="mt-3 flex flex-wrap items-center gap-2 text-sm">
            <span className="text-muted">{d.home.sourcesTitle}:</span>
            {connectors.map((c) => <Badge key={c.key} tone="navy">{c.name}</Badge>)}
          </div>
        ) : null}
      </section>

      <section aria-labelledby="pillars-title">
        <h2 id="pillars-title" className="mb-3 text-lg font-semibold text-navy">{d.home.pillarsTitle}</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {pillars.map((p, i) => (
            <Card key={p.t} className="border-t-4" style={{ borderTopColor: ["#082B50", "#087F5B", "#D9A323"][i] }}>
              <CardHeader title={p.t} as="h3" />
              <CardBody>
                <p className="text-sm text-ink">{p.x}</p>
                <Link href={p.href} className="link mt-3 inline-block text-sm">{d.common.open} →</Link>
              </CardBody>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}
