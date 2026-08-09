import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for supabase/migrations/*_study_plans.sql: owner-scoped
// with a staff bypass (same reasoning as skill_progress/mock_exams — a
// teacher plausibly wants visibility into a student's revision plan).
// services/study-plan.ts's business logic (cancel-then-create, cascading
// plan completion) needs the Next-bound server-only Supabase client and
// can't run here directly — same constraint as progress.ts/mock-exam.ts
// (see progress-rls.test.ts) — so this exercises the underlying RLS/data
// shape those functions depend on.

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-study-plan" },
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

describe("study_plans / study_sessions RLS", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let otherStudent: { client: SupabaseClient<Database>; userId: string };
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let skillId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant Plan");
    otherStudent = await createSignedInUser("Autre Étudiant Plan");
    teacher = await createSignedInUser("Professeur Plan");
    await admin.from("profiles").update({ role: "teacher" }).eq("id", teacher.userId);

    const { data: skill } = await admin
      .from("skills")
      .select("id")
      .eq("title", "Limites et continuité")
      .single();
    skillId = skill!.id;
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(otherStudent.userId);
    await admin.auth.admin.deleteUser(teacher.userId);
  });

  it("lets a student create their own plan + sessions, hides them from other students, but not staff", async () => {
    const { data: plan, error: planError } = await student.client
      .from("study_plans")
      .insert({ profile_id: student.userId })
      .select()
      .single();
    expect(planError).toBeNull();
    expect(plan?.status).toBe("active");

    const { data: session, error: sessionError } = await student.client
      .from("study_sessions")
      .insert({
        study_plan_id: plan!.id,
        skill_id: skillId,
        order: 0,
        scheduled_for: new Date().toISOString().slice(0, 10),
      })
      .select()
      .single();
    expect(sessionError).toBeNull();
    expect(session?.completed_at).toBeNull();

    const { data: hiddenPlan } = await otherStudent.client
      .from("study_plans")
      .select("*")
      .eq("id", plan!.id);
    expect(hiddenPlan).toEqual([]);
    const { data: hiddenSession } = await otherStudent.client
      .from("study_sessions")
      .select("*")
      .eq("id", session!.id);
    expect(hiddenSession).toEqual([]);

    const { data: visibleToStaff } = await teacher.client
      .from("study_plans")
      .select("*")
      .eq("id", plan!.id)
      .single();
    expect(visibleToStaff?.id).toBe(plan!.id);
  });

  it("blocks creating a plan under another student's profile_id", async () => {
    const { error } = await student.client
      .from("study_plans")
      .insert({ profile_id: otherStudent.userId });
    expect(error).not.toBeNull();
  });

  it("lets the owning student mark their own session complete, but not another student", async () => {
    const { data: plan } = await student.client
      .from("study_plans")
      .insert({ profile_id: student.userId })
      .select()
      .single();
    const { data: session } = await student.client
      .from("study_sessions")
      .insert({
        study_plan_id: plan!.id,
        skill_id: skillId,
        order: 0,
        scheduled_for: new Date().toISOString().slice(0, 10),
      })
      .select()
      .single();

    const { data: deniedUpdate } = await otherStudent.client
      .from("study_sessions")
      .update({ completed_at: new Date().toISOString() })
      .eq("id", session!.id)
      .select();
    expect(deniedUpdate).toEqual([]);

    const { data: ownUpdate, error: ownUpdateError } = await student.client
      .from("study_sessions")
      .update({ completed_at: new Date().toISOString() })
      .eq("id", session!.id)
      .select()
      .single();
    expect(ownUpdateError).toBeNull();
    expect(ownUpdate?.completed_at).not.toBeNull();
  });
});
