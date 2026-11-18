"""Logique applicative : import, sites, règles, analyses, audit."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import time
from typing import Any

import shapely
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import __version__
from app.geo.engine import ENGINE_VERSION, RuleInput, ScreeningParams, screen_site
from app.geo.importers import ImportedLayer
from app.geo.validation import (
    GeometryError,
    check_lonlat_range,
    clean_geometry,
    outside_africa,
    require_polygonal,
)
from app.models import (
    GRID_EVIDENCE,
    LAND_EVIDENCE,
    AnalysisRun,
    AuditLog,
    ConstraintRule,
    Dataset,
    DatasetVersion,
    Feature,
    Layer,
    Project,
    Site,
)


class BusinessError(ValueError):
    """Requête refusée pour une raison métier ; message destiné à l'utilisateur."""

    def __init__(self, message: str, code: str = "regle_metier"):
        super().__init__(message)
        self.code = code


def audit(db: Session, actor: str, action: str, entity_type: str, entity_id: int | None, project_id: int | None, **details: Any) -> None:
    db.add(
        AuditLog(
            actor=actor,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            project_id=project_id,
            details=details,
        )
    )


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def geom_sha256(geom: BaseGeometry) -> str:
    return hashlib.sha256(shapely.to_wkb(geom)).hexdigest()


# --- Jeux de données -------------------------------------------------------------------------

def add_dataset_version(db: Session, dataset: Dataset, filename: str, layer: ImportedLayer) -> DatasetVersion:
    no = (dataset.latest_version.version_no + 1) if dataset.latest_version else 1
    version = DatasetVersion(
        dataset=dataset,
        version_no=no,
        sha256=layer.sha256,
        original_filename=filename[:300],
        file_format=layer.file_format,
        source_crs=layer.source_crs,
        crs_origin=layer.crs_origin,
        feature_count=len(layer.geometries),
        geometry_types=layer.geometry_types,
        bbox=layer.bbox,
        warnings=layer.warnings,
    )
    version.features = [
        Feature(feature_index=i, geom=g, properties=p) for i, (g, p) in enumerate(zip(layer.geometries, layer.properties))
    ]
    db.add(version)
    db.flush()
    return version


def version_geometries(db: Session, version_id: int) -> list[BaseGeometry]:
    rows = db.execute(
        select(Feature.geom).where(Feature.dataset_version_id == version_id).order_by(Feature.feature_index)
    ).scalars()
    return list(rows)


# --- Sites -----------------------------------------------------------------------------------

def validate_boundary(geojson_geometry: dict[str, Any], *, repair: bool = False) -> tuple[BaseGeometry, list[str]]:
    try:
        geom = shape(geojson_geometry)
    except Exception as exc:
        raise GeometryError(f"Géométrie GeoJSON illisible : {exc}") from exc
    geom, warnings = clean_geometry(geom, repair=repair, label="Limite de site")
    check_lonlat_range(geom)
    poly = require_polygonal(geom, "Limite de site")
    if outside_africa(poly):
        warnings.append("Site entièrement hors d'Afrique : vérifier l'ordre des axes (lon, lat)")
    return poly, warnings


def check_site_statuses(db: Session, site: Site) -> None:
    """Un statut « vérifié/confirmé » exige une pièce du bon type, non fictive, du même projet."""

    def _evidence(dataset_id: int | None, allowed: tuple[str, ...], label: str) -> None:
        if dataset_id is None:
            raise BusinessError(f"{label} : pièce justificative obligatoire (jeu de données de type {', '.join(allowed)})", "piece_manquante")
        ds = db.get(Dataset, dataset_id)
        if ds is None or ds.project_id != site.project_id:
            raise BusinessError(f"{label} : pièce introuvable dans ce projet", "piece_invalide")
        if ds.category not in allowed:
            raise BusinessError(f"{label} : la pièce doit être de type {', '.join(allowed)} (reçu {ds.category})", "piece_invalide")
        if ds.is_synthetic:
            raise BusinessError(f"{label} : une donnée fictive ne peut pas servir de preuve", "piece_fictive")

    if site.land_status == "verifie_sur_piece":
        _evidence(site.land_evidence_dataset_id, LAND_EVIDENCE, "Foncier vérifié")
    if site.grid_status == "raccordement_confirme":
        _evidence(site.grid_evidence_dataset_id, GRID_EVIDENCE, "Raccordement confirmé")


LAND_LABELS = {
    "inconnu": "Foncier : inconnu (aucune pièce foncière)",
    "declare_non_verifie": "Foncier : déclaré, non vérifié",
    "verifie_sur_piece": "Foncier : vérifié sur pièce fournie par l'utilisateur",
}
GRID_LABELS = {
    "inconnu": "Raccordement : inconnu (aucune étude réseau)",
    "etude_en_cours": "Raccordement : étude en cours, non confirmé",
    "raccordement_confirme": "Raccordement : confirmé sur pièce fournie par l'utilisateur",
}


# --- Règles ----------------------------------------------------------------------------------

def check_rule(db: Session, project_id: int, rule: ConstraintRule) -> None:
    ds = db.get(Dataset, rule.dataset_id)
    if ds is None or ds.project_id != project_id:
        raise BusinessError("Le jeu de données de la règle doit appartenir au même projet", "isolation_projet")
    if rule.buffer_m < 0:
        raise BusinessError("Le buffer doit être positif ou nul")
    if rule.buffer_m > 0 and rule.justification_type == "aucun_buffer":
        raise BusinessError("Un buffer non nul exige une justification (hypothèse, texte cité, norme ou étude)", "justification_manquante")
    if rule.justification_type != "aucun_buffer" and not rule.justification.strip():
        raise BusinessError("Préciser la justification ou la référence du buffer", "justification_manquante")


