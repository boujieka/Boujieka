"""Import de fichiers vectoriels avec contrôle du SCR et des géométries.

Formats : GeoJSON, Shapefile en ZIP, GeoPackage, KML, KMZ, CSV de points (colonnes lon/lat ou x/y).
Lecture via GDAL (pyogrio) sauf CSV (module ``csv``, pour un contrôle explicite des colonnes).

Sécurité (CLAUDE.md §13) : taille maximale, liste blanche d'extensions, archives ZIP contrôlées
(nombre d'entrées, taille décompressée, taux de compression, chemins absolus ou « .. », liens
symboliques). Aucune URL n'est jamais téléchargée par ce module (pas de risque SSRF).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math
import stat
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

import pyogrio
import shapely
from pyproj import CRS
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from app.geo.crs import STORAGE_EPSG, CRSError, crs_label, parse_crs, transform_geom
from app.geo.validation import GeometryError, check_lonlat_range, clean_geometry, outside_africa

EXTENSIONS = {
    ".geojson": "geojson",
    ".json": "geojson",
    ".zip": "shapefile_zip",
    ".gpkg": "gpkg",
    ".kml": "kml",
    ".kmz": "kmz",
    ".csv": "csv",
}
MAX_FEATURES = 50_000
ZIP_MAX_ENTRIES = 200
ZIP_MAX_TOTAL_BYTES = 200 * 1024 * 1024
ZIP_MAX_RATIO = 100


class ImportError_(ValueError):
    """Fichier refusé ; le message est destiné à l'utilisateur."""


@dataclass
class ImportedLayer:
    file_format: str
    sha256: str
    source_crs: str
    crs_origin: str  # "fichier", "declare", "implicite_rfc7946", "implicite_kml"
    geometries: list[BaseGeometry]  # EPSG:4326, valides, 2D
    properties: list[dict[str, Any]]
    warnings: list[str] = field(default_factory=list)
    skipped_empty: int = 0

    @property
    def bbox(self) -> list[float] | None:
        if not self.geometries:
            return None
        return list(shapely.GeometryCollection(self.geometries).bounds)

    @property
    def geometry_types(self) -> list[str]:
        return sorted({g.geom_type for g in self.geometries})


