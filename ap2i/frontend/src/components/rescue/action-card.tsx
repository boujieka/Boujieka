"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Field, Input, Select, Textarea } from "@/components/ui/form";
import { NatureBadge } from "@/components/badges";
import { Amount, DateV, V } from "@/components/value";
import { label } from "@/i18n";
import type { RescueAction } from "@/lib/types";
import { apiSend } from "../download";
import { useI18n } from "../i18n-provider";

const EDITABLE = ["recommended_action", "responsible_institution", "priority", "estimated_timeframe", "indicative_budget", "budget_currency", "expected_result", "monitoring_indicator", "assigned_to", "due_date"] as const;
type Editable = (typeof EDITABLE)[number];

/** Renders free-form JSON fields (contributing factors, dependencies) verbatim: strings as-is, lists as lists. */
function Verbatim({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === "") return <V value={null} />;
  if (typeof value === "string") return <span className="whitespace-pre-line">{value}</span>;
  if (Array.isArray(value)) return value.length ? <ul className="list-disc pl-5">{value.map((v, i) => <li key={i}><Verbatim value={v} /></li>)}</ul> : <V value={null} />;
  if (typeof value === "object") return <ul className="list-disc pl-5">{Object.entries(value as Record<string, unknown>).map(([k, v]) => <li key={k}><span className="text-muted">{k}:</span> <Verbatim value={v} /></li>)}</ul>;
  return <span>{String(value)}</span>;
}

