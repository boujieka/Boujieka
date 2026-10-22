"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { downloadVia } from "./download";

export interface ReportRequest { report_type: string; format: "pdf" | "xlsx" | "csv"; country?: string; year_from?: number; year_to?: number; sector?: string; partner?: string }

/** POST /reports through the proxy and download the generated file. */
export function ReportButton({ request, label, busyLabel, variant = "secondary" }: { request: ReportRequest; label: string; busyLabel: string; variant?: "primary" | "secondary" | "outline" }) {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  return (
    <div className="min-w-0">
      <Button variant={variant} disabled={busy} onClick={async () => {
        setBusy(true);
        setErr(null);
        const r = await downloadVia("/api/proxy/reports", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(request) });
        if (!r.ok) setErr(`${r.status}: ${r.error}`);
        setBusy(false);
      }}>
        {busy ? busyLabel : label}
      </Button>
      {err ? <p role="alert" className="mt-1 text-xs text-danger break-anywhere">{err}</p> : null}
    </div>
  );
}
