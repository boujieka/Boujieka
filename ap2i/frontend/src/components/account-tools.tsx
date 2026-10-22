"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Field, Input } from "@/components/ui/form";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { DateV } from "@/components/value";
import { apiSend } from "./download";
import { useI18n } from "./i18n-provider";

export function MfaTools({ enabled }: { enabled: boolean }) {
  const { d } = useI18n();
  const router = useRouter();
  const [setup, setSetup] = useState<{ secret: string; otpauth_uri: string } | null>(null);
  const [code, setCode] = useState("");
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  if (enabled) {
    return (
      <form className="space-y-2" onSubmit={async (e) => {
        e.preventDefault();
        const r = await apiSend("auth/mfa/disable", "POST", { code });
        setMsg(r.ok ? { ok: true, text: d.common.success } : { ok: false, text: `${r.status}: ${r.error}` });
        if (r.ok) { await fetch("/api/session/logout", { method: "POST" }); router.push("/login"); router.refresh(); }
      }}>
        <Field label={d.auth.mfaCode} htmlFor="mfa-off"><Input id="mfa-off" inputMode="numeric" value={code} onChange={(e) => setCode(e.target.value)} required /></Field>
        <Button type="submit" variant="danger" size="sm">{d.auth.mfaDisable}</Button>
        {msg ? <Alert tone={msg.ok ? "success" : "danger"}>{msg.text}</Alert> : null}
      </form>
    );
  }
  return (
    <div className="space-y-3">
      {!setup ? (
        <Button size="sm" onClick={async () => {
          const r = await apiSend<{ secret: string; otpauth_uri: string }>("auth/mfa/setup", "POST");
          if (r.ok && r.data) setSetup(r.data);
          else setMsg({ ok: false, text: `${r.status}: ${r.error}` });
        }}>{d.auth.mfaSetup}</Button>
      ) : (
        <form className="space-y-2" onSubmit={async (e) => {
          e.preventDefault();
          const r = await apiSend("auth/mfa/enable", "POST", { code });
          setMsg(r.ok ? { ok: true, text: d.auth.mfaEnabledNote } : { ok: false, text: `${r.status}: ${r.error}` });
          if (r.ok) { await fetch("/api/session/logout", { method: "POST" }); setTimeout(() => { router.push("/login"); router.refresh(); }, 1500); }
        }}>
          <p className="text-xs font-semibold uppercase text-muted">{d.auth.mfaUri}</p>
          <code className="block rounded bg-gray-bg p-2 text-xs break-anywhere">{setup.otpauth_uri}</code>
          <p className="text-xs"><span className="text-muted">{d.auth.mfaSecret}:</span> <code className="break-anywhere">{setup.secret}</code></p>
          <Field label={d.auth.mfaCode} htmlFor="mfa-on"><Input id="mfa-on" inputMode="numeric" value={code} onChange={(e) => setCode(e.target.value)} required /></Field>
          <Button type="submit" size="sm">{d.auth.mfaEnable}</Button>
        </form>
      )}
      {msg ? <Alert tone={msg.ok ? "success" : "danger"}>{msg.text}</Alert> : null}
    </div>
  );
}

interface Key { id: number; name: string; prefix: string; created_at: string; revoked_at: string | null; last_used_at: string | null }

export function ApiKeys({ keys, canCreate }: { keys: Key[]; canCreate: boolean }) {
  const { d } = useI18n();
  const router = useRouter();
  const [name, setName] = useState("");
  const [created, setCreated] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  return (
    <div className="space-y-3">
      {keys.length ? (
        <Table caption={d.auth.apiKeys}>
          <THead><TR><TH>{d.common.name}</TH><TH>{d.auth.prefix}</TH><TH>{d.auth.created}</TH><TH>{d.auth.lastUsed}</TH><TH /></TR></THead>
          <TBody>{keys.map((k) => (
            <TR key={k.id}><TD>{k.name}</TD><TD className="font-mono text-xs">{k.prefix}</TD><TD><DateV value={k.created_at} /></TD><TD><DateV value={k.last_used_at} /></TD>
              <TD>{k.revoked_at ? <span className="text-xs text-muted">{d.auth.revoked} <DateV value={k.revoked_at} /></span> : <Button size="sm" variant="outline" onClick={async () => { await apiSend(`auth/api-keys/${k.id}`, "DELETE"); router.refresh(); }}>{d.auth.revoke}</Button>}</TD></TR>))}
          </TBody>
        </Table>
      ) : null}
      {canCreate ? (
        <form className="flex flex-wrap items-end gap-2" onSubmit={async (e) => {
          e.preventDefault();
          setErr(null);
          const r = await apiSend<{ key: string }>("auth/api-keys", "POST", { name });
          if (r.ok && r.data) { setCreated(r.data.key); setName(""); router.refresh(); } else setErr(`${r.status}: ${r.error}`);
        }}>
          <Field label={d.auth.apiKeyName} htmlFor="key-name"><Input id="key-name" required maxLength={100} value={name} onChange={(e) => setName(e.target.value)} /></Field>
          <Button type="submit" size="sm">{d.auth.createKey}</Button>
        </form>
      ) : <p className="text-sm text-muted">{d.auth.apiKeysEnterprise}</p>}
      {created ? <Alert tone="warning" title={d.auth.keyShownOnce}><code className="break-anywhere">{created}</code></Alert> : null}
      {err ? <Alert tone="danger">{err}</Alert> : null}
    </div>
  );
}
