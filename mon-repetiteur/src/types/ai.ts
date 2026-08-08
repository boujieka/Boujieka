import type { Database } from "@/lib/supabase/database.types";

export type AiConversation = Database["public"]["Tables"]["ai_conversations"]["Row"];
export type AiMessage = Database["public"]["Tables"]["ai_messages"]["Row"];
export type AiMessageRole = Database["public"]["Enums"]["ai_message_role"];

/** Snapshot of where in the curriculum a tutoring conversation is anchored
 * (CLAUDE.md §18) — as much or as little as is known when it starts. */
export interface TutorContext {
  programId?: string;
  classId?: string;
  subjectId?: string;
  topicId?: string;
  skillId?: string;
  lessonId?: string;
  exerciseId?: string;
}
