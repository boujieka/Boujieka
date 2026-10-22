"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Field, Input, Select, Textarea } from "@/components/ui/form";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { apiSend } from "../download";
import { useI18n } from "../i18n-provider";

export function RolesEditor({ userId, roles, active, allRoles }: { userId: number; roles: string[]; active: boolean; allRoles: string[] }) {
  const { d } = useI18n();
  const router = useRouter();
  const [value, setValue] = useState(roles.join(", "));
  const [isActive, setIsActive] = useState(active);
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <form className="flex min-w-72 flex-col gap-1" onSubmit={async (e) => {
      e.preventDefault();
      const r = await apiSend(`admin/users/${userId}/roles`, "PUT", { roles: value.split(",").map((s) => s.trim()).filter(Boolean), is_active: isActive });
      setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
      if (r.ok) router.refresh();
    }}>
      <label className="sr-only" htmlFor={`roles-${userId}`}>{d.admin.roles}</label>
      <Input id={`roles-${userId}`} list="all-roles" value={value} onChange={(e) => setValue(e.target.value)} className="py-1 font-mono text-xs" />
      <datalist id="all-roles">{allRoles.map((r) => <option key={r} value={r} />)}</datalist>
      <label className="flex items-center gap-1 text-xs"><input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} />{d.admin.active}</label>
      <Button size="sm" type="submit">{d.admin.saveRoles}</Button>
      {msg ? <span role="status" className="text-xs break-anywhere">{msg}</span> : null}
    </form>
  );
}

export function OrgForm() {
  const { d } = useI18n();
  const router = useRouter();
  const [f, setF] = useState({ name: "", short_name: "", org_type: "institution", is_tenant: true, country_iso3: "CMR" });
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <form className="grid gap-3 sm:grid-cols-2" onSubmit={async (e) => {
      e.preventDefault();
      const r = await apiSend("admin/organizations", "POST", { ...f, short_name: f.short_name || null, country_iso3: f.country_iso3 || null });
      setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
      if (r.ok) router.refresh();
    }}>
      <Field label={d.common.name} htmlFor="o-name"><Input id="o-name" required minLength={2} value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} /></Field>
      <Field label={d.admin.shortName} htmlFor="o-short"><Input id="o-short" value={f.short_name} onChange={(e) => setF({ ...f, short_name: e.target.value })} /></Field>
      <Field label={d.admin.orgType} htmlFor="o-type"><Input id="o-type" value={f.org_type} onChange={(e) => setF({ ...f, org_type: e.target.value })} /></Field>
      <Field label={d.common.country} htmlFor="o-country"><Input id="o-country" maxLength={3} value={f.country_iso3} onChange={(e) => setF({ ...f, country_iso3: e.target.value.toUpperCase() })} /></Field>
      <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={f.is_tenant} onChange={(e) => setF({ ...f, is_tenant: e.target.checked })} />{d.admin.isTenant}</label>
      <div><Button type="submit">{d.admin.createOrg}</Button></div>
      {msg ? <p role="status" className="text-sm sm:col-span-2">{msg}</p> : null}
    </form>
  );
}

export function GrantForm({ plans }: { plans: string[] }) {
  const { d } = useI18n();
  const router = useRouter();
  const [f, setF] = useState({ plan: plans[1] ?? plans[0] ?? "", user_id: "", organization_id: "", ends_on: "", seats: "" });
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <form className="grid gap-3 sm:grid-cols-3" onSubmit={async (e) => {
      e.preventDefault();
      const r = await apiSend("admin/subscriptions", "POST", {
        plan: f.plan, user_id: f.user_id ? Number(f.user_id) : null, organization_id: f.organization_id ? Number(f.organization_id) : null,
        ends_on: f.ends_on || null, seats: f.seats ? Number(f.seats) : null,
      });
      setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
      if (r.ok) router.refresh();
    }}>
      <Field label="Plan" htmlFor="g-plan"><Select id="g-plan" value={f.plan} onChange={(e) => setF({ ...f, plan: e.target.value })}>{plans.map((p) => <option key={p}>{p}</option>)}</Select></Field>
      <Field label={d.admin.userId} htmlFor="g-user"><Input id="g-user" type="number" value={f.user_id} onChange={(e) => setF({ ...f, user_id: e.target.value })} /></Field>
      <Field label={d.admin.orgId} htmlFor="g-org"><Input id="g-org" type="number" value={f.organization_id} onChange={(e) => setF({ ...f, organization_id: e.target.value })} /></Field>
      <Field label={d.admin.endsOn} htmlFor="g-end"><Input id="g-end" type="date" value={f.ends_on} onChange={(e) => setF({ ...f, ends_on: e.target.value })} /></Field>
      <Field label={d.admin.seats} htmlFor="g-seats"><Input id="g-seats" type="number" value={f.seats} onChange={(e) => setF({ ...f, seats: e.target.value })} /></Field>
      <div className="flex items-end"><Button type="submit">{d.admin.grant}</Button></div>
      {msg ? <p role="status" className="text-sm sm:col-span-3">{msg}</p> : null}
    </form>
  );
}

interface UploadResult { imported?: number; errors?: { row: number; field: string; error: string }[] | Record<string, unknown>[]; message?: string; run_id?: number; status?: string; review?: number; failed?: number; visibility?: string }

