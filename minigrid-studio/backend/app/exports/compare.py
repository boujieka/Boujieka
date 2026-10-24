"""Side-by-side comparison of 2 to 4 runs (pure: used by the API and by the in-browser demo).

Each item: {"run": {"id", "status", "result"}, "project": str, "version": {"scenario", "version",
"status", "assumptions"}}. The first item is the base for the differences."""
from __future__ import annotations

from .labels import kpi_label, labels, series_label

COMPARE_SERIES = ["revenue", "ebitda", "cfads", "debt_service", "dscr", "senior_debt_balance", "project_cash_flow",
                  "distributions"]


def _flat(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _flat(v, f"{prefix}{k}.")
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from _flat(v, f"{prefix}{i}.")
    else:
        yield prefix[:-1], d


def compare_runs(items: list[dict], lang: str) -> dict:
    lab = labels(lang)
    results = [it["run"]["result"] for it in items]
    runs = [{"run_id": it["run"]["id"], "project": it["project"], "scenario": it["version"]["scenario"],
             "version": it["version"]["version"], "status": it["run"]["status"], "version_status": it["version"]["status"],
             "options": res.get("options", []), "solver": res.get("solver", {}).get("method")}
            for it, res in zip(items, results)]
    keys: list[str] = []
    for res in results:
        keys += [k for k in res.get("kpis", {}) if k not in keys]
    kpis = {}
    for k in keys:
        vals = [res["kpis"].get(k, {}).get("value") for res in results]
        first = next((res["kpis"][k] for res in results if k in res["kpis"]), {})
        base = vals[0]
        kpis[k] = {"label": kpi_label(k, first.get("label", k), lang), "unit": first.get("unit", ""),
                   "source": first.get("source", ""), "values": vals,
                   "deltas": [None if v is None or base is None else v - base for v in vals]}
    # series are aligned on calendar years (runs may start in different years)
    years = sorted({int(y) for res in results for y in res["series"]["year"]["values"]})
    series = {}
    for k in COMPARE_SERIES:
        if all(k in res.get("series", {}) for res in results):
            s0 = results[0]["series"][k]
            aligned = []
            for res in results:
                by_year = dict(zip((int(y) for y in res["series"]["year"]["values"]), res["series"][k]["values"]))
                aligned.append([by_year.get(y) for y in years])
            series[k] = {"label": series_label(k, s0["label"], lang), "unit": s0["unit"], "values": aligned}
    flats = [dict(_flat(it["version"]["assumptions"])) for it in items]
    paths: list[str] = []
    for f in flats:
        paths += [k for k in f if k not in paths]
    diffs = []
    for path in paths:
        vals = [f.get(path) for f in flats]
        if any(v != vals[0] for v in vals[1:]):
            parts = path.split(".")
            key = f"lots.<i>.{parts[2]}" if parts[0] == "lots" and len(parts) > 2 else ".".join(parts[:2])
            diffs.append({"path": path, "label": lab["fields"].get(key, path), "values": vals})
    return {"runs": runs, "years": years, "kpis": kpis, "series": series, "assumption_diffs": diffs[:500]}
