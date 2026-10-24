import { useCallback, useEffect, useMemo, useState } from "react";
import { Api, FieldEntry, Labels, Me } from "./api";
import { AppContext } from "./context";
import { Key, Lang, t } from "./i18n";
import { href, useRoute } from "./router";
import { Alert, errorText } from "./components/ui";
import { LoginPage, InvitePage } from "./pages/Auth";
import { ProjectsPage } from "./pages/Projects";
import { ProjectPage } from "./pages/Project";
import { VersionPage } from "./pages/Version";
import { RunPage } from "./pages/Run";
import { ComparePage } from "./pages/Compare";
import { AdminPage } from "./pages/Admin";

const storage = {
  get: (k: string) => { try { return sessionStorage.getItem(k); } catch { return null; } },
  set: (k: string, v: string | null) => { try { if (v === null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, v); } catch { /* blocked */ } },
};
const prefLang = (): Lang => {
  try { const v = localStorage.getItem("mgs-lang"); if (v === "fr" || v === "en") return v; } catch { /* blocked */ }
  return "fr";
};

export default function App() {
  const route = useRoute();
  const [lang, setLangState] = useState<Lang>(prefLang);
  const [token, setToken] = useState<string | null>(() => storage.get("mgs-token"));
  const [me, setMe] = useState<Me | null>(null);
  const [labels, setLabels] = useState<Labels | null>(null);
  const [fields, setFields] = useState<FieldEntry[]>([]);
  const [toast, setToast] = useState<{ text: string; kind: "error" | "info" } | null>(null);
  const [compareRuns, setCompareRunsState] = useState<string[]>(() => JSON.parse(storage.get("mgs-compare") ?? "[]"));

  const signOut = useCallback((expired = false) => {
    storage.set("mgs-token", null);
    setToken(null);
    setMe(null);
    if (expired) setToast({ text: t("sessionExpired", lang), kind: "info" });
  }, [lang]);
  const api = useMemo(() => new Api(token, () => signOut(true)), [token, signOut]);
  const notify = useCallback((text: string, kind: "error" | "info" = "info") => setToast({ text, kind }), []);
  const setLang = (l: Lang) => {
    setLangState(l);
    try { localStorage.setItem("mgs-lang", l); } catch { /* blocked */ }
  };
  const setCompareRuns = (ids: string[]) => { setCompareRunsState(ids); storage.set("mgs-compare", JSON.stringify(ids)); };

  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  useEffect(() => {
    api.labels(lang).then(setLabels).catch((e) => notify(errorText(e), "error"));
  }, [api, lang, notify]);
  useEffect(() => {
    if (!token) return;
    api.me().then(setMe).catch(() => undefined);
    api.fields().then(setFields).catch(() => undefined);
  }, [api, token]);
  useEffect(() => {
    if (!toast) return;
    const id = setTimeout(() => setToast(null), toast.kind === "error" ? 12000 : 5000);
    return () => clearTimeout(id);
  }, [toast]);

  const onToken = (tok: string) => { storage.set("mgs-token", tok); setToken(tok); };
  const langSwitch = (
    <button onClick={() => setLang(lang === "fr" ? "en" : "fr")} aria-label={t("language", lang)}>
      {lang === "fr" ? "EN" : "FR"}
    </button>
  );
  const toastEl = toast && (
    <div className="toast" role={toast.kind === "error" ? "alert" : "status"}>
      <Alert kind={toast.kind === "error" ? "critical" : "info"}>
        <div className="row"><span className="grow">{toast.text}</span>
          <button className="link" onClick={() => setToast(null)}>{t("dismiss", lang)}</button></div>
      </Alert>
    </div>
  );

  if (route.name === "invite" && route.id && (!token || !me)) {
    return <main className="main" style={{ margin: "0 auto", maxWidth: 520 }}>
      <div className="row"><h1 className="grow">{t("title", lang)}</h1>{langSwitch}</div>
      <InvitePage token={route.id} lang={lang} api={api} signedIn={!!token} onToken={onToken} />{toastEl}
    </main>;
  }
  if (!token || !me || !labels) {
    return <main className="main" style={{ margin: "0 auto", maxWidth: 520 }}>
      <div className="row"><h1 className="grow">{t("title", lang)}</h1>{langSwitch}</div>
      <p className="disclaimer">{t("disclaimer", lang)}</p>
      {!token ? <LoginPage lang={lang} onToken={onToken} /> : <p className="muted">{t("loading", lang)}</p>}
      {toastEl}
    </main>;
  }

  const isAdmin = me.memberships.some((m) => m.role === "admin");
  const nav = [
    { name: "projects", label: t("projects", lang), match: ["projects", "project", "versions", "runs"] },
    { name: "compare", label: `${t("compare", lang)}${compareRuns.length ? ` (${compareRuns.length})` : ""}`, match: ["compare"] },
    ...(isAdmin ? [{ name: "admin", label: t("admin", lang), match: ["admin"] }] : []),
  ];
  let page: React.ReactNode;
  switch (route.name) {
    case "projects": page = route.id ? <ProjectPage id={route.id} /> : <ProjectsPage />; break;
    case "versions": page = route.id ? <VersionPage id={route.id} /> : null; break;
    case "runs": page = route.id ? <RunPage id={route.id} /> : null; break;
    case "compare": page = <ComparePage />; break;
    case "admin": page = <AdminPage />; break;
    case "invite": page = route.id ? <InvitePage token={route.id} lang={lang} api={api} signedIn onToken={onToken} /> : null; break;
    default: page = <ProjectsPage />;
  }

  return (
    <AppContext.Provider value={{ api, me, lang, labels, fields, notify, compareRuns, setCompareRuns }}>
      <div className="shell">
        <nav className="side" aria-label="Navigation">
          <div className="brand">{t("title", lang)}</div>
          {nav.map((n) => (
            <a key={n.name} href={href(n.name)} aria-current={n.match.includes(route.name) ? "page" : undefined}>{n.label}</a>
          ))}
          <div className="spacer" />
          <div className="who">{me.name}<br />{me.email}<br />
            {me.memberships.map((m) => `${m.organization} · ${t(`role_${m.role}` as Key, lang)}`).join(", ")}</div>
          <div className="row" style={{ marginTop: 8 }}>
            {langSwitch}
            <button onClick={() => { api.logout().catch(() => undefined); signOut(); }}>{t("logout", lang)}</button>
          </div>
        </nav>
        <main className="main">
          <p className="disclaimer">{t("disclaimer", lang)}</p>
          {page}
        </main>
      </div>
      {toastEl}
    </AppContext.Provider>
  );
}
