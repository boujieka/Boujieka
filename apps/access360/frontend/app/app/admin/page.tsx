"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { KeyRound, ShieldCheck } from "lucide-react";
import { Field } from "@/components/field";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, orgPath } from "@/lib/api";
import { dateTime } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { AdminOrg, AuditRow, Member } from "@/lib/types";

function Members() {
  const { org, isAdmin } = useSession();
  const { t } = useI18n();
  const list = useApi<Member[]>(org ? orgPath(org.id, "/members") : null);
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("analyst");
  const [msg, setMsg] = useState<{ kind: "success" | "danger"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  async function add(e: FormEvent) {
    e.preventDefault();
    if (!org) return;
    setBusy(true);
    setMsg(null);
    try {
      await api(orgPath(org.id, "/members"), { method: "POST", body: { email, role } });
      setEmail("");
      setMsg({ kind: "success", text: t("common.saved") });
      list.reload();
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t("admin.members")}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        {list.loading && !list.data ? <Loading /> : null}
        {list.error ? <ErrorBox error={list.error} onRetry={list.reload} /> : null}
        {list.data ? (
          <TableWrap>
            <Table>
              <thead>
                <tr>
                  <Th>{t("common.name")}</Th>
                  <Th>{t("auth.email")}</Th>
                  <Th>{t("admin.role")}</Th>
                  <Th>{t("admin.mfa")}</Th>
                </tr>
              </thead>
              <tbody>
                {list.data.map((m) => (
                  <tr key={m.user_id}>
                    <Td>{m.full_name}</Td>
                    <Td className="break-all">{m.email}</Td>
                    <Td>
                      <Badge variant="navy">{m.role}</Badge>
                    </Td>
                    <Td>{m.mfa_enabled ? <Badge variant="success">{t("common.yes")}</Badge> : <Badge variant="neutral">{t("common.no")}</Badge>}</Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </TableWrap>
        ) : null}
        <form onSubmit={add} className="flex flex-col gap-3 rounded-md border border-border p-4">
          <div className="text-sm font-semibold text-navy-900">{t("admin.addMember")}</div>
          <p className="text-xs text-muted-foreground">{t("admin.addMemberNote")}</p>
          <div className="grid gap-3 sm:grid-cols-[minmax(0,1fr)_10rem_auto] sm:items-end">
            <Field label={t("auth.email")}>{(id) => <Input id={id} type="email" required value={email} disabled={!isAdmin} onChange={(e) => setEmail(e.target.value)} />}</Field>
            <Field label={t("admin.role")}>
              {(id) => (
                <Select id={id} value={role} disabled={!isAdmin} onChange={(e) => setRole(e.target.value)}>
                  <option value="admin">admin</option>
                  <option value="analyst">analyst</option>
                  <option value="viewer">viewer</option>
                </Select>
              )}
            </Field>
            <Button type="submit" disabled={!isAdmin || busy || !email}>
              {t("common.add")}
            </Button>
          </div>
          {!isAdmin ? <p className="text-xs text-muted-foreground">{t("common.notAllowed")}</p> : null}
          {msg ? <Alert variant={msg.kind}>{msg.text}</Alert> : null}
        </form>
      </CardContent>
    </Card>
  );
}

function Mfa() {
  const { me, refresh } = useSession();
  const { t } = useI18n();
  const [setup, setSetup] = useState<{ secret: string; otpauth_uri: string } | null>(null);
  const [code, setCode] = useState("");
  const [msg, setMsg] = useState<{ kind: "success" | "danger"; text: string } | null>(null);
  if (!me) return null;

  async function start() {
    setMsg(null);
    try {
      setSetup(await api<{ secret: string; otpauth_uri: string }>("/api/auth/mfa/setup", { method: "POST" }));
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    }
  }
  async function verify(e: FormEvent) {
    e.preventDefault();
    setMsg(null);
    try {
      await api("/api/auth/mfa/verify", { method: "POST", body: { code } });
      setSetup(null);
      setMsg({ kind: "success", text: t("admin.mfaDone") });
      await refresh();
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ShieldCheck className="size-4 text-emerald-700" aria-hidden /> {t("admin.mfaSetup")}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {me.mfa_enabled ? (
          <>
            <Alert variant="success">{t("admin.mfaEnabled")}</Alert>
            {!me.session_mfa ? <Alert variant="warning">{t("admin.sessionNoMfa")}</Alert> : null}
          </>
        ) : setup ? (
          <form onSubmit={verify} className="flex flex-col gap-3">
            <p className="text-sm text-muted-foreground">{t("admin.mfaHelp")}</p>
            <div>
              <div className="text-xs text-muted-foreground">{t("admin.mfaSecret")}</div>
              <code className="block break-all rounded bg-surface-muted px-2 py-1 font-mono text-sm" data-testid="mfa-secret">
                {setup.secret}
              </code>
            </div>
            <div>
              <div className="text-xs text-muted-foreground">{t("admin.mfaUri")}</div>
              <code className="block break-all rounded bg-surface-muted px-2 py-1 font-mono text-xs">{setup.otpauth_uri}</code>
            </div>
            <Field label={t("auth.totp")}>
              {(id) => <Input id={id} inputMode="numeric" autoComplete="one-time-code" maxLength={8} value={code} onChange={(e) => setCode(e.target.value.trim())} />}
            </Field>
            <Button type="submit" disabled={code.length < 6}>
              {t("admin.mfaVerify")}
            </Button>
          </form>
        ) : (
          <div>
            <Button onClick={start}>{t("admin.mfaStart")}</Button>
          </div>
        )}
        {msg ? <Alert variant={msg.kind}>{msg.text}</Alert> : null}
      </CardContent>
    </Card>
  );
}

function AccountSecurity() {
  const { me, refresh } = useSession();
  const { t } = useI18n();
  const router = useRouter();
  const [current, setCurrent] = useState("");
  const [pw, setPw] = useState("");
  const [pw2, setPw2] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ kind: "success" | "danger"; text: string } | null>(null);
  if (!me) return null;

  async function change(e: FormEvent) {
    e.preventDefault();
    setMsg(null);
    if (pw !== pw2) {
      setMsg({ kind: "danger", text: t("auth.passwordMismatch") });
      return;
    }
    setBusy(true);
    try {
      await api("/api/auth/password/change", { method: "POST", body: { current_password: current, new_password: pw } });
      setCurrent("");
      setPw("");
      setPw2("");
      setMsg({ kind: "success", text: t("admin.passwordChanged") });
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    } finally {
      setBusy(false);
    }
  }
  async function logoutAll() {
    setMsg(null);
    try {
      await api("/api/auth/logout-all", { method: "POST" });
      await refresh();
      router.push("/login");
    } catch (err) {
      setMsg({ kind: "danger", text: err instanceof Error ? err.message : String(err) });
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <KeyRound className="size-4 text-navy-700" aria-hidden /> {t("admin.account")}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <form onSubmit={change} className="flex flex-col gap-3" noValidate>
          <div className="text-sm font-semibold text-navy-900">{t("admin.changePassword")}</div>
          <div className="grid gap-3 sm:grid-cols-3">
            <Field label={t("admin.currentPassword")}>
              {(id) => <Input id={id} type="password" autoComplete="current-password" value={current} onChange={(e) => setCurrent(e.target.value)} />}
            </Field>
            <Field label={t("auth.newPassword")} hint={t("auth.passwordRule")}>
              {(id, d) => <Input id={id} aria-describedby={d} type="password" autoComplete="new-password" value={pw} onChange={(e) => setPw(e.target.value)} />}
            </Field>
            <Field label={t("auth.confirmPassword")}>
              {(id) => <Input id={id} type="password" autoComplete="new-password" value={pw2} onChange={(e) => setPw2(e.target.value)} />}
            </Field>
          </div>
          <div>
            <Button type="submit" disabled={busy || !current || !pw || !pw2}>
              {busy ? t("common.saving") : t("admin.changePassword")}
            </Button>
          </div>
        </form>
        <div className="flex flex-col gap-2 border-t border-border pt-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-muted-foreground">{t("admin.logoutAllHelp")}</p>
          <Button variant="outline" onClick={logoutAll}>
            {t("admin.logoutAll")}
          </Button>
        </div>
        {msg ? <Alert variant={msg.kind}>{msg.text}</Alert> : null}
      </CardContent>
    </Card>
  );
}

function Audit() {
  const { org, isAdmin } = useSession();
  const { t, locale } = useI18n();
  const log = useApi<AuditRow[]>(org && isAdmin ? orgPath(org.id, "/audit") : null);
  return (
    <Card>
      <CardHeader>
        <CardTitle>{t("admin.audit")}</CardTitle>
      </CardHeader>
      <CardContent>
        {!isAdmin ? <p className="text-sm text-muted-foreground">{t("admin.auditAdminsOnly")}</p> : null}
        {log.loading && !log.data ? <Loading /> : null}
        {log.error ? <ErrorBox error={log.error} onRetry={log.reload} /> : null}
        {log.data ? (
          <TableWrap className="max-h-96">
            <Table className="text-xs">
              <thead className="sticky top-0 bg-surface">
                <tr>
                  <Th>{t("common.date")}</Th>
                  <Th>{t("admin.action")}</Th>
                  <Th>{t("admin.entity")}</Th>
                  <Th>Detail</Th>
                </tr>
              </thead>
              <tbody>
                {log.data.map((a, i) => (
                  <tr key={i}>
                    <Td className="whitespace-nowrap">{dateTime(a.at, locale)}</Td>
                    <Td>{a.action}</Td>
                    <Td>
                      {a.entity}
                      {a.entity_id ? <span className="block font-mono text-[10px] text-subtle-foreground">{a.entity_id}</span> : null}
                    </Td>
                    <Td className="max-w-80 break-all font-mono text-[11px] text-muted-foreground">{a.detail ? JSON.stringify(a.detail) : "–"}</Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </TableWrap>
        ) : null}
      </CardContent>
    </Card>
  );
}

function Platform() {
  const { t, locale } = useI18n();
  const orgs = useApi<AdminOrg[]>("/api/admin/organizations");
  const [msg, setMsg] = useState<string | null>(null);
  async function setStatus(o: AdminOrg, status: "verified" | "rejected") {
    setMsg(null);
    try {
      await api(`/api/admin/organizations/${o.id}/accreditation`, { method: "POST", body: { status, note: "" } });
      orgs.reload();
    } catch (err) {
      setMsg(err instanceof Error ? err.message : String(err));
    }
  }
  return (
    <Card>
      <CardHeader>
        <CardTitle>{t("admin.platform")}</CardTitle>
        <CardDescription>{t("admin.organisations")}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {msg ? <Alert variant="danger">{msg}</Alert> : null}
        {orgs.loading && !orgs.data ? <Loading /> : null}
        {orgs.error ? <ErrorBox error={orgs.error} onRetry={orgs.reload} /> : null}
        {orgs.data ? (
          <TableWrap>
            <Table className="text-xs">
              <thead>
                <tr>
                  <Th>{t("common.name")}</Th>
                  <Th>{t("admin.kind")}</Th>
                  <Th>{t("admin.plan")}</Th>
                  <Th>{t("admin.accreditation")}</Th>
                  <Th>{t("common.date")}</Th>
                  <Th>{t("common.actions")}</Th>
                </tr>
              </thead>
              <tbody>
                {orgs.data.map((o) => (
                  <tr key={o.id}>
                    <Td>{o.name}</Td>
                    <Td>{o.kind}</Td>
                    <Td>{o.plan ?? "–"}</Td>
                    <Td>
                      <Badge variant={o.accreditation_status === "verified" ? "success" : o.accreditation_status === "rejected" ? "danger" : o.accreditation_status === "pending" ? "gold" : "neutral"}>{o.accreditation_status}</Badge>
                    </Td>
                    <Td className="whitespace-nowrap">{dateTime(o.created_at, locale)}</Td>
                    <Td>
                      {o.kind === "accredited" ? (
                        <span className="flex gap-1">
                          <Button size="sm" variant="accent" onClick={() => setStatus(o, "verified")} disabled={o.accreditation_status === "verified"}>
                            {t("admin.verify")}
                          </Button>
                          <Button size="sm" variant="outline" onClick={() => setStatus(o, "rejected")} disabled={o.accreditation_status === "rejected"}>
                            {t("admin.reject")}
                          </Button>
                        </span>
                      ) : (
                        "–"
                      )}
                    </Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </TableWrap>
        ) : null}
      </CardContent>
    </Card>
  );
}

export default function AdminPage() {
  const { me } = useSession();
  const { t } = useI18n();
  return (
    <>
      <PageHeader title={t("admin.title")} />
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
        <Members />
        <Mfa />
      </div>
      <div className="mt-6 flex flex-col gap-6">
        <AccountSecurity />
        <Audit />
        {me?.is_superadmin ? <Platform /> : null}
      </div>
    </>
  );
}
