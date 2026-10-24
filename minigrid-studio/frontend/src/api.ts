// Typed client of the /api/v1 REST API. The token lives in sessionStorage (cleared with the tab).

export type Role = "admin" | "analyst" | "reviewer" | "investor";
export interface Indicator { value: number | null; unit: string; label: string; source: string; derived: boolean; experimental: boolean }
export interface Series { values: (number | null)[]; unit: string; label: string; source: string; derived: boolean }
export interface RunResult {
  status: string; options: string[]; solver: { method: string; converged: boolean; rounds: number };
  kpis: Record<string, Indicator>; series: Record<string, Series>; checks: Record<string, number>;
  failed_checks: string[]; warnings: string[]; pasted_values: Record<string, number | null>;
}
export interface Run {
  id: string; version_id: string; engine_version: string; status: string; inputs_hash: string;
  error: string; duration_ms: number; created_at: string; result: RunResult;
}
export interface Project {
  id: string; org_id: string; name: string; country: string; description: string;
  restricted: boolean; archived: boolean; created_at: string;
}
export interface Version {
  id: string; project_id: string; scenario: string; version: number; parent_id: string | null;
  options: Record<string, boolean>; solver_method: string; changes: Record<string, unknown>;
  provenance: Record<string, unknown>; note: string; content_hash: string; status: string;
  created_by: string; created_at: string; submitted_by: string | null; reviewed_by: string | null;
  reviewed_at: string | null; review_comment: string;
}
export interface VersionDetail extends Version { assumptions: Assumptions }
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Assumptions = Record<string, any>;
export interface Membership { org_id: string; organization: string; role: Role }
export interface Me { id: string; email: string; name: string; memberships: Membership[] }
export interface Member { user_id: string; email: string; name: string; role: Role }
export interface Invitation { id: string; email: string; role: Role; expires_at: string; accepted_at: string | null; token: string | null }
export interface AuditEvent { id: number; org_id: string | null; user_id: string | null; action: string; entity_type: string; entity_id: string; payload: Record<string, unknown>; created_at: string }
export interface FieldEntry { path: string; group: string; fr: string; en: string; unit: string; cell: string; doc: string; type?: string }
export interface EngineOption { name: string; default: boolean; doc: string }
export interface Labels {
  groups: Record<string, string>; kpis: Record<string, string>; series: Record<string, string>;
  checks: Record<string, string>; fields: Record<string, string>; units: Record<string, string>;
  message_rules: [string, string][];
}
export interface Comparison {
  runs: { run_id: string; project: string; scenario: string; version: number; status: string; version_status: string; options: string[]; solver: string }[];
  years: number[];
  kpis: Record<string, { label: string; unit: string; source: string; values: (number | null)[]; deltas: (number | null)[] }>;
  series: Record<string, { label: string; unit: string; values: (number | null)[][] }>;
  assumption_diffs: { path: string; label: string; values: unknown[] }[];
}

