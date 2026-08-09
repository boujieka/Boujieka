import { getSkillOptions, listAllExercises, nextStatus } from "@/services/admin";
import { createExerciseAction, setExerciseStatusAction } from "./actions";
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
const labelClasses = "flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300";

const DIFFICULTY_LABELS: Record<string, string> = { easy: "Facile", medium: "Moyen", hard: "Difficile" };
const TYPE_LABELS: Record<string, string> = { multiple_choice: "QCM", true_false: "Vrai/Faux" };

export default async function AdminExercisesPage() {
  const [exercises, skillOptions] = await Promise.all([listAllExercises(), getSkillOptions()]);

  return (
    <>
      <PageHeader title="Exercices" />

      <Card className="flex flex-col gap-3">
        <h2 className="text-sm font-medium text-zinc-950 dark:text-zinc-50">Nouvel exercice</h2>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">
          Seuls les QCM et Vrai/Faux sont pris en charge — ce sont les seuls types que
          l&apos;interface élève sait afficher pour l&apos;instant.
        </p>
        <form action={createExerciseAction} className="flex flex-col gap-3">
          <label className={labelClasses}>
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
          <label className={labelClasses}>
            Type
            <select name="type" required className={selectClasses} defaultValue="multiple_choice">
              <option value="multiple_choice">QCM</option>
              <option value="true_false">Vrai/Faux</option>
            </select>
          </label>
          <label className={labelClasses}>
            Difficulté
            <select name="difficulty" className={selectClasses} defaultValue="medium">
              <option value="easy">Facile</option>
              <option value="medium">Moyen</option>
              <option value="hard">Difficile</option>
            </select>
          </label>
          <label className={labelClasses}>
            Énoncé
            <textarea name="prompt" required rows={2} className={textareaClasses} />
          </label>

          <fieldset className="flex flex-col gap-2 rounded-lg border border-zinc-200 p-3 dark:border-zinc-800">
            <legend className="px-1 text-xs text-zinc-500 dark:text-zinc-400">
              Pour un QCM — choix (2 à 4, laisser vide si inutilisé)
            </legend>
            <Field label="Choix 1" name="choice0" />
            <Field label="Choix 2" name="choice1" />
            <Field label="Choix 3" name="choice2" />
            <Field label="Choix 4" name="choice3" />
            <label className={labelClasses}>
              Index du choix correct (0 = premier choix)
              <select name="correctIndex" className={selectClasses} defaultValue="0">
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </label>
          </fieldset>

          <label className={labelClasses}>
            Pour Vrai/Faux — réponse correcte
            <select name="answer" className={selectClasses} defaultValue="true">
              <option value="true">Vrai</option>
              <option value="false">Faux</option>
            </select>
          </label>

          <Button type="submit" className="w-fit">
            Créer (brouillon)
          </Button>
        </form>
      </Card>

      {exercises.length === 0 ? (
        <EmptyState message="Aucun exercice pour le moment." />
      ) : (
        <ul className="flex flex-col gap-3">
          {exercises.map((exercise) => {
            const meta = CONTENT_STATUS_META[exercise.status];
            const next = nextStatus(exercise.status);
            return (
              <li key={exercise.id}>
                <Card className="flex flex-col gap-2">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {exercise.topicTitle} · {exercise.skillTitle} ·{" "}
                        {TYPE_LABELS[exercise.type] ?? exercise.type} ·{" "}
                        {DIFFICULTY_LABELS[exercise.difficulty] ?? exercise.difficulty}
                      </p>
                      <p className="font-medium text-zinc-950 dark:text-zinc-50">
                        {exercise.prompt}
                      </p>
                    </div>
                    <Badge tone={meta.tone} className="shrink-0">
                      {meta.label}
                    </Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {next ? (
                      <form action={setExerciseStatusAction}>
                        <input type="hidden" name="exerciseId" value={exercise.id} />
                        <input type="hidden" name="status" value={next} />
                        <Button type="submit" variant="secondary" size="sm">
                          Passer à « {CONTENT_STATUS_META[next].label} »
                        </Button>
                      </form>
                    ) : null}
                    {exercise.status !== "archived" ? (
                      <form action={setExerciseStatusAction}>
                        <input type="hidden" name="exerciseId" value={exercise.id} />
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
