import { useMemo, useState } from "react";
import type { Assumptions, FieldEntry, VersionDetail } from "../api";
import { canEdit, canReview, useApp } from "../context";
import { formatDate, formatValue } from "../i18n";
import { href, navigate } from "../router";
import { Alert, errorText, Loading, RunBadge, StatusBadge, useLoad, useMessage } from "../components/ui";

type Draft = Record<string, unknown>;   // dotted path -> new value

const LOT_FIELDS = ["name", "included", "country", "grids", "connections_per_grid", "kwp_per_grid", "people_per_connection",
  "baseline_kwh_month", "peak_kwh_month", "expansion_module_kw", "tariff", "capex_net_of_grant", "transfer_fee",
  "grant_per_connection", "battery_cost", "fixed_fee_per_grid", "fee_per_customer", "ratchet_share", "diesel_price"];
const TEXT_LOT = new Set(["name", "country"]);
const REQUIRED_LOT = new Set(["name", "included", "country", "grids", "connections_per_grid", "kwp_per_grid",
  "people_per_connection", "baseline_kwh_month", "peak_kwh_month", "expansion_module_kw"]);
const CHOICES: Record<string, string[]> = {
  "debt.sizing_method": ["Gearing", "DSCR"], "refi.sizing_method": ["Gearing", "DSCR"],
  "debt.rate_choice": ["Fixed", "Floating"], "refi.rate_choice": ["Fixed", "Floating"],
  "debt.drawdown": ["Pari Passu", "Equity first"], "tax.vat_capex": ["Recoverable", "Irrecoverable"],
  "tax.vat_opex": ["Recoverable", "Irrecoverable"], "currency.case": ["1", "2"], "demand.consumption_case": ["1", "2", "3"],
  "macro.fx_case": ["1", "2"],
};

function get(obj: Assumptions, path: string): unknown {
  return path.split(".").reduce<unknown>((o, k) => (o == null ? o : (o as Record<string, unknown>)[k]), obj);
}

/** Leaf paths of one group as the editor shows them (MoneyInput -> .value, lists -> .i). */
function leaves(a: Assumptions, f: FieldEntry): { path: string; value: unknown; suffix: string }[] {
  const v = get(a, f.path);
  if (Array.isArray(v)) return v.map((x, i) => ({ path: `${f.path}.${i}`, value: x, suffix: `[${i + 1}]` }));
  if (v && typeof v === "object" && "value" in (v as object)) {
    const m = v as { value: number; basis: string; vat: string };
    return [{ path: `${f.path}.value`, value: m.value, suffix: `(${m.basis}${m.vat !== "none" ? `, TVA ${m.vat}` : ""})` }];
  }
  return [{ path: f.path, value: v, suffix: "" }];
}

