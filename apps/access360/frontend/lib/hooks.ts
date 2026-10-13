"use client";

import { useCallback, useEffect, useState } from "react";
import { api, BackendUnavailableError, errorMessage } from "./api";
import { useI18n } from "./i18n";
import { useSession } from "./session";

export interface Loadable<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
  reload: () => void;
  setData: (d: T | null) => void;
}

/** GET a JSON resource; pass null to skip. */
export function useApi<T>(path: string | null): Loadable<T> {
  const [data, setData] = useState<T | null>(null);
  const { t } = useI18n();
  const { markUnavailable } = useSession();
  const [failure, setFailure] = useState<unknown>(null);
  const [loading, setLoading] = useState<boolean>(!!path);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (!path) return;
    let alive = true;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetch lifecycle
    setLoading(true);
    api<T>(path)
      .then((d) => {
        if (!alive) return;
        setData(d);
        setFailure(null);
      })
      .catch((e: unknown) => {
        if (alive) setFailure(e);
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, [path, tick]);

  useEffect(() => {
    if (failure instanceof BackendUnavailableError) markUnavailable();
  }, [failure, markUnavailable]);

  // translated at render time so the unavailability notice follows the language toggle
  const error = failure === null ? null : errorMessage(failure, t);
  const reload = useCallback(() => setTick((x) => x + 1), []);
  return { data, error, loading, reload, setData };
}
