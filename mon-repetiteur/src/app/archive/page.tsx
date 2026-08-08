import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getPrograms, getSubjects } from "@/services/curriculum";
import { getExams } from "@/services/exam-archive";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { cn } from "@/lib/cn";

const DEFAULT_PROGRAM_CODE = "terminale_c";

const RIGHTS_LABELS: Record<string, string> = {
  verified: "Vérifié",
  permission_required: "Permission requise",
  publicly_reusable: "Réutilisable publiquement",
  restricted: "Restreint",
  unknown: "Droits non résolus",
};

export default async function ArchivePage({
  searchParams,
}: {
  searchParams: Promise<{ program?: string }>;
}) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const { program: requestedProgramCode } = await searchParams;

  const programs = await getPrograms();
  if (programs.length === 0) {
    return (
      <AppShell>
        <main className="mx-auto max-w-2xl px-6 py-12">
          <EmptyState message="Aucun programme disponible pour le moment." />
        </main>
      </AppShell>
    );
  }
  const program =
    programs.find((p) => p.code === (requestedProgramCode ?? DEFAULT_PROGRAM_CODE)) ??
    programs[0];

  const subjects = await getSubjects(program.id);
  const subject = subjects[0];
  if (!subject) {
    return (
      <AppShell>
        <main className="mx-auto max-w-2xl px-6 py-12">
          <EmptyState message="Programme non encore configuré." />
        </main>
      </AppShell>
    );
  }

  const exams = await getExams(subject.id);

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <div className="flex flex-col gap-4">
          {programs.length > 1 ? (
            <div className="flex gap-2" role="tablist" aria-label="Programme">
              {programs.map((p) => (
                <Link
                  key={p.id}
                  href={`/archive?program=${p.code}`}
                  role="tab"
                  aria-selected={p.id === program.id}
                  className={cn(
                    "rounded-full px-3 py-1.5 text-xs font-medium transition-colors",
                    p.id === program.id
                      ? "bg-indigo-600 text-white"
                      : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700",
                  )}
                >
                  {p.name}
                </Link>
              ))}
            </div>
          ) : null}
          <PageHeader title={`Archive des épreuves — ${subject.name}`} />
        </div>

        {exams.length === 0 ? (
          <EmptyState message="Aucune épreuve archivée pour le moment." />
        ) : (
          <ul className="flex flex-col gap-3">
            {exams.map((exam) => (
              <li key={exam.id}>
                <Card className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-medium text-zinc-950 dark:text-zinc-50">{exam.title}</p>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400">
                      {exam.year}
                      {exam.session ? ` — ${exam.session}` : ""}
                    </p>
                  </div>
                  {exam.accessUrl ? (
                    <a
                      href={exam.accessUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="shrink-0 text-sm font-medium text-indigo-600 dark:text-indigo-400"
                    >
                      Voir le sujet
                    </a>
                  ) : (
                    <Badge tone="neutral" className="shrink-0">
                      {RIGHTS_LABELS[exam.rights_status] ?? exam.rights_status}
                    </Badge>
                  )}
                </Card>
              </li>
            ))}
          </ul>
        )}
      </main>
    </AppShell>
  );
}
