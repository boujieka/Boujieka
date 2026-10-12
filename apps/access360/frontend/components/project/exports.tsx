"use client";

import { FileSpreadsheet, FileText } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { DocumentsTable } from "@/components/documents-table";
import { ErrorBox, Loading } from "@/components/page";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { orgPath } from "@/lib/api";
import { dateTime } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { DocumentRow, Project } from "@/lib/types";

export function ExportsTab({ project }: { project: Project }) {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const docs = useApi<DocumentRow[]>(org ? orgPath(org.id, "/documents") : null);
  const run = project.latest_run;
  if (!org) return null;
  const base = run ? orgPath(org.id, `/projects/${project.id}/runs/${run.id}`) : null;
  // the backend records each download as a generated document; refresh the list shortly after
  const refreshSoon = () => window.setTimeout(docs.reload, 1500);

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex flex-wrap items-center gap-2">
            {t("exp.title")} {run ? <StatusBadge status={run.status} /> : null} <DemoBadge show={!!run?.is_demo} />
          </CardTitle>
          {run ? (
            <CardDescription>
              {dateTime(run.created_at, locale)} · {t("results.engine")} {run.engine_version}
            </CardDescription>
          ) : null}
        </CardHeader>
        <CardContent>
          {!base ? (
            <p className="text-sm text-muted-foreground">{t("exp.noRun")}</p>
          ) : (
            <div className="flex flex-col gap-3">
              <div className="flex flex-wrap gap-3">
                <Button asChild variant="outline">
                  <a href={`${base}/export.xlsx`} download onClick={refreshSoon} data-testid="download-xlsx">
                    <FileSpreadsheet aria-hidden /> {t("exp.xlsx")}
                  </a>
                </Button>
                <Button asChild variant="outline">
                  <a href={`${base}/teaser.pdf`} download onClick={refreshSoon} data-testid="download-teaser">
                    <FileText aria-hidden /> {t("exp.teaser")}
                  </a>
                </Button>
              </div>
              {run?.is_demo ? <p className="text-xs text-gold-700">{t("exp.demoNote")}</p> : null}
            </div>
          )}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>{t("exp.documents")}</CardTitle>
        </CardHeader>
        <CardContent>
          {docs.loading && !docs.data ? <Loading /> : null}
          {docs.error ? <ErrorBox error={docs.error} onRetry={docs.reload} /> : null}
          {docs.data ? <DocumentsTable docs={docs.data.filter((d) => d.project_id === project.id)} orgId={org.id} /> : null}
        </CardContent>
      </Card>
    </div>
  );
}
