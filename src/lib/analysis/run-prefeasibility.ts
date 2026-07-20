/**
 * Orchestrateur de pré-faisabilité.
 *
 * Chaîne complète, exécutée côté serveur, qui relie les modules purs à la base :
 *   productible (NASA POWER) → simulation & dimensionnement à cible fixée →
 *   modèle technico-économique → décarbonisation → bancabilité.
 *
 * Persiste prefeasibility_studies, techno_economic_models,
 * decarbonization_metrics et bankability_scores en une transaction.
 */
import { prisma } from "@/lib/db";
import { physicalDefaults } from "@/lib/config";
import { sizeToTargetReliability, type BatteryParams } from "@/lib/simulation";
import { fetchProductible, syntheticProductible } from "@/lib/nasa-power";
import { computeTechnoEconomic } from "@/lib/techno-economic";
import { computeDecarbonization } from "@/lib/decarbonization";
import { computeBankability } from "@/lib/bankability";

export interface PrefeasibilityOptions {
  performanceRatio?: number;
  battery?: Partial<BatteryParams>;
  weatherYear?: number;
}

export interface PrefeasibilityOutcome {
  productibleSource: "nasa_power" | "synthetic";
  coverageRate: number;
  targetReached: boolean;
  pvSizeKwp: number;
  batterySizeKwh: number;
  backupSizeKw: number;
  rating: string;
}

