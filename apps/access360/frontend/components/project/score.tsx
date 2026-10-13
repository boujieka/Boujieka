"use client";

import { useCallback, useEffect, useState, type FormEvent } from "react";
import { Info, Loader2, Lock } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { Field } from "@/components/field";
import { ErrorBox, Loading } from "@/components/page";
import { DecisionBadge, GateOverrideNote, GateStateBadge, ScoreBreakdown, SourcesList } from "@/components/score";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { api, ApiError, orgPath } from "@/lib/api";
import { num } from "@/lib/format";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import { USER_GATES, type GateState, type Json, type Project, type ScoreResult, type UserGate } from "@/lib/types";

type Tri = "unknown" | "yes" | "no";

/** The project GET does not return the stored gates or score context, so the form is seeded from the score response. */
function seedFrom(s: ScoreResult) {
  const gates = Object.fromEntries(USER_GATES.map((g) => [g, s.gates.find((x) => x.gate === g)?.state ?? "unknown"])) as Record<UserGate, GateState>;
  const speed = s.parts.find((p) => p.criterion === "speed");
  const months = s.sources.months_to_power === "user estimate" && typeof speed?.raw === "number" ? String(speed.raw) : "";
  const eq = s.parts.find((p) => p.criterion === "equity")?.raw;
  const u = eq && typeof eq === "object" && !Array.isArray(eq) ? (eq as Record<string, Json>).underserved_area : null;
  const underserved: Tri = u === true ? "yes" : u === false ? "no" : "unknown";
  return { gates, months, underserved };
}

