import { UploadForm } from "@/components/admin/forms";
import { PageHeader } from "@/components/page-header";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface Tpl { projects: { columns: string[]; required: string[] }; budget_lines: { columns: string[]; required: string[] }; rules: string[] }

export default async function UploadsPage() {
  const { d } = await getI18n();
  const t = await apiGet<Tpl>("/uploads/templates");
  const cols = (x: { columns: string[]; required: string[] }) => (
    <details className="mt-3 text-xs"><summary className="cursor-pointer text-navy">{d.admin.templates}</summary>
      <p className="mt-1"><span className="font-semibold">{d.admin.required}:</span> <span className="font-mono">{x.required.join(", ")}</span></p>
      <p className="mt-1 font-mono break-anywhere">{x.columns.join(", ")}</p>
    </details>
  );
  return (
    <div className="space-y-4">
      <PageHeader title={d.admin.uploads} />
      {t.ok ? <ul className="list-disc space-y-1 pl-5 text-sm">{t.data.rules.map((r) => <li key={r}>{r}</li>)}</ul> : null}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card><CardHeader title={d.admin.uploadProjects} /><CardBody><UploadForm kind="projects" />{t.ok ? cols(t.data.projects) : null}</CardBody></Card>
        <Card><CardHeader title={d.admin.uploadBudget} /><CardBody><UploadForm kind="budget-lines" />{t.ok ? cols(t.data.budget_lines) : null}</CardBody></Card>
      </div>
    </div>
  );
}
