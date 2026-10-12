"use client";

import Link from "next/link";
import { Clock } from "lucide-react";
import { PageHeader } from "@/components/page";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { useI18n, type DictKey } from "@/lib/i18n";

export function PlannedPage({ title, phase, text, links }: { title: DictKey; phase: DictKey; text: DictKey; links: { href: string; key: DictKey }[] }) {
  const { t } = useI18n();
  return (
    <>
      <PageHeader
        title={t(title)}
        badges={
          <>
            <Badge variant="neutral">
              <Clock aria-hidden /> {t("common.planned")}
            </Badge>
            <Badge variant="gold">{t(phase)}</Badge>
          </>
        }
      />
      <Card className="max-w-3xl">
        <CardContent className="pt-5">
          <p className="text-sm leading-relaxed text-foreground">{t(text)}</p>
          <div className="mt-6 border-t border-border pt-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">{t("planned.today")}</p>
            <ul className="mt-2 flex flex-wrap gap-3 text-sm">
              {links.map((l) => (
                <li key={l.href}>
                  <Link href={l.href} className="font-medium text-navy-700 underline-offset-4 hover:underline">
                    {t(l.key)}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>
    </>
  );
}
