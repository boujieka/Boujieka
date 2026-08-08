import type { Database } from "@/lib/supabase/database.types";

export type Program = Database["public"]["Tables"]["programs"]["Row"];
export type Class = Database["public"]["Tables"]["classes"]["Row"];
export type Subject = Database["public"]["Tables"]["subjects"]["Row"];
export type Topic = Database["public"]["Tables"]["topics"]["Row"];
export type Skill = Database["public"]["Tables"]["skills"]["Row"];
export type Lesson = Database["public"]["Tables"]["lessons"]["Row"];
export type ContentStatus = Database["public"]["Enums"]["content_status"];
