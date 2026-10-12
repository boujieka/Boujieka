"use client";

import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { Field } from "@/components/field";
import { PageHeader } from "@/components/page";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { api, ApiError, orgPath } from "@/lib/api";
import { STAGES } from "@/lib/constants";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Country, Project } from "@/lib/types";

const MapView = dynamic(() => import("@/components/map-view").then((m) => m.MapView), { ssr: false });

export default function NewProjectPage() {
  const { org, canEdit } = useSession();
  const { t } = useI18n();
  const router = useRouter();
  const countries = useApi<Country[]>("/api/countries");
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const [stage, setStage] = useState<string>("screening");
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const latN = lat.trim() === "" ? null : Number(lat);
  const lonN = lon.trim() === "" ? null : Number(lon);
  const picked = latN !== null && lonN !== null && Number.isFinite(latN) && Number.isFinite(lonN) ? { lat: latN, lon: lonN } : null;

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    setBusy(true);
    setError(null);
    setErrors({});
    try {
      const p = await api<Project>(orgPath(org.id, "/projects"), {
        method: "POST",
        body: { name, country, stage, technology: "solar_battery_minigrid", latitude: latN, longitude: lonN },
      });
      router.push(`/app/projects/${p.id}`);
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <PageHeader title={t("projects.createTitle")} />
      {!canEdit ? <Alert variant="warning">{t("common.notAllowed")}</Alert> : null}
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)]">
        <Card>
          <CardContent className="pt-5">
            <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
              <Field label={t("common.name")} error={errors.name}>
                {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} required maxLength={200} value={name} onChange={(e) => setName(e.target.value)} />}
              </Field>
              <Field label={t("common.country")} error={errors.country}>
                {(id, d, inv) => (
                  <Select id={id} aria-describedby={d} aria-invalid={inv} required value={country} onChange={(e) => setCountry(e.target.value)}>
                    <option value="">{t("projects.selectCountry")}</option>
                    {(countries.data ?? []).map((c) => (
                      <option key={c.iso3} value={c.name}>
                        {c.name}
                      </option>
                    ))}
                  </Select>
                )}
              </Field>
              <Field label={t("common.stage")} error={errors.stage}>
                {(id, d) => (
                  <Select id={id} aria-describedby={d} value={stage} onChange={(e) => setStage(e.target.value)}>
                    {STAGES.map((s) => (
                      <option key={s} value={s}>
                        {t(`stage.${s}` as DictKey)}
                      </option>
                    ))}
                  </Select>
                )}
              </Field>
              <div className="grid grid-cols-2 gap-3">
                <Field label={`${t("projects.latitude")} (${t("common.optional")})`} error={errors.latitude}>
                  {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="-1.2345" />}
                </Field>
                <Field label={`${t("projects.longitude")} (${t("common.optional")})`} error={errors.longitude}>
                  {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} inputMode="decimal" value={lon} onChange={(e) => setLon(e.target.value)} placeholder="36.789" />}
                </Field>
              </div>
              {error ? <Alert variant="danger">{error}</Alert> : null}
              <Button type="submit" disabled={busy || !canEdit || !name || !country} data-testid="create-project">
                {busy ? t("common.saving") : t("common.create")}
              </Button>
            </form>
          </CardContent>
        </Card>
        <div className="flex flex-col gap-2">
          <p className="text-xs text-muted-foreground">{t("projects.pickOnMap")}</p>
          <MapView
            height={380}
            picked={picked}
            onPick={(p) => {
              setLat(String(p.lat));
              setLon(String(p.lon));
            }}
          />
        </div>
      </div>
    </>
  );
}
