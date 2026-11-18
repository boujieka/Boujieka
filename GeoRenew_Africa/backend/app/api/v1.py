"""API REST /api/v1."""

from __future__ import annotations

import datetime as dt
from typing import Annotated, Any
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import Response
from shapely.geometry import mapping
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import __version__
from app.config import get_settings
from app.db import get_db
from app.geo.engine import ENGINE_VERSION
from app.geo.importers import EXTENSIONS, read_vector_file
from app.geo.validation import require_polygonal
from app.models import (
    DATA_NATURES,
    DATASET_CATEGORIES,
    GRID_STATUSES,
    JUSTIFICATION_TYPES,
    LAND_STATUSES,
    RULE_KINDS,
    TECHNOLOGIES,
    AnalysisRun,
    AuditLog,
    ConstraintRule,
    Dataset,
    Project,
    Site,
)
from app.schemas import AnalysisIn, ProjectIn, ProjectPatch, RuleIn, RulePatch, SiteIn, SitePatch
from app.serializers import (
    dataset_out,
    project_out,
    rule_out,
    run_csv,
    run_geojson,
    run_out,
    site_out,
    version_out,
)
from app.services import (
    BusinessError,
    add_dataset_version,
    audit,
    check_rule,
    check_site_statuses,
    run_analysis,
    validate_boundary,
)

router = APIRouter(prefix="/api/v1")
DB = Annotated[Session, Depends(get_db)]
ANONYMOUS = "anonyme (authentification non implémentée)"


def actor(x_actor: Annotated[str | None, Header()] = None) -> str:
    """Identité déclarative pour l'audit. N'EST PAS une authentification (voir docs)."""
    if not x_actor:
        return ANONYMOUS
    return "".join(ch for ch in x_actor if ch.isprintable())[:200] or ANONYMOUS


Actor = Annotated[str, Depends(actor)]


def _get(db: Session, model, obj_id: int, label: str):
    obj = db.get(model, obj_id)
    if obj is None:
        raise HTTPException(404, detail={"code": "introuvable", "message": f"{label} introuvable"})
    return obj


async def _read_upload(file: UploadFile) -> bytes:
    limit = get_settings().max_upload_mb * 1024 * 1024
    data = await file.read(limit + 1)
    if len(data) > limit:
        raise BusinessError(f"Fichier supérieur à {get_settings().max_upload_mb} Mo", "fichier_trop_gros")
    return data


def _check_url(url: str) -> str:
    """URL de source : métadonnée seulement, jamais téléchargée par le serveur (anti-SSRF)."""
    url = url.strip()
    if url and urlparse(url).scheme not in ("http", "https"):
        raise BusinessError("L'URL de source doit commencer par http:// ou https://")
    return url[:1000]


# --- Méta ------------------------------------------------------------------------------------

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__, "moteur": ENGINE_VERSION}


@router.get("/meta")
def meta() -> dict[str, Any]:
    return {
        "version": __version__,
        "engine_version": ENGINE_VERSION,
        "technologies": TECHNOLOGIES,
        "dataset_categories": DATASET_CATEGORIES,
        "data_natures": DATA_NATURES,
        "rule_kinds": RULE_KINDS,
        "justification_types": JUSTIFICATION_TYPES,
        "land_statuses": LAND_STATUSES,
        "grid_statuses": GRID_STATUSES,
        "upload_extensions": sorted(EXTENSIONS),
        "max_upload_mb": get_settings().max_upload_mb,
    }


# --- Projets ---------------------------------------------------------------------------------

@router.get("/projects")
def list_projects(db: DB) -> list[dict[str, Any]]:
    return [project_out(p) for p in db.execute(select(Project).order_by(Project.id)).scalars()]


@router.post("/projects", status_code=201)
def create_project(body: ProjectIn, db: DB, who: Actor) -> dict[str, Any]:
    p = Project(**body.model_dump())
    db.add(p)
    db.flush()
    audit(db, who, "projet.cree", "project", p.id, p.id, nom=p.name)
    db.commit()
    return project_out(p)


@router.get("/projects/{project_id}")
def get_project(project_id: int, db: DB) -> dict[str, Any]:
    return project_out(_get(db, Project, project_id, "Projet"))


