"use client";

import dynamic from "next/dynamic";
import { useMemo, useState, type FormEvent } from "react";
import { BarChart3, Layers, Upload } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { Field } from "@/components/field";
import { ErrorBox, Loading, PageHeader, Unavailable } from "@/components/page";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select, Textarea } from "@/components/ui/input";
import { api, ApiError, orgPath } from "@/lib/api";
import { date, DASH } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Country, CountryProfile, DatasetDetail, DatasetMeta, GeoJSONFeatureCollection, Project } from "@/lib/types";
import { AFRICA_BOUNDS, type MapLayer, type MapProject } from "@/components/map-view";

const MapView = dynamic(() => import("@/components/map-view").then((m) => m.MapView), { ssr: false, loading: () => <div className="h-[520px] rounded-lg border border-border bg-[#e9edf2]" data-testid="map-container" /> });

// fixed categorical order; colour follows the dataset's position in the list, never its visibility
const LAYER_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"];
const LAYER_TYPES = ["boundaries", "settlements", "grid", "substations", "health", "schools", "markets", "anchors", "minigrids", "constraints", "other"];
const QUALITY = ["verified_source", "secondary", "user_assumption", "synthetic_demo"];
const META_KEYS = ["title", "layer_type", "source_institution", "publication_date", "geographic_coverage", "resolution", "licence", "retrieval_date", "quality", "limitations"] as const;
type MetaKey = (typeof META_KEYS)[number];

function MetaList({ d }: { d: DatasetMeta }) {
  const { t, locale } = useI18n();
  const rows: [DictKey, string][] = [
    ["exp2.meta.source_institution", d.source_institution],
    ["exp2.meta.publication_date", d.publication_date],
    ["exp2.meta.geographic_coverage", d.geographic_coverage],
    ["exp2.meta.resolution", d.resolution],
    ["exp2.meta.licence", d.licence],
    ["exp2.meta.retrieval_date", date(d.retrieval_date, locale)],
    ["exp2.meta.quality", d.quality.replace(/_/g, " ")],
    ["exp2.meta.limitations", d.limitations],
  ];
  if (d.source_version) rows.push(["exp2.meta.source_version", d.source_version]);
  if (d.source_url) rows.push(["exp2.meta.source_url", d.source_url]);
  if (d.attribution) rows.push(["exp2.meta.attribution", d.attribution]);
  return (
    <dl className="mt-2 grid grid-cols-[auto_1fr] gap-x-3 gap-y-1 text-xs">
      {rows.map(([k, v]) => (
        <div key={k} className="contents">
          <dt className="text-subtle-foreground">{t(k)}</dt>
          <dd className="break-words text-foreground">{v || t("common.dataUnavailable")}</dd>
        </div>
      ))}
    </dl>
  );
}

