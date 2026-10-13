"use client";
import type { ReactNode } from "react";
import { BackendNotice } from "@/components/backend-notice";
import { Brand } from "@/components/brand";
import { LangToggle } from "@/components/lang-toggle";
import { useI18n } from "@/lib/i18n";

export function AuthShell({ title, children }: { title: string; children: ReactNode }) {
  const { t } = useI18n();
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="flex items-center justify-between px-4 py-4 sm:px-6">
        <Brand />
        <LangToggle />
      </header>
      <main className="flex flex-1 items-start justify-center px-4 pb-16 pt-6 sm:pt-12">
        <div className="w-full max-w-md rounded-lg border border-border bg-surface p-6 shadow-sm sm:p-8">
          <h1 className="text-xl font-semibold tracking-tight text-navy-900">{title}</h1>
          <p className="mt-1 text-xs text-muted-foreground">{t("brand.tagline")}</p>
          <BackendNotice className="mt-6" />
          <div className="mt-6">{children}</div>
        </div>
      </main>
    </div>
  );
}