export async function runPrefeasibility(
  opportunityId: string,
  options: PrefeasibilityOptions = {},
): Promise<PrefeasibilityOutcome> {
  const opportunity = await prisma.opportunity.findUniqueOrThrow({
    where: { id: opportunityId },
    include: { site: { include: { loadProfile: true } } },
  });
  const site = opportunity.site;
  if (!site.loadProfile) {
    throw new Error("Le site n'a pas de courbe de charge. Renseigner un profil avant l'analyse.");
  }

  const load = site.loadProfile.hourlyKw as number[];
  const performanceRatio = options.performanceRatio ?? physicalDefaults.performanceRatio;
  const battery: BatteryParams = {
    roundTrip: options.battery?.roundTrip ?? physicalDefaults.batteryRoundTrip,
    dod: options.battery?.dod ?? physicalDefaults.batteryDod,
    cRate: options.battery?.cRate ?? physicalDefaults.batteryCRate,
  };

  // 1) Productible via NASA POWER (repli synthétique si indisponible).
  const weatherYear = options.weatherYear ?? new Date().getUTCFullYear() - 2;
  let productible;
  try {
    productible = await fetchProductible(site.latitude, site.longitude, performanceRatio, weatherYear);
  } catch (e) {
    console.warn("NASA POWER indisponible, repli synthétique :", (e as Error).message);
    productible = syntheticProductible(performanceRatio);
  }

  // 2) Dimensionnement à fiabilité cible fixée.
  const sizing = sizeToTargetReliability({
    load,
    yieldPerKwp: productible.yieldPerKwp,
    targetReliabilityRate: opportunity.targetReliabilityRate,
    battery,
  });

  // 3) Modèle technico-économique.
  const techno = computeTechnoEconomic({
    pvSizeKwp: sizing.pvSizeKwp,
    batterySizeKwh: sizing.batterySizeKwh,
    backupSizeKw: sizing.backupSizeKw,
    servedRenewableKwh: sizing.simulation.servedRenewableKwh,
    currentGridTariff: site.currentGridTariff ?? 0.15,
  });

  // 4) Décarbonisation via facteur d'émission du pays.
  const factor = await prisma.gridEmissionFactor.findUnique({ where: { country: site.country } });
  const emissionFactor = factor?.emissionFactorTco2PerMwh ?? 0.5;
  const decarb = computeDecarbonization({
    servedRenewableKwh: sizing.simulation.servedRenewableKwh,
    emissionFactorTco2PerMwh: emissionFactor,
  });

  // 5) Bancabilité (avec dimension résilience).
  const bankability = computeBankability({
    irr: techno.irr,
    paybackYears: techno.paybackYears,
    coverageRate: sizing.coverageRate,
    targetReached: sizing.targetReached,
    loadCriticality: site.loadCriticality,
    gridOutageHoursYear: site.gridOutageHoursYear,
    annualCo2AvoidedTonnes: decarb.annualCo2AvoidedTonnes,
    emissionFactorTco2PerMwh: emissionFactor,
  });

  // Trace des hypothèses (objet littéral compatible JSONB Prisma).
  const assumptions = {
    performanceRatio,
    battery: { roundTrip: battery.roundTrip, dod: battery.dod, cRate: battery.cRate },
    productibleSource: productible.source,
    specificYield: productible.specificYield,
    weatherYear: productible.year,
  };

  // Persistance transactionnelle.
  await prisma.$transaction(async (tx) => {
    const study = await tx.prefeasibilityStudy.upsert({
      where: { opportunityId },
      update: {
        pvSizeKwp: sizing.pvSizeKwp,
        batterySizeKwh: sizing.batterySizeKwh,
        backupSizeKw: sizing.backupSizeKw,
        annualYieldKwh: sizing.annualYieldKwh,
        coverageRate: sizing.coverageRate,
        residualDeficitKwh: sizing.residualDeficitKwh,
        reliabilityCost: sizing.reliabilityCost,
        simulationMethod: "cible_fixee",
        assumptions,
      },
      create: {
        opportunityId,
        pvSizeKwp: sizing.pvSizeKwp,
        batterySizeKwh: sizing.batterySizeKwh,
        backupSizeKw: sizing.backupSizeKw,
        annualYieldKwh: sizing.annualYieldKwh,
        coverageRate: sizing.coverageRate,
        residualDeficitKwh: sizing.residualDeficitKwh,
        reliabilityCost: sizing.reliabilityCost,
        simulationMethod: "cible_fixee",
        assumptions,
      },
    });

    await tx.technoEconomicModel.upsert({
      where: { prefeasibilityStudyId: study.id },
      update: {
        capex: techno.capex,
        opexAnnual: techno.opexAnnual,
        ppaTariff: techno.ppaTariff,
        irr: techno.irr,
        paybackYears: techno.paybackYears,
        annualSavings: techno.annualSavings,
        currency: techno.currency,
      },
      create: {
        prefeasibilityStudyId: study.id,
        capex: techno.capex,
        opexAnnual: techno.opexAnnual,
        ppaTariff: techno.ppaTariff,
        irr: techno.irr,
        paybackYears: techno.paybackYears,
        annualSavings: techno.annualSavings,
        currency: techno.currency,
      },
    });

    await tx.decarbonizationMetric.upsert({
      where: { opportunityId },
      update: {
        gridEmissionFactorId: factor?.id ?? null,
        annualCo2AvoidedTonnes: decarb.annualCo2AvoidedTonnes,
        lifetimeCo2AvoidedTonnes: decarb.lifetimeCo2AvoidedTonnes,
      },
      create: {
        opportunityId,
        gridEmissionFactorId: factor?.id ?? null,
        annualCo2AvoidedTonnes: decarb.annualCo2AvoidedTonnes,
        lifetimeCo2AvoidedTonnes: decarb.lifetimeCo2AvoidedTonnes,
      },
    });

    await tx.bankabilityScore.upsert({
      where: { opportunityId },
      update: { ...bankability },
      create: { opportunityId, ...bankability },
    });
  });

  return {
    productibleSource: productible.source,
    coverageRate: sizing.coverageRate,
    targetReached: sizing.targetReached,
    pvSizeKwp: sizing.pvSizeKwp,
    batterySizeKwh: sizing.batterySizeKwh,
    backupSizeKw: sizing.backupSizeKw,
    rating: bankability.rating,
  };
}
