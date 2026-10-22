"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button, type ButtonProps } from "@/components/ui/button";
import { apiSend } from "../download";
import { useI18n } from "../i18n-provider";

/** Calls an API endpoint through the proxy, shows the result, refreshes the server data. */
export function ActionButton({ path, method = "POST", body, children, variant = "outline", confirm }: { path: string; method?: string; body?: unknown; children: React.ReactNode; variant?: ButtonProps["variant"]; confirm?: string }) {
  const { d } = useI18n();
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  return (
    <span className="inline-flex flex-col">
      <Button size="sm" variant={variant} disabled={busy} onClick={async () => {
        if (confirm && !window.confirm(confirm)) return;
        setBusy(true);
        const r = await apiSend(path, method, body);
        setBusy(false);
        setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
        if (r.ok) router.refresh();
      }}>{busy ? d.common.loading : children}</Button>
      {msg ? <span role="status" className="mt-1 max-w-56 text-xs break-anywhere">{msg}</span> : null}
    </span>
  );
}
