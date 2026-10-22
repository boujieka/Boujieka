import { useMemo } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSelection, useSnap } from "../lib/context";
import { commitmentsOf, disbursedByCurrency, maxLevel } from "../lib/agg";
import { currencyLines, fmtAmount, fmtDate, fmtNum, fmtPct } from "../lib/format";
import { go, href, type Route } from "../lib/router";
import { AfricaMap } from "../components/Maps";
import { FilterBar } from "../components/FilterBar";
import { DataTable } from "../components/DataTable";
import { Card, PageHead } from "../components/ui";

const METRICS = ["projects", "commitments", "active", "completed", "attention", "coverage"] as const;
type Metric = (typeof METRICS)[number];

export function Africa({ route }: { route: Route }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = { ...route.filters, country: undefined };
  const sel = useSelection(f);
  const metric = (METRICS as readonly string[]).includes(route.qs.get("metric") ?? "") ? (route.qs.get("metric") as Metric) : "projects";

  const rows = useMemo(() => s.ref.countries.map((c) => {
    const ps = sel.projects.filter((p) => p.country === c.iso3);
    const has = c.documented_projects > 0;
    const ids = new Set(ps.map((p) => p.id));
    const money = commitmentsOf(sel.agreements.filter((a) => ids.has(a.project)));
    const dq = ps.filter((p) => p.dq).map((p) => p.dq!.completeness);
    const lastSync = s.africa.countries.find((x) => x.iso3 === c.iso3)?.last_update ?? null;
    return {
      iso3: c.iso3, name: names.country(c.iso3), region: c.region, has,
      projects: has ? ps.length : null,
      commitments: has ? money.usd : null,
      disbursed: has ? disbursedByCurrency(sel.agreements.filter((a) => ids.has(a.project))) : null,
      active: has ? ps.filter((p) => p.status === "active").length : null,
      completed: has ? ps.filter((p) => p.status === "completed" || p.status === "closed").length : null,
      attention: has ? ps.filter((p) => { const l = maxLevel(p); return l === "critical_attention" || l === "high_attention"; }).length : null,
      coverage: has && dq.length ? dq.reduce((a, b) => a + b, 0) / dq.length : null,
      lastSync: has ? lastSync : null,
    };
  }), [s, sel, names]);

  const values = useMemo(() => {
    const m = new Map<string, number>();
    for (const r of rows) {
      const v = r[metric];
      if (r.has && v !== null && v !== undefined) m.set(r.iso3, v as number);
    }
    return m;
  }, [rows, metric]);
  const fmt = (v: number) => (metric === "commitments" ? fmtAmount(v, locale, "USD") : metric === "coverage" ? fmtPct(v, locale) : fmtNum(v, locale));
  const open = (iso3: string) => go(`/country/${iso3}`, { ...route.filters, country: undefined });

  return (
    <div>
      <PageHead title={t("africa.title")} subtitle={t("africa.subtitle")}>
        <label className="inline">
          <span>{t("africa.metric")}</span>
          <select value={metric} onChange={(e) => go("/africa", route.filters, { metric: e.target.value })} data-testid="metric">
            {METRICS.map((m) => <option key={m} value={m}>{t(`metric.${m}`)}</option>)}
          </select>
        </label>
      </PageHead>
      <FilterBar route={route} undated={sel.undatedExcluded} />
      <div className="grid-2-1">
        <Card title={t(`metric.${metric}`)} note={t("africa.clickHint")}>
          <AfricaMap values={values} label={t(`metric.${metric}`)} format={fmt} onSelect={open} />
        </Card>
        <Card title={names.country("CMR")}>
          {(() => {
            const r = rows.find((x) => x.iso3 === "CMR")!;
            return (
              <dl className="dl">
                <div><dt>{t("kpi.projects")}</dt><dd>{fmtNum(r.projects, locale)}</dd></div>
                <div><dt>{t("kpi.commitments")}</dt><dd>{fmtAmount(r.commitments, locale, "USD")}</dd></div>
                <div><dt>{t("kpi.disbursed")}</dt><dd>{r.disbursed ? currencyLines(r.disbursed, locale) : "—"}</dd></div>
                <div><dt>{t("kpi.active")}</dt><dd>{fmtNum(r.active, locale)}</dd></div>
                <div><dt>{t("kpi.completed")}</dt><dd>{fmtNum(r.completed, locale)}</dd></div>
                <div><dt>{t("kpi.attention")}</dt><dd>{fmtNum(r.attention, locale)}</dd></div>
                <div><dt>{t("kpi.coverage")}</dt><dd>{fmtPct(r.coverage, locale)}</dd></div>
                <div><dt>{t("kpi.lastSync")}</dt><dd>{fmtDate(r.lastSync, locale)}</dd></div>
                <a className="btn sm" href={href("/country/CMR", { ...route.filters, country: undefined })} data-testid="open-cmr">{t("africa.openCountry")} →</a>
              </dl>
            );
          })()}
        </Card>
      </div>
      <Card title={t("africa.table")}>
        <DataTable rows={rows} rowKey={(r) => r.iso3} pageSize={60} exportName="ap2i_africa" provenance={[s.meta.scope, `snapshot ${s.meta.generated_at}`]}
          initialSort={{ key: "projects", dir: -1 }}
          columns={[
            { key: "name", label: t("col.country"), value: (r) => r.name, render: (r) => <a href={href(`/country/${r.iso3}`, {})}>{r.name}</a> },
            { key: "region", label: t("col.region"), value: (r) => r.region },
            { key: "projects", label: t("metric.projects"), value: (r) => r.projects, align: "right", render: (r) => r.has ? fmtNum(r.projects, locale) : <span className="na">{t("africa.noData")}</span> },
            { key: "commitments", label: t("metric.commitments"), value: (r) => r.commitments, align: "right", render: (r) => fmtAmount(r.commitments, locale, "USD") },
            { key: "disbursed", label: t("kpi.disbursed"), value: (r) => (r.disbursed ? currencyLines(r.disbursed, locale) : null) },
            { key: "active", label: t("metric.active"), value: (r) => r.active, align: "right" },
            { key: "completed", label: t("metric.completed"), value: (r) => r.completed, align: "right" },
            { key: "attention", label: t("metric.attention"), value: (r) => r.attention, align: "right" },
            { key: "coverage", label: t("metric.coverage"), value: (r) => r.coverage, align: "right", render: (r) => fmtPct(r.coverage, locale) },
            { key: "lastSync", label: t("kpi.lastSync"), value: (r) => r.lastSync, render: (r) => fmtDate(r.lastSync, locale) },
          ]} />
      </Card>
    </div>
  );
}
