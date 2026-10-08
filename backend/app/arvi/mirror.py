"""Mirror engine: cells, confidence and the ARVI-1/2/3 indicators (all CALCULATION).

A cell is (exporter r, partner p, HS code k, year t). X is what r declares exporting to p; M is
what p declares importing from r. Amounts stay in Decimal; ratios are rounded only for display.

Confidence (blueprint §8) is rule-based and measures how far a gap can be trusted as a gap
between two declarations of the same goods. Three of its nine components are not computed yet
and the score is rescaled from the 70 points that are: "share of the gap explained" (needs the
reconciliation engine), "independent corroboration" (needs production data) and "unit-value
coherence", which the blueprint defines against an international reference price (not collected).
Comparing the two declared unit values with each other would penalise exactly the gaps ARVI-2
is meant to show, so it is not used as a proxy.
Thresholds marked [HYPOTHÈSE] are provisional.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from app.arvi.comtrade import Flow
from app.arvi.taxonomy import HUB_PARTNERS, LANDLOCKED, PILOT, RESOURCES, YEARS, hs_to_resource

ZERO = Decimal(0)
# Relative gap band compatible with usual freight and insurance (CIF vs FOB). [HYPOTHÈSE]
CIF_FOB_BAND = (Decimal("0"), Decimal("0.10"))
COMPUTED_POINTS = 70
LEVELS = ((70, "high"), (40, "medium"), (0, "low"))  # [HYPOTHÈSE]


def rel(num: Decimal, den: Decimal) -> Decimal | None:
    return None if den == 0 else num / den


def r4(d: Decimal | None) -> str | None:
    return None if d is None else str(d.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def level(score: int) -> str:
    return next(name for floor, name in LEVELS if score >= floor)


@dataclass
class Cell:
    reporter: str
    partner: str
    hs: str
    year: int
    x: Decimal | None = None
    m: Decimal | None = None
    x_kg: Decimal | None = None
    m_kg: Decimal | None = None
    kg_estimated: bool = False
    m_valuation: str | None = None
    sources: set[str] = field(default_factory=set)
    score: int = 0
    reasons: list[tuple[int, str]] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.x is not None and self.m is not None:
            return "complete"
        return "export_only" if self.x is not None else "import_only"

    @property
    def gap(self) -> Decimal | None:
        return None if self.status != "complete" else self.m - self.x

    @property
    def rel_gap(self) -> Decimal | None:
        if self.status != "complete":
            return None
        return rel(self.m - self.x, max(self.m, self.x))

    @property
    def weight(self) -> Decimal:
        return max(self.x or ZERO, self.m or ZERO)

    def uv(self, side: str) -> Decimal | None:
        v, kg = (self.x, self.x_kg) if side == "x" else (self.m, self.m_kg)
        if v is None or kg is None or kg == 0:
            return None
        return v / kg * 1000  # USD per tonne

    def to_json(self) -> dict:
        return {
            "partner": self.partner, "hs": self.hs, "year": self.year, "status": self.status,
            "x": r4(self.x), "m": r4(self.m), "gap": r4(self.gap), "rel_gap": r4(self.rel_gap),
            "x_t": r4(self.x_kg / 1000) if self.x_kg is not None else None,
            "m_t": r4(self.m_kg / 1000) if self.m_kg is not None else None,
            "uv_x": r4(self.uv("x")), "uv_m": r4(self.uv("m")), "m_valuation": self.m_valuation,
            "cif_fob_band": self.in_cif_band(), "score": self.score, "level": level(self.score),
            "reasons": [t for _, t in sorted(self.reasons, key=lambda r: r[0])[:3]],
            "sources": sorted(self.sources),
        }

    def in_cif_band(self) -> bool | None:
        g = self.rel_gap
        return None if g is None else CIF_FOB_BAND[0] <= g <= CIF_FOB_BAND[1]


def build_cells(flows: Iterable[Flow]) -> dict[tuple, Cell]:
    cells: dict[tuple, Cell] = {}
    for f in flows:
        if f.reporter == f.partner:
            continue
        if f.flow == "X" and f.reporter in PILOT:
            key = (f.reporter, f.partner, f.hs, f.year)
            c = cells.setdefault(key, Cell(*key))
            c.x, c.x_kg = (c.x or ZERO) + f.value_usd, _add(c.x_kg, f.net_kg)
        elif f.flow == "M" and f.partner in PILOT:
            key = (f.partner, f.reporter, f.hs, f.year)  # exporter first
            c = cells.setdefault(key, Cell(*key))
            c.m, c.m_kg = (c.m or ZERO) + f.value_usd, _add(c.m_kg, f.net_kg)
            c.m_valuation = f.valuation
        else:
            continue
        c.kg_estimated |= f.net_kg_estimated
        c.sources.add(f.sha256)
    return cells


def _add(a: Decimal | None, b: Decimal | None) -> Decimal | None:
    if a is None:
        return b
    return a if b is None else a + b


def score_cells(cells: dict[tuple, Cell]) -> None:
    # Reporting coverage: years each exporter declared each resource, and years each partner
    # declared imports of it from that exporter.
    exp_years: dict[tuple, set[int]] = defaultdict(set)
    imp_years: dict[tuple, set[int]] = defaultdict(set)
    signs: dict[tuple, list[int]] = defaultdict(list)
    for c in cells.values():
        res = hs_to_resource(c.hs).key
        if c.x is not None:
            exp_years[(c.reporter, res)].add(c.year)
        if c.m is not None:
            imp_years[(c.reporter, c.partner, res)].add(c.year)
        if c.gap is not None and c.gap != 0:
            signs[(c.reporter, c.partner, c.hs)].append(1 if c.gap > 0 else -1)
    n_years = len(YEARS)

    for c in cells.values():
        res = hs_to_resource(c.hs).key
        pts, why = 0, []
        # 1. Mirror availability (15)
        if c.status == "complete":
            pts += 10
            if c.x_kg is not None and c.m_kg is not None and not c.kg_estimated:
                pts += 5
            else:
                why.append((2, "Quantités absentes ou estimées d'un côté"))
        else:
            why.append((0, "Exportateur seul déclarant" if c.status == "export_only"
                        else "Partenaire seul déclarant (l'exportateur ne déclare pas ce flux)"))
        # 2. Quantity coherence (15)
        if c.status == "complete" and c.x_kg and c.m_kg:
            d = abs(c.m_kg - c.x_kg) / max(c.m_kg, c.x_kg)
            if d <= Decimal("0.10"):
                pts += 15
            elif d <= Decimal("0.25"):
                pts += 8
                why.append((3, "Quantités divergentes (10 à 25 %)"))
            else:
                why.append((1, "Quantités très divergentes (plus de 25 %)"))
        # 3. Exporter reporting regularity (10)
        ey = len(exp_years[(c.reporter, res)])
        pts += round(10 * ey / n_years)
        if ey < n_years:
            why.append((5, f"Exportateur déclarant {ey} année(s) sur {n_years}"))
        # 4. Partner reporting regularity (10)
        iy = len(imp_years[(c.reporter, c.partner, res)])
        pts += round(10 * iy / n_years)
        if iy < n_years:
            why.append((6, f"Partenaire déclarant {iy} année(s) sur {n_years}"))
        # 5. No hub / transit (10)
        hub_pts = 10
        if c.partner in HUB_PARTNERS:
            hub_pts -= 5
            why.append((3, "Partenaire identifié comme plateforme de négoce ou de transit"))
        if c.reporter in LANDLOCKED:
            hub_pts -= 5
            why.append((4, "Pays enclavé : exportations en transit par un pays tiers"))
        pts += hub_pts
        # 6. Temporal stability of the gap's sign (10)
        if c.gap:
            sign = 1 if c.gap > 0 else -1
            same = signs[(c.reporter, c.partner, c.hs)].count(sign)
            pts += 10 if same >= 3 else 5 if same == 2 else 0
            if same < 3:
                why.append((5, "Écart non persistant dans le temps"))
        c.score = round(pts * 100 / COMPUTED_POINTS)
        c.reasons = why


def indicators(cells: dict[tuple, Cell]) -> list[dict]:
    """ARVI-1/2/3 per (country, resource, year)."""
    groups: dict[tuple, list[Cell]] = defaultdict(list)
    for c in cells.values():
        groups[(c.reporter, hs_to_resource(c.hs).key, c.year)].append(c)

    out = []
    for (country, res_key, year), cs in sorted(groups.items()):
        res = RESOURCES[res_key]
        if res_key not in PILOT.get(country, ()):
            continue
        x_total = sum((c.x for c in cs if c.x is not None), ZERO)
        m_total = sum((c.m for c in cs if c.m is not None), ZERO)
        comp = [c for c in cs if c.status == "complete"]
        pos = sum((c.gap for c in comp if c.gap > 0), ZERO)
        neg = sum((c.gap for c in comp if c.gap < 0), ZERO)
        exp_only = sum((c.x for c in cs if c.status == "export_only"), ZERO)
        imp_only = sum((c.m for c in cs if c.status == "import_only"), ZERO)
        total_w = sum((c.weight for c in cs), ZERO)
        comp_w = sum((c.weight for c in comp), ZERO)
        score = round(sum((c.score * c.weight for c in cs), ZERO) / total_w) if total_w else 0

        # ARVI-2: unit values per HS code over complete cells with both quantities.
        arvi2 = []
        for hs in res.hs_codes:
            q = [c for c in comp if c.hs == hs and c.x_kg and c.m_kg]
            if not q:
                continue
            sx, sm = sum((c.x for c in q), ZERO), sum((c.m for c in q), ZERO)
            kx, km = sum((c.x_kg for c in q), ZERO), sum((c.m_kg for c in q), ZERO)
            uvx, uvm = sx / kx * 1000, sm / km * 1000
            arvi2.append({"hs": hs, "stage": res.stage_of(hs).name_fr, "cells": len(q),
                          "uv_x": r4(uvx), "uv_m": r4(uvm), "ratio": r4(uvm / uvx)})

        # ARVI-3: export structure along the chain, from each side's declarations.
        by_stage = []
        for st in res.stages:
            vx = sum((c.x for c in cs if c.x is not None and c.hs in st.hs_codes), ZERO)
            vm = sum((c.m for c in cs if c.m is not None and c.hs in st.hs_codes), ZERO)
            by_stage.append({"order": st.order, "stage": st.name_fr, "x": r4(vx), "m": r4(vm),
                             "share_x": r4(rel(vx, x_total)), "share_m": r4(rel(vm, m_total))})

        # A side with no declaration at all is "not declared", never zero.
        has_x, has_m = any(c.x is not None for c in cs), any(c.m is not None for c in cs)
        both = has_x and has_m
        top = sorted(cs, key=lambda c: c.weight, reverse=True)
        out.append({
            "country": country, "resource": res_key, "year": year,
            "arvi1": {
                "x_total": r4(x_total) if has_x else None, "m_total": r4(m_total) if has_m else None,
                "gap_total": r4(m_total - x_total) if both else None,
                "rel_gap_total": r4(rel(m_total - x_total, max(m_total, x_total))) if both else None,
                "complete_positive": r4(pos), "complete_negative": r4(neg),
                "complete_net": r4(pos + neg),
                "export_only": r4(exp_only), "import_only": r4(imp_only),
                "complete_share": r4(rel(comp_w, total_w)),
                "cells": len(cs), "complete_cells": len(comp),
            },
            "arvi2": arvi2,
            "arvi3": {"lowest_stage": res.stages[0].name_fr,
                      "lowest_share_x": by_stage[0]["share_x"] if has_x else None,
                      "lowest_share_m": by_stage[0]["share_m"] if has_m else None,
                      "by_stage": by_stage},
            "confidence": {"score": score, "level": level(score)},
            "cells": [c.to_json() for c in top],
        })
    return out
