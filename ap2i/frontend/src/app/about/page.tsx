import Image from "next/image";
import Link from "next/link";
import type { Methodology } from "@/components/methodology";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

export const metadata = { title: "About" };

export default async function AboutPage() {
  const { d } = await getI18n();
  const m = await apiGet<Methodology>("/methodology");
  return (
    <div className="space-y-6">
      <PageHeader title={d.about.title} subtitle={d.meta.tagline} />
      <Card><CardBody className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <Image src="/ap2i-logo.png" alt="AP²I logo" width={120} height={120} className="h-24 w-24 object-contain" />
        <p className="text-sm sm:text-base">{d.about.intro}</p>
      </CardBody></Card>
      {!m.ok ? <ErrorState d={d} status={m.status} message={m.error} /> : (
        <>
          <Card>
            <CardHeader title={d.about.principles} />
            <CardBody><ul className="list-disc space-y-1 pl-5 text-sm">{m.data.data_principles.map((p) => <li key={p}>{p}</li>)}</ul></CardBody>
          </Card>
          <Alert tone="warning" title={d.about.coverage}><p>{d.coverage.text}</p><p className="mt-1 text-xs">API: “{m.data.coverage}”</p></Alert>
        </>
      )}
      <p><Link className="link" href="/methodology">{d.about.methodology} →</Link></p>
    </div>
  );
}