@router.patch("/projects/{project_id}")
def patch_project(project_id: int, body: ProjectPatch, db: DB, who: Actor) -> dict[str, Any]:
    p = _get(db, Project, project_id, "Projet")
    changes = body.model_dump(exclude_unset=True)
    for k, v in changes.items():
        setattr(p, k, v)
    audit(db, who, "projet.modifie", "project", p.id, p.id, champs=sorted(changes))
    db.commit()
    return project_out(p)


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: DB, who: Actor) -> Response:
    p = _get(db, Project, project_id, "Projet")
    audit(db, who, "projet.supprime", "project", p.id, p.id, nom=p.name)
    db.delete(p)
    db.commit()
    return Response(status_code=204)


# --- Jeux de données -------------------------------------------------------------------------

def _dataset_form(
    name: str, category: str, nature: str, source_name: str, source_url: str, licence: str, producer: str,
    reference_date: str, horizontal_accuracy_m: str, is_synthetic: bool, notes: str,
) -> dict[str, Any]:
    if category not in DATASET_CATEGORIES:
        raise BusinessError(f"Catégorie inconnue : {category}")
    if nature not in DATA_NATURES:
        raise BusinessError(f"Nature inconnue : {nature}")
    if not name.strip():
        raise BusinessError("Nom du jeu de données obligatoire")
    ref = None
    if reference_date.strip():
        try:
            ref = dt.date.fromisoformat(reference_date.strip())
        except ValueError as exc:
            raise BusinessError("Date de référence au format AAAA-MM-JJ") from exc
    acc = None
    if horizontal_accuracy_m.strip():
        try:
            acc = float(horizontal_accuracy_m.replace(",", "."))
        except ValueError as exc:
            raise BusinessError("Précision horizontale : nombre attendu (mètres)") from exc
        if acc < 0:
            raise BusinessError("Précision horizontale positive attendue")
    return dict(
        name=name.strip()[:200], category=category, nature=nature, source_name=source_name[:300],
        source_url=_check_url(source_url), licence=licence[:300], producer=producer[:300], reference_date=ref,
        horizontal_accuracy_m=acc, is_synthetic=is_synthetic, notes=notes,
    )


@router.get("/projects/{project_id}/datasets")
def list_datasets(project_id: int, db: DB) -> list[dict[str, Any]]:
    _get(db, Project, project_id, "Projet")
    rows = db.execute(select(Dataset).where(Dataset.project_id == project_id).order_by(Dataset.id)).scalars()
    return [dataset_out(d) for d in rows]


@router.post("/projects/{project_id}/datasets", status_code=201)
async def import_dataset(
    project_id: int,
    db: DB,
    who: Actor,
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(...),
    nature: str = Form("inconnue"),
    source_name: str = Form(""),
    source_url: str = Form(""),
    licence: str = Form(""),
    producer: str = Form(""),
    reference_date: str = Form(""),
    horizontal_accuracy_m: str = Form(""),
    is_synthetic: bool = Form(False),
    notes: str = Form(""),
    declared_crs: str = Form(""),
    layer: str = Form(""),
    repair: bool = Form(False),
    x_column: str = Form(""),
    y_column: str = Form(""),
) -> dict[str, Any]:
    project = _get(db, Project, project_id, "Projet")
    fields = _dataset_form(name, category, nature, source_name, source_url, licence, producer,
                           reference_date, horizontal_accuracy_m, is_synthetic, notes)
    data = await _read_upload(file)
    imported = read_vector_file(
        file.filename or "fichier", data, declared_crs=declared_crs or None, layer=layer or None,
        repair=repair, x_column=x_column or None, y_column=y_column or None,
    )
    ds = Dataset(project=project, **fields)
    db.add(ds)
    db.flush()
    v = add_dataset_version(db, ds, file.filename or "fichier", imported)
    audit(db, who, "donnees.importees", "dataset", ds.id, project.id, version=v.version_no, sha256=v.sha256,
          entites=v.feature_count, scr_source=v.source_crs)
    db.commit()
    db.refresh(ds)
    return dataset_out(ds)


