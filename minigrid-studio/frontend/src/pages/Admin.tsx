import { FormEvent, useState } from "react";
import type { Invitation, Role } from "../api";
import { useApp } from "../context";
import { formatDate, Key } from "../i18n";
import { errorText, Loading, useLoad } from "../components/ui";

const ROLES: Role[] = ["admin", "analyst", "reviewer", "investor"];

export function AdminPage() {
  const { me, t } = useApp();
  const orgs = me.memberships.filter((m) => m.role === "admin");
  const [orgId, setOrgId] = useState(orgs[0]?.org_id ?? "");
  if (!orgs.length) return <p className="muted">—</p>;
  return (
    <section>
      <div className="row"><h1 className="grow">{t("admin")}</h1>
        {orgs.length > 1 && <select value={orgId} onChange={(e) => setOrgId(e.target.value)} aria-label={t("organisation")}>
          {orgs.map((o) => <option key={o.org_id} value={o.org_id}>{o.organization}</option>)}</select>}
      </div>
      <OrgAdmin orgId={orgId} key={orgId} />
    </section>
  );
}

function OrgAdmin({ orgId }: { orgId: string }) {
  const { api, t, lang, notify, me } = useApp();
  const [members, reloadMembers] = useLoad(() => api.members(orgId), [api, orgId]);
  const [invitations, reloadInvitations] = useLoad(() => api.invitations(orgId), [api, orgId]);
  const [audit, , auditLoading] = useLoad(() => api.audit(orgId, 300), [api, orgId]);
  const [created, setCreated] = useState<Invitation | null>(null);
  const [actionFilter, setActionFilter] = useState("");

  async function invite(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    try {
      setCreated(await api.invite(orgId, String(f.get("email")), String(f.get("role")) as Role));
      (e.target as HTMLFormElement).reset();
      reloadInvitations();
    } catch (err) { notify(errorText(err), "error"); }
  }
  async function act(fn: () => Promise<unknown>) {
    try { await fn(); reloadMembers(); } catch (err) { notify(errorText(err), "error"); }
  }
  const link = created?.token ? `${location.origin}${location.pathname}#/invite/${created.token}` : "";
  const nameOf = (id: string | null) => members?.find((m) => m.user_id === id)?.email ?? (id ? id.slice(0, 8) : "—");

  return <>
    <h2>{t("members")}</h2>
    {!members ? <Loading /> : (
      <div className="card scroll-x">
        <table className="data">
          <thead><tr><th scope="col">{t("name")}</th><th scope="col">{t("email")}</th><th scope="col">{t("role")}</th><th scope="col" /></tr></thead>
          <tbody>{members.map((m) => (
            <tr key={m.user_id}>
              <td>{m.name}</td><td>{m.email}</td>
              <td><select value={m.role} aria-label={`${t("role")} — ${m.email}`} onChange={(e) => act(() => api.setRole(orgId, m.user_id, e.target.value as Role))}>
                {ROLES.map((r) => <option key={r} value={r}>{t(`role_${r}` as Key)}</option>)}</select></td>
              <td>{m.user_id !== me.id && <button className="danger" onClick={() => {
                if (window.confirm(t("confirmRemove"))) act(() => api.removeMember(orgId, m.user_id));
              }}>{t("remove")}</button>}</td>
            </tr>
          ))}</tbody>
        </table>
      </div>
    )}

    <h2>{t("invitations")}</h2>
    <form className="card row" onSubmit={invite} aria-label={t("invite")}>
      <input name="email" type="email" required placeholder={t("email")} aria-label={t("email")} className="grow" />
      <select name="role" aria-label={t("role")} defaultValue="analyst">{ROLES.map((r) => <option key={r} value={r}>{t(`role_${r}` as Key)}</option>)}</select>
      <button className="primary" type="submit">{t("invite")}</button>
    </form>
    {created?.token && (
      <div className="card">
        <p className="small">{t("inviteToken")}</p>
        <div className="row"><input readOnly value={link} className="grow mono" aria-label="invitation link" onFocus={(e) => e.target.select()} />
          <button onClick={() => navigator.clipboard?.writeText(link)}>{t("copy")}</button></div>
      </div>
    )}
    {invitations && invitations.length > 0 && (
      <div className="card scroll-x">
        <table className="data">
          <thead><tr><th scope="col">{t("email")}</th><th scope="col">{t("role")}</th><th scope="col">{t("expires")}</th><th scope="col">{t("status")}</th></tr></thead>
          <tbody>{invitations.map((i) => (
            <tr key={i.id}><td>{i.email}</td><td>{t(`role_${i.role}` as Key)}</td><td className="small">{formatDate(i.expires_at, lang)}</td>
              <td>{i.accepted_at ? <span className="badge good">✓ {t("accepted")}</span> : <span className="badge">{t("pending")}</span>}</td></tr>
          ))}</tbody>
        </table>
      </div>
    )}

    <h2>{t("auditLog")}</h2>
    <input type="search" placeholder={t("search")} value={actionFilter} onChange={(e) => setActionFilter(e.target.value)} aria-label={t("search")} style={{ marginBottom: 8 }} />
    {auditLoading && !audit ? <Loading /> : (
      <div className="card scroll-x" style={{ maxHeight: 520, overflowY: "auto" }}>
        <table className="data">
          <thead><tr><th scope="col">{t("date")}</th><th scope="col">{t("user")}</th><th scope="col">{t("action")}</th><th scope="col">{t("entity")}</th></tr></thead>
          <tbody>{(audit ?? []).filter((e) => !actionFilter || `${e.action} ${e.entity_type} ${nameOf(e.user_id)}`.includes(actionFilter)).map((e) => (
            <tr key={e.id}><td className="small">{formatDate(e.created_at, lang)}</td><td className="small">{nameOf(e.user_id)}</td>
              <td className="mono">{e.action}</td><td className="small">{e.entity_type} <span className="mono">{e.entity_id.slice(0, 8)}</span></td></tr>
          ))}</tbody>
        </table>
      </div>
    )}
  </>;
}
