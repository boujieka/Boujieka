import "server-only";
import { createClient } from "@/lib/supabase/server";

export interface AuthResult {
  error: string | null;
  /** True once the caller has an active session (email confirmed, or
   * confirmation disabled — the case in local dev). False means a
   * confirmation email was sent and no session exists yet. */
  hasSession: boolean;
}

export async function signUpWithPassword(input: {
  email: string;
  password: string;
  fullName: string;
}): Promise<AuthResult> {
  const supabase = await createClient();
  const { data, error } = await supabase.auth.signUp({
    email: input.email,
    password: input.password,
    options: { data: { full_name: input.fullName } },
  });

  return {
    error: error?.message ?? null,
    hasSession: data.session !== null,
  };
}

export async function signInWithPassword(input: {
  email: string;
  password: string;
}): Promise<{ error: string | null }> {
  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword(input);
  return { error: error?.message ?? null };
}

export async function signOut(): Promise<void> {
  const supabase = await createClient();
  await supabase.auth.signOut();
}
