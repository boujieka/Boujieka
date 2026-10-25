import { useState, type ReactNode } from "react";
import { useI18n } from "../lib/i18n";
import { useSnap } from "../lib/context";
import { fmtDate } from "../lib/format";
import { href, type Route } from "../lib/router";
import { withoutYears } from "../lib/filters";
import { GlobalSearch } from "./GlobalSearch";

// Inline icons (stroke = currentColor): consistent rendering on every platform, unlike text glyphs.
const ICONS: Record<string, string> = {
  home: "M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
  africa: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-2 4l3 1 2 3-1 3 2 3-3 3-1-3-3-2v-3z",
  country: "M4 4h16v16H4zM4 10h16M10 4v16",
  projects: "M4 6h16M4 12h16M4 18h10",
  finance: "M12 3v18M16 7c0-1.7-1.8-3-4-3s-4 1.3-4 3 1.8 3 4 3 4 1.3 4 3-1.8 3-4 3-4-1.3-4-3",
  performance: "M4 20V10M10 20V4M16 20v-7M22 20H2",
  rescue: "M12 21s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.5-7 10-7 10z",
  data: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
  about: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 11v6M12 7h.01",
  plans: "M4 7h16v13H4zM8 7V4h8v3",
  contact: "M4 6h16v12H4zM4 6l8 7 8-7",
  alerts: "M6 16V11a6 6 0 1 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0",
  map: "M9 4L3 6v14l6-2 6 2 6-2V4l-6 2zM9 4v14M15 6v14",
};

// Phase 3 (Oct 2026): five main entries for the questions users ask; the expert tools stay one click away.
type NavItem = { key: string; path: string; view?: string };
const NAV: NavItem[] = [
  { key: "projects", path: "/projects" }, { key: "finance", path: "/finance" }, { key: "alerts", path: "/performance" },
  { key: "map", path: "/projects", view: "map" }, { key: "about", path: "/about" },
];
const TOOLS: NavItem[] = [{ key: "country", path: "/country/CMR" }, { key: "africa", path: "/africa" }, { key: "rescue", path: "/rescue" }, { key: "data", path: "/data" }];
// pages that belong to a main entry (a project page is part of "Projects")
const SECTION: Record<string, string> = { project: "projects", projects: "projects", finance: "finance", performance: "alerts", alerts: "alerts", about: "about",
  country: "country", africa: "africa", rescue: "rescue", data: "data" };

function Icon({ name }: { name: string }) {
  return (
    <svg className="ico" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d={ICONS[name]} />
    </svg>
  );
}

export function Layout({ route, children }: { route: Route; children: ReactNode }) {
  const { t, locale, setLocale } = useI18n();
  const s = useSnap();
  const [open, setOpen] = useState(false);
  const isMap = route.path[0] === "projects" && route.qs.get("view") === "map";
  const section = isMap ? "map" : SECTION[route.path[0] ?? ""] ?? null;
  const keep = route.path[0] === "project" ? withoutYears(route.filters) : route.filters;
  const link = (n: NavItem, filters: boolean) => (
    <a key={n.key} href={href(n.path, filters ? keep : {}, n.view ? { view: n.view } : undefined)} aria-current={section === n.key ? "page" : undefined}
      onClick={() => setOpen(false)} data-testid={`nav-${n.key}`}>
      <Icon name={n.key} />{t(`nav.${n.key}`)}
    </a>
  );
  return (
    <div className="shell">
      <a className="skip" href="#/" onClick={(e) => { e.preventDefault(); document.getElementById("main")?.focus(); }}>
        {locale === "fr" ? "Aller au contenu" : "Skip to content"}
      </a>
      <aside className={`side ${open ? "open" : ""}`} aria-label={t("nav.menu")}>
        <a className="brand" href="#/">
          <img src={`${import.meta.env.BASE_URL}ap2i-logo-72.png`} alt="" width={36} height={36} />
          <span><b>AP²I</b><small>{t("app.name")}</small></span>
        </a>
        <nav aria-label={t("nav.menu")}>
          <a href="#/" aria-current={route.path[0] ? undefined : "page"} onClick={() => setOpen(false)} data-testid="nav-home"><Icon name="home" />{t("nav.home")}</a>
          {NAV.map((n) => link(n, n.key !== "about"))}
          <p className="nav-group">{t("nav.tools")}</p>
          <div className="nav-tools">{TOOLS.map((n) => link(n, n.key !== "africa"))}</div>
        </nav>
        <div className="side-foot">
          <span className="badge b-gold">{t("snapshot.badge")}</span>
          <span>{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)}</span>
        </div>
      </aside>
      <div className="main-col">
        <header className="topbar">
          <button className="btn xs ghost menu-btn" onClick={() => setOpen((o) => !o)} aria-expanded={open} aria-label={t("nav.menu")}>☰</button>
          <span className="topbar-title">AP²I</span>
          {route.path[0] ? <GlobalSearch /> : <span className="gsearch-spacer" />}
          <span className="topbar-r">
            <span className="muted small hide-sm">{t("snapshot.latestSource")} : {fmtDate(s.meta.latest_source_update, locale)}</span>
            <a className="btn xs ghost hide-xs" href="#/plans">{t("nav.plans")}</a>
            <a className="btn xs gold hide-xs" href="#/contact" data-testid="cta-demo">{t("nav.contact")}</a>
            <button className={`btn xs ${locale === "fr" ? "" : "ghost"}`} onClick={() => setLocale("fr")} aria-pressed={locale === "fr"} lang="fr">FR</button>
            <button className={`btn xs ${locale === "en" ? "" : "ghost"}`} onClick={() => setLocale("en")} aria-pressed={locale === "en"} lang="en">EN</button>
          </span>
        </header>
        <main id="main" tabIndex={-1}>
          {children}
        </main>
        <footer className="foot">
          <div>
            <b>AP²I — {t("app.name")}</b>
            <p className="small">{t("snapshot.readonly")}</p>
            <p className="small">{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)}</p>
          </div>
          <nav className="foot-links" aria-label="Footer">
            <a href="#/about">{t("nav.about")}</a>
            <a href="#/plans">{t("nav.plans")}</a>
            <a href="#/contact">{t("nav.contact")}</a>
            <a href="#/legal/terms">{locale === "fr" ? "Conditions d'utilisation" : "Terms of use"}</a>
            <a href="#/legal/privacy">{locale === "fr" ? "Confidentialité" : "Privacy"}</a>
            <a href="#/legal/data">{locale === "fr" ? "Licences et attribution des données" : "Data licences & attribution"}</a>
          </nav>
        </footer>
      </div>
      {open && <div className="scrim" onClick={() => setOpen(false)} aria-hidden />}
    </div>
  );
}
