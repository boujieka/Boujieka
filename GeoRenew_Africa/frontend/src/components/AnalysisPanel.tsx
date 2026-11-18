import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import { formatHa, formatNumber, shortHash } from "../lib/format";
import type { AnalysisRun, AnalysisSummary, AreaMetric, Dataset, IntervalMetric, Meta, Site, ValueMetric } from "../types";
import { ErrorBox, Field, NatureBadge, Select, Warnings } from "./ui";

interface Props {
  site: Site | null;
  meta: Meta;
  datasets: Dataset[];
  runId: number | null;
  setRunId: (id: number | null) => void;
}

const AREA_KEYS = [
  "surface_brute", "surface_recul", "surface_exclusions_strictes", "surface_nette",
  "somme_exclusions_par_regle", "chevauchement_non_double_compte", "surface_contraintes_indicatives",
];

function MetricRow({ k, m }: { k: string; m: AreaMetric | ValueMetric | IntervalMetric }) {
  let value: string;
  if ("valeur_m2" in m) value = formatHa(m.valeur_m2);
  else if ("bas_m2" in m) value = m.bas_m2 === null ? "—" : `${formatHa(m.bas_m2)} – ${formatHa(m.haut_m2)}`;
  else value = formatNumber(m.valeur, 2, m.unite);
  return (
    <tr data-testid={`metric-${k}`} className={k === "surface_nette" ? "key" : ""}>
      <th scope="row">{label(k)}</th>
      <td className="num">{value}</td>
      <td><NatureBadge nature={m.nature} /></td>
      <td className="small muted">{m.methode}</td>
    </tr>
  );
}

function StatusForm({ site, meta, datasets }: { site: Site; meta: Meta; datasets: Dataset[] }) {
  const qc = useQueryClient();
  const save = useMutation({
    mutationFn: (body: unknown) => api.patch<Site>(`/sites/${site.id}`, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["sites", site.project_id] }),
  });
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const num = (k: string) => (f.get(k) ? Number(f.get(k)) : null);
    save.mutate({
      land_status: f.get("land_status"), land_evidence_dataset_id: num("land_evidence_dataset_id"),
      grid_status: f.get("grid_status"), grid_evidence_dataset_id: num("grid_evidence_dataset_id"),
    });
  };
  const opts = (cats: string[]) => [<option key="" value="">— aucune —</option>,
    ...datasets.filter((d) => cats.includes(d.category)).map((d) => <option key={d.id} value={d.id}>{d.name}</option>)];
  return (
    <form className="form" onSubmit={onSubmit} key={site.id}>
      <Field label={t("status.land")}><Select name="land_status" values={meta.land_statuses} defaultValue={site.land_status} /></Field>
      <Field label={t("status.evidence")} hint="Cadastre officiel ou relevé qualifié, non fictif.">
        <select name="land_evidence_dataset_id" defaultValue={site.land_evidence_dataset_id ?? ""}>{opts(["cadastre_officiel", "releve_qualifie"])}</select>
      </Field>
      <Field label={t("status.grid")}><Select name="grid_status" values={meta.grid_statuses} defaultValue={site.grid_status} /></Field>
      <Field label={t("status.evidence")} hint="Étude réseau ou accord du gestionnaire, non fictif.">
        <select name="grid_evidence_dataset_id" defaultValue={site.grid_evidence_dataset_id ?? ""}>{opts(["etude_reseau", "accord_gestionnaire"])}</select>
      </Field>
      <button type="submit" disabled={save.isPending}>{t("status.save")}</button>
      <ErrorBox error={save.error} />
      {save.isSuccess && <p className="ok small">Statuts enregistrés.</p>}
    </form>
  );
}

