import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for supabase/migrations/*_skill_progress.sql: the
// update_skill_progress trigger, and skill_progress's RLS (own rows, or
// staff).

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-progress" },
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

describe("skill_progress", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let otherStudent: { client: SupabaseClient<Database>; userId: string };
  let exerciseId: string;
  let skillId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant Progress");
    teacher = await createSignedInUser("Professeur Progress");
    otherStudent = await createSignedInUser("Autre Étudiant");

    await admin.from("profiles").update({ role: "teacher" }).eq("id", teacher.userId);

    const { data: exercise, error } = await admin
      .from("exercises")
      .select("id, skill_id")
      .eq(
        "skill_id",
        (
          await admin
            .from("skills")
            .select("id")
            .eq("title", "Limites et continuité")
            .single()
        ).data!.id,
      )
      .single();
    if (error || !exercise) throw error ?? new Error("seeded exercise missing");
    exerciseId = exercise.id;
    skillId = exercise.skill_id;
    await admin.from("exercises").update({ status: "published" }).eq("id", exerciseId);
  });

  afterAll(async () => {
    await admin.from("exercises").update({ status: "draft" }).eq("id", exerciseId);
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(teacher.userId);
    await admin.auth.admin.deleteUser(otherStudent.userId);
  });

  it("computes mastery_score from attempts via the trigger, through real RLS-scoped inserts", async () => {
    // true_false exercise, correct answer is true (seeded).
    await student.client.from("attempts").insert({
      profile_id: student.userId,
      attemptable_type: "exercise",
      attemptable_id: exerciseId,
      answer: true,
      is_correct: true,
      score: 1,
    });
    await student.client.from("attempts").insert({
      profile_id: student.userId,
      attemptable_type: "exercise",
      attemptable_id: exerciseId,
      answer: false,
      is_correct: false,
      score: 0,
    });

    const { data, error } = await student.client
      .from("skill_progress")
      .select("*")
      .eq("skill_id", skillId)
      .single();
    expect(error).toBeNull();
    expect(data?.mastery_score).toBeCloseTo(0.5);
  });

  it("hides one student's progress from another student, but not from staff", async () => {
    const { data: hiddenFromOther } = await otherStudent.client
      .from("skill_progress")
      .select("*")
      .eq("profile_id", student.userId);
    expect(hiddenFromOther).toEqual([]);

    const { data: visibleToStaff } = await teacher.client
      .from("skill_progress")
      .select("*")
      .eq("profile_id", student.userId)
      .eq("skill_id", skillId)
      .single();
    expect(visibleToStaff?.mastery_score).toBeCloseTo(0.5);
  });
});
