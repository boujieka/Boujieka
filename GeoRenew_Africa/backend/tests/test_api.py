"""Tests d'intégration de l'API : critères d'acceptation P1 (PROMPT_CLAUDE_CODE.md §V)."""

import csv
import io
import json

import pytest
from shapely.geometry import LineString, mapping

from app.config import get_settings
from tests.helpers import X0, Y0, fc, ll, site_1km, utm_box


def new_project(client, **kw):
    body = {"name": "Projet test", "country_iso3": "zaf", "technology": "pv", **kw}
    r = client.post("/api/v1/projects", json=body)
    assert r.status_code == 201, r.text
    return r.json()


def upload(client, project_id, geojson, name, category="exclusion", path="datasets", **form):
    files = {"file": (f"{name}.geojson", json.dumps(geojson).encode(), "application/geo+json")}
    data = {"name": name, "category": category, **{k: str(v) for k, v in form.items()}}
    if path != "datasets":
        data.pop("category")
    return client.post(f"/api/v1/projects/{project_id}/{path}", files=files, data=data)


def add_rule(client, project_id, dataset_id, **kw):
    body = {"name": "Règle", "dataset_id": dataset_id, "kind": "exclusion_stricte", **kw}
    return client.post(f"/api/v1/projects/{project_id}/constraints", json=body)


def analyse(client, site_id, **kw):
    return client.post(f"/api/v1/sites/{site_id}/analyses", json=kw)


@pytest.fixture
def setup(client):
    """Projet, un site dessiné de 1 km² et deux exclusions qui se chevauchent."""
    p = new_project(client)
    s = client.post(f"/api/v1/projects/{p['id']}/sites", json={"name": "Site A", "geometry": mapping(site_1km())})
    assert s.status_code == 201, s.text
    a = ll(utm_box(100, 100, 300, 300))
    b = ll(utm_box(200, 200, 400, 400))
    d = upload(client, p["id"], fc(a, b), "Zones humides", nature="observee", source_name="Relevé test",
               licence="CC-BY-4.0", reference_date="2026-01-15")
    assert d.status_code == 201, d.text
    r = add_rule(client, p["id"], d.json()["id"], name="Zones humides")
    assert r.status_code == 201, r.text
    return {"project": p, "site": s.json(), "dataset": d.json(), "rule": r.json()}


def net_ha(run):
    return run["results"]["indicateurs"]["surface_nette"]["valeur_ha"]


def test_health_and_meta(client):
    assert client.get("/api/v1/health").json()["status"] == "ok"
    meta = client.get("/api/v1/meta").json()
    assert "exclusion_stricte" in meta["rule_kinds"] and ".gpkg" in meta["upload_extensions"]


def test_acceptance_scenario(client, setup):
    site_id = setup["site"]["id"]
    r = analyse(client, site_id, setback_m=50, setback_justification="Hypothèse utilisateur à confirmer")
    assert r.status_code == 201, r.text
    run = r.json()
    ind = run["results"]["indicateurs"]
    assert ind["surface_brute"]["valeur_ha"] == pytest.approx(100, rel=1e-9)
    # exclusions 7 ha (chevauchement compté une fois), dont rien dans la bande de recul
    assert ind["surface_exclusions_strictes"]["valeur_ha"] == pytest.approx(7, rel=1e-8)
    assert net_ha(run) == pytest.approx(81 - 7, rel=1e-9)
    assert run["results"]["scr_calcul"] == "EPSG:32735"
    assert run["results"]["niveau_etude"] == "reconnaissance préliminaire"
    assert all(c["ok"] for c in run["results"]["controles"])
    kinds = [l["kind"] for l in run["layers"]]
    assert kinds[0] == "limite_site" and kinds[-1] == "surface_nette"


def test_rerun_is_idempotent_and_reproducible(client, setup):
    site_id = setup["site"]["id"]
    first = analyse(client, site_id, setback_m=20, setback_justification="h").json()
    again = analyse(client, site_id, setback_m=20, setback_justification="h")
    assert again.status_code == 200 and again.json()["reused"] is True and again.json()["id"] == first["id"]
    forced = analyse(client, site_id, setback_m=20, setback_justification="h", force=True).json()
    assert forced["id"] != first["id"]
    assert forced["input_hash"] == first["input_hash"]
    assert forced["results"] == first["results"]
    g1 = client.get(f"/api/v1/analyses/{first['id']}/geojson").json()["features"]
    g2 = client.get(f"/api/v1/analyses/{forced['id']}/geojson").json()["features"]
    assert [f["geometry"] for f in g1] == [f["geometry"] for f in g2]


def test_results_change_when_constraints_change(client, setup):
    site_id, rule_id = setup["site"]["id"], setup["rule"]["id"]
    base = analyse(client, site_id).json()
    r = client.patch(f"/api/v1/constraints/{rule_id}", json={"buffer_m": 20})
    assert r.status_code == 422  # buffer sans justification
    r = client.patch(f"/api/v1/constraints/{rule_id}", json={
        "buffer_m": 20, "justification_type": "hypothese_utilisateur", "justification": "Marge prudente, à confirmer"})
    assert r.status_code == 200, r.text
    buffered = analyse(client, site_id).json()
    assert buffered["input_hash"] != base["input_hash"]
    assert net_ha(buffered) < net_ha(base)
    client.patch(f"/api/v1/constraints/{rule_id}", json={"active": False})
    off = analyse(client, site_id).json()
    assert net_ha(off) == pytest.approx(100, rel=1e-9)


