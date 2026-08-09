import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getActiveStudyPlan } from "@/services/study-plan";
import { completeStudySessionAction, generateStudyPlanAction } from "./actions";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";

function formatSessionDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    weekday: "short",
    day: "numeric",
    month: "short",
    timeZone: "UTC",
  });
}

export default async function StudyPlanPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const current = await getActiveStudyPlan();

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader
          title="Plan de révision"
          actions={
            <form action={generateStudyPlanAction}>
              <Button type="submit" variant="secondary" size="sm">
                {current ? "Générer un nouveau plan" : "Générer un plan"}
              </Button>
            </form>
          }
        />

        {!current ? (
          <EmptyState message="Aucun plan de révision — générez-en un à partir de vos compétences à travailler en priorité." />
        ) : (
          <>
            {current.studyPlan.status === "completed" ? (
              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800 dark:border-emerald-800 dark:bg-emerald-950 dark:text-emerald-200">
                Plan terminé — toutes les séances ont été complétées.
              </div>
            ) : null}

            <ul className="flex flex-col gap-3">
              {current.sessions.map((session) => (
                <li key={session.id}>
                  <Card className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {formatSessionDate(session.scheduled_for)} · {session.topicTitle}
                      </p>
                      <p className="font-medium text-zinc-950 dark:text-zinc-50">
                        {session.skillTitle}
                      </p>
                    </div>
                    <div className="flex shrink-0 items-center gap-2">
                      {session.completed_at ? (
                        <Badge tone="success">Terminé</Badge>
                      ) : (
                        <>
                          <Link
                            href={`/practice/${session.skill_id}`}
                            className={buttonVariants({ variant: "secondary", size: "sm" })}
                          >
                            S&apos;entraîner
                          </Link>
                          <form action={completeStudySessionAction}>
                            <input type="hidden" name="sessionId" value={session.id} />
                            <Button type="submit" size="sm">
                              Marquer terminé
                            </Button>
                          </form>
                        </>
                      )}
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
