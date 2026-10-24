// Minimal hash router: #/projects, #/projects/<id>, #/versions/<id>, #/runs/<id>,
// #/compare, #/admin, #/invite/<token>. The hash never reaches the server.
import { useEffect, useState } from "react";

export interface Route { name: string; id?: string; query: URLSearchParams }

export function parseHash(hash: string): Route {
  const [path, qs] = hash.replace(/^#\/?/, "").split("?");
  const [name = "projects", id] = path.split("/").filter(Boolean);
  return { name, id: id ? decodeURIComponent(id) : undefined, query: new URLSearchParams(qs ?? "") };
}

export function href(name: string, id?: string, query?: Record<string, string>): string {
  const q = query && Object.keys(query).length ? `?${new URLSearchParams(query)}` : "";
  return `#/${name}${id ? `/${encodeURIComponent(id)}` : ""}${q}`;
}

export function navigate(name: string, id?: string, query?: Record<string, string>) {
  window.location.hash = href(name, id, query);
}

export function useRoute(): Route {
  const [route, setRoute] = useState(() => parseHash(window.location.hash));
  useEffect(() => {
    const on = () => setRoute(parseHash(window.location.hash));
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return route;
}
