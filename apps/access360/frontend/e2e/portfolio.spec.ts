import { expect, test, type Page } from "@playwright/test";
import path from "node:path";

// Phase 2: mandatory gates, Electrification Acceleration Score, portfolio ranking; plus the PostGIS site context.
const PASSWORD = "E2e-Password-2027";
const OUT = path.resolve(__dirname, "../../docs/screenshots");

async function createProject(page: Page, name: string, lat: string, lon: string) {
  await page.goto("/app/projects/new");
  await page.getByLabel("Name", { exact: true }).fill(name);
  await page.getByLabel("Country").selectOption({ label: "Kenya" });
  await page.getByLabel(/^Latitude/).fill(lat);
  await page.getByLabel(/^Longitude/).fill(lon);
  await page.getByTestId("create-project").click();
  await expect(page).toHaveURL(/\/app\/projects\/[0-9a-f-]{36}/);
  await expect(page.getByRole("heading", { name })).toBeVisible();
}

async function setGates(page: Page, state: Record<string, string>, months?: string, underserved?: string) {
  await page.getByTestId("tab-score").click();
  await expect(page.getByTestId("gates-form")).toBeVisible();
  for (const [g, v] of Object.entries(state)) await page.getByTestId(`gate-select-${g}`).selectOption(v);
  if (months !== undefined) await page.getByTestId("months-to-power").fill(months);
  if (underserved !== undefined) await page.getByTestId("underserved").selectOption(underserved);
  await page.getByTestId("save-gates").click();
  await expect(page.getByTestId("gates-saved")).toBeVisible();
}

