import { getSubjectOptions, listAllExams, nextStatus } from "@/services/admin";
import { createExamAction, setExamRightsStatusAction, setExamStatusAction } from "./actions";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/field";
import { EmptyState } from "@/components/ui/empty-state";
import { CONTENT_STATUS_META } from "@/lib/content-status";
import { cn } from "@/lib/cn";
import type { ExamRightsStatus } from "@/types/exam-archive";

const selectClasses = cn(
  "rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-base text-zinc-950",
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2",
  "dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50 dark:focus-visible:ring-offset-zinc-950",
);
const labelClasses = "flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300";

const RIGHTS_STATUSES: ExamRightsStatus[] = [
  "unknown",
  "verified",
  "publicly_reusable",
  "permission_required",
  "restricted",
];
const RIGHTS_LABELS: Record<ExamRightsStatus, string> = {
  verified: "Vérifié",
  permission_required: "Permission requise",
  publicly_reusable: "Réutilisable publiquement",
  restricted: "Restreint",
  unknown: "Droits non résolus",
};

export default async function AdminExamsPage() {
  const [exams, subjectOptions] = await Promise.all([listAllExams(), getSubjectOptions()]);

  return (
    <>
      <PageHeader title="Épreuves" />

      <Card className="flex flex-col gap-3">
        <h2 className="text-sm font-medium text-zinc-950 dark:text-zinc-50">Nouvelle épreuve</h2>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">
          rights_status détermine si le lien source sera un jour visible aux élèves
          (CLAUDE.md §15) — laissez « Droits non résolus » sauf source réellement vérifiée.
        </p>
        <form action={createExamAction} className="flex flex-col gap-3">
          <label className={labelClasses}>
            Programme · Matière
            <select name="subject" required className={selectClasses} defaultValue="">
              <option value="" disabled>
                Sélectionner…
              </option>
              {subjectOptions.map((option) => (
                <option key={option.subjectId} value={`${option.programId}|${option.subjectId}`}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <Field label="Titre" name="title" required />
          <div className="grid grid-cols-2 gap-3">
            <Field label="Année" name="year" type="number" required />
            <Field label="Session (optionnel)" name="session" />
          </div>
          <label className={labelClasses}>
            Statut des droits
            <select name="rightsStatus" className={selectClasses} defaultValue="unknown">
              {RIGHTS_STATUSES.map((status) => (
                <option key={status} value={status}>
                  {RIGHTS_LABELS[status]}
                </option>
              ))}
            </select>
          </label>
          <Field label="Source (optionnel)" name="source" />
          <Field label="URL source (optionnel)" name="sourceUrl" type="url" />
          <Field label="Référence de permission (optionnel)" name="permissionReference" />
          <Button type="submit" className="w-fit">
            Créer (brouillon)
          </Button>
        </form>
      </Card>

      {exams.length === 0 ? (
        <EmptyState message="Aucune épreuve pour le moment." />
      ) : (
        <ul className="flex flex-col gap-3">
          {exams.map((exam) => {
            const meta = CONTENT_STATUS_META[exam.status];
            const next = nextStatus(exam.status);
            return (
              <li key={exam.id}>
                <Card className="flex flex-col gap-3">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">
                        {exam.year}
                        {exam.session ? ` — ${exam.session}` : ""}
                      </p>
                      <p className="font-medium text-zinc-950 dark:text-zinc-50">{exam.title}</p>
                    </div>
                    <div className="flex shrink-0 flex-col items-end gap-1">
                      <Badge tone={meta.tone}>{meta.label}</Badge>
                      <Badge tone="neutral">{RIGHTS_LABELS[exam.rights_status]}</Badge>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {next ? (
                      <form action={setExamStatusAction}>
                        <input type="hidden" name="examId" value={exam.id} />
                        <input type="hidden" name="status" value={next} />
                        <Button type="submit" variant="secondary" size="sm">
                          Passer à « {CONTENT_STATUS_META[next].label} »
                        </Button>
                      </form>
                    ) : null}
                    {exam.status !== "archived" ? (
                      <form action={setExamStatusAction}>
                        <input type="hidden" name="examId" value={exam.id} />
                        <input type="hidden" name="status" value="archived" />
                        <Button type="submit" variant="ghost" size="sm">
                          Archiver
                        </Button>
                      </form>
                    ) : null}
                  </div>

                  <form action={setExamRightsStatusAction} className="flex flex-wrap items-end gap-2">
                    <input type="hidden" name="examId" value={exam.id} />
                    <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700 dark:text-zinc-300">
                      Modifier le statut des droits
                      <select
                        name="rightsStatus"
                        className={cn(selectClasses, "py-1.5 text-sm")}
                        defaultValue={exam.rights_status}
                      >
                        {RIGHTS_STATUSES.map((status) => (
                          <option key={status} value={status}>
                            {RIGHTS_LABELS[status]}
                          </option>
                        ))}
                      </select>
                    </label>
                    <Button type="submit" variant="secondary" size="sm">
                      Mettre à jour
                    </Button>
                  </form>
                </Card>
              </li>
            );
          })}
        </ul>
      )}
    </>
  );
}
