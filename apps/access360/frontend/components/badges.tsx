"use client";
import { AlertTriangle, CheckCircle2, CircleDashed, FlaskConical, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useI18n } from "@/lib/i18n";
import type { RunStatus } from "@/lib/types";

/** Plain wording model status. "Validated" is only shown when the API status is exactly "validated". */
export function StatusBadge({ status }: { status: RunStatus | string | null | undefined }) {
  const { t } = useI18n();
  switch (status) {
    case "validated":
      return (
        <Badge variant="success" data-testid="status-badge" data-status="validated">
          <CheckCircle2 aria-hidden /> {t("status.validated")}
        </Badge>
      );
    case "warning":
      return (
        <Badge variant="warning" data-testid="status-badge" data-status="warning">
          <AlertTriangle aria-hidden /> {t("status.warning")}
        </Badge>
      );
    case "failed_checks":
      return (
        <Badge variant="danger" data-testid="status-badge" data-status="failed_checks">
          <XCircle aria-hidden /> {t("status.failed_checks")}
        </Badge>
      );
    case "incomplete_inputs":
      return (
        <Badge variant="danger" data-testid="status-badge" data-status="incomplete_inputs">
          <CircleDashed aria-hidden /> {t("status.incomplete_inputs")}
        </Badge>
      );
    default:
      return (
        <Badge variant="neutral" data-testid="status-badge" data-status="none">
          {t("status.notRun")}
        </Badge>
      );
  }
}

export function DemoBadge({ show = true, className }: { show?: boolean; className?: string }) {
  const { t } = useI18n();
  if (!show) return null;
  return (
    <Badge variant="gold" className={className} data-testid="demo-badge">
      <FlaskConical aria-hidden /> {t("common.demoBadge")}
    </Badge>
  );
}
