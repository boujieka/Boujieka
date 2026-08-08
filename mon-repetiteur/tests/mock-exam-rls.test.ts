import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for supabase/migrations/*_mock_exams.sql: owner-scoped
// with a staff bypass (unlike AI Tutor's private-only conversations —
// mock exam results are more like graded assessment data, same reasoning
// as skill_progress).

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-mock-exam" },
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

describe("mock_exams RLS", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let otherStudent: { client: SupabaseClient<Database>; userId: string };
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let subjectId: string;
  let classId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant Exam");
    otherStudent = await createSignedInUser("Autre Étudiant Exam");
    teacher = await createSignedInUser("Professeur Exam");
    await admin.from("profiles").update({ role: "teacher" }).eq("id", teacher.userId);

    const { data: program } = await admin
      .from("programs")
      .select("id")
      .eq("code", "terminale_c")
      .single();
    const { data: subject } = await admin
      .from("subjects")
      .select("id")
      .eq("program_id", program!.id)
      .eq("slug", "mathematiques")
      .single();
    const { data: cls } = await admin
      .from("classes")
      .select("id")
      .eq("program_id", program!.id)
      .eq("code", "terminale")
      .single();
    subjectId = subject!.id;
    classId = cls!.id;
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(otherStudent.userId);
    await admin.auth.admin.deleteUser(teacher.userId);
  });

  it("lets a student create their own mock exam and hides it from other students", async () => {
    const { data: mockExam, error } = await student.client
      .from("mock_exams")
      .insert({ profile_id: student.userId, subject_id: subjectId, class_id: classId })
      .select()
      .single();
    expect(error).toBeNull();
    expect(mockExam?.status).toBe("in_progress");

    const { data: hidden } = await otherStudent.client
      .from("mock_exams")
      .select("*")
      .eq("id", mockExam!.id);
    expect(hidden).toEqual([]);

    const { data: visibleToStaff } = await teacher.client
      .from("mock_exams")
      .select("*")
      .eq("id", mockExam!.id)
      .single();
    expect(visibleToStaff?.id).toBe(mockExam!.id);

    // Don't leave an in_progress exam behind for the exam-mode test below
    // to trip over.
    await admin.from("mock_exams").delete().eq("id", mockExam!.id);
  });

  it("blocks creating a mock exam under another student's profile_id", async () => {
    const { error } = await student.client
      .from("mock_exams")
      .insert({ profile_id: otherStudent.userId, subject_id: subjectId, class_id: classId });
    expect(error).not.toBeNull();
  });

  it("counts as exam-mode-active while in_progress, and stops after submission", async () => {
    // Mirrors the query isExamModeActive() runs — verifies the underlying
    // data/RLS shape it depends on, since the function itself needs a
    // live Next.js request scope this test doesn't have.
    const { data: mockExam } = await student.client
      .from("mock_exams")
      .insert({ profile_id: student.userId, subject_id: subjectId, class_id: classId })
      .select()
      .single();

    const activeCount = await student.client
      .from("mock_exams")
      .select("id", { count: "exact", head: true })
      .eq("profile_id", student.userId)
      .eq("status", "in_progress");
    expect(activeCount.count).toBeGreaterThan(0);

    await student.client
      .from("mock_exams")
      .update({ status: "submitted", score: 1, submitted_at: new Date().toISOString() })
      .eq("id", mockExam!.id);

    const afterSubmit = await student.client
      .from("mock_exams")
      .select("id", { count: "exact", head: true })
      .eq("profile_id", student.userId)
      .eq("status", "in_progress");
    expect(afterSubmit.count).toBe(0);
  });
});
