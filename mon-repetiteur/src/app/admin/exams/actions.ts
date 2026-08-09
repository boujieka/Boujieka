"use server";

import { redirect } from "next/navigation";
import { createExam, setExamRightsStatus, setExamStatus } from "@/services/admin";
import type { ContentStatus } from "@/types/curriculum";
import type { ExamRightsStatus } from "@/types/exam-archive";

export async function createExamAction(formData: FormData) {
  const [programId, subjectId] = String(formData.get("subject") ?? "").split("|");

  await createExam({
    programId: programId ?? "",
    subjectId: subjectId ?? "",
    year: Number(formData.get("year") ?? 0),
    session: String(formData.get("session") ?? ""),
    title: String(formData.get("title") ?? ""),
    rightsStatus: String(formData.get("rightsStatus") ?? "unknown") as ExamRightsStatus,
    source: String(formData.get("source") ?? ""),
    sourceUrl: String(formData.get("sourceUrl") ?? ""),
    permissionReference: String(formData.get("permissionReference") ?? ""),
  });
  redirect("/admin/exams");
}

export async function setExamStatusAction(formData: FormData) {
  const examId = String(formData.get("examId") ?? "");
  const status = String(formData.get("status") ?? "") as ContentStatus;
  if (examId && status) {
    await setExamStatus(examId, status);
  }
  redirect("/admin/exams");
}

export async function setExamRightsStatusAction(formData: FormData) {
  const examId = String(formData.get("examId") ?? "");
  const rightsStatus = String(formData.get("rightsStatus") ?? "") as ExamRightsStatus;
  if (examId && rightsStatus) {
    await setExamRightsStatus(examId, rightsStatus);
  }
  redirect("/admin/exams");
}
