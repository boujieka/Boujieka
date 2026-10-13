"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { Field } from "@/components/field";
import { Kpi } from "@/components/kpi";
import { SiteContextCard } from "@/components/project/site-context";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { api, ApiError, orgPath } from "@/lib/api";
import { STAGES } from "@/lib/constants";
import { dateTime } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { fmtMetric, label, SUMMARY_KPIS } from "@/lib/metrics";
import { useSession } from "@/lib/session";
import type { Country, Project } from "@/lib/types";

export function OverviewTab({ project, onChanged }: { project: Project; onChanged: () => void }) {
  const { org, canEdit, isAdmin } = useSession();
  const { t, locale } = useI18n();
  const router = useRouter();
  const countries = useApi<Country[]>("/api/countries");
  const [f, setF] = useState({
    name: project.name,
    country: project.country,
    stage: project.stage,
    latitude: project.latitude === null ? "" : String(project.latitude),
    longitude: project.longitude === null ? "" : String(project.longitude),
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [msg, setMsg] = useState<{ kind: "success" | "danger"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const ccy = typeof project.inputs?.currency === "string" ? project.inputs.currency : "LCY";
  const run = project.latest_run;
  const countryOptions = [...new Set([project.country, ...(countries.data ?? []).map((c) => c.name)])];

  async function save(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    setBusy(true);
    setMsg(null);
    setErrors({});
    try {
      await api(orgPath(org.id, `/projects/${project.id}`), {
        method: "PUT",
        body: {
          name: f.name,
          country: f.country,
          stage: f.stage,
          technology: project.technology,
          latitude: f.latitude.trim() === "" ? null : Number(f.latitude),
          longitude: f.longitude.trim() === "" ? null : Number(f.longitude),
          geometry: project.geometry ?? null,
        },
      });
      setMsg({ kind: "success", text: t("common.saved") });
      onChanged();
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!org || !window.confirm(t("projects.deleteConfirm"))) return;
    try {
      await api(orgPath(org.id, `/projects/${project.id}`), { method: "DELETE" });
      router.push("/app/projects");
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>{t("overview.fields")}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={save} className="flex flex-col gap-4">
            <Field label={t("common.name")} error={errors.name}>
              {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} value={f.name} disabled={!canEdit} onChange={(e) => setF({ ...f, name: e.target.value })} />}
            </Field>
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label={t("common.country")} error={errors.country}>
                {(id, d) => (
                  <Select id={id} aria-describedby={d} value={f.country} disabled={!canEdit} onChange={(e) => setF({ ...f, country: e.target.value })}>
                    {countryOptions.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </Select>
                )}
              </Field>
              <Field label={t("common.stage")} error={errors.stage}>
                {(id, d) => (
                  <Select id={id} aria-describedby={d} value={f.stage} disabled={!canEdit} onChange={(e) => setF({ ...f, stage: e.target.value })}>
                    {STAGES.map((s) => (
                      <option key={s} value={s}>
                        {t(`stage.${s}` as DictKey)}
                      </option>
                    ))}
                  </Select>
                )}
              </Field>
              <Field label={t("projects.latitude")} error={errors.latitude}>
                {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={f.latitude} disabled={!canEdit} onChange={(e) => setF({ ...f, latitude: e.target.value })} />}
              </Field>
              <Field label={t("projects.longitude")} error={errors.longitude}>
                {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={f.longitude} disabled={!canEdit} onChange={(e) => setF({ ...f, longitude: e.target.value })} />}
              </Field>
            </div>
            {msg ? <Alert variant={msg.kind}>{msg.text}</Alert> : null}
            <div className="flex flex-wrap justify-between gap-2">
              <Button type="submit" disabled={!canEdit || busy}>
                {busy ? t("common.saving") : t("common.save")}
              </Button>
              {isAdmin ? (
                <Button type="button" variant="outline" className="text-danger-700" onClick={remove}>
                  {t("projects.delete")}
                </Button>
              ) : null}
            </div>
          </form>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="flex flex-wrap items-center gap-2">
            {t("overview.latestRun")} <StatusBadge status={run?.status} /> <DemoBadge show={!!run?.is_demo} />
          </CardTitle>
          {run ? (
            <p className="text-xs text-subtle-foreground">
              {dateTime(run.created_at, locale)} · {t("results.engine")} {run.engine_version}
            </p>
          ) : null}
        </CardHeader>
        <CardContent>
          {!run ? (
            <p className="text-sm text-muted-foreground">{t("overview.noRun")}</p>
          ) : (
            <div className="flex flex-col gap-3">
              {run.inputs_version !== project.inputs_version ? <Alert variant="warning">{t("overview.inputsChanged")}</Alert> : null}
              <div className="grid grid-cols-2 gap-3">
                {SUMMARY_KPIS.map((m) => (
                  <Kpi key={m.key} label={label(m, locale)} value={fmtMetric(m.kind, run.key[m.key as keyof typeof run.key], ccy, locale)} />
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
      <SiteContextCard key={`${project.latitude},${project.longitude}`} project={project} />
    </div>
  );
}
