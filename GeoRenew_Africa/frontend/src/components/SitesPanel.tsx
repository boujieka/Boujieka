import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import type { Site } from "../types";
import { ErrorBox, Field, Warnings } from "./ui";

interface Props {
  projectId: number;
  sites: Site[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  drawing: boolean;
  drawCoords: [number, number][];
  setDrawing: (v: boolean) => void;
  setDrawCoords: (c: [number, number][]) => void;
}

export function SitesPanel({ projectId, sites, selectedId, onSelect, drawing, drawCoords, setDrawing, setDrawCoords }: Props) {
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const [warnings, setWarnings] = useState<string[]>([]);
  const refresh = () => {
    qc.invalidateQueries({ queryKey: ["sites", projectId] });
    qc.invalidateQueries({ queryKey: ["datasets", projectId] });
    qc.invalidateQueries({ queryKey: ["project", projectId] });
  };

  const create = useMutation({
    mutationFn: () => api.post<Site>(`/projects/${projectId}/sites`, {
      name: name.trim() || `Site ${sites.length + 1}`,
      geometry: { type: "Polygon", coordinates: [[...drawCoords, drawCoords[0]]] },
    }),
    onSuccess: (s) => { setDrawing(false); setDrawCoords([]); setName(""); setWarnings(s.warnings ?? []); refresh(); onSelect(s.id); },
  });

  const importSites = useMutation({
    mutationFn: (form: FormData) => api.upload<{ sites: Site[]; warnings: string[] }>(`/projects/${projectId}/sites/import`, form),
    onSuccess: (r) => { setWarnings(r.warnings); refresh(); if (r.sites[0]) onSelect(r.sites[0].id); },
  });

  const remove = useMutation({ mutationFn: (id: number) => api.del(`/sites/${id}`), onSuccess: refresh });

  const onImport = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    importSites.mutate(new FormData(e.currentTarget));
  };

  return (
    <div className="panel">
      <ul className="list" data-testid="site-list">
        {sites.length === 0 && <li className="muted">{t("sites.empty")}</li>}
        {sites.map((s) => (
          <li key={s.id} className={s.id === selectedId ? "selected" : ""}>
            <button className="link" onClick={() => onSelect(s.id)}>{s.name}</button>
            <div className="small muted">{t("sites.source")} : {s.boundary_source || "—"}</div>
            <div className="small">
              Foncier : {label(s.land_status).toLowerCase()} · Raccordement : {label(s.grid_status).toLowerCase()}
            </div>
            <button className="danger small" onClick={() => confirm(`Supprimer « ${s.name} » ?`) && remove.mutate(s.id)}>
              {t("common.delete")}
            </button>
          </li>
        ))}
      </ul>

      <h3>{t("sites.draw")}</h3>
      {!drawing ? (
        <button onClick={() => { setDrawCoords([]); setDrawing(true); }}>{t("sites.draw")}</button>
      ) : (
        <div className="draw-box">
          <p className="small">{t("sites.draw.help")} ({drawCoords.length} sommet(s))</p>
          <Field label={t("project.name")}><input value={name} onChange={(e) => setName(e.target.value)} /></Field>
          <div className="row">
            <button disabled={drawCoords.length < 3 || create.isPending} onClick={() => create.mutate()}>{t("sites.draw.finish")}</button>
            <button className="secondary" onClick={() => { setDrawing(false); setDrawCoords([]); }}>{t("sites.draw.cancel")}</button>
          </div>
        </div>
      )}
      <ErrorBox error={create.error} />

      <h3>{t("sites.import")}</h3>
      <form onSubmit={onImport} className="form">
        <Field label={t("data.file")}><input type="file" name="file" required accept=".geojson,.json,.zip,.gpkg,.kml,.kmz" /></Field>
        <Field label={t("project.name")}><input name="name" required defaultValue="Limites de site" /></Field>
        <Field label={t("sites.name_field")}><input name="name_field" /></Field>
        <Field label={t("data.source")}><input name="source_name" /></Field>
        <Field label={t("data.licence")}><input name="licence" /></Field>
        <Field label={t("data.accuracy")}><input name="horizontal_accuracy_m" inputMode="decimal" /></Field>
        <Field label={t("data.declared_crs")}><input name="declared_crs" placeholder="EPSG:…" /></Field>
        <label className="check"><input type="checkbox" name="is_synthetic" value="true" /> {t("data.synthetic")}</label>
        <button type="submit" disabled={importSites.isPending}>{t("sites.import")}</button>
      </form>
      <ErrorBox error={importSites.error} />
      <Warnings items={warnings} />
    </div>
  );
}
