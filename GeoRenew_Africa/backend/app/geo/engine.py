"""Moteur de screening spatial (phase P1) — reconstruit de zéro, le prototype initial étant perdu.

Entrée : une limite de site (EPSG:4326), un recul de limite, des règles d'exclusion strictes et
des contraintes indicatives, chacune avec ses géométries (EPSG:4326), un buffer et sa
justification.

Méthode (voir docs/METHODES_P1.md) :

1. Projection de toutes les géométries dans la zone UTM WGS 84 du centroïde du site.
2. Zone aménageable = site rétréci du recul (buffer négatif, ``quad_segs`` fixe).
3. Zone de chaque règle = union des entités tamponnées, coupée par le site.
4. Exclusions strictes : **union** de toutes les zones strictes, donc un chevauchement n'est
   soustrait qu'une seule fois. Surface nette = zone aménageable − union des exclusions.
5. Contraintes indicatives : surface affectée *dans* la surface nette ; jamais soustraite.
6. Intervalle de sensibilité de la surface nette, seulement si la précision de position est
   renseignée pour la limite et pour chaque couche d'exclusion stricte.
7. Contrôle croisé : surface brute UTM vs surface géodésique (ellipsoïde WGS 84).

Le moteur est pur et déterministe : mêmes entrées → mêmes sorties, bit à bit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import shapely
import shapely.validation
from pyproj import CRS, Geod
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from app.geo.crs import STORAGE_EPSG, transform_geom, utm_epsg_for
from app.geo.validation import GeometryError, polygonal_part, require_polygonal

ENGINE_VERSION = "screening-1.0.0"
QUAD_SEGS = 16  # segments par quart de cercle pour tous les buffers (cercle ≈ 64 côtés)
AREA_TOLERANCE_M2 = 1e-3
GEODESIC_TOLERANCE = 0.005  # 0,5 % d'écart toléré entre surface UTM et surface géodésique

HARD = "exclusion_stricte"
SOFT = "contrainte_indicative"

_GEOD = Geod(ellps="WGS84")


@dataclass(frozen=True)
class RuleInput:
    rule_id: int
    name: str
    kind: str
    buffer_m: float
    geometries: tuple[BaseGeometry, ...]
    accuracy_m: float | None = None
    justification: str = ""
    reference: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ScreeningParams:
    setback_m: float = 0.0
    setback_justification: str = ""
    boundary_accuracy_m: float | None = None
    density_mwp_dc_per_ha: float | None = None
    density_justification: str = ""


@dataclass
class ScreeningResult:
    crs_epsg: int
    crs_name: str
    metrics: dict[str, Any]
    per_rule: list[dict[str, Any]]
    checks: list[dict[str, Any]]
    warnings: list[str]
    layers: list[tuple[str, int | None, BaseGeometry, float]]  # (type, rule_id, géométrie EPSG:4326, aire m² UTM)

    def as_dict(self) -> dict[str, Any]:
        return {
            "version_moteur": ENGINE_VERSION,
            "scr_calcul": f"EPSG:{self.crs_epsg}",
            "scr_calcul_nom": self.crs_name,
            "niveau_etude": "reconnaissance préliminaire",
            "mention": "Screening géospatial indicatif — non bancable, ne remplace pas une étude de faisabilité.",
            "indicateurs": self.metrics,
            "par_regle": self.per_rule,
            "controles": self.checks,
            "avertissements": self.warnings,
        }


def _area_metric(m2: float, nature: str, method: str) -> dict[str, Any]:
    return {"valeur_m2": m2, "valeur_ha": m2 / 10_000.0, "unite": "m²", "nature": nature, "methode": method}


def _rule_zone(
    geoms_utm: list[BaseGeometry], buffer_m: float, clip: BaseGeometry
) -> tuple[BaseGeometry, int, int]:
    """Zone d'une règle coupée par ``clip``. Retourne (zone, entités retenues, entités sans effet)."""
    parts: list[BaseGeometry] = []
    kept = 0
    no_effect = 0
    reach = max(buffer_m, 0.0)
    for g in geoms_utm:
        if g.distance(clip) > reach + 1e-9:
            continue
        kept += 1
        if buffer_m != 0:
            z = g.buffer(buffer_m, quad_segs=QUAD_SEGS)
        else:
            z = polygonal_part(g)
        if z is None or z.is_empty:
            no_effect += 1
            continue
        parts.append(z)
    if not parts:
        return Polygon(), kept, no_effect
    zone = shapely.union_all(parts).intersection(clip)
    return (polygonal_part(zone) or Polygon()), kept, no_effect


def _shrink(site: BaseGeometry, d: float) -> BaseGeometry:
    if d == 0:
        return site
    return polygonal_part(site.buffer(-d, quad_segs=QUAD_SEGS)) or Polygon()


