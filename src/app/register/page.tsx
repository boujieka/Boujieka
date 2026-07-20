"use client";

import { useFormState, useFormStatus } from "react-dom";
import Link from "next/link";
import { registerAction, type ActionState } from "@/lib/auth/actions";
import { Wordmark } from "@/components/logo";

function SubmitBtn() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} className="btn-primary w-full">
      {pending ? "Création…" : "Créer mon compte"}
    </button>
  );
}

export default function RegisterPage() {
  const [state, action] = useFormState<ActionState, FormData>(registerAction, {});
  return (
    <div className="flex min-h-screen items-center justify-center bg-navy-50 px-6 py-12">
      <div className="w-full max-w-lg">
        <div className="mb-6 flex justify-center">
          <Wordmark />
        </div>
        <div className="card">
          <h1 className="text-xl font-semibold">Créer un compte</h1>
          <p className="mt-1 text-sm text-navy-500">
            Rejoignez ATEN comme entreprise consommatrice (offtaker) ou développeur.
          </p>
          <form action={action} className="mt-5 space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="label" htmlFor="organizationName">Raison sociale</label>
                <input id="organizationName" name="organizationName" required className="input" />
              </div>
              <div>
                <label className="label" htmlFor="organizationType">Type d'organisation</label>
                <select id="organizationType" name="organizationType" className="select" defaultValue="offtaker">
                  <option value="offtaker">Offtaker (consommateur)</option>
                  <option value="developer">Développeur</option>
                </select>
              </div>
              <div>
                <label className="label" htmlFor="country">Pays (ISO)</label>
                <input id="country" name="country" required maxLength={3} placeholder="CM" className="input uppercase" />
              </div>
              <div className="sm:col-span-2">
                <label className="label" htmlFor="sector">Secteur (optionnel)</label>
                <input id="sector" name="sector" className="input" placeholder="Industrie, tertiaire, …" />
              </div>
              <div className="sm:col-span-2">
                <label className="label" htmlFor="fullName">Nom complet</label>
                <input id="fullName" name="fullName" required className="input" />
              </div>
              <div>
                <label className="label" htmlFor="email">Email</label>
                <input id="email" name="email" type="email" required className="input" />
              </div>
              <div>
                <label className="label" htmlFor="password">Mot de passe</label>
                <input id="password" name="password" type="password" required className="input" />
              </div>
            </div>
            {state.error && <p className="text-sm text-red-600">{state.error}</p>}
            <SubmitBtn />
          </form>
          <p className="mt-4 text-center text-sm text-navy-500">
            Déjà inscrit ? <Link href="/login" className="font-medium text-gold-600">Se connecter</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
