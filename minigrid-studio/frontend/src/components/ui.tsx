import { DependencyList, useCallback, useEffect, useState } from "react";
import { ApiError } from "../api";
import { useApp } from "../context";
import { statusKey, translateMessage } from "../i18n";

/** Load data, re-run on deps change; errors go to the toast. */
export function useLoad<T>(load: () => Promise<T>, deps: DependencyList): [T | undefined, () => void, boolean] {
  const { notify } = useApp();
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(true);
  const [tick, setTick] = useState(0);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const run = useCallback(load, deps);
  useEffect(() => {
    let live = true;
    setLoading(true);
    run().then((d) => { if (live) setData(d); }).catch((e) => notify(errorText(e), "error"))
      .finally(() => { if (live) setLoading(false); });
    return () => { live = false; };
  }, [run, tick, notify]);
  return [data, () => setTick((x) => x + 1), loading];
}

export function errorText(e: unknown): string {
  if (e instanceof ApiError) {
    const d = e.detail as { message?: string; problems?: string[] } | string | { msg: string }[];
    if (typeof d === "string") return `${e.status} — ${d}`;
    if (Array.isArray(d)) return `${e.status} — ${d.map((x) => x.msg).join("; ")}`;
    if (d && typeof d === "object" && "message" in d) return `${e.status} — ${d.message}${d.problems ? ` : ${d.problems.join(" | ")}` : ""}`;
    return `${e.status} — ${e.message}`;
  }
  return String(e);
}

export function StatusBadge({ status }: { status: string }) {
  const { t } = useApp();
  const cls = status === "approved" ? "good" : status === "rejected" ? "bad" : status === "submitted" ? "warn" : "";
  const icon = status === "approved" ? "✓" : status === "rejected" ? "✕" : status === "submitted" ? "…" : "○";
  return <span className={`badge ${cls}`}><span aria-hidden="true">{icon}</span>{t(statusKey(status))}</span>;
}

export function RunBadge({ status }: { status: string }) {
  const { t } = useApp();
  if (status === "reconciled-engine") return <span className="badge good"><span aria-hidden="true">✓</span>{t("status_reconciled")}</span>;
  if (status === "variant") return <span className="badge warn"><span aria-hidden="true">≈</span>{t("status_variant")}</span>;
  return <span className="badge bad"><span aria-hidden="true">✕</span>{t("status_failed")}</span>;
}

export function Alert({ kind, children }: { kind: "critical" | "warning" | "info"; children: React.ReactNode }) {
  const icon = kind === "critical" ? "!" : kind === "warning" ? "⚠" : "i";
  const label = kind === "critical" ? "Critique / Critical" : kind === "warning" ? "Attention / Warning" : "Info";
  return (
    <div className={`alert ${kind}`} role={kind === "critical" ? "alert" : undefined}>
      <span className="icon" aria-label={label} title={label}>{icon}</span><div>{children}</div>
    </div>
  );
}

/** Engine messages in the interface language. */
export function useMessage() {
  const { labels } = useApp();
  return (text: string) => translateMessage(text, labels.message_rules);
}

export function Loading() {
  const { t } = useApp();
  return <p className="muted" aria-live="polite">{t("loading")}</p>;
}
