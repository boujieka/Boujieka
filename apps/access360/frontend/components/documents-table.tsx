"use client";

import { DemoBadge } from "@/components/badges";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { orgPath } from "@/lib/api";
import { dateTime } from "@/lib/format";
import { useI18n } from "@/lib/i18n";
import type { DocumentRow } from "@/lib/types";

const KIND: Record<string, [string, string]> = {
  model_xlsx: ["Excel model", "Modèle Excel"],
  teaser_pdf: ["One page teaser (PDF)", "Fiche d'une page (PDF)"],
  summary_pdf: ["Project summary (PDF)", "Synthèse du projet (PDF)"],
};

const FILE: Record<string, string> = { model_xlsx: "export.xlsx", teaser_pdf: "teaser.pdf", summary_pdf: "summary.pdf" };

export function DocumentsTable({ docs, orgId, projects }: { docs: DocumentRow[]; orgId: string; projects?: Record<string, { name: string; is_demo: boolean }> }) {
  const { t, locale } = useI18n();
  if (!docs.length) return <p className="text-sm text-muted-foreground">{t("exp.empty")}</p>;
  return (
    <TableWrap>
      <Table data-testid="documents-table">
        <thead>
          <tr>
            <Th>{t("common.date")}</Th>
            <Th>{t("exp.kind")}</Th>
            {projects ? <Th>{t("common.project")}</Th> : null}
            <Th>{t("results.engine")}</Th>
            <Th>{t("results.inputsHash")}</Th>
            <Th>
              <span className="sr-only">{t("common.download")}</span>
            </Th>
          </tr>
        </thead>
        <tbody>
          {docs.map((d) => {
            const ext = FILE[d.kind] ?? "teaser.pdf";
            const p = projects?.[d.project_id];
            return (
              <tr key={d.id}>
                <Td className="whitespace-nowrap">{dateTime(d.created_at, locale)}</Td>
                <Td>{KIND[d.kind]?.[locale === "fr" ? 1 : 0] ?? d.kind}</Td>
                {projects ? (
                  <Td>
                    {p ? p.name : d.project_id.slice(0, 8)}
                    {p?.is_demo ? <DemoBadge className="ml-2" /> : null}
                  </Td>
                ) : null}
                <Td>{d.engine_version}</Td>
                <Td>
                  <span className="font-mono text-xs" title={d.inputs_sha256}>
                    {d.inputs_sha256.slice(0, 16)}…
                  </span>
                </Td>
                <Td>
                  <a className="text-sm font-medium text-navy-700 underline-offset-4 hover:underline" href={orgPath(orgId, `/projects/${d.project_id}/runs/${d.run_id}/${ext}`)} download>
                    {t("common.download")}
                  </a>
                </Td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </TableWrap>
  );
}
