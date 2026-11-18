import { useQueries, useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import type { FeatureCollection } from "geojson";
import { AnalysisPanel } from "../components/AnalysisPanel";
import { DataPanel } from "../components/DataPanel";
import { MapView, type Overlay } from "../components/MapView";
import { RulesPanel } from "../components/RulesPanel";
import { SitesPanel } from "../components/SitesPanel";
import { ErrorBox } from "../components/ui";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import type { Dataset, Meta, Project, Rule, Site } from "../types";

type Tab = "sites" | "data" | "rules" | "analysis";

const DATA_COLORS: Record<string, string> = {
  exclusion: "#c92a2a", contrainte: "#e67700", reseau_electrique: "#5f3dc4",
  cadastre_officiel: "#495057", releve_qualifie: "#495057", limite_site: "#1864ab",
};
const RESULT_STYLE: Record<string, { color: string; opacity: number; dashed?: boolean }> = {
  bande_recul: { color: "#f08c00", opacity: 0.45 },
  exclusion_stricte: { color: "#e03131", opacity: 0.55 },
  contrainte_indicative: { color: "#fab005", opacity: 0.45, dashed: true },
  surface_nette: { color: "#2f9e44", opacity: 0.5 },
};

export function ProjectPage({ meta }: { meta: Meta }) {
  const projectId = Number(useParams().id);
  const [tab, setTab] = useState<Tab>("sites");
  const [siteId, setSiteId] = useState<number | null>(null);
  const [runId, setRunId] = useState<number | null>(null);
  const [visible, setVisible] = useState<Set<number>>(new Set());
  const [drawing, setDrawing] = useState(false);
  const [drawCoords, setDrawCoords] = useState<[number, number][]>([]);

  const project = useQuery({ queryKey: ["project", projectId], queryFn: () => api.get<Project>(`/projects/${projectId}`) });
  const sites = useQuery({ queryKey: ["sites", projectId], queryFn: () => api.get<Site[]>(`/projects/${projectId}/sites`) });
  const datasets = useQuery({ queryKey: ["datasets", projectId], queryFn: () => api.get<Dataset[]>(`/projects/${projectId}/datasets`) });
  const rules = useQuery({ queryKey: ["rules", projectId], queryFn: () => api.get<Rule[]>(`/projects/${projectId}/constraints`) });

  // Par défaut, afficher les couches utilisées par des règles
  useEffect(() => {
    if (rules.data && visible.size === 0) setVisible(new Set(rules.data.map((r) => r.dataset_id)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rules.data]);

  const visibleDatasets = (datasets.data ?? []).filter((d) => visible.has(d.id) && d.category !== "limite_site");
  const layerQueries = useQueries({
    queries: visibleDatasets.map((d) => ({
      queryKey: ["dataset-geojson", d.id, d.latest_version?.id],
      queryFn: () => api.get<FeatureCollection>(`/datasets/${d.id}/geojson`),
    })),
  });
  const runGeo = useQuery({
    queryKey: ["analysis-geojson", runId],
    queryFn: () => api.get<FeatureCollection>(`/analyses/${runId}/geojson`),
    enabled: runId !== null,
  });

  const site = sites.data?.find((s) => s.id === siteId) ?? null;
  useEffect(() => { setRunId(null); }, [siteId]);

  const overlays = useMemo<Overlay[]>(() => {
    const out: Overlay[] = [];
    visibleDatasets.forEach((d, i) => {
      const data = layerQueries[i]?.data;
      if (data) out.push({ id: `ds-${d.id}`, label: `${d.name}${d.is_synthetic ? " (fictif)" : ""}`,
        color: DATA_COLORS[d.category] ?? "#868e96", data, fillOpacity: 0.2 });
    });
    if (runGeo.data) {
      for (const kind of ["bande_recul", "exclusion_stricte", "contrainte_indicative", "surface_nette"]) {
        const feats = runGeo.data.features.filter((f) => f.properties?.couche === kind);
        if (feats.length === 0) continue;
        const st = RESULT_STYLE[kind];
        out.push({ id: `run-${kind}`, label: `${label(kind)} (analyse n° ${runId})`, color: st.color,
          fillOpacity: st.opacity, dashed: st.dashed, data: { type: "FeatureCollection", features: feats } });
      }
    }
    if (sites.data) {
      out.push({
        id: "sites", label: "Limites de sites", color: "#1864ab", fillOpacity: 0.05,
        data: { type: "FeatureCollection", features: sites.data.map((s) => ({
          type: "Feature", geometry: s.geometry, properties: { id: s.id, nom: s.name } })) },
      });
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sites.data, runGeo.data, runId, layerQueries.map((q) => q.dataUpdatedAt).join(","), visible]);

  const fitTo = useMemo<[number, number, number, number] | null>(() => {
    if (site) return site.bbox;
    const all = sites.data ?? [];
    if (all.length === 0) return null;
    return [Math.min(...all.map((s) => s.bbox[0])), Math.min(...all.map((s) => s.bbox[1])),
      Math.max(...all.map((s) => s.bbox[2])), Math.max(...all.map((s) => s.bbox[3]))];
  }, [site, sites.data]);

  const toggle = (id: number) => setVisible((v) => { const n = new Set(v); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const p = project.data;

  return (
    <div className="project">
      {p?.is_fictional && <div className="fictional-banner" data-testid="fictional-banner">{t("fictional.banner")}</div>}
      <ErrorBox error={project.error} />
      <div className="project-body">
        <aside className="sidebar">
          <h2>{p?.name ?? t("common.loading")}</h2>
          {p && <div className="small muted">{p.country_iso3} · {label(p.technology)}</div>}
          <nav className="tabs" role="tablist">
            {(["sites", "data", "rules", "analysis"] as Tab[]).map((k) => (
              <button key={k} role="tab" aria-selected={tab === k} className={tab === k ? "active" : ""} onClick={() => setTab(k)}>
                {t(`tab.${k}` as const)}
              </button>
            ))}
          </nav>
          {tab === "sites" && (
            <SitesPanel projectId={projectId} sites={sites.data ?? []} selectedId={siteId}
              onSelect={(id) => { setSiteId(id); }} drawing={drawing} drawCoords={drawCoords}
              setDrawing={setDrawing} setDrawCoords={setDrawCoords} />
          )}
          {tab === "data" && <DataPanel projectId={projectId} meta={meta} datasets={datasets.data ?? []} visible={visible} toggle={toggle} />}
          {tab === "rules" && <RulesPanel projectId={projectId} meta={meta} rules={rules.data ?? []} datasets={datasets.data ?? []} />}
          {tab === "analysis" && <AnalysisPanel site={site} meta={meta} datasets={datasets.data ?? []} runId={runId} setRunId={setRunId} />}
        </aside>
        <MapView overlays={overlays} fitTo={fitTo} drawing={drawing} drawCoords={drawCoords} onDrawChange={setDrawCoords} />
      </div>
    </div>
  );
}
