"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useState, type FormEvent } from "react";
import { AuthShell } from "@/components/auth-shell";
import { Field } from "@/components/field";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n";

const linkCls = "text-sm font-medium text-navy-700 underline-offset-4 hover:underline";

function ResetForm() {
  const { t } = useI18n();
  const token = useSearchParams().get("token") ?? "";
  const [pw, setPw] = useState("");
  const [pw2, setPw2] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (!token) {
    return (
      <div className="flex flex-col gap-4">
        <Alert variant="warning">{t("auth.resetMissingToken")}</Alert>
        <Link className={linkCls} href="/forgot-password">
          {t("auth.requestNewLink")}
        </Link>
      </div>
    );
  }
  if (done) {
    return (
      <div className="flex flex-col gap-4">
        <Alert variant="success">{t("auth.resetDone")}</Alert>
        <Link className={linkCls} href="/login">
          {t("auth.backToLogin")}
        </Link>
      </div>
    );
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (pw !== pw2) {
      setError(t("auth.passwordMismatch"));
      return;
    }
    setBusy(true);
    setError(null);
    try {
      await api("/api/auth/password/reset", { method: "POST", body: { token, new_password: pw } });
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
      <Field label={t("auth.newPassword")} hint={t("auth.passwordRule")}>
        {(id, d) => <Input id={id} aria-describedby={d} type="password" autoComplete="new-password" required value={pw} onChange={(e) => setPw(e.target.value)} />}
      </Field>
      <Field label={t("auth.confirmPassword")}>
        {(id, d) => <Input id={id} aria-describedby={d} type="password" autoComplete="new-password" required value={pw2} onChange={(e) => setPw2(e.target.value)} />}
      </Field>
      {error ? <Alert variant="danger">{error}</Alert> : null}
      <Button type="submit" disabled={busy || !pw || !pw2}>
        {busy ? t("common.loading") : t("auth.resetSubmit")}
      </Button>
      <Link className={linkCls} href="/forgot-password">
        {t("auth.requestNewLink")}
      </Link>
    </form>
  );
}

export default function ResetPasswordPage() {
  const { t } = useI18n();
  return (
    <AuthShell title={t("auth.resetTitle")}>
      <Suspense fallback={null}>
        <ResetForm />
      </Suspense>
    </AuthShell>
  );
}
