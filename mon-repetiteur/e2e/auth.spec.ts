import { afterAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, loginViaUi, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): Registration + Login. Logout is covered
// as part of this same session rather than its own file — it's one
// short, linear story (register -> land on dashboard -> log out -> can't
// reach a protected page -> log back in).
//
// Note: this suite runs under plain Vitest (not @playwright/test), so
// assertions use vitest's own `expect` against plain awaited Playwright
// calls (page.textContent(), locator.isVisible()) rather than
// @playwright/test's locator-aware matchers (toHaveText, toBeVisible).

describe("registration and login", () => {
  const email = uniqueEmail("e2e-auth");

  afterAll(async () => {
    await deleteUserByEmail(email);
  });

  it("lets a new student sign up and land on the dashboard", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Auth Student", email });
    expect(await page.locator("h1").textContent()).toBe("Tableau de bord");
    expect(await page.getByText("E2E Auth Student").isVisible()).toBe(true);
    await context.close();
  });

  it("logs the student out and blocks access to protected pages until they log back in", async () => {
    const { context, page } = await newPage();
    await loginViaUi(page, { email });
    expect(await page.locator("h1").textContent()).toBe("Tableau de bord");

    await page.click('button:has-text("Se déconnecter")');
    await page.waitForURL((url) => url.pathname === "/" || url.pathname === "/login", {
      timeout: 10_000,
    });

    // Signed out: /account must redirect to /login, not render the dashboard.
    await page.goto(`${E2E_BASE_URL}/account`);
    await page.waitForURL(`${E2E_BASE_URL}/login`, { timeout: 10_000 });

    // Logging back in reaches the dashboard again.
    await loginViaUi(page, { email });
    expect(await page.locator("h1").textContent()).toBe("Tableau de bord");

    await context.close();
  });
});
