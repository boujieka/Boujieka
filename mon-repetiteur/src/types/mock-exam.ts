import type { Database } from "@/lib/supabase/database.types";

export type MockExam = Database["public"]["Tables"]["mock_exams"]["Row"];
export type MockExamQuestion = Database["public"]["Tables"]["mock_exam_questions"]["Row"];
export type MockExamAnswer = Database["public"]["Tables"]["mock_exam_answers"]["Row"];
export type MockExamStatus = Database["public"]["Enums"]["mock_exam_status"];
