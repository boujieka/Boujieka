import "server-only";
import { createClient } from "@/lib/supabase/server";
import { scoreExercise } from "@/lib/scoring";
import type { Json } from "@/lib/supabase/database.types";
import type { Exercise } from "@/types/exercise";
import type { MockExam, MockExamQuestion } from "@/types/mock-exam";

export interface CreateMockExamResult {
  error: string | null;
  mockExam: MockExam | null;
}

/**
 * Assembles a mock exam from every currently published exercise across a
 * subject/class's skills. No sampling/limits yet — the vertical only has
 * nine exercises total, so "all of them" is the whole exam; revisit once
 * there's enough content that a fixed-size draw makes sense.
 */
export async function createMockExam(
  subjectId: string,
  classId: string,
): Promise<CreateMockExamResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", mockExam: null };
  }

  const { data: topics } = await supabase
    .from("topics")
    .select("id")
    .eq("subject_id", subjectId)
    .eq("class_id", classId);
  const topicIds = (topics ?? []).map((t) => t.id);
  if (topicIds.length === 0) {
    return { error: "Aucun chapitre disponible pour cet examen.", mockExam: null };
  }

  const { data: skills } = await supabase.from("skills").select("id").in("topic_id", topicIds);
  const skillIds = (skills ?? []).map((s) => s.id);
  if (skillIds.length === 0) {
    return { error: "Aucune compétence disponible pour cet examen.", mockExam: null };
  }

  const { data: exercises } = await supabase
    .from("exercises")
    .select("id")
    .in("skill_id", skillIds)
    .eq("status", "published")
    .order("created_at");
  if (!exercises || exercises.length === 0) {
    return { error: "Aucun exercice publié disponible pour cet examen.", mockExam: null };
  }

  const { data: mockExam, error: examError } = await supabase
    .from("mock_exams")
    .insert({ profile_id: user.id, subject_id: subjectId, class_id: classId })
    .select()
    .single();
  if (examError || !mockExam) {
    return { error: examError?.message ?? "Échec de la création de l'examen.", mockExam: null };
  }

  const questionRows = exercises.map((exercise, index) => ({
    mock_exam_id: mockExam.id,
    exercise_id: exercise.id,
    order: index,
  }));
  const { error: questionsError } = await supabase
    .from("mock_exam_questions")
    .insert(questionRows);
  if (questionsError) {
    return { error: questionsError.message, mockExam };
  }

  return { error: null, mockExam };
}

export interface MockExamQuestionWithExercise extends MockExamQuestion {
  exercise: Exercise;
}

export async function getMockExamWithQuestions(mockExamId: string): Promise<{
  mockExam: MockExam | null;
  questions: MockExamQuestionWithExercise[];
}> {
  const supabase = await createClient();

  const { data: mockExam } = await supabase
    .from("mock_exams")
    .select("*")
    .eq("id", mockExamId)
    .maybeSingle();
  if (!mockExam) {
    return { mockExam: null, questions: [] };
  }

  const { data: questions } = await supabase
    .from("mock_exam_questions")
    .select("*, exercise:exercises(*)")
    .eq("mock_exam_id", mockExamId)
    .order("order");

  return { mockExam, questions: (questions ?? []) as MockExamQuestionWithExercise[] };
}

export interface SubmitMockExamResult {
  error: string | null;
  mockExam: MockExam | null;
}

/**
 * Grades every answered question server-side against its exercise's
 * stored content (scoreExercise — the same function Exercises' single-
 * attempt flow uses, never a client-supplied correctness), then marks the
 * exam submitted with an overall score. Immutable once submitted.
 */
export async function submitMockExam(
  mockExamId: string,
  answers: Record<string, Json>,
): Promise<SubmitMockExamResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", mockExam: null };
  }

  const { mockExam, questions } = await getMockExamWithQuestions(mockExamId);
  if (!mockExam) {
    return { error: "Examen introuvable.", mockExam: null };
  }
  if (mockExam.status === "submitted") {
    return { error: "Cet examen a déjà été soumis.", mockExam };
  }

  let correctCount = 0;
  let gradedCount = 0;
  const answerRows: {
    mock_exam_id: string;
    mock_exam_question_id: string;
    answer: Json;
    is_correct: boolean | null;
  }[] = [];

  for (const question of questions) {
    const answer = answers[question.id];
    if (answer === undefined) continue;

    const isCorrect = scoreExercise(question.exercise, answer);
    if (isCorrect !== null) {
      gradedCount += 1;
      if (isCorrect) correctCount += 1;
    }
    answerRows.push({
      mock_exam_id: mockExamId,
      mock_exam_question_id: question.id,
      answer,
      is_correct: isCorrect,
    });
  }

  if (answerRows.length > 0) {
    const { error: insertError } = await supabase.from("mock_exam_answers").insert(answerRows);
    if (insertError) {
      return { error: insertError.message, mockExam };
    }
  }

  const score = gradedCount > 0 ? correctCount / gradedCount : 0;

  const { data: updated, error: updateError } = await supabase
    .from("mock_exams")
    .update({ status: "submitted", score, submitted_at: new Date().toISOString() })
    .eq("id", mockExamId)
    .select()
    .single();
  if (updateError) {
    return { error: updateError.message, mockExam };
  }

  return { error: null, mockExam: updated };
}
