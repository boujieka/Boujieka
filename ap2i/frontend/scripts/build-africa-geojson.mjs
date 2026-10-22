#!/usr/bin/env node
/**
 * Builds public/africa.geojson from world-atlas@2.0.2 (Natural Earth 1:110m, public domain).
 *
 * Keeps only the 54 countries listed by GET /api/v1/countries (matched on `iso_numeric`,
 * zero-padded to 3 digits like world-atlas ids, e.g. "012" for Algeria, "120" for Cameroon).
 * The list is fetched from AP2I_API_URL; if the API is unreachable, the cached copy
 * scripts/africa-countries.json (same shape) is used and the script says so.
 *
 * Countries absent from the 1:110m dataset (small island states) are NOT dropped: they are
 * emitted as Point features at their capital (property `geometry_kind: "marker"`) so the map
 * can draw them as clickable circle markers with the same data as the polygons.
 */
import { readFile, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { feature } from "topojson-client";

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const API = (process.env.AP2I_API_URL || "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

// Capital coordinates [lon, lat] for countries without a 1:110m polygon.
const CAPITALS = {
  "132": { capital: "Praia", coords: [-23.5133, 14.9315] }, // Cabo Verde
  "174": { capital: "Moroni", coords: [43.2551, -11.7172] }, // Comoros
  "480": { capital: "Port Louis", coords: [57.4977, -20.1609] }, // Mauritius
  "690": { capital: "Victoria", coords: [55.4513, -4.6191] }, // Seychelles
  "678": { capital: "São Tomé", coords: [6.7273, 0.3365] }, // São Tomé and Príncipe
};

const pad = (v) => String(v).padStart(3, "0");

async function loadCountries() {
  try {
    const r = await fetch(`${API}/countries`, { signal: AbortSignal.timeout(10000) });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    const list = data.map((c) => ({ iso_numeric: c.iso_numeric, iso3: c.iso3, name_en: c.name_en }));
    await writeFile(path.join(here, "africa-countries.json"), JSON.stringify(list, null, 1) + "\n");
    console.log(`countries: ${list.length} from ${API}/countries (cache refreshed)`);
    return list;
  } catch (e) {
    const list = JSON.parse(await readFile(path.join(here, "africa-countries.json"), "utf8"));
    console.warn(`API unreachable (${e.message}); using cached scripts/africa-countries.json (${list.length} countries)`);
    return list;
  }
}

const countries = await loadCountries();
const wanted = new Map(countries.map((c) => [pad(c.iso_numeric), c]));
const topo = require("world-atlas/countries-110m.json");
const fc = feature(topo, topo.objects.countries);

const features = [];
const found = new Set();
for (const f of fc.features) {
  const id = pad(f.id);
  const c = wanted.get(id);
  if (!c) continue;
  found.add(id);
  features.push({ type: "Feature", id: Number(id), properties: { iso_numeric: id, iso3: c.iso3, name: c.name_en, geometry_kind: "polygon" }, geometry: f.geometry });
}
const missing = [];
for (const [id, c] of wanted) {
  if (found.has(id)) continue;
  const cap = CAPITALS[id];
  if (!cap) {
    missing.push(`${c.iso3} (${id})`);
    continue;
  }
  features.push({
    type: "Feature", id: Number(id),
    properties: { iso_numeric: id, iso3: c.iso3, name: c.name_en, geometry_kind: "marker", capital: cap.capital },
    geometry: { type: "Point", coordinates: cap.coords },
  });
}
if (missing.length) {
  console.error(`No geometry and no capital marker for: ${missing.join(", ")}`);
  process.exit(1);
}
features.sort((a, b) => a.properties.iso3.localeCompare(b.properties.iso3));
const out = {
  type: "FeatureCollection",
  metadata: {
    source: "world-atlas@2.0.2 countries-110m.json (Natural Earth 1:110m, public domain)",
    note: "Small island states without a 1:110m polygon are Point features at their capital (geometry_kind=marker).",
  },
  features,
};
await writeFile(path.join(root, "public", "africa.geojson"), JSON.stringify(out));
const markers = features.filter((f) => f.properties.geometry_kind === "marker").map((f) => f.properties.iso3);
console.log(`wrote public/africa.geojson: ${features.length} features (${features.length - markers.length} polygons, markers: ${markers.join(", ")})`);
