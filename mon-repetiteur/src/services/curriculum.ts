import "server-only";
import { createClient } from "@/lib/supabase/server";
import type { Class, Lesson, Program, Skill, Subject, Topic } from "@/types/curriculum";

/** All programs (e.g. Terminale C, GCE A-Level). Readable by any signed-in user. */
export async function getPrograms(): Promise<Program[]> {
  const supabase = await createClient();
  const { data, error } = await supabase.from("programs").select("*").order("code");
  if (error) {
    console.error("getPrograms:", error.message);
    return [];
  }
  return data;
}

export async function getClasses(programId: string): Promise<Class[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("classes")
    .select("*")
    .eq("program_id", programId)
    .order("order");
  if (error) {
    console.error("getClasses:", error.message);
    return [];
  }
  return data;
}

export async function getSubjects(programId: string): Promise<Subject[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("subjects")
    .select("*")
    .eq("program_id", programId)
    .order("name");
  if (error) {
    console.error("getSubjects:", error.message);
    return [];
  }
  return data;
}

/** Top-level topics (no parent) for a subject within a class level. */
export async function getTopics(subjectId: string, classId: string): Promise<Topic[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("topics")
    .select("*")
    .eq("subject_id", subjectId)
    .eq("class_id", classId)
    .is("parent_id", null)
    .order("order");
  if (error) {
    console.error("getTopics:", error.message);
    return [];
  }
  return data;
}

export async function getSkills(topicId: string): Promise<Skill[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("skills")
    .select("*")
    .eq("topic_id", topicId)
    .order("order");
  if (error) {
    console.error("getSkills:", error.message);
    return [];
  }
  return data;
}

/** Lessons for a skill. RLS decides visibility (published, own draft, or staff) —
 * an empty result for a student can mean "no lesson yet" or "not published yet",
 * which the UI should treat the same way (CLAUDE.md §23 empty state). */
export async function getLessonsForSkill(skillId: string): Promise<Lesson[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("lessons")
    .select("*")
    .eq("skill_id", skillId)
    .order("created_at");
  if (error) {
    console.error("getLessonsForSkill:", error.message);
    return [];
  }
  return data;
}

/** A single lesson. RLS decides visibility (published, or own draft, or staff). */
export async function getLesson(lessonId: string): Promise<Lesson | null> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("lessons")
    .select("*")
    .eq("id", lessonId)
    .maybeSingle();
  if (error) {
    console.error("getLesson:", error.message);
    return null;
  }
  return data;
}
