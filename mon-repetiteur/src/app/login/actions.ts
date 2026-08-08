"use server";

import { redirect } from "next/navigation";
import { signInWithPassword } from "@/services/auth";

export interface LoginState {
  error: string | null;
}

export async function loginAction(
  _prevState: LoginState,
  formData: FormData,
): Promise<LoginState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");

  if (!email || !password) {
    return { error: "Email et mot de passe requis." };
  }

  const { error } = await signInWithPassword({ email, password });
  if (error) {
    return { error };
  }

  redirect("/account");
}
