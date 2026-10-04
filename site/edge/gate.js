// Netlify Edge Function: downloads (report PDFs, data CSVs) require a free Cartouche account.
// Written into site/dist/netlify/edge-functions/ by site/build.py only when Supabase is configured
// (SUPABASE_URL + SUPABASE_PUBLISHABLE_KEY or SUPABASE_ANON_KEY); __CONFIG__ is replaced then.
// The access token is the one Supabase Auth issued at sign-in; it is checked against Supabase on
// every download, so an expired or revoked session is refused.
const CFG = __CONFIG__;
export const COOKIE = "cartouche_at";

export async function allowed(token, fetcher = fetch) {
  if (!token || token.length > 4096) return false;
  try {
    const r = await fetcher(`${CFG.url}/auth/v1/user`, { headers: { apikey: CFG.key, Authorization: `Bearer ${token}` } });
    return r.ok;
  } catch {
    return false;  // Supabase unreachable: fail closed
  }
}

export default async (request, context) => {
  if (await allowed(context.cookies.get(COOKIE))) return context.next();
  const url = new URL(request.url);
  const to = new URL("/", url);
  to.searchParams.set("next", url.pathname);
  to.hash = "compte";
  return new Response(null, { status: 302, headers: { Location: to.toString(), "Cache-Control": "no-store" } });
};

export const config = { path: ["/rapports/*.pdf", "/donnees/*.csv"], cache: "manual" };
