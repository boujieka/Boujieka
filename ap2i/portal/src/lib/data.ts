import { useEffect, useState } from "react";
import type { Snapshot } from "./types";

const BASE = `${import.meta.env.BASE_URL}data/`;
const cache = new Map<string, Promise<unknown>>();

export function fetchJSON<T>(name: string): Promise<T> {
  if (!cache.has(name)) {
    cache.set(name, fetch(BASE + name).then((r) => {
      if (!r.ok) throw new Error(`${name}: HTTP ${r.status}`);
      return r.json();
    }).catch((e) => {
      cache.delete(name); // allow a retry
      throw e;
    }));
  }
  return cache.get(name) as Promise<T>;
}

let core: Promise<Snapshot> | null = null;

/** The core tables (≈2 MB, gzip-compressed by the host); per-project files are loaded on demand. */
export function loadSnapshot(): Promise<Snapshot> {
  core ??= Promise.all([
    fetchJSON("meta.json"), fetchJSON("ref.json"), fetchJSON("projects.json"), fetchJSON("agreements.json"),
    fetchJSON("flows.json"), fetchJSON("alerts.json"), fetchJSON("data-quality.json"), fetchJSON("africa.json"),
  ]).then(([meta, ref, projects, agreements, flows, alerts, dataQuality, africa]) => ({
    meta, ref, projects, agreements, flows, alerts, dataQuality, africa,
  }) as Snapshot).catch((e) => {
    core = null;
    throw e;
  });
  return core;
}

export function useAsync<T>(fn: () => Promise<T>, deps: unknown[]) {
  const [state, set] = useState<{ data?: T; error?: string; loading: boolean }>({ loading: true });
  const [nonce, setNonce] = useState(0);
  useEffect(() => {
    let live = true;
    set((s) => ({ ...s, loading: true, error: undefined }));
    fn().then((data) => live && set({ data, loading: false }), (e) => live && set({ error: String(e?.message ?? e), loading: false }));
    return () => {
      live = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, nonce]);
  return { ...state, retry: () => setNonce((n) => n + 1) };
}
