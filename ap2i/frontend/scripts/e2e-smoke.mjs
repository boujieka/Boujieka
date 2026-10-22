#!/usr/bin/env node
/**
 * Browser smoke test against a running production build (npm start) and the running API.
 *   BASE_URL=http://localhost:3000 AP2I_E2E_EMAIL=... AP2I_E2E_PASSWORD=... node scripts/e2e-smoke.mjs
 * Uses playwright-core with the Chromium at CHROMIUM_PATH (default /opt/pw-browsers/chromium).
 * Saves screenshots to ./screenshots and exits non-zero on any failed check or browser console error.
 * Note: with AP2I_E2E_CREATE_PLAN=1 it creates one Project Rescue plan (a write).
 */
import { mkdir } from "node:fs/promises";
import { chromium } from "playwright-core";

const BASE = process.env.BASE_URL || "http://localhost:3000";
const EMAIL = process.env.AP2I_E2E_EMAIL;
const PASSWORD = process.env.AP2I_E2E_PASSWORD;
const OUT = new URL("../screenshots/", import.meta.url).pathname;
await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || "/opt/pw-browsers/chromium",
  args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
});
const results = [];
const consoleErrors = [];

function watch(page, tag) {
  page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(`[${tag}] ${m.text()}`); });
  page.on("pageerror", (e) => consoleErrors.push(`[${tag}] pageerror: ${e.message}`));
}
function check(name, ok, detail = "") {
  results.push({ name, ok, detail });
  console.log(`${ok ? "PASS" : "FAIL"} ${name}${detail ? ` — ${detail}` : ""}`);
}
async function visit(page, path, { shot, wait } = {}) {
  const r = await page.goto(BASE + path, { waitUntil: "networkidle", timeout: 90000 });
  if (wait) await page.waitForSelector(wait, { timeout: 30000 }).catch(() => null);
  if (shot) await page.screenshot({ path: OUT + shot, fullPage: true });
  return r;
}
const text = (page) => page.locator("main").innerText();

const desktop = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: "fr-FR" });
const page = await desktop.newPage();
watch(page, "desktop");

// Public pages
let r = await visit(page, "/", { shot: "01-home-desktop.png" });
let t = await text(page);
check("/ renders", r.status() === 200 && t.includes("Chaque projet"), `status ${r.status()}`);
check("/ live KPI (documented projects > 0)", /projets documentés\s*[1-9]/i.test(t));

r = await visit(page, "/africa", { wait: ".maplibregl-canvas" });
await page.waitForTimeout(2500);
await page.screenshot({ path: OUT + "02-africa-desktop.png", fullPage: true });
const rows = await page.locator("table tbody tr").count();
const canvas = await page.locator(".maplibregl-canvas").count();
t = await text(page);
check("/africa map canvas", canvas === 1);
check("/africa table has 54 countries", rows === 54, `${rows} rows`);
check("/africa shows 'Non disponible' for no-data countries", t.includes("Non disponible"));
check("/africa island states listed", t.includes("Maurice") || t.includes("Mauritius"));

r = await visit(page, "/countries/CMR", { wait: "canvas" });
await page.waitForTimeout(1500);
await page.screenshot({ path: OUT + "03-country-cmr-desktop.png", fullPage: true });
t = await text(page);
check("/countries/CMR renders with data", r.status() === 200 && t.includes("Cameroun") && t.includes("Portefeuille annuel"), `status ${r.status()}`);
check("/countries/CMR charts present", (await page.locator("canvas").count()) >= 4);

r = await visit(page, "/countries/SEN");
t = await text(page);
check("/countries/SEN empty state", t.includes("Aucun enregistrement de projet importé"));

r = await visit(page, "/projects", { shot: "04-projects-desktop.png" });
const prow = await page.locator("table tbody tr").count();
check("/projects lists projects", r.status() === 200 && prow > 10, `${prow} rows`);
const firstRef = (await page.locator("table tbody tr td a").first().innerText()).trim();

r = await visit(page, `/projects/${firstRef}`);
t = await text(page);
check(`/projects/${firstRef} renders`, r.status() === 200 && t.includes("Accords de financement") && t.includes("Sources et provenance"));
r = await visit(page, "/projects/AP2I-CMR-ENERGY-000001", { wait: "canvas", shot: "05-project-detail-desktop.png" });
t = await text(page);
check("/projects/AP2I-CMR-ENERGY-000001 indicators + alerts", /formule/i.test(t) && t.includes("LOW_DISBURSEMENT"));

r = await visit(page, "/performance", { shot: "06-performance-desktop.png" });
t = await text(page);
check("/performance renders alerts + disclaimer", r.status() === 200 && t.includes("pas des constats de fraude") && (await page.locator("table tbody tr").count()) > 5);

