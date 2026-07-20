import Link from "next/link";
import { notFound } from "next/navigation";
import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, SectionTitle, Stat, LinkButton, EmptyState, Badge } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { regenerateProfileAction } from "@/lib/actions/sites";
import { DailyProfileChart } from "@/components/charts";
import { fmtInt, fmtNum, CRITICALITY_LABELS, STAGE_LABELS } from "@/lib/format";
import { sectorTemplates } from "@/lib/load-profiles/sectoral";

export default async function SiteDetailPage({ params }: { params: { id: string } }) {
  const session = await requireRole("offtaker");
  const site = await prisma.site.findFirst({
    where: { id: params.id, organizationId: session.organizationId, deletedAt: null },
    include: { loadProfile: true, opportunities: { where: { deletedAt: null } } },
  });
  if (!site) notFound();

  const load = (site.loadProfile?.hourlyKw as number[] | undefined) ?? [];
  const flatYield = load.map((_, h) => {
    const hod = h % 24;
    const x = (hod - 6) / 12;
    return x > 0 && x < 1 ? Math.sin(Math.PI * x) * 0.6 : 0;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{site.name}</h1>
          <p className="text-sm text-navy-500">
            {site.country} · {site.latitude.toFixed(3)}, {site.longitude.toFixed(3)}
          </p>
        </div>
        <LinkButton href={`/opportunities/new?siteId=${site.id}`} variant="gold">
          + Opportunité sur ce site
        </LinkButton>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Conso. annuelle" value={site.annualConsumptionKwh ? `${fmtInt(site.annualConsumptionKwh / 1000)} MWh` : "—"} />
        <Stat label="Pointe" value={site.peakDemandKw ? `${fmtInt(site.peakDemandKw)} kW` : "—"} />
        <Stat label="Criticité" value={CRITICALITY_LABELS[site.loadCriticality]} accent="gold" />
        <Stat label="Coupures réseau" value={site.gridOutageHoursYear ? `${fmtInt(site.gridOutageHoursYear)} h/an` : "—"} accent="navy" />
      </div>

      <Card>
        <SectionTitle>Courbe de charge (journée moyenne)</SectionTitle>
        {site.loadProfile ? (
          <>
            <DailyProfileChart load={load} yieldPerKwp={flatYield} />
            <p className="mt-2 text-xs text-navy-400">
              Source : {site.loadProfile.source} · {load.length} pas horaires · productible illustratif.
            </p>
          </>
        ) : (
          <EmptyState title="Aucune courbe de charge">
            Générez un profil-type sectoriel ci-dessous (nécessite la consommation annuelle).
          </EmptyState>
        )}

        {site.annualConsumptionKwh ? (
          <div className="mt-4 border-t border-navy-50 pt-4">
            <ActionForm action={regenerateProfileAction} className="flex flex-wrap items-end gap-3">
              <input type="hidden" name="siteId" value={site.id} />
              <div>
                <label className="label">Profil-type sectoriel</label>
                <select name="sectorTemplate" className="select" defaultValue={site.loadProfile?.sectorTemplate ?? "industrie_continue"}>
                  {sectorTemplates.map((t) => (
                    <option key={t.key} value={t.key}>{t.label}</option>
                  ))}
                </select>
              </div>
              <SubmitButton variant="ghost">Régénérer la courbe</SubmitButton>
            </ActionForm>
          </div>
        ) : null}
      </Card>

      <Card>
        <SectionTitle>Détails</SectionTitle>
        <dl className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-3">
          <Detail label="Surface disponible" value={site.availableAreaM2 ? `${fmtInt(site.availableAreaM2)} m²` : "—"} />
          <Detail label="Tarif réseau" value={site.currentGridTariff ? `${fmtNum(site.currentGridTariff, 3)} /kWh` : "—"} />
          <Detail label="Coût coupure/h" value={site.outageCostPerHour ? fmtInt(site.outageCostPerHour) : "—"} />
        </dl>
      </Card>

      <Card>
        <SectionTitle>Opportunités du site</SectionTitle>
        {site.opportunities.length === 0 ? (
          <EmptyState title="Aucune opportunité" />
        ) : (
          <ul className="divide-y divide-navy-50">
            {site.opportunities.map((o) => (
              <li key={o.id} className="flex items-center justify-between py-2">
                <Link href={`/opportunities/${o.id}`} className="font-medium hover:text-gold-600">{o.title}</Link>
                <Badge tone="muted">{STAGE_LABELS[o.stage]}</Badge>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs text-navy-400">{label}</dt>
      <dd className="font-medium text-navy-800">{value}</dd>
    </div>
  );
}
