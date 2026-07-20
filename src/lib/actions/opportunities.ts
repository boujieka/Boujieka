"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/db";
import { getSession } from "@/lib/auth/session";
import { opportunitySchema } from "@/lib/validation";
import type { FormState } from "./sites";

const STAGES = [
  "identifiee",
  "qualifiee",
  "term_sheet",
  "mandat",
  "bouclage_financier",
  "realisee",
  "abandonnee",
] as const;

export async function createOpportunityAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "offtaker") return { error: "Accès réservé aux offtakers." };

  const parsed = opportunitySchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  const d = parsed.data;

  // Le site doit appartenir à l'organisation de l'utilisateur.
  const site = await prisma.site.findFirst({
    where: { id: d.siteId, organizationId: session.organizationId },
  });
  if (!site) return { error: "Site introuvable." };

  const opp = await prisma.opportunity.create({
    data: {
      siteId: d.siteId,
      title: d.title,
      targetReliabilityRate: d.targetReliabilityRate,
      ownerUserId: session.userId,
    },
  });

  revalidatePath("/opportunities");
  redirect(`/opportunities/${opp.id}`);
}

/** Fait progresser une opportunité dans le pipeline (offtaker propriétaire / admin). */
export async function updateStageAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session) return { error: "Non authentifié." };

  const opportunityId = String(formData.get("opportunityId"));
  const stage = String(formData.get("stage"));
  if (!STAGES.includes(stage as (typeof STAGES)[number])) return { error: "Étape invalide." };

  const opp = await prisma.opportunity.findUnique({ where: { id: opportunityId }, include: { site: true } });
  if (!opp) return { error: "Opportunité introuvable." };
  const isOwner = opp.site.organizationId === session.organizationId;
  if (!isOwner && session.role !== "admin") return { error: "Non autorisé." };

  await prisma.opportunity.update({
    where: { id: opportunityId },
    data: { stage: stage as (typeof STAGES)[number] },
  });
  revalidatePath(`/opportunities/${opportunityId}`);
  return {};
}
