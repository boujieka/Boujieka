import Link from "next/link";
import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";
import type { Dashboard, Sector } from "@/lib/types";

export const metadata = { title: "Sectors" };

export default async function SectorsPage() {
  const { d, locale } = await getI18n();
  const [sectors, dash] = await Promise.all([apiGet<Sector[]>("/sectors"), apiGet<Dashboard>("/countries/CMR/dashboard")]);
  const counts = new Map(dash.ok ? dash.data.by_sector.map((s) => [s.code, s]) : []);
  return (
    <div>
      <PageHeader title={d.sectors.title} subtitle={d.sectors.subtitle} />
      <CoverageNotice d={d} className="mb-4" />
      {!sectors.ok ? <ErrorState d={d} status={sectors.status} message={sectors.error} /> : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sectors.data.map((s) => {
            const c = counts.get(s.code);
            return (
              <Card key={s.code}>
                <CardHeader as="h2" title={<Link className="hover:underline" href={`/sectors/${s.code}`}>{locale === "fr" ? s.name_fr : s.name_en}</Link>} description={<span className="font-mono text-xs">{s.code}</span>} />
                <CardBody className="text-sm">
                  <p>{d.common.projects} (CMR): {c ? <Link className="link" href={`/projects?country=CMR&sector=${s.code}`}>{c.projects}</Link> : <span className="italic text-muted">{d.common.na}</span>}</p>
                  <p className="mt-2 text-xs text-muted">{d.sectors.indicators}:</p>
                  <ul className="mt-1 flex flex-wrap gap-1">{s.indicators.map((i) => <li key={i.code}><Badge tone="outline">{locale === "fr" ? i.name_fr : i.name_en}</Badge></li>)}</ul>
                </CardBody>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
