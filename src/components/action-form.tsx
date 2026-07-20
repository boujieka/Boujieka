"use client";

import { useFormState, useFormStatus } from "react-dom";
import type { ReactNode } from "react";

export interface FormState {
  error?: string;
}

type Action = (prev: FormState, formData: FormData) => Promise<FormState>;

export function SubmitButton({
  children,
  variant = "primary",
  className = "",
}: {
  children: ReactNode;
  variant?: "primary" | "gold" | "vert" | "ghost";
  className?: string;
}) {
  const { pending } = useFormStatus();
  const cls =
    variant === "gold" ? "btn-gold" : variant === "vert" ? "btn-vert" : variant === "ghost" ? "btn-ghost" : "btn-primary";
  return (
    <button type="submit" disabled={pending} className={`${cls} ${className}`}>
      {pending ? "…" : children}
    </button>
  );
}

/**
 * Enveloppe <form> liée à une server action typée (prev, formData) => FormState.
 * Affiche l'erreur retournée. Les champs cachés/visibles sont passés en enfants.
 */
export function ActionForm({
  action,
  children,
  className = "",
}: {
  action: Action;
  children: ReactNode;
  className?: string;
}) {
  const [state, formAction] = useFormState<FormState, FormData>(action, {});
  return (
    <form action={formAction} className={className}>
      {children}
      {state.error && <p className="mt-2 text-sm text-red-600">{state.error}</p>}
    </form>
  );
}
