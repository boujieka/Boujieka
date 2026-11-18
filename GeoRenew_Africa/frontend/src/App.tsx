import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import { ErrorBox } from "./components/ui";
import { getLang, setLang, t, type Lang } from "./i18n";
import { api } from "./lib/api";
import { MethodPage } from "./pages/MethodPage";
import { Portfolio } from "./pages/Portfolio";
import { ProjectPage } from "./pages/ProjectPage";
import type { Meta } from "./types";

export function App() {
  const [, rerender] = useState(0);
  const meta = useQuery({ queryKey: ["meta"], queryFn: () => api.get<Meta>("/meta"), staleTime: Infinity });
  const changeLang = (l: Lang) => { setLang(l); rerender((n) => n + 1); };
  return (
    <div className="app">
      <header className="topbar">
        <div>
          <span className="brand">{t("app.title")}</span> <span className="small muted">{t("app.subtitle")}</span>
        </div>
        <nav>
          <NavLink to="/" end>{t("nav.portfolio")}</NavLink>
          <NavLink to="/methode">{t("nav.method")}</NavLink>
          <select aria-label="Langue" value={getLang()} onChange={(e) => changeLang(e.target.value as Lang)}>
            <option value="fr">FR</option>
            <option value="en">EN</option>
          </select>
        </nav>
      </header>
      <div className="disclaimer">{t("app.disclaimer")}</div>
      <ErrorBox error={meta.error} />
      {meta.data && (
        <Routes>
          <Route path="/" element={<Portfolio meta={meta.data} />} />
          <Route path="/projets/:id" element={<ProjectPage meta={meta.data} />} />
          <Route path="/methode" element={<MethodPage />} />
        </Routes>
      )}
      <footer className="footer small muted">
        v{meta.data?.version} · moteur {meta.data?.engine_version}
      </footer>
    </div>
  );
}
