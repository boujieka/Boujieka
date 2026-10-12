"use client";

import { BookOpen, Calculator, ClipboardList, FileText, GraduationCap, PlayCircle, Presentation } from "lucide-react";
import { PageHeader } from "@/components/page";
import { Badge } from "@/components/ui/badge";
import { useI18n, type DictKey } from "@/lib/i18n";

const ITEMS: { key: DictKey; icon: typeof BookOpen; main?: boolean }[] = [
  { key: "academy.book1", icon: BookOpen, main: true },
  { key: "academy.model1", icon: Calculator },
  { key: "academy.manual1", icon: FileText },
  { key: "academy.case1", icon: Presentation },
  { key: "academy.templates", icon: ClipboardList },
  { key: "academy.exercises", icon: GraduationCap },
  { key: "academy.video", icon: PlayCircle },
];

export default function AcademyPage() {
  const { t } = useI18n();
  return (
    <>
      <PageHeader title={t("academy.title")} lead={t("academy.lead")} />
      <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {ITEMS.map((it) => (
          <li key={it.key} className={it.main ? "flex flex-col gap-3 rounded-lg border border-gold-100 bg-gold-50 p-5 sm:col-span-2 lg:col-span-3" : "flex flex-col gap-3 rounded-lg border border-border bg-surface p-5"}>
            <div className="flex items-start justify-between gap-3">
              <it.icon className="size-5 shrink-0 text-gold-700" aria-hidden />
              <Badge variant="neutral">{t("common.inPreparation")}</Badge>
            </div>
            <h2 className={it.main ? "text-lg font-semibold text-navy-900" : "text-sm font-semibold text-navy-900"}>{t(it.key)}</h2>
          </li>
        ))}
      </ul>
    </>
  );
}
