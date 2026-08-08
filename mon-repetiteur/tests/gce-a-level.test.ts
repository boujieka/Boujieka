import { describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Data-integrity checks for the GCE A-Level seed content
// (supabase/seed.sql) — RLS mechanics for curriculum tables are already
// covered by curriculum-rls.test.ts using Terminale C; this instead
// verifies the two programs' content is real, complete, and genuinely
// isolated from each other (not, say, accidentally sharing a subject
// row via a slug collision).

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-gce" },
});

describe("GCE A-Level seed content", () => {
  it("exists as a program distinct from Terminale C", async () => {
    const { data: programs } = await admin
      .from("programs")
      .select("code, name, language")
      .order("code");
    expect(programs).toEqual([
      { code: "gce_a_level", name: "GCE Advanced Level", language: "en" },
      { code: "terminale_c", name: "Terminale C", language: "fr" },
    ]);
  });

  it("has its own Mathematics subject, not shared with Terminale C's Mathématiques", async () => {
    const { data: program } = await admin
      .from("programs")
      .select("id")
      .eq("code", "gce_a_level")
      .single();

    const { data: subjects } = await admin
      .from("subjects")
      .select("slug, name")
      .eq("program_id", program!.id);

    expect(subjects).toEqual([{ slug: "mathematics", name: "Mathematics" }]);
  });

  it("has two topics, six skills, and six draft exercises under its own class levels", async () => {
    const { data: program } = await admin
      .from("programs")
      .select("id")
      .eq("code", "gce_a_level")
      .single();
    const { data: subject } = await admin
      .from("subjects")
      .select("id")
      .eq("program_id", program!.id)
      .eq("slug", "mathematics")
      .single();
    const { data: upperSixth } = await admin
      .from("classes")
      .select("id")
      .eq("program_id", program!.id)
      .eq("code", "upper_sixth")
      .single();

    const { data: topics } = await admin
      .from("topics")
      .select("id, title")
      .eq("subject_id", subject!.id)
      .eq("class_id", upperSixth!.id);
    expect(topics?.map((t) => t.title).sort()).toEqual(["Algebra and Functions", "Statistics"]);

    const topicIds = topics!.map((t) => t.id);
    const { data: skills } = await admin.from("skills").select("id").in("topic_id", topicIds);
    expect(skills).toHaveLength(6);

    const { data: exercises } = await admin
      .from("exercises")
      .select("status")
      .in(
        "skill_id",
        skills!.map((s) => s.id),
      );
    expect(exercises).toHaveLength(6);
    expect(exercises?.every((e) => e.status === "draft")).toBe(true);
  });

  it("does not leak into Terminale C's subject/topic listing", async () => {
    const { data: terminaleC } = await admin
      .from("programs")
      .select("id")
      .eq("code", "terminale_c")
      .single();

    const { data: subjects } = await admin
      .from("subjects")
      .select("slug")
      .eq("program_id", terminaleC!.id);
    expect(subjects?.map((s) => s.slug)).toEqual(["mathematiques"]);
    expect(subjects?.some((s) => s.slug === "mathematics")).toBe(false);
  });
});
