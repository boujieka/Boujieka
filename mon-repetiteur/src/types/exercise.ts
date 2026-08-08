import type { Database } from "@/lib/supabase/database.types";

export type Exercise = Database["public"]["Tables"]["exercises"]["Row"];
export type ExerciseType = Database["public"]["Enums"]["exercise_type"];
export type DifficultyLevel = Database["public"]["Enums"]["difficulty_level"];
export type Attempt = Database["public"]["Tables"]["attempts"]["Row"];