def detect_format(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in EXTENSIONS:
        raise ImportError_(
            f"Extension {ext or '(aucune)'} non acceptée. Formats admis : " + ", ".join(sorted(EXTENSIONS))
        )
    return EXTENSIONS[ext]


def _safe_extract(data: bytes, dest: Path) -> list[Path]:
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise ImportError_("Archive ZIP illisible") from exc
    infos = zf.infolist()
    if len(infos) > ZIP_MAX_ENTRIES:
        raise ImportError_(f"Archive refusée : plus de {ZIP_MAX_ENTRIES} entrées")
    total = sum(i.file_size for i in infos)
    if total > ZIP_MAX_TOTAL_BYTES:
        raise ImportError_("Archive refusée : taille décompressée excessive")
    compressed = sum(i.compress_size for i in infos) or 1
    if total / compressed > ZIP_MAX_RATIO:
        raise ImportError_("Archive refusée : taux de compression anormal (risque de bombe ZIP)")
    out: list[Path] = []
    for info in infos:
        name = PurePosixPath(info.filename.replace("\\", "/"))
        if name.is_absolute() or ".." in name.parts or (info.filename[:1] == "/"):
            raise ImportError_(f"Archive refusée : chemin dangereux {info.filename!r}")
        if stat.S_ISLNK(info.external_attr >> 16):
            raise ImportError_(f"Archive refusée : lien symbolique {info.filename!r}")
        if info.is_dir():
            continue
        target = dest.joinpath(*name.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(info) as src:
            content = src.read(ZIP_MAX_TOTAL_BYTES + 1)
        if len(content) != info.file_size:
            raise ImportError_("Archive refusée : taille d'entrée incohérente")
        target.write_bytes(content)
        out.append(target)
    return out


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, (dt.date, dt.datetime, dt.time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    if hasattr(value, "item"):  # numpy scalaire
        return _json_safe(value.item())
    return str(value)


def _read_gdal(path: Path, layer: str | None) -> tuple[list[BaseGeometry | None], list[dict], str | None]:
    try:
        layers = pyogrio.list_layers(path)
    except Exception as exc:
        raise ImportError_(f"Fichier illisible par GDAL : {exc}") from exc
    names = [str(n) for n, _ in layers]
    if layer is None:
        if len(names) > 1:
            raise ImportError_("Le fichier contient plusieurs couches ; préciser « layer » parmi : " + ", ".join(names))
        layer = names[0] if names else None
    elif layer not in names:
        raise ImportError_(f"Couche {layer!r} absente. Couches disponibles : " + ", ".join(names))
    try:
        meta, _fids, wkb, field_data = pyogrio.raw.read(path, layer=layer, max_features=MAX_FEATURES + 1)
    except Exception as exc:
        raise ImportError_(f"Lecture impossible : {exc}") from exc
    if len(wkb) > MAX_FEATURES:
        raise ImportError_(f"Plus de {MAX_FEATURES} entités : découper le fichier")
    fields = list(meta["fields"])
    geoms = [shapely.from_wkb(b) if b is not None else None for b in wkb]
    props = [{f: _json_safe(field_data[j][i]) for j, f in enumerate(fields)} for i in range(len(geoms))]
    return geoms, props, meta.get("crs")


def _geojson_declares_crs(data: bytes) -> bool:
    try:
        obj = json.loads(data)
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(obj, dict) and obj.get("crs") is not None


def _read_csv(data: bytes, x_col: str | None, y_col: str | None) -> tuple[list[BaseGeometry | None], list[dict]]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ImportError_("CSV non encodé en UTF-8") from exc
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    cols = reader.fieldnames or []
    lower = {c.lower(): c for c in cols}
    x_col = x_col or next((lower[c] for c in ("lon", "longitude", "lng", "x") if c in lower), None)
    y_col = y_col or next((lower[c] for c in ("lat", "latitude", "y") if c in lower), None)
    if not x_col or not y_col or x_col not in cols or y_col not in cols:
        raise ImportError_("Colonnes de coordonnées introuvables ; préciser x_column et y_column. Colonnes : " + ", ".join(cols))
    geoms, props = [], []
    for n, row in enumerate(reader, start=2):
        if len(geoms) >= MAX_FEATURES:
            raise ImportError_(f"Plus de {MAX_FEATURES} lignes : découper le fichier")
        try:
            x = float(row[x_col].replace(",", "."))
            y = float(row[y_col].replace(",", "."))
        except (TypeError, ValueError, AttributeError) as exc:
            raise ImportError_(f"CSV ligne {n} : coordonnées non numériques") from exc
        geoms.append(Point(x, y))
        props.append({k: v for k, v in row.items() if k not in (x_col, y_col) and k is not None})
    return geoms, props


def read_vector_file(
    filename: str,
    data: bytes,
    *,
    declared_crs: str | None = None,
    layer: str | None = None,
    repair: bool = False,
    x_column: str | None = None,
    y_column: str | None = None,
) -> ImportedLayer:
    fmt = detect_format(filename)
    if not data:
        raise ImportError_("Fichier vide")
    sha = hashlib.sha256(data).hexdigest()
    warnings: list[str] = []
    declared = parse_crs(declared_crs) if declared_crs else None

    with tempfile.TemporaryDirectory(prefix="georenew-") as tmp:
        tmpdir = Path(tmp)
        file_crs: str | None = None
        if fmt == "csv":
            geoms, props = _read_csv(data, x_column, y_column)
        else:
            if fmt in ("shapefile_zip", "kmz"):
                files = _safe_extract(data, tmpdir)
                wanted = ".shp" if fmt == "shapefile_zip" else ".kml"
                cands = [p for p in files if p.suffix.lower() == wanted]
                if len(cands) != 1:
                    raise ImportError_(f"L'archive doit contenir exactement un fichier {wanted} (trouvé {len(cands)})")
                path = cands[0]
                if fmt == "shapefile_zip":
                    stem = path.with_suffix("")
                    present = {p.suffix.lower() for p in files if p.with_suffix("") == stem}
                    for req in (".shx", ".dbf"):
                        if req not in present:
                            raise ImportError_(f"Shapefile incomplet : fichier {req} manquant")
                    if ".prj" not in present and declared is None:
                        raise ImportError_("Shapefile sans fichier .prj : déclarer le SCR (champ declared_crs)")
            else:
                path = tmpdir / ("input" + Path(filename).suffix.lower())
                path.write_bytes(data)
            geoms, props, file_crs = _read_gdal(path, layer)
            if fmt == "geojson" and not _geojson_declares_crs(data):
                file_crs = None  # GDAL renvoie EPSG:4326 par défaut : SCR implicite, pas déclaré

    # Détermination du SCR source
    if fmt in ("kml", "kmz"):
        src, origin = CRS.from_epsg(STORAGE_EPSG), "implicite_kml"
        if declared is not None and declared != src:
            raise ImportError_("Le KML est toujours en WGS 84 ; le SCR déclaré est incohérent")
    elif file_crs:
        src, origin = parse_crs(file_crs), "fichier"
        if declared is not None and not declared.equals(src, ignore_axis_order=True):
            raise ImportError_(
                f"SCR déclaré ({crs_label(declared)}) différent du SCR du fichier ({crs_label(src)}) : import refusé"
            )
    elif declared is not None:
        src, origin = declared, "declare"
    elif fmt == "geojson":
        src, origin = CRS.from_epsg(STORAGE_EPSG), "implicite_rfc7946"
        warnings.append("GeoJSON sans SCR explicite : WGS 84 supposé (RFC 7946)")
    elif fmt == "csv":
        raise ImportError_("CSV sans SCR : déclarer le SCR des coordonnées (champ declared_crs, ex. EPSG:4326)")
    else:
        raise ImportError_("SCR absent du fichier : déclarer le SCR (champ declared_crs)")
    if src.is_geographic is False and src.is_projected is False:
        raise ImportError_(f"SCR non supporté : {crs_label(src)}")

    out_geoms: list[BaseGeometry] = []
    out_props: list[dict] = []
    skipped = 0
    for i, (g, p) in enumerate(zip(geoms, props)):
        if g is None or g.is_empty:
            skipped += 1
            continue
        try:
            g, w = clean_geometry(g, repair=repair, label=f"Entité n° {i + 1}")
            g = transform_geom(g, src, STORAGE_EPSG)
            check_lonlat_range(g)
            if not g.is_valid:  # la reprojection peut rendre invalide une géométrie limite
                g, w2 = clean_geometry(g, repair=repair, label=f"Entité n° {i + 1} (après reprojection)")
                w += w2
        except (GeometryError, CRSError) as exc:
            raise ImportError_(str(exc)) from exc
        warnings.extend(w)
        out_geoms.append(g)
        out_props.append(p)
    if skipped:
        warnings.append(f"{skipped} entité(s) sans géométrie ignorée(s)")
    if not out_geoms:
        raise ImportError_("Aucune géométrie exploitable dans le fichier")
    if outside_africa(shapely.GeometryCollection(out_geoms)):
        warnings.append("Emprise entièrement hors d'Afrique : vérifier le SCR et l'ordre des axes")

    return ImportedLayer(
        file_format=fmt,
        sha256=sha,
        source_crs=crs_label(src),
        crs_origin=origin,
        geometries=out_geoms,
        properties=out_props,
        warnings=warnings,
        skipped_empty=skipped,
    )
