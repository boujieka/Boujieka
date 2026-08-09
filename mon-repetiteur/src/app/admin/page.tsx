import Link from "next/link";
import { listAllExams, listAllExercises, listAllLessons } from "@/services/admin";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { buttonVariants } from "@/components/ui/button";
import { CONTENT_STATUS_META } from "@/lib/content-status";
import type { ContentStatus } from "@/types/curriculum";

const STATUSES: ContentStatus[] = ["draft", "under_review", "validated", "published", "archived"];

function countByStatus(items: { status: ContentStatus }[]): Record<ContentStatus, number> {
  const counts = Object.fromEntries(STATUSES.map((status) => [status, 0])) as Record<
    ContentStatus,
    number
  >;
  for (const item of items) counts[item.status] += 1;
  return counts;
}

export default async function AdminOverviewPage() {
  const [lessons, exercises, exams] = await Promise.all([
    listAllLessons(),
    listAllExercises(),
    listAllExams(),
  ]);

  const sections = [
    { label: "Leçons", href: "/admin/lessons", items: lessons },
    { label: "Exercices", href: "/admin/exercises", items: exercises },
    { label: "Épreuves", href: "/admin/exams", items: exams },
  ];

  return (
    <>
      <PageHeader title="Administration" />

      <div className="flex flex-col gap-4">
        {sections.map((section) => {
          const counts = countByStatus(section.items);
          return (
            <Card key={section.href} className="flex flex-col gap-3">
              <div className="flex items-center justify-between gap-3">
                <p className="font-medium text-zinc-950 dark:text-zinc-50">
                  {section.label} ({section.items.length})
                </p>
                <Link
                  href={section.href}
                  className={buttonVariants({ variant: "secondary", size: "sm" })}
                >
                  Gérer
                </Link>
              </div>
              <div className="flex flex-wrap gap-x-4 gap-y-1">
                {STATUSES.map((status) => (
                  <p key={status} className="text-xs text-zinc-500 dark:text-zinc-400">
                    {CONTENT_STATUS_META[status].label} : {counts[status]}
                  </p>
                ))}
              </div>
            </Card>
          );
        })}
      </div>
    </>
  );
}
