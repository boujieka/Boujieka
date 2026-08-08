import type { Database } from "@/lib/supabase/database.types";

export type Exam = Database["public"]["Tables"]["exams"]["Row"];
export type ExamQuestion = Database["public"]["Tables"]["exam_questions"]["Row"];
export type ExamRightsStatus = Database["public"]["Enums"]["exam_rights_status"];

/** Rights statuses that permit exposing source_url to the client (CLAUDE.md §15). */
export const EXPOSABLE_RIGHTS_STATUSES: readonly ExamRightsStatus[] = [
  "verified",
  "publicly_reusable",
];

/** An exam as returned to the client — never carries source_url directly. */
export interface ExamListItem extends Omit<Exam, "source_url"> {
  /** Only set when rights_status allows exposing it; null otherwise. */
  accessUrl: string | null;
}
