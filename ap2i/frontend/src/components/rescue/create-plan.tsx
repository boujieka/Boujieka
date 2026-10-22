"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Field, Input } from "@/components/ui/form";
import { apiSend } from "../download";
import { useI18n } from "../i18n-provider";

export function CreatePlan({ initialProject, hasOrg }: { initialProject?: string; hasOrg: boolean }) {
  const { d } = useI18n();
  const router = useRouter();
  const [project, setProject] = useState(initialProject ?? "");
  const [priv, setPriv] = useState(hasOrg);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      setBusy(true);
      setErr(null);
      const r = await apiSend<{ id: number }>("rescue/plans", "POST", { project: project.trim(), private: priv });
      setBusy(false);
      if (r.ok && r.data) router.push(`/rescue/plans/${r.data.id}`);
      else setErr(`${r.status}: ${r.error}`);
    }}>
      <Field label={d.rescue.projectRef} htmlFor="plan-project">
        <Input id="plan-project" required value={project} onChange={(e) => setProject(e.target.value)} placeholder="AP2I-CMR-ENERGY-000001" />
      </Field>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" checked={priv} onChange={(e) => setPriv(e.target.checked)} className="h-4 w-4 accent-[#082B50]" />
        {d.rescue.private}
      </label>
      <Button type="submit" disabled={busy || !project.trim()}>{busy ? d.common.loading : d.rescue.create}</Button>
      {err ? <p role="alert" className="text-sm text-danger break-anywhere">{err}</p> : null}
    </form>
  );
}
