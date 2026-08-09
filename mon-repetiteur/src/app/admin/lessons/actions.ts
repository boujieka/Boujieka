"use server";

import { redirect } from "next/navigation";
import { createLesson, setLessonStatus } from "@/services/admin";
import type { ContentStatus } from "@/types/curriculum";

// Same mutate-then-redirect-to-the-same-route pattern used across the app
// (submitMockExamAction, completeStudySessionAction, …) — a full
// navigation re-fetches the server component with fresh data.

export async function createLessonAction(formData: FormData) {
  await createLesson({
    skillId: String(formData.get("skillId") ?? ""),
    title: String(formData.get("title") ?? ""),
    content: String(formData.get("content") ?? ""),
  });
  redirect("/admin/lessons");
}

export async function setLessonStatusAction(formData: FormData) {
  const lessonId = String(formData.get("lessonId") ?? "");
  const status = String(formData.get("status") ?? "") as ContentStatus;
  if (lessonId && status) {
    await setLessonStatus(lessonId, status);
  }
  redirect("/admin/lessons");
}
