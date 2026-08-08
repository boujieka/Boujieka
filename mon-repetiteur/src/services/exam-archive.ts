import "server-only";
import { createClient } from "@/lib/supabase/server";
import { toExamListItem } from "@/lib/exam-rights";
import type { ExamListItem } from "@/types/exam-archive";

export async function getExams(subjectId: string): Promise<ExamListItem[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("exams")
    .select("*")
    .eq("subject_id", subjectId)
    .order("year", { ascending: false });

  if (error) {
    console.error("getExams:", error.message);
    return [];
  }

  return data.map(toExamListItem);
}
