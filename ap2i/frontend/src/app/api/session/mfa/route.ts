import { NextResponse, type NextRequest } from "next/server";
import { API_URL, cookieOptions, MFA_COOKIE, SESSION_COOKIE } from "@/lib/session";
import { readJson, rejectCrossOrigin } from "@/lib/route-guard";

export const dynamic = "force-dynamic";

/** POST {code}: completes an MFA login using the challenge held in the httpOnly MFA cookie. */
export async function POST(req: NextRequest) {
  const bad = rejectCrossOrigin(req);
  if (bad) return bad;
  const challenge = req.cookies.get(MFA_COOKIE)?.value;
  const body = await readJson(req);
  if (!challenge) return NextResponse.json({ detail: "MFA challenge expired; log in again" }, { status: 401 });
  if (!body || typeof body.code !== "string") return NextResponse.json({ detail: "code required" }, { status: 422 });
  let r: Response;
  try {
    r = await fetch(`${API_URL}/auth/login/mfa`, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ challenge, code: body.code }),
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ detail: "API unreachable" }, { status: 503 });
  }
  const data = await r.json().catch(() => ({}));
  if (!r.ok || typeof data.access_token !== "string") {
    return NextResponse.json({ detail: data.detail ?? "Invalid code" }, { status: r.ok ? 502 : r.status });
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set(SESSION_COOKIE, data.access_token, cookieOptions(Number(data.expires_in) || 3600));
  res.cookies.delete(MFA_COOKIE);
  return res;
}
