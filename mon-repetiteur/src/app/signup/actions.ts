"use server";

import { redirect } from "next/navigation";
import { signUpWithPassword } from "@/services/auth";

export interface SignupState {
  error: string | null;
  /** True once a confirmation email was sent and the caller should check
   * their inbox instead of being redirected straight in. */
  awaitingConfirmation: boolean;
}

export async function signupAction(
  _prevState: SignupState,
  formData: FormData,
): Promise<SignupState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const fullName = String(formData.get("fullName") ?? "").trim();

  if (!email || !password || !fullName) {
    return { error: "Tous les champs sont requis.", awaitingConfirmation: false };
  }
  if (password.length < 8) {
    return {
      error: "Le mot de passe doit contenir au moins 8 caractères.",
      awaitingConfirmation: false,
    };
  }

  const { error, hasSession } = await signUpWithPassword({ email, password, fullName });
  if (error) {
    return { error, awaitingConfirmation: false };
  }

  if (!hasSession) {
    return { error: null, awaitingConfirmation: true };
  }

  redirect("/account");
}
