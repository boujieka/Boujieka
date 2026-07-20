import { requireRole } from "@/lib/auth/guards";
import { Card } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { createSiteAction } from "@/lib/actions/sites";
import { sectorTemplates } from "@/lib/load-profiles/sectoral";

export default async function NewSitePage() {
  await requireRole("offtaker");

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Nouveau site</h1>
        <p className="text-sm text-navy-500">
          Renseignez la localisation (pour NASA POWER), la charge et sa criticité. Un profil-type
          sectoriel peut être généré à défaut de courbe horaire réelle.
        </p>
      </div>

      <Card>
        <ActionForm action={createSiteAction} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2">
              <label className="label">Nom du site *</label>
              <input name="name" required className="input" placeholder="Usine de Bonabéri" />
            </div>
            <div>
              <label className="label">Latitude *</label>
              <input name="latitude" type="number" step="any" required className="input" placeholder="4.07" />
            </div>
            <div>
              <label className="label">Longitude *</label>
              <input name="longitude" type="number" step="any" required className="input" placeholder="9.68" />
            </div>
            <div>
              <label className="label">Pays (ISO) *</label>
              <input name="country" required maxLength={3} className="input uppercase" placeholder="CM" />
            </div>
            <div>
              <label className="label">Surface disponible (m²)</label>
              <input name="availableAreaM2" type="number" step="any" className="input" />
            </div>
            <div>
              <label className="label">Tarif réseau actuel (devise/kWh)</label>
              <input name="currentGridTariff" type="number" step="any" className="input" placeholder="0.14" />
            </div>
            <div>
              <label className="label">Consommation annuelle (kWh)</label>
              <input name="annualConsumptionKwh" type="number" step="any" className="input" placeholder="8760000" />
            </div>
            <div>
              <label className="label">Pointe de puissance (kW)</label>
              <input name="peakDemandKw" type="number" step="any" className="input" placeholder="1400" />
            </div>
            <div>
              <label className="label">Criticité de la charge *</label>
              <select name="loadCriticality" className="select" defaultValue="moyenne">
                <option value="faible">Faible</option>
                <option value="moyenne">Moyenne</option>
                <option value="elevee">Élevée</option>
                <option value="critique">Critique</option>
              </select>
            </div>
            <div>
              <label className="label">Coût d'une heure de coupure</label>
              <input name="outageCostPerHour" type="number" step="any" className="input" placeholder="5000" />
            </div>
            <div>
              <label className="label">Heures de coupure réseau / an</label>
              <input name="gridOutageHoursYear" type="number" step="any" className="input" placeholder="400" />
            </div>
            <div className="sm:col-span-2">
              <label className="label">Profil-type sectoriel (génère la courbe de charge)</label>
              <select name="sectorTemplate" className="select" defaultValue="">
                <option value="">— Aucun (je fournirai la courbe plus tard) —</option>
                {sectorTemplates.map((t) => (
                  <option key={t.key} value={t.key}>
                    {t.label}
                  </option>
                ))}
              </select>
              <p className="mt-1 text-xs text-navy-400">
                Nécessite la consommation annuelle. La courbe de 8760 pas est calibrée sur cette consommation.
              </p>
            </div>
          </div>
          <SubmitButton variant="gold">Créer le site</SubmitButton>
        </ActionForm>
      </Card>
    </div>
  );
}
