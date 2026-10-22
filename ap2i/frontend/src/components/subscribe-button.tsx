"use client";

import { useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { interpolate } from "@/i18n";
import { useI18n } from "./i18n-provider";

/** POST /billing/checkout. Online payment is not activated: the API answers 402 and the message is shown as is. */
export function SubscribeButton({ plan, loggedIn }: { plan: string; loggedIn: boolean }) {
  const { d } = useI18n();
  const [res, setRes] = useState<{ status: number; message: string; id?: number } | null>(null);
  const [busy, setBusy] = useState(false);
  if (!loggedIn) return <a className="link text-sm" href={`/login?next=/pricing`}>{d.pricing.loginToSubscribe}</a>;
  return (
    <div className="space-y-2">
      <Button disabled={busy} onClick={async () => {
        setBusy(true);
        const r = await fetch("/api/proxy/billing/checkout", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ plan }) });
        const body = await r.json().catch(() => null);
        const detail = body?.detail;
        setRes({ status: r.status, message: typeof detail === "string" ? detail : detail?.message ?? JSON.stringify(body), id: detail?.subscription_request_id });
        setBusy(false);
      }}>{d.pricing.subscribe}</Button>
      {res ? (
        <Alert tone={res.status === 402 ? "warning" : res.status < 300 ? "success" : "danger"} title={`${d.pricing.paymentNote} (HTTP ${res.status})`}>
          <p>“{res.message}”</p>
          {res.id ? <p className="mt-1">{interpolate(d.pricing.requestRecorded, { id: res.id })}</p> : null}
        </Alert>
      ) : null}
    </div>
  );
}
