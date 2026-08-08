// Seed skeleton for local/dev databases. Run with `npm run db:seed`
// (wraps `prisma db seed`, configured in prisma.config.ts).
//
// This only seeds the Subject taxonomy — the reference data every later
// phase hangs off of. Full curriculum content (topics/chapters) is
// populated in the Curriculum phase, not here.
import "dotenv/config";
import { PrismaClient } from "../src/generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

const CORE_SUBJECTS = [
  { slug: "mathematiques", name: "Mathématiques" },
  { slug: "francais", name: "Français" },
  { slug: "histoire-geographie", name: "Histoire-Géographie" },
  { slug: "sciences-vie-terre", name: "Sciences de la Vie et de la Terre" },
  { slug: "physique-chimie", name: "Physique-Chimie" },
  { slug: "anglais", name: "Anglais" },
] as const;

async function main() {
  for (const subject of CORE_SUBJECTS) {
    await prisma.subject.upsert({
      where: { slug: subject.slug },
      update: { name: subject.name },
      create: subject,
    });
  }
  console.log(`Seeded ${CORE_SUBJECTS.length} subjects.`);
}

main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