export function UploadForm({ kind }: { kind: "projects" | "budget-lines" }) {
  const { d } = useI18n();
  const [file, setFile] = useState<File | null>(null);
  const [priv, setPriv] = useState(false);
  const [busy, setBusy] = useState(false);
  const [res, setRes] = useState<{ status: number; body: UploadResult | null; error?: string } | null>(null);
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      if (!file) return;
      setBusy(true);
      const fd = new FormData();
      fd.append("file", file);
      if (kind === "projects") fd.append("private", String(priv));
      const r = await fetch(`/api/proxy/uploads/${kind}`, { method: "POST", body: fd });
      const body = await r.json().catch(() => null);
      setBusy(false);
      setRes({ status: r.status, body: r.ok ? body : null, error: r.ok ? undefined : typeof body?.detail === "string" ? body.detail : JSON.stringify(body?.detail ?? body) });
    }}>
      <Field label={d.admin.file} htmlFor={`file-${kind}`}><Input id={`file-${kind}`} type="file" accept=".csv,.xlsx" required onChange={(e) => setFile(e.target.files?.[0] ?? null)} /></Field>
      {kind === "projects" ? <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={priv} onChange={(e) => setPriv(e.target.checked)} />{d.admin.privateImport}</label> : null}
      <Button type="submit" disabled={busy || !file}>{busy ? d.common.loading : d.admin.upload}</Button>
      {res ? (
        <div className="space-y-2">
          {res.error ? <Alert tone="danger">HTTP {res.status}: {res.error}</Alert> : (
            <Alert tone={res.body?.errors?.length ? "warning" : "success"}>
              {d.admin.imported}: {res.body?.imported ?? 0}{res.body?.run_id ? ` · run #${res.body.run_id} (${res.body.status}) · ${d.admin.reviewCount}: ${res.body.review} · ${d.admin.failed}: ${res.body.failed} · ${res.body.visibility}` : ""}
              {res.body?.message ? <p>{res.body.message}</p> : null}
            </Alert>
          )}
          {res.body?.errors?.length ? (
            <Table caption={d.admin.rowErrors}>
              <THead><TR><TH>{d.admin.row}</TH><TH>{d.project.field}</TH><TH>{d.common.error}</TH></TR></THead>
              <TBody>{res.body.errors.map((er, i) => { const e2 = er as Record<string, unknown>; return <TR key={i}><TD>{String(e2.row ?? "")}</TD><TD className="font-mono text-xs">{String(e2.field ?? "")}</TD><TD>{String(e2.error ?? JSON.stringify(er))}</TD></TR>; })}</TBody>
            </Table>
          ) : null}
        </div>
      ) : null}
    </form>
  );
}

export function DocumentUploadForm() {
  const { d } = useI18n();
  const [file, setFile] = useState<File | null>(null);
  const [project, setProject] = useState("");
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [busy, setBusy] = useState(false);
  const [res, setRes] = useState<{ ok: boolean; text: string } | null>(null);
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      if (!file) return;
      setBusy(true);
      const fd = new FormData();
      fd.append("file", file);
      fd.append("project", project.trim());
      fd.append("source_url", url.trim());
      if (title.trim()) fd.append("title", title.trim());
      const r = await fetch("/api/proxy/uploads/documents", { method: "POST", body: fd });
      const body = await r.json().catch(() => null);
      setBusy(false);
      if (!r.ok) {
        setRes({ ok: false, text: `HTTP ${r.status}: ${typeof body?.detail === "string" ? body.detail : JSON.stringify(body?.detail ?? body)}` });
      } else {
        const ratings = body?.ratings && Object.keys(body.ratings).length ? ` · ${JSON.stringify(body.ratings)}` : "";
        setRes({ ok: true, text: `#${body.document_id} · ${body.characters} car. · ${d.admin.parsedAs}: ${body.parsed_as ?? d.admin.textOnly}${ratings}` });
      }
    }}>
      <p className="text-xs text-muted">{d.admin.uploadDocumentIntro}</p>
      <Field label={d.admin.projectRef} htmlFor="doc-project"><Input id="doc-project" required placeholder="AP2I-CMR-…" value={project} onChange={(e) => setProject(e.target.value)} /></Field>
      <Field label={d.admin.sourceUrl} htmlFor="doc-url"><Input id="doc-url" type="url" required placeholder="https://www.afdb.org/…" value={url} onChange={(e) => setUrl(e.target.value)} /></Field>
      <Field label={d.admin.docTitle} htmlFor="doc-title"><Input id="doc-title" value={title} onChange={(e) => setTitle(e.target.value)} /></Field>
      <Field label={d.admin.file} htmlFor="doc-file"><Input id="doc-file" type="file" accept=".pdf,application/pdf" required onChange={(e) => setFile(e.target.files?.[0] ?? null)} /></Field>
      <Button type="submit" disabled={busy || !file}>{busy ? d.common.loading : d.admin.upload}</Button>
      {res ? <Alert tone={res.ok ? "success" : "danger"}>{res.text}</Alert> : null}
    </form>
  );
}

export function SettingForm({ group, initial }: { group: string; initial: unknown }) {
  const { d } = useI18n();
  const router = useRouter();
  const [text, setText] = useState(JSON.stringify(initial ?? {}, null, 2));
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <form className="space-y-2" onSubmit={async (e) => {
      e.preventDefault();
      let value: unknown;
      try { value = JSON.parse(text); } catch { setMsg(d.admin.invalidJson); return; }
      const r = await apiSend(`admin/settings/${group}`, "PUT", { value });
      setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
      if (r.ok) router.refresh();
    }}>
      <label htmlFor={`set-${group}`} className="text-sm font-semibold">{group}</label>
      <Textarea id={`set-${group}`} rows={5} value={text} onChange={(e) => setText(e.target.value)} className="font-mono text-xs" />
      <Button size="sm" type="submit">{d.common.save}</Button>
      {msg ? <p role="status" className="text-xs">{msg}</p> : null}
    </form>
  );
}
