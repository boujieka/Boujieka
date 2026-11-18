"""Validation des géométries (CLAUDE.md §5 : refuser proprement les erreurs)."""

from __future__ import annotations

import shapely
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.validation import explain_validity, make_valid

# Emprise large de l'Afrique et de ses îles (Cap-Vert, Maurice, Seychelles, Réunion...).
# Une géométrie hors de cette emprise n'est pas refusée mais signalée.
AFRICA_BBOX = (-26.0, -47.0, 64.0, 38.0)


class GeometryError(ValueError):
    """Géométrie invalide, vide ou de type inattendu."""


def check_lonlat_range(geom: BaseGeometry) -> None:
    minx, miny, maxx, maxy = geom.bounds
    if minx < -180 or maxx > 180 or miny < -90 or maxy > 90:
        raise GeometryError(
            "Coordonnées hors de la plage longitude/latitude "
            f"(emprise {minx:.3f}, {miny:.3f}, {maxx:.3f}, {maxy:.3f}). "
            "Le fichier est probablement en coordonnées projetées sans SCR déclaré."
        )


def outside_africa(geom: BaseGeometry) -> bool:
    minx, miny, maxx, maxy = geom.bounds
    a = AFRICA_BBOX
    return maxx < a[0] or minx > a[2] or maxy < a[1] or miny > a[3]


def clean_geometry(geom: BaseGeometry | None, *, repair: bool, label: str) -> tuple[BaseGeometry, list[str]]:
    """Retourne une géométrie 2D valide, ou lève ``GeometryError``.

    ``repair=False`` (défaut côté API) : une géométrie invalide est refusée avec la raison GEOS.
    ``repair=True`` : ``make_valid`` est appliqué et un avertissement est enregistré.
    """
    warnings: list[str] = []
    if geom is None or geom.is_empty:
        raise GeometryError(f"{label} : géométrie absente ou vide")
    if shapely.has_z(geom):
        geom = shapely.force_2d(geom)
        warnings.append(f"{label} : coordonnée Z ignorée (calculs en 2D)")
    if not geom.is_valid:
        reason = explain_validity(geom)
        if not repair:
            raise GeometryError(f"{label} : géométrie invalide ({reason})")
        geom = make_valid(geom)
        warnings.append(f"{label} : géométrie réparée par make_valid ({reason})")
    return geom, warnings


def polygonal_part(geom: BaseGeometry) -> Polygon | MultiPolygon | None:
    """Partie surfacique d'une géométrie (utile après make_valid, qui peut produire des collections)."""
    if isinstance(geom, (Polygon, MultiPolygon)):
        return geom
    polys = [g for g in getattr(geom, "geoms", []) if isinstance(g, (Polygon, MultiPolygon))]
    if not polys:
        return None
    merged = shapely.union_all(polys)
    return merged if isinstance(merged, (Polygon, MultiPolygon)) else None


def require_polygonal(geom: BaseGeometry, label: str) -> Polygon | MultiPolygon:
    poly = polygonal_part(geom)
    if poly is None or poly.is_empty:
        raise GeometryError(f"{label} : une limite de site doit être un polygone (reçu {geom.geom_type})")
    if poly.area == 0:
        raise GeometryError(f"{label} : polygone d'aire nulle")
    return poly