export function ScoreTab({ project }: { project: Project }) {
  const { org, canEdit } = useSession();
  const { t, locale } = useI18n();
  const [score, setScore] = useState<ScoreResult | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [gates, setGates] = useState<Record<UserGate, GateState> | null>(null);
  const [months, setMonths] = useState("");
  const [underserved, setUnderserved] = useState<Tri>("unknown");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saved, setSaved] = useState(false);

  const load = useCallback(
    async (seed: boolean) => {
      if (!org) return;
      try {
        const s = await api<ScoreResult>(orgPath(org.id, `/projects/${project.id}/score`), { method: "POST", body: {} });
        setScore(s);
        setLoadError(null);
        if (seed) {
          const f = seedFrom(s);
          setGates(f.gates);
          setMonths(f.months);
          setUnderserved(f.underserved);
        }
      } catch (e) {
        setLoadError(e instanceof Error ? e.message : String(e));
      }
    },
    [org, project.id],
  );

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetch lifecycle
    load(true);
  }, [load]);

  async function save(e: FormEvent) {
    e.preventDefault();
    if (!org || !gates) return;
    setBusy(true);
    setError(null);
    setErrors({});
    setSaved(false);
    try {
      const m = months.trim() === "" ? null : Number(months.replace(",", "."));
      await api(orgPath(org.id, `/projects/${project.id}/gates`), {
        method: "PUT",
        body: { gates, months_to_power: m, underserved_area: underserved === "unknown" ? null : underserved === "yes" },
      });
      await load(false);
      setSaved(true);
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  if (loadError && !score) return <ErrorBox error={loadError} onRetry={() => load(true)} />;
  if (!score || !gates) return <Loading />;
  const modelGate = score.gates.find((g) => g.gate === "model_checks");

  return (
    <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)]">
      <Card>
        <CardHeader>
          <CardTitle>{t("score.gatesTitle")}</CardTitle>
          <CardDescription>{t("score.gatesLead")}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={save} className="flex flex-col gap-4" data-testid="gates-form" noValidate>
            {USER_GATES.map((g) => (
              <Field key={g} label={t(`score.gate.${g}` as DictKey)} error={errors[`gates.${g}`]}>
                {(id, d, inv) => (
                  <Select
                    id={id}
                    aria-describedby={d}
                    aria-invalid={inv}
                    data-testid={`gate-select-${g}`}
                    value={gates[g]}
                    disabled={!canEdit}
                    onChange={(e) => setGates({ ...gates, [g]: e.target.value as GateState })}
                  >
                    {(["unknown", "met", "not_met"] as const).map((s) => (
                      <option key={s} value={s}>
                        {t(`score.state.${s}` as DictKey)}
                      </option>
                    ))}
                  </Select>
                )}
              </Field>
            ))}
            <div className="rounded-md border border-dashed border-border-strong bg-surface-muted/60 px-3 py-2" data-testid="model-gate">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-medium text-muted-foreground">{t("score.gate.model_checks")}</span>
                <span className="flex items-center gap-2">
                  <Badge variant="neutral">
                    <Lock aria-hidden /> {t("score.readOnly")}
                  </Badge>
                  {modelGate ? <GateStateBadge state={modelGate.state} /> : null}
                </span>
              </div>
              <p className="mt-1 text-xs text-subtle-foreground">{score.sources.model_checks ?? t("common.dataUnavailable")}</p>
            </div>

            <div className="border-t border-border pt-4">
              <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("score.context")}</p>
              <div className="grid gap-4 sm:grid-cols-2">
                <Field label={t("score.monthsToPower")} hint={t("score.monthsHint")} error={errors.months_to_power}>
                  {(id, d, inv) => (
                    <Input
                      id={id}
                      aria-describedby={d}
                      aria-invalid={inv}
                      inputMode="decimal"
                      data-testid="months-to-power"
                      value={months}
                      disabled={!canEdit}
                      onChange={(e) => setMonths(e.target.value)}
                    />
                  )}
                </Field>
                <Field label={t("score.underserved")} hint={t("score.underservedHint")} error={errors.underserved_area}>
                  {(id, d, inv) => (
                    <Select id={id} aria-describedby={d} aria-invalid={inv} data-testid="underserved" value={underserved} disabled={!canEdit} onChange={(e) => setUnderserved(e.target.value as Tri)}>
                      <option value="unknown">{t("score.state.unknown")}</option>
                      <option value="yes">{t("common.yes")}</option>
                      <option value="no">{t("common.no")}</option>
                    </Select>
                  )}
                </Field>
              </div>
            </div>
            {error ? <Alert variant="danger">{error}</Alert> : null}
            {saved ? (
              <Alert variant="success" data-testid="gates-saved">
                {t("score.saved")}
              </Alert>
            ) : null}
            {!canEdit ? <p className="text-xs text-muted-foreground">{t("common.notAllowed")}</p> : null}
            <div>
              <Button type="submit" disabled={!canEdit || busy} data-testid="save-gates">
                {busy ? <Loader2 className="animate-spin" aria-hidden /> : null}
                {t("score.save")}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <div className="flex flex-col gap-6">
        <Card data-testid="score-card">
          <CardHeader>
            <div className="flex flex-wrap items-center gap-2">
              <CardTitle>{t("score.title")}</CardTitle>
              <DemoBadge show={score.is_demo} />
            </div>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-wrap items-end gap-x-6 gap-y-3">
              <div>
                <span className={score.decision === "excluded" ? "text-4xl font-semibold tabular text-subtle-foreground line-through" : "text-4xl font-semibold tabular text-navy-900"} data-testid="score-value">
                  {num(score.score, locale, 1)}
                </span>
                <span className="ml-1 text-sm text-muted-foreground">{t("score.outOf")}</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-xs text-muted-foreground">{t("score.decision")}</span>
                <span className="flex flex-wrap items-center gap-2">
                  <DecisionBadge decision={score.decision} />
                  {score.decision === "excluded" ? <GateOverrideNote /> : null}
                </span>
              </div>
            </div>
            <p className="text-sm text-foreground" data-testid="decision-explanation">
              {score.decision_explanation}
            </p>
            {score.score_is_partial ? (
              <Alert variant="warning" data-testid="score-partial">
                <Info aria-hidden />
                <span>
                  {t("score.partial", { n: score.missing_criteria.length })} {t("score.missing")}:{" "}
                  {score.missing_criteria.map((c) => `${t(`score.crit.${c}` as DictKey)} (${t("common.dataUnavailable")})`).join("; ")}
                </span>
              </Alert>
            ) : null}
            <div className="border-t border-border pt-4">
              <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("score.breakdown")}</h3>
              <ScoreBreakdown parts={score.parts} />
            </div>
            <p className="text-xs text-subtle-foreground">{t("score.gateRule")}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{t("score.sources")}</CardTitle>
            <CardDescription>{t("score.serverText")}</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <SourcesList sources={score.sources} />
            <Alert variant="info" data-testid="weights-note">
              <Info aria-hidden />
              <span>{t("score.assumptionsNote")}</span>
            </Alert>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