export function AnalysisPanel({ site, meta, datasets, runId, setRunId }: Props) {
  const qc = useQueryClient();
  const [reused, setReused] = useState(false);
  const history = useQuery({
    queryKey: ["analyses", site?.id],
    queryFn: () => api.get<AnalysisSummary[]>(`/sites/${site!.id}/analyses`),
    enabled: !!site,
  });
  const run = useQuery({
    queryKey: ["analysis", runId],
    queryFn: () => api.get<AnalysisRun>(`/analyses/${runId}`),
    enabled: runId !== null,
  });
  const launch = useMutation({
    mutationFn: (body: unknown) => api.post<AnalysisRun>(`/sites/${site!.id}/analyses`, body),
    onSuccess: (r) => {
      setReused(!!r.reused);
      qc.setQueryData(["analysis", r.id], r);
      qc.invalidateQueries({ queryKey: ["analyses", site!.id] });
      setRunId(r.id);
    },
  });

  if (!site) return <div className="panel muted">{t("analysis.select_site")}</div>;

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const n = (k: string) => Number(String(f.get(k) || "0").replace(",", "."));
    const density = String(f.get("density") || "").trim();
    launch.mutate({
      setback_m: n("setback_m"), setback_justification: f.get("setback_justification") ?? "",
      density_mwp_dc_per_ha: density ? Number(density.replace(",", ".")) : null,
      density_justification: f.get("density_justification") ?? "", force: f.get("force") === "on",
    });
  };

  const r = run.data?.site_id === site.id ? run.data : null;
  const res = r?.results;
  return (
    <div className="panel">
      <h3>{site.name}</h3>
      <form className="form" onSubmit={onSubmit}>
        <div className="row">
          <Field label={t("analysis.setback")}><input name="setback_m" inputMode="decimal" defaultValue="0" /></Field>
          <Field label={t("analysis.setback_justification")}><input name="setback_justification" placeholder="ex. hypothèse utilisateur" /></Field>
        </div>
        <div className="row">
          <Field label={t("analysis.density")}><input name="density" inputMode="decimal" /></Field>
          <Field label={t("analysis.density_justification")}><input name="density_justification" /></Field>
        </div>
        <label className="check"><input type="checkbox" name="force" /> {t("analysis.force")}</label>
        <button type="submit" disabled={launch.isPending} data-testid="run-analysis">{t("analysis.run")}</button>
      </form>
      <ErrorBox error={launch.error} />
      {reused && r && <p className="info small">{t("analysis.reused")}</p>}

      {res && r && (
        <section data-testid="results">
          <h3>{t("analysis.results")} — analyse n° {r.id}</h3>
          {res.donnees_fictives && <div className="fictional-inline">DONNÉES FICTIVES</div>}
          <p className="small"><strong>{res.niveau_etude}</strong> — {res.mention}</p>
          <p className="small muted">
            Surfaces mesurées en {res.scr_calcul} ({res.scr_calcul_nom}) · moteur {r.engine_version} · logiciel {r.software_version} ·
            empreinte des entrées <code title={r.input_hash}>{shortHash(r.input_hash)}</code>
          </p>
          <table className="metrics">
            <tbody>
              {AREA_KEYS.map((k) => res.indicateurs[k] && <MetricRow key={k} k={k} m={res.indicateurs[k]} />)}
              <MetricRow k="intervalle_surface_nette" m={res.indicateurs.intervalle_surface_nette} />
              <MetricRow k="puissance_indicative_mwp_dc" m={res.indicateurs.puissance_indicative_mwp_dc} />
            </tbody>
          </table>
          <div className="row">
            <a className="button" href={`/api/v1/analyses/${r.id}/geojson`} download>{t("analysis.export_geojson")}</a>
            <a className="button" href={`/api/v1/analyses/${r.id}/csv`} download>{t("analysis.export_csv")}</a>
          </div>

          <h4>{t("analysis.statuses")}</h4>
          <ul className="small">
            <li>{res.statuts.foncier_libelle}</li>
            <li>{res.statuts.raccordement_libelle}</li>
            <li>{res.statuts.capacite_reseau}</li>
          </ul>

          <h4>{t("analysis.per_rule")}</h4>
          <table className="metrics small">
            <thead><tr><th>Règle</th><th>Type</th><th>Buffer</th><th>Surface</th><th>Entités</th></tr></thead>
            <tbody>
              {res.par_regle.map((p) => (
                <tr key={p.regle_id}>
                  <td>{p.nom}</td><td>{label(p.type)}</td><td className="num">{p.buffer_m} m</td>
                  <td className="num">{formatHa(p.surface_dans_zone_amenageable_m2 ?? p.surface_dans_surface_nette_m2)}</td>
                  <td className="num">{p.entites_retenues}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h4>{t("analysis.checks")}</h4>
          <ul className="small">
            {res.controles.map((c) => <li key={c.nom} className={c.ok ? "ok" : "error"}>{c.ok ? "✓" : "✗"} {c.nom} — {c.detail}</li>)}
          </ul>
          {res.avertissements.length > 0 && <><h4>{t("analysis.warnings")}</h4><Warnings items={res.avertissements} /></>}
        </section>
      )}

      <h4>{t("analysis.statuses")} (modifier)</h4>
      <StatusForm site={site} meta={meta} datasets={datasets} />

      <h4>{t("analysis.history")}</h4>
      <ul className="list small">
        {(history.data ?? []).map((h) => (
          <li key={h.id} className={h.id === runId ? "selected" : ""}>
            <button className="link" onClick={() => { setReused(false); setRunId(h.id); }}>
              n° {h.id} — {formatNumber(h.surface_nette_ha, 2, "ha")} nets · recul {h.recul_m} m · {h.regles} règle(s)
            </button>
            <span className="muted"> {h.created_at?.slice(0, 19).replace("T", " ")} · {shortHash(h.input_hash, 8)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
