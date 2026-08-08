"use client";

import { useTransition } from "react";
import { logoutAction } from "./actions";
import { Button } from "@/components/ui/button";

export function LogoutButton() {
  const [pending, startTransition] = useTransition();

  return (
    <Button
      type="button"
      variant="secondary"
      size="sm"
      disabled={pending}
      onClick={() => startTransition(() => logoutAction())}
    >
      {pending ? "Déconnexion…" : "Se déconnecter"}
    </Button>
  );
}
