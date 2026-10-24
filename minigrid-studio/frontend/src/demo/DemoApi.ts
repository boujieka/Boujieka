// In-browser stand-in for the REST API: the engine runs in Pyodide (worker.ts) and projects,
// versions and runs are kept in this browser only (localStorage, memory if storage is blocked).
// Single local user, fictitious data, no accounts, no review between people, no server.
import { Api, ApiError, Comparison, EngineOption, FieldEntry, Labels, Me, Project, Run, Version, VersionDetail } from "../api";

const DEMO_ORG = "demo-local";
const KEY = "mgs-demo-v1";
const RUN_KEY = (id: string) => `mgs-demo-run-${id}`;
const MAX_RUNS = 40;

interface Store { projects: Project[]; versions: VersionDetail[]; runs: Omit<Run, "result">[] }
interface Meta { engine_version: string; labels: Labels; fields: FieldEntry[]; options: EngineOption[]; templates: { name: string; description: string }[] }

const uid = () => (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);
const now = () => new Date().toISOString();
const memory = new Map<string, string>();
const storage = {
  get(k: string): string | null { try { return localStorage.getItem(k) ?? memory.get(k) ?? null; } catch { return memory.get(k) ?? null; } },
  set(k: string, v: string) { try { localStorage.setItem(k, v); memory.delete(k); } catch { memory.set(k, v); } },
  del(k: string) { try { localStorage.removeItem(k); } catch { /* blocked */ } memory.delete(k); },
};

class Engine {
  private worker: Worker | null = null;
  private seq = 0;
  private pending = new Map<number, { resolve: (v: string) => void; reject: (e: Error) => void }>();
  call(fn: string, ...args: unknown[]): Promise<string> {
    if (!this.worker) {
      this.worker = new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
      this.worker.onmessage = (e: MessageEvent<{ id: number; ok: boolean; value?: string; error?: string }>) => {
        const p = this.pending.get(e.data.id);
        this.pending.delete(e.data.id);
        if (e.data.ok) p?.resolve(e.data.value!); else p?.reject(new Error(e.data.error));
      };
    }
    const id = ++this.seq;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.worker!.postMessage({ id, fn, args, base: import.meta.env.BASE_URL });
    });
  }
}

export class DemoApi extends Api {
  private engine = new Engine();
  private metaCache = new Map<string, Promise<Meta>>();
  private template: Promise<Record<string, unknown>> | null = null;

  constructor() { super(null); }

  private load(): Store {
    try { return JSON.parse(storage.get(KEY) ?? "") as Store; } catch { return { projects: [], versions: [], runs: [] }; }
  }
  private save(s: Store) { storage.set(KEY, JSON.stringify(s)); }
  private meta(lang: string): Promise<Meta> {
    if (!this.metaCache.has(lang)) this.metaCache.set(lang, this.engine.call("meta", lang).then((j) => JSON.parse(j) as Meta));
    return this.metaCache.get(lang)!;
  }
  private notFound(): never { throw new ApiError(404, "not found"); }
  private unavailable(): never {
    throw new ApiError(501, "Non disponible dans la démo navigateur / not available in the browser demo");
  }

  /** Removes everything this demo stored in the browser. */
  reset() {
    const s = this.load();
    s.runs.forEach((r) => storage.del(RUN_KEY(r.id)));
    storage.del(KEY);
  }

  // session: a single local user
  async login(): Promise<{ access_token: string }> { return { access_token: "demo" }; }
  async logout(): Promise<void> { /* nothing to revoke */ }
  async me(): Promise<Me> {
    return { id: "demo-user", email: "demo@local", name: "Démo / Demo", memberships: [{ org_id: DEMO_ORG, organization: "Démo locale", role: "analyst" }] };
  }

  // engine metadata
  async labels(lang: string) { return (await this.meta(lang)).labels; }
  async fields() { return (await this.meta("fr")).fields; }
  async options() { return (await this.meta("fr")).options; }
  async templates() { return (await this.meta("fr")).templates; }

  // projects
  async projects() { return this.load().projects; }
  async project(id: string) { return this.load().projects.find((p) => p.id === id) ?? this.notFound(); }
  async createProject(body: { org_id: string; name: string; country: string; description: string; restricted: boolean }) {
    const s = this.load();
    const p: Project = { id: uid(), org_id: DEMO_ORG, name: body.name, country: body.country, description: body.description,
      restricted: false, archived: false, created_at: now() };
    s.projects.push(p);
    this.save(s);
    return p;
  }
  async patchProject(id: string, body: Partial<Project>) {
    const s = this.load();
    const p = s.projects.find((x) => x.id === id) ?? this.notFound();
    Object.assign(p, body);
    this.save(s);
    return p;
  }

