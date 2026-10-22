import { NextResponse, type NextRequest } from "next/server";
import { API_URL, SESSION_COOKIE } from "@/lib/session";
import { filterHeaders, FORWARD_REQUEST_HEADERS, FORWARD_RESPONSE_HEADERS, isSafePath, SAFE_METHODS } from "@/lib/proxy-rules";
import { rejectCrossOrigin } from "@/lib/route-guard";

export const dynamic = "force-dynamic";

/**
 * Generic authenticated proxy: /api/proxy/<path> → AP2I_API_URL/<path>.
 * - adds the bearer token from the httpOnly session cookie (the browser never sees it);
 * - refuses state-changing requests whose Origin is not this app (CSRF);
 * - forwards only an allowlist of request/response headers;
 * - streams request and response bodies (multipart uploads, PDF/XLSX/CSV downloads with Content-Disposition).
 */
async function handle(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  if (!isSafePath(path)) return NextResponse.json({ detail: "Path not allowed" }, { status: 400 });
  if (!SAFE_METHODS.has(req.method)) {
    const bad = rejectCrossOrigin(req);
    if (bad) return bad;
  }
  const target = `${API_URL}/${path.map(encodeURIComponent).join("/")}${req.nextUrl.search}`;
  const headers = filterHeaders(req.headers, FORWARD_REQUEST_HEADERS);
  const token = req.cookies.get(SESSION_COOKIE)?.value;
  if (token) headers.set("authorization", `Bearer ${token}`);
  const init: RequestInit & { duplex?: "half" } = { method: req.method, headers, cache: "no-store", redirect: "manual" };
  if (!SAFE_METHODS.has(req.method) && req.body) {
    init.body = req.body;
    init.duplex = "half";
  }
  let upstream: Response;
  try {
    upstream = await fetch(target, init);
  } catch {
    return NextResponse.json({ detail: "API unreachable" }, { status: 503 });
  }
  const out = filterHeaders(upstream.headers, FORWARD_RESPONSE_HEADERS);
  out.set("cache-control", "no-store");
  const res = new NextResponse(upstream.body, { status: upstream.status, headers: out });
  if (upstream.status === 401 && token) res.cookies.delete(SESSION_COOKIE);
  return res;
}

export { handle as GET, handle as POST, handle as PUT, handle as PATCH, handle as DELETE };
