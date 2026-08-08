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
    return <Empty message="Aucun programme disponible pour le moment." />;
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
    return <Empty message="Programme non encore configuré." />;
  }

  const topics = await getTopics(subject.id, targetClass.id);
  const topicsWithSkills = await Promise.all(
    topics.map(async (topic) => ({
      topic,
      skills: await getSkillsWithLessons(topic),
    })),
  );

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 px-6 py-12">
      <div className="flex flex-col gap-2">
        {programs.length > 1 ? (
          <nav className="flex gap-3 text-xs">
            {programs.map((p) => (
              <Link
                key={p.id}
                href={`/learn?program=${p.code}`}
                className={
                  p.id === program.id
                    ? "font-semibold underline"
                    : "text-zinc-500 underline dark:text-zinc-400"
                }
              >
                {p.name}
              </Link>
            ))}
          </nav>
        ) : null}
        <p className="text-sm text-zinc-500">
          {program.name} — {targetClass.name}
        </p>
        <div className="flex items-center justify-between gap-2">
          <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
            {subject.name}
          </h1>
          <div className="flex shrink-0 items-center gap-3">
            <Link href={`/archive?program=${program.code}`} className="text-xs underline">
              Archive des épreuves
            </Link>
            <form action={startMockExamAction}>
              <input type="hidden" name="subjectId" value={subject.id} />
              <input type="hidden" name="classId" value={targetClass.id} />
              <button type="submit" className="text-xs underline">
                Passer un examen blanc
              </button>
            </form>
          </div>
        </div>
      </div>

      {topicsWithSkills.length === 0 ? (
        <Empty message="Aucun chapitre disponible pour le moment." />
      ) : (
        topicsWithSkills.map(({ topic, skills }) => (
          <section key={topic.id} className="flex flex-col gap-3">
            <h2 className="text-lg font-medium text-black dark:text-zinc-50">
              {topic.title}
            </h2>
            <ul className="flex flex-col gap-2">
              {skills.map(({ skill, lessons }) => (
                <li
                  key={skill.id}
                  className="rounded border border-zinc-200 p-3 dark:border-zinc-800"
                >
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium text-black dark:text-zinc-50">
                      {skill.title}
                    </p>
                    <div className="flex shrink-0 items-center gap-3">
                      <Link href={`/practice/${skill.id}`} className="text-xs underline">
                        S&apos;entraîner
                      </Link>
                      <form action={startTutorConversationAction}>
                        <input type="hidden" name="skillId" value={skill.id} />
                        <input type="hidden" name="topicId" value={topic.id} />
                        <input type="hidden" name="subjectId" value={subject.id} />
                        <button type="submit" className="text-xs underline">
                          Demander de l&apos;aide
                        </button>
                      </form>
                    </div>
                  </div>
                  {lessons.length === 0 ? (
                    <p className="mt-1 text-sm text-zinc-500">
                      Leçon pas encore publiée.
                    </p>
                  ) : (
                    lessons.map((lesson) => (
                      <div key={lesson.id} className="mt-1">
                        <p className="text-sm text-zinc-700 dark:text-zinc-300">
                          {lesson.content}
                        </p>
                        {lesson.status !== "published" ? (
                          <p className="mt-1 text-xs uppercase tracking-wide text-amber-600 dark:text-amber-400">
                            {lesson.status}
                          </p>
                        ) : null}
                      </div>
                    ))
                  )}
                </li>
              ))}
            </ul>
          </section>
        ))
      )}
    </main>
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

function Empty({ message }: { message: string }) {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col items-center justify-center px-6 text-center">
      <p className="text-zinc-500">{message}</p>
    </main>
  );
}
