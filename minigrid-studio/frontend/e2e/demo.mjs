// Smoke test of the in-browser demo (engine in Pyodide), served as on Netlify.
//   node tools/web_demo/serve.mjs 8888 &   BASE=http://localhost:8888/app/ node frontend/e2e/demo.mjs
import { createRequire } from "node:module";
import fs from "node:fs";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const BASE = process.env.BASE ?? "http://localhost:8888/app/";
const SHOTS = process.env.SHOTS ?? "/tmp/mgs-shots";
fs.mkdirSync(SHOTS, { recursive: true });
const results = [];
const check = (name, ok, extra = "") => { results.push(ok); console.log(`${ok ? "PASS" : "FAIL"} ${name} ${extra}`); };

const browser = await chromium.launch();
const page = await (await browser.newContext({ acceptDownloads: true, viewport: { width: 1360, height: 900 } })).newPage();
const errors = [];
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
page.on("pageerror", (e) => errors.push(String(e)));

const t0 = Date.now();
await page.goto(BASE);
await page.getByRole("heading", { name: "Projets" }).waitFor({ timeout: 120000 });
check("engine loaded in the browser", true, `${((Date.now() - t0) / 1000).toFixed(1)} s`);
check("demo banner shown", await page.getByText("Démo dans le navigateur.").isVisible());

await page.getByRole("button", { name: "Nouveau projet" }).click();
await page.getByLabel("Nom").fill("Portefeuille test");
await page.getByRole("button", { name: "Créer" }).click();
await page.getByRole("heading", { name: "Portefeuille test" }).waitFor();
check("no workbook import in the demo", (await page.getByRole("button", { name: "Importer" }).count()) === 0);
await page.getByRole("button", { name: "À partir d'un gabarit" }).click();
await page.getByRole("button", { name: "Créer" }).click();
await page.getByRole("button", { name: "Calculer" }).waitFor();
const t1 = Date.now();
await page.getByRole("button", { name: "Calculer" }).click();
await page.getByRole("heading", { name: /Résultats/ }).waitFor({ timeout: 120000 });
const irr = await page.locator(".kpi").first().innerText();
check("project IRR equals the server engine (8,11 %)", /8,11\s?%/.test(irr), `${irr.replace(/\n/g, " | ")} in ${((Date.now() - t1) / 1000).toFixed(1)} s`);
check("reconciled status", await page.getByText("Moteur rapproché du classeur").first().isVisible());
await page.screenshot({ path: `${SHOTS}/demo-run.png`, fullPage: true });
const runUrl = page.url();

for (const [label, ext] of [["Classeur Studio (.xlsx, formules de contrôle)", ".xlsx"], ["Séries annuelles (.csv)", ".csv"]]) {
  const [dl] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: label }).click()]);
  const p = `${SHOTS}/demo-export${ext}`;
  await dl.saveAs(p);
  check(`export ${ext}`, fs.statSync(p).size > 1000, `${dl.suggestedFilename()} ${fs.statSync(p).size} B`);
}
check("no CrossBoundary export in the demo", (await page.getByRole("button", { name: "Choisir le fichier" }).count()) === 0);

await page.getByRole("button", { name: "Ajouter à la comparaison" }).click();
await page.locator("a", { hasText: "← " }).first().click();
await page.getByRole("tab", { name: "Dette senior" }).click();
const dscr = page.getByLabel("DSCR cible", { exact: true });
await dscr.fill("1,3");
await dscr.blur();
await page.getByRole("button", { name: "Enregistrer comme nouvelle version" }).click();
await page.waitForFunction(() => /v2/.test(document.querySelector("h1")?.textContent ?? ""), null, { timeout: 30000 });
await page.getByRole("button", { name: "Calculer" }).click();
await page.getByRole("heading", { name: /Résultats/ }).waitFor({ timeout: 120000 });
await page.getByRole("button", { name: "Ajouter à la comparaison" }).click();
await page.getByRole("link", { name: /Comparer \(2\)/ }).click();
await page.getByText("Hypothèses qui diffèrent").waitFor({ timeout: 60000 });
check("comparison works in the browser", (await page.locator("table.data").last().innerText()).includes("debt.target_dscr"));

await page.reload();
await page.getByRole("heading", { name: "Comparaison de scénarios" }).waitFor({ timeout: 120000 });
await page.goto(runUrl);
await page.getByRole("heading", { name: /Résultats/ }).waitFor({ timeout: 120000 });
check("data kept in the browser after reload", true);

await page.getByRole("button", { name: "Langue" }).click();
await page.getByRole("tab", { name: "Senior debt" }).waitFor({ timeout: 10000 }).catch(() => undefined);
await page.goto(BASE);
await page.getByRole("heading", { name: "Projects" }).waitFor({ timeout: 60000 });
check("English", true);
check("no console errors (CSP included)", errors.length === 0, errors.slice(0, 3).join(" | "));
await browser.close();
console.log(`\n${results.filter(Boolean).length}/${results.length} checks passed`);
process.exit(results.every(Boolean) ? 0 : 1);
