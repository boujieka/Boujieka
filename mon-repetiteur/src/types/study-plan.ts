import type { Database } from "@/lib/supabase/database.types";

export type StudyPlan = Database["public"]["Tables"]["study_plans"]["Row"];
export type StudySession = Database["public"]["Tables"]["study_sessions"]["Row"];
export type StudyPlanStatus = Database["public"]["Enums"]["study_plan_status"];
