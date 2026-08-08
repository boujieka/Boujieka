import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getStudentProgress } from "@/services/progress";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { cn } from "@/lib/cn";

function masteryBarColor(score: number): string {
  if (score >= 0.7) return "bg-emerald-500";
  if (score >= 0.4) return "bg-amber-500";
  return "bg-rose-500";
}

export default async function ProgressPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const progress = await getStudentProgress();
  const average =
    progress.length > 0
      ? progress.reduce((sum, entry) => sum + entry.masteryScore, 0) / progress.length
      : null;

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader title="Ma progression" />

        {progress.length === 0 ? (
          <EmptyState message="Aucune progression pour le moment — commencez par un exercice." />
        ) : (
          <>
            {average !== null ? (
              <Card className="flex items-center justify-between">
                <p className="text-sm text-zinc-500 dark:text-zinc-400">
                  Maîtrise moyenne ({progress.length} compétence
                  {progress.length > 1 ? "s" : ""})
                </p>
                <p className="text-2xl font-semibold tabular-nums text-zinc-950 dark:text-zinc-50">
                  {Math.round(average * 100)}%
                </p>
              </Card>
            ) : null}

            <ul className="flex flex-col gap-3">
              {progress.map((entry) => (
                <li key={entry.skillId}>
                  <Card>
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <p className="text-xs text-zinc-500 dark:text-zinc-400">
                          {entry.topicTitle}
                        </p>
                        <p className="font-medium text-zinc-950 dark:text-zinc-50">
                          {entry.skillTitle}
                        </p>
                      </div>
                      <p className="shrink-0 text-sm font-medium tabular-nums text-zinc-700 dark:text-zinc-300">
                        {Math.round(entry.masteryScore * 100)}%
                      </p>
                    </div>
                    <div
                      role="progressbar"
                      aria-valuenow={Math.round(entry.masteryScore * 100)}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-label={`Maîtrise de ${entry.skillTitle}`}
                      className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800"
                    >
                      <div
                        className={cn("h-full rounded-full", masteryBarColor(entry.masteryScore))}
                        style={{ width: `${Math.round(entry.masteryScore * 100)}%` }}
                      />
                    </div>
                  </Card>
                </li>
              ))}
            </ul>
          </>
        )}
      </main>
    </AppShell>
  );
}
