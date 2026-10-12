"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { orgPath } from "@/lib/api";
import { dateTime, moneyCompact, num, pct } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Project } from "@/lib/types";

export default function ProjectsPage() {
  const { org, canEdit } = useSession();
  const { t, locale } = useI18n();
  const list = useApi<Project[]>(org ? orgPath(org.id, "/projects") : null);

  return (
    <>
      <PageHeader
        title={t("projects.title")}
        actions={
          canEdit ? (
            <Button asChild variant="accent">
              <Link href="/app/projects/new" data-testid="new-project">
                <Plus aria-hidden /> {t("projects.new")}
              </Link>
            </Button>
          ) : null
        }
      />
      {list.loading && !list.data ? <Loading /> : null}
      {list.error ? <ErrorBox error={list.error} onRetry={list.reload} /> : null}
      {list.data && list.data.length === 0 ? <p className="text-sm text-muted-foreground">{t("projects.empty")}</p> : null}
      {list.data && list.data.length > 0 ? (
        <Card>
          <TableWrap>
            <Table>
              <thead>
                <tr>
                  <Th>{t("common.name")}</Th>
                  <Th>{t("common.country")}</Th>
                  <Th>{t("common.stage")}</Th>
                  <Th>{t("projects.latestRun")}</Th>
                  <Th className="text-right">Capex</Th>
                  <Th className="text-right">{t("dash.plannedConnections")}</Th>
                  <Th className="text-right">Project IRR</Th>
                  <Th>{t("projects.updated")}</Th>
                </tr>
              </thead>
              <tbody>
                {list.data.map((p) => (
                  <tr key={p.id} className="hover:bg-surface-muted/60">
                    <Td>
                      <Link href={`/app/projects/${p.id}`} className="font-medium text-navy-800 underline-offset-4 hover:underline">
                        {p.name}
                      </Link>
                      {p.is_demo ? <DemoBadge className="ml-2" /> : null}
                    </Td>
                    <Td>{p.country}</Td>
                    <Td>{t(`stage.${p.stage}` as DictKey)}</Td>
                    <Td>
                      <StatusBadge status={p.latest_run?.status} />
                    </Td>
                    <Td className="text-right whitespace-nowrap">{p.latest_run ? moneyCompact(p.latest_run.key.capex_total_usd, "USD", locale) : "–"}</Td>
                    <Td className="text-right">{p.latest_run ? num(p.latest_run.key.connections_target, locale) : "–"}</Td>
                    <Td className="text-right">{p.latest_run ? pct(p.latest_run.key.project_irr_post_subsidy, locale) : "–"}</Td>
                    <Td className="whitespace-nowrap text-muted-foreground">{dateTime(p.updated_at, locale)}</Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </TableWrap>
        </Card>
      ) : null}
    </>
  );
}
