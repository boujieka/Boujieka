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

// First vertical only (PRD.md §5): Terminale C -> Mathématiques. Program
// picking, multi-subject navigation, etc. are later work — this page's job
// right now is to prove the loop's LEARN step against real data.
export default async function LearnPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const programs = await getPrograms();
  const program = programs.find((p) => p.code === "terminale_c");

  if (!program) {
    return (
      <Empty message="Aucun programme disponible pour le moment." />
    );
  }

  const [classes, subjects] = await Promise.all([
    getClasses(program.id),
    getSubjects(program.id),
  ]);
  const terminaleClass = classes.find((c) => c.code === "terminale");
  const subject = subjects.find((s) => s.slug === "mathematiques");

  if (!terminaleClass || !subject) {
    return <Empty message="Programme non encore configuré." />;
  }

  const topics = await getTopics(subject.id, terminaleClass.id);
  const topicsWithSkills = await Promise.all(
    topics.map(async (topic) => ({
      topic,
      skills: await getSkillsWithLessons(topic),
    })),
  );

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 px-6 py-12">
      <div>
        <p className="text-sm text-zinc-500">{program.name}</p>
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
          {subject.name}
        </h1>
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
                  <p className="text-sm font-medium text-black dark:text-zinc-50">
                    {skill.title}
                  </p>
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
