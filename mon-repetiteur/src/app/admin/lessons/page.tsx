import { getSkillOptions, listAllLessons, nextStatus } from "@/services/admin";
import { createLessonAction, setLessonStatusAction } from "./actions";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/field";
import { EmptyState } from "@/components/ui/empty-state";
import { CONTENT_STATUS_META } from "@/lib/content-status";
import { cn } from "@/lib/cn";

const selectClasses = cn(
  "rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-base text-zinc-950",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2",
  "dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50 dark:focus-visible:ring-offset-zinc-950",
);
const textareaClasses = cn(selectClasses, "resize-y");

export default async function AdminLessonsPage() {
  const [lessons, skillOptions] = await Promise.all([listAllLessons(), getSkillOptions()]);

  return (
    <>
      <PageHeader title="Leçons" />

      <Card className="flex flex-col gap-3">
        <h2 className="text-sm font-medium text-zinc-950 dark:text-zinc-50">Nouvelle leçon</h2>
        <form action={createLessonAction} className="flex flex-col gap-3">
          <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Compétence
            <select name="skillId" required className={selectClasses} defaultValue="">
              <option value="" disabled>
                Sélectionner…
              </option>
              {skillOptions.map((option) => (
                <option key={option.skillId} value={option.skillId}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <Field label="Titre" name="title" required />
          <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Contenu
            <textarea name="content" required rows={3} className={textareaClasses} />
          </label>
          <Button type="submit" className="w-fit">
            Créer (brouillon)
          </Button>
        </form>
      </Card>

      {lessons.length === 0 ? (
        <EmptyState message="Aucune leçon pour le moment." />
      ) : (
        <ul className="flex flex-col gap-3">
          {lessons.map((lesson) => {
            const meta = CONTENT_STATUS_META[lesson.status];
            const next = nextStatus(lesson.status);
            return (
              <li key={lesson.id}>
                <Card className="flex flex-col gap-2">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {lesson.topicTitle} · {lesson.skillTitle}
                      </p>
                      <p className="font-medium text-zinc-950 dark:text-zinc-50">{lesson.title}</p>
                    </div>
                    <Badge tone={meta.tone} className="shrink-0">
                      {meta.label}
                    </Badge>
                  </div>
                  <p className="text-sm text-zinc-600 dark:text-zinc-400">{lesson.content}</p>
                  <div className="flex flex-wrap gap-2">
                    {next ? (
                      <form action={setLessonStatusAction}>
                        <input type="hidden" name="lessonId" value={lesson.id} />
                        <input type="hidden" name="status" value={next} />
                        <Button type="submit" variant="secondary" size="sm">
                          Passer à « {CONTENT_STATUS_META[next].label} »
                        </Button>
                      </form>
                    ) : null}
                    {lesson.status !== "archived" ? (
                      <form action={setLessonStatusAction}>
                        <input type="hidden" name="lessonId" value={lesson.id} />
                        <input type="hidden" name="status" value="archived" />
                        <Button type="submit" variant="ghost" size="sm">
                          Archiver
                        </Button>
                      </form>
                    ) : null}
                  </div>
                </Card>
              </li>
            );
          })}
        </ul>
      )}
    </>
  );
}
