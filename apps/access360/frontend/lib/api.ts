// Thin client for the same-origin /api proxy. Cookies are httpOnly; we never read or store tokens.

import type { DictKey } from "./i18n";

export interface FieldError {
  loc: (string | number)[];
  msg: string;
  type?: string;
}

export class ApiError extends Error {
  status: number;
  detail: unknown;
  headers: Headers;
  constructor(status: number, detail: unknown, headers: Headers) {
    super(ApiError.describe(detail, status));
    this.status = status;
    this.detail = detail;
    this.headers = headers;
  }

  static describe(detail: unknown, status: number): string {
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail
        .map((d) => {
          if (d && typeof d === "object" && "msg" in d) {
            const e = d as FieldError;
            const where = (e.loc || []).filter((x) => x !== "body").join(".");
            return where ? `${where}: ${e.msg}` : e.msg;
          }
          return String(d);
        })
        .join("; ");
    }
    return `Request failed (${status})`;
  }

  /** Validation errors keyed by dotted path without the leading "body". */
  fieldErrors(): Record<string, string> {
    const out: Record<string, string> = {};
    if (Array.isArray(this.detail)) {
      for (const d of this.detail) {
        if (d && typeof d === "object" && "loc" in d) {
          const e = d as FieldError;
          const path = (e.loc || []).filter((x) => x !== "body").join(".");
          out[path] = out[path] ? `${out[path]}; ${e.msg}` : e.msg;
        }
      }
    }
    return out;
  }
}

/**
 * The /api proxy could not reach the backend: network failure, a gateway status (502/503/504) without a
 * JSON body from the API, or a non-JSON 5xx page produced by the proxy itself. Genuine API errors (JSON
 * bodies with a `detail`, including a 503 the backend raises on purpose) stay ApiError.
 */
export class BackendUnavailableError extends Error {
  status: number;
  constructor(status: number) {
    super("The ACCESS360 service is not connected at the moment. Sign-in, projects and models are unavailable. The public pages still work.");
    this.name = "BackendUnavailableError";
    this.status = status;
  }
}

export const isBackendUnavailable = (e: unknown): e is BackendUnavailableError => e instanceof BackendUnavailableError;

/** User facing text for a caught error; the unavailability notice is translated. */
export function errorMessage(e: unknown, t: (k: DictKey) => string): string {
  if (isBackendUnavailable(e)) return t("common.backendUnavailable");
  return e instanceof Error ? e.message : String(e);
}

type Method = "GET" | "POST" | "PUT" | "DELETE";

export async function api<T>(path: string, opts: { method?: Method; body?: unknown; form?: FormData } = {}): Promise<T> {
  const method = opts.method || "GET";
  const headers: Record<string, string> = { Accept: "application/json" };
  // CSRF mitigation required by the backend on every state changing request
  if (method !== "GET") headers["X-Requested-With"] = "access360";
  let body: BodyInit | undefined;
  if (opts.form) {
    body = opts.form;
  } else if (opts.body !== undefined) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(opts.body);
  }
  let res: Response;
  try {
    res = await fetch(path, { method, headers, body, credentials: "include", cache: "no-store" });
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") throw e;
    throw new BackendUnavailableError(0);
  }
  if (res.status === 204) return undefined as T;
  const ct = res.headers.get("content-type") || "";
  const isJson = ct.includes("application/json");
  const data: unknown = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);
  if (!res.ok) {
    const fromApi = isJson && !!data && typeof data === "object" && "detail" in (data as Record<string, unknown>);
    if (!fromApi && res.status >= 500) throw new BackendUnavailableError(res.status);
    const detail = fromApi ? (data as { detail: unknown }).detail : data;
    throw new ApiError(res.status, detail, res.headers);
  }
  return data as T;
}

export const orgPath = (orgId: string, rest: string) => `/api/orgs/${encodeURIComponent(orgId)}${rest}`;
