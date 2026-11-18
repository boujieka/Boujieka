"""Projet de démonstration — DONNÉES FICTIVES.

Les géométries de ``examples/demo_fictive/`` sont inventées pour la démonstration : elles ne
représentent aucun site, aucune zone humide, aucune route ni aucune pente réelle. Elles sont
générées par ``python -m app.demo generate`` (construction en UTM 35S) et chargées par
``python -m app.demo load`` via le même pipeline d'import que les fichiers utilisateur.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from shapely.geometry import LineString, Polygon, box, mapping
from sqlalchemy import select

from app.db import SessionLocal
from app.geo.crs import transform_geom
from app.geo.importers import read_vector_file
from app.models import ConstraintRule, Dataset, Project, Site
from app.services import add_dataset_version, audit

DEMO_DIR = Path(__file__).resolve().parents[2] / "examples" / "demo_fictive"
PROJECT_NAME = "DÉMO — Projet PV fictif"
EPSG = 32735
X0, Y0 = 520_000.0, 7_060_000.0
SOURCE = "Généré par app/demo.py — DONNÉES FICTIVES, aucune valeur réelle"


def _ll(g):
    return transform_geom(g, EPSG, 4326)


def _fc(items):
    return {
        "type": "FeatureCollection",
        "name": "DONNEES_FICTIVES",
        "features": [{"type": "Feature", "geometry": mapping(_ll(g)), "properties": p} for g, p in items],
    }


def generate() -> None:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    site_a = Polygon([(X0, Y0), (X0 + 1800, Y0 + 100), (X0 + 1700, Y0 + 1300), (X0 + 200, Y0 + 1400)])
    site_b = box(X0 + 2500, Y0 + 200, X0 + 3300, Y0 + 900)
    files = {
        "sites_FICTIFS.geojson": [(site_a, {"nom": "Parcelle A (fictive)"}), (site_b, {"nom": "Parcelle B (fictive)"})],
        "zones_humides_FICTIVES.geojson": [
            (box(X0 + 300, Y0 + 300, X0 + 700, Y0 + 650), {"nom": "Zone humide fictive 1"}),
            (box(X0 + 550, Y0 + 500, X0 + 900, Y0 + 850), {"nom": "Zone humide fictive 2 (chevauche 1)"}),
        ],
        "route_FICTIVE.geojson": [
            (LineString([(X0 - 200, Y0 + 1000), (X0 + 1000, Y0 + 900), (X0 + 3600, Y0 + 700)]), {"nom": "Route fictive"})
        ],
        "pente_indicative_FICTIVE.geojson": [
            (box(X0 + 1200, Y0 + 200, X0 + 1800, Y0 + 800), {"classe": "pente > seuil (fictif)"})
        ],
    }
    for name, items in files.items():
        (DEMO_DIR / name).write_text(json.dumps(_fc(items), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("écrit", DEMO_DIR / name)


def _dataset(db, project, filename, name, category):
    data = (DEMO_DIR / filename).read_bytes()
    layer = read_vector_file(filename, data)
    ds = Dataset(project=project, name=name, category=category, nature="hypothese", source_name=SOURCE,
                 licence="Exemple fourni avec GeoRenew Africa", is_synthetic=True,
                 notes="DONNÉES FICTIVES — ne pas utiliser pour une décision")
    db.add(ds)
    db.flush()
    return ds, add_dataset_version(db, ds, filename, layer), layer


def load() -> None:
    actor = "chargement démo"
    with SessionLocal() as db:
        if db.execute(select(Project).where(Project.name == PROJECT_NAME)).scalar_one_or_none():
            print("Projet de démonstration déjà présent : rien à faire.")
            return
        p = Project(name=PROJECT_NAME, country_iso3="ZAF", technology="pv", is_fictional=True,
                    description="Démonstration du screening P1. DONNÉES FICTIVES : aucun site, réseau ni contrainte réels.")
        db.add(p)
        db.flush()
        ds, v, layer = _dataset(db, p, "sites_FICTIFS.geojson", "Limites de parcelles (fictives)", "limite_site")
        for g, props in zip(layer.geometries, layer.properties):
            db.add(Site(project=p, name=props["nom"], boundary=g, boundary_dataset_version_id=v.id,
                        boundary_source=f"Import « {ds.name} » v1"))
        wet, _, _ = _dataset(db, p, "zones_humides_FICTIVES.geojson", "Zones humides (fictives)", "exclusion")
        road, _, _ = _dataset(db, p, "route_FICTIVE.geojson", "Route (fictive)", "exclusion")
        slope, _, _ = _dataset(db, p, "pente_indicative_FICTIVE.geojson", "Pente indicative (fictive)", "contrainte")
        db.add_all([
            ConstraintRule(project=p, dataset=wet, name="Zones humides", kind="exclusion_stricte", buffer_m=30,
                           justification_type="hypothese_utilisateur",
                           justification="Hypothèse de démonstration, aucune valeur réglementaire"),
            ConstraintRule(project=p, dataset=road, name="Emprise et recul route", kind="exclusion_stricte", buffer_m=40,
                           justification_type="hypothese_utilisateur",
                           justification="Hypothèse de démonstration, aucune valeur réglementaire"),
            ConstraintRule(project=p, dataset=slope, name="Pente à vérifier", kind="contrainte_indicative",
                           buffer_m=0, justification_type="aucun_buffer", justification=""),
        ])
        db.flush()
        audit(db, actor, "demo.chargee", "project", p.id, p.id)
        db.commit()
        print(f"Projet de démonstration créé (id {p.id}) — DONNÉES FICTIVES.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "load"
    {"generate": generate, "load": load}[cmd]()