# --- Analyses --------------------------------------------------------------------------------

def run_analysis(
    db: Session,
    site: Site,
    *,
    setback_m: float,
    setback_justification: str,
    rule_ids: list[int] | None,
    density_mwp_dc_per_ha: float | None,
    density_justification: str,
    force: bool,
    actor: str,
) -> tuple[AnalysisRun, bool]:
    if setback_m < 0:
        raise BusinessError("Le recul doit être positif ou nul")
    if setback_m > 0 and not setback_justification.strip():
        raise BusinessError("Un recul non nul exige une justification", "justification_manquante")
    if density_mwp_dc_per_ha is not None:
        if density_mwp_dc_per_ha <= 0:
            raise BusinessError("La densité de puissance doit être strictement positive")
        if not density_justification.strip():
            raise BusinessError("La densité de puissance est une hypothèse : la justifier", "justification_manquante")

    project_rules = db.execute(
        select(ConstraintRule).where(ConstraintRule.project_id == site.project_id).order_by(ConstraintRule.id)
    ).scalars().all()
    if rule_ids is None:
        rules = [r for r in project_rules if r.active]
    else:
        by_id = {r.id: r for r in project_rules}
        unknown = [i for i in rule_ids if i not in by_id]
        if unknown:
            raise BusinessError(f"Règles inconnues dans ce projet : {unknown}", "isolation_projet")
        rules = [by_id[i] for i in sorted(set(rule_ids))]

    engine_rules: list[RuleInput] = []
    rule_snap: list[dict[str, Any]] = []
    synthetic = site.project.is_fictional
    for r in rules:
        ds = r.dataset
        v = ds.latest_version
        if v is None:
            raise BusinessError(f"Règle « {r.name} » : le jeu de données n'a aucune version importée")
        synthetic = synthetic or ds.is_synthetic
        ref = {
            "jeu_id": ds.id,
            "jeu_nom": ds.name,
            "version_id": v.id,
            "version_no": v.version_no,
            "sha256": v.sha256,
            "source": ds.source_name,
            "licence": ds.licence,
            "date_reference": ds.reference_date.isoformat() if ds.reference_date else None,
            "nature": ds.nature,
            "fictif": ds.is_synthetic,
            "precision_m": ds.horizontal_accuracy_m,
        }
        rule_snap.append(
            {
                "id": r.id,
                "nom": r.name,
                "type": r.kind,
                "buffer_m": r.buffer_m,
                "justification_type": r.justification_type,
                "justification": r.justification,
                "donnees": ref,
            }
        )
        engine_rules.append(
            RuleInput(
                rule_id=r.id,
                name=r.name,
                kind=r.kind,
                buffer_m=r.buffer_m,
                geometries=tuple(version_geometries(db, v.id)),
                accuracy_m=ds.horizontal_accuracy_m,
                justification=f"{r.justification_type} : {r.justification}".strip(" :"),
                reference=ref,
            )
        )

    inputs = {
        "version_moteur": ENGINE_VERSION,
        "site": {
            "id": site.id,
            "limite_sha256_wkb": geom_sha256(site.boundary),
            "limite_source": site.boundary_source,
            "limite_precision_m": site.boundary_accuracy_m,
            "statut_foncier": site.land_status,
            "statut_raccordement": site.grid_status,
        },
        "parametres": {
            "recul_m": setback_m,
            "recul_justification": setback_justification,
            "densite_mwp_dc_par_ha": density_mwp_dc_per_ha,
            "densite_justification": density_justification,
        },
        "regles": rule_snap,
        "donnees_fictives": synthetic,
    }
    input_hash = sha256_json(inputs)

    if not force:
        existing = db.execute(
            select(AnalysisRun).where(AnalysisRun.site_id == site.id, AnalysisRun.input_hash == input_hash).order_by(AnalysisRun.id)
        ).scalars().first()
        if existing is not None:
            return existing, True

    t0 = time.perf_counter()
    result = screen_site(
        site.boundary,
        ScreeningParams(
            setback_m=setback_m,
            setback_justification=setback_justification,
            boundary_accuracy_m=site.boundary_accuracy_m,
            density_mwp_dc_per_ha=density_mwp_dc_per_ha,
            density_justification=density_justification,
        ),
        engine_rules,
    )
    duration = int((time.perf_counter() - t0) * 1000)
    results = result.as_dict()
    results["statuts"] = {
        "foncier": site.land_status,
        "foncier_libelle": LAND_LABELS[site.land_status],
        "raccordement": site.grid_status,
        "raccordement_libelle": GRID_LABELS[site.grid_status],
        "capacite_reseau": "Non évaluée : aucune conclusion sur la capacité d'accueil sans étude du gestionnaire de réseau.",
    }
    results["donnees_fictives"] = synthetic
    results["parametres"] = inputs["parametres"]

    run = AnalysisRun(
        site=site,
        input_hash=input_hash,
        inputs=inputs,
        results=results,
        software_version=__version__,
        engine_version=ENGINE_VERSION,
        duration_ms=duration,
        actor=actor,
    )
    run.layers = [Layer(kind=k, rule_id=rid, geom=g, area_m2=a) for k, rid, g, a in result.layers]
    db.add(run)
    db.flush()
    audit(db, actor, "analyse.executee", "analysis_run", run.id, site.project_id, site_id=site.id, input_hash=input_hash, force=force)
    return run, False


def now_iso() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def project_or_404(db: Session, project_id: int) -> Project:
    p = db.get(Project, project_id)
    if p is None:
        raise LookupError("Projet introuvable")
    return p