@router.post("/datasets/{dataset_id}/versions", status_code=201)
async def add_version(
    dataset_id: int, db: DB, who: Actor, file: UploadFile = File(...), declared_crs: str = Form(""),
    layer: str = Form(""), repair: bool = Form(False), x_column: str = Form(""), y_column: str = Form(""),
) -> dict[str, Any]:
    ds = _get(db, Dataset, dataset_id, "Jeu de données")
    data = await _read_upload(file)
    imported = read_vector_file(file.filename or "fichier", data, declared_crs=declared_crs or None,
                                layer=layer or None, repair=repair, x_column=x_column or None, y_column=y_column or None)
    v = add_dataset_version(db, ds, file.filename or "fichier", imported)
    audit(db, who, "donnees.nouvelle_version", "dataset", ds.id, ds.project_id, version=v.version_no, sha256=v.sha256)
    db.commit()
    return version_out(v)


@router.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int, db: DB) -> dict[str, Any]:
    ds = _get(db, Dataset, dataset_id, "Jeu de données")
    out = dataset_out(ds)
    out["versions"] = [version_out(v) for v in ds.versions]
    return out


@router.get("/datasets/{dataset_id}/geojson")
def dataset_geojson(dataset_id: int, db: DB) -> dict[str, Any]:
    ds = _get(db, Dataset, dataset_id, "Jeu de données")
    v = ds.latest_version
    feats = [] if v is None else [
        {"type": "Feature", "geometry": mapping(f.geom), "properties": {**f.properties, "_index": f.feature_index}}
        for f in v.features
    ]
    return {
        "type": "FeatureCollection",
        "metadata": {"jeu_id": ds.id, "nom": ds.name, "categorie": ds.category, "nature": ds.nature,
                     "fictif": ds.is_synthetic, "version": v.version_no if v else None,
                     "sha256": v.sha256 if v else None, "source": ds.source_name, "licence": ds.licence},
        "features": feats,
    }


@router.delete("/datasets/{dataset_id}", status_code=204)
def delete_dataset(dataset_id: int, db: DB, who: Actor) -> Response:
    ds = _get(db, Dataset, dataset_id, "Jeu de données")
    audit(db, who, "donnees.supprimees", "dataset", ds.id, ds.project_id, nom=ds.name)
    db.delete(ds)
    db.commit()
    return Response(status_code=204)


# --- Sites -----------------------------------------------------------------------------------

@router.get("/projects/{project_id}/sites")
def list_sites(project_id: int, db: DB) -> list[dict[str, Any]]:
    _get(db, Project, project_id, "Projet")
    return [site_out(s) for s in db.execute(select(Site).where(Site.project_id == project_id).order_by(Site.id)).scalars()]


@router.post("/projects/{project_id}/sites", status_code=201)
def create_site(project_id: int, body: SiteIn, db: DB, who: Actor) -> dict[str, Any]:
    project = _get(db, Project, project_id, "Projet")
    geom, warnings = validate_boundary(body.geometry, repair=body.repair)
    s = Site(project=project, name=body.name, boundary=geom, boundary_source=body.boundary_source,
             boundary_accuracy_m=body.boundary_accuracy_m)
    db.add(s)
    db.flush()
    audit(db, who, "site.cree", "site", s.id, project.id, source=body.boundary_source, avertissements=warnings)
    db.commit()
    out = site_out(s)
    out["warnings"] = warnings
    return out


