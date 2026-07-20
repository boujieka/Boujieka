import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, EmptyState, LinkButton } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { createOpportunityAction } from "@/lib/actions/opportunities";

export default async function NewOpportunityPage({
  searchParams,
}: {
  searchParams: { siteId?: string };
}) {
  const session = await requireRole("offtaker");
  const sites = await prisma.site.findMany({
    where: { organizationId: session.organizationId, deletedAt: null },
    orderBy: { name: "asc" },
  });

  if (sites.length === 0) {
    return (
      <div className="mx-auto max-w-2xl">
        <EmptyState title="Aucun site disponible">
          <LinkButton href="/sites/new" variant="primary">Créer d'abord un site</LinkButton>
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Nouvelle opportunité</h1>
        <p className="text-sm text-navy-500">
          Le taux de couverture cible impose la fiabilité recherchée par la simulation.
        </p>
      </div>
      <Card>
        <ActionForm action={createOpportunityAction} className="space-y-4">
          <div>
            <label className="label">Site *</label>
            <select name="siteId" className="select" defaultValue={searchParams.siteId ?? ""} required>
              <option value="" disabled>— Choisir un site —</option>
              {sites.map((s) => (
                <option key={s.id} value={s.id}>{s.name} · {s.country}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Intitulé *</label>
            <input name="title" required className="input" placeholder="Solarisation + secours — Usine…" />
          </div>
          <div>
            <label className="label">Taux de couverture cible *</label>
            <input
              name="targetReliabilityRate"
              type="number"
              step="0.01"
              min="0.1"
              max="1"
              defaultValue="0.95"
              required
              className="input"
            />
            <p className="mt-1 text-xs text-navy-400">
              Ex. 0.95 = 95 % de la charge annuelle servie par le renouvelable.
            </p>
          </div>
          <SubmitButton variant="gold">Créer l'opportunité</SubmitButton>
        </ActionForm>
      </Card>
    </div>
  );
}
