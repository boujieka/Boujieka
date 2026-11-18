// Test E2E de bout en bout (Playwright) contre une instance en marche.
// Prérequis : API + front servis sur GEORENEW_URL (défaut http://127.0.0.1:8000) et démo chargée
// (python -m app.demo load). Usage : node e2e/smoke.mjs [dossier_captures]
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

// Playwright préinstallé (global) ou ajouté au projet : résolu par require, comme Node le permet.
const { chromium } = createRequire(import.meta.url)("playwright");

const BASE = process.env.GEORENEW_URL ?? "http://127.0.0.1:8000";
const SHOTS = process.argv[2];
const here = path.dirname(fileURLToPath(import.meta.url));
const exclusionFile = path.resolve(here, "../../examples/demo_fictive/zones_humides_FICTIVES.geojson");

function assert(cond, msg) {
  if (!cond) throw new Error(`ÉCHEC : ${msg}`);
  console.log(`ok - ${msg}`);
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: SHOTS ? 2 : 1 });
const appErrors = [];
page.on("pageerror", (e) => appErrors.push(e.message));
page.on("dialog", (d) => d.accept());

try {
  // 1. Portefeuille et projet de démonstration
  await page.goto(BASE + "/");
  await page.getByTestId("project-list").getByText("DÉMO — Projet PV fictif").click();
  await page.getByTestId("fictional-banner").waitFor();
  assert(true, "bandeau DONNÉES FICTIVES affiché sur le projet de démonstration");

  // 2. Sélection d'un site puis analyse
  await page.getByRole("button", { name: "Parcelle A (fictive)" }).click();
  await page.getByRole("tab", { name: "Analyse" }).click();
  await page.locator('input[name="setback_m"]').fill("20");
  await page.locator('input[name="setback_justification"]').fill("Hypothèse de démonstration");
  await page.getByTestId("run-analysis").click();
  await page.getByTestId("results").waitFor();
  const net = page.getByTestId("metric-surface_nette");
  assert((await net.textContent()).includes("Calculé"), "surface nette étiquetée « Calculé »");
  assert((await page.getByTestId("metric-puissance_indicative_mwp_dc").textContent()).includes("Inconnu"),
    "puissance sans densité étiquetée « Inconnu »");
  assert((await page.getByTestId("metric-intervalle_surface_nette").textContent()).includes("Inconnu"),
    "intervalle sans précision déclarée étiqueté « Inconnu »");
  const netText = await net.textContent();
  await page.waitForFunction(() => {
    const m = window.__georenewMap;
    return m && m.getSource("run-surface_nette") && m.getLayer("run-exclusion_stricte-fill");
  });
  assert(true, "couches de résultat (surface nette, exclusions) affichées sur la carte");
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, "analyse_demo.png") });

  // 3. Relance identique : résultat réutilisé
  await page.getByTestId("run-analysis").click();
  await page.getByText("résultat réutilisé").waitFor();
  assert((await net.textContent()) === netText, "relance identique : même surface nette, analyse réutilisée");

  // 4. Nouveau projet, site dessiné, import, règle, analyse
  await page.getByRole("link", { name: "Portefeuille" }).click();
  await page.locator('input[name="name"]').fill("Projet E2E");
  await page.locator('input[name="country_iso3"]').fill("zaf");
  await page.getByRole("button", { name: "Créer le projet" }).click();
  await page.getByRole("tab", { name: "Sites" }).waitFor();
  await page.waitForFunction(() => window.__georenewMap?.loaded());
  await page.evaluate(() => window.__georenewMap.jumpTo({ center: [27.2, -26.5], zoom: 14 }));
  await page.getByRole("button", { name: "Dessiner un site" }).click();
  const box = await page.getByTestId("map").boundingBox();
  const cx = box.x + box.width / 2, cy = box.y + box.height / 2;
  for (const [dx, dy] of [[-150, -100], [150, -100], [150, 100], [-150, 100]]) await page.mouse.click(cx + dx, cy + dy);
  await page.getByText("4 sommet(s)").waitFor();
  await page.getByRole("button", { name: "Terminer" }).click();
  await page.getByTestId("site-list").getByRole("button", { name: "Site 1" }).waitFor();
  assert(true, "site dessiné sur la carte et enregistré");

  await page.getByRole("tab", { name: "Données" }).click();
  await page.locator('input[type="file"][name="file"]').setInputFiles(exclusionFile);
  await page.locator('form input[name="name"]').fill("Exclusions test (fictives)");
  await page.locator('input[name="is_synthetic"]').check();
  await page.getByRole("button", { name: "Importer un jeu de données" }).click();
  await page.getByText("SHA-256").first().waitFor();
  assert((await page.locator(".prov").first().textContent()).includes("EPSG:4326"), "jeu importé avec SCR source et empreinte affichés");

  await page.getByRole("tab", { name: "Règles" }).click();
  await page.locator('form input[name="name"]').fill("Exclusion test");
  await page.locator('input[name="buffer_m"]').fill("50");
  await page.getByRole("button", { name: "Nouvelle règle" }).click();
  await page.locator(".error").first().waitFor().catch(() => {});
  // sans justification, le formulaire HTML ou l'API refuse ; on justifie puis on recrée
  await page.locator('select[name="justification_type"]').selectOption("hypothese_utilisateur");
  await page.locator('textarea[name="justification"]').fill("Hypothèse de test E2E");
  await page.getByRole("button", { name: "Nouvelle règle" }).click();
  await page.getByTestId("rule-list").getByText("Exclusion test").waitFor();
  assert(true, "règle d'exclusion créée avec buffer justifié");

  await page.getByRole("tab", { name: "Sites" }).click();
  await page.getByTestId("site-list").getByRole("button", { name: "Site 1" }).click();
  await page.getByRole("tab", { name: "Analyse" }).click();
  await page.getByTestId("run-analysis").click();
  await page.getByTestId("results").waitFor();
  assert((await page.getByTestId("results").textContent()).includes("reconnaissance préliminaire"),
    "niveau d'étude « reconnaissance préliminaire » affiché");
  const exportHref = await page.getByRole("link", { name: "Exporter CSV" }).getAttribute("href");
  const csv = await (await page.request.get(BASE + exportHref)).text();
  assert(csv.includes("surface_nette") && csv.includes("DONNÉES FICTIVES"), "export CSV téléchargeable et marqué fictif");

  assert(appErrors.length === 0, `aucune erreur JavaScript (${appErrors.join(" | ") || "0"})`);
  console.log("E2E : tous les contrôles sont passés");
} catch (e) {
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, "echec.png") }).catch(() => {});
  console.error(e.message);
  process.exitCode = 1;
} finally {
  await browser.close();
}
