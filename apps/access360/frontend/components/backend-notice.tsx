"use client";
import type { ReactNode } from "react";
import { PlugZap } from "lucide-react";
import { Alert } from "@/components/ui/alert";
import { useI18n } from "@/lib/i18n";
import { useSession } from "@/lib/session";

/** Shown when the /api proxy cannot reach the backend. Renders nothing while the service answers. */
export function BackendNotice({ className, children }: { className?: string; children?: ReactNode }) {
  const { unavailable } = useSession();
  const { t } = useI18n();
  if (!unavailable) return null;
  return (
    <Alert variant="warning" role="alert" className={className} data-testid="backend-unavailable">
      <PlugZap aria-hidden />
      <div className="flex flex-col gap-2">
        <span>{t("common.backendUnavailable")}</span>
        {children}
      </div>
    </Alert>
  );
}
