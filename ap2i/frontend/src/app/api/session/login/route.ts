import { NextResponse, type NextRequest } from "next/server";
import { API_URL, cookieOptions, MFA_COOKIE, SESSION_COOKIE } from "@/lib/session";
import { readJson, rejectCrossOrigin } from "@/lib/route-guard";

export const dynamic = "force-dynamic";

/** POST {email, password}: logs in against the backend and stores the access token in an httpOnly cookie.
 * When MFA is enabled the challenge is kept in a short-lived httpOnly cookie; the browser only learns `mfa_required`. */
export async function POST(req: NextRequest) {
  const bad = rejectCrossOrigin(req);
  if (bad) return bad;
  const body = await readJson(req);
  if (!body || typeof body.email !== "string" || typeof body.password !== "string") {
    return NextResponse.json({ detail: "email and password required" }, { status: 422 });
  }
  let r: Response;
  try {
    r = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ email: body.email, password: body.password }),
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ detail: "API unreachable" }, { status: 503 });
  }
  const data = await r.json().catch(() => ({}));
  if (!r.ok) return NextResponse.json({ detail: data.detail ?? "Login failed" }, { status: r.status });
  if (data.mfa_required && typeof data.challenge === "string") {
    const res = NextResponse.json({ mfa_required: true });
    res.cookies.set(MFA_COOKIE, data.challenge, cookieOptions(300));
    return res;
  }
  if (typeof data.access_token !== "string") return NextResponse.json({ detail: "Unexpected response" }, { status: 502 });
  const res = NextResponse.json({ ok: true });
  res.cookies.set(SESSION_COOKIE, data.access_token, cookieOptions(Number(data.expires_in) || 3600));
  res.cookies.delete(MFA_COOKIE);
  return res;
}
