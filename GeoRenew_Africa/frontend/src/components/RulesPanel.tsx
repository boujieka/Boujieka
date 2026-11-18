import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import type { Dataset, Meta, Rule } from "../types";
import { ErrorBox, Field, Select } from "./ui";

interface Props { projectId: number; meta: Meta; rules: Rule[]; datasets: Dataset[] }

export function RulesPanel({ projectId, meta, rules, datasets }: Props) {
  const qc = useQueryClient();
  const [jtype, setJtype] = useState("aucun_buffer");
  const refresh = () => {
    qc.invalidateQueries({ queryKey: ["rules", projectId] });
    qc.invalidateQueries({ queryKey: ["project", projectId] });
  };
  const create = useMutation({ mutationFn: (body: unknown) => api.post<Rule>(`/projects/${projectId}/constraints`, body), onSuccess: refresh });
  const patch = useMutation({ mutationFn: ({ id, body }: { id: number; body: unknown }) => api.patch<Rule>(`/constraints/${id}`, body), onSuccess: refresh });
  const remove = useMutation({ mutationFn: (id: number) => api.del(`/constraints/${id}`), onSuccess: refresh });
  const usable = datasets.filter((d) => d.category !== "limite_site");

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    create.mutate({
      name: f.get("name"), dataset_id: Number(f.get("dataset_id")), kind: f.get("kind"),
      buffer_m: Number(String(f.get("buffer_m") || "0").replace(",", ".")),
      justification_type: f.get("justification_type"), justification: f.get("justification") ?? "",
    }, { onSuccess: () => (e.target as HTMLFormElement).reset() });
  };

  return (
    <div className="panel">
      <p className="small muted">{t("rules.help")}</p>
      <ul className="list" data-testid="rule-list">
        {rules.length === 0 && <li className="muted">{t("rules.empty")}</li>}
        {rules.map((r) => (
          <li key={r.id} className={r.active ? "" : "inactive"}>
            <label className="check">
              <input type="checkbox" checked={r.active} onChange={() => patch.mutate({ id: r.id, body: { active: !r.active } })} aria-label={t("rules.active")} />
              <strong>{r.name}</strong> <span className={`badge kind-${r.kind}`}>{label(r.kind)}</span>
            </label>
            <div className="small">{r.dataset_name} · buffer {r.buffer_m} m · {label(r.justification_type)}</div>
            {r.justification && <div className="small muted">{r.justification}</div>}
            <button className="danger small" onClick={() => confirm(`Supprimer « ${r.name} » ?`) && remove.mutate(r.id)}>{t("common.delete")}</button>
          </li>
        ))}
      </ul>
      <ErrorBox error={patch.error} />

      <h3>{t("rules.new")}</h3>
      {usable.length === 0 ? <p className="muted small">Importez d'abord un jeu de données (onglet Données).</p> : (
        <form onSubmit={onSubmit} className="form">
          <Field label={t("project.name")}><input name="name" required /></Field>
          <Field label={t("rules.dataset")}>
            <select name="dataset_id" required>{usable.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}</select>
          </Field>
          <Field label={t("rules.kind")}><Select name="kind" values={meta.rule_kinds} /></Field>
          <Field label={t("rules.buffer")}><input name="buffer_m" inputMode="decimal" defaultValue="0" /></Field>
          <Field label={t("rules.justification_type")}><Select name="justification_type" values={meta.justification_types} value={jtype} onChange={setJtype} /></Field>
          <Field label={t("rules.justification")}><textarea name="justification" rows={2} required={jtype !== "aucun_buffer"} /></Field>
          <button type="submit" disabled={create.isPending}>{t("rules.new")}</button>
        </form>
      )}
      <ErrorBox error={create.error} />
    </div>
  );
}
