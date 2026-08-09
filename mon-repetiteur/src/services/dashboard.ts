import "server-only";
import { createClient } from "@/lib/supabase/server";
import { getCurrentProfile } from "@/services/profiles";
import { getStudentProgress, getWeakSkills } from "@/services/progress";
import type { Profile } from "@/types/profile";
import type { SkillProgressEntry } from "@/types/progress";
import type { MockExam } from "@/types/mock-exam";

export interface RecentActivityEntry {
  attemptId: string;
  exerciseId: string;
  skillId: string;
  skillTitle: string;
  topicTitle: string;
  isCorrect: boolean | null;
  attemptedAt: string;
}

export interface DashboardData {
  profile: Profile;
  weakSkills: SkillProgressEntry[];
  recentActivity: RecentActivityEntry[];
  activeMockExam: MockExam | null;
  stats: {
    totalAttempts: number;
    averageMastery: number | null;
  };
}

/**
 * Aggregates PRD §7 item 8 ("student's current progress, weak skills,
 * recent activity, entry points into the loop") from existing services/
 * tables — no new schema needed. Pure read-side aggregation: every
 * sub-query is scoped to the signed-in user by RLS, same as the services
 * it reuses (getStudentProgress/getWeakSkills).
 */
export async function getDashboardData(): Promise<DashboardData | null> {
  const profile = await getCurrentProfile();
  if (!profile) return null;

  const [weakSkills, allProgress, recentActivity, activeMockExam, totalAttempts] =
    await Promise.all([
      getWeakSkills(),
      getStudentProgress(),
      getRecentActivity(profile.id),
      getActiveMockExam(profile.id),
      getTotalAttemptsCount(profile.id),
    ]);

  const averageMastery =
    allProgress.length === 0
      ? null
      : allProgress.reduce((sum, entry) => sum + entry.masteryScore, 0) / allProgress.length;

  return {
    profile,
    weakSkills,
    recentActivity,
    activeMockExam,
    stats: { totalAttempts, averageMastery },
  };
}

/**
 * attempts.attemptable_id is intentionally polymorphic (no FK — see the
 * exercises migration), so it can't be embedded via a single PostgREST
 * select like the exam page's exercise join. Two-step instead: recent
 * attempts, then the exercises (with skill/topic) they point to.
 */
async function getRecentActivity(profileId: string, limit = 5): Promise<RecentActivityEntry[]> {
  const supabase = await createClient();

  const { data: attempts, error: attemptsError } = await supabase
    .from("attempts")
    .select("id, attemptable_id, is_correct, attempted_at")
    .eq("profile_id", profileId)
    .eq("attemptable_type", "exercise")
    .order("attempted_at", { ascending: false })
    .limit(limit);
  if (attemptsError) {
    console.error("getRecentActivity (attempts):", attemptsError.message);
    return [];
  }
  if (!attempts || attempts.length === 0) return [];

  const exerciseIds = [...new Set(attempts.map((a) => a.attemptable_id))];
  const { data: exercises, error: exercisesError } = await supabase
    .from("exercises")
    .select("id, skill_id, skills(title, topics(title))")
    .in("id", exerciseIds);
  if (exercisesError) {
    console.error("getRecentActivity (exercises):", exercisesError.message);
    return [];
  }

  const exerciseById = new Map((exercises ?? []).map((exercise) => [exercise.id, exercise]));

  return attempts
    .map((attempt): RecentActivityEntry | null => {
      const exercise = exerciseById.get(attempt.attemptable_id);
      if (!exercise || !exercise.skills) return null;
      return {
        attemptId: attempt.id,
        exerciseId: attempt.attemptable_id,
        skillId: exercise.skill_id,
        skillTitle: exercise.skills.title,
        topicTitle: exercise.skills.topics?.title ?? "",
        isCorrect: attempt.is_correct,
        attemptedAt: attempt.attempted_at,
      };
    })
    .filter((entry): entry is RecentActivityEntry => entry !== null);
}

/** Most recent in_progress mock exam, if any — surfaced as a "resume" entry point. */
async function getActiveMockExam(profileId: string): Promise<MockExam | null> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("mock_exams")
    .select("*")
    .eq("profile_id", profileId)
    .eq("status", "in_progress")
    .order("started_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (error) {
    console.error("getActiveMockExam:", error.message);
    return null;
  }
  return data;
}

async function getTotalAttemptsCount(profileId: string): Promise<number> {
  const supabase = await createClient();
  const { count, error } = await supabase
    .from("attempts")
    .select("id", { count: "exact", head: true })
    .eq("profile_id", profileId);
  if (error) {
    console.error("getTotalAttemptsCount:", error.message);
    return 0;
  }
  return count ?? 0;
}
