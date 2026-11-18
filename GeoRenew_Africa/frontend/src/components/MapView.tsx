import maplibregl, { type GeoJSONSource, type StyleSpecification } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef, useState } from "react";
import type { FeatureCollection } from "geojson";
import { t } from "../i18n";

export interface Overlay {
  id: string;
  label: string;
  color: string;
  data: FeatureCollection;
  fillOpacity?: number;
  dashed?: boolean;
}

interface Props {
  overlays: Overlay[];
  fitTo?: [number, number, number, number] | null;
  drawing?: boolean;
  onDrawChange?: (coords: [number, number][]) => void;
  drawCoords?: [number, number][];
}

const EMPTY: FeatureCollection = { type: "FeatureCollection", features: [] };

const STYLE: StyleSpecification = {
  version: 8,
  sources: {
    osm: {
      type: "raster",
      tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      maxzoom: 19,
      attribution: "© contributeurs OpenStreetMap (fond de démonstration, aucune donnée métier)",
    },
  },
  layers: [
    { id: "background", type: "background", paint: { "background-color": "#eef1ec" } },
    { id: "osm", type: "raster", source: "osm" },
  ],
};

function drawFC(coords: [number, number][]): FeatureCollection {
  const feats: FeatureCollection["features"] = coords.map((c) => ({
    type: "Feature",
    geometry: { type: "Point", coordinates: c },
    properties: {},
  }));
  if (coords.length >= 2) {
    const ring = coords.length >= 3 ? [...coords, coords[0]] : coords;
    feats.push({ type: "Feature", geometry: { type: "LineString", coordinates: ring }, properties: {} });
  }
  return { type: "FeatureCollection", features: feats };
}

export function MapView({ overlays, fitTo, drawing = false, onDrawChange, drawCoords = [] }: Props) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [ready, setReady] = useState(false);
  const [basemap, setBasemap] = useState(true);
  const added = useRef<Set<string>>(new Set());
  const drawRef = useRef({ drawing, drawCoords, onDrawChange });
  drawRef.current = { drawing, drawCoords, onDrawChange };

  useEffect(() => {
    if (!container.current) return;
    const map = new maplibregl.Map({ container: container.current, style: STYLE, center: [20, 2], zoom: 2.6 });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.addControl(new maplibregl.ScaleControl({ unit: "metric", maxWidth: 140 }), "bottom-left");
    map.on("load", () => {
      map.addSource("draw", { type: "geojson", data: EMPTY });
      map.addLayer({ id: "draw-line", type: "line", source: "draw", filter: ["==", "$type", "LineString"],
        paint: { "line-color": "#d9480f", "line-width": 2, "line-dasharray": [2, 1] } });
      map.addLayer({ id: "draw-pt", type: "circle", source: "draw", filter: ["==", "$type", "Point"],
        paint: { "circle-radius": 4, "circle-color": "#d9480f", "circle-stroke-color": "#fff", "circle-stroke-width": 1 } });
      setReady(true);
    });
    map.on("click", (e) => {
      const d = drawRef.current;
      if (!d.drawing || !d.onDrawChange) return;
      d.onDrawChange([...d.drawCoords, [e.lngLat.lng, e.lngLat.lat]]);
    });
    mapRef.current = map;
    (window as unknown as { __georenewMap?: maplibregl.Map }).__georenewMap = map; // accès pour les tests E2E
    return () => {
      map.remove();
      mapRef.current = null;
      added.current.clear();
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !ready) return;
    map.setLayoutProperty("osm", "visibility", basemap ? "visible" : "none");
  }, [basemap, ready]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !ready) return;
    const wanted = new Set(overlays.map((o) => o.id));
    for (const id of [...added.current]) {
      if (!wanted.has(id)) {
        for (const suffix of ["fill", "line", "pt"]) if (map.getLayer(`${id}-${suffix}`)) map.removeLayer(`${id}-${suffix}`);
        if (map.getSource(id)) map.removeSource(id);
        added.current.delete(id);
      }
    }
    for (const o of overlays) {
      const src = map.getSource(o.id) as GeoJSONSource | undefined;
      if (src) {
        src.setData(o.data);
        continue;
      }
      map.addSource(o.id, { type: "geojson", data: o.data });
      const before = map.getLayer("draw-line") ? "draw-line" : undefined;
      map.addLayer({ id: `${o.id}-fill`, type: "fill", source: o.id, filter: ["==", "$type", "Polygon"],
        paint: { "fill-color": o.color, "fill-opacity": o.fillOpacity ?? 0.35 } }, before);
      map.addLayer({ id: `${o.id}-line`, type: "line", source: o.id,
        filter: ["any", ["==", "$type", "Polygon"], ["==", "$type", "LineString"]],
        paint: { "line-color": o.color, "line-width": 2, ...(o.dashed ? { "line-dasharray": [3, 2] } : {}) } }, before);
      map.addLayer({ id: `${o.id}-pt`, type: "circle", source: o.id, filter: ["==", "$type", "Point"],
        paint: { "circle-radius": 5, "circle-color": o.color, "circle-stroke-color": "#fff", "circle-stroke-width": 1 } }, before);
      added.current.add(o.id);
    }
    // Ordre d'empilement = ordre de la liste
    for (const o of overlays) for (const suffix of ["fill", "line", "pt"]) {
      if (map.getLayer(`${o.id}-${suffix}`)) map.moveLayer(`${o.id}-${suffix}`, "draw-line");
    }
  }, [overlays, ready]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !ready) return;
    (map.getSource("draw") as GeoJSONSource).setData(drawing ? drawFC(drawCoords) : EMPTY);
    map.getCanvas().style.cursor = drawing ? "crosshair" : "";
  }, [drawing, drawCoords, ready]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !ready || !fitTo) return;
    map.fitBounds([[fitTo[0], fitTo[1]], [fitTo[2], fitTo[3]]], { padding: 50, maxZoom: 16, duration: 0 });
  }, [fitTo, ready]);

  return (
    <div className="map-wrap">
      <div ref={container} className="map" data-testid="map" />
      <div className="map-legend" aria-label={t("map.legend")}>
        <label className="legend-row">
          <input type="checkbox" checked={basemap} onChange={(e) => setBasemap(e.target.checked)} /> {t("map.basemap")}
        </label>
        {overlays.map((o) => (
          <div key={o.id} className="legend-row">
            <span className="swatch" style={{ background: o.color, opacity: o.fillOpacity ?? 0.6 }} />
            {o.label}
          </div>
        ))}
      </div>
    </div>
  );
}
