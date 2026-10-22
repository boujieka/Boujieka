import { useMemo, useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { disbursementRate, maxLevel } from "../lib/agg";
import { fmtAmount, fmtDate, fmtPct } from "../lib/format";
import { go, href, type Route } from "../lib/router";
import { FilterBar } from "../components/FilterBar";
import { DataTable, type Column } from "../components/DataTable";
import { ProjectMap, type Marker } from "../components/Maps";
import { Badge, Card, Empty, LevelBadge, PageHead } from "../components/ui";
import type { AgreementRow, ProjectRow } from "../lib/types";

const LEVEL_COLOR = { critical_attention: "#B42318", high_attention: "#D9A323", watch: "#4C78A8", information: "#087F5B" } as const;

export function precisionOf(p: string | null): Marker["precision"] {
  if (!p) return "unknown";
  if (/exactness 1\b|exact/i.test(p)) return "exact";
  return "approx";
}

export function Projects({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = route.filters;
  const sel = useSelection(f);
  const view = (["table", "cards", "map"] as const).find((v) => v === route.qs.get("view")) ?? "table";
  const [compare, setCompare] = useState<string[]>([]);
  const [showCompare, setShowCompare] = useState(false);
  const agrByProject = useMemo(() => {
    const m = new Map<number, AgreementRow[]>();
    for (const a of s.agreements) m.set(a.project, [...(m.get(a.project) ?? []), a]);
    return m;
  }, [s]);
  const rate = (p: ProjectRow) => disbursementRate(agrByProject.get(p.id) ?? []).value;
  const toggle = (ref: string) => setCompare((c) => (c.includes(ref) ? c.filter((x) => x !== ref) : c.length >= 4 ? c : [...c, ref]));

  const columns: Column<ProjectRow>[] = [
    { key: "cmp", label: "✓", width: "2rem", value: () => null, render: (p) => (
      <input type="checkbox" aria-label={`${t("projects.compare")} ${p.ref}`} checked={compare.includes(p.ref)} onChange={() => toggle(p.ref)} />) },
    { key: "ref", label: t("col.ref"), value: (p) => p.ref, render: (p) => <a href={href(`/project/${p.ref}`, f)} className="mono">{p.ref}</a> },
    { key: "title", label: t("col.title"), value: (p) => p.title, render: (p) => <a href={href(`/project/${p.ref}`, f)}>{p.title}</a> },
    { key: "sector", label: t("col.sector"), value: (p) => names.sector(p.sector) },
    { key: "status", label: t("col.status"), value: (p) => t(`status.${p.status}`) },
    { key: "partners", label: t("col.partners"), value: (p) => p.partners.map((c) => names.partner(c)).join(", ") },
    { key: "approval", label: t("col.approval"), value: (p) => p.approval, render: (p) => fmtDate(p.approval, locale) },
    { key: "end", label: t("col.end"), value: (p) => p.current_end, render: (p) => fmtDate(p.current_end, locale) },
    { key: "usd", label: t("col.committed"), align: "right", value: (p) => sel.usd.get(p.id) ?? null, render: (p) => fmtAmount(sel.usd.get(p.id) ?? null, locale, "USD") },
    { key: "rate", label: t("col.rate"), align: "right", value: (p) => rate(p), render: (p) => fmtPct(rate(p), locale) },
    { key: "alerts", label: t("col.alerts"), value: (p) => { const l = maxLevel(p); return l ? ["critical_attention", "high_attention", "watch", "information"].indexOf(l) : null; },
      render: (p) => { const l = maxLevel(p); return l ? <LevelBadge level={l} /> : null; } },
    { key: "dq", label: t("col.dq"), align: "right", value: (p) => p.dq?.completeness ?? null, render: (p) => fmtPct(p.dq?.completeness ?? null, locale) },
  ];
  const provenance = [s.meta.scope, `snapshot ${s.meta.generated_at}`, `filters: ${window.location.hash}`,
    "committed_usd: sum of agreement commitments converted at the approval-year rate; blank = not convertible"];

  const markers = useMemo(() => {
    const out: Marker[] = [];
    for (const p of sel.projects) {
      const l = maxLevel(p);
      for (const loc of p.locations) out.push({ ref: p.ref, title: p.title, lat: Number(loc.lat), lon: Number(loc.lon), precision: precisionOf(loc.precision),
        color: l ? LEVEL_COLOR[l] : "#082B50" });
    }
    return out;
  }, [sel.projects]);
  const noCoords = sel.projects.filter((p) => !p.locations.length).length;
  const cmp = compare.map((r) => s.projects.find((p) => p.ref === r)!).filter(Boolean);

  return (
    <div>
      <PageHead title={t("projects.title")} subtitle={t("projects.results", { n: sel.projects.length })}>
        <div className="seg" role="tablist">
          {(["table", "cards", "map"] as const).map((v) => (
            <a key={v} role="tab" aria-selected={view === v} className={`btn xs ${view === v ? "" : "ghost"}`} href={href("/projects", f, { view: v })} data-testid={`view-${v}`}>{t(`projects.${v}`)}</a>
          ))}
          <button className="btn xs gold" disabled={compare.length < 2} onClick={() => setShowCompare(true)} title={t("projects.compareHint")}>{t("projects.compareN", { n: compare.length })}</button>
        </div>
      </PageHead>
      <FilterBar route={route} undated={sel.undatedExcluded} />
      {!sel.projects.length ? <Empty /> : view === "table" ? (
        <Card>
          <DataTable rows={sel.projects} columns={columns} rowKey={(p) => p.id} exportName="ap2i_projects" provenance={provenance} caption={t("common.projects")}
            initialSort={{ key: "ref", dir: 1 }} testId="projects-table" />
        </Card>
      ) : view === "cards" ? (
        <div className="cards">
          {sel.projects.slice(0, 120).map((p) => {
            const l = maxLevel(p);
            return (
              <a key={p.id} className="pcard" href={href(`/project/${p.ref}`, f)}>
                <span className="mono small">{p.ref}</span>
                <b>{p.title}</b>
                <span className="small muted">{names.sector(p.sector)} · {t(`status.${p.status}`)} · {p.partners.map((c) => names.partner(c)).join(", ") || "—"}</span>
                <span className="pcard-f"><span>{fmtAmount(sel.usd.get(p.id) ?? null, locale, "USD")}</span>{l && <LevelBadge level={l} />}</span>
              </a>
            );
          })}
          {sel.projects.length > 120 && <p className="muted">{sel.projects.length - 120} + … — {t("projects.table")}</p>}
        </div>
      ) : (
        <Card note={<>{t("projects.mapNote")} {noCoords ? t("projects.noCoords", { n: noCoords }) : ""}</>}>
          <ProjectMap markers={markers} onOpen={(ref) => go(`/project/${ref}`, f)} />
          <div className="legend">
            {Object.entries(LEVEL_COLOR).map(([k, c]) => <span key={k}><i style={{ background: c }} />{t(`level.${k}`)}</span>)}
            <span><i style={{ background: "#082B50" }} />{t("level.none")}</span>
            <span className="muted">○ {t("precision.approx")} / ● {t("precision.exact")}</span>
          </div>
        </Card>
      )}
      {showCompare && cmp.length >= 2 && (
        <div className="modal" role="dialog" aria-modal="true" aria-label={t("projects.compare")}>
          <div className="modal-b">
            <header className="card-h"><h3>{t("projects.compare")}</h3><button className="btn xs ghost" onClick={() => setShowCompare(false)}>{t("common.close")}</button></header>
            <div className="table-wrap">
              <table className="cmp">
                <tbody>
                  {[
                    [t("col.title"), (p: ProjectRow) => p.title],
                    [t("col.sector"), (p: ProjectRow) => names.sector(p.sector)],
                    [t("col.status"), (p: ProjectRow) => t(`status.${p.status}`)],
                    [t("col.partners"), (p: ProjectRow) => p.partners.map((c) => names.partner(c)).join(", ")],
                    [t("col.approval"), (p: ProjectRow) => fmtDate(p.approval, locale)],
                    [t("col.end"), (p: ProjectRow) => fmtDate(p.current_end, locale)],
                    [t("col.committed"), (p: ProjectRow) => fmtAmount(sel.usd.get(p.id) ?? null, locale, "USD")],
                    [t("col.rate"), (p: ProjectRow) => fmtPct(rate(p), locale)],
                    [t("col.alerts"), (p: ProjectRow) => Object.entries(p.alerts).map(([k, v]) => `${t(`level.${k}`)}: ${v}`).join(" · ") || t("level.none")],
                    [t("profile.physical"), (p: ProjectRow) => (p.physical_progress === null ? t("common.na") : `${p.physical_progress} %`)],
                    [t("profile.rating"), (p: ProjectRow) => p.latest_rating?.rating ?? t("common.na")],
                    [t("col.dq"), (p: ProjectRow) => fmtPct(p.dq?.completeness ?? null, locale)],
                  ].map(([label, fn]) => (
                    <tr key={label as string}><th>{label as string}</th>{cmp.map((p) => <td key={p.id}>{(fn as (p: ProjectRow) => string)(p)}</td>)}</tr>
                  ))}
                  <tr><th>{t("col.ref")}</th>{cmp.map((p) => <td key={p.id}><a href={href(`/project/${p.ref}`, f)} className="mono">{p.ref}</a></td>)}</tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
      {compare.length > 0 && !showCompare && <div className="cmp-bar"><Badge tone="gold">{compare.length}/4</Badge> {t("projects.compareHint")}</div>}
    </div>
  );
}