def _net_area(site, setback, hard_geoms, buffer_delta: dict[int, float]) -> float:
    """Surface nette pour un jeu de buffers ajustés (calcul d'intervalle)."""
    buildable = _shrink(site, setback)
    zones = []
    for rule, geoms in hard_geoms:
        z, _, _ = _rule_zone(geoms, rule.buffer_m + buffer_delta[rule.rule_id], site)
        zones.append(z)
    union = shapely.union_all(zones) if zones else Polygon()
    return buildable.difference(union).area


def screen_site(boundary: BaseGeometry, params: ScreeningParams, rules: list[RuleInput]) -> ScreeningResult:
    """Exécute le screening. ``boundary`` et les géométries des règles sont en EPSG:4326."""
    warnings: list[str] = []
    if boundary is None or boundary.is_empty:
        raise GeometryError("Limite de site absente ou vide")
    if not boundary.is_valid:
        raise GeometryError("Limite de site invalide (" + shapely.validation.explain_validity(boundary) + ")")
    site_ll = require_polygonal(boundary, "Limite de site")
    if params.setback_m < 0:
        raise GeometryError("Le recul de limite doit être positif ou nul")
    for r in rules:
        if r.kind not in (HARD, SOFT):
            raise GeometryError(f"Règle {r.name!r} : type inconnu {r.kind!r}")
        if r.buffer_m < 0:
            raise GeometryError(f"Règle {r.name!r} : buffer négatif interdit")

    c = site_ll.centroid
    epsg = utm_epsg_for(c.x, c.y)
    utm = CRS.from_epsg(epsg)
    central_meridian = (epsg % 100) * 6 - 183
    minx, _, maxx, _ = site_ll.bounds
    if max(abs(minx - central_meridian), abs(maxx - central_meridian)) > 3.5:
        warnings.append(
            "Le site déborde de sa zone UTM : distorsion d'échelle accrue (voir contrôle géodésique)."
        )

    site = transform_geom(site_ll, STORAGE_EPSG, utm)
    gross = site.area

    buildable = _shrink(site, params.setback_m)
    setback_strip = polygonal_part(site.difference(buildable)) or Polygon()
    if params.setback_m > 0 and buildable.is_empty:
        warnings.append("Le recul de limite consomme la totalité du site.")

    hard_geoms: list[tuple[RuleInput, list[BaseGeometry]]] = []
    soft_geoms: list[tuple[RuleInput, list[BaseGeometry]]] = []
    for r in rules:
        geoms = [transform_geom(g, STORAGE_EPSG, utm) for g in r.geometries]
        (hard_geoms if r.kind == HARD else soft_geoms).append((r, geoms))

    per_rule: list[dict[str, Any]] = []
    layers: list[tuple[str, int | None, BaseGeometry]] = []
    hard_zones: list[BaseGeometry] = []

    for r, geoms in hard_geoms:
        zone, kept, no_effect = _rule_zone(geoms, r.buffer_m, site)
        hard_zones.append(zone)
        layers.append((HARD, r.rule_id, zone))
        if no_effect:
            warnings.append(
                f"Règle « {r.name} » : {no_effect} entité(s) ponctuelle(s) ou linéaire(s) sans buffer "
                "n'excluent aucune surface."
            )
        per_rule.append(
            {
                "regle_id": r.rule_id,
                "nom": r.name,
                "type": r.kind,
                "buffer_m": r.buffer_m,
                "justification": r.justification,
                "reference_donnees": r.reference,
                "entites_retenues": kept,
                "surface_dans_site_m2": zone.area,
                "surface_dans_zone_amenageable_m2": zone.intersection(buildable).area,
            }
        )

    hard_union = (polygonal_part(shapely.union_all(hard_zones)) if hard_zones else None) or Polygon()
    excluded_in_buildable = buildable.intersection(hard_union).area
    net_geom = polygonal_part(buildable.difference(hard_union)) or Polygon()
    net = net_geom.area
    sum_individual = sum(p["surface_dans_zone_amenageable_m2"] for p in per_rule if p["type"] == HARD)

    soft_zones: list[BaseGeometry] = []
    for r, geoms in soft_geoms:
        zone, kept, no_effect = _rule_zone(geoms, r.buffer_m, site)
        in_net = polygonal_part(zone.intersection(net_geom)) or Polygon()
        soft_zones.append(in_net)
        layers.append((SOFT, r.rule_id, in_net))
        if no_effect:
            warnings.append(
                f"Contrainte « {r.name} » : {no_effect} entité(s) ponctuelle(s) ou linéaire(s) sans buffer "
                "n'ont aucune emprise."
            )
        per_rule.append(
            {
                "regle_id": r.rule_id,
                "nom": r.name,
                "type": r.kind,
                "buffer_m": r.buffer_m,
                "justification": r.justification,
                "reference_donnees": r.reference,
                "entites_retenues": kept,
                "surface_dans_site_m2": zone.area,
                "surface_dans_surface_nette_m2": in_net.area,
            }
        )
    soft_union = shapely.union_all(soft_zones).area if soft_zones else 0.0

    method_utm = f"Aire planimétrique en EPSG:{epsg} ({utm.name})"
    metrics: dict[str, Any] = {
        "surface_brute": _area_metric(gross, "calcule", method_utm),
        "surface_recul": _area_metric(
            setback_strip.area, "calcule", f"Bande de recul de {params.setback_m:g} m (buffer intérieur)"
        ),
        "surface_exclusions_strictes": _area_metric(
            excluded_in_buildable, "calcule", "Union des exclusions strictes dans la zone aménageable"
        ),
        "surface_nette": _area_metric(net, "calcule", "Zone aménageable moins l'union des exclusions strictes"),
        "somme_exclusions_par_regle": _area_metric(
            sum_individual, "calcule", "Somme des surfaces de chaque exclusion, chevauchements compris"
        ),
        "chevauchement_non_double_compte": _area_metric(
            sum_individual - excluded_in_buildable,
            "calcule",
            "Surface en chevauchement entre exclusions, soustraite une seule fois",
        ),
        "surface_contraintes_indicatives": _area_metric(
            soft_union, "calcule", "Union des contraintes indicatives dans la surface nette (non soustraite)"
        ),
    }

    # Intervalle de sensibilité à la précision de position.
    missing = []
    if params.boundary_accuracy_m is None:
        missing.append("limite de site")
    missing += [r.name for r, _ in hard_geoms if r.accuracy_m is None]
    if missing:
        metrics["intervalle_surface_nette"] = {
            "bas_m2": None,
            "haut_m2": None,
            "nature": "inconnu",
            "methode": "Précision de position non renseignée pour : " + ", ".join(missing),
        }
    else:
        acc_b = params.boundary_accuracy_m or 0.0
        site_low = _shrink(site, acc_b)
        site_high = polygonal_part(site.buffer(acc_b, quad_segs=QUAD_SEGS)) if acc_b else site
        low = _net_area(site_low, params.setback_m, hard_geoms, {r.rule_id: r.accuracy_m for r, _ in hard_geoms})
        high = _net_area(
            site_high, params.setback_m, hard_geoms, {r.rule_id: -(r.accuracy_m or 0.0) for r, _ in hard_geoms}
        )
        metrics["intervalle_surface_nette"] = {
            "bas_m2": low,
            "haut_m2": high,
            "nature": "calcule",
            "methode": (
                "Sensibilité géométrique : limite et exclusions décalées de ± leur précision de position "
                "déclarée. Ce n'est pas un intervalle statistique."
            ),
        }

    if params.density_mwp_dc_per_ha is not None:
        metrics["puissance_indicative_mwp_dc"] = {
            "valeur": net / 10_000.0 * params.density_mwp_dc_per_ha,
            "unite": "MWp DC",
            "nature": "hypothetique",
            "methode": (
                f"Surface nette × densité hypothétique de {params.density_mwp_dc_per_ha:g} MWp DC/ha "
                f"({params.density_justification or 'justification non fournie'}). Strictement indicatif : "
                "aucune implantation, ni pente, ni ombrage, ni MW AC."
            ),
        }
    else:
        metrics["puissance_indicative_mwp_dc"] = {
            "valeur": None,
            "unite": "MWp DC",
            "nature": "inconnu",
            "methode": "Densité de puissance non renseignée",
        }

    # Contrôles
    geodesic = abs(_GEOD.geometry_area_perimeter(site_ll)[0])
    rel = abs(gross - geodesic) / geodesic if geodesic else 0.0
    balance = gross - setback_strip.area - excluded_in_buildable - net
    checks = [
        {
            "nom": "conservation_des_surfaces",
            "ok": abs(balance) <= AREA_TOLERANCE_M2 + 1e-9 * gross,
            "detail": f"brute − recul − exclusions − nette = {balance:.6f} m²",
        },
        {
            "nom": "controle_geodesique",
            "ok": rel <= GEODESIC_TOLERANCE,
            "detail": f"surface géodésique WGS 84 = {geodesic:.3f} m² ; écart relatif UTM = {rel:.5%}",
        },
    ]
    if rel > GEODESIC_TOLERANCE:
        warnings.append("Écart UTM/géodésique supérieur à 0,5 % : vérifier la projection choisie.")

    layers = (
        [("limite_site", None, site), ("bande_recul", None, setback_strip)]
        + layers
        + [("exclusions_union", None, hard_union), ("surface_nette", None, net_geom)]
    )
    layers_ll = [(k, rid, transform_geom(g, utm, STORAGE_EPSG), g.area) for k, rid, g in layers]

    return ScreeningResult(
        crs_epsg=epsg,
        crs_name=utm.name,
        metrics=metrics,
        per_rule=per_rule,
        checks=checks,
        warnings=warnings,
        layers=layers_ll,
    )
