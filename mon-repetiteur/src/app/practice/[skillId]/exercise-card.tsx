"use client";

import { useActionState } from "react";
import { submitAttemptAction, type AttemptState } from "./actions";
import type { Exercise } from "@/types/exercise";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/cn";

const initialState: AttemptState = { error: null, isCorrect: null, submitted: false };

interface MultipleChoiceContent {
  choices: string[];
  correctIndex: number;
}

const choiceClasses = cn(
  "flex cursor-pointer items-center gap-3 rounded-lg border border-zinc-200 px-3 py-2.5 text-sm",
  "has-[:checked]:border-indigo-500 has-[:checked]:bg-indigo-50",
  "dark:border-zinc-700 dark:has-[:checked]:border-indigo-500 dark:has-[:checked]:bg-indigo-950",
);

export function ExerciseCard({ exercise }: { exercise: Exercise }) {
  const boundAction = submitAttemptAction.bind(null, exercise.id);
  const [state, formAction, pending] = useActionState(boundAction, initialState);

  return (
    <Card className="flex flex-col gap-3">
      <p className="font-medium text-zinc-950 dark:text-zinc-50">{exercise.prompt}</p>

      {exercise.type === "multiple_choice" || exercise.type === "true_false" ? (
        <form action={formAction} className="flex flex-col gap-3">
          <div className="flex flex-col gap-2">
            {exercise.type === "multiple_choice"
              ? (exercise.content as unknown as MultipleChoiceContent).choices.map(
                  (choice, index) => (
                    <label key={index} className={choiceClasses}>
                      <input
                        type="radio"
                        name="answer"
                        value={index}
                        required
                        className="accent-indigo-600"
                      />
                      {choice}
                    </label>
                  ),
                )
              : (
                  <>
                    <label className={choiceClasses}>
                      <input
                        type="radio"
                        name="answer"
                        value="true"
                        required
                        className="accent-indigo-600"
                      />
                      Vrai
                    </label>
                    <label className={choiceClasses}>
                      <input
                        type="radio"
                        name="answer"
                        value="false"
                        required
                        className="accent-indigo-600"
                      />
                      Faux
                    </label>
                  </>
                )}
          </div>
          <Button type="submit" size="sm" disabled={pending} className="w-fit">
            {pending ? "Envoi…" : "Valider"}
          </Button>
        </form>
      ) : (
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Ce type d&apos;exercice n&apos;est pas encore pris en charge.
        </p>
      )}

      {state.error ? (
        <p role="alert" className="text-sm text-rose-600 dark:text-rose-400">
          {state.error}
        </p>
      ) : null}
      {state.submitted ? (
        <p
          role="status"
          className={cn(
            "flex items-center gap-1.5 text-sm font-medium",
            state.isCorrect
              ? "text-emerald-600 dark:text-emerald-400"
              : "text-rose-600 dark:text-rose-400",
          )}
        >
          {state.isCorrect ? "Correct !" : "Incorrect."}
        </p>
      ) : null}
    </Card>
  );
}
