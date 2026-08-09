import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests filling a real gap: curriculum-rls.test.ts and
// exam-archive-rls.test.ts already exercise a signed-in teacher session
// creating lessons/exams via the exercises_insert_staff-style RLS
// policies, but exercises-rls.test.ts never did the same for exercises —
// only the "student is blocked" half was covered. services/admin.ts's
// createExercise()/setExerciseStatus() (used by the Admin CMS, Phase 9)
// depend on exactly this working for a real teacher session, not just
// service_role. (Can't call the service functions directly — server-only
// Supabase client needs a Next request scope, same constraint noted in
// dashboard.test.ts/study-plan-rls.test.ts.)

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-cms" },
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

describe("Admin CMS RLS (exercises)", () => {
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let student: { client: SupabaseClient<Database>; userId: string };
  let skillId: string;
  let exerciseId: string;

  beforeAll(async () => {
    teacher = await createSignedInUser("Professeur Admin");
    student = await createSignedInUser("Étudiant Admin");
    await admin.from("profiles").update({ role: "teacher" }).eq("id", teacher.userId);

    // A dedicated throwaway skill, not a seeded one another test file
    // owns — exercises-rls.test.ts's queries assume exactly one exercise
    // per its seeded skill_id (.single()), and tests run in parallel
    // against the same database, so reusing that skill here would race
    // with it (this broke it once already — see git history).
    const { data: topic, error: topicError } = await admin
      .from("topics")
      .select("id")
      .limit(1)
      .single();
    if (topicError || !topic) throw topicError ?? new Error("no seeded topic to attach to");
    const { data: skill, error: skillError } = await admin
      .from("skills")
      .insert({ topic_id: topic.id, title: `Admin CMS test skill ${crypto.randomUUID()}` })
      .select()
      .single();
    if (skillError || !skill) throw skillError ?? new Error("test skill insert failed");
    skillId = skill.id;
  });

  afterAll(async () => {
    // Cascades to the exercise too (exercises.skill_id -> skills.id on delete cascade).
    await admin.from("skills").delete().eq("id", skillId);
    await admin.auth.admin.deleteUser(teacher.userId);
    await admin.auth.admin.deleteUser(student.userId);
  });

  it("lets a real teacher session create an exercise as a draft (is_staff() RLS, not just service_role)", async () => {
    const { data: exercise, error } = await teacher.client
      .from("exercises")
      .insert({
        skill_id: skillId,
        type: "true_false",
        prompt: `Admin CMS test exercise ${crypto.randomUUID()}`,
        content: { answer: true },
        created_by: teacher.userId,
      })
      .select()
      .single();
    expect(error).toBeNull();
    expect(exercise?.status).toBe("draft");
    exerciseId = exercise!.id;
  });

  it("blocks the same insert from a student session", async () => {
    const { error } = await student.client.from("exercises").insert({
      skill_id: skillId,
      type: "true_false",
      prompt: `Blocked test exercise ${crypto.randomUUID()}`,
      content: { answer: true },
    });
    expect(error).not.toBeNull();
  });

  it("lets a teacher advance the exercise through the full content lifecycle, and blocks a student from doing the same", async () => {
    for (const status of ["under_review", "validated", "published"] as const) {
      const { data, error } = await teacher.client
        .from("exercises")
        .update({ status })
        .eq("id", exerciseId)
        .select()
        .single();
      expect(error).toBeNull();
      expect(data?.status).toBe(status);
    }

    // RLS's UPDATE policy filters via USING, so a blocked update isn't a
    // Postgres error — it's a successful update of zero rows (the row is
    // invisible to the policy, not "rejected"). .select() surfaces that
    // as an empty result, same pattern as study-plan-rls.test.ts.
    const { data: blockedUpdate } = await student.client
      .from("exercises")
      .update({ status: "archived" })
      .eq("id", exerciseId)
      .select();
    expect(blockedUpdate).toEqual([]);

    // Published, so a student can now read it — proves the lifecycle
    // advance actually changed what's visible, not just the row's value.
    const { data: visible } = await student.client
      .from("exercises")
      .select("*")
      .eq("id", exerciseId)
      .single();
    expect(visible?.status).toBe("published");
  });
});
