import { FormEvent, useState } from "react";
import { canEdit, useApp } from "../context";
import { formatDate } from "../i18n";
import { href, navigate } from "../router";
import { errorText, Loading, StatusBadge, useLoad } from "../components/ui";

export function ProjectPage({ id }: { id: string }) {
  const { api, t, lang, notify, roleIn, demo } = useApp();
  const [project, reloadProject] = useLoad(() => api.project(id), [api, id]);
  const [versions, reloadVersions, loading] = useLoad(() => api.versions(id), [api, id]);
  const [templates] = useLoad(() => api.templates(), [api]);
  const [mode, setMode] = useState<"" | "template" | "import">("");
  const [busy, setBusy] = useState(false);
  if (!project) return <Loading />;
  const role = roleIn(project.org_id);
  const editable = canEdit(role) && !project.archived;

  async function createFromTemplate(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setBusy(true);
    try {
      const v = await api.createVersion(id, { scenario: String(f.get("scenario")), template: String(f.get("template")), note: String(f.get("note")) });
      navigate("versions", v.id);
    } catch (err) { notify(errorText(err), "error"); } finally { setBusy(false); }
  }
  async function importWorkbook(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const file = f.get("file") as File | null;
    if (!file || !file.size) return;
    setBusy(true);
    try {
      const v = await api.importXlsm(id, file, String(f.get("scenario")));
      navigate("versions", v.id);
    } catch (err) { notify(errorText(err), "error"); } finally { setBusy(false); }
  }
  async function patch(body: { archived?: boolean; restricted?: boolean }) {
    try { await api.patchProject(id, body); reloadProject(); reloadVersions(); } catch (err) { notify(errorText(err), "error"); }
  }

  const scenarioField = (
    <label className="field">{t("scenario")}
      <input name="scenario" required defaultValue="base" pattern="[A-Za-z0-9_\- ]{1,100}" maxLength={100} /></label>
  );
  return (
    <section>
      <p className="small"><a href={href("projects")}>← {t("projects")}</a></p>
      <div className="row">
        <h1 className="grow">{project.name}</h1>
        {project.archived && <span className="badge">{t("archived")}</span>}
        {project.restricted && <span className="badge">🔒 {t("restricted")}</span>}
      </div>
      <p className="muted">{project.country}{project.description && ` — ${project.description}`}</p>
      {role === "admin" && (
        <div className="row small no-print" style={{ marginBottom: 12 }}>
          <button onClick={() => patch({ archived: !project.archived })}>{project.archived ? t("unarchive") : t("archive")}</button>
          <label className="row"><input type="checkbox" checked={project.restricted} onChange={(e) => patch({ restricted: e.target.checked })} />{t("restricted")}</label>
        </div>
      )}
      {role === "investor" && <p className="small muted">{t("investorNote")}</p>}

      <div className="row"><h2 className="grow">{t("versions")}</h2>
        {editable && <>
          <button onClick={() => setMode(mode === "template" ? "" : "template")} aria-expanded={mode === "template"}>{t("fromTemplate")}</button>
          {!demo && <button onClick={() => setMode(mode === "import" ? "" : "import")} aria-expanded={mode === "import"}>{t("import")}</button>}
        </>}
      </div>
      {mode === "template" && (
        <form className="card stack" onSubmit={createFromTemplate}>
          {scenarioField}
          <label className="field">{t("template")}
            <select name="template">{(templates ?? []).map((tp) => <option key={tp.name} value={tp.name}>{tp.name} — {tp.description}</option>)}</select></label>
          <label className="field">{t("note")}<input name="note" maxLength={5000} /></label>
          <div className="row"><button className="primary" type="submit" disabled={busy}>{t("create")}</button></div>
        </form>
      )}
      {mode === "import" && (
        <form className="card stack" onSubmit={importWorkbook}>
          <p className="small muted">{t("importNote")}</p>
          {scenarioField}
          <label className="field">{t("importWorkbook")}<input name="file" type="file" accept=".xlsm,.xlsx" required /></label>
          <div className="row"><button className="primary" type="submit" disabled={busy}>{busy ? t("loading") : t("import")}</button></div>
        </form>
      )}
      {loading && !versions ? <Loading /> : (
        <div className="card scroll-x">
          <table className="data">
            <thead><tr>
              <th scope="col">{t("scenario")}</th><th scope="col">{t("version")}</th><th scope="col">{t("status")}</th>
              <th scope="col">{t("solver")}</th><th scope="col">{t("options")}</th><th scope="col">{t("createdAt")}</th><th scope="col">{t("note")}</th>
            </tr></thead>
            <tbody>{(versions ?? []).slice().sort((a, b) => a.scenario.localeCompare(b.scenario) || b.version - a.version).map((v) => (
              <tr key={v.id}>
                <td><a href={href("versions", v.id)}>{v.scenario}</a></td>
                <td className="num">v{v.version}</td>
                <td><StatusBadge status={v.status} /></td>
                <td className="small">{t(v.solver_method === "exact" ? "solver_exact" : "solver_excel_macros")}</td>
                <td className="small">{Object.entries(v.options).filter(([, on]) => on).map(([k]) => k).join(", ") || "—"}</td>
                <td className="small">{formatDate(v.created_at, lang)}</td>
                <td className="small">{v.note}{Object.keys(v.changes).length > 0 && <span className="muted"> ({Object.keys(v.changes).length} {t("changes")})</span>}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </section>
  );
}
