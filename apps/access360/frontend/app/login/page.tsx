"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState, type FormEvent } from "react";
import { AuthShell } from "@/components/auth-shell";
import { Field } from "@/components/field";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api, ApiError, isBackendUnavailable } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";

const DEMO_EMAIL = "demo@access360.example";

function LoginForm() {
  const { t } = useI18n();
  const router = useRouter();
  const params = useSearchParams();
  const demo = params.get("demo") === "1";
  const { refresh, markUnavailable } = useSession();
  const [email, setEmail] = useState(demo ? DEMO_EMAIL : "");
  const [password, setPassword] = useState("");
  const [totp, setTotp] = useState("");
  const [needTotp, setNeedTotp] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api("/api/auth/login", { method: "POST", body: { email, password, totp: needTotp ? totp : null } });
      await refresh();
      const next = params.get("next");
      router.push(next && next.startsWith("/app") ? next : "/app");
    } catch (err) {
      if (isBackendUnavailable(err)) {
        markUnavailable();
      } else if (err instanceof ApiError && err.status === 401 && err.headers.get("X-MFA-Required") === "1") {
        setNeedTotp(true);
        setError(null);
      } else {
        setError(err instanceof Error ? err.message : String(err));
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
      {demo ? <Alert variant="warning">{t("auth.demoHint")}</Alert> : null}
      <Field label={t("auth.email")}>
        {(id, d) => <Input id={id} aria-describedby={d} type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />}
      </Field>
      <Field label={t("auth.password")}>
        {(id, d) => (
          <Input id={id} aria-describedby={d} type="password" autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        )}
      </Field>
      {needTotp ? (
        <>
          <Alert variant="info">{t("auth.mfaRequired")}</Alert>
          <Field label={t("auth.totp")}>
            {(id, d) => (
              <Input id={id} aria-describedby={d} inputMode="numeric" autoComplete="one-time-code" maxLength={8} value={totp} onChange={(e) => setTotp(e.target.value.trim())} autoFocus />
            )}
          </Field>
        </>
      ) : null}
      {error ? <Alert variant="danger">{error}</Alert> : null}
      <Button type="submit" disabled={busy || !email || !password}>
        {busy ? t("common.loading") : t("auth.submitLogin")}
      </Button>
      <Link className="text-sm font-medium text-navy-700 underline-offset-4 hover:underline" href="/forgot-password">
        {t("auth.forgotLink")}
      </Link>
      <p className="text-sm text-muted-foreground">
        {t("auth.noAccount")}{" "}
        <Link className="font-medium text-navy-700 underline-offset-4 hover:underline" href="/register">
          {t("home.register")}
        </Link>
      </p>
    </form>
  );
}

export default function LoginPage() {
  const { t } = useI18n();
  return (
    <AuthShell title={t("auth.loginTitle")}>
      <Suspense fallback={null}>
        <LoginForm />
      </Suspense>
    </AuthShell>
  );
}
