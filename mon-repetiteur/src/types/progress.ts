import type { Database } from "@/lib/supabase/database.types";

export type SkillProgress = Database["public"]["Tables"]["skill_progress"]["Row"];

export interface SkillProgressEntry {
  skillId: string;
  skillTitle: string;
  topicTitle: string;
  masteryScore: number;
  updatedAt: string;
}
