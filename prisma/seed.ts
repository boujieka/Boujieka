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

/**
 * Cas d'usage réel — Industrie du Congo (INDUCO), Brazzaville.
 * Preneur d'ancrage industriel : unité manufacturière multi-produits (~700
 * emplois) alimentée par diesel de secours devenu source principale
 * (~2,64 M USD/an), plafonnée à ~50 % de sa capacité, avec un déficit de
 * puissance hors réseau d'environ 1 680 kW et 20 200 m² de toitures.
 * Chiffres indicatifs, à consolider en étude de faisabilité.
 */
async function seedInduco() {
  const password = await hash("demo1234", 10);

  const org = await prisma.organization.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000d1" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000d1",
      name: "Industrie du Congo (INDUCO)",
      type: "offtaker",
      country: "CG",
      sector: "Industrie manufacturière multi-produits",
      description:
        "Unité manufacturière multi-produits à Brazzaville (~700 emplois), " +
        "confrontée à une insécurité chronique d'approvisionnement électrique.",
    },
  });

  await prisma.user.upsert({
    where: { email: "induco@aten.demo" },
    update: {},
    create: {
      organizationId: org.id,
      email: "induco@aten.demo",
      passwordHash: password,
      fullName: "Direction INDUCO",
      role: "offtaker",
    },
  });

  const site = await prisma.site.upsert({
    where: { id: "00000000-0000-0000-0000-0000000000d2" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000d2",
      organizationId: org.id,
      name: "Site de Massissia (Madibou, Brazzaville)",
      latitude: -4.35,
      longitude: 15.18,
      country: "CG",
      availableAreaM2: 20200, // trois hangars (note §3.3)
      // Coût actuel de l'énergie, dominé par le diesel devenu source principale.
      // Dérivation : 2,64 M$/an ÷ ~12 GWh servis (production plafonnée à 50 %)
      // ≈ 0,22 $/kWh de carburant ; + O&M, lubrifiants et révisions (~35 %)
      // ≈ 0,30 $/kWh. Ce n'est PAS le tarif E2C nominal (réseau indisponible la
      // majorité du temps) mais le coût réellement supporté — base des économies.
      currentGridTariff: 0.3,
      // Énergie en PLEINE production (charge à servir pour lever le plafond à
      // 50 %) : ≈ 24 GWh/an, soit un fonctionnement largement continu à ~2 740 kW
      // moyen (= 4 600 kW de pointe × facteur de charge ~0,60). Le profil horaire
      // est modélisé comme continu (gabarit « industrie_continue »).
      annualConsumptionKwh: 24_000_000,
      // Pointe de CONCEPTION en pleine production (transfo 5 750 kVA × cos φ 0,8
      // ≈ 4 600 kW) — supérieure au tirage horaire moyen ; réserve pour
      // l'expansion (projet de recyclage évoqué dans la note).
      peakDemandKw: 4600,
      loadCriticality: "critique",
      // Coût d'une heure de non-fourniture ≈ déficit hors réseau 1 680 kW ×
      // valeur de la charge perdue (VoLL industriel conservateur ~2 $/kWh)
      // ≈ 3 400 $/h. Cohérent avec un coût d'opportunité > facture diesel (note §4).
      outageCostPerHour: 3400,
      // Réseau E2C indisponible la majorité du temps (diesel = source principale) :
      // ~57 % de 8760 h ≈ 5 000 h/an d'indisponibilité subie.
      gridOutageHoursYear: 5000,
    },
  });

  const hourlyKw = generateSectoralProfile("industrie_continue", 24_000_000, 4600);
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
    where: { id: "00000000-0000-0000-0000-0000000000d3" },
    update: {},
    create: {
      id: "00000000-0000-0000-0000-0000000000d3",
      siteId: site.id,
      title: "Solaire + stockage + secours — INDUCO Brazzaville",
      stage: "identifiee",
      targetReliabilityRate: 0.97, // fermeté de fourniture recherchée
    },
  });

  console.log("✔ Cas d'usage INDUCO (Industrie du Congo, Brazzaville)");
  console.log("  Connexion : induco@aten.demo (mdp : demo1234)");
}

async function main() {
  await seedEmissionFactors();
  await seedDemo();
  await seedInduco();
}

main()
  .then(() => prisma.$disconnect())
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
