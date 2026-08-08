import { notFound, redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getMockExamWithQuestions } from "@/services/mock-exam";
import { submitMockExamAction } from "./actions";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { cn } from "@/lib/cn";

interface MultipleChoiceContent {
  choices: string[];
  correctIndex: number;
}

function scoreTone(score: number): "success" | "warning" | "danger" {
  if (score >= 0.7) return "success";
  if (score >= 0.4) return "warning";
  return "danger";
}

export default async function MockExamPage({
  params,
}: {
  params: Promise<{ mockExamId: string }>;
}) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const { mockExamId } = await params;
  const { mockExam, questions } = await getMockExamWithQuestions(mockExamId);

  // RLS already scopes this to the caller's own exam (or staff) — a null
  // result here means "not found", never "someone else's".
  if (!mockExam) {
    notFound();
  }

  if (mockExam.status === "submitted") {
    const score = mockExam.score ?? 0;
    return (
      <AppShell>
        <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
          <PageHeader title="Résultat de l'examen" />

          <Card className="flex flex-col items-center gap-2 py-8 text-center">
            <p className="text-5xl font-semibold tabular-nums text-zinc-950 dark:text-zinc-50">
              {Math.round(score * 100)}%
            </p>
            <Badge tone={scoreTone(score)}>
              {questions.filter((q) => q.isCorrect).length} / {questions.length} correctes
            </Badge>
          </Card>

          <ul className="flex flex-col gap-2">
            {questions.map((question, index) => (
              <li key={question.id}>
                <Card className="flex items-center justify-between gap-3">
                  <p className="text-sm text-zinc-700 dark:text-zinc-300">
                    {index + 1}. {question.exercise.prompt}
                  </p>
                  {question.isCorrect === null ? (
                    <Badge tone="neutral" className="shrink-0">
                      Non noté
                    </Badge>
                  ) : (
                    <Badge tone={question.isCorrect ? "success" : "danger"} className="shrink-0">
                      {question.isCorrect ? "Correct" : "Incorrect"}
                    </Badge>
                  )}
                </Card>
              </li>
            ))}
          </ul>
        </main>
      </AppShell>
    );
  }

  const submitAction = submitMockExamAction.bind(null, mockExamId);

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader title="Examen blanc — Mathématiques" />

        {questions.length === 0 ? (
          <EmptyState message="Aucun exercice publié disponible pour cet examen pour le moment." />
        ) : (
          <form action={submitAction} className="flex flex-col gap-4">
            {questions.map((question, index) => (
              <fieldset
                key={question.id}
                className="flex flex-col gap-3 rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900"
              >
                <legend className="text-sm font-medium text-zinc-950 dark:text-zinc-50">
                    {index + 1}. {question.exercise.prompt}
                  </legend>
                  <div className="flex flex-col gap-2">
                    {question.exercise.type === "multiple_choice"
                      ? (
                          question.exercise.content as unknown as MultipleChoiceContent
                        ).choices.map((choice, choiceIndex) => (
                          <label key={choiceIndex} className={choiceClasses}>
                            <input
                              type="radio"
                              name={`question:${question.id}`}
                              value={choiceIndex}
                              required
                              className="accent-indigo-600"
                            />
                            {choice}
                          </label>
                        ))
                      : question.exercise.type === "true_false"
                        ? (
                            <>
                              <label className={choiceClasses}>
                                <input
                                  type="radio"
                                  name={`question:${question.id}`}
                                  value="true"
                                  required
                                  className="accent-indigo-600"
                                />
                                Vrai
                              </label>
                              <label className={choiceClasses}>
                                <input
                                  type="radio"
                                  name={`question:${question.id}`}
                                  value="false"
                                  required
                                  className="accent-indigo-600"
                                />
                                Faux
                              </label>
                            </>
                          )
                        : (
                            <p className="text-sm text-zinc-500 dark:text-zinc-400">
                              Ce type d&apos;exercice n&apos;est pas encore pris en charge.
                            </p>
                          )}
                  </div>
              </fieldset>
            ))}
            <Button type="submit" className="w-fit">
              Soumettre l&apos;examen
            </Button>
          </form>
        )}
      </main>
    </AppShell>
  );
}

const choiceClasses = cn(
  "flex cursor-pointer items-center gap-3 rounded-lg border border-zinc-200 px-3 py-2.5 text-sm",
  "has-[:checked]:border-indigo-500 has-[:checked]:bg-indigo-50",
  "dark:border-zinc-700 dark:has-[:checked]:border-indigo-500 dark:has-[:checked]:bg-indigo-950",
);
