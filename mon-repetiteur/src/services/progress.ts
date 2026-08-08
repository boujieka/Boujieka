import "server-only";
import { createClient } from "@/lib/supabase/server";
import type { SkillProgressEntry } from "@/types/progress";

/**
 * The signed-in student's own progress, one row per skill they've
 * attempted at least one graded exercise on. mastery_score is maintained
 * by the update_skill_progress trigger (see the skill_progress migration),
 * never computed here.
 */
export async function getStudentProgress(): Promise<SkillProgressEntry[]> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return [];

  const { data, error } = await supabase
    .from("skill_progress")
    .select("mastery_score, updated_at, skills(id, title, topics(title))")
    .eq("profile_id", user.id)
    .order("mastery_score", { ascending: true });

  if (error) {
    console.error("getStudentProgress:", error.message);
    return [];
  }

  return data
    .filter((row) => row.skills !== null)
    .map((row) => ({
      skillId: row.skills!.id,
      skillTitle: row.skills!.title,
      topicTitle: row.skills!.topics?.title ?? "",
      masteryScore: row.mastery_score,
      updatedAt: row.updated_at,
    }));
}

/** Skills below `threshold` mastery, weakest first — for AI Tutor / Dashboard use later. */
export async function getWeakSkills(threshold = 0.5, limit = 5): Promise<SkillProgressEntry[]> {
  const progress = await getStudentProgress();
  return progress.filter((entry) => entry.masteryScore < threshold).slice(0, limit);
}
