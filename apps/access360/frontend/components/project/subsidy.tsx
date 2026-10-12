"use client";

import { useState, type FormEvent } from "react";
import { CheckCircle2, XCircle } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { Field } from "@/components/field";
import { Kpi } from "@/components/kpi";
import { ErrorBox } from "@/components/page";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api, ApiError, orgPath } from "@/lib/api";
import { money, pct, ratio } from "@/lib/format";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Project, SubsidyResult } from "@/lib/types";
import { projectCurrency } from "./results";

const toNum = (s: string) => (s.trim() === "" ? null : Number(s.replace(",", ".")));

export function SubsidyTab({ project }: { project: Project }) {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const ccy = projectCurrency(project);
  const [minDscr, setMinDscr] = useState("1.3");
  const [minIrr, setMinIrr] = useState("");
  const [maxGrant, setMaxGrant] = useState("");
  const [res, setRes] = useState<SubsidyResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const demo = project.is_demo || project.inputs?.provenance === "illustrative";

  async function solve(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    setBusy(true);
    setError(null);
    setErrors({});
    try {
      const irr = toNum(minIrr);
      setRes(
        await api<SubsidyResult>(orgPath(org.id, `/projects/${project.id}/minimum-subsidy`), {
          method: "POST",
          body: { min_dscr: toNum(minDscr), min_equity_irr: irr === null ? null : irr / 100, max_grant: toNum(maxGrant) },
        }),
      );
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
      <Card>
        <CardHeader>
          <CardTitle>{t("sub.title")}</CardTitle>
          <CardDescription>{t("sub.lead")}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={solve} className="flex flex-col gap-4">
            <Field label={t("sub.minDscr")} error={errors.min_dscr}>
              {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={minDscr} onChange={(e) => setMinDscr(e.target.value)} />}
            </Field>
            <Field label={`${t("sub.minIrr")} (${t("common.optional")})`} error={errors.min_equity_irr}>
              {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={minIrr} onChange={(e) => setMinIrr(e.target.value)} />}
            </Field>
            <Field label={`${t("sub.maxGrant", { ccy })} (${t("common.optional")})`} error={errors.max_grant}>
              {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={maxGrant} onChange={(e) => setMaxGrant(e.target.value)} />}
            </Field>
            <Button type="submit" disabled={busy || !project.has_inputs} data-testid="solve-subsidy">
              {busy ? t("common.loading") : t("sub.solve")}
            </Button>
            {!project.has_inputs ? <p className="text-sm text-muted-foreground">{t("results.noRun")}</p> : null}
          </form>
        </CardContent>
      </Card>
      <div className="flex flex-col gap-4">
        {error ? <ErrorBox error={error} /> : null}
        {res ? (
          <Card data-testid="subsidy-result">
            <CardHeader>
              <CardTitle className="flex flex-wrap items-center gap-2">
                {res.feasible ? (
                  <Badge variant="success">
                    <CheckCircle2 aria-hidden /> {t("sub.feasible")}
                  </Badge>
                ) : (
                  <Badge variant="danger">
                    <XCircle aria-hidden /> {t("sub.notFeasible")}
                  </Badge>
                )}
                <DemoBadge show={demo} />
              </CardTitle>
              <CardDescription>{res.reason}</CardDescription>
              {typeof res.monotone === "boolean" ? (
                <CardDescription>
                  {t("sub.monotone")}: {res.monotone ? t("common.yes") : t("common.no")}
                </CardDescription>
              ) : null}
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3">
                <Kpi label={t("sub.grant")} value={money(res.grant, ccy, locale)} />
                <Kpi label={t("sub.perConnection")} value={money(res.grant_per_connection, ccy, locale)} />
                <Kpi label={t("sub.dscr")} value={ratio(res.dscr_min, locale)} />
                <Kpi label={t("sub.irr")} value={pct(res.equity_irr, locale)} />
              </div>
            </CardContent>
          </Card>
        ) : null}
      </div>
    </div>
  );
}
