"""Systèmes de coordonnées : choix d'un SCR métrique et reprojections.

Règle (CLAUDE.md §4) : les longueurs et surfaces sont mesurées dans un SCR métrique adapté,
jamais en EPSG:4326 ni EPSG:3857. Le moteur utilise la zone UTM (WGS 84) qui contient le
centroïde du site ; la surface est recoupée par un calcul géodésique indépendant
(``app.geo.engine``) pour détecter une distorsion anormale.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
import shapely
from pyproj import CRS, Transformer
from shapely.geometry.base import BaseGeometry

STORAGE_EPSG = 4326  # stockage et affichage ; jamais utilisé pour mesurer


class CRSError(ValueError):
    """SCR absent, illisible ou incohérent."""


def utm_epsg_for(lon: float, lat: float) -> int:
    """Code EPSG de la zone UTM WGS 84 contenant (lon, lat).

    Les exceptions norvégiennes (zones 32V, 31X–37X) ne concernent pas l'Afrique et ne sont pas
    gérées.
    """
    if not (-180.0 <= lon <= 180.0 and -80.0 <= lat <= 84.0):
        raise CRSError(f"Coordonnées hors du domaine UTM : lon={lon}, lat={lat}")
    zone = int((lon + 180.0) // 6.0) + 1
    zone = min(zone, 60)
    return (32600 if lat >= 0 else 32700) + zone


def parse_crs(value: str | int | None) -> CRS | None:
    if value is None or value == "":
        return None
    try:
        return CRS.from_user_input(value)
    except Exception as exc:  # pyproj lève CRSError ou ValueError selon les cas
        raise CRSError(f"SCR illisible : {value!r} ({exc})") from exc


def crs_label(crs: CRS) -> str:
    epsg = crs.to_epsg()
    return f"EPSG:{epsg}" if epsg else crs.name


@lru_cache(maxsize=128)
def _transformer(src_wkt: str, dst_wkt: str) -> Transformer:
    return Transformer.from_crs(CRS.from_wkt(src_wkt), CRS.from_wkt(dst_wkt), always_xy=True)


def transform_geom(geom: BaseGeometry, src: CRS | int, dst: CRS | int) -> BaseGeometry:
    src_crs = src if isinstance(src, CRS) else CRS.from_epsg(src)
    dst_crs = dst if isinstance(dst, CRS) else CRS.from_epsg(dst)
    if src_crs == dst_crs:
        return geom
    tr = _transformer(src_crs.to_wkt(), dst_crs.to_wkt())

    def _fn(coords: np.ndarray) -> np.ndarray:
        x, y = tr.transform(coords[:, 0], coords[:, 1])
        out = np.column_stack([x, y])
        if not np.all(np.isfinite(out)):
            raise CRSError("La reprojection a produit des coordonnées non finies (SCR incohérent ?)")
        return out

    return shapely.transform(geom, _fn)
