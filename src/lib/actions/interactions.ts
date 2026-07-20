"use server";

import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/db";
import { getSession } from "@/lib/auth/session";
import { eoiSchema, messageSchema } from "@/lib/validation";
import type { FormState } from "./sites";

/** Expression d'intérêt d'un développeur sur une opportunité. */
export async function submitEoiAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "developer") return { error: "Réservé aux développeurs." };

  const parsed = eoiSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };

  const profile = await prisma.developerProfile.findUnique({
    where: { organizationId: session.organizationId },
  });
  if (!profile) return { error: "Complétez d'abord votre profil développeur." };

  await prisma.expressionOfInterest.upsert({
    where: {
      opportunityId_developerProfileId: {
        opportunityId: parsed.data.opportunityId,
        developerProfileId: profile.id,
      },
    },
    update: { message: parsed.data.message, status: "soumise" },
    create: {
      opportunityId: parsed.data.opportunityId,
      developerProfileId: profile.id,
      message: parsed.data.message,
    },
  });
  revalidatePath(`/opportunities/${parsed.data.opportunityId}`);
  return {};
}

/** Réponse de l'offtaker à une expression d'intérêt. */
export async function respondEoiAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session) return { error: "Non authentifié." };
  const eoiId = String(formData.get("eoiId"));
  const status = String(formData.get("status"));
  if (!["acceptee", "refusee"].includes(status)) return { error: "Statut invalide." };

  const eoi = await prisma.expressionOfInterest.findUnique({
    where: { id: eoiId },
    include: { opportunity: { include: { site: true } } },
  });
  if (!eoi) return { error: "Introuvable." };
  const isOwner = eoi.opportunity.site.organizationId === session.organizationId;
  if (!isOwner && session.role !== "admin") return { error: "Non autorisé." };

  await prisma.expressionOfInterest.update({
    where: { id: eoiId },
    data: { status: status as "acceptee" | "refusee" },
  });
  revalidatePath(`/opportunities/${eoi.opportunityId}`);
  return {};
}

/** Messagerie intermédiée, rattachée à une opportunité. */
export async function sendMessageAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session) return { error: "Non authentifié." };

  const parsed = messageSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Message invalide" };

  await prisma.message.create({
    data: {
      opportunityId: parsed.data.opportunityId,
      senderUserId: session.userId,
      recipientUserId: parsed.data.recipientUserId,
      body: parsed.data.body,
    },
  });
  revalidatePath(`/opportunities/${parsed.data.opportunityId}`);
  revalidatePath("/messages");
  return {};
}

/** Validation d'un match dans le modèle intermédié (admin). */
export async function updateMatchStatusAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "admin") return { error: "Réservé à l'administrateur." };

  const matchId = String(formData.get("matchId"));
  const status = String(formData.get("status"));
  if (!["propose", "valide_admin", "ecarte"].includes(status)) return { error: "Statut invalide." };

  const match = await prisma.match.update({
    where: { id: matchId },
    data: { status: status as "propose" | "valide_admin" | "ecarte" },
  });
  revalidatePath("/admin/matches");
  revalidatePath(`/opportunities/${match.opportunityId}`);
  return {};
}
