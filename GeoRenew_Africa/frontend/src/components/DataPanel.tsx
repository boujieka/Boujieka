import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import { shortHash } from "../lib/format";
import type { Dataset, Meta } from "../types";
import { ErrorBox, FictionalBadge, Field, Select, Warnings } from "./ui";

interface Props {
  projectId: number;
  meta: Meta;
  datasets: Dataset[];
  visible: Set<number>;
  toggle: (id: number) => void;
}

export function DataPanel({ projectId, meta, datasets, visible, toggle }: Props) {
  const qc = useQueryClient();
  const [warnings, setWarnings] = useState<string[]>([]);
  const imp = useMutation({
    mutationFn: (form: FormData) => api.upload<Dataset>(`/projects/${projectId}/datasets`, form),
    onSuccess: (d) => {
      setWarnings(d.latest_version?.warnings ?? []);
      qc.invalidateQueries({ queryKey: ["datasets", projectId] });
      qc.invalidateQueries({ queryKey: ["project", projectId] });
      toggle(d.id);
    },
  });
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    imp.mutate(new FormData(e.currentTarget));
  };

  return (
    <div className="panel">
      <ul className="list">
        {datasets.length === 0 && <li className="muted">{t("data.empty")}</li>}
        {datasets.map((d) => {
          const v = d.latest_version;
          return (
            <li key={d.id}>
              <label className="check">
                <input type="checkbox" checked={visible.has(d.id)} onChange={() => toggle(d.id)} aria-label={t("data.show")} />
                <strong>{d.name}</strong> {d.is_synthetic && <FictionalBadge />}
              </label>
              <dl className="prov">
                <dt>Catégorie</dt><dd>{label(d.category)}</dd>
                <dt>Nature</dt><dd>{label(d.nature)}</dd>
                <dt>Source</dt><dd>{d.source_name || <em>non renseignée</em>}</dd>
                <dt>Licence</dt><dd>{d.licence || <em>non renseignée</em>}</dd>
                <dt>Date réf.</dt><dd>{d.reference_date ?? <em>inconnue</em>}</dd>
                <dt>Précision</dt><dd>{d.horizontal_accuracy_m !== null ? `${d.horizontal_accuracy_m} m` : <em>inconnue</em>}</dd>
                {v && <>
                  <dt>Version</dt><dd>v{v.version_no} · {v.feature_count} entité(s) · {v.geometry_types.join(", ")}</dd>
                  <dt>SCR source</dt><dd>{v.source_crs} ({label(v.crs_origin)})</dd>
                  <dt>Fichier</dt><dd>{v.original_filename} · SHA-256 <code title={v.sha256}>{shortHash(v.sha256)}</code></dd>
                </>}
              </dl>
              <Warnings items={v?.warnings} />
            </li>
          );
        })}
      </ul>

      <h3>{t("data.import")}</h3>
      <form onSubmit={onSubmit} className="form">
        <Field label={t("data.file")} hint={`${meta.upload_extensions.join(", ")} — ${meta.max_upload_mb} Mo max.`}>
          <input type="file" name="file" required accept={meta.upload_extensions.join(",")} />
        </Field>
        <Field label={t("project.name")}><input name="name" required /></Field>
        <Field label={t("data.category")}><Select name="category" values={meta.dataset_categories.filter((c) => c !== "limite_site")} /></Field>
        <Field label={t("data.nature")}><Select name="nature" values={meta.data_natures} defaultValue="inconnue" /></Field>
        <Field label={t("data.source")}><input name="source_name" /></Field>
        <Field label={t("data.source_url")}><input name="source_url" type="url" /></Field>
        <Field label={t("data.licence")}><input name="licence" /></Field>
        <Field label={t("data.producer")}><input name="producer" /></Field>
        <Field label={t("data.reference_date")}><input name="reference_date" type="date" /></Field>
        <Field label={t("data.accuracy")}><input name="horizontal_accuracy_m" inputMode="decimal" /></Field>
        <Field label={t("data.declared_crs")}><input name="declared_crs" placeholder="EPSG:…" /></Field>
        <details>
          <summary>Options avancées</summary>
          <Field label={t("data.layer")}><input name="layer" /></Field>
          <Field label={t("data.x_column")}><input name="x_column" /></Field>
          <Field label={t("data.y_column")}><input name="y_column" /></Field>
          <label className="check"><input type="checkbox" name="repair" value="true" /> {t("data.repair")}</label>
        </details>
        <label className="check"><input type="checkbox" name="is_synthetic" value="true" /> {t("data.synthetic")}</label>
        <button type="submit" disabled={imp.isPending}>{imp.isPending ? t("common.loading") : t("data.import")}</button>
      </form>
      <ErrorBox error={imp.error} />
      <Warnings items={warnings} />
    </div>
  );
}
