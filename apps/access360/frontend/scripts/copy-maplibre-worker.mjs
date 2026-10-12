// MapLibre GL 6 loads its web worker from a separate module file next to the library. Bundlers rewrite
// import.meta.url, so we serve the worker from /maplibre/ and point the library at it (see map-view.tsx).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "node_modules", "maplibre-gl", "dist", "maplibre-gl-worker.mjs");
const outDir = join(root, "public", "maplibre");
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "maplibre-gl-worker.mjs"));
console.log("copied maplibre-gl-worker.mjs to public/maplibre/");
