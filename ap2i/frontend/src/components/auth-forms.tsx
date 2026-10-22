"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Field, Input, Select } from "@/components/ui/form";
import { safeNext } from "@/lib/safe-next";
import { apiSend } from "./download";
import { useI18n } from "./i18n-provider";

function errText(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (detail && typeof detail === "object") {
    const o = detail as Record<string, unknown>;
    if (Array.isArray(o.password)) return o.password.join(" ");
    return JSON.stringify(detail);
  }
  return "Error";
}

export function LoginForm() {
  const { d } = useI18n();
  const router = useRouter();
  const sp = useSearchParams();
  const next = safeNext(sp.get("next"));
  const [step, setStep] = useState<"password" | "mfa">("password");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function post(url: string, body: unknown) {
    setBusy(true);
    setErr(null);
    const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
    const data = await r.json().catch(() => ({}));
    setBusy(false);
    if (!r.ok) {
      setErr(`${r.status}: ${errText(data.detail)}`);
      return null;
    }
    return data;
  }
  return (
    <div className="space-y-4">
      {sp.get("logged_out") ? <Alert tone="success">{d.auth.loggedOut}</Alert> : null}
      {step === "password" ? (
        <form className="space-y-3" onSubmit={async (e) => {
          e.preventDefault();
          const data = await post("/api/session/login", { email, password });
          if (!data) return;
          if (data.mfa_required) setStep("mfa");
          else { router.push(next); router.refresh(); }
        }}>
          <Field label={d.auth.email} htmlFor="email"><Input id="email" type="email" autoComplete="username" required value={email} onChange={(e) => setEmail(e.target.value)} /></Field>
          <Field label={d.auth.password} htmlFor="password"><Input id="password" type="password" autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} /></Field>
          <Button type="submit" disabled={busy} className="w-full">{busy ? d.common.loading : d.auth.submitLogin}</Button>
        </form>
      ) : (
        <form className="space-y-3" onSubmit={async (e) => {
          e.preventDefault();
          const data = await post("/api/session/mfa", { code: code.trim() });
          if (data) { router.push(next); router.refresh(); }
        }}>
          <h2 className="text-lg font-semibold text-navy">{d.auth.mfaTitle}</h2>
          <Field label={d.auth.mfaCode} htmlFor="code"><Input id="code" inputMode="numeric" autoComplete="one-time-code" pattern="[0-9]{6,8}" required value={code} onChange={(e) => setCode(e.target.value)} /></Field>
          <Button type="submit" disabled={busy} className="w-full">{d.auth.verify}</Button>
        </form>
      )}
      {err ? <Alert tone="danger">{err}</Alert> : null}
      <div className="flex flex-wrap justify-between gap-2 text-sm">
        <Link className="link" href="/forgot-password">{d.auth.forgot}</Link>
        <span>{d.auth.noAccount} <Link className="link" href="/register">{d.nav.register}</Link></span>
      </div>
    </div>
  );
}

export function RegisterForm() {
  const { d, locale } = useI18n();
  const [f, setF] = useState({ email: "", password: "", full_name: "", organization_name: "", locale });
  const [done, setDone] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  if (done) return <Alert tone="success">{d.auth.registered}</Alert>;
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setF({ ...f, [k]: e.target.value });
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      setBusy(true);
      setErr(null);
      const r = await apiSend("auth/register", "POST", { ...f, organization_name: f.organization_name || null });
      setBusy(false);
      if (r.ok) setDone(true);
      else setErr(`${r.status}: ${errText((r.data as { detail?: unknown } | null)?.detail ?? r.error)}`);
    }}>
      <Field label={d.auth.fullName} htmlFor="full_name"><Input id="full_name" required minLength={2} autoComplete="name" value={f.full_name} onChange={set("full_name")} /></Field>
      <Field label={d.auth.email} htmlFor="r-email"><Input id="r-email" type="email" required autoComplete="email" value={f.email} onChange={set("email")} /></Field>
      <Field label={d.auth.password} htmlFor="r-password" hint={d.auth.passwordRules}><Input id="r-password" type="password" required autoComplete="new-password" value={f.password} onChange={set("password")} /></Field>
      <Field label={`${d.auth.organization} (${d.common.optional})`} htmlFor="org"><Input id="org" autoComplete="organization" value={f.organization_name} onChange={set("organization_name")} /></Field>
      <Field label={d.auth.locale} htmlFor="r-locale"><Select id="r-locale" value={f.locale} onChange={set("locale")}><option value="fr">Français</option><option value="en">English</option></Select></Field>
      <Button type="submit" disabled={busy} className="w-full">{d.auth.submitRegister}</Button>
      {err ? <Alert tone="danger">{err}</Alert> : null}
    </form>
  );
}

export function VerifyEmail() {
  const { d } = useI18n();
  const sp = useSearchParams();
  const token = sp.get("token");
  const [state, setState] = useState<{ ok: boolean; msg: string } | null>(null);
  const started = useRef(false);
  useEffect(() => {
    if (!token || started.current) return;
    started.current = true;
    apiSend("auth/verify-email", "POST", { token }).then((r) => setState(r.ok ? { ok: true, msg: d.auth.verified } : { ok: false, msg: `${r.status}: ${r.error}` }));
  }, [token, d]);
  if (!token) return <Alert tone="danger">{d.auth.missingToken}</Alert>;
  if (!state) return <p>{d.auth.verifying}</p>;
  return <Alert tone={state.ok ? "success" : "danger"}>{state.msg} {state.ok ? <Link className="link" href="/login">{d.nav.login}</Link> : null}</Alert>;
}

export function ForgotForm() {
  const { d } = useI18n();
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      const r = await apiSend("auth/password/forgot", "POST", { email });
      setMsg(r.ok ? { ok: true, text: d.auth.resetSent } : { ok: false, text: `${r.status}: ${r.error}` });
    }}>
      <Field label={d.auth.email} htmlFor="f-email"><Input id="f-email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} /></Field>
      <Button type="submit" className="w-full">{d.auth.sendReset}</Button>
      {msg ? <Alert tone={msg.ok ? "success" : "danger"}>{msg.text}</Alert> : null}
    </form>
  );
}

export function ResetForm() {
  const { d } = useI18n();
  const sp = useSearchParams();
  const token = sp.get("token");
  const [pw, setPw] = useState("");
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  if (!token) return <Alert tone="danger">{d.auth.missingToken}</Alert>;
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      const r = await apiSend("auth/password/reset", "POST", { token, new_password: pw });
      setMsg(r.ok ? { ok: true, text: d.auth.resetDone } : { ok: false, text: `${r.status}: ${errText((r.data as { detail?: unknown } | null)?.detail ?? r.error)}` });
    }}>
      <Field label={d.auth.newPassword} htmlFor="new-pw" hint={d.auth.passwordRules}><Input id="new-pw" type="password" autoComplete="new-password" required value={pw} onChange={(e) => setPw(e.target.value)} /></Field>
      <Button type="submit" className="w-full">{d.common.save}</Button>
      {msg ? <Alert tone={msg.ok ? "success" : "danger"}>{msg.text} {msg.ok ? <Link className="link" href="/login">{d.nav.login}</Link> : null}</Alert> : null}
    </form>
  );
}
