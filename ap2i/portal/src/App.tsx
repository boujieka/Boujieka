import { useCallback, useEffect, useMemo, useState } from "react";
import { I18nCtx, translate } from "./lib/i18n";
import { SnapCtx } from "./lib/context";
import { loadSnapshot, useAsync } from "./lib/data";
import { useRoute } from "./lib/router";
import type { Locale } from "./lib/format";
import { Layout } from "./components/Layout";
import { ErrorState, Loading } from "./components/ui";
import { Home } from "./pages/Home";
import { Africa } from "./pages/Africa";
import { Country } from "./pages/Country";
import { Projects } from "./pages/Projects";
import { Project } from "./pages/Project";
import { Finance } from "./pages/Finance";
import { Performance } from "./pages/Performance";
import { Rescue } from "./pages/Rescue";
import { DataExplorer } from "./pages/DataExplorer";
import { About } from "./pages/About";

function initialLocale(): Locale {
  try {
    const v = localStorage.getItem("ap2i.portal.locale");
    if (v === "fr" || v === "en") return v;
  } catch { /* storage unavailable */ }
  return navigator.language?.toLowerCase().startsWith("en") ? "en" : "fr";
}

export function App() {
  const [locale, setLocaleState] = useState<Locale>(initialLocale);
  const setLocale = useCallback((l: Locale) => {
    setLocaleState(l);
    try {
      localStorage.setItem("ap2i.portal.locale", l);
    } catch { /* ignore */ }
  }, []);
  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);
  const i18n = useMemo(() => ({ locale, setLocale, t: (k: string, v?: Record<string, string | number>) => translate(locale, k, v) }), [locale, setLocale]);
  const snap = useAsync(loadSnapshot, []);
  const route = useRoute();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [route.path.join("/")]);

  let page;
  switch (route.path[0]) {
    case undefined: page = <Home />; break;
    case "africa": page = <Africa route={route} />; break;
    case "country": page = <Country route={route} />; break;
    case "projects": page = <Projects route={route} />; break;
    case "project": page = <Project route={route} />; break;
    case "finance": page = <Finance route={route} />; break;
    case "performance": page = <Performance route={route} />; break;
    case "rescue": page = <Rescue route={route} />; break;
    case "data": page = <DataExplorer route={route} />; break;
    case "about": page = <About />; break;
    default: page = <Home />;
  }
  return (
    <I18nCtx.Provider value={i18n}>
      {snap.loading && !snap.data ? <div className="boot"><Loading /></div>
        : snap.error || !snap.data ? <div className="boot"><ErrorState error={snap.error ?? ""} retry={snap.retry} /></div>
        : (
          <SnapCtx.Provider value={snap.data}>
            <Layout route={route}>{page}</Layout>
          </SnapCtx.Provider>
        )}
    </I18nCtx.Provider>
  );
}
