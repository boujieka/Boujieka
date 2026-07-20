"use server";

import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/db";
import { getSession } from "@/lib/auth/session";
import { developerProfileSchema } from "@/lib/validation";
import type { FormState } from "./sites";

export async function upsertDeveloperProfileAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "developer") return { error: "Accès réservé aux développeurs." };

  const countriesRaw = formData.getAll("countries").map(String).filter(Boolean);
  const countries =
    countriesRaw.length === 1
      ? countriesRaw[0].split(/[\s,;]+/).map((c) => c.trim()).filter(Boolean)
      : countriesRaw;
  const raw = {
    minProjectSizeKw: formData.get("minProjectSizeKw"),
    maxProjectSizeKw: formData.get("maxProjectSizeKw"),
    financingCapacity: formData.get("financingCapacity"),
    trackRecordMw: formData.get("trackRecordMw"),
    projectsCompleted: formData.get("projectsCompleted"),
    countries,
    technologies: formData.getAll("technologies").map(String),
  };
  const parsed = developerProfileSchema.safeParse(raw);
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  const d = parsed.data;
  if (d.maxProjectSizeKw < d.minProjectSizeKw) return { error: "Taille max < taille min." };

  await prisma.$transaction(async (tx) => {
    const profile = await tx.developerProfile.upsert({
      where: { organizationId: session.organizationId },
      update: {
        minProjectSizeKw: d.minProjectSizeKw,
        maxProjectSizeKw: d.maxProjectSizeKw,
        financingCapacity: d.financingCapacity,
        trackRecordMw: d.trackRecordMw,
        projectsCompleted: d.projectsCompleted,
      },
      create: {
        organizationId: session.organizationId,
        minProjectSizeKw: d.minProjectSizeKw,
        maxProjectSizeKw: d.maxProjectSizeKw,
        financingCapacity: d.financingCapacity,
        trackRecordMw: d.trackRecordMw,
        projectsCompleted: d.projectsCompleted,
      },
    });

    // Remplace zones et technologies.
    await tx.developerZone.deleteMany({ where: { developerProfileId: profile.id } });
    await tx.developerTechnology.deleteMany({ where: { developerProfileId: profile.id } });
    await tx.developerZone.createMany({
      data: d.countries.map((c) => ({ developerProfileId: profile.id, country: c.toUpperCase() })),
    });
    await tx.developerTechnology.createMany({
      data: d.technologies.map((technology) => ({ developerProfileId: profile.id, technology })),
    });
  });

  revalidatePath("/developers/profile");
  return {};
}
