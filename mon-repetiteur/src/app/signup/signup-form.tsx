"use client";

import { useActionState } from "react";
import { signupAction, type SignupState } from "./actions";

const initialState: SignupState = { error: null, awaitingConfirmation: false };

export function SignupForm() {
  const [state, formAction, pending] = useActionState(signupAction, initialState);

  if (state.awaitingConfirmation) {
    return (
      <p role="status" className="text-sm text-zinc-700 dark:text-zinc-300">
        Compte créé. Vérifiez votre boîte mail pour confirmer votre adresse
        avant de vous connecter.
      </p>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-4" noValidate>
      <label className="flex flex-col gap-1 text-sm">
        Nom complet
        <input
          name="fullName"
          type="text"
          required
          autoComplete="name"
          className="rounded border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Email
        <input
          name="email"
          type="email"
          required
          autoComplete="email"
          className="rounded border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        Mot de passe
        <input
          name="password"
          type="password"
          required
          minLength={8}
          autoComplete="new-password"
          className="rounded border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
        />
      </label>
      {state.error ? (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          {state.error}
        </p>
      ) : null}
      <button
        type="submit"
        disabled={pending}
        className="rounded bg-black px-4 py-2 text-white disabled:opacity-50 dark:bg-white dark:text-black"
      >
        {pending ? "Création…" : "Créer un compte"}
      </button>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Déjà un compte ?{" "}
        <a href="/login" className="underline">
          Se connecter
        </a>
      </p>
    </form>
  );
}
