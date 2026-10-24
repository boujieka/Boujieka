// End-to-end smoke test of the web interface against a running API and Vite dev server.
//   BASE=http://localhost:5173 ADMIN_EMAIL=... ADMIN_PASSWORD=... SHOTS=/tmp/shots node e2e/smoke.mjs
// Uses the Playwright + Chromium already installed on the machine (require('playwright')).
import { createRequire } from "node:module";
import fs from "node:fs";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const BASE = process.env.BASE ?? "http://localhost:5173";
const SHOTS = process.env.SHOTS ?? "/tmp/mgs-shots";
const ADMIN = { email: process.env.ADMIN_EMAIL, password: process.env.ADMIN_PASSWORD };
fs.mkdirSync(SHOTS, { recursive: true });

const results = [];
const check = (name, ok, extra = "") => { results.push({ name, ok, extra }); console.log(`${ok ? "PASS" : "FAIL"} ${name} ${extra}`); };

const browser = await chromium.launch();
const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1360, height: 900 }, locale: "fr-FR" });
const page = await ctx.newPage();
const consoleErrors = [];
page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text()); });
page.on("pageerror", (e) => consoleErrors.push(String(e)));

async function shot(name) { await page.screenshot({ path: `${SHOTS}/${name}.png`, fullPage: true }); }

// 1. sign in
await page.goto(BASE);
await page.getByLabel("E-mail").fill(ADMIN.email);
await page.getByLabel("Mot de passe").fill(ADMIN.password);
await page.getByRole("button", { name: "Se connecter" }).click();
await page.getByRole("heading", { name: "Projets" }).waitFor();
check("login and project list", true);
await shot("01-projects");

// 2. new project, version from the fictitious template, calculation
const projectName = `E2E ${Date.now()}`;
await page.getByRole("button", { name: "Nouveau projet" }).click();
await page.getByLabel("Nom").fill(projectName);
await page.getByLabel("Pays").fill("Fictitia");
await page.getByRole("button", { name: "Créer" }).click();
await page.getByRole("heading", { name: projectName }).waitFor();
check("project created", true);
await page.getByRole("button", { name: "À partir d'un gabarit" }).click();
await page.getByLabel("Gabarit").selectOption("demo_fictitious");
await page.getByRole("button", { name: "Créer" }).click();
await page.getByRole("button", { name: "Calculer" }).waitFor();
check("version created from template", /base · v1/.test(await page.locator("h1").innerText()));
await page.goBack();
await page.getByRole("heading", { name: "Versions de scénario" }).waitFor();
await shot("02-project");
await page.goForward();
await page.getByRole("button", { name: "Calculer" }).waitFor();
await shot("03-version");
await page.getByRole("button", { name: "Calculer" }).click();
await page.getByRole("heading", { name: /Résultats/ }).waitFor({ timeout: 60000 });
const irr = await page.locator(".kpi").first().innerText();
check("run page shows the project IRR", /TRI projet/.test(irr) && /%/.test(irr), irr.replace(/\n/g, " | "));
check("run reconciled with the workbook", await page.getByText("Moteur rapproché du classeur").first().isVisible());
await page.locator(".chart svg").first().hover({ position: { x: 200, y: 100 } });
check("chart tooltip on hover", await page.locator(".chart .tip").first().isVisible());
await shot("04-run");
const runUrl = page.url();

// 3. exports
for (const [label, ext] of [["Rapport PDF", ".pdf"], ["Classeur Studio (.xlsx, formules de contrôle)", ".xlsx"], ["Séries annuelles (.csv)", ".csv"]]) {
  const [dl] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: label }).click()]);
  const path = `${SHOTS}/export${ext}`;
  await dl.saveAs(path);
  const size = fs.statSync(path).size;
  check(`export ${ext}`, dl.suggestedFilename().endsWith(ext) && size > 1000, `${dl.suggestedFilename()} ${size} B`);
}

// 4. edit an assumption -> new version -> run
await page.locator("a", { hasText: "← " }).first().click();
await page.getByRole("tab", { name: "Dette senior" }).click();
const dscr = page.getByLabel("DSCR cible", { exact: true });
const before = Number((await dscr.inputValue()).replace(",", "."));
await dscr.fill(String(Math.round((before + 0.1) * 100) / 100).replace(".", ","));   // French decimal comma
await dscr.blur();
await page.getByRole("button", { name: "Enregistrer comme nouvelle version" }).click();
const v1Url = page.url();
await page.waitForFunction((u) => location.href !== u, v1Url, { timeout: 15000 });
check("revision creates a new version", true, await page.locator("h1").innerText());
await page.getByRole("button", { name: "Calculer" }).click();
await page.getByRole("heading", { name: /Résultats/ }).waitFor({ timeout: 60000 });
await page.getByRole("button", { name: "Ajouter à la comparaison" }).click();
await page.goto(runUrl);
await page.getByRole("button", { name: "Ajouter à la comparaison" }).click();

