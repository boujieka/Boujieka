import Link from "next/link";
import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, SectionTitle, LinkButton, EmptyState, Badge } from "@/components/ui";
import { fmtInt, CRITICALITY_LABELS } from "@/lib/format";

export default async function SitesPage() {
  const session = await requireRole("offtaker");
  const sites = await prisma.site.findMany({
    where: { organizationId: session.organizationId, deletedAt: null },
    include: { loadProfile: true, _count: { select: { opportunities: true } } },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Sites de consommation</h1>
        <LinkButton href="/sites/new" variant="gold">+ Nouveau site</LinkButton>
      </div>

      {sites.length === 0 ? (
        <EmptyState title="Aucun site enregistré">
          Ajoutez un site physique de consommation pour démarrer une origination.
        </EmptyState>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {sites.map((s) => (
            <Card key={s.id}>
              <div className="flex items-start justify-between">
                <div>
                  <Link href={`/sites/${s.id}`} className="text-lg font-semibold hover:text-gold-600">
                    {s.name}
                  </Link>
                  <p className="text-sm text-navy-400">
                    {s.country} · {s.latitude.toFixed(2)}, {s.longitude.toFixed(2)}
                  </p>
                </div>
                <Badge tone={s.loadProfile ? "vert" : "muted"}>
                  {s.loadProfile ? "Profil de charge" : "Sans profil"}
                </Badge>
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                <div>
                  <div className="text-xs text-navy-400">Conso./an</div>
                  <div className="font-medium">{s.annualConsumptionKwh ? `${fmtInt(s.annualConsumptionKwh / 1000)} MWh` : "—"}</div>
                </div>
                <div>
                  <div className="text-xs text-navy-400">Criticité</div>
                  <div className="font-medium">{CRITICALITY_LABELS[s.loadCriticality]}</div>
                </div>
                <div>
                  <div className="text-xs text-navy-400">Opportunités</div>
                  <div className="font-medium">{s._count.opportunities}</div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
