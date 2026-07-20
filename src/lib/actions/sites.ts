"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/db";
import { getSession } from "@/lib/auth/session";
import { siteSchema } from "@/lib/validation";
import { generateSectoralProfile, type SectorTemplate } from "@/lib/load-profiles/sectoral";

export interface FormState {
  error?: string;
}

export async function createSiteAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "offtaker") return { error: "Accès réservé aux offtakers." };

  const parsed = siteSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  const d = parsed.data;

  const site = await prisma.site.create({
    data: {
      organizationId: session.organizationId,
      name: d.name,
      latitude: d.latitude,
      longitude: d.longitude,
      country: d.country.toUpperCase(),
      availableAreaM2: d.availableAreaM2,
      currentGridTariff: d.currentGridTariff,
      annualConsumptionKwh: d.annualConsumptionKwh,
      peakDemandKw: d.peakDemandKw,
      loadCriticality: d.loadCriticality,
      outageCostPerHour: d.outageCostPerHour,
      gridOutageHoursYear: d.gridOutageHoursYear,
    },
  });

  // Mode de saisie simplifié : génération d'un profil-type sectoriel si
  // consommation annuelle et gabarit fournis.
  if (d.sectorTemplate && d.annualConsumptionKwh) {
    const hourlyKw = generateSectoralProfile(
      d.sectorTemplate as SectorTemplate,
      d.annualConsumptionKwh,
      d.peakDemandKw,
    );
    await prisma.loadProfile.create({
      data: {
        siteId: site.id,
        hourlyKw,
        source: `profil_type:${d.sectorTemplate}`,
        sectorTemplate: d.sectorTemplate,
      },
    });
  }

  revalidatePath("/sites");
  redirect(`/sites/${site.id}`);
}

/** Régénère la courbe de charge d'un site depuis un gabarit sectoriel. */
export async function regenerateProfileAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const session = await getSession();
  if (!session || session.role !== "offtaker") return { error: "Accès réservé aux offtakers." };

  const siteId = String(formData.get("siteId"));
  const template = String(formData.get("sectorTemplate")) as SectorTemplate;
  const site = await prisma.site.findFirst({ where: { id: siteId, organizationId: session.organizationId } });
  if (!site) return { error: "Site introuvable." };
  if (!site.annualConsumptionKwh) return { error: "Renseigner la consommation annuelle du site." };

  const hourlyKw = generateSectoralProfile(template, site.annualConsumptionKwh, site.peakDemandKw ?? undefined);
  await prisma.loadProfile.upsert({
    where: { siteId },
    update: { hourlyKw, source: `profil_type:${template}`, sectorTemplate: template },
    create: { siteId, hourlyKw, source: `profil_type:${template}`, sectorTemplate: template },
  });

  revalidatePath(`/sites/${siteId}`);
  return {};
}