for (const p of ["/sectors/ENERGY", "/financing", "/explorer", "/pricing", "/about", "/methodology", "/countries", "/sectors", "/reports"]) {
  r = await visit(page, p);
  check(`${p} renders`, r.status() === 200 && !(await text(page)).includes("Erreur "), `status ${r.status()}`);
}

// Language switch persists in a cookie
await visit(page, "/");
await page.getByRole("button", { name: "en", exact: true }).click();
await page.waitForLoadState("networkidle");
await page.waitForTimeout(800);
t = await text(page);
const cookies = await desktop.cookies();
check("language switch to EN", t.includes("Every Project") && cookies.some((c) => c.name === "ap2i_locale" && c.value === "en"));
await page.getByRole("button", { name: "fr", exact: true }).click();
await page.waitForLoadState("networkidle");

// Login + authenticated pages
if (EMAIL && PASSWORD) {
  await visit(page, "/login");
  await page.fill("#email", EMAIL);
  await page.fill("#password", PASSWORD);
  await Promise.all([page.waitForURL((u) => !u.pathname.startsWith("/login"), { timeout: 30000 }), page.click("button[type=submit]")]);
  const c2 = await desktop.cookies();
  const sess = c2.find((c) => c.name === "ap2i_session");
  check("login sets httpOnly SameSite=Strict session cookie", !!sess && sess.httpOnly && sess.sameSite === "Strict");
  const tokenInJs = await page.evaluate(() => document.cookie.includes("ap2i_session"));
  check("session token not readable from JS", !tokenInJs);

  r = await visit(page, "/intelligence");
  await page.getByRole("button", { name: /Banque mondiale au Cameroun entre 2015 et 2025/ }).click();
  await page.waitForSelector("text=Citations (", { timeout: 60000 }).catch(() => null);
  await page.screenshot({ path: OUT + "07-intelligence-desktop.png", fullPage: true });
  t = await text(page);
  check("/intelligence answer sections", t.includes("Faits") && t.includes("Calculs") && t.includes("Informations manquantes") && t.includes("Citations ("));
  check("/intelligence citations link to projects", (await page.locator('a[href^="/projects/AP2I-"]').count()) > 0);

  r = await visit(page, "/admin/connectors", { shot: "08-admin-connectors-desktop.png" });
  t = await text(page);
  check("/admin/connectors renders connectors", r.status() === 200 && t.includes("worldbank_projects") && t.includes("Synchroniser maintenant"));

  r = await visit(page, "/rescue");
  t = await text(page);
  check("/rescue dashboard renders (gated feature available)", r.status() === 200 && t.includes("Créer un plan pour un projet") && !t.includes("Connexion requise"));
  if (process.env.AP2I_E2E_CREATE_PLAN === "1") {
    await page.fill("#plan-project", "AP2I-CMR-ENERGY-000001");
    const priv = page.getByLabel(/Plan privé/);
    if (await priv.isChecked()) await priv.uncheck();
    await Promise.all([page.waitForURL(/\/rescue\/plans\/\d+/, { timeout: 30000 }), page.getByRole("button", { name: "Créer le plan" }).click()]);
    await page.waitForLoadState("networkidle");
    await page.screenshot({ path: OUT + "09-rescue-plan-desktop.png", fullPage: true });
    t = await text(page);
    check("rescue plan created and shows actions with evidence", t.includes("Éléments probants") && t.includes("Approuver"), page.url());
  } else {
    await page.screenshot({ path: OUT + "09-rescue-desktop.png", fullPage: true });
  }
  for (const p of ["/admin/sync-runs", "/admin/review", "/admin/matches", "/admin/users", "/admin/system", "/account", "/reports"]) {
    r = await visit(page, p);
    check(`${p} (logged in) renders`, r.status() === 200 && !(await text(page)).includes("Erreur "), `status ${r.status()}`);
  }
} else {
  console.log("SKIP authenticated checks (set AP2I_E2E_EMAIL / AP2I_E2E_PASSWORD)");
}

// Mobile 375px
const mobile = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const m = await mobile.newPage();
watch(m, "mobile");
for (const [p, shot] of [["/", "10-home-mobile-375.png"], ["/countries/CMR", "11-country-cmr-mobile-375.png"], ["/africa", "12-africa-mobile-375.png"], ["/projects", null], ["/projects/AP2I-CMR-ENERGY-000001", null], ["/performance", null]]) {
  await visit(m, p, { wait: p === "/africa" ? ".maplibregl-canvas" : undefined });
  await m.waitForTimeout(p === "/" ? 300 : 1500);
  const sw = await m.evaluate(() => document.documentElement.scrollWidth);
  check(`mobile 375px no horizontal page scroll ${p}`, sw <= 375, `scrollWidth ${sw}`);
  if (shot) await m.screenshot({ path: OUT + shot, fullPage: true });
}

await browser.close();
check("no browser console errors", consoleErrors.length === 0, consoleErrors.slice(0, 10).join(" | "));
const failed = results.filter((x) => !x.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
process.exit(failed.length ? 1 : 0);
