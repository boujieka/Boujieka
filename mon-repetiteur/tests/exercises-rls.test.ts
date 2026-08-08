import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests against the local Supabase stack for
// supabase/migrations/*_exercises.sql: exercises follow the same
// publish-gate pattern as lessons; attempts are owner-scoped and
// immutable once written.

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-exercises" },
});

async function createSignedInUser(fullName: string) {
  const email = `${crypto.randomUUID()}@example.com`;
  const password = "correct horse battery staple";

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

describe("exercises & attempts RLS", () => {
  let studentA: { client: SupabaseClient<Database>; userId: string };
  let studentB: { client: SupabaseClient<Database>; userId: string };
  let skillId: string;

  beforeAll(async () => {
    studentA = await createSignedInUser("Étudiant A");
    studentB = await createSignedInUser("Étudiant B");

    const { data: skill, error } = await admin
      .from("skills")
      .select("id")
      .eq("title", "Vocabulaire des probabilités")
      .single();
    if (error || !skill) throw error ?? new Error("seeded skill missing");
    skillId = skill.id;
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(studentA.userId);
    await admin.auth.admin.deleteUser(studentB.userId);
  });

  it("hides draft exercises from students, shows them once published", async () => {
    const { data: exercise } = await admin
      .from("exercises")
      .select("*")
      .eq("skill_id", skillId)
      .single();
    expect(exercise?.status).toBe("draft");

    const { data: hidden } = await studentA.client
      .from("exercises")
      .select("*")
      .eq("id", exercise!.id);
    expect(hidden).toEqual([]);

    await admin.from("exercises").update({ status: "published" }).eq("id", exercise!.id);

    const { data: visible } = await studentA.client
      .from("exercises")
      .select("*")
      .eq("id", exercise!.id)
      .single();
    expect(visible?.status).toBe("published");

    // revert for other tests / re-runs
    await admin.from("exercises").update({ status: "draft" }).eq("id", exercise!.id);
  });

  it("blocks a student from creating or editing exercises", async () => {
    const { error: insertError } = await studentA.client.from("exercises").insert({
      skill_id: skillId,
      type: "true_false",
      prompt: "test",
      content: { answer: true },
    });
    expect(insertError).not.toBeNull();
  });

  it("lets a student record an attempt on a published exercise, scoped to themself", async () => {
    const { data: exercise } = await admin
      .from("exercises")
      .select("*")
      .eq("skill_id", skillId)
      .single();
    await admin.from("exercises").update({ status: "published" }).eq("id", exercise!.id);

    const { data: attempt, error } = await studentA.client
      .from("attempts")
      .insert({
        profile_id: studentA.userId,
        attemptable_type: "exercise",
        attemptable_id: exercise!.id,
        answer: 1,
        is_correct: true,
        score: 1,
      })
      .select()
      .single();
    expect(error).toBeNull();
    expect(attempt?.profile_id).toBe(studentA.userId);

    // Student B can't see student A's attempt.
    const { data: hiddenFromB } = await studentB.client
      .from("attempts")
      .select("*")
      .eq("id", attempt!.id);
    expect(hiddenFromB).toEqual([]);

    // Attempts are immutable: no update policy for authenticated.
    const { error: updateError } = await studentA.client
      .from("attempts")
      .update({ is_correct: false })
      .eq("id", attempt!.id);
    expect(updateError).not.toBeNull();

    await admin.from("exercises").update({ status: "draft" }).eq("id", exercise!.id);
  });

  it("blocks a student from inserting an attempt on another student's behalf", async () => {
    const { data: exercise } = await admin
      .from("exercises")
      .select("*")
      .eq("skill_id", skillId)
      .single();

    const { error } = await studentA.client.from("attempts").insert({
      profile_id: studentB.userId,
      attemptable_type: "exercise",
      attemptable_id: exercise!.id,
      answer: 0,
      is_correct: false,
      score: 0,
    });
    expect(error).not.toBeNull();
  });
});
