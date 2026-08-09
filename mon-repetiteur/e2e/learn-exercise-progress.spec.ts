import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, getAdminClient, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): Lesson -> Exercise -> Progress/Dashboard —
// the core LEARN -> PRACTICE -> DIAGNOSE loop from CLAUDE.md §2. Uses a
// dedicated throwaway skill/exercise (not seeded content another suite's
// test toggles the status of) so this can't race with `npm test`'s
// integration tests.

describe("learn -> exercise -> progress loop", () => {
  const email = uniqueEmail("e2e-learn");
  let skillId: string;

  beforeAll(async () => {
    const admin = getAdminClient();
    const { data: program } = await admin
      .from("programs")
      .select("id")
      .eq("code", "terminale_c")
      .single();
    const { data: cls } = await admin
      .from("classes")
      .select("id")
      .eq("program_id", program!.id)
      .eq("code", "terminale")
      .single();
    const { data: topic } = await admin
      .from("topics")
      .select("id")
      .eq("class_id", cls!.id)
      .limit(1)
      .single();
    const { data: skill, error: skillError } = await admin
      .from("skills")
      .insert({ topic_id: topic!.id, title: `E2E loop skill ${crypto.randomUUID()}` })
      .select()
      .single();
    if (skillError || !skill) throw skillError ?? new Error("skill insert failed");
    skillId = skill.id;

    const { error: exerciseError } = await admin.from("exercises").insert({
      skill_id: skillId,
      type: "true_false",
      prompt: "E2E test: 2 + 2 = 4.",
      content: { answer: true },
      status: "published",
    });
    if (exerciseError) throw exerciseError;
  });

  afterAll(async () => {
    const admin = getAdminClient();
    await admin.from("skills").delete().eq("id", skillId);
    await deleteUserByEmail(email);
  });

  it("shows the skill on /learn, lets the student practice it, and reflects the attempt on the dashboard", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Loop Student", email });

    await page.goto(`${E2E_BASE_URL}/learn`);
    const skillCard = page.locator("li").filter({ hasText: "E2E loop skill" });
    expect(await skillCard.isVisible()).toBe(true);

    // Next's <Link> does a client-side (History API) transition, not a
    // classic document navigation — page.waitForNavigation() doesn't
    // reliably observe it. click() + waitForURL() does.
    await skillCard.getByRole("link", { name: "S'entraîner" }).click();
    await page.waitForURL(`${E2E_BASE_URL}/practice/${skillId}`, { timeout: 10_000 });
    expect(new URL(page.url()).pathname).toBe(`/practice/${skillId}`);

    await page.locator('label:has-text("Vrai") input[type="radio"]').check();
    await page.click('button:has-text("Valider")');
    await page.waitForSelector('[role="status"]');
    expect(await page.locator('[role="status"]').textContent()).toContain("Correct");

    // Dashboard reflects it: stats increment, no longer "no activity".
    await page.goto(`${E2E_BASE_URL}/account`);
    const recentActivitySection = page.locator("section", { hasText: "Activité récente" });
    expect(await recentActivitySection.getByText("Aucune activité récente").count()).toBe(0);

    const attemptsValue = page
      .locator('p:has-text("Exercices tentés")')
      .locator("xpath=following-sibling::p");
    expect(await attemptsValue.textContent()).toBe("1");

    await context.close();
  });
});
