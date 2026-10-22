"use client";

/** Downloads a file returned by the proxy (Content-Disposition preserved) without exposing any token. */
export async function downloadVia(url: string, init: RequestInit = {}): Promise<{ ok: boolean; status: number; error?: string }> {
  const r = await fetch(url, init);
  if (!r.ok) {
    const body = await r.json().catch(() => null);
    const detail = body?.detail;
    return { ok: false, status: r.status, error: typeof detail === "string" ? detail : detail?.message ?? JSON.stringify(detail ?? r.statusText) };
  }
  const blob = await r.blob();
  const cd = r.headers.get("content-disposition") ?? "";
  const m = /filename="?([^";]+)"?/i.exec(cd);
  const name = m?.[1] ?? "ap2i-download";
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  return { ok: true, status: r.status };
}

export async function apiSend<T = unknown>(path: string, method: string, body?: unknown): Promise<{ ok: boolean; status: number; data: T | null; error?: string }> {
  const r = await fetch(`/api/proxy/${path.replace(/^\//, "")}`, {
    method,
    headers: body !== undefined ? { "content-type": "application/json", accept: "application/json" } : { accept: "application/json" },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const data = await r.json().catch(() => null);
  if (!r.ok) {
    const detail = data?.detail;
    const error = typeof detail === "string" ? detail : detail?.message ?? (detail ? JSON.stringify(detail) : r.statusText || `HTTP ${r.status}`);
    return { ok: false, status: r.status, data, error };
  }
  return { ok: true, status: r.status, data: data as T };
}
