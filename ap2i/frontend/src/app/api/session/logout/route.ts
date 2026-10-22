import { NextResponse, type NextRequest } from "next/server";
import { API_URL, SESSION_COOKIE } from "@/lib/session";
import { rejectCrossOrigin } from "@/lib/route-guard";

export const dynamic = "force-dynamic";

/** POST: revokes the backend token (token_version bump) and clears the session cookie. */
export async function POST(req: NextRequest) {
  const bad = rejectCrossOrigin(req);
  if (bad) return bad;
  const token = req.cookies.get(SESSION_COOKIE)?.value;
  if (token) {
    await fetch(`${API_URL}/auth/logout`, { method: "POST", headers: { authorization: `Bearer ${token}` }, cache: "no-store" }).catch(() => null);
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.delete(SESSION_COOKIE);
  return res;
}
