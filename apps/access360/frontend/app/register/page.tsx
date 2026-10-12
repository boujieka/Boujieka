"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { AuthShell } from "@/components/auth-shell";
import { Field } from "@/components/field";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input, Select } from "@/components/ui/input";
import { api, ApiError } from "@/lib/api";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import { passwordOk } from "@/lib/utils";

const KINDS = ["individual", "developer", "investor", "government", "accredited"] as const;
type Kind = (typeof KINDS)[number];

export default function RegisterPage() {
  const { t, locale } = useI18n();
  const router = useRouter();
  const { refresh } = useSession();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", org_name: "", org_kind: "developer" as Kind, accept_terms: false });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const set = <K extends keyof typeof form>(k: K, v: (typeof form)[K]) => setForm((f) => ({ ...f, [k]: v }));

  async function submit(e: FormEvent) {
    e.preventDefault();
    const errs: Record<string, string> = {};
    if (!passwordOk(form.password)) errs.password = t("auth.passwordWeak");
    if (!form.accept_terms) errs.accept_terms = t("auth.termsRequired");
    setErrors(errs);
    if (Object.keys(errs).length) return;
    setBusy(true);
    setError(null);
    try {
      await api("/api/auth/register", { method: "POST", body: { ...form, locale } });
      await refresh();
      router.push("/app");
    } catch (err) {
      if (err instanceof ApiError) {
        setErrors(err.fieldErrors());
      }
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthShell title={t("auth.registerTitle")}>
      <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
        <Field label={t("auth.fullName")} error={errors.full_name}>
          {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} autoComplete="name" required value={form.full_name} onChange={(e) => set("full_name", e.target.value)} />}
        </Field>
        <Field label={t("auth.email")} error={errors.email}>
          {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} type="email" autoComplete="email" required value={form.email} onChange={(e) => set("email", e.target.value)} />}
        </Field>
        <Field label={t("auth.password")} error={errors.password} hint={t("auth.passwordRule")}>
          {(id, d, inv) => (
            <Input id={id} aria-describedby={d} aria-invalid={inv} type="password" autoComplete="new-password" required value={form.password} onChange={(e) => set("password", e.target.value)} />
          )}
        </Field>
        <Field label={t("auth.orgName")} error={errors.org_name}>
          {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} autoComplete="organization" required value={form.org_name} onChange={(e) => set("org_name", e.target.value)} />}
        </Field>
        <Field label={t("auth.orgKind")} error={errors.org_kind} hint={form.org_kind === "accredited" ? t("auth.accreditedNote") : undefined}>
          {(id, d) => (
            <Select id={id} aria-describedby={d} value={form.org_kind} onChange={(e) => set("org_kind", e.target.value as Kind)}>
              {KINDS.map((k) => (
                <option key={k} value={k}>
                  {t(`auth.kind.${k}` as DictKey)}
                </option>
              ))}
            </Select>
          )}
        </Field>
        <div className="flex flex-col gap-1">
          <label className="flex items-start gap-2 text-sm text-foreground">
            <input
              type="checkbox"
              className="mt-0.5 size-4 accent-emerald-600"
              checked={form.accept_terms}
              onChange={(e) => set("accept_terms", e.target.checked)}
              aria-invalid={!!errors.accept_terms}
              required
            />
            <span>{t("auth.terms")}</span>
          </label>
          {errors.accept_terms ? <p className="text-xs text-danger-700">{errors.accept_terms}</p> : null}
        </div>
        {error ? <Alert variant="danger">{error}</Alert> : null}
        <Button type="submit" disabled={busy}>
          {busy ? t("common.loading") : t("auth.submitRegister")}
        </Button>
        <p className="text-sm text-muted-foreground">
          {t("auth.haveAccount")}{" "}
          <Link className="font-medium text-navy-700 underline-offset-4 hover:underline" href="/login">
            {t("home.login")}
          </Link>
        </p>
      </form>
    </AuthShell>
  );
}
