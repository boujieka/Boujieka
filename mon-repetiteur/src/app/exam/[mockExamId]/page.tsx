import { notFound, redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getMockExamWithQuestions } from "@/services/mock-exam";
import { submitMockExamAction } from "./actions";

interface MultipleChoiceContent {
  choices: string[];
  correctIndex: number;
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
    return (
      <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-6 py-12">
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
          Résultat de l&apos;examen
        </h1>
        <p className="text-3xl font-semibold tabular-nums text-black dark:text-zinc-50">
          {Math.round((mockExam.score ?? 0) * 100)}%
        </p>
        <ul className="flex flex-col gap-2">
          {questions.map((question) => (
            <li
              key={question.id}
              className="rounded border border-zinc-200 p-3 text-sm dark:border-zinc-800"
            >
              {question.exercise.prompt}
            </li>
          ))}
        </ul>
      </main>
    );
  }

  const submitAction = submitMockExamAction.bind(null, mockExamId);

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-6 py-12">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        Examen blanc — Mathématiques
      </h1>

      {questions.length === 0 ? (
        <p className="text-zinc-500">
          Aucun exercice publié disponible pour cet examen pour le moment.
        </p>
      ) : (
        <form action={submitAction} className="flex flex-col gap-6">
          {questions.map((question, index) => (
            <fieldset
              key={question.id}
              className="rounded border border-zinc-200 p-4 dark:border-zinc-800"
            >
              <legend className="text-sm font-medium text-black dark:text-zinc-50">
                {index + 1}. {question.exercise.prompt}
              </legend>
              <div className="mt-2 flex flex-col gap-2">
                {question.exercise.type === "multiple_choice"
                  ? (question.exercise.content as unknown as MultipleChoiceContent).choices.map(
                      (choice, choiceIndex) => (
                        <label key={choiceIndex} className="flex items-center gap-2 text-sm">
                          <input
                            type="radio"
                            name={`question:${question.id}`}
                            value={choiceIndex}
                            required
                          />
                          {choice}
                        </label>
                      ),
                    )
                  : question.exercise.type === "true_false"
                    ? (
                        <div className="flex gap-4 text-sm">
                          <label className="flex items-center gap-2">
                            <input
                              type="radio"
                              name={`question:${question.id}`}
                              value="true"
                              required
                            />
                            Vrai
                          </label>
                          <label className="flex items-center gap-2">
                            <input
                              type="radio"
                              name={`question:${question.id}`}
                              value="false"
                              required
                            />
                            Faux
                          </label>
                        </div>
                      )
                    : (
                        <p className="text-sm text-zinc-500">
                          Ce type d&apos;exercice n&apos;est pas encore pris en charge.
                        </p>
                      )}
              </div>
            </fieldset>
          ))}
          <button
            type="submit"
            className="w-fit rounded bg-black px-4 py-2 text-sm text-white dark:bg-white dark:text-black"
          >
            Soumettre l&apos;examen
          </button>
        </form>
      )}
    </main>
  );
}
