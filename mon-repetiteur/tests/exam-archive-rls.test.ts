import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for supabase/migrations/*_exam_archive.sql: same
// publish-gate pattern as lessons/exercises (staff write, published-or-
// own-or-staff read).

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-exam-archive" },
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

describe("exam archive RLS", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let subjectId: string;
  let programId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant Archive");
    teacher = await createSignedInUser("Professeur Archive");
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
    programId = program!.id;
    subjectId = subject!.id;
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(teacher.userId);
  });

  it("lets any authenticated student see the published DEMO exam entries", async () => {
    const { data, error } = await student.client
      .from("exams")
      .select("title, status, rights_status")
      .eq("subject_id", subjectId);
    expect(error).toBeNull();
    expect(data?.length).toBeGreaterThan(0);
    for (const exam of data ?? []) {
      expect(exam.status).toBe("published");
      expect(exam.title).toContain("[DEMO]");
    }
  });

  it("blocks a student from creating an exam record", async () => {
    const { error } = await student.client.from("exams").insert({
      program_id: programId,
      subject_id: subjectId,
      year: 2024,
      title: "Unauthorized exam",
    });
    expect(error).not.toBeNull();
  });

  it("hides a draft exam from students but shows it to staff and its author", async () => {
    const { data: exam, error } = await teacher.client
      .from("exams")
      .insert({
        program_id: programId,
        subject_id: subjectId,
        year: 2024,
        title: `Test draft exam ${crypto.randomUUID()}`,
        created_by: teacher.userId,
      })
      .select()
      .single();
    expect(error).toBeNull();
    expect(exam?.status).toBe("draft");

    const { data: hidden } = await student.client
      .from("exams")
      .select("*")
      .eq("id", exam!.id);
    expect(hidden).toEqual([]);

    const { data: visibleToAuthor } = await teacher.client
      .from("exams")
      .select("*")
      .eq("id", exam!.id)
      .single();
    expect(visibleToAuthor?.id).toBe(exam!.id);

    await admin.from("exams").delete().eq("id", exam!.id);
  });
});
