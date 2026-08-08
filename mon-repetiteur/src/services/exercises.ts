import "server-only";
import { createClient } from "@/lib/supabase/server";
import { scoreExercise } from "@/lib/scoring";
import type { Json } from "@/lib/supabase/database.types";
import type { Attempt, Exercise } from "@/types/exercise";

/** Exercises for a skill. RLS decides visibility (published, own draft, or staff). */
export async function getExercises(skillId: string): Promise<Exercise[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("exercises")
    .select("*")
    .eq("skill_id", skillId)
    .order("created_at");
  if (error) {
    console.error("getExercises:", error.message);
    return [];
  }
  return data;
}

export interface SubmitExerciseAttemptResult {
  error: string | null;
  attempt: Attempt | null;
}

/**
 * Grades `answer` server-side against the exercise's stored content and
 * records an immutable attempt. Never trusts a client-supplied
 * correctness/score — see scoreExercise (CLAUDE.md §1/§13).
 */
export async function submitExerciseAttempt(
  exerciseId: string,
  answer: Json,
): Promise<SubmitExerciseAttemptResult> {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", attempt: null };
  }

  const { data: exercise, error: exerciseError } = await supabase
    .from("exercises")
    .select("*")
    .eq("id", exerciseId)
    .maybeSingle();
  if (exerciseError || !exercise) {
    return { error: "Exercice introuvable.", attempt: null };
  }

  const isCorrect = scoreExercise(exercise, answer);

  const { data: attempt, error: insertError } = await supabase
    .from("attempts")
    .insert({
      profile_id: user.id,
      attemptable_type: "exercise",
      attemptable_id: exerciseId,
      answer,
      is_correct: isCorrect,
      score: isCorrect === null ? null : isCorrect ? 1 : 0,
    })
    .select()
    .single();

  if (insertError) {
    return { error: insertError.message, attempt: null };
  }

  return { error: null, attempt };
}
