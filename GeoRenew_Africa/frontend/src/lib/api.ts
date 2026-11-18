/** Client de l'API /api/v1. Les messages d'erreur du serveur sont rendus tels quels (en français). */

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

function errorMessage(body: unknown, status: number): { code: string; message: string } {
  const detail = (body as { detail?: unknown })?.detail;
  if (detail && typeof detail === "object" && !Array.isArray(detail) && "message" in detail) {
    const d = detail as { code?: string; message: string };
    return { code: d.code ?? "erreur", message: d.message };
  }
  if (Array.isArray(detail)) {
    // Erreurs de validation FastAPI
    const msg = detail
      .map((e: { loc?: unknown[]; msg?: string }) => `${(e.loc ?? []).slice(1).join(".")} : ${e.msg ?? ""}`)
      .join(" ; ");
    return { code: "validation", message: msg };
  }
  return { code: "erreur", message: `Erreur HTTP ${status}` };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api/v1${path}`, init);
  if (res.status === 204) return undefined as T;
  const text = await res.text();
  const body = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const { code, message } = errorMessage(body, res.status);
    throw new ApiError(res.status, code, message);
  }
  return body as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }),
  del: (path: string) => request<void>(path, { method: "DELETE" }),
  upload: <T>(path: string, form: FormData) => request<T>(path, { method: "POST", body: form }),
};

export { errorMessage };
