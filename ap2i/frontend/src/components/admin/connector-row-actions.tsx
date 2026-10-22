"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/form";
import { apiSend } from "../download";
import { useI18n } from "../i18n-provider";

export function ConnectorActions({ k, enabled, schedule, status }: { k: string; enabled: boolean; schedule: string | null; status: string }) {
  const { d } = useI18n();
  const router = useRouter();
  const [cron, setCron] = useState(schedule ?? "");
  const [busy, setBusy] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  async function run(kind: string, path: string, method: string, body?: unknown) {
    setBusy(kind);
    setMsg(kind === "sync" ? d.admin.syncing : null);
    const r = await apiSend<Record<string, unknown>>(path, method, body);
    setBusy(null);
    setMsg(r.ok ? `${d.common.success}${kind === "sync" && r.data ? `: ${JSON.stringify(r.data).slice(0, 300)}` : ""}` : `${r.status}: ${r.error}`);
    if (r.ok) router.refresh();
  }
  return (
    <div className="min-w-64 space-y-2">
      <div className="flex flex-wrap gap-1">
        <Button size="sm" variant={enabled ? "outline" : "secondary"} disabled={!!busy || (!enabled && status === "not_implemented")} onClick={() => run("toggle", `admin/connectors/${k}`, "PATCH", { enabled: !enabled })}>
          {enabled ? d.admin.disable : d.admin.enable}
        </Button>
        {k !== "manual_upload" ? <Button size="sm" disabled={!!busy} onClick={() => run("sync", `admin/connectors/${k}/sync`, "POST")}>{busy === "sync" ? d.common.loading : d.admin.syncNow}</Button> : null}
      </div>
      <form className="flex gap-1" onSubmit={(e) => { e.preventDefault(); run("cron", `admin/connectors/${k}`, "PATCH", { schedule_cron: cron }); }}>
        <label className="sr-only" htmlFor={`cron-${k}`}>{d.admin.schedule}</label>
        <Input id={`cron-${k}`} value={cron} onChange={(e) => setCron(e.target.value)} placeholder="30 2 * * *" className="py-1 font-mono text-xs" />
        <Button size="sm" variant="outline" type="submit" disabled={!!busy}>{d.common.save}</Button>
      </form>
      {msg ? <p role="status" className="text-xs break-anywhere">{msg}</p> : null}
    </div>
  );
}
