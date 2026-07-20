import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";
import { getApiSession } from "@/lib/auth/guards";
import { runMatching } from "@/lib/analysis/run-matching";

/**
 * POST /api/opportunities/:id/matching
 * Exécute le moteur de matching pondéré et persiste les appariements.
 * GET renvoie les matches existants classés par score décroissant.
 */
export async function POST(_req: NextRequest, { params }: { params: { id: string } }) {
  const session = await getApiSession();
  if (!session) return NextResponse.json({ error: "Non authentifié" }, { status: 401 });

  const opp = await prisma.opportunity.findUnique({
    where: { id: params.id },
    include: { site: true },
  });
  if (!opp) return NextResponse.json({ error: "Opportunité introuvable" }, { status: 404 });
  const isOwner = opp.site.organizationId === session.organizationId;
  if (!isOwner && session.role !== "admin") {
    return NextResponse.json({ error: "Non autorisé" }, { status: 403 });
  }

  try {
    const result = await runMatching(params.id, { userId: session.userId });
    return NextResponse.json({ ok: true, ...result });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 422 });
  }
}

export async function GET(_req: NextRequest, { params }: { params: { id: string } }) {
  const session = await getApiSession();
  if (!session) return NextResponse.json({ error: "Non authentifié" }, { status: 401 });

  const matches = await prisma.match.findMany({
    where: { opportunityId: params.id },
    orderBy: { compatibilityScore: "desc" },
    include: { developerProfile: { include: { organization: true } } },
  });
  return NextResponse.json({ matches });
}
