import { expect, test } from "@playwright/test";

const PASSWORD = "E2e-Password-2027";

test("register, model a project, export, switch language, optimizer and explore", async ({ page }) => {
  const pageErrors: string[] = [];
  page.on("pageerror", (e) => pageErrors.push(e.message));

  // 1. register
  const email = `e2e-${Date.now()}@example.org`;
  await page.goto("/register");
  await page.getByLabel("Full name").fill("E2E Tester");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(PASSWORD);
  await page.getByLabel("Organisation name").fill("E2E Developer Ltd");
  await page.getByLabel("Organisation type").selectOption("developer");
  await page.getByLabel(/I accept the terms/).check();
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page).toHaveURL(/\/app$/);
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();

  // 2. create a project
  await page.goto("/app/projects/new");
  await page.getByLabel("Name", { exact: true }).fill("E2E solar site");
  await page.getByLabel("Country").selectOption({ label: "Kenya" });
  await page.getByTestId("create-project").click();
  await expect(page).toHaveURL(/\/app\/projects\/[0-9a-f-]{36}/);
  await expect(page.getByRole("heading", { name: "E2E solar site" })).toBeVisible();

  // 3. load the synthetic demo inputs and save
  await page.getByTestId("tab-inputs").click();
  await page.getByTestId("load-demo-inputs").click();
  await expect(page.getByTestId("inputs-message")).toContainText("SYNTHETIC");
  await page.getByTestId("save-inputs").click();
  await expect(page.getByTestId("inputs-message")).toContainText("Inputs saved");

  // 4. run the model
  await page.getByTestId("tab-results").click();
  await page.getByTestId("run-model").click();
  const badge = page.getByTestId("tab-results").locator("xpath=ancestor::*[@role='tablist']/following-sibling::*").getByTestId("status-badge").first();
  await expect(badge).toBeVisible();
  await expect(badge).toHaveAttribute("data-status", /^(validated|warning|failed_checks|incomplete_inputs)$/);
  await expect(page.getByTestId("kpi-project_irr_post_subsidy")).toBeVisible();
  await expect(page.getByTestId("kpi-project_irr_post_subsidy")).not.toContainText("–");
  await expect(page.getByTestId("demo-badge").first()).toBeVisible();

  // 5. sensitivity
  await page.getByTestId("tab-sensitivity").click();
  await page.getByTestId("run-sensitivity").click();
  await expect(page.getByTestId("sensitivity-table")).toBeVisible();
  expect(await page.getByTestId("sensitivity-table").locator("tbody tr").count()).toBeGreaterThan(1);

  // 6. teaser PDF
  await page.getByTestId("tab-exports").click();
  const href = await page.getByTestId("download-teaser").getAttribute("href");
  expect(href).toBeTruthy();
  const pdf = await page.request.get(href!);
  expect(pdf.status()).toBe(200);
  expect(pdf.headers()["content-type"]).toContain("application/pdf");
  expect((await pdf.body()).subarray(0, 5).toString()).toBe("%PDF-");
  const dl = page.waitForEvent("download");
  await page.getByTestId("download-teaser").click();
  expect((await dl).suggestedFilename()).toMatch(/\.pdf$/);

  // 7. French
  await page.getByTestId("lang-fr").click();
  const nav = page.getByTestId("main-nav");
  await expect(nav).toContainText("Tableau de bord");
  await expect(nav).toContainText("Projets");
  await expect(nav).toContainText("Explorer l'Afrique");
  await page.getByTestId("lang-en").click();
  await expect(nav).toContainText("Dashboard");

  // 8. optimizer demo comparison
  await page.goto("/app/optimizer");
  await expect(page.getByText(/SYNTHETIC DEMO DATA/)).toBeVisible();
  await page.getByTestId("compare-options").click();
  await expect(page.getByTestId("options-table")).toBeVisible();
  expect(await page.getByTestId("options-table").locator("tbody tr").count()).toBeGreaterThanOrEqual(3);
  await expect(page.getByTestId("optimizer-explanation")).not.toBeEmpty();

  // 9. explore: the map container renders and the page does not crash
  await page.goto("/app/explore");
  await expect(page.getByTestId("map-container")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Explore Africa" })).toBeVisible();
  await page.waitForTimeout(3000);
  await expect(page.getByRole("heading", { name: "Explore Africa" })).toBeVisible();

  // 10. country profile and admin 1 regions from the bundled public reference data (python -m app.ingest_public)
  await expect(page.getByTestId("platform-dataset-list")).toContainText("Natural Earth Admin 1");
  await page.getByTestId("country-select").selectOption({ label: "Kenya" });
  const profile = page.getByTestId("country-profile");
  await expect(profile).toContainText("Kenya");
  const api = await (await page.request.get("/api/countries/KEN/profile")).json();
  const access = api.indicators.find((i: { key: string }) => i.key === "access_to_electricity");
  const card = page.getByTestId("indicator-access_to_electricity");
  await expect(card).toContainText("Access to electricity (% of population)");
  await expect(card.getByTestId("indicator-year")).toHaveText(String(access.year));
  await expect(card).toContainText("CC-BY-4.0");
  await expect(page.getByTestId("indicator-renewables_share_elec")).toContainText("%");
  await expect(page.getByTestId("profile-sources")).toContainText("Natural Earth");
  await expect(page.getByTestId("admin1-status")).toContainText(`${api.admin1_count} regions`);
  await expect(page.getByTestId("boundary-status")).toContainText("Data unavailable: upload a district boundary dataset");
  await page.getByTestId("lang-fr").click();
  await expect(page.getByTestId("country-profile")).toContainText("Profil pays");
  await page.getByTestId("lang-en").click();
  expect(pageErrors, pageErrors.join("\n")).toEqual([]);
});
