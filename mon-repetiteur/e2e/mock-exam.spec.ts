import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import { deleteUserByEmail, getAdminClient, newPage, signUpViaUi, uniqueEmail } from "./browser";

// Critical flow (CLAUDE.md §29): Mock exam — create, take, submit, see a
// score. Assumes a freshly-reset DB (no other exercise left published,
// see the "revert" step every other spec's afterAll performs) so the
// generated mock exam contains exactly this spec's one fixture question.

describe("mock exam", () => {
  const email = uniqueEmail("e2e-mock-exam");
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
      .insert({ topic_id: topic!.id, title: `E2E mock exam skill ${crypto.randomUUID()}` })
      .select()
      .single();
    if (skillError || !skill) throw skillError ?? new Error("skill insert failed");
    skillId = skill.id;

    const { error: exerciseError } = await admin.from("exercises").insert({
      skill_id: skillId,
      type: "true_false",
      prompt: "E2E mock exam test: 3 + 3 = 6.",
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

  it("creates a mock exam from published exercises, grades it on submit, and shows the score", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Mock Exam Student", email });

    await page.goto(`${E2E_BASE_URL}/learn`);
    // Server Action redirect() is a client-side (History API) transition
    // here — click() + waitForURL() observes it reliably; waitForURL()
    // alone won't work for the submit step below since it redirects to
    // the *same* URL (taking view -> results view), so that step instead
    // waits for the results-only DOM content to appear.
    await page.click('button:has-text("Examen blanc")');
    await page.waitForURL(/\/exam\//, { timeout: 10_000 });
    expect(new URL(page.url()).pathname).toMatch(/^\/exam\//);

    await page.locator('label:has-text("Vrai") input[type="radio"]').first().check();
    await page.click('button:has-text("Soumettre l\'examen")');
    await page.waitForSelector("p.text-5xl", { timeout: 10_000 });

    const scoreText = await page.locator("p.text-5xl").textContent();
    expect(scoreText).toBe("100%");
    expect(await page.getByText("Correct").first().isVisible()).toBe(true);

    await context.close();
  });
});
