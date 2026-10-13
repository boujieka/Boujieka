"use client";
// Shared building blocks for the Electrification Acceleration Score (project tab and portfolio page).
// Every figure comes from the API; texts returned by the server (explanations, sources) are rendered as text.

import { AlertTriangle, CheckCircle2, HelpCircle, ShieldAlert, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { num, pct } from "@/lib/format";
import { useI18n, type DictKey } from "@/lib/i18n";
import type { Decision, GateRow, GateState, ScorePart } from "@/lib/types";
import { cn } from "@/lib/utils";

export function DecisionBadge({ decision }: { decision: Decision }) {
  const { t } = useI18n();
  const map = {
    eligible: { variant: "success" as const, Icon: CheckCircle2 },
    review_required: { variant: "warning" as const, Icon: AlertTriangle },
    excluded: { variant: "danger" as const, Icon: XCircle },
  };
  const { variant, Icon } = map[decision] ?? map.review_required;
  return (
    <Badge variant={variant} data-testid="decision-badge" data-decision={decision}>
      <Icon aria-hidden /> {t(`score.decision.${decision}` as DictKey)}
    </Badge>
  );
}

export function GateStateBadge({ state }: { state: GateState }) {
  const { t } = useI18n();
  const variant = state === "met" ? "success" : state === "not_met" ? "danger" : "neutral";
  const Icon = state === "met" ? CheckCircle2 : state === "not_met" ? XCircle : HelpCircle;
  return (
    <Badge variant={variant} data-gate-state={state}>
      <Icon aria-hidden /> {t(`score.state.${state}` as DictKey)}
    </Badge>
  );
}

/** Horizontal bar for a score 0..100. An excluded project shows its score struck through: the gate overrides it. */
export function ScoreBar({ score, decision, className }: { score: number; decision: Decision; className?: string }) {
  const { t, locale } = useI18n();
  const w = Math.max(0, Math.min(100, score));
  const fill = decision === "eligible" ? "bg-emerald-600" : decision === "review_required" ? "bg-gold-500" : "bg-border-strong";
  return (
    <div className={cn("flex min-w-36 items-center gap-2", className)} data-testid="score-bar">
      <div
        className="h-2 flex-1 overflow-hidden rounded-full bg-surface-muted"
        role="meter"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={score}
        aria-label={t("pf.score")}
      >
        <div className={cn("h-full rounded-full", fill)} style={{ width: `${w}%` }} />
      </div>
      <span className={cn("w-10 text-right text-sm font-semibold tabular", decision === "excluded" ? "text-subtle-foreground line-through" : "text-navy-900")}>
        {num(score, locale, 1)}
      </span>
    </div>
  );
}

export function GateOverrideNote() {
  const { t } = useI18n();
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-danger-700" data-testid="gate-overrides">
      <ShieldAlert className="size-3.5" aria-hidden /> {t("score.gateOverrides")}
    </span>
  );
}

/** One bar per criterion: points against the maximum the weight allows, with the server's explanation. */
export function ScoreBreakdown({ parts, compact = false }: { parts: ScorePart[]; compact?: boolean }) {
  const { t, locale } = useI18n();
  return (
    <ul className={cn("flex flex-col", compact ? "gap-2" : "gap-3")} data-testid="score-breakdown">
      {parts.map((p) => {
        const max = p.weight * 100;
        const missing = p.normalised === null || p.points === null;
        const share = missing || max <= 0 ? 0 : Math.max(0, Math.min(1, (p.points ?? 0) / max));
        return (
          <li key={p.criterion} data-testid={`part-${p.criterion}`} data-missing={missing ? "true" : "false"}>
            <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-0.5">
              <span className="text-sm font-medium text-navy-900">{t(`score.crit.${p.criterion}` as DictKey)}</span>
              <span className="text-xs text-muted-foreground tabular">
                {missing ? (
                  <span className="italic text-subtle-foreground">{t("common.dataUnavailable")}</span>
                ) : (
                  t("score.ptsOf", { p: num(p.points, locale, 1), max: num(max, locale, 1) })
                )}
                <span className="ml-2 text-subtle-foreground">
                  {t("score.weight")} {pct(p.weight, locale)}
                </span>
              </span>
            </div>
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-surface-muted" aria-hidden>
              {missing ? (
                <div className="h-full w-full bg-[repeating-linear-gradient(45deg,var(--border)_0,var(--border)_4px,transparent_4px,transparent_8px)]" />
              ) : (
                <div className="h-full rounded-full bg-navy-700" style={{ width: `${share * 100}%` }} />
              )}
            </div>
            <p className="mt-1 text-xs text-muted-foreground">{p.explanation}</p>
          </li>
        );
      })}
    </ul>
  );
}

export function GatesList({ gates }: { gates: GateRow[] }) {
  const { t } = useI18n();
  return (
    <ul className="flex flex-col divide-y divide-border" data-testid="gates-list">
      {gates.map((g) => (
        <li key={g.gate} className="flex items-start justify-between gap-3 py-1.5 text-sm" data-testid={`gate-${g.gate}`}>
          <span className="text-foreground">{t(`score.gate.${g.gate}` as DictKey)}</span>
          <GateStateBadge state={g.state} />
        </li>
      ))}
    </ul>
  );
}

const SOURCE_KEYS = ["model_checks", "financial", "customer_mix", "months_to_power", "readiness"];

export function SourcesList({ sources }: { sources: Record<string, string> }) {
  const { t } = useI18n();
  const keys = Object.keys(sources);
  return (
    <dl className="grid gap-x-4 gap-y-1.5 text-xs sm:grid-cols-[max-content_minmax(0,1fr)]" data-testid="score-sources">
      {keys.map((k) => (
        <div key={k} className="contents">
          <dt className="font-medium text-muted-foreground">{SOURCE_KEYS.includes(k) ? t(`score.src.${k}` as DictKey) : k}</dt>
          <dd className="text-foreground">{sources[k]}</dd>
        </div>
      ))}
    </dl>
  );
}
