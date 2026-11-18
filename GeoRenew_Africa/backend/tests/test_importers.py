"""Import de fichiers : formats, contrôle du SCR, géométries, sécurité des archives."""

import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pyogrio
import pytest
import shapely
from shapely.geometry import Polygon

from app.geo.crs import transform_geom
from app.geo.importers import ImportError_, read_vector_file
from tests.helpers import UTM35S, fc, site_1km, utm_box


def write_vector(path: Path, geoms_utm, driver: str, crs: str | None = f"EPSG:{UTM35S}") -> Path:
    pyogrio.raw.write(
        path,
        np.array([shapely.to_wkb(g) for g in geoms_utm], dtype=object),
        [np.array([f"zone {i}" for i in range(len(geoms_utm))], dtype=object)],
        ["nom"],
        driver=driver,
        geometry_type="Polygon",
        crs=crs,
    )
    return path


def zip_dir(files: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    return buf.getvalue()


def shapefile_zip(tmp_path: Path, with_prj: bool = True) -> bytes:
    shp = write_vector(tmp_path / "zones.shp", [utm_box(0, 0, 1000, 1000)], "ESRI Shapefile")
    files = {p.name: p.read_bytes() for p in tmp_path.glob("zones.*") if with_prj or p.suffix != ".prj"}
    assert shp.exists()
    return zip_dir(files)


def test_geojson_without_crs_assumes_rfc7946():
    data = json.dumps(fc(site_1km())).encode()
    layer = read_vector_file("site.geojson", data)
    assert layer.source_crs == "EPSG:4326" and layer.crs_origin == "implicite_rfc7946"
    assert any("RFC 7946" in w for w in layer.warnings)
    assert len(layer.sha256) == 64


def test_geojson_with_projected_coordinates_but_no_crs_is_refused():
    data = json.dumps(fc(utm_box(0, 0, 1000, 1000))).encode()  # coordonnées UTM sans SCR
    with pytest.raises(ImportError_, match="hors de la plage"):
        read_vector_file("site.geojson", data)


def test_gpkg_in_utm_is_reprojected_without_area_loss(tmp_path):
    path = write_vector(tmp_path / "zones.gpkg", [utm_box(0, 0, 1000, 1000)], "GPKG")
    layer = read_vector_file("zones.gpkg", path.read_bytes())
    assert layer.source_crs == "EPSG:32735" and layer.crs_origin == "fichier"
    back = transform_geom(layer.geometries[0], 4326, UTM35S)
    assert back.area == pytest.approx(1_000_000, rel=1e-9)
    assert layer.properties[0]["nom"] == "zone 0"
    lon, lat = layer.geometries[0].centroid.coords[0]
    assert 26.5 < lon < 27.5 and -27 < lat < -26


def test_geojson_legacy_crs_member_is_honoured():
    data = fc(utm_box(0, 0, 1000, 1000))
    data["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::32735"}}
    layer = read_vector_file("legacy.geojson", json.dumps(data).encode())
    assert layer.source_crs == "EPSG:32735" and layer.crs_origin == "fichier"
    assert transform_geom(layer.geometries[0], 4326, UTM35S).area == pytest.approx(1_000_000, rel=1e-9)


def test_declared_crs_conflicting_with_file_is_refused(tmp_path):
    path = write_vector(tmp_path / "zones.gpkg", [utm_box(0, 0, 1000, 1000)], "GPKG")
    with pytest.raises(ImportError_, match="différent"):
        read_vector_file("zones.gpkg", path.read_bytes(), declared_crs="EPSG:32736")


def test_shapefile_zip_with_prj(tmp_path):
    layer = read_vector_file("zones.zip", shapefile_zip(tmp_path))
    assert layer.file_format == "shapefile_zip"
    assert transform_geom(layer.geometries[0], 4326, UTM35S).area == pytest.approx(1_000_000, rel=1e-9)


def test_shapefile_without_prj_requires_declared_crs(tmp_path):
    data = shapefile_zip(tmp_path, with_prj=False)
    with pytest.raises(ImportError_, match=r"\.prj"):
        read_vector_file("zones.zip", data)
    layer = read_vector_file("zones.zip", data, declared_crs="EPSG:32735")
    assert layer.crs_origin == "declare"


def test_kml_is_read_as_wgs84(tmp_path):
    path = write_vector(tmp_path / "site.kml", [site_1km()], "KML", crs="EPSG:4326")
    layer = read_vector_file("site.kml", path.read_bytes())
    assert layer.crs_origin == "implicite_kml"
    assert transform_geom(layer.geometries[0], 4326, UTM35S).area == pytest.approx(1_000_000, rel=1e-6)


def test_kmz(tmp_path):
    path = write_vector(tmp_path / "doc.kml", [site_1km()], "KML", crs="EPSG:4326")
    layer = read_vector_file("site.kmz", zip_dir({"doc.kml": path.read_bytes()}))
    assert layer.file_format == "kmz" and len(layer.geometries) == 1


def test_csv_points_need_crs():
    data = "nom;lon;lat\nP1;27,01;-26,5\nP2;27.02;-26.51\n".encode()
    with pytest.raises(ImportError_, match="SCR"):
        read_vector_file("points.csv", data)
    layer = read_vector_file("points.csv", data, declared_crs="EPSG:4326")
    assert [g.geom_type for g in layer.geometries] == ["Point", "Point"]
    assert layer.properties[0] == {"nom": "P1"}


def test_csv_with_non_numeric_coordinate_is_refused():
    with pytest.raises(ImportError_, match="ligne 3"):
        read_vector_file("p.csv", b"lon,lat\n27,-26\nabc,-26\n", declared_crs="EPSG:4326")


def test_invalid_polygon_refused_or_repaired():
    bowtie = Polygon([(27, -26.5), (27.01, -26.51), (27.01, -26.5), (27, -26.51)])
    data = json.dumps(fc(bowtie)).encode()
    with pytest.raises(ImportError_, match="invalide"):
        read_vector_file("x.geojson", data)
    layer = read_vector_file("x.geojson", data, repair=True)
    assert layer.geometries[0].is_valid
    assert any("réparée" in w for w in layer.warnings)


def test_unknown_extension_and_empty_file():
    with pytest.raises(ImportError_, match="Extension"):
        read_vector_file("x.exe", b"MZ")
    with pytest.raises(ImportError_, match="vide"):
        read_vector_file("x.geojson", b"")


def test_zip_path_traversal_refused():
    with pytest.raises(ImportError_, match="chemin dangereux"):
        read_vector_file("evil.zip", zip_dir({"../../etc/zones.shp": b"x"}))


def test_zip_bomb_ratio_refused():
    with pytest.raises(ImportError_, match="compression"):
        read_vector_file("bomb.zip", zip_dir({"a.shp": b"\0" * 5_000_000}))


def test_zip_with_too_many_entries_refused():
    with pytest.raises(ImportError_, match="entrées"):
        read_vector_file("many.zip", zip_dir({f"f{i}.txt": b"x" for i in range(201)}))


def test_null_geometries_skipped_with_warning():
    data = fc(site_1km())
    data["features"].append({"type": "Feature", "geometry": None, "properties": {}})
    layer = read_vector_file("s.geojson", json.dumps(data).encode())
    assert len(layer.geometries) == 1 and layer.skipped_empty == 1


def test_far_from_africa_warns():
    data = json.dumps(fc(Polygon([(2.3, 48.8), (2.31, 48.8), (2.31, 48.81), (2.3, 48.8)]))).encode()
    layer = read_vector_file("paris.geojson", data)
    assert any("hors d'Afrique" in w for w in layer.warnings)
