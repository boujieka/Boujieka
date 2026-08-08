"use client";

import { useActionState } from "react";
import { submitAttemptAction, type AttemptState } from "./actions";
import type { Exercise } from "@/types/exercise";

const initialState: AttemptState = { error: null, isCorrect: null, submitted: false };

interface MultipleChoiceContent {
  choices: string[];
  correctIndex: number;
}

export function ExerciseCard({ exercise }: { exercise: Exercise }) {
  const boundAction = submitAttemptAction.bind(null, exercise.id);
  const [state, formAction, pending] = useActionState(boundAction, initialState);

  return (
    <div className="rounded border border-zinc-200 p-4 dark:border-zinc-800">
      <p className="text-sm font-medium text-black dark:text-zinc-50">{exercise.prompt}</p>

      {exercise.type === "multiple_choice" || exercise.type === "true_false" ? (
        <form action={formAction} className="mt-3 flex flex-col gap-2">
          {exercise.type === "multiple_choice"
            ? (exercise.content as unknown as MultipleChoiceContent).choices.map(
                (choice, index) => (
                  <label key={index} className="flex items-center gap-2 text-sm">
                    <input type="radio" name="answer" value={index} required />
                    {choice}
                  </label>
                ),
              )
            : (
                <div className="flex gap-4 text-sm">
                  <label className="flex items-center gap-2">
                    <input type="radio" name="answer" value="true" required /> Vrai
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="radio" name="answer" value="false" required /> Faux
                  </label>
                </div>
              )}
          <button
            type="submit"
            disabled={pending}
            className="mt-1 w-fit rounded bg-black px-3 py-1.5 text-sm text-white disabled:opacity-50 dark:bg-white dark:text-black"
          >
            {pending ? "Envoi…" : "Valider"}
          </button>
        </form>
      ) : (
        <p className="mt-2 text-sm text-zinc-500">
          Ce type d&apos;exercice n&apos;est pas encore pris en charge.
        </p>
      )}

      {state.error ? (
        <p role="alert" className="mt-2 text-sm text-red-600 dark:text-red-400">
          {state.error}
        </p>
      ) : null}
      {state.submitted ? (
        <p
          role="status"
          className={`mt-2 text-sm font-medium ${
            state.isCorrect
              ? "text-green-600 dark:text-green-400"
              : "text-red-600 dark:text-red-400"
          }`}
        >
          {state.isCorrect ? "Correct !" : "Incorrect."}
        </p>
      ) : null}
    </div>
  );
}