test("gates, acceleration score, portfolio ranking and site context", async ({ page }) => {
  const pageErrors: string[] = [];
  page.on("pageerror", (e) => pageErrors.push(e.message));

  await page.goto("/register");
  await page.getByLabel("Full name").fill("E2E Portfolio");
  await page.getByLabel("Email").fill(`e2e-pf-${Date.now()}@example.org`);
  await page.getByLabel("Password").fill(PASSWORD);
  await page.getByLabel("Organisation name").fill("E2E Portfolio Ltd");
  await page.getByLabel("Organisation type").selectOption("developer");
  await page.getByLabel(/I accept the terms/).check();
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page).toHaveURL(/\/app$/);

  // project A: modelled, every gate met -> eligible with a rank
  await createProject(page, "E2E eligible site", "-1.29", "36.82");
  // site context from PostGIS (Nairobi area)
  const ctx = page.getByTestId("site-context");
  await expect(ctx).toBeVisible();
  await expect(ctx.getByTestId("context-country")).toContainText("Kenya");
  await expect(ctx.getByTestId("context-places")).toContainText("km");
  await expect(ctx.getByTestId("places-note")).toContainText("Natural Earth populated places");
  await expect(ctx).toContainText("Licence");
  if (process.env.SCREENSHOTS) await ctx.screenshot({ path: `${OUT}/project-site-context.png` });

  await page.getByTestId("tab-inputs").click();
  await page.getByTestId("load-demo-inputs").click();
  await page.getByTestId("save-inputs").click();
  await expect(page.getByTestId("inputs-message")).toContainText("Inputs saved");
  await page.getByTestId("tab-results").click();
  await page.getByTestId("run-model").click();
  await expect(page.getByTestId("kpi-project_irr_post_subsidy")).toBeVisible();

  await page.getByTestId("tab-score").click();
  await expect(page.getByTestId("model-gate")).toContainText("latest run status");
  await expect(page.getByTestId("weights-note")).toContainText("initial design assumptions");
  // equity has no underserved assessment yet: the criterion is shown as unavailable
  await expect(page.getByTestId("part-equity")).toHaveAttribute("data-missing", "true");
  await expect(page.getByTestId("part-equity")).toContainText("Data unavailable");
  const all = { land_rights: "met", permits: "met", technical_feasibility: "met", environmental_social: "met", regulatory: "met" };
  await setGates(page, all, "12", "yes");
  await expect(page.getByTestId("part-equity")).toHaveAttribute("data-missing", "false");
  await expect(page.getByTestId("score-value")).toHaveText(/^\d+(\.\d)?$/);
  const modelGateMet = (await page.getByTestId("model-gate").locator("[data-gate-state]").getAttribute("data-gate-state")) === "met";
  await expect(page.getByTestId("score-card").getByTestId("decision-badge")).toHaveAttribute("data-decision", modelGateMet ? "eligible" : "excluded");
  await page.reload();
  await expect(page.getByTestId("gate-select-permits")).toHaveValue("met");
  await expect(page.getByTestId("months-to-power")).toHaveValue("12");
  if (process.env.SCREENSHOTS) await page.evaluate(() => window.scrollTo(0, 0));
  if (process.env.SCREENSHOTS) await page.screenshot({ path: `${OUT}/project-score.png`, fullPage: true });

  // project B: a failed gate -> excluded, whatever its score
  await createProject(page, "E2E excluded site", "-0.10", "34.75");
  await setGates(page, { ...all, land_rights: "not_met" });
  await expect(page.getByTestId("score-card").getByTestId("decision-badge")).toHaveAttribute("data-decision", "excluded");
  await expect(page.getByTestId("score-card").getByTestId("gate-overrides")).toBeVisible();

  // portfolio
  await page.goto("/app/portfolio");
  await expect(page.getByRole("heading", { name: "Portfolio", exact: true })).toBeVisible();
  await page.getByLabel("Portfolio name").fill("E2E pipeline");
  await page.getByRole("button", { name: "Create portfolio" }).click();
  await expect(page.getByTestId("portfolio-name")).toHaveText("E2E pipeline");
  for (const name of ["E2E eligible site", "E2E excluded site"]) {
    await page.getByTestId("add-project-select").selectOption({ label: `${name} (Kenya)` });
    await page.getByTestId("add-project").click();
    await expect(page.getByTestId("ranking-table").locator(`[data-project="${name}"]`)).toBeVisible();
  }
  const rows = page.getByTestId("ranking-row");
  await expect(rows).toHaveCount(2);

  const excluded = page.locator('[data-testid=ranking-row][data-project="E2E excluded site"]');
  await expect(excluded).toHaveAttribute("data-decision", "excluded");
  await expect(excluded.getByTestId("rank")).toHaveText("Not ranked");
  await expect(excluded.getByTestId("gate-overrides")).toBeVisible();
  if (modelGateMet) {
    const eligible = page.locator('[data-testid=ranking-row][data-project="E2E eligible site"]');
    await expect(eligible).toHaveAttribute("data-decision", "eligible");
    await expect(eligible.getByTestId("rank")).toHaveText("1");
  }
  // the eligible site runs on synthetic demo inputs, so it is totalled as demo, never as real
  if (modelGateMet) {
    await expect(page.getByTestId("totals-demo")).toContainText("1 modelled");
  }
  await expect(page.getByTestId("totals-real")).toContainText("0 modelled");

  // weights rerun the analysis on the server
  await page.getByTestId("weight-access_impact").fill("50");
  await page.getByTestId("apply-weights").click();
  await expect(rows).toHaveCount(2);
  await expect(excluded.getByTestId("rank")).toHaveText("Not ranked");

  // row expansion: criteria, gates and sources
  await excluded.getByTestId("expand-row").click();
  const detail = page.getByTestId("ranking-detail");
  await expect(detail.getByTestId("score-breakdown")).toBeVisible();
  await expect(detail.getByTestId("gate-land_rights").locator("[data-gate-state]")).toHaveAttribute("data-gate-state", "not_met");
  await expect(detail.getByTestId("score-sources")).toContainText("milestones marked done");
  await expect(detail).toContainText("Excluded whatever the score");
  if (process.env.SCREENSHOTS) await page.evaluate(() => window.scrollTo(0, 0));
  if (process.env.SCREENSHOTS) await page.screenshot({ path: `${OUT}/portfolio-analysis.png`, fullPage: true });

  await page.getByTestId("lang-fr").click();
  await expect(page.getByRole("heading", { name: "Portefeuille", exact: true })).toBeVisible();
  await expect(excluded.getByTestId("rank")).toHaveText("Non classé");
  await page.getByTestId("lang-en").click();

  // dashboard card
  await page.goto("/app");
  await expect(page.getByTestId("dash-portfolios")).toContainText("Saved portfolios: 1");
  expect(pageErrors, pageErrors.join("\n")).toEqual([]);
});
