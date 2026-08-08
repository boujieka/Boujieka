import "server-only";
import { createClient as createSupabaseClient } from "@supabase/supabase-js";
import type { Database } from "./database.types";

/**
 * Service-role Supabase client. Bypasses Row Level Security entirely.
 *
 * Server-only — the `server-only` import makes this a build error if it
 * ever ends up in a client bundle. NEVER expose SUPABASE_SERVICE_ROLE_KEY
 * to the browser (CLAUDE.md §12). Reserve this for operations that
 * legitimately need to act outside a specific user's RLS scope (e.g. the
 * Admin CMS, background jobs) — most server code should use
 * `lib/supabase/server.ts` instead, which stays scoped to the caller.
 */
export function createAdminClient() {
  return createSupabaseClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    { auth: { autoRefreshToken: false, persistSession: false } },
  );
}
