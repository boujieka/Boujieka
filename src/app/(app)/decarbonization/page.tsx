import Link from "next/link";
import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import type { Prisma } from "@prisma/client";
import { Card, SectionTitle, Stat, EmptyState } from "@/components/ui";
import { aggregatePortfolio } from "@/lib/decarbonization";
import { fmtInt } from "@/lib/format";

export default async function DecarbonizationPage() {
  const session = await requireRole("offtaker", "admin");

  const where: Prisma.OpportunityWhereInput =
    session.role === "offtaker"
      ? { site: { organizationId: session.organizationId }, deletedAt: null }
      : { deletedAt: null };

  const opportunities = await prisma.opportunity.findMany({
    where,
    include: { site: true, decarbonization: { include: { gridEmissionFactor: true } }, prefeasibility: true },
    orderBy: { createdAt: "desc" },
  });

  const withMetrics = opportunities.filter((o) => o.decarbonization);
  const portfolio = aggregatePortfolio(
    withMetrics.map((o) => ({
      annualCo2AvoidedTonnes: o.decarbonization!.annualCo2AvoidedTonnes,
      lifetimeCo2AvoidedTonnes: o.decarbonization!.lifetimeCo2AvoidedTonnes,
    })),
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Suivi de décarbonisation</h1>
        <p className="text-sm text-navy-500">
          tCO₂ évitées via le facteur d'émission réseau par pays — {session.role === "admin" ? "portefeuille global" : "votre portefeuille"}.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Stat label="CO₂ évité / an" value={`${fmtInt(portfolio.annualCo2AvoidedTonnes)} t`} accent="vert" />
        <Stat label="CO₂ évité (durée de vie)" value={`${fmtInt(portfolio.lifetimeCo2AvoidedTonnes)} t`} accent="vert" />
        <Stat label="Opportunités chiffrées" value={fmtInt(withMetrics.length)} accent="navy" />
      </div>

      <Card>
        <SectionTitle>Détail par opportunité</SectionTitle>
        {withMetrics.length === 0 ? (
          <EmptyState title="Aucune métrique de décarbonisation">
            Lancez la pré-faisabilité d'une opportunité pour chiffrer le CO₂ évité.
          </EmptyState>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-left text-xs uppercase tracking-wide text-navy-400">
              <tr>
                <th className="py-2">Opportunité</th>
                <th className="py-2">Pays</th>
                <th className="py-2">Facteur</th>
                <th className="py-2">CO₂/an</th>
                <th className="py-2">CO₂ vie</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-50">
              {withMetrics.map((o) => (
                <tr key={o.id}>
                  <td className="py-2">
                    <Link href={`/opportunities/${o.id}`} className="font-medium hover:text-gold-600">{o.title}</Link>
                  </td>
                  <td className="py-2">{o.site.country}</td>
                  <td className="py-2">{o.decarbonization!.gridEmissionFactor?.emissionFactorTco2PerMwh.toFixed(2) ?? "—"} tCO₂/MWh</td>
                  <td className="py-2 font-medium text-vert-700">{fmtInt(o.decarbonization!.annualCo2AvoidedTonnes)} t</td>
                  <td className="py-2">{fmtInt(o.decarbonization!.lifetimeCo2AvoidedTonnes)} t</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}
