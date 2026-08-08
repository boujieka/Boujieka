import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests against the local Supabase stack for
// supabase/migrations/*_curriculum.sql: structural tables (programs/
// classes/subjects/topics/skills) are staff-writable but readable by any
// authenticated user; lessons add a publish gate on top.

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-curriculum" },
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

describe("curriculum RLS", () => {
  let student: { client: SupabaseClient<Database>; userId: string };
  let teacher: { client: SupabaseClient<Database>; userId: string };
  let programId: string;

  beforeAll(async () => {
    student = await createSignedInUser("Étudiant");
    teacher = await createSignedInUser("Professeur");

    const { error: promoteError } = await admin
      .from("profiles")
      .update({ role: "teacher" })
      .eq("id", teacher.userId);
    if (promoteError) throw promoteError;

    const { data: program, error: programError } = await admin
      .from("programs")
      .select("id")
      .eq("code", "terminale_c")
      .single();
    if (programError || !program) throw programError ?? new Error("terminale_c program missing");
    programId = program.id;
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(student.userId);
    await admin.auth.admin.deleteUser(teacher.userId);
  });

  it("lets any authenticated user read the seeded programs", async () => {
    const { data, error } = await student.client.from("programs").select("code");
    expect(error).toBeNull();
    expect(data?.map((p) => p.code)).toEqual(
      expect.arrayContaining(["terminale_c", "gce_a_level"]),
    );
  });

  it("blocks a student from writing to structural curriculum tables", async () => {
    const { error } = await student.client
      .from("subjects")
      .insert({ program_id: programId, slug: "test-subject", name: "Test" });
    expect(error).not.toBeNull();
  });

  it("lets a teacher create the curriculum tree, and a student read it once created", async () => {
    const { data: subject, error: subjectError } = await teacher.client
      .from("subjects")
      .insert({ program_id: programId, slug: `test-${crypto.randomUUID()}`, name: "Test Maths" })
      .select()
      .single();
    expect(subjectError).toBeNull();
    expect(subject).not.toBeNull();

    const { data: readBack, error: readError } = await student.client
      .from("subjects")
      .select("*")
      .eq("id", subject!.id)
      .single();
    expect(readError).toBeNull();
    expect(readBack?.name).toBe("Test Maths");

    // cleanup
    await admin.from("subjects").delete().eq("id", subject!.id);
  });

  it("hides a draft lesson from other students but shows it to its author and to staff", async () => {
    const { data: cls } = await admin
      .from("classes")
      .select("id")
      .eq("program_id", programId)
      .eq("code", "terminale")
      .single();
    const { data: subject } = await teacher.client
      .from("subjects")
      .insert({ program_id: programId, slug: `test-${crypto.randomUUID()}`, name: "Test Subject" })
      .select()
      .single();
    const { data: topic } = await teacher.client
      .from("topics")
      .insert({ subject_id: subject!.id, class_id: cls!.id, title: "Test topic" })
      .select()
      .single();
    const { data: skill } = await teacher.client
      .from("skills")
      .insert({ topic_id: topic!.id, title: "Test skill" })
      .select()
      .single();
    const { data: lesson, error: lessonError } = await teacher.client
      .from("lessons")
      .insert({
        skill_id: skill!.id,
        title: "Test lesson",
        content: "placeholder",
        created_by: teacher.userId,
      })
      .select()
      .single();
    expect(lessonError).toBeNull();
    expect(lesson?.status).toBe("draft");

    // Student can't see the draft lesson.
    const { data: hiddenFromStudent } = await student.client
      .from("lessons")
      .select("*")
      .eq("id", lesson!.id);
    expect(hiddenFromStudent).toEqual([]);

    // The teacher who authored it can see it.
    const { data: visibleToAuthor } = await teacher.client
      .from("lessons")
      .select("*")
      .eq("id", lesson!.id)
      .single();
    expect(visibleToAuthor?.id).toBe(lesson!.id);

    // Once published, the student can see it too.
    await admin.from("lessons").update({ status: "published" }).eq("id", lesson!.id);
    const { data: visibleAfterPublish } = await student.client
      .from("lessons")
      .select("*")
      .eq("id", lesson!.id)
      .single();
    expect(visibleAfterPublish?.status).toBe("published");

    // cleanup (cascades: subject -> topic -> skill -> lesson)
    await admin.from("subjects").delete().eq("id", subject!.id);
  });
});
