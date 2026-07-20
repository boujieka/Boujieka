/**
 * Amorçage de la base ATEN.
 *
 * - Facteurs d'émission réseau par pays (référentiel, focus Afrique centrale).
 * - Un jeu de démonstration : un offtaker (site industriel) et un développeur,
 *   avec comptes de connexion, pour illustrer les deux faces de la plateforme.
 *
 * Idempotent : ré-exécutable via `npm run db:seed`.
 */
import { PrismaClient } from "@prisma/client";
import { hash } from "bcryptjs";
import { generateSectoralProfile } from "../src/lib/load-profiles/sectoral";

const prisma = new PrismaClient();

/**
 * Facteurs d'émission du réseau (tCO2/MWh). Les valeurs d'Afrique centrale
 * varient fortement selon le mix hydro-thermique national ; versionnées par
 * année et à réviser périodiquement.
 */
const EMISSION_FACTORS: {
  country: string;
  factor: number;
  source: string;
  year: number;
}[] = [
  { country: "CM", factor: 0.28, source: "IFI 2021 / mix hydro-thermique", year: 2021 },
  { country: "GA", factor: 0.42, source: "IFI 2021", year: 2021 },
  { country: "CG", factor: 0.55, source: "IFI 2021", year: 2021 },
  { country: "CD", factor: 0.03, source: "IFI 2021 / dominante hydro", year: 2021 },
  { country: "TD", factor: 0.62, source: "IFI 2021 / thermique", year: 2021 },
  { country: "CF", factor: 0.58, source: "IFI 2021 / thermique", year: 2021 },
  { country: "GQ", factor: 0.5, source: "IFI 2021", year: 2021 },
  { country: "CI", factor: 0.4, source: "IFI 2021", year: 2021 },
  { country: "SN", factor: 0.52, source: "IFI 2021", year: 2021 },
  { country: "NG", factor: 0.44, source: "IFI 2021", year: 2021 },
  { country: "GH", factor: 0.35, source: "IFI 2021", year: 2021 },
  { country: "KE", factor: 0.25, source: "IFI 2021 / géothermie+hydro", year: 2021 },
  { country: "ZA", factor: 0.9, source: "IFI 2021 / charbon", year: 2021 },
  { country: "MA", factor: 0.61, source: "IFI 2021", year: 2021 },
  { country: "FR", factor: 0.05, source: "IEA 2022 / nucléaire", year: 2022 },
];

async function seedEmissionFactors() {
  for (const e of EMISSION_FACTORS) {
    await prisma.gridEmissionFactor.upsert({
      where: { country: e.country },
      update: { emissionFactorTco2PerMwh: e.factor, source: e.source, year: e.year },
      create: {
        country: e.country,
        emissionFactorTco2PerMwh: e.factor,
        source: e.source,
        year: e.year,
      },
    });
  }
  console.log(`✔ ${EMISSION_FACTORS.length} facteurs d'émission`);
}

async function seedDemo() {
  const password = await hash("demo1234", 10);

  // --- Face offtaker : industriel camerounais ---
  const offtakerOrg = await prisma.organization.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000a1" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000a1",
      name: "Cimenterie du Wouri",
      type: "offtaker",
      country: "CM",
      sector: "Industrie — matériaux",
      description: "Cimenterie à Douala, consommation continue, réseau instable.",
    },
  });

  await prisma.user.upsert({
    where: { email: "offtaker@aten.demo" },
    update: {},
    create: {
      organizationId: offtakerOrg.id,
      email: "offtaker@aten.demo",
      passwordHash: password,
      fullName: "Awa Njoya (Cimenterie du Wouri)",
      role: "offtaker",
    },
  });

  const site = await prisma.site.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000b1" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000b1",
      organizationId: offtakerOrg.id,
      name: "Usine de Bonabéri",
      latitude: 4.07,
      longitude: 9.68,
      country: "CM",
      availableAreaM2: 25000,
      currentGridTariff: 0.14,
      annualConsumptionKwh: 8_760_000, // ~1 MW moyen
      peakDemandKw: 1400,
      loadCriticality: "critique",
      outageCostPerHour: 5000,
      gridOutageHoursYear: 400,
    },
  });

  const hourlyKw = generateSectoralProfile("industrie_continue", 8_760_000, 1400);
  await prisma.loadProfile.upsert({
    where: { siteId: site.id },
    update: { hourlyKw, source: "profil_type:industrie_continue", sectorTemplate: "industrie_continue" },
    create: {
      siteId: site.id,
      hourlyKw,
      source: "profil_type:industrie_continue",
      sectorTemplate: "industrie_continue",
    },
  });

  await prisma.opportunity.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000c1" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000c1",
      siteId: site.id,
      title: "Solarisation + secours — Usine de Bonabéri",
      stage: "identifiee",
      targetReliabilityRate: 0.95,
    },
  });

  // --- Face développeur ---
  const devOrg = await prisma.organization.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000a2" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000a2",
      name: "Sahel Solar Developers",
      type: "developer",
      country: "CM",
      sector: "Développement EnR",
      description: "Développeur solaire + stockage, Afrique centrale et de l'Ouest.",
    },
  });

  await prisma.user.upsert({
    where: { email: "developer@aten.demo" },
    update: {},
    create: {
      organizationId: devOrg.id,
      email: "developer@aten.demo",
      passwordHash: password,
      fullName: "Koffi Mensah (Sahel Solar)",
      role: "developer",
    },
  });

  const devProfile = await prisma.developerProfile.upsert({
    where: { organizationId: devOrg.id },
    update: {},
    create: {
      organizationId: devOrg.id,
      minProjectSizeKw: 200,
      maxProjectSizeKw: 5000,
      financingCapacity: "mixte",
      trackRecordMw: 45,
      projectsCompleted: 12,
    },
  });

  for (const country of ["CM", "GA", "CI", "SN"]) {
    await prisma.developerZone.upsert({
      where: { id: `zone-${devProfile.id}-${country}` },
      update: {},
      create: { id: `zone-${devProfile.id}-${country}`, developerProfileId: devProfile.id, country },
    });
  }
  for (const technology of ["solaire", "stockage", "hybride"] as const) {
    await prisma.developerTechnology.upsert({
      where: { developerProfileId_technology: { developerProfileId: devProfile.id, technology } },
      update: {},
      create: { developerProfileId: devProfile.id, technology },
    });
  }

  // --- Administrateur plateforme (Aigle Group) ---
  const adminOrg = await prisma.organization.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000a0" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000a0",
      name: "Aigle Group (opérateur ATEN)",
      type: "developer",
      country: "CM",
      sector: "Plateforme",
    },
  });
  await prisma.user.upsert({
    where: { email: "admin@aten.demo" },
    update: {},
    create: {
      organizationId: adminOrg.id,
      email: "admin@aten.demo",
      passwordHash: password,
      fullName: "Opérateur ATEN",
      role: "admin",
    },
  });

  console.log("✔ Jeu de démonstration (offtaker / developer / admin)");
  console.log("  Connexions : offtaker@aten.demo · developer@aten.demo · admin@aten.demo (mdp : demo1234)");
}

async function main() {
  await seedEmissionFactors();
  await seedDemo();
}

main()
  .then(() => prisma.$disconnect())
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
