import Link from "next/link";
import { redirect } from "next/navigation";
import { getDashboardData } from "@/services/dashboard";
import { LogoutButton } from "./logout-button";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { BookIcon, ChartIcon, ArchiveIcon, CalendarIcon, AdminIcon } from "@/components/ui/icons";
import { cn } from "@/lib/cn";

const ROLE_LABELS: Record<string, string> = {
  student: "Élève",
  parent: "Parent",
  teacher: "Enseignant",
  admin: "Administrateur",
};

const QUICK_LINKS = [
  { href: "/learn", label: "Voir le programme", description: "Cours et exercices", icon: BookIcon },
  { href: "/progress", label: "Ma progression", description: "Points forts et faibles", icon: ChartIcon },
  { href: "/plan", label: "Plan de révision", description: "Séances programmées", icon: CalendarIcon },
  { href: "/archive", label: "Archive des épreuves", description: "Sujets des années précédentes", icon: ArchiveIcon },
];

/** Same threshold scheme as /progress and /exam — kept as a local helper
 * rather than shared, matching those pages' existing pattern. */
function masteryTone(score: number): "success" | "warning" | "danger" {
  if (score >= 0.7) return "success";
  if (score >= 0.4) return "warning";
  return "danger";
}

/**
 * The "Accueil" landing page — doubles as PRD §7 item 8's Dashboard
 * (progress, weak skills, recent activity, entry points into the loop)
 * and the account/profile view. Kept as one route rather than splitting
 * into a separate /dashboard: the account page already served as the
 * app's home screen, and this is the smallest change that satisfies the
 * Dashboard requirement (CLAUDE.md §34/§35).
 */
export default async function AccountPage() {
  const data = await getDashboardData();
  if (!data) {
    redirect("/login");
  }

  const { profile, weakSkills, recentActivity, activeMockExam, stats } = data;
  const isStaff = profile.role === "teacher" || profile.role === "admin";
  const quickLinks = isStaff
    ? [
        ...QUICK_LINKS,
        {
          href: "/admin",
          label: "Administration",
          description: "Leçons, exercices, épreuves",
          icon: AdminIcon,
        },
      ]
    : QUICK_LINKS;

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader title="Tableau de bord" />

        {activeMockExam ? (
          <div className="flex items-center justify-between gap-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4 dark:border-indigo-800 dark:bg-indigo-950">
            <p className="text-sm text-indigo-800 dark:text-indigo-200">
              Un examen blanc est en cours.
            </p>
            <Link
              href={`/exam/${activeMockExam.id}`}
              className={cn(buttonVariants({ size: "sm" }), "shrink-0")}
            >
              Reprendre
            </Link>
          </div>
        ) : null}

        <Card className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-base font-semibold text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
              {(profile.full_name ?? "?").charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="font-medium text-zinc-950 dark:text-zinc-50">
                {profile.full_name ?? "—"}
              </p>
              <Badge tone="info">{ROLE_LABELS[profile.role] ?? profile.role}</Badge>
            </div>
          </div>
          <LogoutButton />
        </Card>

        <div className="grid grid-cols-2 gap-3">
          <Card className="flex flex-col gap-1">
            <p className="text-xs text-zinc-500 dark:text-zinc-400">Exercices tentés</p>
            <p className="text-2xl font-semibold tabular-nums text-zinc-950 dark:text-zinc-50">
              {stats.totalAttempts}
            </p>
          </Card>
          <Card className="flex flex-col gap-1">
            <p className="text-xs text-zinc-500 dark:text-zinc-400">Maîtrise moyenne</p>
            <p className="text-2xl font-semibold tabular-nums text-zinc-950 dark:text-zinc-50">
              {stats.averageMastery === null ? "—" : `${Math.round(stats.averageMastery * 100)}%`}
            </p>
          </Card>
        </div>

        <section className="flex flex-col gap-3">
          <h2 className="text-lg font-medium text-zinc-950 dark:text-zinc-50">
            Points à travailler
          </h2>
          {weakSkills.length === 0 ? (
            <EmptyState message="Aucune compétence à renforcer identifiée pour le moment." />
          ) : (
            <ul className="flex flex-col gap-3">
              {weakSkills.map((skill) => (
                <li key={skill.skillId}>
                  <Card className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {skill.topicTitle}
                      </p>
                      <p className="font-medium text-zinc-950 dark:text-zinc-50">
                        {skill.skillTitle}
                      </p>
                      <Badge tone={masteryTone(skill.masteryScore)} className="mt-1">
                        {Math.round(skill.masteryScore * 100)}% de maîtrise
                      </Badge>
                    </div>
                    <Link
                      href={`/practice/${skill.skillId}`}
                      className={cn(buttonVariants({ variant: "secondary", size: "sm" }), "shrink-0")}
                    >
                      S&apos;entraîner
                    </Link>
                  </Card>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="flex flex-col gap-3">
          <h2 className="text-lg font-medium text-zinc-950 dark:text-zinc-50">
            Activité récente
          </h2>
          {recentActivity.length === 0 ? (
            <EmptyState message="Aucune activité récente — commencez par un exercice." />
          ) : (
            <ul className="flex flex-col gap-2">
              {recentActivity.map((entry) => (
                <li key={entry.attemptId}>
                  <Card className="flex items-center justify-between gap-3 py-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {entry.topicTitle}
                      </p>
                      <p className="text-sm font-medium text-zinc-950 dark:text-zinc-50">
                        {entry.skillTitle}
                      </p>
                    </div>
                    {entry.isCorrect === null ? (
                      <Badge tone="neutral" className="shrink-0">
                        Non noté
                      </Badge>
                    ) : (
                      <Badge tone={entry.isCorrect ? "success" : "danger"} className="shrink-0">
                        {entry.isCorrect ? "Correct" : "Incorrect"}
                      </Badge>
                    )}
                  </Card>
                </li>
              ))}
            </ul>
          )}
        </section>

        <ul className="flex flex-col gap-3">
          {quickLinks.map(({ href, label, description, icon: Icon }) => (
            <li key={href}>
              <Link href={href}>
                <Card className="flex items-center gap-3 transition-colors hover:border-indigo-300 dark:hover:border-indigo-700">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-400">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="font-medium text-zinc-950 dark:text-zinc-50">{label}</p>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">{description}</p>
                  </div>
                </Card>
              </Link>
            </li>
          ))}
        </ul>
      </main>
    </AppShell>
  );
}
