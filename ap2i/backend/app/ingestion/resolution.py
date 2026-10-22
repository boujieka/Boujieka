"""Project entity resolution (Master prompt §15).

Deterministic matching (automatic):
  * the same source identifier, or an identifier the source itself declares equivalent
    (World Bank P-number <-> IATI 44000-P-number, IATI other-identifier A1);
  * an official parent link (IATI related-activity type 1; World Bank parentprojid for
    Additional Financing) -> the record becomes a financing of the parent's master project.

Probabilistic matching (NEVER automatic): candidate pairs are scored on title similarity,
dates, sector and executing agency, and queued for human review. An accepted candidate is
merged with a reversible ProjectMerge record.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime, timezone

from sqlalchemy import or_, select, update
from sqlalchemy.orm import Session

from app.models import (
    Document,
    FinancingAgreement,
    MatchCandidate,
    Project,
    ProjectAlert,
    ProjectAlias,
    ProjectIdentifier,
    ProjectLocation,
    ProjectMerge,
    ProjectSourceLink,
    ResultsIndicator,
    SourceObservation,
)

STOPWORDS = {
    # en
    "the", "of", "and", "for", "in", "to", "a", "an", "project", "program", "programme", "support", "phase",
    "development", "cameroon", "republic", "additional", "financing", "on", "with", "at", "by", "ii", "iii", "i",
    # fr
    "de", "du", "des", "la", "le", "les", "et", "en", "au", "aux", "pour", "projet", "programme", "appui",
    "developpement", "cameroun", "republique", "d", "l", "un", "une", "sur", "dans", "par",
}
# Minimal bilingual equivalences so FR/EN titles of the same project can be compared.
SYNONYMS = {
    "routier": "road", "route": "road", "routes": "road", "roads": "road", "transports": "transport",
    "eau": "water", "potable": "drinking", "assainissement": "sanitation", "electricite": "electricity",
    "energie": "energy", "electrique": "electricity", "sante": "health", "education": "education",
    "agricole": "agriculture", "agriculture": "agriculture", "rural": "rural", "urbain": "urban", "urbaine": "urban",
    "reseau": "network", "reseaux": "network", "interconnexion": "interconnection", "hydroelectrique": "hydropower",
    "barrage": "dam", "pont": "bridge", "ponts": "bridge", "corridor": "corridor", "secteur": "sector",
    "formation": "training", "professionnelle": "vocational", "competences": "skills",
}
MATCH_THRESHOLD = 0.55


def normalize_title(title: str) -> set[str]:
    t = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode().lower()
    tokens = re.findall(r"[a-z0-9]+", t)
    out = set()
    for tok in tokens:
        if tok in STOPWORDS or len(tok) < 3 and not tok.isdigit():
            continue
        out.add(SYNONYMS.get(tok, tok))
    return out


def title_similarity(a: str, b: str) -> float:
    ta, tb = normalize_title(a), normalize_title(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    # One shared generic word ("education", "road") is weak evidence: require two for full weight.
    return (inter / len(ta | tb)) * min(1.0, inter / 2)


def _ref_date(p: Project) -> date | None:
    return p.original_approval_date or p.implementation_start_date


def score_pair(a: Project, b: Project) -> tuple[float, dict]:
    sim = title_similarity(a.title, b.title)
    for al in a.aliases:
        sim = max(sim, title_similarity(al.alias, b.title))
    for bl in b.aliases:
        sim = max(sim, title_similarity(a.title, bl.alias))
    features: dict = {"title_similarity": round(sim, 3)}
    score = 0.6 * sim
    da, db_ = _ref_date(a), _ref_date(b)
    if da and db_:
        gap = abs((da - db_).days) / 365.25
        features["date_gap_years"] = round(gap, 2)
        score += 0.2 * max(0.0, 1 - gap / 3)
        if gap > 5:
            score *= 0.6  # operations approved years apart are rarely the same project
    else:
        features["date_gap_years"] = None
        score += 0.05
    if a.sector_id and b.sector_id:
        features["same_sector"] = a.sector_id == b.sector_id
        score += 0.1 if a.sector_id == b.sector_id else 0.0
    if a.executing_agency and b.executing_agency:
        ea = normalize_title(a.executing_agency)
        eb = normalize_title(b.executing_agency)
        overlap = len(ea & eb) / len(ea | eb) if ea and eb else 0
        features["agency_overlap"] = round(overlap, 3)
        score += 0.1 * overlap
    return round(min(score, 1.0), 3), features


def find_by_identifiers(db: Session, identifiers: list[str]) -> Project | None:
    ids = [i for i in identifiers if i]
    if not ids:
        return None
    row = db.scalar(select(ProjectIdentifier).where(ProjectIdentifier.identifier.in_(ids)))
    if row is None:
        return None
    project = db.get(Project, row.project_id)
    while project is not None and project.merged_into_id:
        project = db.get(Project, project.merged_into_id)
    return project


def register_identifier(db: Session, project_id: int, scheme: str, identifier: str, source_record_id: int | None) -> None:
    if not identifier:
        return
    exists = db.scalar(select(ProjectIdentifier).where(ProjectIdentifier.scheme == scheme,
                                                       ProjectIdentifier.identifier == identifier))
    if exists is None:
        db.add(ProjectIdentifier(project_id=project_id, scheme=scheme, identifier=identifier,
                                 source_record_id=source_record_id))
        db.flush()


def generate_candidates(db: Session, project_ids: list[int], country_id: int | None = None) -> int:
    """Score new projects against other live projects of the same country; queue pairs >= threshold."""
    created = 0
    for pid in project_ids:
        p = db.get(Project, pid)
        if p is None or p.merged_into_id:
            continue
        partners_p = {a.partner_id for a in p.agreements}
        others = db.scalars(select(Project).where(
            Project.country_id == p.country_id, Project.id != p.id, Project.merged_into_id.is_(None),
            Project.tenant_id.is_(None) if p.tenant_id is None else Project.tenant_id == p.tenant_id,
        )).all()
        for o in others:
            partners_o = {a.partner_id for a in o.agreements}
            # Same partner + different identifiers = different operations of that partner (the
            # deterministic rules already cover the same operation). Only cross-source pairs qualify.
            if partners_p and partners_o and partners_p == partners_o:
                continue
            score, features = score_pair(p, o)
            if score < MATCH_THRESHOLD:
                continue
            a_id, b_id = sorted((p.id, o.id))
            exists = db.scalar(select(MatchCandidate).where(MatchCandidate.project_a_id == a_id,
                                                            MatchCandidate.project_b_id == b_id))
            if exists:
                continue
            db.add(MatchCandidate(project_a_id=a_id, project_b_id=b_id, score=score, features=features))
            created += 1
    db.flush()
    return created


# --- merge / reverse merge -------------------------------------------------------------------

_MOVABLE = [
    ("financing_agreements", FinancingAgreement),
    ("project_source_links", ProjectSourceLink),
    ("project_identifiers", ProjectIdentifier),
    ("project_aliases", ProjectAlias),
    ("documents", Document),
    ("project_locations", ProjectLocation),
    ("results_indicators", ResultsIndicator),
    ("source_observations", SourceObservation),
    ("project_alerts", ProjectAlert),
]


def merge_projects(db: Session, survivor_id: int, merged_id: int, user_id: int | None, reason: str,
                   candidate_id: int | None = None) -> ProjectMerge:
    if survivor_id == merged_id:
        raise ValueError("Cannot merge a project into itself")
    survivor = db.get(Project, survivor_id)
    merged = db.get(Project, merged_id)
    if survivor is None or merged is None:
        raise ValueError("Unknown project")
    if survivor.merged_into_id or merged.merged_into_id:
        raise ValueError("One of the projects is already merged")
    if survivor.country_id != merged.country_id or survivor.tenant_id != merged.tenant_id:
        raise ValueError("Projects from different countries or workspaces cannot be merged")
    moved: dict[str, list[int]] = {}
    for name, model in _MOVABLE:
        ids = list(db.scalars(select(model.id).where(model.project_id == merged_id)))
        if name == "project_aliases":
            # avoid unique-constraint clashes: drop aliases the survivor already has
            have = set(db.scalars(select(ProjectAlias.alias).where(ProjectAlias.project_id == survivor_id)))
            ids = [i for i in ids if db.get(ProjectAlias, i).alias not in have]
        if name == "project_source_links":
            have = set(db.scalars(select(ProjectSourceLink.source_record_id).where(ProjectSourceLink.project_id == survivor_id)))
            ids = [i for i in ids if db.get(ProjectSourceLink, i).source_record_id not in have]
        if ids:
            db.execute(update(model).where(model.id.in_(ids)).values(project_id=survivor_id))
        moved[name] = ids
    if merged.title and merged.title != survivor.title:
        if not db.scalar(select(ProjectAlias).where(ProjectAlias.project_id == survivor_id, ProjectAlias.alias == merged.title)):
            alias = ProjectAlias(project_id=survivor_id, alias=merged.title, language=merged.title_language)
            db.add(alias)
            db.flush()
            moved["created_alias"] = [alias.id]
    merged.merged_into_id = survivor_id
    record = ProjectMerge(survivor_id=survivor_id, merged_id=merged_id, merged_by=user_id, reason=reason,
                          moved=moved, match_candidate_id=candidate_id)
    db.add(record)
    db.flush()
    return record


def reverse_merge(db: Session, merge_id: int, user_id: int | None) -> ProjectMerge:
    record = db.get(ProjectMerge, merge_id)
    if record is None or record.reversed_at is not None:
        raise ValueError("Merge not found or already reversed")
    for name, model in _MOVABLE:
        ids = record.moved.get(name) or []
        if ids:
            db.execute(update(model).where(model.id.in_(ids)).values(project_id=record.merged_id))
    for alias_id in record.moved.get("created_alias") or []:
        alias = db.get(ProjectAlias, alias_id)
        if alias:
            db.delete(alias)
    merged = db.get(Project, record.merged_id)
    merged.merged_into_id = None
    record.reversed_at = datetime.now(timezone.utc)
    record.reversed_by = user_id
    if record.match_candidate_id:
        cand = db.get(MatchCandidate, record.match_candidate_id)
        if cand:
            cand.status = "rejected"
            cand.review_note = (cand.review_note or "") + " | merge reversed"
    db.flush()
    return record


def pending_candidates(db: Session, country_id: int | None = None):
    q = select(MatchCandidate).where(MatchCandidate.status == "pending").order_by(MatchCandidate.score.desc())
    if country_id:
        q = q.join(Project, Project.id == MatchCandidate.project_a_id).where(Project.country_id == country_id)
    return db.scalars(q).all()


__all__ = ["merge_projects", "reverse_merge", "generate_candidates", "find_by_identifiers", "register_identifier",
           "score_pair", "title_similarity", "pending_candidates", "or_"]