@router.post("/projects/{project_id}/sites/import", status_code=201)
async def import_sites(
    project_id: int, db: DB, who: Actor, file: UploadFile = File(...), name: str = Form(...),
    name_field: str = Form(""), nature: str = Form("inconnue"), source_name: str = Form(""),
    source_url: str = Form(""), licence: str = Form(""), producer: str = Form(""),
    reference_date: str = Form(""), horizontal_accuracy_m: str = Form(""), is_synthetic: bool = Form(False),
    notes: str = Form(""), declared_crs: str = Form(""), layer: str = Form(""), repair: bool = Form(False),
) -> dict[str, Any]:
    """Importe un fichier de limites : un site par polygone, provenance conservée."""
    project = _get(db, Project, project_id, "Projet")
    fields = _dataset_form(name, "limite_site", nature, source_name, source_url, licence, producer,
                           reference_date, horizontal_accuracy_m, is_synthetic, notes)
    data = await _read_upload(file)
    imported = read_vector_file(file.filename or "fichier", data, declared_crs=declared_crs or None,
                                layer=layer or None, repair=repair)
    polys = [require_polygonal(g, f"Entité n° {i + 1}") for i, g in enumerate(imported.geometries)]
    ds = Dataset(project=project, **fields)
    db.add(ds)
    db.flush()
    v = add_dataset_version(db, ds, file.filename or "fichier", imported)
    sites = []
    for i, (g, props) in enumerate(zip(polys, imported.properties)):
        label = str(props.get(name_field) or "").strip() if name_field else ""
        s = Site(project=project, name=(label or f"{ds.name} — site {i + 1}")[:200], boundary=g,
                 boundary_dataset_version_id=v.id, boundary_source=f"Import « {ds.name} » v{v.version_no}",
                 boundary_accuracy_m=ds.horizontal_accuracy_m)
        db.add(s)
        sites.append(s)
    db.flush()
    audit(db, who, "sites.importes", "dataset", ds.id, project.id, sites=[s.id for s in sites], sha256=v.sha256)
    db.commit()
    return {"dataset": dataset_out(ds), "sites": [site_out(s) for s in sites], "warnings": imported.warnings}


@router.get("/sites/{site_id}")
def get_site(site_id: int, db: DB) -> dict[str, Any]:
    return site_out(_get(db, Site, site_id, "Site"))


@router.patch("/sites/{site_id}")
def patch_site(site_id: int, body: SitePatch, db: DB, who: Actor) -> dict[str, Any]:
    s = _get(db, Site, site_id, "Site")
    changes = body.model_dump(exclude_unset=True)
    warnings: list[str] = []
    if "geometry" in changes:
        geom, warnings = validate_boundary(changes.pop("geometry"))
        s.boundary = geom
        s.boundary_dataset_version_id = None
        if "boundary_source" not in changes:
            s.boundary_source = "Tracé manuel dans l'interface (modifié)"
    for k, v in changes.items():
        setattr(s, k, v)
    check_site_statuses(db, s)
    audit(db, who, "site.modifie", "site", s.id, s.project_id, champs=sorted(body.model_dump(exclude_unset=True)))
    db.commit()
    out = site_out(s)
    out["warnings"] = warnings
    return out


@router.delete("/sites/{site_id}", status_code=204)
def delete_site(site_id: int, db: DB, who: Actor) -> Response:
    s = _get(db, Site, site_id, "Site")
    audit(db, who, "site.supprime", "site", s.id, s.project_id, nom=s.name)
    db.delete(s)
    db.commit()
    return Response(status_code=204)


@router.get("/projects/{project_id}/sites.geojson")
def sites_geojson(project_id: int, db: DB) -> dict[str, Any]:
    p = _get(db, Project, project_id, "Projet")
    return {
        "type": "FeatureCollection",
        "metadata": {"projet_id": p.id, "projet": p.name, "fictif": p.is_fictional, "scr": "EPSG:4326"},
        "features": [
            {"type": "Feature", "geometry": mapping(s.boundary),
             "properties": {"site_id": s.id, "nom": s.name, "source_limite": s.boundary_source,
                            "statut_foncier": s.land_status, "statut_raccordement": s.grid_status}}
            for s in p.sites
        ],
    }


# --- Règles ----------------------------------------------------------------------------------

@router.get("/projects/{project_id}/constraints")
def list_rules(project_id: int, db: DB) -> list[dict[str, Any]]:
    _get(db, Project, project_id, "Projet")
    rows = db.execute(select(ConstraintRule).where(ConstraintRule.project_id == project_id).order_by(ConstraintRule.id)).scalars()
    return [rule_out(r) for r in rows]


@router.post("/projects/{project_id}/constraints", status_code=201)
def create_rule(project_id: int, body: RuleIn, db: DB, who: Actor) -> dict[str, Any]:
    _get(db, Project, project_id, "Projet")
    r = ConstraintRule(project_id=project_id, **body.model_dump())
    check_rule(db, project_id, r)
    db.add(r)
    db.flush()
    audit(db, who, "regle.creee", "constraint_rule", r.id, project_id, **body.model_dump())
    db.commit()
    return rule_out(r)


