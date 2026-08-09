import { afterAll, describe, expect, it } from "vitest";
import { E2E_BASE_URL } from "./config";
import {
  deleteUserByEmail,
  newPage,
  promoteToTeacher,
  signUpViaUi,
  uniqueEmail,
} from "./browser";

// Critical authorization path (CLAUDE.md §13): the Admin CMS's
// server-side staff gate (src/app/admin/layout.tsx). RLS is the real
// backstop on every write regardless of this UI gate, but a regression
// here would still let a student reach staff-only *listings* — this is
// the one thing standing in the way of that, so it gets its own
// regression coverage rather than relying on the manual verification
// done when Phase 9 was built.

describe("Admin CMS authorization", () => {
  const studentEmail = uniqueEmail("e2e-admin-student");
  const teacherEmail = uniqueEmail("e2e-admin-teacher");

  afterAll(async () => {
    await deleteUserByEmail(studentEmail);
    await deleteUserByEmail(teacherEmail);
  });

  it("redirects a student away from /admin and hides the Administration entry point", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Admin Student", email: studentEmail });

    expect(await page.getByText("Administration").count()).toBe(0);

    await page.goto(`${E2E_BASE_URL}/admin`);
    await page.waitForURL(`${E2E_BASE_URL}/account`, { timeout: 10_000 });

    await context.close();
  });

  it("lets a teacher reach /admin and shows the Administration entry point", async () => {
    const { context, page } = await newPage();
    await signUpViaUi(page, { fullName: "E2E Admin Teacher", email: teacherEmail });
    await promoteToTeacher(teacherEmail);

    await page.goto(`${E2E_BASE_URL}/account`);
    expect(await page.getByText("Administration").isVisible()).toBe(true);

    await page.goto(`${E2E_BASE_URL}/admin`);
    expect(await page.locator("h1").textContent()).toBe("Administration");

    await context.close();
  });
});
