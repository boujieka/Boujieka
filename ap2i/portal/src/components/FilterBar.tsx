import { useEffect, useMemo, useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { LEVELS, type Filters } from "../lib/filters";
import { go, type Route } from "../lib/router";

const STATUSES = ["active", "completed", "closed", "pipeline", "cancelled", "dropped", "suspended", "unknown"];
const SAVED_KEY = "ap2i.portal.savedViews";

interface SavedView { name: string; hash: string }

function readSaved(): SavedView[] {
  try {
    const v = JSON.parse(localStorage.getItem(SAVED_KEY) ?? "[]");
    return Array.isArray(v) ? v.filter((x) => typeof x?.name === "string" && typeof x?.hash === "string").slice(0, 30) : [];
  } catch {
    return [];
  }
}

export function FilterBar({ route, undated, hide = [] }: { route: Route; undated?: number; hide?: (keyof Filters)[] }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const f = route.filters;
  const [more, setMore] = useState(false);
  const [open, setOpen] = useState(false); // mobile: filters collapsed behind a button
  const [q, setQ] = useState(f.q ?? "");
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState<SavedView[]>(readSaved);
  const path = "/" + route.path.join("/");
  useEffect(() => setQ(f.q ?? ""), [f.q]);

  const set = (patch: Partial<Filters>) => {
    const extra: Record<string, string> = {};
    for (const k of ["view", "dim", "col", "measure", "metric", "sort", "drill"]) {
      const v = route.qs.get(k);
      if (v) extra[k] = v;
    }
    go(path, { ...f, ...patch }, extra);
  };
  // debounce search typing
  useEffect(() => {
    if ((f.q ?? "") === q) return;
    const id = setTimeout(() => set({ q: q || undefined }), 300);
    return () => clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q]);

  const countries = useMemo(() => s.ref.countries.filter((c) => c.documented_projects > 0), [s]);
  const regions = useMemo(() => [...new Set(s.projects.filter((p) => !f.country || p.country === f.country).map((p) => p.region).filter(Boolean))].sort() as string[], [s, f.country]);
  const years = useMemo(() => {
    const ys: number[] = [];
    for (let y = s.meta.years[1]; y >= 2000; y--) ys.push(y);
    return ys;
  }, [s]);
  const active = Object.keys(f).filter((k) => !hide.includes(k as keyof Filters)).length;
  const partnerOpts = useMemo(() => s.ref.partners.filter((p) => s.projects.some((x) => x.partners.includes(p.code))), [s]);
  const instrumentOpts = useMemo(() => s.ref.instruments.filter((i) => s.agreements.some((a) => a.instrument === i.code)), [s]);
  const chips: { k: keyof Filters; label: string }[] = [];
  if (f.y0 || f.y1) chips.push({ k: "y0", label: `${f.y0 ?? "…"}–${f.y1 ?? "…"}` });
  if (f.sector) chips.push({ k: "sector", label: names.sector(f.sector === "UNCLASSIFIED" ? null : f.sector) });
  if (f.partner) chips.push({ k: "partner", label: names.partner(f.partner) });
  if (f.status) chips.push({ k: "status", label: f.status.map((x) => t(`status.${x}`)).join(", ") });
  if (f.alert) chips.push({ k: "alert", label: f.alert === "any" ? t("filters.any") : f.alert === "attention" ? t("kpi.attention") : t(`level.${f.alert}`) });
  if (f.q) chips.push({ k: "q", label: `« ${f.q} »` });
  if (f.instrument) chips.push({ k: "instrument", label: names.instrument(f.instrument) });
  if (f.region) chips.push({ k: "region", label: f.region });
  if (f.minusd) chips.push({ k: "minusd", label: `≥ ${new Intl.NumberFormat(locale).format(f.minusd)} USD` });
  if (f.dq) chips.push({ k: "dq", label: `≥ ${f.dq * 100} %` });

  const share = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt(t("filters.share"), window.location.href);
    }
  };
  const save = () => {
    const name = window.prompt(t("filters.saveName"))?.trim().slice(0, 60);
    if (!name) return;
    const next = [{ name, hash: window.location.hash }, ...saved.filter((v) => v.name !== name)].slice(0, 30);
    setSaved(next);
    try {
      localStorage.setItem(SAVED_KEY, JSON.stringify(next));
    } catch { /* storage unavailable: the view stays shareable by link */ }
  };

  return (
    <form className={`filterbar ${open ? "open" : ""}`} role="search" aria-label={t("filters.title")} onSubmit={(e) => e.preventDefault()}>
      <div className="fb-mobile">
        <button type="button" className="btn xs" onClick={() => setOpen((o) => !o)} aria-expanded={open} data-testid="f-toggle">
          {t("common.filters")}{active ? ` (${active})` : ""}
        </button>
        {chips.filter((c) => !hide.includes(c.k)).map((c) => (
          <button key={c.k} type="button" className="chip" onClick={() => set(c.k === "y0" ? { y0: undefined, y1: undefined } : { [c.k]: undefined })}
            aria-label={`${t("filters.reset")} : ${c.label}`}>{c.label} ×</button>
        ))}
      </div>
      <div className="fb-row">
        {!hide.includes("country") && <label>
          <span>{t("filters.country")}</span>
          <select value={f.country ?? ""} onChange={(e) => set({ country: e.target.value || undefined, region: undefined })} data-testid="f-country">
            <option value="">{t("filters.all")}</option>
            {countries.map((c) => <option key={c.iso3} value={c.iso3}>{names.country(c.iso3)}</option>)}
          </select>
        </label>}
        <label className="yr">
          <span>{t("filters.years")}</span>
          <span className="yr-pair">
            <select value={f.y0 ?? ""} onChange={(e) => set({ y0: e.target.value ? Number(e.target.value) : undefined })} aria-label={`${t("filters.years")} min`} data-testid="f-y0">
              <option value="">…</option>
              {years.map((y) => <option key={y} value={y}>{y}</option>)}
            </select>
            <select value={f.y1 ?? ""} onChange={(e) => set({ y1: e.target.value ? Number(e.target.value) : undefined })} aria-label={`${t("filters.years")} max`} data-testid="f-y1">
              <option value="">…</option>
              {years.map((y) => <option key={y} value={y}>{y}</option>)}
            </select>
          </span>
        </label>
        <label>
          <span>{t("filters.sector")}</span>
          <select value={f.sector ?? ""} onChange={(e) => set({ sector: e.target.value || undefined })} data-testid="f-sector">
            <option value="">{t("filters.all")}</option>
            {s.ref.sectors.map((x) => <option key={x.code} value={x.code}>{names.sector(x.code)}</option>)}
            <option value="UNCLASSIFIED">{names.sector(null)}</option>
          </select>
        </label>
        <label>
          <span>{t("filters.partner")}</span>
          <select value={f.partner ?? ""} onChange={(e) => set({ partner: e.target.value || undefined })} data-testid="f-partner">
            <option value="">{t("filters.all")}</option>
            {partnerOpts.map((p) => <option key={p.code} value={p.code}>{p.short_name}</option>)}
          </select>
        </label>
        <label>
          <span>{t("filters.status")}</span>
          <select value={f.status?.[0] ?? ""} onChange={(e) => set({ status: e.target.value ? [e.target.value] : undefined })} data-testid="f-status">
            <option value="">{t("filters.all")}</option>
            {STATUSES.map((x) => <option key={x} value={x}>{t(`status.${x}`)}</option>)}
          </select>
        </label>
          <label>
          <span>{t("filters.alert")}</span>
          <select value={f.alert ?? ""} onChange={(e) => set({ alert: (e.target.value || undefined) as Filters["alert"] })} data-testid="f-alert">
            <option value="">{t("filters.all")}</option>
            <option value="any">{t("filters.any")}</option>
            {LEVELS.map((l) => <option key={l} value={l}>{t(`level.${l}`)}</option>)}
          </select>
        </label>
        <label className="grow">
          <span>{t("filters.search")}</span>
          <input type="search" value={q} maxLength={100} onChange={(e) => setQ(e.target.value)} data-testid="f-q" />
        </label>
      </div>
      {more && (
        <div className="fb-row">
          <label>
            <span>{t("filters.instrument")}</span>
            <select value={f.instrument ?? ""} onChange={(e) => set({ instrument: e.target.value || undefined })}>
              <option value="">{t("filters.all")}</option>
              {instrumentOpts.map((i) => <option key={i.code} value={i.code}>{names.instrument(i.code)}</option>)}
            </select>
          </label>
          <label>
            <span>{t("filters.region")}</span>
            <select value={f.region ?? ""} onChange={(e) => set({ region: e.target.value || undefined })}>
              <option value="">{t("filters.all")}</option>
              {regions.map((r) => <option key={r} value={r}>{r}</option>)}
            </select>
          </label>

          <label>
            <span>{t("filters.minusd")}</span>
            <select value={f.minusd ?? ""} onChange={(e) => set({ minusd: e.target.value ? Number(e.target.value) : undefined })}>
              <option value="">{t("filters.all")}</option>
              {[1e6, 1e7, 5e7, 1e8, 5e8].map((v) => <option key={v} value={v}>≥ {new Intl.NumberFormat(locale).format(v)} USD</option>)}
            </select>
          </label>
          <label>
            <span>{t("filters.dq")}</span>
            <select value={f.dq ?? ""} onChange={(e) => set({ dq: e.target.value ? Number(e.target.value) : undefined })}>
              <option value="">{t("filters.all")}</option>
              {[0.25, 0.5, 0.75].map((v) => <option key={v} value={v}>≥ {v * 100} %</option>)}
            </select>
          </label>
        </div>
      )}
      <div className="fb-actions">
        <button type="button" className="btn xs ghost" onClick={() => setMore((m) => !m)} aria-expanded={more}>{more ? t("filters.less") : t("filters.more")}</button>
        {active > 0 && <button type="button" className="btn xs ghost" onClick={() => go(path, {})} data-testid="f-reset">{t("filters.reset")} ({active})</button>}
        <button type="button" className="btn xs ghost" onClick={share}>{copied ? t("filters.copied") : t("filters.share")}</button>
        <button type="button" className="btn xs ghost" onClick={save}>{t("filters.save")}</button>
        {saved.length > 0 && (
          <select aria-label={t("filters.saved")} value="" onChange={(e) => { if (e.target.value) window.location.hash = e.target.value; }}>
            <option value="">{t("filters.saved")}</option>
            {saved.map((v) => <option key={v.name} value={v.hash}>{v.name}</option>)}
          </select>
        )}
        <span className="muted small">{t("filters.yearsNote")}</span>
        {undated ? <span className="muted small">{t("filters.undated", { n: undated })}</span> : null}
      </div>
    </form>
  );
}
