import { NextResponse, type NextRequest } from "next/server";
import { LOCALE_COOKIE, normalizeLocale } from "@/i18n";
import { readJson, rejectCrossOrigin } from "@/lib/route-guard";

export const dynamic = "force-dynamic";

/** POST {locale}: persists the UI language in a cookie (not httpOnly-sensitive, but set server-side). */
export async function POST(req: NextRequest) {
  const bad = rejectCrossOrigin(req);
  if (bad) return bad;
  const body = await readJson(req);
  const locale = normalizeLocale(typeof body?.locale === "string" ? body.locale : null);
  const res = NextResponse.json({ locale });
  res.cookies.set(LOCALE_COOKIE, locale, {
    httpOnly: false, sameSite: "lax", path: "/", maxAge: 60 * 60 * 24 * 365, secure: process.env.NODE_ENV === "production" && process.env.AP2I_INSECURE_COOKIES !== "1",
  });
  return res;
}
