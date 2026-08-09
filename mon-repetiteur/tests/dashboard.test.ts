import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for the query semantics services/dashboard.ts relies
// on (it uses the Next-bound server-only Supabase client, which can't run
// outside a request scope in tests — same constraint as progress.ts/
// mock-exam.ts, see tests/progress-rls.test.ts). Exercised here directly
// against real RLS with a plain @supabase/supabase-js client instead.

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-dashboard" },
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

describe("dashboard aggregation queries", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let otherStudent: { client: SupabaseClient<Database>; userId: string };
  let exerciseId: string;
  let skillId: string;
  let subjectId: string;
  let classId: string;
  let mockExamId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant Dashboard");
    otherStudent = await createSignedInUser("Autre Étudiant Dashboard");

    const { data: exercise, error } = await admin
      .from("exercises")
      .select("id, skill_id, skills(topic_id, topics(subject_id, class_id))")
      .eq(
        "skill_id",
        (
          await admin.from("skills").select("id").eq("title", "Limites et continuité").single()
        ).data!.id,
      )
      .single();
    if (error || !exercise) throw error ?? new Error("seeded exercise missing");
    exerciseId = exercise.id;
    skillId = exercise.skill_id;
    subjectId = exercise.skills!.topics!.subject_id;
    classId = exercise.skills!.topics!.class_id;
    await admin.from("exercises").update({ status: "published" }).eq("id", exerciseId);

    const { data: mockExam, error: mockExamError } = await admin
      .from("mock_exams")
      .insert({ profile_id: student.userId, subject_id: subjectId, class_id: classId })
      .select()
      .single();
    if (mockExamError || !mockExam) throw mockExamError ?? new Error("mock exam insert failed");
    mockExamId = mockExam.id;

    await student.client.from("attempts").insert({
      profile_id: student.userId,
      attemptable_type: "exercise",
      attemptable_id: exerciseId,
      answer: true,
      is_correct: true,
      score: 1,
    });
  });

  afterAll(async () => {
    await admin.from("mock_exams").delete().eq("id", mockExamId);
    await admin.from("exercises").update({ status: "draft" }).eq("id", exerciseId);
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(otherStudent.userId);
  });

  it("resolves recent activity via the two-step attempts -> exercises(skills(topics)) join, scoped to the caller", async () => {
    const { data: attempts, error: attemptsError } = await student.client
      .from("attempts")
      .select("id, attemptable_id, is_correct, attempted_at")
      .eq("profile_id", student.userId)
      .eq("attemptable_type", "exercise")
      .order("attempted_at", { ascending: false })
      .limit(5);
    expect(attemptsError).toBeNull();
    expect(attempts).toHaveLength(1);

    const { data: exercises, error: exercisesError } = await student.client
      .from("exercises")
      .select("id, skill_id, skills(title, topics(title))")
      .in("id", [exerciseId]);
    expect(exercisesError).toBeNull();
    expect(exercises?.[0]?.skill_id).toBe(skillId);
    expect(exercises?.[0]?.skills?.title).toBe("Limites et continuité");
    expect(exercises?.[0]?.skills?.topics?.title).toBeTruthy();

    // Another student's client sees none of this student's attempts (RLS).
    const { data: hiddenFromOther } = await otherStudent.client
      .from("attempts")
      .select("id")
      .eq("profile_id", student.userId);
    expect(hiddenFromOther).toEqual([]);
  });

  it("finds the caller's in_progress mock exam and excludes submitted ones", async () => {
    const { data: active, error } = await student.client
      .from("mock_exams")
      .select("*")
      .eq("profile_id", student.userId)
      .eq("status", "in_progress")
      .order("started_at", { ascending: false })
      .limit(1)
      .maybeSingle();
    expect(error).toBeNull();
    expect(active?.id).toBe(mockExamId);

    await admin
      .from("mock_exams")
      .update({ status: "submitted", score: 1, submitted_at: new Date().toISOString() })
      .eq("id", mockExamId);

    const { data: noneActive } = await student.client
      .from("mock_exams")
      .select("*")
      .eq("profile_id", student.userId)
      .eq("status", "in_progress")
      .order("started_at", { ascending: false })
      .limit(1)
      .maybeSingle();
    expect(noneActive).toBeNull();

    // Reset back to in_progress so afterAll's cleanup path stays uniform
    // regardless of test order.
    await admin
      .from("mock_exams")
      .update({ status: "in_progress", score: null, submitted_at: null })
      .eq("id", mockExamId);
  });

  it("counts the caller's total attempts", async () => {
    const { count, error } = await student.client
      .from("attempts")
      .select("id", { count: "exact", head: true })
      .eq("profile_id", student.userId);
    expect(error).toBeNull();
    expect(count).toBe(1);
  });
});
