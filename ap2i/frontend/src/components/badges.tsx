"use client";

import { Badge, type Tone } from "@/components/ui/badge";
import { label } from "@/i18n";
import { useI18n } from "./i18n-provider";

const natureTone: Record<string, Tone> = {
  officially_reported: "navy", verified: "emerald", calculated: "gold", estimated: "gold", ai_generated: "danger", missing: "outline",
};

export function NatureBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  return <Badge tone={natureTone[value] ?? "neutral"} title={d.common.dataNature}>{label(d.natures, value)}</Badge>;
}

export function VerificationBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  const tone: Tone = value === "verified" ? "emerald" : value === "rejected" ? "danger" : value === "needs_review" ? "gold" : "outline";
  return <Badge tone={tone} title={d.common.verification}>{label(d.verificationStatus, value)}</Badge>;
}

export function StatusBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  const tone: Tone = value === "active" ? "emerald" : value === "pipeline" ? "gold" : value === "cancelled" || value === "dropped" ? "danger" : "navy";
  return <Badge tone={tone}>{label(d.projectStatus, value)}</Badge>;
}

export function OperationalBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  const tone: Tone = value === "operational" ? "emerald" : value === "not_operational" ? "danger" : value === "unknown" ? "outline" : "gold";
  return <Badge tone={tone}>{label(d.operationalStatus, value)}</Badge>;
}


export function LevelBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  const tone: Tone = value === "critical_attention" ? "danger" : value === "high_attention" ? "gold" : value === "watch" ? "navy" : "outline";
  return <Badge tone={tone}>{label(d.alertLevel, value)}</Badge>;
}

export function ReviewBadge({ value }: { value: string | null | undefined }) {
  const { d } = useI18n();
  if (!value) return null;
  return <Badge tone="outline">{label(d.reviewStatus, value)}</Badge>;
}

export function UsdCompleteBadge({ complete }: { complete: boolean | null | undefined }) {
  const { d } = useI18n();
  if (complete === null || complete === undefined) return null;
  return <Badge tone={complete ? "emerald" : "gold"}>{complete ? d.common.usdComplete : d.common.usdIncomplete}</Badge>;
}
