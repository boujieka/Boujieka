import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/db";
import { getApiSession } from "@/lib/auth/guards";
import { runPrefeasibility } from "@/lib/analysis/run-prefeasibility";

/**
 * POST /api/opportunities/:id/prefeasibility
 * Lance la chaîne de pré-faisabilité (simulation → technico-éco → CO₂ → banca).
 * Corps optionnel : { performanceRatio?, weatherYear?, battery? }.
 */
export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
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

  const body = await req.json().catch(() => ({}));
  try {
    const outcome = await runPrefeasibility(params.id, {
      performanceRatio: body.performanceRatio,
      weatherYear: body.weatherYear,
      battery: body.battery,
    });
    return NextResponse.json({ ok: true, outcome });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 422 });
  }
}
