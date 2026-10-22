import json

from sqlalchemy import select

import app.models as m
from app.publish.snapshot import export_public_snapshot


def test_public_snapshot_reconciles_and_excludes_private_data(loaded, client, tmp_path):
    db = loaded
    cid = db.scalar(select(m.Country.id).where(m.Country.iso3 == "CMR"))
    org = m.Organization(name="SYNTHETIC ministry", short_name="SYN")
    db.add(org)
    db.flush()
    db.add(m.Project(ap2i_id="AP2I-CMR-HEALTH-990001", country_id=cid, title="SYNTHETIC confidential hospital", status="active",
                     tenant_id=org.id))
    db.commit()

    out = export_public_snapshot(db, tmp_path, ["CMR"], client=client)
    assert all(r["ok"] for r in out["reconciliation"]), out["reconciliation"]
    data = tmp_path / "data"
    projects = json.loads((data / "projects.json").read_text())
    refs = {p["ref"] for p in projects}
    assert "AP2I-CMR-HEALTH-990001" not in refs  # tenant-private project never published
    assert not (data / "p" / "AP2I-CMR-HEALTH-990001.json").exists()
    assert "confidential" not in (data / "alerts.json").read_text()
    public = {p.ap2i_id for p in db.scalars(select(m.Project).where(m.Project.tenant_id.is_(None), m.Project.merged_into_id.is_(None),
                                                                   m.Project.country_id == cid))}
    assert refs == public
    for ref in refs:
        detail = json.loads((data / "p" / f"{ref}.json").read_text())
        assert detail["observations"] is None  # plan-gated field provenance is not exported
    meta = json.loads((data / "meta.json").read_text())
    assert meta["counts"]["projects"] == len(refs) and len(meta["checksum"]) == 64
    flows = json.loads((data / "flows.json").read_text())
    assert len(flows["kind"]) == len(flows["usd"]) == len(flows["year"])
