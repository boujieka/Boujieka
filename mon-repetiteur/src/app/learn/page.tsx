import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import {
  getClasses,
  getLessonsForSkill,
  getPrograms,
  getSkills,
  getSubjects,
  getTopics,
} from "@/services/curriculum";
import type { Skill, Topic } from "@/types/curriculum";
import { startTutorConversationAction } from "@/app/tutor/actions";
import { startMockExamAction } from "@/app/exam/actions";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ChatIcon } from "@/components/ui/icons";
import { cn } from "@/lib/cn";
import { CONTENT_STATUS_META } from "@/lib/content-status";

const DEFAULT_PROGRAM_CODE = "terminale_c";

export default async function LearnPage({
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

  const [classes, subjects] = await Promise.all([
    getClasses(program.id),
    getSubjects(program.id),
  ]);
  // The terminal (exam) year is the highest-order class. Each program has
  // exactly one subject for now, so the first one is unambiguous — this
  // stops being safe the moment a program gets a second subject.
  const targetClass = [...classes].sort((a, b) => b.order - a.order)[0];
  const subject = subjects[0];

  if (!targetClass || !subject) {
    return (
      <AppShell>
        <main className="mx-auto max-w-2xl px-6 py-12">
          <EmptyState message="Programme non encore configuré." />
        </main>
      </AppShell>
    );
  }

  const topics = await getTopics(subject.id, targetClass.id);
  const topicsWithSkills = await Promise.all(
    topics.map(async (topic) => ({
      topic,
      skills: await getSkillsWithLessons(topic),
    })),
  );

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <div className="flex flex-col gap-4">
          {programs.length > 1 ? (
            <div className="flex gap-2" role="tablist" aria-label="Programme">
              {programs.map((p) => (
                <Link
                  key={p.id}
                  href={`/learn?program=${p.code}`}
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

          <PageHeader
            eyebrow={`${program.name} — ${targetClass.name}`}
            title={subject.name}
            actions={
              <>
                <Link
                  href={`/archive?program=${program.code}`}
                  className={buttonVariants({ variant: "secondary", size: "sm" })}
                >
                  Archive des épreuves
                </Link>
                <form action={startMockExamAction}>
                  <input type="hidden" name="subjectId" value={subject.id} />
                  <input type="hidden" name="classId" value={targetClass.id} />
                  <Button type="submit" size="sm">
                    Examen blanc
                  </Button>
                </form>
              </>
            }
          />
        </div>

        {topicsWithSkills.length === 0 ? (
          <EmptyState message="Aucun chapitre disponible pour le moment." />
        ) : (
          topicsWithSkills.map(({ topic, skills }) => (
            <section key={topic.id} className="flex flex-col gap-3">
              <h2 className="text-lg font-medium text-zinc-950 dark:text-zinc-50">
                {topic.title}
              </h2>
              <ul className="flex flex-col gap-3">
                {skills.map(({ skill, lessons }) => (
                  <li key={skill.id}>
                    <Card className="flex flex-col gap-3">
                      <div className="flex items-start justify-between gap-3">
                        <p className="font-medium text-zinc-950 dark:text-zinc-50">
                          {skill.title}
                        </p>
                        <div className="flex shrink-0 gap-2">
                          <Link
                            href={`/practice/${skill.id}`}
                            className={buttonVariants({ variant: "secondary", size: "sm" })}
                          >
                            S&apos;entraîner
                          </Link>
                          <form action={startTutorConversationAction}>
                            <input type="hidden" name="skillId" value={skill.id} />
                            <input type="hidden" name="topicId" value={topic.id} />
                            <input type="hidden" name="subjectId" value={subject.id} />
                            <Button type="submit" variant="ghost" size="sm">
                              <ChatIcon className="h-4 w-4" />
                              Aide
                            </Button>
                          </form>
                        </div>
                      </div>

                      {lessons.length === 0 ? (
                        <p className="text-sm text-zinc-500 dark:text-zinc-400">
                          Leçon pas encore publiée.
                        </p>
                      ) : (
                        lessons.map((lesson) => {
                          const meta = CONTENT_STATUS_META[lesson.status];
                          return (
                            <div key={lesson.id} className="flex flex-col gap-1.5">
                              <p className="text-sm text-zinc-700 dark:text-zinc-300">
                                {lesson.content}
                              </p>
                              {lesson.status !== "published" && meta ? (
                                <Badge tone={meta.tone} className="w-fit">
                                  {meta.label}
                                </Badge>
                              ) : null}
                            </div>
                          );
                        })
                      )}
                    </Card>
                  </li>
                ))}
              </ul>
            </section>
          ))
        )}
      </main>
    </AppShell>
  );
}

async function getSkillsWithLessons(topic: Topic) {
  const skills = await getSkills(topic.id);
  return Promise.all(
    skills.map(async (skill: Skill) => ({
      skill,
      lessons: await getLessonsForSkill(skill.id),
    })),
  );
}
