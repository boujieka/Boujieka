"use client";

import "maplibre-gl/dist/maplibre-gl.css";
import type { FeatureCollection, Geometry } from "geojson";
import type { Map as MlMap, MapGeoJSONFeature } from "maplibre-gl";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Select } from "@/components/ui/form";
import type { OverviewCountry } from "@/lib/types";
import { useI18n } from "../i18n-provider";
import { CountryFigures } from "./country-figures";

const NO_DATA = "#c9cfd6";
// Sequential scale (light → dark emerald) on documented project counts.
const STEPS: [number, string][] = [[1, "#b7e0d0"], [25, "#6fbf9f"], [100, "#2f9e76"], [250, "#087F5B"]];

function colorFor(c: OverviewCountry | undefined): string {
  if (!c || !c.has_data || c.documented_projects === null) return NO_DATA;
  let col = STEPS[0][1];
  for (const [min, color] of STEPS) if (c.documented_projects >= min) col = color;
  return col;
}

interface Props { countries: OverviewCountry[] }

export function AfricaMap({ countries }: Props) {
  const { d, locale } = useI18n();
  const router = useRouter();
  const ref = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MlMap | null>(null);
  const [failed, setFailed] = useState(false);
  const byIso3 = useMemo(() => new Map(countries.map((c) => [c.iso3, c])), [countries]);
  const [selected, setSelected] = useState<string>(() => (byIso3.has("CMR") ? "CMR" : countries[0]?.iso3 ?? ""));
  const [islands, setIslands] = useState<string[]>([]);
  const dataRef = useRef(byIso3);
  dataRef.current = byIso3;

  useEffect(() => {
    let cancelled = false;
    let map: MlMap | null = null;
    (async () => {
      try {
        const [{ default: maplibregl }, geo] = await Promise.all([
          import("maplibre-gl"),
          fetch("/africa.geojson").then((r) => r.json() as Promise<FeatureCollection<Geometry, Record<string, string>>>),
        ]);
        if (cancelled || !ref.current) return;
        setIslands(geo.features.filter((f) => f.properties.geometry_kind === "marker").map((f) => f.properties.iso3));
        map = new maplibregl.Map({
          container: ref.current,
          style: { version: 8, sources: {}, layers: [{ id: "bg", type: "background", paint: { "background-color": "#e9f0f6" } }] },
          bounds: [[-26, -36], [64, 38]],
          fitBoundsOptions: { padding: 10 },
          attributionControl: false,
          dragRotate: false,
          pitchWithRotate: false,
          renderWorldCopies: false,
        });
        mapRef.current = map;
        map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
        map.touchZoomRotate.disableRotation();
        map.on("load", () => {
          if (!map) return;
          map.addSource("africa", { type: "geojson", data: geo, promoteId: "iso3" });
          map.addLayer({ id: "fill", type: "fill", source: "africa", filter: ["==", ["geometry-type"], "Polygon"], paint: { "fill-color": "#ccc", "fill-opacity": 0.95 } });
          map.addLayer({ id: "fill-multi", type: "fill", source: "africa", filter: ["==", ["geometry-type"], "MultiPolygon"], paint: { "fill-color": "#ccc", "fill-opacity": 0.95 } });
          map.addLayer({ id: "line", type: "line", source: "africa", filter: ["!=", ["geometry-type"], "Point"], paint: { "line-color": "#ffffff", "line-width": ["case", ["boolean", ["feature-state", "selected"], false], 3, 0.8] } });
          map.addLayer({ id: "outline-sel", type: "line", source: "africa", filter: ["!=", ["geometry-type"], "Point"], paint: { "line-color": "#D9A323", "line-width": 2.5, "line-opacity": ["case", ["boolean", ["feature-state", "selected"], false], 1, 0] } });
          map.addLayer({ id: "islands", type: "circle", source: "africa", filter: ["==", ["geometry-type"], "Point"], paint: { "circle-radius": 7, "circle-color": "#ccc", "circle-stroke-color": ["case", ["boolean", ["feature-state", "selected"], false], "#D9A323", "#082B50"], "circle-stroke-width": 1.5 } });
          paint();
          const layers = ["fill", "fill-multi", "islands"];
          const pick = (f: MapGeoJSONFeature | undefined) => (f?.properties?.iso3 as string | undefined) ?? undefined;
          for (const id of layers) {
            map.on("mousemove", id, (e) => {
              const iso = pick(e.features?.[0]);
              if (iso) setSelected(iso);
              map!.getCanvas().style.cursor = "pointer";
            });
            map.on("mouseleave", id, () => (map!.getCanvas().style.cursor = ""));
            map.on("click", id, (e) => {
              const iso = pick(e.features?.[0]);
              if (iso) router.push(`/countries/${iso}`);
            });
          }
        });
      } catch {
        if (!cancelled) setFailed(true);
      }
    })();
    function paint() {
      if (!map) return;
      const expr: unknown[] = ["match", ["get", "iso3"]];
      for (const [iso, c] of dataRef.current) expr.push(iso, colorFor(c));
      expr.push(NO_DATA);
      for (const l of ["fill", "fill-multi"]) map.setPaintProperty(l, "fill-color", expr as never);
      map.setPaintProperty("islands", "circle-color", expr as never);
    }
    return () => {
      cancelled = true;
      map?.remove();
      mapRef.current = null;
    };
  }, [router]);

  // Repaint when filters change the data.
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded() || !map.getLayer("fill")) return;
    const expr: unknown[] = ["match", ["get", "iso3"]];
    for (const [iso, c] of byIso3) expr.push(iso, colorFor(c));
    expr.push(NO_DATA);
    for (const l of ["fill", "fill-multi"]) map.setPaintProperty(l, "fill-color", expr as never);
    map.setPaintProperty("islands", "circle-color", expr as never);
  }, [byIso3]);

  // Highlight the selected country.
  const prevSel = useRef<string | null>(null);
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.getSource("africa")) return;
    if (prevSel.current) map.setFeatureState({ source: "africa", id: prevSel.current }, { selected: false });
    if (selected) map.setFeatureState({ source: "africa", id: selected }, { selected: true });
    prevSel.current = selected;
  }, [selected]);

  const sel = byIso3.get(selected);
  const sorted = [...countries].sort((a, b) => (locale === "fr" ? a.name_fr : a.name_en).localeCompare(locale === "fr" ? b.name_fr : b.name_en));
  const nm = (c: OverviewCountry) => (locale === "fr" ? c.name_fr : c.name_en);

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
      <div className="min-w-0">
        {failed ? <Alert tone="warning">{d.africa.mapUnavailable}</Alert> : null}
        <div ref={ref} role="region" aria-label={d.africa.mapLabel} className="h-[420px] w-full overflow-hidden rounded-lg border border-line bg-[#e9f0f6] sm:h-[560px]" />
        <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted" aria-label={d.africa.legendTitle}>
          <span className="font-semibold text-ink">{d.africa.legendTitle}:</span>
          <span className="inline-flex items-center gap-1"><span className="inline-block h-3 w-4 rounded-sm" style={{ background: NO_DATA }} />{d.africa.legendNoData}</span>
          <span className="inline-flex items-center gap-1">
            {d.africa.legendData}:
            {STEPS.map(([min, col], i) => (
              <span key={min} className="inline-flex items-center gap-0.5"><span className="inline-block h-3 w-4 rounded-sm" style={{ background: col }} />{min}{i === STEPS.length - 1 ? "+" : `–${STEPS[i + 1][0] - 1}`}</span>
            ))}
          </span>
          <span className="inline-flex items-center gap-1"><span className="inline-block h-3 w-3 rounded-full border border-navy" style={{ background: NO_DATA }} />{d.africa.legendIslands}</span>
        </div>
        <p className="mt-1 text-xs text-muted">{d.africa.hoverHint}</p>
      </div>
      <aside className="min-w-0 space-y-3">
        <div>
          <label htmlFor="country-select" className="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted">{d.common.country}</label>
          <Select id="country-select" value={selected} onChange={(e) => setSelected(e.target.value)}>
            {sorted.map((c) => <option key={c.iso3} value={c.iso3}>{nm(c)}{c.has_data ? "" : ` — ${d.africa.legendNoData}`}</option>)}
          </Select>
        </div>
        <div className="rounded-lg border border-line bg-white p-3" aria-live="polite">{sel ? <CountryFigures c={sel} /> : null}</div>
        {islands.length ? (
          <div className="rounded-lg border border-line bg-white p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-muted">{d.africa.islandStates}</p>
            <p className="text-xs text-muted">{d.africa.legendIslands}</p>
            <ul className="mt-2 flex flex-wrap gap-2">
              {islands.map((iso) => {
                const c = byIso3.get(iso);
                return (
                  <li key={iso}>
                    <button type="button" onClick={() => setSelected(iso)} className="inline-flex items-center gap-1 rounded border border-line px-2 py-1 text-xs hover:bg-navy-50" aria-pressed={selected === iso}>
                      <span className="inline-block h-2.5 w-2.5 rounded-full border border-navy" style={{ background: colorFor(c) }} />
                      {c ? nm(c) : iso}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ) : null}
      </aside>
    </div>
  );
}
