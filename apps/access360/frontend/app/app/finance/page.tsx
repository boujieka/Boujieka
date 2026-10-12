"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { Card } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, orgPath } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { fmtMetric, label, SUMMARY_KPIS } from "@/lib/metrics";
import { useSession } from "@/lib/session";
import type { Project } from "@/lib/types";

export default function FinancePage() {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const list = useApi<Project[]>(org ? orgPath(org.id, "/projects") : null);
  const [ccy, setCcy] = useState<Record<string, string>>({});

  // the currency code lives in each project's inputs
  useEffect(() => {
    if (!org || !list.data) return;
    let alive = true;
    Promise.all(
      list.data
        .filter((p) => p.latest_run)
        .map((p) =>
          api<Project>(orgPath(org.id, `/projects/${p.id}`))
            .then((full) => [p.id, typeof full.inputs?.currency === "string" ? full.inputs.currency : "LCY"] as const)
            .catch(() => [p.id, "LCY"] as const),
        ),
    ).then((pairs) => alive && setCcy(Object.fromEntries(pairs)));
    return () => {
      alive = false;
    };
  }, [org, list.data]);

  const real = (list.data ?? []).filter((p) => !p.is_demo);
  const demo = (list.data ?? []).filter((p) => p.is_demo);

  const table = (rows: Project[], isDemo: boolean) => (
    <Card>
      <div className="flex items-center gap-2 px-4 pt-3 text-sm font-semibold text-navy-900">
        {isDemo ? t("dash.demo") : t("dash.real")} <DemoBadge show={isDemo} />
      </div>
      {rows.length === 0 ? (
        <p className="px-4 py-3 text-sm text-muted-foreground">{t("dash.noProjects")}</p>
      ) : (
        <TableWrap>
          <Table className="text-xs" data-testid={isDemo ? "finance-demo" : "finance-real"}>
            <thead>
              <tr>
                <Th>{t("common.project")}</Th>
                <Th>{t("common.status")}</Th>
                {SUMMARY_KPIS.map((m) => (
                  <Th key={m.key} className="text-right">
                    {label(m, locale)}
                  </Th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((p) => (
                <tr key={p.id}>
                  <Td>
                    <Link href={`/app/projects/${p.id}?tab=results`} className="font-medium text-navy-800 underline-offset-4 hover:underline">
                      {p.name}
                    </Link>
                    <div className="text-subtle-foreground">{p.country}</div>
                  </Td>
                  <Td>
                    <StatusBadge status={p.latest_run?.status} />
                  </Td>
                  {SUMMARY_KPIS.map((m) => (
                    <Td key={m.key} className="text-right whitespace-nowrap">
                      {p.latest_run ? fmtMetric(m.kind, p.latest_run.key[m.key as keyof typeof p.latest_run.key], ccy[p.id] ?? "LCY", locale) : "–"}
                    </Td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        </TableWrap>
      )}
    </Card>
  );

  return (
    <>
      <PageHeader title={t("fin.title")} lead={t("fin.lead")} />
      {list.loading && !list.data ? <Loading /> : null}
      {list.error ? <ErrorBox error={list.error} onRetry={list.reload} /> : null}
      {list.data ? (
        <div className="flex flex-col gap-6">
          {table(real, false)}
          {table(demo, true)}
        </div>
      ) : null}
    </>
  );
}
