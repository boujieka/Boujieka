import { useState, type ReactNode } from "react";
import { useI18n } from "../lib/i18n";
import { useSnap } from "../lib/context";
import { fmtDate } from "../lib/format";
import { href, type Route } from "../lib/router";
import { withoutYears } from "../lib/filters";

const NAV: { key: string; path: string; icon: string }[] = [
  { key: "home", path: "/", icon: "⌂" },
  { key: "africa", path: "/africa", icon: "◍" },
  { key: "country", path: "/country/CMR", icon: "▤" },
  { key: "projects", path: "/projects", icon: "☰" },
  { key: "finance", path: "/finance", icon: "$" },
  { key: "performance", path: "/performance", icon: "◔" },
  { key: "rescue", path: "/rescue", icon: "✚" },
  { key: "data", path: "/data", icon: "⊞" },
  { key: "about", path: "/about", icon: "ⓘ" },
];

export function Layout({ route, children }: { route: Route; children: ReactNode }) {
  const { t, locale, setLocale } = useI18n();
  const s = useSnap();
  const [open, setOpen] = useState(false);
  const cur = "/" + (route.path[0] ?? "");
  const keep = route.path[0] === "project" ? withoutYears(route.filters) : route.filters;
  return (
    <div className="shell">
      <a className="skip" href="#main">{locale === "fr" ? "Aller au contenu" : "Skip to content"}</a>
      <aside className={`side ${open ? "open" : ""}`} aria-label={t("nav.menu")}>
        <a className="brand" href="#/">
          <img src={`${import.meta.env.BASE_URL}ap2i-logo.png`} alt="" width={36} height={36} />
          <span><b>AP²I</b><small>{t("app.name")}</small></span>
        </a>
        <nav>
          {NAV.map((n) => {
            const isCur = n.path === "/" ? cur === "/" : cur === "/" + n.path.split("/")[1];
            return (
              <a key={n.key} href={href(n.path, n.key === "home" || n.key === "about" ? {} : keep)} aria-current={isCur ? "page" : undefined}
                onClick={() => setOpen(false)} data-testid={`nav-${n.key}`}>
                <span className="ico" aria-hidden>{n.icon}</span>{t(`nav.${n.key}`)}
              </a>
            );
          })}
        </nav>
        <div className="side-foot">
          <span className="badge b-gold">{t("snapshot.badge")}</span>
          <span>{t("snapshot.asOf")} {fmtDate(s.meta.generated_at, locale)}</span>
        </div>
      </aside>
      <div className="main-col">
        <header className="topbar">
          <button className="btn xs ghost menu-btn" onClick={() => setOpen((o) => !o)} aria-expanded={open} aria-label={t("nav.menu")}>☰</button>
          <span className="topbar-title">AP²I — <em>{t("app.tagline")}</em></span>
          <span className="topbar-r">
            <span className="muted small hide-sm">{t("snapshot.latestSource")} : {fmtDate(s.meta.latest_source_update, locale)}</span>
            <button className={`btn xs ${locale === "fr" ? "" : "ghost"}`} onClick={() => setLocale("fr")} aria-pressed={locale === "fr"}>FR</button>
            <button className={`btn xs ${locale === "en" ? "" : "ghost"}`} onClick={() => setLocale("en")} aria-pressed={locale === "en"}>EN</button>
          </span>
        </header>
        <main id="main" tabIndex={-1}>
          {children}
          <p className="scope-note">{t("snapshot.readonly")}</p>
        </main>
      </div>
      {open && <div className="scrim" onClick={() => setOpen(false)} aria-hidden />}
    </div>
  );
}
