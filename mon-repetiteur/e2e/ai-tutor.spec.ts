import { afterAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): AI Tutor. This environment has no
// ANTHROPIC_API_KEY configured, so the honest, correct behavior to
// assert is the "not configured" state (CLAUDE.md §41: never claim a
// working AI response wasn't actually exercised) — not a live model
// reply. The exam-mode gate (CLAUDE.md §22) that disables the Tutor
// during a mock exam is covered at the data layer by
// tests/ai-tutor-rls.test.ts, since observing it here would also
// require a real provider call to distinguish "blocked" from "would
// have replied anyway".

describe("AI tutor", () => {
  const email = uniqueEmail("e2e-tutor");

  afterAll(async () => {
    await deleteUserByEmail(email);
  });

  it("is reachable from a skill's Aide action and honestly reports it isn't configured here", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Tutor Student", email });

    await page.goto(`${E2E_BASE_URL}/learn`);
    // Playwright auto-scrolls the target into view and waits for it to be
    // actionable, so the first match is enough even off-screen. The
    // button submits a Server Action whose redirect() is a client-side
    // (History API) transition, not a classic document navigation —
    // page.waitForNavigation() doesn't reliably observe it, so click()
    // + waitForURL() instead.
    await page.locator('button:has-text("Aide")').first().click();
    await page.waitForURL(/\/tutor\//, { timeout: 10_000 });
    expect(new URL(page.url()).pathname).toMatch(/^\/tutor\//);
    expect(await page.locator("h1").textContent()).toBe("Tuteur IA");
    expect(
      await page.getByText("Le tuteur IA n'est pas encore configuré").isVisible(),
    ).toBe(true);

    await context.close();
  });
});
