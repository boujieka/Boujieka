import { chromium, type Browser, type BrowserContext, type Page } from "playwright";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";
import { CHROMIUM_EXECUTABLE_PATH, E2E_BASE_URL, TEST_PASSWORD } from "./config";

// A single shared browser instance across every spec file in the suite
// (launching Chromium repeatedly is the slow part) — each test still
// gets its own isolated BrowserContext (so cookies/storage never leak
// between tests), just not its own browser process.
let browserPromise: Promise<Browser> | null = null;

export function getBrowser(): Promise<Browser> {
  if (!browserPromise) {
    browserPromise = chromium.launch({
      headless: true,
      executablePath: CHROMIUM_EXECUTABLE_PATH,
    });
  }
  return browserPromise;
}

export async function closeBrowser(): Promise<void> {
  if (browserPromise) {
    const browser = await browserPromise;
    await browser.close();
    browserPromise = null;
  }
}

export async function newPage(
  viewport: { width: number; height: number } = { width: 390, height: 844 },
): Promise<{ context: BrowserContext; page: Page }> {
  const browser = await getBrowser();
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  return { context, page };
}

// ---------------------------------------------------------------------------
// Admin (service_role) helpers — for out-of-band fixture setup (promoting a
// role, direct DB assertions) the UI has no path for. Same client shape as
// tests/*.test.ts's integration tests.
// ---------------------------------------------------------------------------

export function getAdminClient(): SupabaseClient<Database> {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  return createClient(url, serviceRoleKey, {
    auth: { autoRefreshToken: false, persistSession: false, storageKey: "e2e-admin" },
  });
}

export async function promoteToTeacher(email: string): Promise<void> {
  const admin = getAdminClient();
  const { data, error } = await admin.auth.admin.listUsers();
  if (error) throw error;
  const user = data.users.find((u) => u.email === email);
  if (!user) throw new Error(`promoteToTeacher: no such user ${email}`);
  const { error: updateError } = await admin
    .from("profiles")
    .update({ role: "teacher" })
    .eq("id", user.id);
  if (updateError) throw updateError;
}

export async function deleteUserByEmail(email: string): Promise<void> {
  const admin = getAdminClient();
  const { data, error } = await admin.auth.admin.listUsers();
  if (error) throw error;
  const user = data.users.find((u) => u.email === email);
  if (user) {
    await admin.auth.admin.deleteUser(user.id);
  }
}

// ---------------------------------------------------------------------------
// Real-UI flows shared across specs
// ---------------------------------------------------------------------------

export function uniqueEmail(prefix: string): string {
  return `${prefix}-${crypto.randomUUID()}@example.com`;
}

export async function signUpViaUi(
  page: Page,
  opts: { fullName: string; email: string },
): Promise<void> {
  await page.goto(`${E2E_BASE_URL}/signup`);
  await page.fill('input[name="fullName"]', opts.fullName);
  await page.fill('input[name="email"]', opts.email);
  await page.fill('input[name="password"]', TEST_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL(`${E2E_BASE_URL}/account`, { timeout: 10_000 });
}

export async function loginViaUi(
  page: Page,
  opts: { email: string; password?: string },
): Promise<void> {
  await page.goto(`${E2E_BASE_URL}/login`);
  await page.fill('input[name="email"]', opts.email);
  await page.fill('input[name="password"]', opts.password ?? TEST_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL(`${E2E_BASE_URL}/account`, { timeout: 10_000 });
}
