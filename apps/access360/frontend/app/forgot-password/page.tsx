"use client";

import Link from "next/link";
import { useState, type FormEvent } from "react";
import { AuthShell } from "@/components/auth-shell";
import { Field } from "@/components/field";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api, isBackendUnavailable } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";

export default function ForgotPasswordPage() {
  const { t } = useI18n();
  const { markUnavailable } = useSession();
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      // the API answers the same way whether or not the account exists
      await api("/api/auth/password/forgot", { method: "POST", body: { email } });
      setSent(true);
    } catch (err) {
      if (isBackendUnavailable(err)) markUnavailable();
      else setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthShell title={t("auth.forgotTitle")}>
      {sent ? (
        <div className="flex flex-col gap-4">
          <Alert variant="success">{t("auth.forgotSent")}</Alert>
          <Link className="text-sm font-medium text-navy-700 underline-offset-4 hover:underline" href="/login">
            {t("auth.backToLogin")}
          </Link>
        </div>
      ) : (
        <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
          <p className="text-sm text-muted-foreground">{t("auth.forgotLead")}</p>
          <Field label={t("auth.email")}>
            {(id, d) => <Input id={id} aria-describedby={d} type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />}
          </Field>
          {error ? <Alert variant="danger">{error}</Alert> : null}
          <Button type="submit" disabled={busy || !email}>
            {busy ? t("common.loading") : t("auth.forgotSubmit")}
          </Button>
          <Link className="text-sm font-medium text-navy-700 underline-offset-4 hover:underline" href="/login">
            {t("auth.backToLogin")}
          </Link>
        </form>
      )}
    </AuthShell>
  );
}
