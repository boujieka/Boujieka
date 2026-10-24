import { FormEvent, useState } from "react";
import { canEdit, useApp } from "../context";
import { href, navigate } from "../router";
import { errorText, Loading, useLoad } from "../components/ui";

export function ProjectsPage() {
  const { api, me, t, notify, roleIn } = useApp();
  const [projects, reload, loading] = useLoad(() => api.projects(), [api]);
  const editableOrgs = me.memberships.filter((m) => canEdit(m.role));
  const [creating, setCreating] = useState(false);

  async function create(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    try {
      const p = await api.createProject({
        org_id: String(f.get("org")), name: String(f.get("name")), country: String(f.get("country")),
        description: String(f.get("description")), restricted: f.get("restricted") === "on",
      });
      reload();
      navigate("projects", p.id);
    } catch (err) { notify(errorText(err), "error"); }
  }

  const orgName = (id: string) => me.memberships.find((m) => m.org_id === id)?.organization ?? "";
  return (
    <section>
      <div className="row"><h1 className="grow">{t("projects")}</h1>
        {editableOrgs.length > 0 && <button className="primary" onClick={() => setCreating(!creating)} aria-expanded={creating}>{t("newProject")}</button>}
      </div>
      {me.memberships.every((m) => m.role === "investor") && <p className="small muted">{t("investorNote")}</p>}
      {creating && (
        <form className="card stack" onSubmit={create} aria-label={t("newProject")}>
          <label className="field">{t("organisation")}
            <select name="org">{editableOrgs.map((m) => <option key={m.org_id} value={m.org_id}>{m.organization}</option>)}</select></label>
          <label className="field">{t("name")}<input name="name" required maxLength={200} /></label>
          <label className="field">{t("country")}<input name="country" maxLength={100} /></label>
          <label className="field">{t("description")}<textarea name="description" rows={3} maxLength={5000} /></label>
          <label className="row small"><input type="checkbox" name="restricted" />{t("restricted")}</label>
          <div className="row"><button className="primary" type="submit">{t("create")}</button>
            <button type="button" onClick={() => setCreating(false)}>{t("cancel")}</button></div>
        </form>
      )}
      {loading && !projects ? <Loading /> : projects && projects.length === 0 ? <p className="muted">{t("noProjects")}</p> : (
        <div className="card scroll-x">
          <table className="data">
            <thead><tr><th scope="col">{t("project")}</th><th scope="col">{t("country")}</th><th scope="col">{t("organisation")}</th><th scope="col">{t("role")}</th><th scope="col">{t("status")}</th></tr></thead>
            <tbody>{(projects ?? []).map((p) => (
              <tr key={p.id}>
                <td><a href={href("projects", p.id)}>{p.name}</a>{p.description && <div className="small muted">{p.description.slice(0, 140)}</div>}</td>
                <td>{p.country}</td><td>{orgName(p.org_id)}</td>
                <td>{roleIn(p.org_id) ? t(`role_${roleIn(p.org_id)}` as never) : ""}</td>
                <td>{p.archived && <span className="badge">{t("archived")}</span>} {p.restricted && <span className="badge">🔒 {t("restricted")}</span>}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </section>
  );
}
