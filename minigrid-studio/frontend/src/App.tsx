import React, { useEffect, useMemo, useState } from "react";
import { Api, Me, Project, Run, Version } from "./api";
import { formatValue, Lang, t } from "./i18n";

export default function App() {
  const [lang, setLang] = useState<Lang>("fr");
  const [token, setToken] = useState<string | null>(() => sessionStorage.getItem("mgs-token"));
  const api = useMemo(() => new Api(token), [token]);
  const [me, setMe] = useState<Me | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [project, setProject] = useState<Project | null>(null);
  const [versions, setVersions] = useState<Version[]>([]);
  const [run, setRun] = useState<Run | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    api.me().then(setMe).then(() => api.projects()).then(setProjects).catch((e) => setError(String(e)));
  }, [api, token]);

  useEffect(() => {
    if (project) api.versions(project.id).then(setVersions).catch((e) => setError(String(e)));
  }, [api, project]);

  async function onLogin(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    try {
      const r = await new Api(null).login(String(form.get("email")), String(form.get("password")));
      sessionStorage.setItem("mgs-token", r.access_token);
      setToken(r.access_token);
      setError("");
    } catch (e) { setError(String(e)); }
  }

  async function onLogout() {
    await api.logout().catch(() => undefined);
    sessionStorage.removeItem("mgs-token");
    setToken(null); setMe(null); setProjects([]); setProject(null); setRun(null);
  }

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 960, margin: "0 auto", padding: 16 }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: 22 }}>{t("title", lang)}</h1>
        <div>
          <button onClick={() => setLang(lang === "fr" ? "en" : "fr")}>{lang === "fr" ? "EN" : "FR"}</button>
          {me && <button onClick={onLogout} style={{ marginLeft: 8 }}>{t("logout", lang)}</button>}
        </div>
      </header>
      <p style={{ fontSize: 13, color: "#555" }}>{t("disclaimer", lang)}</p>
      {error && <p role="alert" style={{ color: "#a00" }}>{t("error", lang)}: {error}</p>}

      {!token && (
        <form onSubmit={onLogin} style={{ display: "grid", gap: 8, maxWidth: 320 }}>
          <label>{t("email", lang)} <input name="email" type="email" required /></label>
          <label>{t("password", lang)} <input name="password" type="password" required minLength={12} /></label>
          <button type="submit">{t("login", lang)}</button>
        </form>
      )}

      {me && (
        <section>
          <h2>{t("projects", lang)}</h2>
          <ul>{projects.map((p) => (
            <li key={p.id}><button onClick={() => { setProject(p); setRun(null); }}>{p.name}</button> {p.country}</li>
          ))}</ul>
        </section>
      )}

      {project && (
        <section>
          <h2>{t("versions", lang)} — {project.name}</h2>
          <button onClick={() => api.newVersion(project.id).then(() => api.versions(project.id)).then(setVersions)
            .catch((e) => setError(String(e)))}>{t("newVersion", lang)}</button>
          <ul>{versions.map((v) => (
            <li key={v.id}>{v.scenario} v{v.version} ({v.status}, {v.solver_method}){" "}
              <button onClick={() => api.run(v.id).then(setRun).catch((e) => setError(String(e)))}>{t("run", lang)}</button>
            </li>
          ))}</ul>
        </section>
      )}

      {run && run.result?.kpis && (
        <section>
          <h2>{t("indicators", lang)}</h2>
          <p><strong>{run.status === "reconciled-engine" ? t("status_reconciled", lang) : t("status_variant", lang)}</strong></p>
          <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 14 }}>
            <tbody>{Object.entries(run.result.kpis).map(([k, i]) => (
              <tr key={k} style={{ borderBottom: "1px solid #ddd" }}>
                <td>{i.label}</td>
                <td style={{ textAlign: "right" }}>{formatValue(i.value, i.unit, lang)}</td>
                <td style={{ color: "#666" }}>{t("source", lang)}: {i.source}
                  {i.derived && ` · ${t("derived", lang)}`}{i.experimental && ` · ${t("experimental", lang)}`}</td>
              </tr>
            ))}</tbody>
          </table>
          <h3>{t("warnings", lang)}</h3>
          {run.result.warnings.length ? <ul>{run.result.warnings.map((w) => <li key={w}>{w}</li>)}</ul> : <p>{t("none", lang)}</p>}
        </section>
      )}
      {run && run.status === "failed" && <p role="alert">{run.error}</p>}
    </main>
  );
}
