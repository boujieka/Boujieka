"use server";

import { redirect } from "next/navigation";
import { createMockExam } from "@/services/mock-exam";

export async function startMockExamAction(formData: FormData) {
  const subjectId = String(formData.get("subjectId") ?? "");
  const classId = String(formData.get("classId") ?? "");
  if (!subjectId || !classId) {
    redirect("/learn");
  }

  const { error, mockExam } = await createMockExam(subjectId, classId);
  if (error || !mockExam) {
    redirect("/learn");
  }

  redirect(`/exam/${mockExam.id}`);
}
