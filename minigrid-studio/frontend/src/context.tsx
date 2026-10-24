import { createContext, useContext } from "react";
import type { Api, FieldEntry, Labels, Me, Role } from "./api";
import type { Key, Lang } from "./i18n";
import { t as translate } from "./i18n";

export interface AppState {
  api: Api;
  me: Me;
  lang: Lang;
  labels: Labels;
  fields: FieldEntry[];
  notify: (message: string, kind?: "error" | "info") => void;
  compareRuns: string[];
  setCompareRuns: (ids: string[]) => void;
}

export const AppContext = createContext<AppState | null>(null);

export function useApp(): AppState & { t: (k: Key) => string; roleIn: (orgId: string) => Role | undefined } {
  const s = useContext(AppContext);
  if (!s) throw new Error("AppContext missing");
  return {
    ...s,
    t: (k: Key) => translate(k, s.lang),
    roleIn: (orgId: string) => s.me.memberships.find((m) => m.org_id === orgId)?.role,
  };
}

export const canEdit = (role?: Role) => role === "admin" || role === "analyst";
export const canReview = (role?: Role) => role === "admin" || role === "reviewer";
