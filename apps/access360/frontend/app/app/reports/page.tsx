"use client";

import { useMemo } from "react";
import { DocumentsTable } from "@/components/documents-table";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { Card, CardContent } from "@/components/ui/card";
import { orgPath } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { DocumentRow, Project } from "@/lib/types";

export default function ReportsPage() {
  const { org } = useSession();
  const { t } = useI18n();
  const docs = useApi<DocumentRow[]>(org ? orgPath(org.id, "/documents") : null);
  const projects = useApi<Project[]>(org ? orgPath(org.id, "/projects") : null);
  const names = useMemo(() => Object.fromEntries((projects.data ?? []).map((p) => [p.id, { name: p.name, is_demo: p.is_demo }])), [projects.data]);
  if (!org) return null;
  return (
    <>
      <PageHeader title={t("reports.title")} lead={t("reports.lead")} />
      <Card>
        <CardContent className="pt-4">
          {docs.loading && !docs.data ? <Loading /> : null}
          {docs.error ? <ErrorBox error={docs.error} onRetry={docs.reload} /> : null}
          {docs.data ? <DocumentsTable docs={docs.data} orgId={org.id} projects={names} /> : null}
        </CardContent>
      </Card>
    </>
  );
}
