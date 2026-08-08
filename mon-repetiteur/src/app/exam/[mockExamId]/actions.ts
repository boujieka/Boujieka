"use server";

import { redirect } from "next/navigation";
import { submitMockExam } from "@/services/mock-exam";
import type { Json } from "@/lib/supabase/database.types";

export async function submitMockExamAction(mockExamId: string, formData: FormData) {
  const answers: Record<string, Json> = {};

  for (const [key, value] of formData.entries()) {
    if (!key.startsWith("question:")) continue;
    const questionId = key.slice("question:".length);
    const raw = String(value);

    if (raw === "true" || raw === "false") {
      answers[questionId] = raw === "true";
    } else if (raw !== "" && !Number.isNaN(Number(raw))) {
      answers[questionId] = Number(raw);
    } else {
      answers[questionId] = raw;
    }
  }

  await submitMockExam(mockExamId, answers);

  // One-shot submit-then-show-results — a full navigation here is simple
  // and correct (unlike the AI Tutor's chat, this isn't a repeated
  // per-message action where an extra round trip would be wasteful).
  redirect(`/exam/${mockExamId}`);
}