@router.patch("/constraints/{rule_id}")
def patch_rule(rule_id: int, body: RulePatch, db: DB, who: Actor) -> dict[str, Any]:
    r = _get(db, ConstraintRule, rule_id, "Règle")
    changes = body.model_dump(exclude_unset=True)
    before = {k: getattr(r, k) for k in changes}
    for k, v in changes.items():
        setattr(r, k, v)
    check_rule(db, r.project_id, r)
    audit(db, who, "regle.modifiee", "constraint_rule", r.id, r.project_id, avant=before, apres=changes)
    db.commit()
    return rule_out(r)


@router.delete("/constraints/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: DB, who: Actor) -> Response:
    r = _get(db, ConstraintRule, rule_id, "Règle")
    audit(db, who, "regle.supprimee", "constraint_rule", r.id, r.project_id, nom=r.name)
    db.delete(r)
    db.commit()
    return Response(status_code=204)


# --- Analyses --------------------------------------------------------------------------------

@router.post("/sites/{site_id}/analyses")
def create_analysis(site_id: int, body: AnalysisIn, db: DB, who: Actor, response: Response) -> dict[str, Any]:
    site = _get(db, Site, site_id, "Site")
    run, reused = run_analysis(
        db, site, setback_m=body.setback_m, setback_justification=body.setback_justification,
        rule_ids=body.rule_ids, density_mwp_dc_per_ha=body.density_mwp_dc_per_ha,
        density_justification=body.density_justification, force=body.force, actor=who,
    )
    db.commit()
    response.status_code = 200 if reused else 201
    return run_out(run, reused)


@router.get("/sites/{site_id}/analyses")
def list_analyses(site_id: int, db: DB) -> list[dict[str, Any]]:
    _get(db, Site, site_id, "Site")
    rows = db.execute(select(AnalysisRun).where(AnalysisRun.site_id == site_id).order_by(AnalysisRun.id.desc())).scalars()
    return [
        {"id": r.id, "created_at": r.created_at.isoformat() if r.created_at else None, "input_hash": r.input_hash,
         "surface_nette_ha": r.results["indicateurs"]["surface_nette"]["valeur_ha"],
         "recul_m": r.inputs["parametres"]["recul_m"], "regles": len(r.inputs["regles"]),
         "donnees_fictives": r.results.get("donnees_fictives", False)}
        for r in rows
    ]


@router.get("/analyses/{run_id}")
def get_analysis(run_id: int, db: DB) -> dict[str, Any]:
    return run_out(_get(db, AnalysisRun, run_id, "Analyse"))


@router.get("/analyses/{run_id}/geojson")
def analysis_geojson(run_id: int, db: DB) -> Response:
    import json

    run = _get(db, AnalysisRun, run_id, "Analyse")
    body = json.dumps(run_geojson(run), ensure_ascii=False)
    return Response(body, media_type="application/geo+json",
                    headers={"Content-Disposition": f'attachment; filename="georenew_analyse_{run.id}.geojson"'})


@router.get("/analyses/{run_id}/csv")
def analysis_csv(run_id: int, db: DB) -> Response:
    run = _get(db, AnalysisRun, run_id, "Analyse")
    return Response("﻿" + run_csv(run), media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="georenew_analyse_{run.id}.csv"'})


# --- Audit -----------------------------------------------------------------------------------

@router.get("/audit-log")
def audit_log(db: DB, project_id: int | None = None, limit: int = 200) -> list[dict[str, Any]]:
    q = select(AuditLog).order_by(AuditLog.id.desc()).limit(min(max(limit, 1), 1000))
    if project_id is not None:
        q = q.where(AuditLog.project_id == project_id)
    return [
        {"id": a.id, "at": a.at.isoformat() if a.at else None, "actor": a.actor, "action": a.action,
         "entity_type": a.entity_type, "entity_id": a.entity_id, "project_id": a.project_id, "details": a.details}
        for a in db.execute(q).scalars()
    ]
