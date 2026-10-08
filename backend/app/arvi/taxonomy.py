"""Pilot scope: resources, their processing chains (HS codes) and the countries covered.

HS codes are HS 2017/2022 headings as used by UN Comtrade. Each chain is ordered from the least
to the most processed stage. Pilot choice follows the blueprint (§14.2): start with resources
whose mirror statistics are the most reliable (base metals, bauxite, manganese, timber), not
crude oil or gold.
"""

from __future__ import annotations

from typing import NamedTuple


class Stage(NamedTuple):
    order: int  # 1 = least processed
    name_fr: str
    hs_codes: tuple[str, ...]


class Resource(NamedTuple):
    key: str
    name_fr: str
    family: str  # minerals | forestry
    stages: tuple[Stage, ...]

    @property
    def hs_codes(self) -> tuple[str, ...]:
        return tuple(c for s in self.stages for c in s.hs_codes)

    def stage_of(self, hs: str) -> Stage:
        for s in self.stages:
            if hs in s.hs_codes:
                return s
        raise KeyError(hs)


RESOURCES: dict[str, Resource] = {
    r.key: r
    for r in (
        Resource("copper", "Cuivre", "minerals", (
            Stage(1, "Minerais et concentrés", ("2603",)),
            Stage(2, "Mattes, cuivre de cément", ("7401",)),
            Stage(3, "Cuivre non affiné (blister, anodes)", ("7402",)),
            Stage(4, "Cuivre affiné (cathodes) et alliages bruts", ("7403",)),
        )),
        Resource("cobalt", "Cobalt", "minerals", (
            Stage(1, "Minerais et concentrés", ("2605",)),
            Stage(2, "Oxydes et hydroxydes", ("282200",)),
            Stage(3, "Mattes, cobalt brut et ouvrages", ("8105",)),
        )),
        Resource("bauxite", "Bauxite et aluminium", "minerals", (
            Stage(1, "Bauxite (minerai)", ("2606",)),
            Stage(2, "Alumine", ("281820",)),
            Stage(3, "Aluminium brut", ("7601",)),
        )),
        Resource("manganese", "Manganèse", "minerals", (
            Stage(1, "Minerais et concentrés", ("2602",)),
            Stage(2, "Ferromanganèse et silicomanganèse", ("720211", "720219", "720230")),
        )),
        Resource("timber", "Bois", "forestry", (
            Stage(1, "Grumes", ("4403",)),
            Stage(2, "Sciages", ("4407",)),
            Stage(3, "Placages", ("4408",)),
            Stage(4, "Contreplaqués", ("4412",)),
        )),
    )
}

# Reporter (ISO3) -> resources covered in the pilot.
PILOT: dict[str, tuple[str, ...]] = {
    "COD": ("copper", "cobalt"),
    "ZMB": ("copper", "cobalt"),
    "GIN": ("bauxite",),
    "GAB": ("manganese", "timber"),
    "ZAF": ("manganese",),
    "CMR": ("timber",),
    "COG": ("timber",),
}

YEARS: tuple[int, ...] = (2019, 2020, 2021, 2022, 2023)

# Partners that commonly act as trading or transit hubs, where the country recorded by the
# exporter often differs from the one recorded by the importer. [HYPOTHÈSE] list, to review.
HUB_PARTNERS: frozenset[str] = frozenset({"CHE", "ARE", "NLD", "BEL", "SGP", "HKG"})

# Landlocked pilot countries (exports transit through a third country's port).
LANDLOCKED: frozenset[str] = frozenset({"ZMB"})


def hs_to_resource(hs: str) -> Resource:
    for r in RESOURCES.values():
        if hs in r.hs_codes:
            return r
    raise KeyError(hs)
