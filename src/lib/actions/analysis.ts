"use server";

import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/db";
import { getSession } from "@/lib/auth/session";
import { runPrefeasibility } from "@/lib/analysis/run-prefeasibility";
import { runMatching } from "@/lib/analysis/run-matching";
import { qualifyOpportunity, generateConceptNote } from "@/lib/ai/claude";
import type { FormState } from "./sites";

/** Vérifie que l'utilisateur peut instruire l'opportunité (propriétaire offtaker ou admin). */
async function assertCanAnalyze(opportunityId: string) {
  const session = await getSession();
  if (!session) return { session: null, opp: null, error: "Non authentifié." as const };
  const opp = await prisma.opportunity.findUnique({
    where: { id: opportunityId },
    include: { site: true },
  });
  if (!opp) return { session, opp: null, error: "Opportunité introuvable." as const };
  const isOwner = opp.site.organizationId === session.organizationId;
  if (!isOwner && session.role !== "admin") return { session, opp, error: "Non autorisé." as const };
  return { session, opp, error: null };
}

export async function runPrefeasibilityAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const opportunityId = String(formData.get("opportunityId"));
  const { error } = await assertCanAnalyze(opportunityId);
  if (error) return { error };

  const overrides = {
    performanceRatio: formData.get("performanceRatio") ? Number(formData.get("performanceRatio")) : undefined,
    weatherYear: formData.get("weatherYear") ? Number(formData.get("weatherYear")) : undefined,
  };

  try {
    await runPrefeasibility(opportunityId, overrides);
  } catch (e) {
    return { error: (e as Error).message };
  }
  revalidatePath(`/opportunities/${opportunityId}`);
  return {};
}

export async function qualifyAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const opportunityId = String(formData.get("opportunityId"));
  const { session, opp, error } = await assertCanAnalyze(opportunityId);
  if (error || !opp) return { error: error ?? "Erreur." };

  const { summary } = await qualifyOpportunity(
    {
      siteName: opp.site.name,
      country: opp.site.country,
      annualConsumptionKwh: opp.site.annualConsumptionKwh,
      peakDemandKw: opp.site.peakDemandKw,
      loadCriticality: opp.site.loadCriticality,
      outageCostPerHour: opp.site.outageCostPerHour,
      gridOutageHoursYear: opp.site.gridOutageHoursYear,
      currentGridTariff: opp.site.currentGridTariff,
      targetReliabilityRate: opp.targetReliabilityRate,
    },
    { userId: session!.userId, opportunityId },
  );

  await prisma.opportunity.update({
    where: { id: opportunityId },
    data: {
      qualificationSummary: summary,
      qualificationStatus: "qualifiee",
      stage: opp.stage === "identifiee" ? "qualifiee" : opp.stage,
    },
  });
  revalidatePath(`/opportunities/${opportunityId}`);
  return {};
}

export async function runMatchingAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const opportunityId = String(formData.get("opportunityId"));
  const { session, error } = await assertCanAnalyze(opportunityId);
  if (error) return { error };

  try {
    await runMatching(opportunityId, { userId: session!.userId });
  } catch (e) {
    return { error: (e as Error).message };
  }
  revalidatePath(`/opportunities/${opportunityId}`);
  return {};
}

export async function generateConceptNoteAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const opportunityId = String(formData.get("opportunityId"));
  const { session, error } = await assertCanAnalyze(opportunityId);
  if (error) return { error };

  const opp = await prisma.opportunity.findUniqueOrThrow({
    where: { id: opportunityId },
    include: {
      site: true,
      prefeasibility: { include: { technoEconomicModel: true } },
      decarbonization: true,
      bankability: true,
    },
  });
  const pf = opp.prefeasibility;
  const te = pf?.technoEconomicModel;
  if (!pf || !te) return { error: "Pré-faisabilité et modèle technico-économique requis." };

  const { content } = await generateConceptNote(
    {
      title: opp.title,
      siteName: opp.site.name,
      country: opp.site.country,
      pvSizeKwp: pf.pvSizeKwp,
      batterySizeKwh: pf.batterySizeKwh,
      backupSizeKw: pf.backupSizeKw,
      coverageRate: pf.coverageRate,
      residualDeficitKwh: pf.residualDeficitKwh,
      annualCo2AvoidedTonnes: opp.decarbonization?.annualCo2AvoidedTonnes ?? 0,
      lifetimeCo2AvoidedTonnes: opp.decarbonization?.lifetimeCo2AvoidedTonnes ?? 0,
      capex: te.capex,
      ppaTariff: te.ppaTariff,
      irr: te.irr,
      paybackYears: te.paybackYears,
      annualSavings: te.annualSavings,
      currency: te.currency,
      rating: opp.bankability?.rating ?? null,
    },
    { userId: session!.userId, opportunityId },
  );

  const last = await prisma.conceptNote.findFirst({
    where: { opportunityId },
    orderBy: { version: "desc" },
  });
  await prisma.conceptNote.create({
    data: { opportunityId, content, generatedBy: "ia", version: (last?.version ?? 0) + 1 },
  });
  revalidatePath(`/opportunities/${opportunityId}`);
  return {};
}