export function VersionPage({ id }: { id: string }) {
  const { api, t, lang, notify, fields, labels, roleIn, me, compareRuns, setCompareRuns } = useApp();
  const msg = useMessage();
  const [version, reloadVersion] = useLoad(() => api.version(id), [api, id]);
  const [project] = useLoad(() => (version ? api.project(version.project_id) : Promise.resolve(undefined)), [api, version?.project_id]);
  const [runs, reloadRuns] = useLoad(() => api.runs(id), [api, id]);
  const [engineOptions] = useLoad(() => api.options(), [api]);
  const [draft, setDraft] = useState<Draft>({});
  const [lots, setLots] = useState<Record<string, unknown>[] | null>(null);
  const [opts, setOpts] = useState<Record<string, boolean> | null>(null);
  const [solver, setSolver] = useState<string | null>(null);
  const [note, setNote] = useState("");
  const [group, setGroup] = useState("debt");
  const [filter, setFilter] = useState("");
  const [busy, setBusy] = useState(false);
  const [perLot, setPerLot] = useState(false);
  const [comment, setComment] = useState("");

  const groups = useMemo(() => {
    const g: Record<string, FieldEntry[]> = {};
    for (const f of fields) if (f.group !== "lots" && f.group !== "constants") (g[f.group] ??= []).push(f);
    return g;
  }, [fields]);

  if (!version || !project) return <Loading />;
  const v: VersionDetail = version;
  const role = roleIn(project.org_id);
  const editable = canEdit(role) && !project.archived;
  const currentLots: Record<string, unknown>[] = lots ?? v.assumptions.lots;
  const currentOpts = opts ?? v.options;
  const nChanges = Object.keys(draft).length + (lots ? 1 : 0) + (opts ? 1 : 0) + (solver ? 1 : 0);

  const setValue = (path: string, raw: string, original: unknown) => {
    let val: unknown = raw;
    if (typeof original === "number" || (original === null && raw !== "" && !Number.isNaN(Number(raw)))) {
      val = raw === "" ? null : Number(raw.replace(",", "."));
    }
    const next = { ...draft };
    if (val === original || (typeof val === "number" && Number.isNaN(val))) delete next[path]; else next[path] = val;
    setDraft(next);
  };

  async function save() {
    setBusy(true);
    try {
      const changes: Record<string, unknown> = { ...draft };
      if (lots) changes.lots = lots;
      const nv = await api.revise(v.id, { changes, options: opts ?? undefined, solver_method: solver ?? undefined, note });
      setDraft({}); setLots(null); setOpts(null); setSolver(null); setNote("");
      navigate("versions", nv.id);
    } catch (err) { notify(errorText(err), "error"); } finally { setBusy(false); }
  }
  async function act(fn: () => Promise<unknown>) {
    setBusy(true);
    try { await fn(); reloadVersion(); reloadRuns(); } catch (err) { notify(msg(errorText(err)), "error"); } finally { setBusy(false); }
  }
  async function calculate() {
    setBusy(true);
    try {
      const r = await api.run(v.id, perLot);
      reloadRuns();
      if (r.status === "failed") notify(msg(r.error), "error"); else navigate("runs", r.id);
    } catch (err) { notify(errorText(err), "error"); } finally { setBusy(false); }
  }

  const fieldsShown = (groups[group] ?? []).filter((f) => !filter ||
    `${f.path} ${f[lang]} ${f.cell}`.toLowerCase().includes(filter.toLowerCase()));
  const changedIn = (g: string) => Object.keys(draft).filter((p) => p.startsWith(`${g}.`)).length;
  const reviewer = canReview(role) && v.created_by !== me.id && v.submitted_by !== me.id;

  return (
    <section>
      <p className="small"><a href={href("projects", project.id)}>← {project.name}</a></p>
      <div className="row">
        <h1 className="grow">{v.scenario} · v{v.version}</h1>
        <StatusBadge status={v.status} />
      </div>
      <p className="small muted">
        {t("createdAt")} {formatDate(v.created_at, lang)} · {t("solver")} : {t(v.solver_method === "exact" ? "solver_exact" : "solver_excel_macros")}
        {v.parent_id && <> · {t("parent")} : <a href={href("versions", v.parent_id)}>{v.parent_id.slice(0, 8)}</a></>}
        {v.provenance && Object.keys(v.provenance).length > 0 && <> · {t("provenance")} : {String(v.provenance.template ?? v.provenance.source ?? "")}
          {v.provenance.filename ? ` (${String(v.provenance.filename)})` : ""}</>}
      </p>
      {v.note && <p>{v.note}</p>}
      {v.review_comment && <Alert kind={v.status === "rejected" ? "warning" : "info"}>{t("reviewComment")} : {v.review_comment}</Alert>}

      {/* workflow */}
      <div className="card no-print">
        <div className="row">
          {editable && <>
            <label className="row small"><input type="checkbox" checked={perLot} onChange={(e) => setPerLot(e.target.checked)} />{t("perLot")}</label>
            <button className="primary" onClick={calculate} disabled={busy}>{busy ? t("loading") : t("calculate")}</button>
            {(v.status === "draft" || v.status === "rejected") && <button onClick={() => act(() => api.submit(v.id))} disabled={busy}>{t("submit")}</button>}
          </>}
          {v.status === "submitted" && canReview(role) && (
            reviewer ? <>
              <input placeholder={t("reviewComment")} value={comment} onChange={(e) => setComment(e.target.value)} maxLength={5000} aria-label={t("reviewComment")} />
              <button className="primary" onClick={() => act(() => api.review(v.id, "approve", comment))} disabled={busy}>{t("approve")}</button>
              <button className="danger" onClick={() => act(() => api.review(v.id, "reject", comment))} disabled={busy}>{t("reject")}</button>
            </> : <span className="small muted">{t("fourEyes")}</span>
          )}
        </div>
        <h3>{t("runs")}</h3>
        {!runs?.length ? <p className="small muted">{t("noRuns")}</p> : (
          <table className="data">
            <thead><tr><th scope="col">{t("date")}</th><th scope="col">{t("status")}</th><th scope="col" className="num">TRI / IRR</th><th scope="col">{t("duration")}</th><th scope="col" /></tr></thead>
            <tbody>{runs.slice().reverse().map((r) => (
              <tr key={r.id}>
                <td><a href={href("runs", r.id)}>{formatDate(r.created_at, lang)}</a></td>
                <td><RunBadge status={r.status} />{r.error && <div className="small">{msg(r.error)}</div>}</td>
                <td className="num">{formatValue(r.result?.kpis?.project_irr?.value, "%", lang)}</td>
                <td className="small">{r.duration_ms} ms</td>
                <td>{r.status !== "failed" && (compareRuns.includes(r.id)
                  ? <span className="small muted">{t("inCompare")}</span>
                  : <button className="link small" disabled={compareRuns.length >= 4} onClick={() => setCompareRuns([...compareRuns, r.id])}>{t("addToCompare")}</button>)}</td>
              </tr>
            ))}</tbody>
          </table>
        )}
      </div>

      {/* assumptions */}
      <div className="row"><h2 className="grow">{t("assumptions")}</h2>
        {!editable && <span className="badge">{t("readOnly")}</span>}</div>
      {editable && <p className="small muted">{t("versionsImmutable")}</p>}
      <div className="group-grid">
        <div className="group-nav" role="tablist" aria-label={t("assumptions")}>
          {[...Object.keys(groups), "lots", "options"].map((g) => (
            <button key={g} role="tab" aria-selected={group === g} aria-current={group === g} onClick={() => setGroup(g)}>
              {g === "options" ? t("options") : labels.groups[g] ?? g}
              {g === "lots" && lots && <span className="count">●</span>}
              {g === "options" && (opts || solver) && <span className="count">●</span>}
              {changedIn(g) > 0 && <span className="count">{changedIn(g)}</span>}
            </button>
          ))}
        </div>
        <div className="card" role="tabpanel" style={{ minWidth: 0 }}>
          {group === "lots" ? (
            <LotsEditor lots={currentLots} editable={editable} onChange={setLots} original={v.assumptions.lots} />
          ) : group === "options" ? (
            <div className="stack" style={{ display: "grid", gap: 10 }}>
              <p className="small muted">{t("optionsNote")}</p>
              {(engineOptions ?? []).map((o) => (
                <label key={o.name} className="row small" style={{ alignItems: "flex-start" }}>
                  <input type="checkbox" disabled={!editable} checked={!!currentOpts[o.name]}
                    onChange={(e) => setOpts({ ...currentOpts, [o.name]: e.target.checked })} />
                  <span><strong className="mono">{o.name}</strong><br />{o.doc}</span>
                </label>
              ))}
              <label className="field">{t("solver")}
                <select disabled={!editable} value={solver ?? v.solver_method} onChange={(e) => setSolver(e.target.value === v.solver_method ? null : e.target.value)}>
                  <option value="excel_macros">{t("solver_excel_macros")}</option>
                  <option value="exact">{t("solver_exact")}</option>
                </select></label>
            </div>
          ) : (
            <>
              <input type="search" placeholder={t("search")} value={filter} onChange={(e) => setFilter(e.target.value)} aria-label={t("search")} style={{ marginBottom: 8 }} />
              <div className="scroll-x">
                <table className="data">
                  <thead><tr><th scope="col">{labels.groups[group]}</th><th scope="col" className="num">{t("value")}</th><th scope="col">{t("unit")}</th><th scope="col">{t("cell")}</th></tr></thead>
                  <tbody>{fieldsShown.flatMap((f) => leaves(v.assumptions, f).map((leaf) => {
                    const changed = leaf.path in draft;
                    const shown = changed ? draft[leaf.path] : leaf.value;
                    const choices = CHOICES[f.path];
                    return (
                      <tr key={leaf.path}>
                        <th scope="row" style={{ fontWeight: 400 }}>
                          {f[lang]} {leaf.suffix && <span className="muted small">{leaf.suffix}</span>}
                          {f.doc && <div className="small muted">{f.doc}</div>}
                        </th>
                        <td className="num">
                          {!editable || f.group === "pasted" || (leaf.value === null && /list/i.test(f.type ?? "")) ? <span>{shown === null ? "—" : String(shown)}</span>
                            : choices ? (
                              <select className={changed ? "changed" : ""} value={String(shown)} aria-label={f[lang]}
                                onChange={(e) => setValue(leaf.path, e.target.value, typeof leaf.value === "number" ? leaf.value : leaf.value)}>
                                {choices.map((c) => <option key={c} value={c}>{c}</option>)}
                              </select>
                            ) : typeof leaf.value === "number" || leaf.value === null ? (
                              <input className={`num ${changed ? "changed" : ""}`} inputMode="decimal" aria-label={f[lang]}
                                defaultValue={shown === null ? "" : String(shown)} key={`${leaf.path}-${v.id}`}
                                onBlur={(e) => setValue(leaf.path, e.target.value.trim(), leaf.value)} />
                            ) : (
                              <input className={changed ? "changed" : ""} aria-label={f[lang]} defaultValue={String(shown ?? "")} key={`${leaf.path}-${v.id}`}
                                onBlur={(e) => setValue(leaf.path, e.target.value, leaf.value)} />
                            )}
                        </td>
                        <td className="small">{labels.units[f.unit] ?? f.unit}
                          {f.unit.startsWith("%") && typeof shown === "number" && <div className="muted">= {formatValue(shown, "%", lang)}</div>}</td>
                        <td className="mono">{f.cell}</td>
                      </tr>
                    );
                  }))}</tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </div>
      {editable && nChanges > 0 && (
        <div className="card row no-print" style={{ position: "sticky", bottom: 8, zIndex: 4 }}>
          <span className="badge warn">{nChanges} {t("changes")}</span>
          <input className="grow" placeholder={t("note")} value={note} onChange={(e) => setNote(e.target.value)} maxLength={5000} aria-label={t("note")} />
          <button onClick={() => { setDraft({}); setLots(null); setOpts(null); setSolver(null); }}>{t("cancel")}</button>
          <button className="primary" onClick={save} disabled={busy}>{t("saveAsNewVersion")}</button>
        </div>
      )}
    </section>
  );
}

function LotsEditor({ lots, original, editable, onChange }: {
  lots: Record<string, unknown>[]; original: Record<string, unknown>[]; editable: boolean;
  onChange: (l: Record<string, unknown>[]) => void;
}) {
  const { t, labels } = useApp();
  const set = (i: number, k: string, raw: string) => {
    const next = lots.map((l) => ({ ...l }));
    next[i][k] = TEXT_LOT.has(k) ? raw : raw.trim() === "" ? (REQUIRED_LOT.has(k) ? 0 : null) : Number(raw.replace(",", "."));
    onChange(next);
  };
  return (
    <>
      <p className="small muted">{t("lotsNote")}</p>
      <div className="scroll-x">
        <table className="data">
          <thead><tr><th scope="col" />{lots.map((l, i) => (
            <th key={i} scope="col">{String(l.name || `Lot ${i + 1}`)}
              {editable && lots.length > 1 && <> <button className="link small" onClick={() => onChange(lots.filter((_, j) => j !== i))}>{t("removeLot")}</button></>}
            </th>))}</tr></thead>
          <tbody>{LOT_FIELDS.map((k) => (
            <tr key={k}>
              <th scope="row" style={{ fontWeight: 400 }}>{labels.fields[`lots.<i>.${k}`] ?? k}</th>
              {lots.map((l, i) => {
                const changed = original[i] === undefined || original[i][k] !== l[k];
                return (
                  <td key={i}>{editable
                    ? <input className={`${TEXT_LOT.has(k) ? "" : "num"} ${changed ? "changed" : ""}`} style={{ width: 120 }}
                        aria-label={`${labels.fields[`lots.<i>.${k}`] ?? k} — ${String(l.name ?? i + 1)}`}
                        defaultValue={l[k] === null || l[k] === undefined ? "" : String(l[k])} key={`${i}-${k}-${lots.length}`}
                        onBlur={(e) => set(i, k, e.target.value)} />
                    : <span>{l[k] === null ? "—" : String(l[k])}</span>}</td>
                );
              })}
            </tr>
          ))}</tbody>
        </table>
      </div>
      {editable && lots.length < 6 && (
        <button style={{ marginTop: 8 }} onClick={() => onChange([...lots, { ...lots[lots.length - 1], name: `Lot ${lots.length + 1}` }])}>{t("addLot")}</button>
      )}
    </>
  );
}
