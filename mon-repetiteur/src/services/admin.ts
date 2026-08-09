import "server-only";
import { createClient } from "@/lib/supabase/server";
import { getCurrentProfile } from "@/services/profiles";
import { getClasses, getPrograms, getSkills, getSubjects, getTopics } from "@/services/curriculum";
import { nextStatus } from "@/lib/content-status";
import type { Profile } from "@/types/profile";
import type { ContentStatus, Lesson } from "@/types/curriculum";
import type { DifficultyLevel, Exercise, ExerciseType } from "@/types/exercise";
import type { Exam, ExamRightsStatus } from "@/types/exam-archive";
import type { Json } from "@/lib/supabase/database.types";

export { nextStatus };

/**
 * Admin CMS (Phase 9, P1): lets teacher/admin roles author lessons/
 * exercises/exam metadata and move them through the content lifecycle
 * (CLAUDE.md §14). All the actual write authorization already lives in
 * RLS (lessons/exercises/exams are staff-insert/update/delete-only,
 * built in Phases 2-4) — requireStaffProfile() below is the
 * application-layer half of CLAUDE.md §13 ("hiding a UI element is not
 * sufficient"): it stops a non-staff user from even reaching the
 * all-statuses *listings* these pages render, which RLS's "published or
 * own or staff" read policies would otherwise happily serve to them if
 * they were staff — the gate here is what keeps a plain student out.
 */

export async function requireStaffProfile(): Promise<Profile | null> {
  const profile = await getCurrentProfile();
  if (!profile) return null;
  if (profile.role !== "teacher" && profile.role !== "admin") return null;
  return profile;
}

// ---------------------------------------------------------------------------
// Curriculum pickers (for content-creation forms)
// ---------------------------------------------------------------------------

export interface SkillOption {
  skillId: string;
  label: string;
}

/** Flattened skill picker across every program — small dataset (one
 * curriculum vertical so far), no pagination needed. */
export async function getSkillOptions(): Promise<SkillOption[]> {
  const programs = await getPrograms();
  const options: SkillOption[] = [];
  for (const program of programs) {
    const [classes, subjects] = await Promise.all([
      getClasses(program.id),
      getSubjects(program.id),
    ]);
    for (const subject of subjects) {
      for (const cls of classes) {
        const topics = await getTopics(subject.id, cls.id);
        for (const topic of topics) {
          const skills = await getSkills(topic.id);
          for (const skill of skills) {
            options.push({
              skillId: skill.id,
              label: `${program.name} · ${subject.name} · ${topic.title} · ${skill.title}`,
            });
          }
        }
      }
    }
  }
  return options;
}

export interface SubjectOption {
  programId: string;
  subjectId: string;
  label: string;
}

export async function getSubjectOptions(): Promise<SubjectOption[]> {
  const programs = await getPrograms();
  const options: SubjectOption[] = [];
  for (const program of programs) {
    const subjects = await getSubjects(program.id);
    for (const subject of subjects) {
      options.push({
        programId: program.id,
        subjectId: subject.id,
        label: `${program.name} · ${subject.name}`,
      });
    }
  }
  return options;
}

// ---------------------------------------------------------------------------
// Lessons
// ---------------------------------------------------------------------------

export type LessonWithSkill = Lesson & { skillTitle: string; topicTitle: string };

export async function listAllLessons(): Promise<LessonWithSkill[]> {
  const staff = await requireStaffProfile();
  if (!staff) return [];

  const supabase = await createClient();
  const { data, error } = await supabase
    .from("lessons")
    .select("*, skills(title, topics(title))")
    .order("created_at", { ascending: false });
  if (error) {
    console.error("listAllLessons:", error.message);
    return [];
  }

  return data
    .filter((row) => row.skills !== null)
    .map((row) => {
      const { skills, ...rest } = row as unknown as Lesson & {
        skills: { title: string; topics: { title: string } | null } | null;
      };
      return { ...rest, skillTitle: skills!.title, topicTitle: skills!.topics?.title ?? "" };
    });
}

export async function createLesson(input: {
  skillId: string;
  title: string;
  content: string;
}): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };
  if (!input.skillId || !input.title.trim() || !input.content.trim()) {
    return { error: "Compétence, titre et contenu requis." };
  }

  const supabase = await createClient();
  const { error } = await supabase.from("lessons").insert({
    skill_id: input.skillId,
    title: input.title,
    content: input.content,
    created_by: staff.id,
  });
  return { error: error?.message ?? null };
}