export function ActionCard({ a }: { a: RescueAction }) {
  const { d } = useI18n();
  const router = useRouter();
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState<Record<Editable, string>>(() => Object.fromEntries(EDITABLE.map((k) => [k, (a[k] as string | null) ?? ""])) as Record<Editable, string>);
  const [pStatus, setPStatus] = useState(a.implementation_status);
  const [pNote, setPNote] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const approved = a.approval_status === "approved" || a.approval_status === "modified";

  async function decide(decision: "approved" | "rejected" | "modified") {
    setBusy(true);
    const changes: Record<string, string | null> = {};
    if (decision === "modified") for (const k of EDITABLE) if ((form[k] || "") !== ((a[k] as string | null) ?? "")) changes[k] = form[k] === "" ? null : form[k];
    const r = await apiSend(`rescue/actions/${a.id}/decision`, "POST", { decision, changes });
    setBusy(false);
    setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
    if (r.ok) {
      setEditing(false);
      router.refresh();
    }
  }
  async function progress(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    const r = await apiSend(`rescue/actions/${a.id}/progress`, "POST", { status: pStatus, note: pNote || null });
    setBusy(false);
    setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
    if (r.ok) {
      setPNote("");
      router.refresh();
    }
  }

  const fields: [string, React.ReactNode][] = [
    [d.rescue.recommended, <V key="r" value={a.recommended_action} />],
    [d.rescue.responsible, <V key="s" value={a.responsible_institution} />],
    [d.rescue.priority, <V key="p" value={a.priority} />],
    [d.rescue.timeframe, <V key="t" value={a.estimated_timeframe} />],
    [d.rescue.budget, <Amount key="b" value={a.indicative_budget} currency={a.budget_currency} />],
    [d.rescue.dependencies, <Verbatim key="dep" value={a.dependencies} />],
    [d.rescue.expectedResult, <V key="e" value={a.expected_result} />],
    [d.rescue.monitoring, <V key="m" value={a.monitoring_indicator} />],
    [d.rescue.assignedTo, <V key="a" value={a.assigned_to} />],
    [d.rescue.dueDate, <DateV key="du" value={a.due_date} />],
    [d.rescue.origin, <span key="o">{a.origin} <NatureBadge value={a.data_nature} /></span>],
  ];
  const labels: Record<Editable, string> = {
    recommended_action: d.rescue.recommended, responsible_institution: d.rescue.responsible, priority: d.rescue.priority, estimated_timeframe: d.rescue.timeframe,
    indicative_budget: d.rescue.budget, budget_currency: d.rescue.budgetCurrency, expected_result: d.rescue.expectedResult, monitoring_indicator: d.rescue.monitoring,
    assigned_to: d.rescue.assignedTo, due_date: d.rescue.dueDate,
  };

  return (
    <article className="rounded-lg border border-line bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-center gap-2">
        <h3 className="text-base font-semibold text-navy">{a.problem}</h3>
        <Badge tone={a.approval_status === "rejected" ? "danger" : approved ? "emerald" : "gold"}>{d.rescue.approval}: {label(d.rescue.approvalStatus, a.approval_status)}</Badge>
        <Badge tone="navy">{d.rescue.implementation}: {label(d.rescue.implStatus, a.implementation_status)}</Badge>
      </div>
      <div className="mt-3 grid gap-4 lg:grid-cols-2">
        <div className="min-w-0 space-y-3 text-sm">
          <div>
            <h4 className="font-semibold">{d.rescue.evidence}</h4>
            {a.evidence?.length ? (
              <ul className="mt-1 space-y-2">
                {a.evidence.map((ev, i) => (
                  <li key={i} className="rounded border border-line bg-gray-bg p-2 text-xs">
                    {Object.entries(ev).map(([k, v]) => (
                      <div key={k} className="break-anywhere"><span className="text-muted">{k}:</span>{" "}
                        {k === "source_record_ids" && Array.isArray(v) ? v.map((id) => <Link key={String(id)} className="link mr-1" href={`/sources/${id}`}>#{String(id)}</Link>)
                          : k === "alert_id" ? <span className="font-mono">{String(v)}</span> : <Verbatim value={v} />}
                      </div>
                    ))}
                  </li>
                ))}
              </ul>
            ) : <V value={null} />}
          </div>
          <div>
            <h4 className="font-semibold">{d.rescue.factors}</h4>
            <Verbatim value={a.contributing_factors} />
          </div>
          {a.progress_note ? <div><h4 className="font-semibold">{d.rescue.progressNote}</h4><pre className="whitespace-pre-wrap text-xs">{a.progress_note}</pre></div> : null}
        </div>
        <div className="min-w-0">
          {!editing ? (
            <dl className="divide-y divide-line text-sm">
              {fields.map(([k, v]) => <div key={k} className="grid grid-cols-[minmax(0,1fr)_minmax(0,1.5fr)] gap-2 py-1"><dt className="text-muted">{k}</dt><dd className="min-w-0 break-anywhere">{v}</dd></div>)}
            </dl>
          ) : (
            <div className="grid gap-2 sm:grid-cols-2">
              {EDITABLE.map((k) => (
                <Field key={k} label={labels[k]} htmlFor={`a${a.id}-${k}`} className={k === "recommended_action" || k === "expected_result" ? "sm:col-span-2" : ""}>
                  {k === "recommended_action" || k === "expected_result" ? (
                    <Textarea id={`a${a.id}-${k}`} rows={3} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />
                  ) : (
                    <Input id={`a${a.id}-${k}`} type={k === "due_date" ? "date" : k === "indicative_budget" ? "number" : "text"} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />
                  )}
                </Field>
              ))}
            </div>
          )}
          <div className="mt-3 flex flex-wrap gap-2">
            {!editing ? (
              <>
                <Button size="sm" variant="secondary" disabled={busy} onClick={() => decide("approved")}>{d.rescue.approve}</Button>
                <Button size="sm" variant="danger" disabled={busy} onClick={() => decide("rejected")}>{d.rescue.reject}</Button>
                <Button size="sm" variant="outline" disabled={busy} onClick={() => setEditing(true)}>{d.rescue.edit}</Button>
              </>
            ) : (
              <>
                <Button size="sm" disabled={busy} onClick={() => decide("modified")}>{d.rescue.modify}</Button>
                <Button size="sm" variant="outline" onClick={() => setEditing(false)}>{d.common.cancel}</Button>
              </>
            )}
          </div>
          <form onSubmit={progress} className="mt-4 rounded border border-line p-3">
            <h4 className="text-sm font-semibold">{d.rescue.progress}</h4>
            {!approved ? <p className="text-xs text-muted">{d.rescue.onlyApproved}</p> : null}
            <div className="mt-2 grid gap-2 sm:grid-cols-2">
              <Field label={d.rescue.progressStatus} htmlFor={`ps-${a.id}`}>
                <Select id={`ps-${a.id}`} value={pStatus} onChange={(e) => setPStatus(e.target.value)} disabled={!approved}>
                  {Object.entries(d.rescue.implStatus).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                </Select>
              </Field>
              <Field label={d.common.note} htmlFor={`pn-${a.id}`}>
                <Input id={`pn-${a.id}`} value={pNote} onChange={(e) => setPNote(e.target.value)} maxLength={2000} disabled={!approved} />
              </Field>
            </div>
            <Button size="sm" type="submit" className="mt-2" disabled={busy || !approved}>{d.rescue.addProgress}</Button>
          </form>
          {msg ? <p role="status" className="mt-2 text-xs break-anywhere">{msg}</p> : null}
        </div>
      </div>
    </article>
  );
}
