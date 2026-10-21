"""Static charts (PNG) for PDF and Word reports, drawn from the snapshot only."""

from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.optimization.system import SCENARIOS  # noqa: E402

COLORS = {"pv_used": "#E8A33D", "discharge": "#5B8DB8", "biomass": "#5E8C4A", "grid": "#7A7A7A", "diesel": "#B5483B", "unserved": "#222222"}
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


def _png(fig) -> bytes:
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()


def _short(key: str) -> str:
    s = SCENARIOS.get(key)
    return (s.label_en.split(". ", 1)[0] if s else key)


def chart(key: str, snap: dict, lang: str = "fr") -> bytes | None:
    fr = lang == "fr"
    ccy = snap["meta"]["currency"]
    if key == "monthly_demand":
        vals = snap["demand"]["monthly_kwh"]
        fig, ax = plt.subplots(figsize=(6.5, 2.6))
        ax.bar(range(12), [v / 1e3 for v in vals], color="#0F6E56")
        ax.set_xticks(range(12), MONTHS)
        ax.set_ylabel("MWh")
        ax.set_title("Consommation mensuelle" if fr else "Monthly consumption", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        return _png(fig)
    scen = {k: v["check"] for k, v in (snap.get("scenarios") or {}).items() if v["check"].get("annual_energy")}
    if key == "energy_mix" and scen:
        fig, ax = plt.subplots(figsize=(6.5, 3.0))
        keys = list(scen)
        bottom = [0.0] * len(keys)
        pv_direct = [max(scen[k]["annual_energy"]["pv_used"] - scen[k]["annual_energy"]["charge"], 0) for k in keys]
        series = [("pv_used", pv_direct)] + [(s, [scen[k]["annual_energy"][s] for k in keys]) for s in ("discharge", "biomass", "grid", "diesel", "unserved")]
        labels = {"pv_used": "PV", "discharge": "BESS", "biomass": "Biomass", "grid": "Grid", "diesel": "Diesel", "unserved": "Unserved"}
        for name, vals in series:
            v = [x / 1e6 for x in vals]
            ax.bar(range(len(keys)), v, bottom=bottom, color=COLORS[name], label=labels[name])
            bottom = [b + x for b, x in zip(bottom, v)]
        ax.set_xticks(range(len(keys)), [_short(k) for k in keys])
        ax.set_ylabel("GWh/yr")
        ax.legend(fontsize=7, ncol=6, loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False)
        ax.set_title("Approvisionnement par source (vérification horaire)" if fr else "Supply by source (hourly verification)", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        return _png(fig)
    if key == "scenario_costs" and scen:
        keys = list(scen)
        fig, ax = plt.subplots(figsize=(6.5, 2.8))
        cap = [scen[k]["metrics"]["annual_capital_cost"] / 1e6 for k in keys]
        ops = [scen[k]["metrics"]["annual_operating_cost"] / 1e6 for k in keys]
        ax.bar(range(len(keys)), cap, color="#2F5D8A", label="Capital")
        ax.bar(range(len(keys)), ops, bottom=cap, color="#C98B2B", label="Exploitation" if fr else "Operating")
        ax.set_xticks(range(len(keys)), [_short(k) for k in keys])
        ax.set_ylabel(f"M {ccy}/yr")
        ax.legend(fontsize=7, frameon=False)
        ax.set_title("Coût annuel équivalent par scénario" if fr else "Equivalent annual cost by scenario", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        return _png(fig)
    fin = snap.get("finance")
    if key == "cash_flow" and fin:
        years = fin["years"]
        cf = [x / 1e6 for x in fin["project_cf"]]
        eq = [x / 1e6 for x in fin["equity_cf"]]
        cum = []
        s = 0.0
        for x in cf:
            s += x
            cum.append(s)
        fig, ax = plt.subplots(figsize=(6.5, 2.8))
        ax.bar([y - 0.2 for y in years], cf, width=0.4, color="#0F6E56", label="Projet" if fr else "Project")
        ax.bar([y + 0.2 for y in years], eq, width=0.4, color="#C98B2B", label="Fonds propres" if fr else "Equity")
        ax.plot(years, cum, color="#222222", lw=1.2, label="Cumul projet" if fr else "Cumulative project")
        ax.axhline(0, color="#999999", lw=0.6)
        ax.set_ylabel(f"M {ccy}")
        ax.legend(fontsize=7, frameon=False)
        ax.set_title("Flux de trésorerie (nominaux)" if fr else "Cash flows (nominal)", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        return _png(fig)
    tor = (snap.get("sensitivity") or {}).get("tornado")
    if key == "tornado" and tor:
        rows = [r for r in tor["rows"] if r["low"] is not None and r["high"] is not None][::-1]
        base = tor["base"] or 0.0
        fig, ax = plt.subplots(figsize=(6.5, 3.2))
        for i, r in enumerate(rows):
            ax.barh(i, (r["low"] - base) / 1e6, left=base / 1e6, color="#B5483B")
            ax.barh(i, (r["high"] - base) / 1e6, left=base / 1e6, color="#0F6E56")
        ax.set_yticks(range(len(rows)), [r["parameter"] for r in rows], fontsize=7)
        ax.axvline(base / 1e6, color="#222222", lw=0.8)
        ax.set_xlabel(f"{tor['metric']} (M {ccy})")
        ax.set_title("Sensibilité (bas = rouge, haut = vert)" if fr else "Sensitivity (low = red, high = green)", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        return _png(fig)
    return None
