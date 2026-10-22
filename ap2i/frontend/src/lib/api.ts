import "server-only";
import { cookies } from "next/headers";
import { API_URL, SESSION_COOKIE } from "./session";
import type { Me } from "./types";

export type ApiResult<T> = { ok: true; status: number; data: T } | { ok: false; status: number; error: string };

/** Server-side GET against the backend, with the session token (if any) and no caching. */
export async function apiGet<T>(path: string, opts: { auth?: boolean } = {}): Promise<ApiResult<T>> {
  const headers: Record<string, string> = { accept: "application/json" };
  if (opts.auth !== false) {
    const token = (await cookies()).get(SESSION_COOKIE)?.value;
    if (token) headers.authorization = `Bearer ${token}`;
  }
  try {
    const r = await fetch(`${API_URL}${path}`, { headers, cache: "no-store", signal: AbortSignal.timeout(60000) });
    const text = await r.text();
    let body: unknown = null;
    try {
      body = text ? JSON.parse(text) : null;
    } catch {
      body = text;
    }
    if (!r.ok) return { ok: false, status: r.status, error: errorMessage(body) };
    return { ok: true, status: r.status, data: body as T };
  } catch (e) {
    return { ok: false, status: 503, error: e instanceof Error ? e.message : "API unreachable" };
  }
}

export function errorMessage(body: unknown): string {
  if (body && typeof body === "object" && "detail" in body) {
    const d = (body as { detail: unknown }).detail;
    if (typeof d === "string") return d;
    if (d && typeof d === "object" && "message" in d && typeof (d as { message: unknown }).message === "string") return (d as { message: string }).message;
    return JSON.stringify(d);
  }
  return typeof body === "string" && body ? body.slice(0, 300) : "Request failed";
}

/** Current user (or null when anonymous / token expired). */
export async function getMe(): Promise<Me | null> {
  const token = (await cookies()).get(SESSION_COOKIE)?.value;
  if (!token) return null;
  const r = await apiGet<Me>("/auth/me");
  return r.ok ? r.data : null;
}

export { canAdmin, hasFeature, hasPermission } from "./perm";
