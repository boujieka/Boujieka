import Link from "next/link";
import { requireUser } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Stat, Card, SectionTitle, LinkButton, EmptyState, RatingBadge, Badge } from "@/components/ui";
import { fmtInt, fmtPct, STAGE_LABELS } from "@/lib/format";

export default async function DashboardPage() {
  const session = await requireUser();

  if (session.role === "developer") return <DeveloperDashboard orgId={session.organizationId} />;
  if (session.role === "admin") return <AdminDashboard />;
  return <OfftakerDashboard orgId={session.organizationId} name={session.fullName} />;
}

async function OfftakerDashboard({ orgId }: { orgId: string; name: string }) {
  const sites = await prisma.site.count({ where: { organizationId: orgId, deletedAt: null } });
  const opportunities = await prisma.opportunity.findMany({
    where: { site: { organizationId: orgId }, deletedAt: null },
    include: { site: true, prefeasibility: true, decarbonization: true, bankability: true },
    orderBy: { createdAt: "desc" },
  });
  const co2 = opportunities.reduce((s, o) => s + (o.decarbonization?.annualCo2AvoidedTonnes ?? 0), 0);
  const withPf = opportunities.filter((o) => o.prefeasibility);
  const avgCoverage = withPf.length
    ? withPf.reduce((s, o) => s + (o.prefeasibility?.coverageRate ?? 0), 0) / withPf.length
    : 0;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Tableau de bord</h1>
          <p className="text-sm text-navy-500">Vue offtaker — décarbonisation & sécurité d'approvisionnement.</p>
        </div>
        <LinkButton href="/sites/new" variant="gold">+ Nouveau site</LinkButton>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Sites" value={fmtInt(sites)} accent="navy" />
        <Stat label="Opportunités" value={fmtInt(opportunities.length)} accent="navy" />
        <Stat label="CO₂ évité / an" value={`${fmtInt(co2)} t`} accent="vert" hint="Objectif décarbonisation" />
        <Stat label="Couverture moyenne" value={fmtPct(avgCoverage)} accent="gold" hint="Objectif sécurité d'appro." />
      </div>

      <Card>
        <SectionTitle action={<LinkButton href="/opportunities" variant="ghost">Tout voir</LinkButton>}>
          Opportunités récentes
        </SectionTitle>
        {opportunities.length === 0 ? (
          <EmptyState title="Aucune opportunité">
            Créez un site puis une opportunité pour lancer la pré-faisabilité.
          </EmptyState>
        ) : (
          <ul className="divide-y divide-navy-50">
            {opportunities.slice(0, 6).map((o) => (
              <li key={o.id} className="flex items-center justify-between py-3">
                <div>
                  <Link href={`/opportunities/${o.id}`} className="font-medium text-navy-800 hover:text-gold-600">
                    {o.title}
                  </Link>
                  <div className="text-xs text-navy-400">
                    {o.site.name} · {o.site.country}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge tone="muted">{STAGE_LABELS[o.stage]}</Badge>
                  {o.bankability && <RatingBadge rating={o.bankability.rating} />}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}

async function DeveloperDashboard({ orgId }: { orgId: string }) {
  const profile = await prisma.developerProfile.findUnique({
    where: { organizationId: orgId },
    include: { zones: true, technologies: true },
  });
  const matches = profile
    ? await prisma.match.findMany({
        where: { developerProfileId: profile.id },
        include: { opportunity: { include: { site: true } } },
        orderBy: { compatibilityScore: "desc" },
      })
    : [];
  const eois = profile
    ? await prisma.expressionOfInterest.count({ where: { developerProfileId: profile.id } })
    : 0;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Tableau de bord</h1>
          <p className="text-sm text-navy-500">Vue développeur — opportunités appariées.</p>
        </div>
        <LinkButton href="/developers/profile" variant="gold">Mon profil</LinkButton>
      </div>

      {!profile ? (
        <EmptyState title="Profil développeur incomplet">
          <LinkButton href="/developers/profile" variant="primary">Compléter mon profil</LinkButton>
        </EmptyState>
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-3">
            <Stat label="Matchs proposés" value={fmtInt(matches.length)} accent="navy" />
            <Stat label="Expressions d'intérêt" value={fmtInt(eois)} accent="gold" />
            <Stat label="Track record" value={`${fmtInt(profile.trackRecordMw)} MW`} accent="vert" />
          </div>

          <Card>
            <SectionTitle action={<LinkButton href="/matching" variant="ghost">Tout voir</LinkButton>}>
              Meilleurs appariements
            </SectionTitle>
            {matches.length === 0 ? (
              <EmptyState title="Aucun appariement pour l'instant" />
            ) : (
              <ul className="divide-y divide-navy-50">
                {matches.slice(0, 6).map((m) => (
                  <li key={m.id} className="flex items-center justify-between py-3">
                    <div>
                      <Link href={`/opportunities/${m.opportunityId}`} className="font-medium hover:text-gold-600">
                        {m.opportunity.title}
                      </Link>
                      <div className="text-xs text-navy-400">
                        {m.opportunity.site.country} · score {(m.compatibilityScore * 100).toFixed(0)}%
                      </div>
                    </div>
                    <Badge tone={m.status === "valide_admin" ? "vert" : "muted"}>
                      {m.status === "valide_admin" ? "Validé" : m.status === "ecarte" ? "Écarté" : "Proposé"}
                    </Badge>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </>
      )}
    </div>
  );
}

async function AdminDashboard() {
  const [opps, pendingMatches, factors] = await Promise.all([
    prisma.opportunity.findMany({
      where: { deletedAt: null },
      include: { decarbonization: true, prefeasibility: true },
    }),
    prisma.match.count({ where: { status: "propose" } }),
    prisma.gridEmissionFactor.count(),
  ]);
  const co2 = opps.reduce((s, o) => s + (o.decarbonization?.annualCo2AvoidedTonnes ?? 0), 0);
  const byStage = opps.reduce<Record<string, number>>((acc, o) => {
    acc[o.stage] = (acc[o.stage] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Tableau de bord — Opérateur</h1>
        <p className="text-sm text-navy-500">Aigle Group — supervision du pipeline et des mises en relation.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Opportunités" value={fmtInt(opps.length)} accent="navy" />
        <Stat label="Matchs à valider" value={fmtInt(pendingMatches)} accent="gold" />
        <Stat label="CO₂ évité / an (portefeuille)" value={`${fmtInt(co2)} t`} accent="vert" />
        <Stat label="Facteurs d'émission" value={fmtInt(factors)} accent="navy" hint="Référentiel pays" />
      </div>
      <Card>
        <SectionTitle>Pipeline par étape</SectionTitle>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-7">
          {Object.entries(STAGE_LABELS).map(([k, label]) => (
            <div key={k} className="rounded-lg bg-navy-50 p-3 text-center">
              <div className="text-2xl font-semibold text-navy-800">{fmtInt(byStage[k] ?? 0)}</div>
              <div className="text-xs text-navy-500">{label}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
