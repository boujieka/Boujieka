"use client";
import type { ReactNode } from "react";
import { Loader2 } from "lucide-react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";

export function PageHeader({ title, lead, actions, badges }: { title: string; lead?: string; actions?: ReactNode; badges?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-xl font-semibold tracking-tight text-navy-900 sm:text-2xl">{title}</h1>
          {badges}
        </div>
        {lead ? <p className="mt-1 max-w-3xl text-sm text-muted-foreground">{lead}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
}

export function Loading() {
  const { t } = useI18n();
  return (
    <div className="flex items-center gap-2 py-8 text-sm text-muted-foreground" role="status">
      <Loader2 className="size-4 animate-spin" aria-hidden /> {t("common.loading")}
    </div>
  );
}

export function ErrorBox({ error, onRetry }: { error: string; onRetry?: () => void }) {
  const { t } = useI18n();
  return (
    <Alert variant="danger" className="items-center justify-between">
      <span>
        {t("common.error")}: {error}
      </span>
      {onRetry ? (
        <Button size="sm" variant="outline" onClick={onRetry}>
          {t("common.retry")}
        </Button>
      ) : null}
    </Alert>
  );
}

export function Unavailable({ text }: { text?: string }) {
  const { t } = useI18n();
  return <p className="text-sm italic text-subtle-foreground">{text ?? t("common.dataUnavailable")}</p>;
}