def test_new_dataset_version_changes_hash(client, setup):
    site_id, ds_id = setup["site"]["id"], setup["dataset"]["id"]
    base = analyse(client, site_id).json()
    files = {"file": ("v2.geojson", json.dumps(fc(ll(utm_box(100, 100, 200, 200)))).encode(), "application/json")}
    v = client.post(f"/api/v1/datasets/{ds_id}/versions", files=files)
    assert v.status_code == 201 and v.json()["version_no"] == 2
    new = analyse(client, site_id).json()
    assert new["input_hash"] != base["input_hash"]
    assert new["results"]["indicateurs"]["surface_exclusions_strictes"]["valeur_m2"] == pytest.approx(10_000, rel=1e-8)
    snap = new["inputs"]["regles"][0]["donnees"]
    assert snap["version_no"] == 2 and snap["licence"] == "CC-BY-4.0" and snap["date_reference"] == "2026-01-15"


def test_traceability_of_dataset(client, setup):
    ds = client.get(f"/api/v1/datasets/{setup['dataset']['id']}").json()
    v = ds["latest_version"]
    assert len(v["sha256"]) == 64 and v["source_crs"] == "EPSG:4326" and v["crs_origin"] == "implicite_rfc7946"
    assert ds["source_name"] == "Relevé test" and ds["nature"] == "observee"


def test_line_layer_requires_justified_buffer(client):
    p = new_project(client)
    road = ll(LineString([(X0 - 500, Y0 + 500), (X0 + 1500, Y0 + 500)]))
    d = upload(client, p["id"], fc(road), "Route").json()
    bad = add_rule(client, p["id"], d["id"], buffer_m=30)
    assert bad.status_code == 422 and bad.json()["detail"]["code"] == "justification_manquante"
    ok = add_rule(client, p["id"], d["id"], buffer_m=30, justification_type="texte_reglementaire_cite",
                  justification="Référence citée par l'utilisateur (non vérifiée par le logiciel)")
    assert ok.status_code == 201


def test_land_and_grid_labels_require_evidence(client, setup):
    pid, site_id = setup["project"]["id"], setup["site"]["id"]
    run = analyse(client, site_id).json()
    assert run["results"]["statuts"]["foncier"] == "inconnu"
    assert run["results"]["statuts"]["raccordement"] == "inconnu"
    assert "Non évaluée" in run["results"]["statuts"]["capacite_reseau"]

    r = client.patch(f"/api/v1/sites/{site_id}", json={"land_status": "verifie_sur_piece"})
    assert r.status_code == 422 and r.json()["detail"]["code"] == "piece_manquante"
    # une couche d'exclusion n'est pas une pièce foncière
    r = client.patch(f"/api/v1/sites/{site_id}", json={"land_status": "verifie_sur_piece",
                                                         "land_evidence_dataset_id": setup["dataset"]["id"]})
    assert r.status_code == 422 and r.json()["detail"]["code"] == "piece_invalide"
    fake = upload(client, pid, fc(site_1km()), "Cadastre fictif", category="cadastre_officiel", is_synthetic="true").json()
    r = client.patch(f"/api/v1/sites/{site_id}", json={"land_status": "verifie_sur_piece", "land_evidence_dataset_id": fake["id"]})
    assert r.status_code == 422 and r.json()["detail"]["code"] == "piece_fictive"
    real = upload(client, pid, fc(site_1km()), "Extrait cadastral", category="cadastre_officiel").json()
    r = client.patch(f"/api/v1/sites/{site_id}", json={"land_status": "verifie_sur_piece", "land_evidence_dataset_id": real["id"]})
    assert r.status_code == 200
    r = client.patch(f"/api/v1/sites/{site_id}", json={"grid_status": "raccordement_confirme"})
    assert r.status_code == 422
    after = analyse(client, site_id).json()
    assert after["results"]["statuts"]["foncier"] == "verifie_sur_piece"
    assert after["results"]["statuts"]["raccordement"] == "inconnu"


def test_project_isolation(client, setup):
    other = new_project(client, name="Autre projet")
    r = add_rule(client, other["id"], setup["dataset"]["id"])
    assert r.status_code == 422 and r.json()["detail"]["code"] == "isolation_projet"
    s2 = client.post(f"/api/v1/projects/{other['id']}/sites", json={"name": "B", "geometry": mapping(site_1km())}).json()
    r = analyse(client, s2["id"], rule_ids=[setup["rule"]["id"]])
    assert r.status_code == 422 and r.json()["detail"]["code"] == "isolation_projet"


