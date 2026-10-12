"use client";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export function LangToggle({ inverted = false }: { inverted?: boolean }) {
  const { locale, setLocale, t } = useI18n();
  return (
    <div role="group" aria-label={t("nav.language")} className={cn("inline-flex rounded-md border p-0.5 text-xs", inverted ? "border-white/25" : "border-border-strong")}>
      {(["en", "fr"] as const).map((l) => (
        <button
          key={l}
          type="button"
          aria-pressed={locale === l}
          data-testid={`lang-${l}`}
          onClick={() => setLocale(l)}
          className={cn(
            "rounded px-2 py-1 font-semibold uppercase",
            locale === l ? (inverted ? "bg-white text-navy-900" : "bg-navy-900 text-white") : inverted ? "text-white/80 hover:text-white" : "text-muted-foreground hover:text-foreground",
          )}
        >
          {l}
        </button>
      ))}
    </div>
  );
}
