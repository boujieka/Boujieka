import Link from "next/link";
import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, SectionTitle, EmptyState, Badge } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { updateMatchStatusAction } from "@/lib/actions/interactions";

export default async function AdminMatchesPage() {
  await requireRole("admin");

  const matches = await prisma.match.findMany({
    orderBy: [{ status: "asc" }, { compatibilityScore: "desc" }],
    include: {
      opportunity: { include: { site: true, bankability: true } },
      developerProfile: { include: { organization: true } },
    },
  });

  const pending = matches.filter((m) => m.status === "propose");
  const decided = matches.filter((m) => m.status !== "propose");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Validation des mises en relation</h1>
        <p className="text-sm text-navy-500">
          Modèle intermédié — l'opérateur valide ou écarte chaque appariement proposé.
        </p>
      </div>

      <Card>
        <SectionTitle>À valider ({pending.length})</SectionTitle>
        {pending.length === 0 ? (
          <EmptyState title="Aucun appariement en attente" />
        ) : (
          <ul className="space-y-3">
            {pending.map((m) => (
              <li key={m.id} className="rounded-lg border border-navy-100 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <Link href={`/opportunities/${m.opportunityId}`} className="font-medium hover:text-gold-600">
                      {m.opportunity.title}
                    </Link>
                    <span className="text-navy-400"> ↔ {m.developerProfile.organization.name}</span>
                    <div className="text-xs text-navy-400">
                      {m.opportunity.site.country} · score {(m.compatibilityScore * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <ActionForm action={updateMatchStatusAction}>
                      <input type="hidden" name="matchId" value={m.id} />
                      <input type="hidden" name="status" value="valide_admin" />
                      <SubmitButton variant="vert">Valider</SubmitButton>
                    </ActionForm>
                    <ActionForm action={updateMatchStatusAction}>
                      <input type="hidden" name="matchId" value={m.id} />
                      <input type="hidden" name="status" value="ecarte" />
                      <SubmitButton variant="ghost">Écarter</SubmitButton>
                    </ActionForm>
                  </div>
                </div>
                {m.explanation && <p className="mt-2 text-sm text-navy-600">{m.explanation}</p>}
              </li>
            ))}
          </ul>
        )}
      </Card>

      {decided.length > 0 && (
        <Card>
          <SectionTitle>Décidés</SectionTitle>
          <ul className="divide-y divide-navy-50">
            {decided.map((m) => (
              <li key={m.id} className="flex items-center justify-between py-2 text-sm">
                <Link href={`/opportunities/${m.opportunityId}`} className="hover:text-gold-600">
                  {m.opportunity.title} ↔ {m.developerProfile.organization.name}
                </Link>
                <Badge tone={m.status === "valide_admin" ? "vert" : "muted"}>
                  {m.status === "valide_admin" ? "Validé" : "Écarté"}
                </Badge>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
