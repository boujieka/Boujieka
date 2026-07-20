import Link from "next/link";
import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, EmptyState, Badge } from "@/components/ui";
import { fmtInt } from "@/lib/format";

export default async function MatchingPage() {
  const session = await requireRole("developer");
  const profile = await prisma.developerProfile.findUnique({
    where: { organizationId: session.organizationId },
  });

  const matches = profile
    ? await prisma.match.findMany({
        where: { developerProfileId: profile.id },
        orderBy: { compatibilityScore: "desc" },
        include: { opportunity: { include: { site: true, bankability: true } } },
      })
    : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Mes appariements</h1>
        <p className="text-sm text-navy-500">
          Opportunités appariées à votre profil, classées par score de compatibilité.
        </p>
      </div>

      {!profile ? (
        <EmptyState title="Profil développeur incomplet">
          <Link href="/developers/profile" className="btn-primary">Compléter mon profil</Link>
        </EmptyState>
      ) : matches.length === 0 ? (
        <EmptyState title="Aucun appariement pour l'instant">
          Les appariements apparaissent lorsqu'un offtaker lance le matching sur une opportunité qualifiée.
        </EmptyState>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {matches.map((m) => (
            <Card key={m.id}>
              <div className="flex items-start justify-between">
                <Link href={`/opportunities/${m.opportunityId}`} className="font-semibold hover:text-gold-600">
                  {m.opportunity.title}
                </Link>
                <span className="text-xl font-bold text-gold-600">{(m.compatibilityScore * 100).toFixed(0)}%</span>
              </div>
              <p className="text-sm text-navy-400">
                {m.opportunity.site.name} · {m.opportunity.site.country}
              </p>
              <div className="mt-2 grid grid-cols-4 gap-1 text-xs text-navy-500">
                <span>Géo {(m.geographyScore * 100).toFixed(0)}</span>
                <span>Tech {(m.technologyScore * 100).toFixed(0)}</span>
                <span>Taille {(m.sizeScore * 100).toFixed(0)}</span>
                <span>Banca {(m.bankabilityAlignment * 100).toFixed(0)}</span>
              </div>
              {m.explanation && <p className="mt-2 text-sm text-navy-600">{m.explanation}</p>}
              <div className="mt-3">
                <Badge tone={m.status === "valide_admin" ? "vert" : m.status === "ecarte" ? "muted" : "navy"}>
                  {m.status === "valide_admin" ? "Validé par l'opérateur" : m.status === "ecarte" ? "Écarté" : "Proposé"}
                </Badge>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
