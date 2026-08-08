"use client";

import { useActionState } from "react";
import Link from "next/link";
import { signupAction, type SignupState } from "./actions";
import { Field } from "@/components/ui/field";
import { Button } from "@/components/ui/button";

const initialState: SignupState = { error: null, awaitingConfirmation: false };

export function SignupForm() {
  const [state, formAction, pending] = useActionState(signupAction, initialState);

  if (state.awaitingConfirmation) {
    return (
      <p
        role="status"
        className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950 dark:text-emerald-300"
      >
        Compte créé. Vérifiez votre boîte mail pour confirmer votre adresse avant de vous
        connecter.
      </p>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-4" noValidate>
      <Field label="Nom complet" name="fullName" type="text" required autoComplete="name" />
      <Field label="Email" name="email" type="email" required autoComplete="email" />
      <Field
        label="Mot de passe"
        name="password"
        type="password"
        required
        minLength={8}
        autoComplete="new-password"
      />
      {state.error ? (
        <p role="alert" className="text-sm text-rose-600 dark:text-rose-400">
          {state.error}
        </p>
      ) : null}
      <Button type="submit" disabled={pending}>
        {pending ? "Création…" : "Créer un compte"}
      </Button>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Déjà un compte ?{" "}
        <Link href="/login" className="font-medium text-indigo-600 dark:text-indigo-400">
          Se connecter
        </Link>
      </p>
    </form>
  );
}
