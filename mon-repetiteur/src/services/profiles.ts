import "server-only";
import { createClient } from "@/lib/supabase/server";
import type { Profile } from "@/types/profile";

/** The signed-in user's own profile, or null if not authenticated. */
export async function getCurrentProfile(): Promise<Profile | null> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return null;

  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .single();

  if (error) {
    console.error("getCurrentProfile:", error.message);
    return null;
  }

  return data;
}
