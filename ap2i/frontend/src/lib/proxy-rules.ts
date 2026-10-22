/** Pure rules used by the API proxy (kept framework-free so they can be unit tested). */

/** Request headers forwarded from the browser to the backend. Everything else is dropped. */
export const FORWARD_REQUEST_HEADERS = ["accept", "accept-language", "content-type", "if-none-match"] as const;

/** Response headers forwarded from the backend to the browser. */
export const FORWARD_RESPONSE_HEADERS = ["content-type", "content-disposition", "content-length", "x-report-id", "x-request-id", "etag"] as const;

/** Paths that must go through the dedicated session routes (they return or consume tokens). */
const BLOCKED = [/^auth\/login(\/|$)/, /^auth\/logout$/];

const SEGMENT = /^[A-Za-z0-9._~@:-]+$/;

export function isSafePath(segments: string[]): boolean {
  if (segments.length === 0 || segments.length > 12) return false;
  for (const s of segments) {
    if (!SEGMENT.test(s) || s === "." || s === "..") return false;
  }
  const joined = segments.join("/");
  return !BLOCKED.some((re) => re.test(joined));
}

export const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);

/**
 * CSRF protection for state-changing requests: the Origin header must be present and match the
 * host the request was addressed to (Host / X-Forwarded-Host). Requests without Origin are refused.
 */
export function isSameOrigin(origin: string | null, host: string | null, forwardedHost?: string | null): boolean {
  if (!origin || !host) return false;
  let o: URL;
  try {
    o = new URL(origin);
  } catch {
    return false;
  }
  const expected = (forwardedHost?.split(",")[0]?.trim() || host).toLowerCase();
  return o.host.toLowerCase() === expected;
}

export function filterHeaders(source: Headers, allow: readonly string[]): Headers {
  const out = new Headers();
  for (const name of allow) {
    const v = source.get(name);
    if (v !== null) out.set(name, v);
  }
  return out;
}
