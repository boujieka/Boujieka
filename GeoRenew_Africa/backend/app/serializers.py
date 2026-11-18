"""Conversion des objets en JSON d'API et en exports (GeoJSON, CSV)."""

from __future__ import annotations

import csv
import io
from typing import Any

from shapely.geometry import mapping

from app.models import AnalysisRun, ConstraintRule, Dataset, DatasetVersion, Project, Site

DISCLAIMER = "Screening géospatial indicatif — non bancable, ne remplace pas une étude de faisabilité."
FICTIONAL = "DONNÉES FICTIVES"


def project_out(p: Project) -> dict[str, Any]:
    return {
        "id": p.id,
        "name": p.name,
        "country_iso3": p.country_iso3,
        "technology": p.technology,
        "description": p.description,
        "is_fictional": p.is_fictional,
        "site_count": len(p.sites),
        "dataset_count": len(p.datasets),
        "rule_count": len(p.rules),
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


def version_out(v: DatasetVersion) -> dict[str, Any]:
    return {
        "id": v.id,
        "version_no": v.version_no,
        "sha256": v.sha256,
        "original_filename": v.original_filename,
        "file_format": v.file_format,
        "source_crs": v.source_crs,
        "crs_origin": v.crs_origin,
        "feature_count": v.feature_count,
        "geometry_types": v.geometry_types,
        "bbox": v.bbox,
        "warnings": v.warnings,
        "imported_at": v.imported_at.isoformat() if v.imported_at else None,
    }


def dataset_out(d: Dataset) -> dict[str, Any]:
    return {
        "id": d.id,
        "project_id": d.project_id,
        "name": d.name,
        "category": d.category,
        "nature": d.nature,
        "source_name": d.source_name,
        "source_url": d.source_url,
        "licence": d.licence,
        "producer": d.producer,
        "reference_date": d.reference_date.isoformat() if d.reference_date else None,
        "horizontal_accuracy_m": d.horizontal_accuracy_m,
        "is_synthetic": d.is_synthetic,
        "notes": d.notes,
        "latest_version": version_out(d.latest_version) if d.latest_version else None,
        "version_count": len(d.versions),
    }


def site_out(s: Site) -> dict[str, Any]:
    return {
        "id": s.id,
        "project_id": s.project_id,
        "name": s.name,
        "geometry": mapping(s.boundary),
        "bbox": list(s.boundary.bounds),
        "boundary_source": s.boundary_source,
        "boundary_dataset_version_id": s.boundary_dataset_version_id,
        "boundary_accuracy_m": s.boundary_accuracy_m,
        "land_status": s.land_status,
        "land_evidence_dataset_id": s.land_evidence_dataset_id,
        "grid_status": s.grid_status,
        "grid_evidence_dataset_id": s.grid_evidence_dataset_id,
        "analysis_count": len(s.analyses),
    }


def rule_out(r: ConstraintRule) -> dict[str, Any]:
    return {
        "id": r.id,
        "project_id": r.project_id,
        "dataset_id": r.dataset_id,
        "dataset_name": r.dataset.name if r.dataset else None,
        "name": r.name,
        "kind": r.kind,
        "buffer_m": r.buffer_m,
        "justification_type": r.justification_type,
        "justification": r.justification,
        "weight": r.weight,
        "active": r.active,
    }


def run_out(run: AnalysisRun, reused: bool | None = None) -> dict[str, Any]:
    out = {
        "id": run.id,
        "site_id": run.site_id,
        "created_at": run.created_at.isoformat() if run.created_at else None,
        "status": run.status,
        "input_hash": run.input_hash,
        "software_version": run.software_version,
        "engine_version": run.engine_version,
        "duration_ms": run.duration_ms,
        "actor": run.actor,
        "inputs": run.inputs,
        "results": run.results,
        "layers": [{"id": l.id, "kind": l.kind, "rule_id": l.rule_id, "area_m2": l.area_m2} for l in run.layers],
    }
    if reused is not None:
        out["reused"] = reused
    return out


def run_geojson(run: AnalysisRun) -> dict[str, Any]:
    names = {r["id"]: r["nom"] for r in run.inputs.get("regles", [])}
    fictional = bool(run.results.get("donnees_fictives"))
    features = []
    for l in run.layers:
        features.append(
            {
                "type": "Feature",
                "geometry": mapping(l.geom),
                "properties": {
                    "couche": l.kind,
                    "regle_id": l.rule_id,
                    "regle_nom": names.get(l.rule_id),
                    "surface_m2": l.area_m2,
                    "surface_ha": l.area_m2 / 10_000.0,
                    "nature": "calcule",
                    "analyse_id": run.id,
                },
            }
        )
    return {
        "type": "FeatureCollection",
        "name": f"georenew_analyse_{run.id}",
        "metadata": {
            "analyse_id": run.id,
            "site_id": run.site_id,
            "empreinte_entrees_sha256": run.input_hash,
            "version_logiciel": run.software_version,
            "version_moteur": run.engine_version,
            "date": run.created_at.isoformat() if run.created_at else None,
            "scr_geometries": "EPSG:4326",
            "scr_calcul_surfaces": run.results.get("scr_calcul"),
            "niveau_etude": run.results.get("niveau_etude"),
            "mention": DISCLAIMER,
            "donnees_fictives": FICTIONAL if fictional else None,
        },
        "features": features,
    }


def run_csv(run: AnalysisRun) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["section", "cle", "libelle", "valeur", "unite", "nature", "methode"])
    res = run.results
    meta = [
        ("analyse_id", run.id),
        ("site_id", run.site_id),
        ("date", run.created_at.isoformat() if run.created_at else ""),
        ("empreinte_entrees_sha256", run.input_hash),
        ("version_logiciel", run.software_version),
        ("version_moteur", run.engine_version),
        ("scr_calcul", res.get("scr_calcul")),
        ("niveau_etude", res.get("niveau_etude")),
        ("mention", DISCLAIMER),
        ("donnees_fictives", FICTIONAL if res.get("donnees_fictives") else "non"),
        ("statut_foncier", res.get("statuts", {}).get("foncier_libelle")),
        ("statut_raccordement", res.get("statuts", {}).get("raccordement_libelle")),
    ]
    for k, v in meta:
        w.writerow(["meta", k, "", v, "", "", ""])
    for key, m in res.get("indicateurs", {}).items():
        if "valeur_m2" in m:
            w.writerow(["indicateur", key, "", repr(m["valeur_m2"]), "m2", m["nature"], m["methode"]])
        elif key == "intervalle_surface_nette":
            w.writerow(["indicateur", key + "_bas", "", m["bas_m2"] if m["bas_m2"] is None else repr(m["bas_m2"]), "m2", m["nature"], m["methode"]])
            w.writerow(["indicateur", key + "_haut", "", m["haut_m2"] if m["haut_m2"] is None else repr(m["haut_m2"]), "m2", m["nature"], m["methode"]])
        else:
            v = m.get("valeur")
            w.writerow(["indicateur", key, "", "" if v is None else repr(v), m.get("unite", ""), m["nature"], m["methode"]])
    for r in res.get("par_regle", []):
        area = r.get("surface_dans_zone_amenageable_m2", r.get("surface_dans_surface_nette_m2"))
        w.writerow(["regle", r["regle_id"], r["nom"], repr(area), "m2", "calcule", f"{r['type']} ; buffer {r['buffer_m']:g} m ; {r['justification']}"])
    for c in res.get("controles", []):
        w.writerow(["controle", c["nom"], "", "ok" if c["ok"] else "ECHEC", "", "", c["detail"]])
    for a in res.get("avertissements", []):
        w.writerow(["avertissement", "", "", a, "", "", ""])
    return buf.getvalue()
