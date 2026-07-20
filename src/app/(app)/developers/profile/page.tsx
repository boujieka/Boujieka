import { requireRole } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { upsertDeveloperProfileAction } from "@/lib/actions/developers";
import { TECH_LABELS } from "@/lib/format";

const TECHS = ["solaire", "stockage", "hybride", "groupe_backup"] as const;

export default async function DeveloperProfilePage() {
  const session = await requireRole("developer");
  const profile = await prisma.developerProfile.findUnique({
    where: { organizationId: session.organizationId },
    include: { zones: true, technologies: true },
  });

  const selectedTechs = new Set(profile?.technologies.map((t) => t.technology) ?? []);
  const countries = profile?.zones.map((z) => z.country).join(", ") ?? "";

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Profil développeur</h1>
        <p className="text-sm text-navy-500">
          Zones, technologies, taille de projet et track record — déterminants du matching.
        </p>
      </div>

      <Card>
        <ActionForm action={upsertDeveloperProfileAction} className="space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="label">Taille de projet min (kW) *</label>
              <input name="minProjectSizeKw" type="number" step="any" required defaultValue={profile?.minProjectSizeKw ?? 200} className="input" />
            </div>
            <div>
              <label className="label">Taille de projet max (kW) *</label>
              <input name="maxProjectSizeKw" type="number" step="any" required defaultValue={profile?.maxProjectSizeKw ?? 5000} className="input" />
            </div>
            <div>
              <label className="label">Capacité de financement *</label>
              <select name="financingCapacity" className="select" defaultValue={profile?.financingCapacity ?? "mixte"}>
                <option value="equity">Fonds propres</option>
                <option value="dette">Dette</option>
                <option value="mixte">Mixte</option>
                <option value="aucune">Aucune</option>
              </select>
            </div>
            <div>
              <label className="label">Track record (MW cumulés)</label>
              <input name="trackRecordMw" type="number" step="any" defaultValue={profile?.trackRecordMw ?? 0} className="input" />
            </div>
            <div>
              <label className="label">Projets livrés</label>
              <input name="projectsCompleted" type="number" defaultValue={profile?.projectsCompleted ?? 0} className="input" />
            </div>
          </div>

          <div>
            <label className="label">Pays couverts (codes ISO, séparés par des virgules) *</label>
            <input name="countries" defaultValue={countries} required className="input uppercase" placeholder="CM, GA, CI, SN" />
          </div>

          <div>
            <span className="label">Technologies maîtrisées *</span>
            <div className="flex flex-wrap gap-3">
              {TECHS.map((t) => (
                <label key={t} className="flex items-center gap-2 rounded-lg border border-navy-200 px-3 py-2 text-sm">
                  <input type="checkbox" name="technologies" value={t} defaultChecked={selectedTechs.has(t)} />
                  {TECH_LABELS[t]}
                </label>
              ))}
            </div>
            <p className="mt-1 text-xs text-navy-400">
              Solaire + stockage confèrent la capacité hybride, exigée par les solutions à fiabilité cible.
            </p>
          </div>

          <SubmitButton variant="gold">Enregistrer le profil</SubmitButton>
        </ActionForm>
      </Card>
    </div>
  );
}