// 5. comparison
await page.getByRole("link", { name: /Comparer \(2\)/ }).click();
await page.getByRole("heading", { name: "Comparaison de scénarios" }).waitFor();
await page.getByText("Hypothèses qui diffèrent").waitFor();
const diffs = await page.locator("table.data").last().innerText();
check("comparison lists the changed DSCR target", diffs.includes("debt.target_dscr"));
check("comparison shows deltas", (await page.getByText(/^Écart/).count()) > 0);
await shot("05-compare");

// 6. lots: remove the last (spare) lot -> new version
await page.goto(runUrl);
await page.locator("a", { hasText: "← " }).first().click();
await page.getByRole("tab", { name: "Sites et lots" }).click();
check("6 lots: no add button (workbook has 6 lot columns)", (await page.getByRole("button", { name: "Ajouter un lot" }).count()) === 0);
await page.locator("thead th").filter({ hasText: "Spare 3" }).getByRole("button", { name: "Retirer" }).click();
await page.getByRole("button", { name: "Enregistrer comme nouvelle version" }).click();
const lotsUrl = page.url();
await page.waitForFunction((u) => location.href !== u, lotsUrl, { timeout: 15000 });
await page.getByRole("tab", { name: "Sites et lots" }).click();
check("lot removed in the new version", (await page.locator("thead th").filter({ hasText: "Spare 3" }).count()) === 0
  && (await page.getByRole("button", { name: "Ajouter un lot" }).count()) === 1);
await shot("06-lots");

// 7. English
await page.getByRole("button", { name: "Langue" }).click();
await page.getByRole("button", { name: "Calculate" }).waitFor();
check("interface switches to English", await page.getByRole("tab", { name: "Senior debt" }).waitFor({ timeout: 10000 }).then(() => true, () => false));
await page.getByRole("button", { name: "Language" }).click();

// 8. invitation of a reviewer, acceptance in a separate browser, four-eyes approval
await page.getByRole("link", { name: "Administration" }).click();
await page.getByLabel("E-mail").fill(`reviewer-${Date.now()}@example.org`);
await page.getByLabel("Rôle", { exact: true }).selectOption("reviewer");
await page.getByRole("button", { name: "Inviter" }).click();
const link = await page.getByLabel("invitation link").inputValue();
check("invitation link created", link.includes("#/invite/"));
await shot("07-admin");
// submit the first version for review (the admin is its author, so cannot approve it)
await page.goto(runUrl);
await page.locator("a", { hasText: "← " }).first().click();
await page.getByRole("button", { name: "Soumettre à revue" }).click();
await page.getByText("Règle des quatre yeux").waitFor();
check("author sees the four-eyes rule instead of approve", true);
const versionUrl = page.url();

const ctx2 = await browser.newContext({ viewport: { width: 1280, height: 860 } });
const p2 = await ctx2.newPage();
await p2.goto(link);
await p2.getByLabel("Nom").fill("Revue");
await p2.getByLabel("Mot de passe").fill("reviewer passphrase 1");
await p2.getByRole("button", { name: "Accepter l'invitation" }).click();
await p2.getByRole("heading", { name: "Projets" }).waitFor({ timeout: 15000 });
check("invitee account created and signed in", true);
await p2.goto(versionUrl);
await p2.getByRole("button", { name: "Approuver" }).click();
await p2.locator(".badge", { hasText: "Approuvée" }).first().waitFor();
check("reviewer approves", true);
await p2.screenshot({ path: `${SHOTS}/08-approved.png`, fullPage: true });

// 9. mobile width
await page.setViewportSize({ width: 390, height: 844 });
await page.goto(runUrl);
await page.getByRole("heading", { name: /Résultats/ }).waitFor();
const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
check("no horizontal page scroll at phone width", overflow <= 1, `overflow ${overflow}px`);
await shot("09-mobile");

check("no console errors", consoleErrors.length === 0, consoleErrors.slice(0, 3).join(" | "));
await browser.close();
const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
process.exit(failed.length ? 1 : 0);
