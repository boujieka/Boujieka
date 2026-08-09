import { afterAll, beforeAll, describe, expect, it } from "vitest";
import type { BrowserContext, Page } from "playwright";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): Dashboard — PRD.md §7 item 8's entry
// points into the LEARN -> PRACTICE -> ... loop. Empty state for a
// brand-new student, and every quick-link actually navigates. One
// signed-up session reused across both assertions (tests in a describe
// block run sequentially by default) rather than a fresh user each time.

describe("dashboard", () => {
  const email = uniqueEmail("e2e-dashboard");
  let context: BrowserContext;
  let page: Page;

  beforeAll(async () => {
    ({ context, page } = await newPage());
    await signUpViaUi(page, { fullName: "E2E Dashboard Student", email });
  });

  afterAll(async () => {
    await context.close();
    await deleteUserByEmail(email);
  });

  it("shows an honest empty state for a brand-new student (no data invented)", async () => {
    expect(await page.getByText("Aucune compétence à renforcer identifiée").isVisible()).toBe(
      true,
    );
    expect(await page.getByText("Aucune activité récente").isVisible()).toBe(true);
    expect(await page.getByText("Exercices tentés").isVisible()).toBe(true);
  });

  it("every quick link navigates to its page", async () => {
    const links: Array<[string, string]> = [
      ["Voir le programme", "/learn"],
      ["Ma progression", "/progress"],
      ["Plan de révision", "/plan"],
      ["Archive des épreuves", "/archive"],
    ];

    for (const [label, path] of links) {
      await page.goto(`${E2E_BASE_URL}/account`);
      // Next's <Link> does a client-side (History API) transition, not a
      // classic document navigation — page.waitForNavigation() doesn't
      // reliably observe it. click() + waitForURL() does.
      await page.click(`a:has-text("${label}")`);
      await page.waitForURL(`${E2E_BASE_URL}${path}`, { timeout: 10_000 });
      expect(new URL(page.url()).pathname).toBe(path);
    }
  });
});