  // versions
  async versions(projectId: string): Promise<Version[]> {
    return this.load().versions.filter((v) => v.project_id === projectId).map(({ assumptions: _a, ...v }) => v);
  }
  async version(id: string) { return this.load().versions.find((v) => v.id === id) ?? this.notFound(); }
  private add(s: Store, v: Omit<VersionDetail, "id" | "version" | "created_at" | "content_hash" | "status" | "created_by"
    | "submitted_by" | "reviewed_by" | "reviewed_at" | "review_comment">): VersionDetail {
    const last = Math.max(0, ...s.versions.filter((x) => x.project_id === v.project_id && x.scenario === v.scenario).map((x) => x.version));
    const full: VersionDetail = { ...v, id: uid(), version: last + 1, created_at: now(), content_hash: "", status: "draft",
      created_by: "demo-user", submitted_by: null, reviewed_by: null, reviewed_at: null, review_comment: "" };
    s.versions.push(full);
    this.save(s);
    return full;
  }
  async createVersion(projectId: string, body: { scenario: string; template: string; options?: Record<string, boolean>; solver_method?: string; note?: string }) {
    if (body.template !== "demo_fictitious") this.unavailable();
    if (!/^[A-Za-z0-9_\- ]{1,100}$/.test(body.scenario)) throw new ApiError(422, "scenario: 1-100 letters, digits, spaces, - or _");
    this.template ??= fetch(`${import.meta.env.BASE_URL}py/template.json`).then((r) => r.json());
    const assumptions = { ...(await this.template) };
    delete assumptions._comment;
    return this.add(this.load(), { project_id: projectId, scenario: body.scenario, parent_id: null, options: body.options ?? {},
      solver_method: body.solver_method ?? "excel_macros", changes: {}, provenance: { template: body.template }, note: body.note ?? "", assumptions });
  }
  async importXlsm(): Promise<Version> { return this.unavailable(); }
  async revise(versionId: string, body: { changes: Record<string, unknown>; options?: Record<string, boolean>; solver_method?: string; note?: string }) {
    const parent = await this.version(versionId);
    const r = JSON.parse(await this.engine.call("revise", JSON.stringify(parent.assumptions), JSON.stringify(body.changes)));
    if (!r.ok) throw new ApiError(422, r.error);
    return this.add(this.load(), { project_id: parent.project_id, scenario: parent.scenario, parent_id: parent.id,
      options: body.options ?? parent.options, solver_method: body.solver_method ?? parent.solver_method,
      changes: body.changes, provenance: { source: "revision" }, note: body.note ?? "", assumptions: r.assumptions });
  }
  async submit(): Promise<Version> { return this.unavailable(); }
  async review(): Promise<Version> { return this.unavailable(); }

  // runs
  async run(versionId: string, perLot = false) {
    const v = await this.version(versionId);
    const out = JSON.parse(await this.engine.call("run", JSON.stringify(v.assumptions), JSON.stringify(v.options), v.solver_method, perLot));
    const run: Run = { id: uid(), version_id: v.id, engine_version: out.engine_version, status: out.status, inputs_hash: out.inputs_hash,
      error: out.error, duration_ms: out.duration_ms, created_at: now(), result: out.result };
    const s = this.load();
    s.runs.push({ ...run, result: undefined } as unknown as Omit<Run, "result">);
    while (s.runs.length > MAX_RUNS) storage.del(RUN_KEY(s.runs.shift()!.id));   // keep the most recent runs
    this.save(s);
    storage.set(RUN_KEY(run.id), JSON.stringify(run.result));
    return run;
  }
  async runs(versionId: string) {
    return Promise.all(this.load().runs.filter((r) => r.version_id === versionId).map((r) => this.getRun(r.id)));
  }
  async getRun(id: string): Promise<Run> {
    const r = this.load().runs.find((x) => x.id === id) ?? this.notFound();
    const result = JSON.parse(storage.get(RUN_KEY(id)) ?? "{}");
    return { ...r, result } as Run;
  }
  async compare(runIds: string[], lang: string): Promise<Comparison> {
    const items = [];
    for (const id of runIds) {
      const run = await this.getRun(id);
      const v = await this.version(run.version_id);
      const p = await this.project(v.project_id);
      items.push({ run, project: p.name, version: { scenario: v.scenario, version: v.version, status: v.status, assumptions: v.assumptions } });
    }
    return JSON.parse(await this.engine.call("compare", JSON.stringify(items), lang));
  }

  // exports
  private save_(blob: Blob, name: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  }
  private async context(runId: string) {
    const run = await this.getRun(runId);
    const v = await this.version(run.version_id);
    const p = await this.project(v.project_id);
    const base = `${p.name}-${v.scenario}-v${v.version}`.replace(/[^A-Za-z0-9_-]+/g, "-").slice(0, 80);
    return { run, v, p, base };
  }
  async exportXlsx(runId: string, lang: string) {
    const { run, v, p, base } = await this.context(runId);
    const b64 = await this.engine.call("studio_xlsx", JSON.stringify({ name: p.name, country: p.country }),
      JSON.stringify({ scenario: v.scenario, version: v.version, status: v.status, assumptions: v.assumptions }), JSON.stringify(run), lang);
    const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    this.save_(new Blob([bytes], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }), `${base}.xlsx`);
  }
  async exportPdf() { window.print(); }     // the browser's own "Save as PDF"
  async exportCsv(runId: string) {
    const { run, base } = await this.context(runId);
    const series = run.result.series;
    const esc = (x: unknown) => { const s = x === null || x === undefined ? "" : String(x); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    const lines = [["series", "label", "unit", "source", "derived", ...series.year.values].map(esc).join(",")];
    for (const [k, s] of Object.entries(series)) lines.push([k, s.label, s.unit, s.source, s.derived, ...s.values].map(esc).join(","));
    lines.push("", ["engine_version", run.engine_version, "status", run.status, "inputs_sha256", run.inputs_hash].map(esc).join(","));
    this.save_(new Blob([lines.join("\n")], { type: "text/csv" }), `${base}.csv`);
  }
  async exportCrossBoundary(): Promise<void> { return this.unavailable(); }

  // administration: not part of the single-user demo
  async members() { return this.unavailable(); }
  async invitations() { return this.unavailable(); }
  async audit() { return this.unavailable(); }
}
