import "server-only";
import { createClient } from "@/lib/supabase/server";
import type { TutorContext } from "@/types/ai";

export interface ResolvedTutorContext {
  programName?: string;
  className?: string;
  subjectName?: string;
  topicTitle?: string;
  skillTitle?: string;
  /** Only populated if the lesson is published (or owned/staff — RLS
   * already enforces this at the query level, this just re-checks the
   * flag so a draft never silently grounds the model's answer). */
  lessonContent?: string;
  exercisePrompt?: string;
}

/**
 * Resolves a conversation's id-based context into human-readable labels
 * and, where available, published lesson/exercise content to ground the
 * model's response — the "metadata filtering -> published educational
 * content" steps of CLAUDE.md §19's RAG pipeline. True vector search
 * (pgvector) is deliberately not implemented yet: the corpus is nine
 * lessons and generating embeddings needs the same missing
 * ANTHROPIC_API_KEY this whole service needs — not worth the complexity
 * until there's enough content and a working embeddings pipeline to
 * justify it. Direct FK-scoped lookup is exact for a corpus this size.
 */
export async function resolveTutorContext(context: TutorContext): Promise<ResolvedTutorContext> {
  const supabase = await createClient();
  const resolved: ResolvedTutorContext = {};

  if (context.programId) {
    const { data } = await supabase
      .from("programs")
      .select("name")
      .eq("id", context.programId)
      .maybeSingle();
    resolved.programName = data?.name;
  }

  if (context.classId) {
    const { data } = await supabase
      .from("classes")
      .select("name")
      .eq("id", context.classId)
      .maybeSingle();
    resolved.className = data?.name;
  }

  if (context.subjectId) {
    const { data } = await supabase
      .from("subjects")
      .select("name")
      .eq("id", context.subjectId)
      .maybeSingle();
    resolved.subjectName = data?.name;
  }

  if (context.topicId) {
    const { data } = await supabase
      .from("topics")
      .select("title")
      .eq("id", context.topicId)
      .maybeSingle();
    resolved.topicTitle = data?.title;
  }

  if (context.skillId) {
    const { data } = await supabase
      .from("skills")
      .select("title")
      .eq("id", context.skillId)
      .maybeSingle();
    resolved.skillTitle = data?.title;
  }

  if (context.lessonId) {
    const { data } = await supabase
      .from("lessons")
      .select("content, status")
      .eq("id", context.lessonId)
      .maybeSingle();
    if (data?.status === "published") {
      resolved.lessonContent = data.content;
    }
  }

  if (context.exerciseId) {
    const { data } = await supabase
      .from("exercises")
      .select("prompt, status")
      .eq("id", context.exerciseId)
      .maybeSingle();
    if (data?.status === "published") {
      resolved.exercisePrompt = data.prompt;
    }
  }

  return resolved;
}