export async function setLessonStatus(
  lessonId: string,
  status: ContentStatus,
): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };

  const supabase = await createClient();
  const { error } = await supabase
    .from("lessons")
    .update({ status, published_at: status === "published" ? new Date().toISOString() : undefined })
    .eq("id", lessonId);
  return { error: error?.message ?? null };
}

// ---------------------------------------------------------------------------
// Exercises — scoped to the two auto-gradable types the rest of the app
// actually renders (multiple_choice, true_false); short_answer/
// free_response have no student-facing UI yet (see practice/exam pages'
// "type not supported" fallback), so an admin form for them would create
// content nothing can serve — not built ahead of that need (CLAUDE.md §6).
// ---------------------------------------------------------------------------

export type ExerciseWithSkill = Exercise & { skillTitle: string; topicTitle: string };

export async function listAllExercises(): Promise<ExerciseWithSkill[]> {
  const staff = await requireStaffProfile();
  if (!staff) return [];

  const supabase = await createClient();
  const { data, error } = await supabase
    .from("exercises")
    .select("*, skills(title, topics(title))")
    .order("created_at", { ascending: false });
  if (error) {
    console.error("listAllExercises:", error.message);
    return [];
  }

  return data
    .filter((row) => row.skills !== null)
    .map((row) => {
      const { skills, ...rest } = row as unknown as Exercise & {
        skills: { title: string; topics: { title: string } | null } | null;
      };
      return { ...rest, skillTitle: skills!.title, topicTitle: skills!.topics?.title ?? "" };
    });
}

export async function createExercise(input: {
  skillId: string;
  type: Extract<ExerciseType, "multiple_choice" | "true_false">;
  difficulty: DifficultyLevel;
  prompt: string;
  content: Json;
}): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };
  if (!input.skillId || !input.prompt.trim()) {
    return { error: "Compétence et énoncé requis." };
  }

  const supabase = await createClient();
  const { error } = await supabase.from("exercises").insert({
    skill_id: input.skillId,
    type: input.type,
    difficulty: input.difficulty,
    prompt: input.prompt,
    content: input.content,
    created_by: staff.id,
  });
  return { error: error?.message ?? null };
}

export async function setExerciseStatus(
  exerciseId: string,
  status: ContentStatus,
): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };

  const supabase = await createClient();
  const { error } = await supabase.from("exercises").update({ status }).eq("id", exerciseId);
  return { error: error?.message ?? null };
}

// ---------------------------------------------------------------------------
// Exams (archive metadata) — rights_status is the field CLAUDE.md §15
// cares most about; kept as its own explicit action rather than folded
// into a generic "edit" form so a reviewer can't change it by accident
// while editing something else.
// ---------------------------------------------------------------------------

export async function listAllExams(): Promise<Exam[]> {
  const staff = await requireStaffProfile();
  if (!staff) return [];

  const supabase = await createClient();
  const { data, error } = await supabase
    .from("exams")
    .select("*")
    .order("created_at", { ascending: false });
  if (error) {
    console.error("listAllExams:", error.message);
    return [];
  }
  return data;
}

export async function createExam(input: {
  programId: string;
  subjectId: string;
  year: number;
  session: string;
  title: string;
  rightsStatus: ExamRightsStatus;
  source: string;
  sourceUrl: string;
  permissionReference: string;
}): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };
  if (!input.subjectId || !input.title.trim() || !input.year) {
    return { error: "Sujet, titre et année requis." };
  }

  const supabase = await createClient();
  const { error } = await supabase.from("exams").insert({
    program_id: input.programId,
    subject_id: input.subjectId,
    year: input.year,
    session: input.session || null,
    title: input.title,
    rights_status: input.rightsStatus,
    source: input.source || null,
    source_url: input.sourceUrl || null,
    permission_reference: input.permissionReference || null,
    created_by: staff.id,
  });
  return { error: error?.message ?? null };
}

export async function setExamStatus(
  examId: string,
  status: ContentStatus,
): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };

  const supabase = await createClient();
  const { error } = await supabase.from("exams").update({ status }).eq("id", examId);
  return { error: error?.message ?? null };
}

export async function setExamRightsStatus(
  examId: string,
  rightsStatus: ExamRightsStatus,
): Promise<{ error: string | null }> {
  const staff = await requireStaffProfile();
  if (!staff) return { error: "Non autorisé." };

  const supabase = await createClient();
  const { error } = await supabase
    .from("exams")
    .update({ rights_status: rightsStatus })
    .eq("id", examId);
  return { error: error?.message ?? null };
}
