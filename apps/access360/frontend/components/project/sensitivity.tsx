"use client";

import { useState } from "react";
import { CheckCircle2, Loader2, XCircle } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { ChartFrame, TornadoChart, type TornadoDatum } from "@/components/charts";
import { ErrorBox } from "@/components/page";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, orgPath } from "@/lib/api";
import { money, pct, ratio } from "@/lib/format";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Project, Sensitivity } from "@/lib/types";
import { projectCurrency } from "./results";

const human = (s: string) => s.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());

export function SensitivityTab({ project }: { project: Project }) {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const [data, setData] = useState<Sensitivity | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const ccy = projectCurrency(project);
  const demo = project.is_demo || project.inputs?.provenance === "illustrative";

  async function run() {
    if (!org) return;
    setBusy(true);
    setError(null);
    try {
      setData(await api<Sensitivity>(orgPath(org.id, `/projects/${project.id}/sensitivity`), { method: "POST" }));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  const base = data?.tornado_npv.find((r) => typeof r.base === "number")?.base ?? null;
  const tornado: TornadoDatum[] =
    data && base !== null
      ? data.tornado_npv
          .filter((r) => typeof r.low === "number" && typeof r.high === "number")
          .map((r) => {
            const lo = Math.min(r.low as number, r.high as number);
            const hi = Math.max(r.low as number, r.high as number);
            return { label: human(r.group), base, low: r.low, high: r.high, down: lo < base ? ([lo, base] as [number, number]) : null, up: hi > base ? ([base, hi] as [number, number]) : null };
          })
      : [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={run} disabled={busy || !project.has_inputs} data-testid="run-sensitivity">
          {busy ? <Loader2 className="animate-spin" aria-hidden /> : null}
          {t("sens.run")}
        </Button>
        <DemoBadge show={demo} />
        {!project.has_inputs ? <span className="text-sm text-muted-foreground">{t("results.noRun")}</span> : null}
      </div>
      {error ? <ErrorBox error={error} /> : null}
      {data ? (
        <>
          <p className="text-xs text-subtle-foreground">{data.note}</p>
          {tornado.length ? (
            <ChartFrame title={t("sens.tornado")} subtitle={ccy} height={Math.max(220, tornado.length * 30 + 70)} testId="tornado">
              <TornadoChart data={tornado} base={base as number} locale={locale} valueFormat={(v) => money(v, ccy, locale)} downName={t("sens.low")} upName={t("sens.high")} baseName={`${t("sens.base")} ${money(base, ccy, locale)}`} />
            </ChartFrame>
          ) : null}
          <Card>
            <CardHeader>
              <CardTitle>{t("tab.sensitivity")}</CardTitle>
            </CardHeader>
            <CardContent>
              <TableWrap>
                <Table className="text-xs" data-testid="sensitivity-table">
                  <thead>
                    <tr>
                      <Th>{t("sens.group")}</Th>
                      <Th>{t("sens.case")}</Th>
                      <Th>{t("sens.checks")}</Th>
                      <Th className="text-right">Project IRR</Th>
                      <Th className="text-right">Equity IRR</Th>
                      <Th className="text-right">NPV ({ccy})</Th>
                      <Th className="text-right">Min DSCR</Th>
                      <Th className="text-right">LCOE ({ccy}/kWh)</Th>
                      <Th className="text-right">Equity support ({ccy})</Th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.rows.map((r, i) => (
                      <tr key={`${r.group}-${i}`} className={r.group === "base" ? "bg-navy-50 font-medium" : undefined}>
                        <Td>{human(r.group)}</Td>
                        <Td>{r.case}</Td>
                        <Td>
                          {r.checks_passed ? (
                            <span className="inline-flex items-center gap-1 text-emerald-700">
                              <CheckCircle2 className="size-3.5" aria-hidden /> {t("common.yes")}
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 text-danger-700">
                              <XCircle className="size-3.5" aria-hidden /> {t("common.no")}
                            </span>
                          )}
                        </Td>
                        <Td className="text-right">{pct(r.project_irr_post_subsidy, locale)}</Td>
                        <Td className="text-right">{pct(r.equity_irr, locale)}</Td>
                        <Td className="text-right whitespace-nowrap">{money(r.project_npv_post_subsidy, ccy, locale).replace(` ${ccy}`, "")}</Td>
                        <Td className="text-right">{ratio(r.dscr_min, locale)}</Td>
                        <Td className="text-right">{money(r.lcoe_per_kwh_sold, ccy, locale, 2).replace(` ${ccy}`, "")}</Td>
                        <Td className="text-right whitespace-nowrap">{money(r.equity_support_total, ccy, locale).replace(` ${ccy}`, "")}</Td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </TableWrap>
            </CardContent>
          </Card>
        </>
      ) : null}
    </div>
  );
}