export class ApiError extends Error {
  constructor(public status: number, public detail: unknown) {
    super(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
}

export class Api {
  constructor(private token: string | null, private onUnauthorized: () => void = () => undefined) {}

  private async raw(path: string, init: RequestInit = {}, json = true): Promise<Response> {
    const headers: Record<string, string> = {};
    if (json && init.body !== undefined) headers["Content-Type"] = "application/json";
    if (this.token) headers.Authorization = `Bearer ${this.token}`;
    const r = await fetch(`/api/v1${path}`, { ...init, headers: { ...headers, ...(init.headers as Record<string, string>) } });
    if (!r.ok) {
      let detail: unknown = r.statusText;
      try { detail = (await r.json()).detail ?? detail; } catch { /* not JSON */ }
      if (r.status === 401 && this.token) this.onUnauthorized();
      throw new ApiError(r.status, detail);
    }
    return r;
  }

  private async req<T>(path: string, init: RequestInit = {}): Promise<T> {
    const r = await this.raw(path, init);
    return r.status === 204 ? (undefined as T) : r.json();
  }

  private post<T>(path: string, body: unknown = {}) { return this.req<T>(path, { method: "POST", body: JSON.stringify(body) }); }

  // auth
  login(email: string, password: string) { return this.post<{ access_token: string }>("/auth/login", { email, password }); }
  acceptInvitation(token: string, name?: string, password?: string) {
    return this.post<{ access_token: string }>("/auth/accept-invitation", { token, name, password });
  }
  me() { return this.req<Me>("/auth/me"); }
  logout() { return this.post<void>("/auth/logout"); }

  // organisation
  members(orgId: string) { return this.req<Member[]>(`/orgs/${orgId}/members`); }
  invite(orgId: string, email: string, role: Role) { return this.post<Invitation>(`/orgs/${orgId}/invitations`, { email, role }); }
  invitations(orgId: string) { return this.req<Invitation[]>(`/orgs/${orgId}/invitations`); }
  setRole(orgId: string, userId: string, role: Role) {
    return this.req<Member>(`/orgs/${orgId}/members/${userId}`, { method: "PUT", body: JSON.stringify({ role }) });
  }
  removeMember(orgId: string, userId: string) { return this.req<void>(`/orgs/${orgId}/members/${userId}`, { method: "DELETE" }); }
  audit(orgId: string, limit = 200) { return this.req<AuditEvent[]>(`/orgs/${orgId}/audit?limit=${limit}`); }

  // projects and versions
  projects() { return this.req<Project[]>("/projects"); }
  project(id: string) { return this.req<Project>(`/projects/${id}`); }
  createProject(body: { org_id: string; name: string; country: string; description: string; restricted: boolean }) {
    return this.post<Project>("/projects", body);
  }
  patchProject(id: string, body: Partial<Pick<Project, "name" | "country" | "description" | "restricted" | "archived">>) {
    return this.req<Project>(`/projects/${id}`, { method: "PATCH", body: JSON.stringify(body) });
  }
  versions(projectId: string) { return this.req<Version[]>(`/projects/${projectId}/versions`); }
  version(id: string) { return this.req<VersionDetail>(`/versions/${id}`); }
  createVersion(projectId: string, body: { scenario: string; template: string; options?: Record<string, boolean>; solver_method?: string; note?: string }) {
    return this.post<Version>(`/projects/${projectId}/versions`, body);
  }
  importXlsm(projectId: string, file: File, scenario: string) {
    const form = new FormData();
    form.append("file", file);
    form.append("scenario", scenario);
    return this.raw(`/projects/${projectId}/versions/import-xlsm`, { method: "POST", body: form }, false).then((r) => r.json() as Promise<Version>);
  }
  revise(versionId: string, body: { changes: Record<string, unknown>; options?: Record<string, boolean>; solver_method?: string; note?: string }) {
    return this.post<Version>(`/versions/${versionId}/revise`, body);
  }
  submit(versionId: string) { return this.post<Version>(`/versions/${versionId}/submit`); }
  review(versionId: string, decision: "approve" | "reject", comment: string) {
    return this.post<Version>(`/versions/${versionId}/review`, { decision, comment });
  }
  run(versionId: string, perLot = false) { return this.post<Run>(`/versions/${versionId}/runs`, { per_lot: perLot }); }
  runs(versionId: string) { return this.req<Run[]>(`/versions/${versionId}/runs`); }
  getRun(id: string) { return this.req<Run>(`/runs/${id}`); }
  compare(runIds: string[], lang: string) { return this.post<Comparison>("/compare", { run_ids: runIds, lang }); }

  // engine metadata
  labels(lang: string) { return this.req<Labels>(`/engine/labels?lang=${lang}`); }
  fields() { return this.req<FieldEntry[]>("/engine/fields"); }
  options() { return this.req<EngineOption[]>("/engine/options"); }
  templates() { return this.req<{ name: string; description: string }[]>("/engine/templates"); }

  // downloads: fetched with the bearer token, then saved through a temporary object URL
  async download(path: string, fallbackName: string, init: RequestInit = {}) {
    const r = await this.raw(path, init, !(init.body instanceof FormData));
    const cd = r.headers.get("Content-Disposition") ?? "";
    const name = /filename="([^"]+)"/.exec(cd)?.[1] ?? fallbackName;
    const url = URL.createObjectURL(await r.blob());
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  }
  exportXlsx(runId: string, lang: string) { return this.download(`/runs/${runId}/export.xlsx?lang=${lang}`, "export.xlsx"); }
  exportPdf(runId: string, lang: string) { return this.download(`/runs/${runId}/report.pdf?lang=${lang}`, "report.pdf"); }
  exportCsv(runId: string) { return this.download(`/runs/${runId}/series.csv`, "series.csv"); }
  exportCrossBoundary(runId: string, template: File) {
    const form = new FormData();
    form.append("template", template);
    return this.download(`/runs/${runId}/export-crossboundary`, "crossboundary.xlsm", { method: "POST", body: form });
  }
}