def test_site_import_creates_sites_with_provenance(client):
    p = new_project(client)
    g = fc(site_1km(), ll(utm_box(2000, 0, 2500, 500)), props=[{"nom": "Nord"}, {"nom": "Sud"}])
    r = upload(client, p["id"], g, "Limites", path="sites/import", name_field="nom", horizontal_accuracy_m="3")
    assert r.status_code == 201, r.text
    sites = r.json()["sites"]
    assert [s["name"] for s in sites] == ["Nord", "Sud"]
    assert sites[0]["boundary_accuracy_m"] == 3 and sites[0]["boundary_dataset_version_id"]
    assert r.json()["dataset"]["category"] == "limite_site"
    lines = fc(ll(LineString([(X0, Y0), (X0 + 100, Y0)])))
    bad = upload(client, p["id"], lines, "Lignes", path="sites/import")
    assert bad.status_code == 422 and "polygone" in bad.json()["detail"]["message"]


def test_invalid_drawn_site_gives_readable_error(client):
    p = new_project(client)
    bowtie = {"type": "Polygon", "coordinates": [[[27, -26.5], [27.01, -26.51], [27.01, -26.5], [27, -26.51], [27, -26.5]]]}
    r = client.post(f"/api/v1/projects/{p['id']}/sites", json={"name": "X", "geometry": bowtie})
    assert r.status_code == 422
    assert r.json()["detail"]["code"] == "geometrie_invalide" and "invalide" in r.json()["detail"]["message"]
    proj = {"type": "Polygon", "coordinates": [[[500000, 7070000], [501000, 7070000], [501000, 7071000], [500000, 7070000]]]}
    r = client.post(f"/api/v1/projects/{p['id']}/sites", json={"name": "Y", "geometry": proj})
    assert r.status_code == 422 and "projetées" in r.json()["detail"]["message"]


def test_upload_size_limit(client, monkeypatch):
    p = new_project(client)
    monkeypatch.setattr(get_settings(), "max_upload_mb", 0)
    r = upload(client, p["id"], fc(site_1km()), "Gros")
    assert r.status_code == 422 and r.json()["detail"]["code"] == "fichier_trop_gros"


def test_source_url_is_metadata_only(client):
    p = new_project(client)
    r = upload(client, p["id"], fc(site_1km()), "X", source_url="file:///etc/passwd")
    assert r.status_code == 422


def test_fictional_project_is_flagged_in_exports(client):
    p = new_project(client, is_fictional=True)
    s = client.post(f"/api/v1/projects/{p['id']}/sites", json={"name": "Démo", "geometry": mapping(site_1km())}).json()
    run = analyse(client, s["id"], density_mwp_dc_per_ha=0.9, density_justification="Hypothèse de démonstration").json()
    assert run["results"]["donnees_fictives"] is True
    assert run["results"]["indicateurs"]["puissance_indicative_mwp_dc"]["nature"] == "hypothetique"
    gj = client.get(f"/api/v1/analyses/{run['id']}/geojson")
    assert gj.headers["content-type"].startswith("application/geo+json")
    meta = gj.json()["metadata"]
    assert meta["donnees_fictives"] == "DONNÉES FICTIVES" and "non bancable" in meta["mention"]
    text = client.get(f"/api/v1/analyses/{run['id']}/csv").text.lstrip("﻿")
    rows = list(csv.DictReader(io.StringIO(text)))
    by_key = {r["cle"]: r for r in rows}
    assert by_key["donnees_fictives"]["valeur"] == "DONNÉES FICTIVES"
    assert float(by_key["surface_nette"]["valeur"]) == pytest.approx(1_000_000, rel=1e-9)
    assert by_key["surface_nette"]["nature"] == "calcule"
    assert by_key["puissance_indicative_mwp_dc"]["nature"] == "hypothetique"


def test_csv_export_roundtrips_exact_values(client, setup):
    run = analyse(client, setup["site"]["id"], setback_m=10, setback_justification="h").json()
    text = client.get(f"/api/v1/analyses/{run['id']}/csv").text.lstrip("﻿")
    rows = {r["cle"]: r for r in csv.DictReader(io.StringIO(text))}
    assert float(rows["surface_nette"]["valeur"]) == run["results"]["indicateurs"]["surface_nette"]["valeur_m2"]
    assert rows["empreinte_entrees_sha256"]["valeur"] == run["input_hash"]


def test_audit_log_records_actions(client, setup):
    analyse(client, setup["site"]["id"])
    client.patch(f"/api/v1/constraints/{setup['rule']['id']}", json={"active": False}, headers={"X-Actor": "analyste.test"})
    log = client.get(f"/api/v1/audit-log?project_id={setup['project']['id']}").json()
    actions = [e["action"] for e in log]
    for a in ("projet.cree", "site.cree", "donnees.importees", "regle.creee", "analyse.executee", "regle.modifiee"):
        assert a in actions
    assert log[0]["actor"] == "analyste.test" and log[0]["details"]["avant"] == {"active": True}


def test_delete_project_cascades(client, setup):
    pid = setup["project"]["id"]
    analyse(client, setup["site"]["id"])
    assert client.delete(f"/api/v1/projects/{pid}").status_code == 204
    assert client.get(f"/api/v1/sites/{setup['site']['id']}").status_code == 404
    assert client.get(f"/api/v1/datasets/{setup['dataset']['id']}").status_code == 404
