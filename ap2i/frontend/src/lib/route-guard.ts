import "server-only";
import { NextResponse, type NextRequest } from "next/server";
import { isSameOrigin } from "./proxy-rules";

/** Returns a 403 response when a state-changing request does not come from this app's origin. */
export function rejectCrossOrigin(req: NextRequest): NextResponse | null {
  if (isSameOrigin(req.headers.get("origin"), req.headers.get("host"), req.headers.get("x-forwarded-host"))) return null;
  return NextResponse.json({ detail: "Cross-origin request refused" }, { status: 403 });
}

export async function readJson(req: NextRequest): Promise<Record<string, unknown> | null> {
  try {
    const b = await req.json();
    return b && typeof b === "object" ? (b as Record<string, unknown>) : null;
  } catch {
    return null;
  }
}
