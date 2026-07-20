"use client";

import { useFormState, useFormStatus } from "react-dom";
import Link from "next/link";
import { loginAction, type ActionState } from "@/lib/auth/actions";
import { Wordmark } from "@/components/logo";

function SubmitBtn({ label, pendingLabel }: { label: string; pendingLabel: string }) {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} className="btn-primary w-full">
      {pending ? pendingLabel : label}
    </button>
  );
}

export default function LoginPage() {
  const [state, action] = useFormState<ActionState, FormData>(loginAction, {});
  return (
    <div className="flex min-h-screen items-center justify-center bg-navy-50 px-6 py-12">
      <div className="w-full max-w-md">
        <div className="mb-6 flex justify-center">
          <Wordmark />
        </div>
        <div className="card">
          <h1 className="text-xl font-semibold">Connexion</h1>
          <p className="mt-1 text-sm text-navy-500">Accédez à votre espace ATEN.</p>
          <form action={action} className="mt-5 space-y-4">
            <div>
              <label className="label" htmlFor="email">Email</label>
              <input id="email" name="email" type="email" required className="input" placeholder="vous@entreprise.com" />
            </div>
            <div>
              <label className="label" htmlFor="password">Mot de passe</label>
              <input id="password" name="password" type="password" required className="input" />
            </div>
            {state.error && <p className="text-sm text-red-600">{state.error}</p>}
            <SubmitBtn label="Se connecter" pendingLabel="Connexion…" />
          </form>
          <p className="mt-4 text-center text-sm text-navy-500">
            Pas de compte ? <Link href="/register" className="font-medium text-gold-600">Créer un compte</Link>
          </p>
        </div>
        <p className="mt-4 text-center text-xs text-navy-400">
          Démo : offtaker@aten.demo · developer@aten.demo · admin@aten.demo — demo1234
        </p>
      </div>
    </div>
  );
}
