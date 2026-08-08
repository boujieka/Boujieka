import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "@/lib/supabase/database.types";

// Integration tests for supabase/migrations/*_ai_tutor.sql: conversations
// and messages are private to their owner — no staff bypass, unlike
// lessons/exercises/skill_progress (see the migration's comment on why).

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const admin: SupabaseClient<Database> = createClient(url, serviceRoleKey, {
  auth: { autoRefreshToken: false, persistSession: false, storageKey: "test-admin-ai" },
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

describe("AI Tutor RLS", () => {
  let studentA: { client: SupabaseClient<Database>; userId: string };
  let studentB: { client: SupabaseClient<Database>; userId: string };

  beforeAll(async () => {
    studentA = await createSignedInUser("Étudiant Tuteur A");
    studentB = await createSignedInUser("Étudiant Tuteur B");
  });

  afterAll(async () => {
    await admin.auth.admin.deleteUser(studentA.userId);
    await admin.auth.admin.deleteUser(studentB.userId);
  });

  it("lets a student create a conversation and add their own messages", async () => {
    const { data: conversation, error: convError } = await studentA.client
      .from("ai_conversations")
      .insert({ profile_id: studentA.userId, context: { subjectId: "test" } })
      .select()
      .single();
    expect(convError).toBeNull();

    const { data: message, error: msgError } = await studentA.client
      .from("ai_messages")
      .insert({ conversation_id: conversation!.id, role: "user", content: "Bonjour" })
      .select()
      .single();
    expect(msgError).toBeNull();
    expect(message?.content).toBe("Bonjour");
  });

  it("hides a student's conversation and messages from another student", async () => {
    const { data: conversation } = await studentA.client
      .from("ai_conversations")
      .insert({ profile_id: studentA.userId, context: {} })
      .select()
      .single();
    await studentA.client
      .from("ai_messages")
      .insert({ conversation_id: conversation!.id, role: "user", content: "Privé" });

    const { data: hiddenConversation } = await studentB.client
      .from("ai_conversations")
      .select("*")
      .eq("id", conversation!.id);
    expect(hiddenConversation).toEqual([]);

    const { data: hiddenMessages } = await studentB.client
      .from("ai_messages")
      .select("*")
      .eq("conversation_id", conversation!.id);
    expect(hiddenMessages).toEqual([]);
  });

  it("blocks inserting a message into another student's conversation", async () => {
    const { data: conversation } = await studentA.client
      .from("ai_conversations")
      .insert({ profile_id: studentA.userId, context: {} })
      .select()
      .single();

    const { error } = await studentB.client
      .from("ai_messages")
      .insert({ conversation_id: conversation!.id, role: "user", content: "Intrusion" });
    expect(error).not.toBeNull();
  });

  it("blocks creating a conversation under another student's profile_id", async () => {
    const { error } = await studentA.client
      .from("ai_conversations")
      .insert({ profile_id: studentB.userId, context: {} });
    expect(error).not.toBeNull();
  });
});
