from sqlalchemy import select

import app.models as m
from app.ingestion.resolution import generate_candidates, merge_projects, reverse_merge, title_similarity


def _project(db, title, approval=None, ap2i="AP2I-CMR-TRANSPORT-90000", partner="WB", ident=None):
    from datetime import date

    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    p = m.Project(ap2i_id=ap2i, country_id=cid, title=title, status="active", original_approval_date=date.fromisoformat(approval) if approval else None)
    db.add(p)
    db.flush()
    pid = db.scalar(select(m.FinancingPartner.id).where(m.FinancingPartner.code == partner))
    db.add(m.FinancingAgreement(project_id=p.id, partner_id=pid, source_identifier=ident or ap2i))
    db.add(m.ProjectAlias(project_id=p.id, alias=title + " (alias)"))
    db.commit()
    return p


def test_title_similarity_bilingual_and_generic_words():
    assert title_similarity("Cameroon - Kribi Gas Power Project", "Kribi Gas Power Project") == 1.0
    assert title_similarity("Projet routier Yaoundé-Douala", "Yaounde-Douala road project") > 0.6
    assert title_similarity("Education Project", "Education II Project") < 0.6  # a single generic word is weak evidence


def test_probabilistic_candidates_are_never_auto_merged(db):
    a = _project(db, "SYNTHETIC Kribi Gas Power Project", "2012-05-01", "AP2I-CMR-ENERGY-900001", "WB")
    b = _project(db, "Cameroon - SYNTHETIC Kribi Gas Power Project", "2012-09-01", "AP2I-CMR-ENERGY-900002", "AFDB")
    n = generate_candidates(db, [b.id])
    db.commit()
    assert n == 1
    cand = db.scalar(select(m.MatchCandidate))
    assert cand.status == "pending" and cand.score >= 0.55
    assert db.get(m.Project, a.id).merged_into_id is None and db.get(m.Project, b.id).merged_into_id is None


def test_same_partner_different_operations_not_candidates(db):
    _project(db, "SYNTHETIC Road Sector Project", "2015-01-01", "AP2I-CMR-TRANSPORT-900003", "WB")
    b = _project(db, "SYNTHETIC Road Sector Project", "2015-03-01", "AP2I-CMR-TRANSPORT-900004", "WB")
    assert generate_candidates(db, [b.id]) == 0


def test_merge_and_reverse_restore_everything(db):
    a = _project(db, "SYNTHETIC Garoua water", "2019-01-01", "AP2I-CMR-WATER-900005", "AFD")
    b = _project(db, "SYNTHETIC Garoua drinking water", "2019-02-01", "AP2I-CMR-WATER-900006", "WB")
    before_b = sorted(x.id for x in b.agreements)
    mg = merge_projects(db, a.id, b.id, None, "test")
    db.commit()
    assert db.get(m.Project, b.id).merged_into_id == a.id
    assert len(db.scalars(select(m.FinancingAgreement).where(m.FinancingAgreement.project_id == a.id)).all()) == 2
    reverse_merge(db, mg.id, None)
    db.commit()
    db.expire_all()
    assert db.get(m.Project, b.id).merged_into_id is None
    assert sorted(x.id for x in db.scalars(select(m.FinancingAgreement).where(m.FinancingAgreement.project_id == b.id))) == before_b
    assert db.get(m.ProjectMerge, mg.id).reversed_at is not None
