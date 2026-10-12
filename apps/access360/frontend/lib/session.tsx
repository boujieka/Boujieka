"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api, ApiError } from "./api";
import type { Me, OrgMembership } from "./types";

const ORG_KEY = "a360_org";

interface SessionCtx {
  me: Me | null;
  loading: boolean;
  error: string | null;
  org: OrgMembership | null;
  setOrgId: (id: string) => void;
  refresh: () => Promise<Me | null>;
  logout: () => Promise<void>;
  canEdit: boolean;
  isAdmin: boolean;
}

const Ctx = createContext<SessionCtx | null>(null);

function readStoredOrg(): string | null {
  try {
    return window.localStorage.getItem(ORG_KEY);
  } catch {
    return null;
  }
}

export function SessionProvider({ children }: { children: ReactNode }) {
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [orgId, setOrgIdState] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const m = await api<Me>("/api/auth/me");
      setMe(m);
      setError(null);
      setOrgIdState((cur) => {
        const pref = cur ?? readStoredOrg();
        if (pref && m.organizations.some((o) => o.id === pref)) return pref;
        return m.organizations[0]?.id ?? null;
      });
      return m;
    } catch (e) {
      setMe(null);
      if (!(e instanceof ApiError && e.status === 401)) setError(e instanceof Error ? e.message : String(e));
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- initial session load
    void refresh();
  }, [refresh]);

  const setOrgId = useCallback((id: string) => {
    setOrgIdState(id);
    try {
      window.localStorage.setItem(ORG_KEY, id);
    } catch {
      /* storage unavailable */
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api("/api/auth/logout", { method: "POST" });
    } finally {
      setMe(null);
    }
  }, []);

  const org = useMemo(() => me?.organizations.find((o) => o.id === orgId) ?? null, [me, orgId]);
  const canEdit = !!org && ["owner", "admin", "analyst"].includes(org.role);
  const isAdmin = !!org && ["owner", "admin"].includes(org.role);

  const value = useMemo(
    () => ({ me, loading, error, org, setOrgId, refresh, logout, canEdit, isAdmin }),
    [me, loading, error, org, setOrgId, refresh, logout, canEdit, isAdmin],
  );
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useSession(): SessionCtx {
  const c = useContext(Ctx);
  if (!c) throw new Error("useSession outside SessionProvider");
  return c;
}
