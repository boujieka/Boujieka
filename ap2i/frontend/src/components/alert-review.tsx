"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input, Select } from "@/components/ui/form";
import { apiSend } from "./download";
import { useI18n } from "./i18n-provider";

export function AlertReview({ id, current }: { id: number; current: string }) {
  const { d } = useI18n();
  const router = useRouter();
  const [status, setStatus] = useState(current);
  const [note, setNote] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <details className="text-xs">
      <summary className="cursor-pointer text-navy">{d.performance.review}</summary>
      <form className="mt-2 space-y-1" onSubmit={async (e) => {
        e.preventDefault();
        const r = await apiSend(`admin/alerts/${id}/review`, "POST", { review_status: status, note: note || null });
        setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
        if (r.ok) router.refresh();
      }}>
        <label className="sr-only" htmlFor={`rs-${id}`}>{d.performance.reviewStatus}</label>
        <Select id={`rs-${id}`} value={status} onChange={(e) => setStatus(e.target.value)} className="py-1 text-xs">
          {Object.entries(d.reviewStatus).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </Select>
        <label className="sr-only" htmlFor={`rn-${id}`}>{d.performance.reviewNote}</label>
        <Input id={`rn-${id}`} value={note} onChange={(e) => setNote(e.target.value)} placeholder={d.performance.reviewNote} className="py-1 text-xs" />
        <Button size="sm" type="submit">{d.common.save}</Button>
        {msg ? <p role="status">{msg}</p> : null}
      </form>
    </details>
  );
}
