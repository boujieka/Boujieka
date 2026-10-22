import type { Me } from "./types";

/** Permission helpers (UI gating only — the backend enforces every permission). */
export function canAdmin(me: Me | null): boolean {
  if (!me?.permissions) return false;
  return me.permissions.some((p) => p === "admin:all" || p === "admin:organization" || p === "data:review");
}

export function hasFeature(me: Me | null, f: string): boolean {
  if (!me) return false;
  return (me.permissions ?? []).includes("admin:all") || (me.features ?? []).includes(f);
}

export function hasPermission(me: Me | null, p: string): boolean {
  if (!me) return false;
  const perms = me.permissions ?? [];
  return perms.includes("admin:all") || perms.includes(p);
}
