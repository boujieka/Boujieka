import { useEffect, useRef, useState } from "react";
import type { Map as MLMap, GeoJSONSource } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
// MapLibre 6 runs its tile worker from a separate module file: bundle it and tell MapLibre where it is.
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import { useI18n } from "../lib/i18n";
import { escapeHtml } from "../lib/format";

const NODATA = "#d5dbe3";
const RAMP = ["#d8efe6", "#8fd0b5", "#3fa883", "#087F5B", "#05563d"];

function emptyStyle() {
  return { version: 8 as const, sources: {}, layers: [{ id: "bg", type: "background" as const, paint: { "background-color": "#eef3f8" } }] };
}

function loadML() {
  return import("maplibre-gl").then((ml) => {
    ml.setWorkerUrl(workerUrl);
    return ml;
  });
}

function webglOK() {
  try {
    const c = document.createElement("canvas");
    return !!(c.getContext("webgl2") || c.getContext("webgl"));
  } catch {
    return false;
  }
}

/** Choropleth of Africa. `values`: iso3 -> number (absent = no data, drawn grey, never as zero). */
export function AfricaMap({ values, label, format, onSelect, selected }: {
  values: Map<string, number>; label: string; format: (v: number) => string; onSelect: (iso3: string) => void; selected?: string;
}) {
  const { t } = useI18n();
  const el = useRef<HTMLDivElement>(null);
  const map = useRef<MLMap | null>(null);
  const [failed, setFailed] = useState(!webglOK());
  const state = useRef({ values, format, onSelect, label });
  state.current = { values, format, onSelect, label };

  const breaks = (vals: number[]) => {
    const v = [...vals].sort((a, b) => a - b);
    if (!v.length) return [];
    return [0.2, 0.4, 0.6, 0.8].map((q) => v[Math.min(v.length - 1, Math.floor(q * v.length))]);
  };

  const paint = () => {
    const m = map.current;
    if (!m || !m.getSource("africa")) return;
    const vals = [...state.current.values.values()];
    const b = breaks(vals);
    // a single distinct value (e.g. one country with data) is drawn in the strong tone, not the palest one
    const single = new Set(vals).size === 1;
    const colorFor = (v: number) => (single ? RAMP[3] : RAMP[b.filter((x) => v > x).length]);
    const expr: unknown[] = ["match", ["get", "iso3"]];
    for (const [iso, v] of state.current.values) expr.push(iso, colorFor(v));
    expr.push(NODATA);
    const e = state.current.values.size ? expr : NODATA;
    m.setPaintProperty("africa-fill", "fill-color", e as never);
    m.setPaintProperty("africa-pts", "circle-color", e as never);
  };

  useEffect(() => {
    if (failed || !el.current) return;
    let disposed = false;
    Promise.all([loadML(), fetch(`${import.meta.env.BASE_URL}africa.geojson`).then((r) => r.json())]).then(([ml, geo]) => {
      if (disposed || !el.current) return;
      const m = new ml.Map({ container: el.current, style: emptyStyle() as never, center: [18, 2], zoom: 2.3, attributionControl: false, dragRotate: false });
      map.current = m;
      (el.current as unknown as { __map?: MLMap }).__map = m; // used by the end-to-end tests to locate a country
      m.addControl(new ml.NavigationControl({ showCompass: false }), "top-right");
      m.addControl(new ml.AttributionControl({ customAttribution: "Natural Earth (public domain)" }));
      m.on("load", () => {
        el.current?.setAttribute("data-ready", "1");
        m.addSource("africa", { type: "geojson", data: geo });
        m.addLayer({ id: "africa-fill", type: "fill", source: "africa", filter: ["!=", ["geometry-type"], "Point"], paint: { "fill-color": NODATA, "fill-opacity": 0.95 } });
        m.addLayer({ id: "africa-line", type: "line", source: "africa", paint: { "line-color": "#ffffff", "line-width": 0.8 } });
        m.addLayer({ id: "africa-sel", type: "line", source: "africa", filter: ["==", ["get", "iso3"], ""], paint: { "line-color": "#D9A323", "line-width": 2.5 } });
        m.addLayer({ id: "africa-pts", type: "circle", source: "africa", filter: ["==", ["geometry-type"], "Point"], paint: { "circle-radius": 6, "circle-color": NODATA, "circle-stroke-color": "#5c6b7a", "circle-stroke-width": 1 } });
        paint();
        const popup = new ml.Popup({ closeButton: false, closeOnClick: false });
        for (const layer of ["africa-fill", "africa-pts"]) {
          m.on("mousemove", layer, (e) => {
            const p = e.features?.[0]?.properties as { iso3: string; name: string } | undefined;
            if (!p) return;
            m.getCanvas().style.cursor = "pointer";
            const v = state.current.values.get(p.iso3);
            popup.setLngLat(e.lngLat).setHTML(`<b>${escapeHtml(p.name)}</b><br/>${escapeHtml(state.current.label)}: ${v === undefined ? escapeHtml(t("africa.noData")) : escapeHtml(state.current.format(v))}`).addTo(m);
          });
          m.on("mouseleave", layer, () => {
            m.getCanvas().style.cursor = "";
            popup.remove();
          });
          m.on("click", layer, (e) => {
            const iso = (e.features?.[0]?.properties as { iso3?: string } | undefined)?.iso3;
            if (iso) state.current.onSelect(iso);
          });
        }
      });
      m.on("error", () => undefined);
    }).catch(() => setFailed(true));
    return () => {
      disposed = true;
      map.current?.remove();
      map.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [failed]);

  useEffect(() => {
    paint();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [values]);
  useEffect(() => {
    const m = map.current;
    if (m?.getLayer("africa-sel")) m.setFilter("africa-sel", ["==", ["get", "iso3"], selected ?? ""]);
  }, [selected]);

  if (failed) return <p className="state">{t("africa.webgl")}</p>;
  const b = breaks([...values.values()]);
  return (
    <div>
      <div ref={el} className="map" role="application" aria-label={label} data-testid="africa-map" />
      <div className="legend" aria-label="legend">
        <span><i style={{ background: NODATA }} /> {t("africa.noData")}</span>
        {new Set(values.values()).size === 1 ? <span><i style={{ background: RAMP[3] }} /> {format([...values.values()][0])}</span>
          : values.size > 0 && RAMP.map((c, i) => (
            <span key={c}><i style={{ background: c }} /> {i === 0 ? "≤ " + format(b[0]) : "> " + format(b[i - 1])}</span>
          ))}
        <span className="muted">{t("africa.islands")}</span>
      </div>
    </div>
  );
}

export interface Marker {
  ref: string;
  title: string;
  lat: number;
  lon: number;
  precision: "exact" | "approx" | "unknown";
  color: string;
}

/** Project markers with clustering. Coordinates are those published by the source, never generated. */
export function ProjectMap({ markers, onOpen, center = [12.5, 6], zoom = 4.6 }: {
  markers: Marker[]; onOpen: (ref: string) => void; center?: [number, number]; zoom?: number;
}) {
  const { t } = useI18n();
  const el = useRef<HTMLDivElement>(null);
  const map = useRef<MLMap | null>(null);
  const [failed, setFailed] = useState(!webglOK());
  const openRef = useRef(onOpen);
  openRef.current = onOpen;
  const toGeo = (ms: Marker[]) => ({
    type: "FeatureCollection" as const,
    features: ms.map((m) => ({ type: "Feature" as const, geometry: { type: "Point" as const, coordinates: [m.lon, m.lat] },
      properties: { ref: m.ref, title: m.title, precision: m.precision, color: m.color } })),
  });
  const markersRef = useRef(markers);
  markersRef.current = markers;

  useEffect(() => {
    if (failed || !el.current) return;
    let disposed = false;
    Promise.all([loadML(), fetch(`${import.meta.env.BASE_URL}africa.geojson`).then((r) => r.json())]).then(([ml, geo]) => {
      if (disposed || !el.current) return;
      const m = new ml.Map({ container: el.current, style: emptyStyle() as never, center, zoom, attributionControl: false, dragRotate: false });
      map.current = m;
      m.addControl(new ml.NavigationControl({ showCompass: false }), "top-right");
      m.addControl(new ml.AttributionControl({ customAttribution: "Natural Earth (public domain)" }));
      m.on("load", () => {
        m.addSource("countries", { type: "geojson", data: geo });
        m.addLayer({ id: "c-fill", type: "fill", source: "countries", paint: { "fill-color": "#e3e8ee" } });
        m.addLayer({ id: "c-line", type: "line", source: "countries", paint: { "line-color": "#ffffff", "line-width": 1 } });
        m.addSource("pts", { type: "geojson", data: toGeo(markersRef.current), cluster: true, clusterRadius: 40, clusterMaxZoom: 9 });
        m.addLayer({ id: "clusters", type: "circle", source: "pts", filter: ["has", "point_count"],
          paint: { "circle-color": "#082B50", "circle-opacity": 0.85, "circle-radius": ["step", ["get", "point_count"], 14, 20, 18, 100, 24] } });
        m.addLayer({ id: "cluster-n", type: "symbol", source: "pts", filter: ["has", "point_count"],
          layout: { "text-field": ["get", "point_count_abbreviated"], "text-size": 11 }, paint: { "text-color": "#ffffff" } });
        m.addLayer({ id: "pt", type: "circle", source: "pts", filter: ["!", ["has", "point_count"]],
          paint: { "circle-radius": 6, "circle-color": ["get", "color"], "circle-stroke-color": "#ffffff", "circle-stroke-width": 1.5,
            "circle-opacity": ["match", ["get", "precision"], "exact", 1, 0.55] } });
        const popup = new ml.Popup({ closeButton: false, closeOnClick: false });
        m.on("click", "clusters", async (e) => {
          const f = e.features?.[0];
          if (!f) return;
          const src = m.getSource("pts") as GeoJSONSource;
          const z = await src.getClusterExpansionZoom(f.properties.cluster_id);
          m.easeTo({ center: (f.geometry as unknown as { coordinates: [number, number] }).coordinates, zoom: z });
        });
        m.on("click", "pt", (e) => {
          const ref = e.features?.[0]?.properties?.ref;
          if (ref) openRef.current(ref);
        });
        m.on("mousemove", "pt", (e) => {
          const p = e.features?.[0]?.properties as { title: string; ref: string; precision: string } | undefined;
          if (!p) return;
          m.getCanvas().style.cursor = "pointer";
          popup.setLngLat(e.lngLat).setHTML(`<b>${escapeHtml(p.ref)}</b><br/>${escapeHtml(p.title.slice(0, 120))}<br/><i>${escapeHtml(t("col.precision"))}: ${escapeHtml(t(`precision.${p.precision}`))}</i>`).addTo(m);
        });
        m.on("mouseleave", "pt", () => {
          m.getCanvas().style.cursor = "";
          popup.remove();
        });
        for (const l of ["clusters"]) m.on("mouseenter", l, () => { m.getCanvas().style.cursor = "pointer"; });
      });
    }).catch(() => setFailed(true));
    return () => {
      disposed = true;
      map.current?.remove();
      map.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [failed]);

  useEffect(() => {
    const src = map.current?.getSource("pts") as GeoJSONSource | undefined;
    src?.setData(toGeo(markers));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [markers]);

  if (failed) return <p className="state">{t("africa.webgl")}</p>;
  return <div ref={el} className="map" role="application" aria-label={t("projects.map")} data-testid="project-map" />;
}
