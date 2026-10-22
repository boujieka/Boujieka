import { MethodologySections, type Methodology } from "@/components/methodology";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

export const metadata = { title: "Methodology" };

export default async function MethodologyPage() {
  const { d } = await getI18n();
  const m = await apiGet<Methodology>("/methodology");
  return (
    <div className="space-y-6">
      <PageHeader title={d.about.methodology} subtitle={d.about.principles} />
      {!m.ok ? <ErrorState d={d} status={m.status} message={m.error} /> : (
        <>
          <ul className="list-disc space-y-1 pl-5 text-sm">{m.data.data_principles.map((p) => <li key={p}>{p}</li>)}</ul>
          <Alert tone="warning" title={d.about.coverage}>{m.data.coverage}</Alert>
          <MethodologySections d={d} m={m.data} />
        </>
      )}
    </div>
  );
}
