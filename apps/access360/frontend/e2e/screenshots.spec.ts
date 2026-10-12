import { expect, test, type Page } from "@playwright/test";
import path from "node:path";

// Captures review screenshots into apps/access360/docs/screenshots (demo workspace, synthetic data).
const OUT = path.resolve(__dirname, "../../docs/screenshots");
const DEMO_PW = process.env.A360_DEMO_PASSWORD || "Demo-password-2027";

async function login(page: Page) {
  await page.goto("/login?demo=1");
  await page.getByLabel("Password").fill(DEMO_PW);
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL(/\/app$/);
}

test.skip(!process.env.SCREENSHOTS, "set SCREENSHOTS=1 to capture review screenshots");

test("review screenshots", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("tagline")).toBeVisible();
  await page.screenshot({ path: `${OUT}/homepage.png`, fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: `${OUT}/homepage-mobile.png`, fullPage: true });
  await page.setViewportSize({ width: 1440, height: 900 });

  await login(page);
  await expect(page.getByTestId("panel-demo")).toBeVisible();
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${OUT}/dashboard.png`, fullPage: true });

  await page.goto("/app/projects");
  await page.getByRole("link", { name: /Demo site batch A/ }).first().click();
  await page.getByTestId("tab-results").click();
  await page.getByTestId("run-model").click();
  await expect(page.getByTestId("kpi-grid")).toBeVisible();
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${OUT}/project-results.png`, fullPage: true });

  await page.getByTestId("tab-sensitivity").click();
  await page.getByTestId("run-sensitivity").click();
  await expect(page.getByTestId("tornado")).toBeVisible();
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${OUT}/project-sensitivity.png`, fullPage: true });

  await page.goto("/app/optimizer");
  await expect(page.getByText(/SYNTHETIC DEMO DATA/)).toBeVisible();
  await page.getByTestId("compare-options").click();
  await expect(page.getByTestId("optimizer-results")).toBeVisible();
  await page.waitForTimeout(500);
  await page.getByTestId("optimizer-results").screenshot({ path: `${OUT}/optimizer-results.png` });

  await page.goto("/app/explore");
  await expect(page.getByTestId("map-container")).toBeVisible();
  await page.getByTestId("dataset-list").locator("input[type=checkbox]").first().click();
  await expect(page.getByTestId("dataset-list").locator("input[type=checkbox]").first()).toBeChecked();
  await page.waitForTimeout(4000);
  await page.screenshot({ path: `${OUT}/explore.png`, fullPage: true });
});
