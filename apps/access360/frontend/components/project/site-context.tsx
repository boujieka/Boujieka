"use client";
// Site context from PostGIS: country and admin 1 region, nearest Natural Earth places, the organisation's own layers.
// Every value comes from the API with its source and licence; null values show "Data unavailable".

import { MapPin } from "lucide-react";
import { DemoBadge } from "@/components/badges";
import { ErrorBox, Loading, Unavailable } from "@/components/page";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { orgPath } from "@/lib/api";
import { num } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Json, Project } from "@/lib/types";

const RADIUS_KM = 25;

interface CtxSource {
  dataset_id: string;
  title: string;
  source_institution: string | null;
  licence: string | null;
  quality: string | null;
  scope: "platform" | "organisation";
}
interface AdminHit {
  properties: Record<string, Json>;
  source: CtxSource;
}
interface SiteContext {
  point: { latitude: number; longitude: number } | null;
  message?: string;
  radius_km?: number;
  country?: AdminHit | null;
  admin1?: AdminHit | null;
  nearest_places?: { name: string | null; admin1: string | null; population_max_estimate: number | null; distance_km: number; source: CtxSource }[];
  places_note?: string;
  organisation_layers?: { layer_type: string; features_within_radius: number; nearest_km: number | null; source: CtxSource }[];
}

const str = (v: Json | undefined) => (typeof v === "string" && v.trim() !== "" ? v : null);

function SourceLine({ s }: { s: CtxSource }) {
  const { t } = useI18n();
  return (
    <p className="mt-0.5 text-xs text-subtle-foreground" data-testid="context-source">
      {t("ctx.source")}: {s.title}
      {s.source_institution ? ` (${s.source_institution})` : ""} · {t("ctx.licence")}: {s.licence ?? t("common.dataUnavailable")}
    </p>
  );
}

export function SiteContextCard({ project }: { project: Project }) {
  const { org } = useSession();
  const { t, locale } = useI18n();
  const hasPoint = project.latitude !== null && project.longitude !== null;
  const ctx = useApi<SiteContext>(org && hasPoint ? orgPath(org.id, `/projects/${project.id}/context?radius_km=${RADIUS_KM}`) : null);
  const c = ctx.data;

  const countryName = (h: AdminHit) => (locale === "fr" ? str(h.properties.name_fr) : null) ?? str(h.properties.name_long) ?? str(h.properties.name);
  const adminName = (h: AdminHit) => {
    const n = (locale === "fr" ? str(h.properties.name_fr) : null) ?? str(h.properties.name);
    const ty = str(h.properties.type_en);
    return n ? (ty ? `${n} (${ty})` : n) : null;
  };

  return (
    <Card className="lg:col-span-2" data-testid="site-context">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MapPin className="size-4 text-emerald-700" aria-hidden /> {t("ctx.title")}
        </CardTitle>
        <CardDescription>{t("ctx.lead", { r: num(RADIUS_KM, locale) })}</CardDescription>
      </CardHeader>
      <CardContent>
        {!hasPoint || (c && c.point === null) ? (
          <Unavailable text={t("ctx.noLocation")} />
        ) : ctx.loading && !c ? (
          <Loading />
        ) : ctx.error ? (
          <ErrorBox error={ctx.error} onRetry={ctx.reload} />
        ) : c ? (
          <div className="grid gap-6 lg:grid-cols-3">
            <section className="flex flex-col gap-3" aria-labelledby="ctx-admin">
              <h3 id="ctx-admin" className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("ctx.admin")}
              </h3>
              <div data-testid="context-country">
                <p className="text-xs text-muted-foreground">{t("common.country")}</p>
                {c.country && countryName(c.country) ? (
                  <>
                    <p className="text-sm font-medium text-navy-900">{countryName(c.country)}</p>
                    <SourceLine s={c.country.source} />
                  </>
                ) : (
                  <Unavailable />
                )}
              </div>
              <div data-testid="context-admin1">
                <p className="text-xs text-muted-foreground">{t("ctx.admin1")}</p>
                {c.admin1 && adminName(c.admin1) ? (
                  <>
                    <p className="text-sm font-medium text-navy-900">{adminName(c.admin1)}</p>
                    <SourceLine s={c.admin1.source} />
                  </>
                ) : (
                  <Unavailable />
                )}
              </div>
            </section>

            <section className="flex min-w-0 flex-col gap-2" aria-labelledby="ctx-places">
              <h3 id="ctx-places" className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("ctx.places")}
              </h3>
              {(c.nearest_places ?? []).length === 0 ? (
                <Unavailable text={t("ctx.noPlaces", { r: num(c.radius_km ?? RADIUS_KM, locale) })} />
              ) : (
                <TableWrap>
                  <Table className="text-xs" data-testid="context-places">
                    <thead>
                      <tr>
                        <Th>{t("common.name")}</Th>
                        <Th className="text-right">{t("ctx.distance")}</Th>
                        <Th className="text-right">{t("ctx.population")}</Th>
                      </tr>
                    </thead>
                    <tbody>
                      {(c.nearest_places ?? []).map((p, i) => (
                        <tr key={i}>
                          <Td>
                            {p.name ?? t("common.dataUnavailable")}
                            {p.admin1 ? <div className="text-subtle-foreground">{p.admin1}</div> : null}
                          </Td>
                          <Td className="text-right whitespace-nowrap">{num(p.distance_km, locale, 1)} km</Td>
                          <Td className="text-right whitespace-nowrap">
                            {p.population_max_estimate === null ? <span className="italic text-subtle-foreground">{t("common.dataUnavailable")}</span> : num(p.population_max_estimate, locale, 0)}
                          </Td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </TableWrap>
              )}
              {c.nearest_places?.[0] ? <SourceLine s={c.nearest_places[0].source} /> : null}
              {c.places_note ? (
                <p className="text-xs text-muted-foreground" data-testid="places-note">
                  {c.places_note}
                </p>
              ) : null}
            </section>

            <section className="flex flex-col gap-2" aria-labelledby="ctx-layers">
              <h3 id="ctx-layers" className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {t("ctx.layers")}
              </h3>
              {(c.organisation_layers ?? []).length === 0 ? (
                <Unavailable text={t("ctx.noLayers")} />
              ) : (
                <ul className="flex flex-col divide-y divide-border" data-testid="context-layers">
                  {(c.organisation_layers ?? []).map((l) => (
                    <li key={l.source.dataset_id} className="py-2">
                      <div className="flex flex-wrap items-center gap-2 text-sm font-medium text-navy-900">
                        {l.source.title}
                        <Badge variant="neutral">{l.layer_type}</Badge>
                        <DemoBadge show={l.source.quality === "synthetic_demo"} />
                      </div>
                      <p className="mt-0.5 text-xs text-foreground">
                        {t("ctx.features", { n: num(l.features_within_radius, locale) })} ·{" "}
                        {l.nearest_km === null ? t("common.dataUnavailable") : t("ctx.nearest", { d: num(l.nearest_km, locale, 1) })}
                      </p>
                      <SourceLine s={l.source} />
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
