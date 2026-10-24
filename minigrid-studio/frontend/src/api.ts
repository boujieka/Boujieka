export interface Indicator { value: number | null; unit: string; label: string; source: string; derived: boolean; experimental: boolean }
export interface Run { id: string; status: string; error: string; result: { kpis: Record<string, Indicator>; warnings: string[]; failed_checks: string[] } }
export interface Project { id: string; org_id: string; name: string; country: string }
export interface Version { id: string; scenario: string; version: number; status: string; solver_method: string }
export interface Me { email: string; memberships: { org_id: string; organization: string; role: string }[] }

export class Api {
  constructor(private token: string | null) {}

  private async req<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (this.token) headers.Authorization = `Bearer ${this.token}`;
    const r = await fetch(`/api/v1${path}`, { ...init, headers });
    if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
    return r.status === 204 ? (undefined as T) : r.json();
  }

  login(email: string, password: string) {
    return this.req<{ access_token: string }>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
  }
  me() { return this.req<Me>("/auth/me"); }
  logout() { return this.req<void>("/auth/logout", { method: "POST" }); }
  projects() { return this.req<Project[]>("/projects"); }
  versions(projectId: string) { return this.req<Version[]>(`/projects/${projectId}/versions`); }
  newVersion(projectId: string) {
    return this.req<Version>(`/projects/${projectId}/versions`, { method: "POST", body: JSON.stringify({ template: "demo_fictitious" }) });
  }
  run(versionId: string) { return this.req<Run>(`/versions/${versionId}/runs`, { method: "POST", body: "{}" }); }
}
