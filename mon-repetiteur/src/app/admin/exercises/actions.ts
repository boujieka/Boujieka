"use server";

import { redirect } from "next/navigation";
import { createExercise, setExerciseStatus } from "@/services/admin";
import type { ContentStatus } from "@/types/curriculum";
import type { DifficultyLevel } from "@/types/exercise";
import type { Json } from "@/lib/supabase/database.types";

export async function createExerciseAction(formData: FormData) {
  const type = String(formData.get("type") ?? "");
  const skillId = String(formData.get("skillId") ?? "");
  const difficulty = String(formData.get("difficulty") ?? "medium") as DifficultyLevel;
  const prompt = String(formData.get("prompt") ?? "");

  let content: Json;
  if (type === "true_false") {
    content = { answer: formData.get("answer") === "true" } as unknown as Json;
  } else {
    const choices = ["choice0", "choice1", "choice2", "choice3"]
      .map((key) => String(formData.get(key) ?? "").trim())
      .filter((choice) => choice.length > 0);
    const correctIndex = Number(formData.get("correctIndex") ?? 0);
    content = { choices, correctIndex } as unknown as Json;
  }

  if (type === "multiple_choice" || type === "true_false") {
    await createExercise({ skillId, type, difficulty, prompt, content });
  }
  redirect("/admin/exercises");
}

export async function setExerciseStatusAction(formData: FormData) {
  const exerciseId = String(formData.get("exerciseId") ?? "");
  const status = String(formData.get("status") ?? "") as ContentStatus;
  if (exerciseId && status) {
    await setExerciseStatus(exerciseId, status);
  }
  redirect("/admin/exercises");
}