function UploadPanel({ onDone }: { onDone: () => void }) {
  const { org, canEdit } = useSession();
  const { t } = useI18n();
  const [format, setFormat] = useState<"geojson" | "csv">("geojson");
  const [file, setFile] = useState<File | null>(null);
  const [meta, setMeta] = useState<Record<MetaKey, string>>({
    title: "",
    layer_type: "settlements",
    source_institution: "",
    publication_date: "",
    geographic_coverage: "",
    resolution: "",
    licence: "",
    retrieval_date: new Date().toISOString().slice(0, 10),
    quality: "secondary",
    limitations: "",
  });
  const [msg, setMsg] = useState<{ kind: "success" | "danger"; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    const missing = META_KEYS.filter((k) => !meta[k].trim());
    if (missing.length || !file) {
      setErrors(Object.fromEntries(missing.map((k) => [k, t("exp2.metaRequired")])));
      setMsg({ kind: "danger", text: t("exp2.metaRequired") });
      return;
    }
    setBusy(true);
    setMsg(null);
    setErrors({});
    try {
      if (format === "geojson") {
        let geojson: unknown;
        try {
          geojson = JSON.parse(await file.text());
        } catch {
          throw new Error("The file is not valid JSON");
        }
        await api(orgPath(org.id, "/datasets"), { method: "POST", body: { ...meta, geojson } });
      } else {
        const fd = new FormData();
        fd.append("meta", JSON.stringify(meta));
        fd.append("file", file);
        await api(orgPath(org.id, "/datasets/csv"), { method: "POST", form: fd });
      }
      setMsg({ kind: "success", text: t("exp2.uploaded") });
      onDone();
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    } finally {
      setBusy(false);
    }
  }

  const text = (k: MetaKey, type = "text") => (
    <Field key={k} label={t(`exp2.meta.${k}` as DictKey)} error={errors[k]}>
      {(id, d, inv) => <Input id={id} type={type} aria-describedby={d} aria-invalid={inv} required value={meta[k]} onChange={(e) => setMeta({ ...meta, [k]: e.target.value })} />}
    </Field>
  );

  return (
    <form onSubmit={submit} className="flex flex-col gap-3">
      {!canEdit ? <Alert variant="warning">{t("common.notAllowed")}</Alert> : null}
      <div className="grid grid-cols-2 gap-3">
        <Field label={t("exp2.format")}>
          {(id) => (
            <Select id={id} value={format} onChange={(e) => setFormat(e.target.value as "geojson" | "csv")}>
              <option value="geojson">GeoJSON</option>
              <option value="csv">CSV</option>
            </Select>
          )}
        </Field>
        <Field label={t("exp2.meta.layer_type")} error={errors.layer_type}>
          {(id) => (
            <Select id={id} value={meta.layer_type} onChange={(e) => setMeta({ ...meta, layer_type: e.target.value })}>
              {LAYER_TYPES.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </Select>
          )}
        </Field>
      </div>
      <Field label={t("exp2.file")} hint={format === "csv" ? t("exp2.csvHint") : undefined}>
        {(id, d) => (
          <input
            id={id}
            aria-describedby={d}
            type="file"
            accept={format === "csv" ? ".csv,text/csv" : ".geojson,.json,application/geo+json,application/json"}
            className="text-xs file:mr-3 file:rounded-md file:border file:border-border-strong file:bg-surface file:px-3 file:py-1.5 file:text-xs"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        )}
      </Field>
      {text("title")}
      {text("source_institution")}
      <div className="grid grid-cols-2 gap-3">
        {text("publication_date")}
        {text("retrieval_date", "date")}
      </div>
      {text("geographic_coverage")}
      <div className="grid grid-cols-2 gap-3">
        {text("resolution")}
        {text("licence")}
      </div>
      <Field label={t("exp2.meta.quality")} error={errors.quality}>
        {(id) => (
          <Select id={id} value={meta.quality} onChange={(e) => setMeta({ ...meta, quality: e.target.value })}>
            {QUALITY.map((q) => (
              <option key={q} value={q}>
                {q.replace(/_/g, " ")}
              </option>
            ))}
          </Select>
        )}
      </Field>
      <Field label={t("exp2.meta.limitations")} error={errors.limitations}>
        {(id, d, inv) => <Textarea id={id} aria-describedby={d} aria-invalid={inv} required value={meta.limitations} onChange={(e) => setMeta({ ...meta, limitations: e.target.value })} />}
      </Field>
      {msg ? <Alert variant={msg.kind}>{msg.text}</Alert> : null}
      <Button type="submit" disabled={!canEdit || busy}>
        <Upload aria-hidden /> {busy ? t("common.saving") : t("exp2.upload")}
      </Button>
    </form>
  );
}

type CountryFc = GeoJSONFeatureCollection & { dataset?: DatasetMeta };

// reference layer colours (fixed, distinct from the dataset palette order)
const ADMIN0_COLOR = "#0b1f3a";
const ADMIN1_COLOR = "#2a78d6";
const PLACES_COLOR = "#e34948";

function indicatorValue(v: number | null, locale: string): string {
  if (v === null || !Number.isFinite(v)) return DASH;
  return new Intl.NumberFormat(locale === "fr" ? "fr-FR" : "en-US", { maximumFractionDigits: 3 }).format(v);
}

function ProfilePanel({ iso3 }: { iso3: string }) {
  const { t, locale } = useI18n();
  const profile = useApi<CountryProfile>(`/api/countries/${iso3}/profile`);
  const p = profile.data && profile.data.iso3 === iso3 ? profile.data : null;
  return (
    <Card data-testid="country-profile">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="size-4 text-emerald-700" aria-hidden /> {t("exp2.profile.title")}
          {p ? <span className="font-normal text-muted-foreground">: {p.name}</span> : null}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {profile.loading && !p ? <Loading /> : null}
        {profile.error ? <Unavailable text={t("exp2.profile.none")} /> : null}
        {p ? (
          <>
            <p className="text-xs text-muted-foreground">{t("exp2.profile.note")}</p>
            <ul className="grid gap-3 md:grid-cols-2" data-testid="profile-indicators">
              {p.indicators.map((i) => (
                <li key={i.key} className="rounded-md border border-border p-3" data-testid={`indicator-${i.key}`}>
                  <div className="text-sm font-medium">{i.title}</div>
                  <div className="mt-1 flex flex-wrap items-baseline gap-x-2">
                    {i.value === null ? (
                      <Unavailable />
                    ) : (
                      <>
                        <span className="text-xl font-semibold tabular-nums" title={String(i.value)} data-testid="indicator-value">
                          {indicatorValue(i.value, locale)}
                        </span>
                        <span className="text-sm text-muted-foreground">{i.unit}</span>
                      </>
                    )}
                  </div>
                  <dl className="mt-2 grid grid-cols-[auto_1fr] gap-x-3 gap-y-0.5 text-xs">
                    <dt className="text-subtle-foreground">{t("exp2.profile.year")}</dt>
                    <dd data-testid="indicator-year">{i.year ?? t("common.dataUnavailable")}</dd>
                    <dt className="text-subtle-foreground">{t("exp2.profile.unit")}</dt>
                    <dd>{i.unit || DASH}</dd>
                    <dt className="text-subtle-foreground">{t("exp2.profile.source")}</dt>
                    <dd className="break-words">{i.source}</dd>
                    <dt className="text-subtle-foreground">{t("exp2.profile.licence")}</dt>
                    <dd className="break-words">{i.licence}</dd>
                  </dl>
                  <Badge variant="neutral" className="mt-2">
                    {i.quality.replace(/_/g, " ")}
                  </Badge>
                </li>
              ))}
            </ul>
            <div>
              <div className="text-sm font-medium">{t("exp2.profile.sources")}</div>
              <ul className="mt-2 flex flex-col gap-2 text-xs" data-testid="profile-sources">
                {p.sources.map((s) => (
                  <li key={s.key} className="rounded-md border border-border p-2">
                    <div className="font-medium">{s.title}</div>
                    <div className="text-muted-foreground">
                      {s.source_institution}
                      {s.version ? ` · ${s.version}` : ""}
                    </div>
                    <div>
                      <span className="text-subtle-foreground">{t("exp2.profile.licence")}: </span>
                      {s.licence}
                    </div>
                    <div>
                      <span className="text-subtle-foreground">{t("exp2.profile.attribution")}: </span>
                      {s.attribution}
                    </div>
                    {s.urls.map((u) => (
                      <div key={u} className="break-all text-subtle-foreground">
                        {u}
                      </div>
                    ))}
                  </li>
                ))}
              </ul>
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}

export default function ExplorePage() {
  const { org } = useSession();
  const { t } = useI18n();
  const countries = useApi<Country[]>("/api/countries");
  const projects = useApi<Project[]>(org ? orgPath(org.id, "/projects") : null);
  const datasets = useApi<DatasetMeta[]>(org ? orgPath(org.id, "/datasets") : null);
  const [country, setCountry] = useState("");
  const [visible, setVisible] = useState<Record<string, DatasetDetail>>({});
  const [loadingLayer, setLoadingLayer] = useState<string | null>(null);
  const [layerError, setLayerError] = useState<string | null>(null);

  const allCountries = useMemo(() => {
    const names = new Set((countries.data ?? []).map((c) => c.name));
    for (const p of projects.data ?? []) names.add(p.country);
    return [...names].sort((a, b) => a.localeCompare(b));
  }, [countries.data, projects.data]);

  const selected = useMemo(() => (countries.data ?? []).find((c) => c.name === country) ?? null, [countries.data, country]);
  const iso = selected?.has_profile ? selected.iso3 : null;
  const boundary = useApi<CountryFc>(iso ? `/api/countries/${iso}/boundary` : null);
  const admin1 = useApi<CountryFc>(iso ? `/api/countries/${iso}/admin1` : null);
  const places = useApi<CountryFc>(iso ? `/api/countries/${iso}/places` : null);
  const ofCountry = (fc: CountryFc | null) => (fc && iso && fc.features.length && fc.features.every((f) => f.properties?.iso3 === iso) ? fc : null);
  const admin1Fc = ofCountry(admin1.data);
  const boundaryFc = ofCountry(boundary.data);
  const placesFc = ofCountry(places.data);

  const mapProjects: MapProject[] = useMemo(
    () =>
      (projects.data ?? [])
        .filter((p) => typeof p.latitude === "number" && typeof p.longitude === "number" && (!country || p.country === country))
        .map((p) => ({ id: p.id, name: p.name, lat: p.latitude as number, lon: p.longitude as number, is_demo: p.is_demo })),
    [projects.data, country],
  );

  const fit = useMemo<[[number, number], [number, number]] | null>(() => {
    if (!country) return AFRICA_BOUNDS;
    if (selected?.bbox) {
      const [w, s, e, n] = selected.bbox;
      return [
        [w, s],
        [e, n],
      ];
    }
    if (!mapProjects.length) return null;
    const lons = mapProjects.map((p) => p.lon);
    const lats = mapProjects.map((p) => p.lat);
    const pad = 0.25;
    return [
      [Math.min(...lons) - pad, Math.min(...lats) - pad],
      [Math.max(...lons) + pad, Math.max(...lats) + pad],
    ];
  }, [country, selected, mapProjects]);

  const colorOf = (id: string) => LAYER_COLORS[Math.max(0, (datasets.data ?? []).findIndex((d) => d.id === id)) % LAYER_COLORS.length];
  const layers: MapLayer[] = useMemo(() => {
    const out: MapLayer[] = [];
    if (admin1Fc && iso) out.push({ id: `ref-admin1-${iso}`, color: ADMIN1_COLOR, geojson: admin1Fc, fillOpacity: 0.06, lineWidth: 1 });
    if (boundaryFc && iso) out.push({ id: `ref-admin0-${iso}`, color: ADMIN0_COLOR, geojson: boundaryFc, fillOpacity: 0, lineWidth: 2.5 });
    if (placesFc && iso) out.push({ id: `ref-places-${iso}`, color: PLACES_COLOR, geojson: placesFc, pointRadius: 3.5 });
    for (const d of Object.values(visible)) out.push({ id: d.id, color: colorOf(d.id), geojson: d.geojson, fillOpacity: d.layer_type === "boundaries" ? 0.06 : undefined, lineWidth: d.layer_type === "boundaries" ? 1 : undefined });
    return out;
  }, [visible, datasets.data, admin1Fc, boundaryFc, placesFc, iso]); // eslint-disable-line react-hooks/exhaustive-deps

  async function toggle(d: DatasetMeta, on: boolean) {
    if (!org) return;
    if (!on) {
      setVisible((v) => {
        const n = { ...v };
        delete n[d.id];
        return n;
      });
      return;
    }
    setLoadingLayer(d.id);
    setLayerError(null);
    try {
      const full = await api<DatasetDetail>(orgPath(org.id, `/datasets/${d.id}`));
      setVisible((v) => ({ ...v, [d.id]: full }));
    } catch (e) {
      setLayerError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoadingLayer(null);
    }
  }

  const anyDemo = (projects.data ?? []).some((p) => p.is_demo) || (datasets.data ?? []).some((d) => d.is_demo);
  const platformSets = (datasets.data ?? []).filter((d) => d.scope === "platform");
  const ownSets = (datasets.data ?? []).filter((d) => d.scope !== "platform");

  const datasetItem = (d: DatasetMeta) => (
    <li key={d.id} className="rounded-md border border-border p-3" data-testid={`dataset-${d.source_key ?? d.id}`}>
      <label className="flex items-start gap-2 text-sm font-medium">
        <input type="checkbox" className="mt-0.5 size-4 accent-emerald-600" checked={!!visible[d.id]} disabled={loadingLayer === d.id} onChange={(e) => toggle(d, e.target.checked)} />
        <span className="mt-1 inline-block size-2.5 shrink-0 rounded-full" style={{ background: colorOf(d.id) }} aria-hidden />
        <span className="min-w-0 break-words">{d.title}</span>
      </label>
      <div className="mt-1.5 flex flex-wrap gap-1">
        <Badge variant="navy">{d.layer_type}</Badge>
        <Badge variant="neutral">
          {d.feature_count} {t("exp2.features")}
        </Badge>
        <Badge variant="neutral">{d.scope}</Badge>
        <DemoBadge show={d.is_demo || d.quality === "synthetic_demo"} />
      </div>
      <details className="mt-1">
        <summary className="cursor-pointer text-xs text-muted-foreground">{t("exp2.meta.source_institution")}: {d.source_institution}</summary>
        <MetaList d={d} />
      </details>
    </li>
  );

  return (
    <>
      <PageHeader title={t("exp2.title")} badges={<DemoBadge show={anyDemo} />} />
      <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_360px]">
        <div className="flex min-w-0 flex-col gap-3">
          <div className="flex flex-wrap items-end gap-3">
            <Field label={t("exp2.country")} className="w-full sm:w-72">
              {(id) => (
                <Select id={id} value={country} onChange={(e) => setCountry(e.target.value)} data-testid="country-select">
                  <option value="">{t("exp2.allAfrica")}</option>
                  {allCountries.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </Select>
              )}
            </Field>
            {country && !mapProjects.length ? <p className="pb-2 text-sm text-muted-foreground">{t("exp2.noProjectsCountry")}</p> : null}
          </div>
          <MapView projects={mapProjects} layers={layers} fit={fit} height={560} />
          <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <span className="inline-block size-3 rounded-full border-2 border-gold-500 bg-navy-900" aria-hidden /> {t("exp2.projects")} ({mapProjects.length})
            </span>
            {admin1Fc ? (
              <span className="flex items-center gap-1.5">
                <span className="inline-block size-3 rounded-sm border-2" style={{ borderColor: ADMIN1_COLOR }} aria-hidden /> {t("exp2.admin1")} ({admin1Fc.features.length})
              </span>
            ) : null}
            {placesFc ? (
              <span className="flex items-center gap-1.5">
                <span className="inline-block size-3 rounded-full" style={{ background: PLACES_COLOR }} aria-hidden /> {t("exp2.settlements")} ({placesFc.features.length})
              </span>
            ) : null}
            {Object.values(visible).map((d) => (
              <span key={d.id} className="flex items-center gap-1.5">
                <span className="inline-block size-3 rounded-full" style={{ background: colorOf(d.id) }} aria-hidden /> {d.title}
              </span>
            ))}
          </div>
          {iso ? <ProfilePanel iso3={iso} /> : null}
        </div>

        <aside className="flex flex-col gap-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Layers className="size-4 text-emerald-700" aria-hidden /> {t("exp2.layers")}
              </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <div className="rounded-md border border-dashed border-border-strong p-3 text-sm" data-testid="boundary-status">
                <div className="font-medium">{t("exp2.boundaries")}</div>
                {!country ? <p className="mt-1 text-xs text-muted-foreground">{t("exp2.selectCountry")}</p> : null}
                {country ? (
                  <dl className="mt-1 flex flex-col gap-0.5 text-xs">
                    <dt className="mt-1 text-subtle-foreground">{t("exp2.admin1")}</dt>
                    <dd data-testid="admin1-status">
                      {admin1Fc ? `${admin1Fc.features.length} ${t("exp2.admin1Count")}` : admin1.loading ? <Loading /> : <Unavailable text={t("exp2.boundariesNa")} />}
                    </dd>
                    <dt className="mt-1 text-subtle-foreground">{t("exp2.districts")}</dt>
                    <dd>
                      <Unavailable text={t("exp2.districtsNa")} />
                    </dd>
                    <dt className="mt-1 text-subtle-foreground">{t("exp2.settlements")}</dt>
                    <dd>{placesFc ? `${placesFc.features.length} ${t("exp2.placesCount")}` : places.loading ? <Loading /> : <Unavailable text={t("exp2.settlementsNa")} />}</dd>
                  </dl>
                ) : null}
                {admin1Fc && admin1.data?.dataset ? (
                  <p className="mt-2 text-xs text-muted-foreground">
                    {t("exp2.boundarySource")}: {admin1.data.dataset.source_institution}, {admin1.data.dataset.publication_date}. {admin1.data.dataset.licence}
                  </p>
                ) : null}
              </div>
              {datasets.loading && !datasets.data ? <Loading /> : null}
              {datasets.error ? <ErrorBox error={datasets.error} onRetry={datasets.reload} /> : null}
              {layerError ? <ErrorBox error={layerError} /> : null}
              {platformSets.length ? (
                <>
                  <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("exp2.platformLayers")}</div>
                  <ul className="flex flex-col gap-3" data-testid="platform-dataset-list">
                    {platformSets.map(datasetItem)}
                  </ul>
                </>
              ) : null}
              <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("exp2.yourLayers")}</div>
              {datasets.data && ownSets.length === 0 ? <p className="text-sm text-muted-foreground">{t("exp2.noDatasets")}</p> : null}
              <ul className="flex flex-col gap-3" data-testid="dataset-list">
                {ownSets.map(datasetItem)}
              </ul>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="size-4 text-emerald-700" aria-hidden /> {t("exp2.upload")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <UploadPanel onDone={datasets.reload} />
            </CardContent>
          </Card>
        </aside>
      </div>
    </>
  );
}
