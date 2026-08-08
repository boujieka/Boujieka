"use client";

import { useActionState } from "react";
import Link from "next/link";
import { loginAction, type LoginState } from "./actions";
import { Field } from "@/components/ui/field";
import { Button } from "@/components/ui/button";

const initialState: LoginState = { error: null };

export function LoginForm() {
  const [state, formAction, pending] = useActionState(loginAction, initialState);

  return (
    <form action={formAction} className="flex flex-col gap-4" noValidate>
      <Field label="Email" name="email" type="email" required autoComplete="email" />
      <Field
        label="Mot de passe"
        name="password"
        type="password"
        required
        autoComplete="current-password"
      />
      {state.error ? (
        <p role="alert" className="text-sm text-rose-600 dark:text-rose-400">
          {state.error}
        </p>
      ) : null}
      <Button type="submit" disabled={pending}>
        {pending ? "Connexion…" : "Se connecter"}
      </Button>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Pas encore de compte ?{" "}
        <Link href="/signup" className="font-medium text-indigo-600 dark:text-indigo-400">
          Créer un compte
        </Link>
      </p>
    </form>
  );
}
