"""Outils de test : géométries de référence construites en UTM puis exprimées en WGS 84.

Les sites de test sont FICTIFS. Construire en UTM permet de connaître la surface exacte attendue
(ex. carré de 1 000 m → 100 ha) indépendamment du moteur.
"""

from shapely.geometry import box, mapping
from shapely.geometry.base import BaseGeometry

from app.geo.crs import transform_geom

UTM35S = 32735  # zone du centroïde des sites de test (Afrique du Sud, ~27° E, ~26,5° S)
X0, Y0 = 500_000.0, 7_070_000.0  # méridien central de la zone 35


def ll(g: BaseGeometry, epsg: int = UTM35S) -> BaseGeometry:
    return transform_geom(g, epsg, 4326)


def utm_box(x1, y1, x2, y2) -> BaseGeometry:
    return box(X0 + x1, Y0 + y1, X0 + x2, Y0 + y2)


def site_1km() -> BaseGeometry:
    return ll(utm_box(0, 0, 1000, 1000))


def fc(*geoms: BaseGeometry, props: list[dict] | None = None) -> dict:
    props = props or [{} for _ in geoms]
    return {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": mapping(g), "properties": p} for g, p in zip(geoms, props)],
    }
