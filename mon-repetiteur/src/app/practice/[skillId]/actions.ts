"use server";

import { submitExerciseAttempt } from "@/services/exercises";
import type { Json } from "@/lib/supabase/database.types";

export interface AttemptState {
  error: string | null;
  isCorrect: boolean | null;
  submitted: boolean;
}

export async function submitAttemptAction(
  exerciseId: string,
  _prevState: AttemptState,
  formData: FormData,
): Promise<AttemptState> {
  const raw = formData.get("answer");
  if (raw === null || raw === "") {
    return { error: "Choisissez une réponse.", isCorrect: null, submitted: false };
  }

  let answer: Json;
  if (raw === "true" || raw === "false") {
    answer = raw === "true";
  } else if (raw !== "" && !Number.isNaN(Number(raw))) {
    answer = Number(raw);
  } else {
    answer = String(raw);
  }

  const { error, attempt } = await submitExerciseAttempt(exerciseId, answer);
  if (error) {
    return { error, isCorrect: null, submitted: false };
  }

  return { error: null, isCorrect: attempt?.is_correct ?? null, submitted: true };
}
