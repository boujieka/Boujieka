"use client";

import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef, useState } from "react";
import type { GeoJSONSource, Map as MlMap, StyleSpecification } from "maplibre-gl";
import { useI18n } from "@/lib/i18n";
import type { GeoJSONFeatureCollection } from "@/lib/types";

const STYLE_URL = process.env.NEXT_PUBLIC_MAP_STYLE_URL || "https://demotiles.maplibre.org/style.json";

const PLAIN_STYLE: StyleSpecification = {
  version: 8,
  sources: {},
  layers: [{ id: "plain-background", type: "background", paint: { "background-color": "#e9edf2" } }],
};

export const AFRICA_BOUNDS: [[number, number], [number, number]] = [
  [-20, -36],
  [53, 38],
];

export interface MapProject {
  id: string;
  name: string;
  lat: number;
  lon: number;
  is_demo: boolean;
}

export interface MapLayer {
  id: string;
  color: string;
  geojson: GeoJSONFeatureCollection;
}

async function loadStyle(): Promise<StyleSpecification | null> {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 6000);
  try {
    const res = await fetch(STYLE_URL, { signal: ctl.signal });
    if (!res.ok) return null;
    const s = (await res.json()) as StyleSpecification;
    return s && s.version === 8 ? s : null;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

function projectsFc(ps: MapProject[]): GeoJSON.FeatureCollection {
  return {
    type: "FeatureCollection",
    features: ps.map((p) => ({ type: "Feature", geometry: { type: "Point", coordinates: [p.lon, p.lat] }, properties: { id: p.id, name: p.name, demo: p.is_demo } })),
  };
}

/** Build popup content from text nodes only (dataset text is untrusted; never set HTML). */
function popupNode(props: Record<string, unknown>): HTMLElement {
  const root = document.createElement("div");
  root.style.fontSize = "12px";
  root.style.maxWidth = "240px";
  const entries = Object.entries(props).slice(0, 12);
  for (const [k, v] of entries) {
    const row = document.createElement("div");
    const b = document.createElement("strong");
    b.textContent = `${k}: `;
    row.appendChild(b);
    row.appendChild(document.createTextNode(v === null || v === undefined ? "–" : typeof v === "object" ? JSON.stringify(v) : String(v)));
    root.appendChild(row);
  }
  return root;
}

export function MapView({
  projects = [],
  layers = [],
  fit,
  onPick,
  picked,
  height = 520,
  onProjectClick,
}: {
  projects?: MapProject[];
  layers?: MapLayer[];
  fit?: [[number, number], [number, number]] | null;
  onPick?: (p: { lat: number; lon: number }) => void;
  picked?: { lat: number; lon: number } | null;
  height?: number | string;
  onProjectClick?: (id: string) => void;
}) {
  const { t } = useI18n();
  const el = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MlMap | null>(null);
  const [ready, setReady] = useState(false);
  const [basemapFailed, setBasemapFailed] = useState(false);
  const [fatal, setFatal] = useState<string | null>(null);
  const shownLayers = useRef<Set<string>>(new Set());
  const pickRef = useRef(onPick);
  const clickRef = useRef(onProjectClick);
  useEffect(() => {
    pickRef.current = onPick;
    clickRef.current = onProjectClick;
  });

  // create the map once
  useEffect(() => {
    let disposed = false;
    let map: MlMap | null = null;
    (async () => {
      const style = await loadStyle();
      if (disposed || !el.current) return;
      if (!style) setBasemapFailed(true);
      try {
        const ml = await import("maplibre-gl");
        if (disposed || !el.current) return;
        map = new ml.Map({
          container: el.current,
          style: style ?? PLAIN_STYLE,
          bounds: AFRICA_BOUNDS,
          fitBoundsOptions: { padding: 20 },
          attributionControl: { compact: true },
        });
        mapRef.current = map;
        map.addControl(new ml.NavigationControl({ showCompass: false }), "top-right");
        map.on("error", (e) => {
          // tile or sprite failures must never crash the page
          const msg = String((e as unknown as { error?: { message?: string } }).error?.message ?? "");
          if (!map?.isStyleLoaded() && /style|fetch|Failed/i.test(msg)) {
            setBasemapFailed(true);
            try {
              map?.setStyle(PLAIN_STYLE);
            } catch {
              /* ignore */
            }
          }
        });
        const init = () => {
          if (!map) return;
          if (!map.getSource("projects")) {
            map.addSource("projects", { type: "geojson", data: projectsFc([]) });
            map.addLayer({
              id: "projects-circle",
              type: "circle",
              source: "projects",
              paint: { "circle-radius": 7, "circle-color": "#0b1f3a", "circle-stroke-color": "#c8962e", "circle-stroke-width": 2.5 },
            });
          }
          if (!map.getSource("picked")) {
            map.addSource("picked", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
            map.addLayer({
              id: "picked-circle",
              type: "circle",
              source: "picked",
              paint: { "circle-radius": 8, "circle-color": "#0f8a5f", "circle-stroke-color": "#ffffff", "circle-stroke-width": 2 },
            });
          }
          shownLayers.current = new Set();
          setReady(true);
        };
        map.on("load", init);
        map.on("style.load", init);
        map.on("click", (e) => {
          const hits = map?.queryRenderedFeatures(e.point, { layers: ["projects-circle"] }) ?? [];
          if (hits.length && clickRef.current) {
            clickRef.current(String(hits[0].properties?.id));
            return;
          }
          if (pickRef.current) pickRef.current({ lat: Number(e.lngLat.lat.toFixed(5)), lon: Number(e.lngLat.lng.toFixed(5)) });
        });
        map.on("click", "projects-circle", (e) => {
          const f = e.features?.[0];
          if (!f || !map) return;
          new ml.Popup({ closeButton: true }).setLngLat(e.lngLat).setDOMContent(popupNode({ project: f.properties?.name })).addTo(map);
        });
        map.on("mouseenter", "projects-circle", () => map && (map.getCanvas().style.cursor = "pointer"));
        map.on("mouseleave", "projects-circle", () => map && (map.getCanvas().style.cursor = ""));
        // dataset popups
        map.on("click", (e) => {
          if (!map) return;
          const ids = [...shownLayers.current].flatMap((id) => [`ds-${id}-pt`, `ds-${id}-ln`, `ds-${id}-fl`]).filter((l) => map!.getLayer(l));
          if (!ids.length) return;
          const hit = map.queryRenderedFeatures(e.point, { layers: ids })[0];
          if (hit) new ml.Popup().setLngLat(e.lngLat).setDOMContent(popupNode((hit.properties as Record<string, unknown>) ?? {})).addTo(map);
        });
      } catch (err) {
        setFatal(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => {
      disposed = true;
      try {
        map?.remove();
      } catch {
        /* ignore */
      }
      mapRef.current = null;
    };
  }, []);

  // projects
  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map) return;
    (map.getSource("projects") as GeoJSONSource | undefined)?.setData(projectsFc(projects));
  }, [ready, projects]);

  // picked location
  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map) return;
    const fc: GeoJSON.FeatureCollection = picked
      ? { type: "FeatureCollection", features: [{ type: "Feature", geometry: { type: "Point", coordinates: [picked.lon, picked.lat] }, properties: {} }] }
      : { type: "FeatureCollection", features: [] };
    (map.getSource("picked") as GeoJSONSource | undefined)?.setData(fc);
  }, [ready, picked]);

  // dataset layers
  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map) return;
    const want = new Set(layers.map((l) => l.id));
    for (const id of [...shownLayers.current]) {
      if (!want.has(id)) {
        for (const l of [`ds-${id}-pt`, `ds-${id}-ln`, `ds-${id}-fl`]) if (map.getLayer(l)) map.removeLayer(l);
        if (map.getSource(`ds-${id}`)) map.removeSource(`ds-${id}`);
        shownLayers.current.delete(id);
      }
    }
    for (const l of layers) {
      if (shownLayers.current.has(l.id)) continue;
      try {
        map.addSource(`ds-${l.id}`, { type: "geojson", data: l.geojson as unknown as GeoJSON.FeatureCollection });
        map.addLayer(
          { id: `ds-${l.id}-fl`, type: "fill", source: `ds-${l.id}`, filter: ["==", ["geometry-type"], "Polygon"], paint: { "fill-color": l.color, "fill-opacity": 0.25 } },
          "projects-circle",
        );
        map.addLayer(
          { id: `ds-${l.id}-ln`, type: "line", source: `ds-${l.id}`, filter: ["in", ["geometry-type"], ["literal", ["LineString", "Polygon"]]], paint: { "line-color": l.color, "line-width": 2 } },
          "projects-circle",
        );
        map.addLayer(
          {
            id: `ds-${l.id}-pt`,
            type: "circle",
            source: `ds-${l.id}`,
            filter: ["==", ["geometry-type"], "Point"],
            paint: { "circle-radius": 5, "circle-color": l.color, "circle-stroke-color": "#ffffff", "circle-stroke-width": 1.5 },
          },
          "projects-circle",
        );
        shownLayers.current.add(l.id);
      } catch {
        /* a malformed layer must not break the map */
      }
    }
  }, [ready, layers]);

  // fit
  useEffect(() => {
    const map = mapRef.current;
    if (!ready || !map || !fit) return;
    try {
      map.fitBounds(fit, { padding: 48, maxZoom: 9, duration: 600 });
    } catch {
      /* ignore */
    }
  }, [ready, fit]);

  return (
    <div className="relative w-full overflow-hidden rounded-lg border border-border bg-[#e9edf2]" style={{ height }} data-testid="map-container">
      <div ref={el} className="absolute inset-0" aria-label="Map" role="region" />
      {basemapFailed || fatal ? (
        <div className="pointer-events-none absolute left-3 top-3 max-w-[80%] rounded-md border border-border bg-surface/95 px-3 py-2 text-xs text-muted-foreground shadow-sm" role="status" data-testid="map-fallback">
          {t("exp2.mapFailed")}
          {fatal ? ` (${fatal})` : ""}
        </div>
      ) : null}
    </div>
  );
}
