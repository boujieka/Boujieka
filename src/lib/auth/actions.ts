"use server";

import { hash, compare } from "bcryptjs";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/db";
import { registerSchema, loginSchema } from "@/lib/validation";
import { createSessionCookie, clearSessionCookie, type Role } from "./session";

export interface ActionState {
  error?: string;
}

export async function registerAction(
  _prev: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const parsed = registerSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  }
  const d = parsed.data;

  const existing = await prisma.user.findUnique({ where: { email: d.email } });
  if (existing) return { error: "Un compte existe déjà avec cet email." };

  const passwordHash = await hash(d.password, 10);
  const user = await prisma.$transaction(async (tx) => {
    const org = await tx.organization.create({
      data: {
        name: d.organizationName,
        type: d.organizationType,
        country: d.country.toUpperCase(),
        sector: d.sector,
      },
    });
    return tx.user.create({
      data: {
        organizationId: org.id,
        email: d.email,
        passwordHash,
        fullName: d.fullName,
        role: d.organizationType as Role, // offtaker | developer
      },
    });
  });

  await createSessionCookie({
    userId: user.id,
    organizationId: user.organizationId,
    role: user.role as Role,
    email: user.email,
    fullName: user.fullName,
  });
  redirect("/dashboard");
}

export async function loginAction(
  _prev: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const parsed = loginSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  }
  const { email, password } = parsed.data;

  const user = await prisma.user.findUnique({ where: { email } });
  if (!user || !user.isActive) return { error: "Identifiants invalides." };

  const ok = await compare(password, user.passwordHash);
  if (!ok) return { error: "Identifiants invalides." };

  await createSessionCookie({
    userId: user.id,
    organizationId: user.organizationId,
    role: user.role as Role,
    email: user.email,
    fullName: user.fullName,
  });
  redirect("/dashboard");
}

export async function logoutAction(): Promise<void> {
  clearSessionCookie();
  redirect("/login");
}
