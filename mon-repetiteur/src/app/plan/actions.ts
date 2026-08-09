"use server";

import { redirect } from "next/navigation";
import { completeStudySession, generateStudyPlan } from "@/services/study-plan";

// Same one-shot mutate-then-redirect-to-the-same-route pattern as the mock
// exam's submitMockExamAction: a full navigation re-fetches the server
// component with fresh data, which is simple and correct here (no repeated
// per-action round trips like the AI Tutor chat that would make it wasteful).

export async function generateStudyPlanAction() {
  await generateStudyPlan();
  redirect("/plan");
}

export async function completeStudySessionAction(formData: FormData) {
  const sessionId = String(formData.get("sessionId") ?? "");
  if (!sessionId) {
    redirect("/plan");
  }
  await completeStudySession(sessionId);
  redirect("/plan");
}
