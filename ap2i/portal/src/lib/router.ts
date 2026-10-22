import { useEffect, useState } from "react";
import { parseFilters, toQuery, type Filters } from "./filters";

export interface Route {
  path: string[]; // e.g. ["project", "AP2I-CMR-ENERGY-000001"]
  qs: URLSearchParams;
  filters: Filters;
}

export function parseHash(hash: string): Route {
  const h = hash.replace(/^#/, "") || "/";
  const [p, q = ""] = h.split("?");
  const qs = new URLSearchParams(q);
  return { path: p.split("/").filter(Boolean).map(decodeURIComponent), qs, filters: parseFilters(qs) };
}

export function useRoute(): Route {
  const [route, setRoute] = useState(() => parseHash(window.location.hash));
  useEffect(() => {
    const on = () => {
      setRoute(parseHash(window.location.hash));
    };
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return route;
}

/** Build a link that keeps (or replaces) the global filters. Extra non-filter params (view, page…) can be passed. */
export function href(path: string, filters: Filters, extra?: Record<string, string | number | undefined>): string {
  let q = toQuery(filters);
  if (extra) {
    const qs = new URLSearchParams(q.replace(/^\?/, ""));
    for (const [k, v] of Object.entries(extra)) if (v !== undefined && v !== "") qs.set(k, String(v));
    q = qs.toString() ? `?${qs}` : "";
  }
  return `#${path}${q}`;
}

export function go(path: string, filters: Filters, extra?: Record<string, string | number | undefined>) {
  window.location.hash = href(path, filters, extra).slice(1);
}
