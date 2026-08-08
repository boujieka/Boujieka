import "server-only";
import { createClient } from "@/lib/supabase/server";

/**
 * Server-side exam-mode check (CLAUDE.md §22): the AI Tutor must refuse
 * to respond while a student is in an active exam. Enforced here, not
 * just hidden in the UI — tutor.ts calls this on every message before
 * touching the provider.
 */
export async function isExamModeActive(profileId: string): Promise<boolean> {
  const supabase = await createClient();
  const { count, error } = await supabase
    .from("mock_exams")
    .select("id", { count: "exact", head: true })
    .eq("profile_id", profileId)
    .eq("status", "in_progress");

  if (error) {
    console.error("isExamModeActive:", error.message);
    // Fail closed: if we can't tell, assume an exam might be active rather
    // than risk giving AI help during one.
    return true;
  }

  return (count ?? 0) > 0;
}
