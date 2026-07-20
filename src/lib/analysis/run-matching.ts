/**
 * Orchestrateur du moteur de matching.
 *
 * Pour une opportunité qualifiée : construit les entrées à partir de la
 * pré-faisabilité, applique les filtres durs et le score pondéré, persiste les
 * matches, puis génère les explications en langage naturel via l'API Claude
 * (journalisées en `explication_matching`).
 */
import { prisma } from "@/lib/db";
import {
  computeCompatibility,
  type OpportunityForMatch,
  type DeveloperForMatch,
  type Technology,
} from "@/lib/matching";
import { explainMatch } from "@/lib/ai/claude";

export interface MatchingResult {
  created: number;
  topScore: number | null;
}

/** Déduit les technologies requises par la solution dimensionnée. */
function requiredTechnologies(study: {
  batterySizeKwh: number;
  backupSizeKw: number;
}): Technology[] {
  const req: Technology[] = ["solaire"];
  if (study.batterySizeKwh > 0) {
    req.push("stockage");
    req.push("hybride"); // solaire + stockage ⇒ solution hybride
  }
  if (study.backupSizeKw > 0) req.push("groupe_backup");
  return req;
}

export async function runMatching(
  opportunityId: string,
  meta: { userId?: string } = {},
): Promise<MatchingResult> {
  const opportunity = await prisma.opportunity.findUniqueOrThrow({
    where: { id: opportunityId },
    include: { site: true, prefeasibility: true, bankability: true },
  });
  if (!opportunity.prefeasibility) {
    throw new Error("Pré-faisabilité requise avant le matching.");
  }

  const oppForMatch: OpportunityForMatch = {
    country: opportunity.site.country,
    region: null,
    projectSizeKw: opportunity.prefeasibility.pvSizeKwp,
    requiredTechnologies: requiredTechnologies(opportunity.prefeasibility),
    rating: opportunity.bankability?.rating ?? null,
  };

  const developers = await prisma.developerProfile.findMany({
    include: { zones: true, technologies: true, organization: true },
  });

  let created = 0;
  let topScore: number | null = null;

  for (const dev of developers) {
    const devForMatch: DeveloperForMatch = {
      zones: dev.zones.map((z) => ({ country: z.country, region: z.region })),
      technologies: dev.technologies.map((t) => t.technology),
      minProjectSizeKw: dev.minProjectSizeKw,
      maxProjectSizeKw: dev.maxProjectSizeKw,
      financingCapacity: dev.financingCapacity,
    };

    const result = computeCompatibility(oppForMatch, devForMatch);
    if (result.hardFiltered || result.compatibilityScore <= 0) {
      // On retire un éventuel ancien match devenu incompatible.
      await prisma.match.deleteMany({
        where: { opportunityId, developerProfileId: dev.id },
      });
      continue;
    }

    // Explication en langage naturel (API Claude, avec repli déterministe).
    const { explanation } = await explainMatch(
      {
        opportunityTitle: opportunity.title,
        developerName: dev.organization.name,
        geographyScore: result.geographyScore,
        technologyScore: result.technologyScore,
        sizeScore: result.sizeScore,
        bankabilityAlignment: result.bankabilityAlignment,
        compatibilityScore: result.compatibilityScore,
        projectSizeKw: oppForMatch.projectSizeKw,
        developerRange: { min: dev.minProjectSizeKw, max: dev.maxProjectSizeKw },
      },
      { userId: meta.userId, opportunityId },
    );

    await prisma.match.upsert({
      where: { opportunityId_developerProfileId: { opportunityId, developerProfileId: dev.id } },
      update: {
        geographyScore: result.geographyScore,
        sizeScore: result.sizeScore,
        technologyScore: result.technologyScore,
        bankabilityAlignment: result.bankabilityAlignment,
        compatibilityScore: result.compatibilityScore,
        explanation,
      },
      create: {
        opportunityId,
        developerProfileId: dev.id,
        geographyScore: result.geographyScore,
        sizeScore: result.sizeScore,
        technologyScore: result.technologyScore,
        bankabilityAlignment: result.bankabilityAlignment,
        compatibilityScore: result.compatibilityScore,
        explanation,
        status: "propose",
      },
    });

    created++;
    if (topScore === null || result.compatibilityScore > topScore) {
      topScore = result.compatibilityScore;
    }
  }

  return { created, topScore };
}
