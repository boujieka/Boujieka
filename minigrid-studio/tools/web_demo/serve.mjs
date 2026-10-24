// Local stand-in for Netlify: serves landing/ at / and the demo at /app/ with the CSP of landing/netlify.toml.
//   node tools/web_demo/serve.mjs [port]
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../landing");
const toml = fs.readFileSync(path.join(ROOT, "netlify.toml"), "utf8");
const rules = [...toml.matchAll(/for = "([^"]+)"\s*\[headers\.values\]([\s\S]*?)(?=\[\[headers\]\]|$)/g)].map((m) => ({
  pattern: m[1], headers: Object.fromEntries([...m[2].matchAll(/^\s*([\w-]+) = "(.*)"$/gm)].map((h) => [h[1], h[2]])),
}));
const matches = (p, url) => (p.endsWith("/*") ? url.startsWith(p.slice(0, -1)) : url === p);
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".wasm": "application/wasm", ".zip": "application/zip", ".png": "image/png", ".svg": "image/svg+xml" };

http.createServer((req, res) => {
  const url = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let file = path.join(ROOT, url);
  if (!file.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
  if (!fs.existsSync(file)) { res.writeHead(404).end("not found"); return; }
  const lookup = url.endsWith("/") ? url : url;
  for (const r of rules) if (matches(r.pattern, lookup)) for (const [k, v] of Object.entries(r.headers)) res.setHeader(k, v);
  res.setHeader("Content-Type", TYPES[path.extname(file)] ?? "application/octet-stream");
  fs.createReadStream(file).pipe(res);
}).listen(Number(process.argv[2] ?? 8888), () => console.log(`serving ${ROOT}`));
