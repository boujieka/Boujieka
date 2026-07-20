import Link from "next/link";
import { requireUser } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import type { Prisma } from "@prisma/client";
import { Card, LinkButton, EmptyState, Badge, RatingBadge } from "@/components/ui";
import { fmtInt, fmtPct, STAGE_LABELS } from "@/lib/format";

export default async function OpportunitiesPage() {
  const session = await requireUser();

  // Offtaker : ses opportunités. Développeur/Admin : les opportunités qualifiées.
  const where: Prisma.OpportunityWhereInput =
    session.role === "offtaker"
      ? { site: { organizationId: session.organizationId }, deletedAt: null }
      : { qualificationStatus: "qualifiee", deletedAt: null };

  const opportunities = await prisma.opportunity.findMany({
    where,
    include: { site: true, prefeasibility: true, decarbonization: true, bankability: true },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Opportunités</h1>
          <p className="text-sm text-navy-500">
            {session.role === "offtaker"
              ? "Vos originations et leur progression."
              : "Opportunités qualifiées ouvertes à l'intérêt des développeurs."}
          </p>
        </div>
        {session.role === "offtaker" && (
          <LinkButton href="/opportunities/new" variant="gold">+ Nouvelle opportunité</LinkButton>
        )}
      </div>

      {opportunities.length === 0 ? (
        <EmptyState title="Aucune opportunité" />
      ) : (
        <div className="overflow-hidden rounded-xl border border-navy-100 bg-white shadow-card">
          <table className="w-full text-sm">
            <thead className="bg-navy-50 text-left text-xs uppercase tracking-wide text-navy-500">
              <tr>
                <th className="px-4 py-3">Opportunité</th>
                <th className="px-4 py-3">Pays</th>
                <th className="px-4 py-3">Étape</th>
                <th className="px-4 py-3">Couverture</th>
                <th className="px-4 py-3">CO₂/an</th>
                <th className="px-4 py-3">Bancabilité</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-50">
              {opportunities.map((o) => (
                <tr key={o.id} className="hover:bg-navy-50/50">
                  <td className="px-4 py-3">
                    <Link href={`/opportunities/${o.id}`} className="font-medium text-navy-800 hover:text-gold-600">
                      {o.title}
                    </Link>
                    <div className="text-xs text-navy-400">{o.site.name}</div>
                  </td>
                  <td className="px-4 py-3">{o.site.country}</td>
                  <td className="px-4 py-3"><Badge tone="muted">{STAGE_LABELS[o.stage]}</Badge></td>
                  <td className="px-4 py-3">{o.prefeasibility ? fmtPct(o.prefeasibility.coverageRate) : "—"}</td>
                  <td className="px-4 py-3">{o.decarbonization ? `${fmtInt(o.decarbonization.annualCo2AvoidedTonnes)} t` : "—"}</td>
                  <td className="px-4 py-3">{o.bankability ? <RatingBadge rating={o.bankability.rating} /> : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
