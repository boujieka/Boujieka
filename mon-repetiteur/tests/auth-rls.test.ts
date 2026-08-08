import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests against the local Supabase stack (npm run db:start).
// Exercises real Postgres RLS policies and triggers from
// supabase/migrations/*_profiles.sql — the thing that actually enforces
// CLAUDE.md §12/§13, not just application code.
//
// Uses @supabase/supabase-js directly rather than lib/supabase/server.ts:
// that wrapper is bound to a Next.js request (next/headers cookies()) and
// can't run outside one.

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin" },
});

async function createSignedInUser(fullName: string) {
  const email = `${crypto.randomUUID()}@example.com`;
  const password = "correct horse battery staple";

  // Distinct storageKey per client: these all share one jsdom `window`, and
  // without it they'd collide on the same default auth storage key.
  const client: SupabaseClient<Database> = createClient(url, anonKey, {
    auth: { autoRefreshToken: false, persistSession: false, storageKey: `test-${email}` },
  });

  const { data, error } = await client.auth.signUp({
    email,
    password,
    options: { data: { full_name: fullName } },
  });
  if (error || !data.user) {
    throw new Error(`signUp failed: ${error?.message}`);
  }

  return { client, userId: data.user.id };
}

describe("profiles RLS", () => {
  let userA: { client: SupabaseClient<Database>; userId: string };
  let userB: { client: SupabaseClient<Database>; userId: string };

  beforeAll(async () => {
    userA = await createSignedInUser("Étudiant A");
    userB = await createSignedInUser("Étudiant B");
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(userA.userId);
    await admin.auth.admin.deleteUser(userB.userId);
  });

  it("auto-provisions a profile row on signup via the handle_new_user trigger", async () => {
    const { data, error } = await userA.client
      .from("profiles")
      .select("*")
      .eq("id", userA.userId)
      .single();

    expect(error).toBeNull();
    expect(data?.full_name).toBe("Étudiant A");
    expect(data?.role).toBe("student");
  });

  it("denies anonymous (unauthenticated) access to profiles entirely", async () => {
    const anon: SupabaseClient<Database> = createClient(url, anonKey, {
      auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-anon" },
    });

    const { data, error } = await anon.from("profiles").select("*");

    // No GRANT to `anon` at all (see migration) — this is a permission
    // error at the table-privilege layer, not just an RLS-filtered empty
    // result. Stricter than RLS alone: even a buggy policy couldn't leak
    // rows to an anonymous caller.
    expect(error?.code).toBe("42501");
    expect(data).toBeNull();
  });

  it("lets a user update their own full_name", async () => {
    const { error } = await userA.client
      .from("profiles")
      .update({ full_name: "Étudiant A (updated)" })
      .eq("id", userA.userId);
    expect(error).toBeNull();

    const { data } = await userA.client
      .from("profiles")
      .select("full_name")
      .eq("id", userA.userId)
      .single();
    expect(data?.full_name).toBe("Étudiant A (updated)");
  });

  it("hides other users' profile rows", async () => {
    const { data, error } = await userA.client
      .from("profiles")
      .select("*")
      .eq("id", userB.userId);

    expect(error).toBeNull();
    expect(data).toEqual([]);
  });

  it("prevents a user from escalating their own role", async () => {
    const { error: updateError } = await userA.client
      .from("profiles")
      .update({ role: "admin" })
      .eq("id", userA.userId);
    // The update itself is allowed by RLS (it's their own row); the
    // prevent_role_escalation trigger is what silently reverts `role`.
    expect(updateError).toBeNull();

    const { data } = await userA.client
      .from("profiles")
      .select("role")
      .eq("id", userA.userId)
      .single();
    expect(data?.role).toBe("student");
  });

  it("lets service_role change a user's role", async () => {
    const { error } = await admin
      .from("profiles")
      .update({ role: "admin" })
      .eq("id", userA.userId);
    expect(error).toBeNull();

    const { data } = await admin
      .from("profiles")
      .select("role")
      .eq("id", userA.userId)
      .single();
    expect(data?.role).toBe("admin");
  });
});
