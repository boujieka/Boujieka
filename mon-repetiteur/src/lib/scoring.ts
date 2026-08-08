import type { Json } from "@/lib/supabase/database.types";
import type { Exercise } from "@/types/exercise";

interface MultipleChoiceContent {
  choices: string[];
  correctIndex: number;
}

interface TrueFalseContent {
  answer: boolean;
}

/**
 * Grades a submitted answer against an exercise's stored content.
 * Pure and server-side only — the client's opinion of correctness is
 * never trusted (CLAUDE.md §1 correctness, §13 authorization).
 *
 * Returns null for types that aren't auto-gradable (short_answer,
 * free_response) — that's "needs human/AI-assisted review", not "wrong".
 */
export function scoreExercise(
  exercise: Pick<Exercise, "type" | "content">,
  answer: Json,
): boolean | null {
  switch (exercise.type) {
    case "multiple_choice": {
      const content = exercise.content as unknown as MultipleChoiceContent;
      return typeof answer === "number" && answer === content.correctIndex;
    }
    case "true_false": {
      const content = exercise.content as unknown as TrueFalseContent;
      return typeof answer === "boolean" && answer === content.answer;
    }
    case "short_answer":
    case "free_response":
      return null;
    default:
      return null;
  }
}
