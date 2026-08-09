import { afterAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): Exam archive. Uses the seeded [DEMO]
// published exam (rights_status='unknown') rather than a throwaway
// fixture — the rights-gating behavior it proves (CLAUDE.md §15: no
// source link when rights are unresolved, only a label) is exactly what
// that seed row exists to demonstrate.

describe("exam archive", () => {
  const email = uniqueEmail("e2e-archive");

  afterAll(async () => {
    await deleteUserByEmail(email);
  });

  it("lists the published demo exam without exposing a source link (rights unresolved)", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Archive Student", email });

    await page.goto(`${E2E_BASE_URL}/archive`);
    const examCard = page.locator("li").filter({ hasText: "[DEMO]" });
    expect(await examCard.isVisible()).toBe(true);
    expect(await examCard.getByText("Droits non résolus").isVisible()).toBe(true);
    expect(await examCard.getByRole("link", { name: "Voir le sujet" }).count()).toBe(0);

    await context.close();
  });
});
