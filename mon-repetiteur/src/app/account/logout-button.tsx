"use client";

import { useTransition } from "react";
import { logoutAction } from "./actions";

export function LogoutButton() {
  const [pending, startTransition] = useTransition();

  return (
    <button
      type="button"
      disabled={pending}
      onClick={() => startTransition(() => logoutAction())}
      className="rounded border border-zinc-300 px-4 py-2 text-sm disabled:opacity-50 dark:border-zinc-700"
    >
      {pending ? "Déconnexion…" : "Se déconnecter"}
    </button>
  );
}
