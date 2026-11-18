import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ErrorBox, FictionalBadge, Field, Select } from "../components/ui";
import { label, t } from "../i18n";
import { api } from "../lib/api";
import type { Meta, Project } from "../types";

export function Portfolio({ meta }: { meta: Meta }) {
  const qc = useQueryClient();
  const nav = useNavigate();
  const projects = useQuery({ queryKey: ["projects"], queryFn: () => api.get<Project[]>("/projects") });
  const create = useMutation({
    mutationFn: (body: unknown) => api.post<Project>("/projects", body),
    onSuccess: (p) => { qc.invalidateQueries({ queryKey: ["projects"] }); nav(`/projets/${p.id}`); },
  });
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    create.mutate({
      name: f.get("name"), country_iso3: f.get("country_iso3"), technology: f.get("technology"),
      description: f.get("description") ?? "", is_fictional: f.get("is_fictional") === "on",
    });
  };

  return (
    <div className="page">
      <h2>{t("portfolio.title")}</h2>
      <div className="grid">
        <section>
          {projects.isLoading && <p>{t("common.loading")}</p>}
          <ErrorBox error={projects.error} />
          {projects.data?.length === 0 && <p className="muted">{t("portfolio.empty")}</p>}
          <ul className="cards" data-testid="project-list">
            {projects.data?.map((p) => (
              <li key={p.id} className="card">
                <Link to={`/projets/${p.id}`}><strong>{p.name}</strong></Link> {p.is_fictional && <FictionalBadge />}
                <div className="small">{p.country_iso3} · {label(p.technology)}</div>
                <div className="small muted">
                  {p.site_count} {t("project.sites")} · {p.dataset_count} {t("project.datasets")} · {p.rule_count} {t("project.rules")}
                </div>
              </li>
            ))}
          </ul>
        </section>
        <section className="card">
          <h3>{t("portfolio.new")}</h3>
          <form className="form" onSubmit={onSubmit}>
            <Field label={t("project.name")}><input name="name" required /></Field>
            <Field label={t("project.country")}><input name="country_iso3" required pattern="[A-Za-z]{3}" placeholder="ZAF" maxLength={3} /></Field>
            <Field label={t("project.technology")}><Select name="technology" values={meta.technologies} /></Field>
            <Field label={t("project.description")}><textarea name="description" rows={2} /></Field>
            <label className="check"><input type="checkbox" name="is_fictional" /> {t("project.fictional")}</label>
            <button type="submit" disabled={create.isPending}>{t("project.create")}</button>
          </form>
          <ErrorBox error={create.error} />
        </section>
      </div>
    </div>
  );
}
