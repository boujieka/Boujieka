"""Cas de référence du moteur de screening (valeurs attendues calculées à la main)."""

import pytest
import shapely
from shapely.geometry import LineString, Point, Polygon

from app.geo.crs import utm_epsg_for
from app.geo.engine import HARD, SOFT, RuleInput, ScreeningParams, screen_site
from app.geo.validation import GeometryError
from tests.helpers import X0, Y0, ll, site_1km, utm_box

REL = 1e-9  # tolérance relative : arrondis flottants des reprojections aller-retour


def m(res, key):
    return res.metrics[key]["valeur_m2"]


def hard(rid, *geoms, buffer=0.0, acc=None, name=None):
    return RuleInput(rid, name or f"R{rid}", HARD, buffer, tuple(geoms), accuracy_m=acc)


def test_gross_area_of_1km_square_is_100_ha():
    res = screen_site(site_1km(), ScreeningParams(), [])
    assert m(res, "surface_brute") == pytest.approx(1_000_000, rel=REL)
    assert m(res, "surface_nette") == pytest.approx(1_000_000, rel=REL)
    assert res.crs_epsg == 32735
    assert all(c["ok"] for c in res.checks)


def test_geodesic_cross_check_matches_utm_scale_factor():
    # Sur le méridien central, le facteur d'échelle UTM vaut 0,9996 : aire UTM ≈ 0,9992 × aire réelle.
    res = screen_site(site_1km(), ScreeningParams(), [])
    detail = next(c for c in res.checks if c["nom"] == "controle_geodesique")
    assert detail["ok"]
    assert "0.07" in detail["detail"] or "0.08" in detail["detail"]


def test_setback_50m_leaves_900m_square():
    res = screen_site(site_1km(), ScreeningParams(setback_m=50), [])
    assert m(res, "surface_recul") == pytest.approx(1_000_000 - 900 * 900, rel=REL)
    assert m(res, "surface_nette") == pytest.approx(810_000, rel=REL)


def test_overlapping_exclusions_are_subtracted_once():
    a = ll(utm_box(100, 100, 300, 300))  # 40 000 m²
    b = ll(utm_box(200, 200, 400, 400))  # 40 000 m², chevauchement 10 000 m²
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, a), hard(2, b)])
    assert m(res, "surface_exclusions_strictes") == pytest.approx(70_000, rel=1e-8)
    assert m(res, "somme_exclusions_par_regle") == pytest.approx(80_000, rel=1e-8)
    assert m(res, "chevauchement_non_double_compte") == pytest.approx(10_000, rel=1e-6)
    assert m(res, "surface_nette") == pytest.approx(930_000, rel=REL)


def test_duplicate_feature_in_same_layer_counted_once():
    a = ll(utm_box(100, 100, 300, 300))
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, a, a)])
    assert m(res, "surface_exclusions_strictes") == pytest.approx(40_000, rel=1e-8)


def test_exclusion_combined_with_setback():
    edge = ll(utm_box(0, 0, 1000, 100))  # bande sud de 100 m, recouvre la bande de recul
    res = screen_site(site_1km(), ScreeningParams(setback_m=50), [hard(1, edge)])
    # zone aménageable 900×900 ; l'exclusion y prend 900 × 50
    assert m(res, "surface_exclusions_strictes") == pytest.approx(45_000, rel=1e-8)
    assert m(res, "surface_nette") == pytest.approx(810_000 - 45_000, rel=REL)
    assert next(c for c in res.checks if c["nom"] == "conservation_des_surfaces")["ok"]


def test_line_buffer_excludes_corridor():
    road = ll(LineString([(X0 - 500, Y0 + 500), (X0 + 1500, Y0 + 500)]))  # traverse le site
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, road, buffer=25)])
    assert m(res, "surface_exclusions_strictes") == pytest.approx(50 * 1000, rel=1e-6)


def test_results_change_with_constraints():
    road = ll(LineString([(X0 - 500, Y0 + 500), (X0 + 1500, Y0 + 500)]))
    r25 = screen_site(site_1km(), ScreeningParams(), [hard(1, road, buffer=25)])
    r50 = screen_site(site_1km(), ScreeningParams(), [hard(1, road, buffer=50)])
    assert m(r50, "surface_nette") < m(r25, "surface_nette")
    assert m(r50, "surface_exclusions_strictes") == pytest.approx(100_000, rel=1e-6)


def test_point_without_buffer_has_no_effect_and_warns():
    p = ll(Point(X0 + 500, Y0 + 500))
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, p)])
    assert m(res, "surface_nette") == pytest.approx(1_000_000, rel=REL)
    assert any("sans buffer" in w for w in res.warnings)


def test_exclusion_outside_site_is_ignored():
    far = ll(utm_box(5000, 5000, 6000, 6000))
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, far, buffer=100)])
    assert res.per_rule[0]["entites_retenues"] == 0
    assert m(res, "surface_nette") == pytest.approx(1_000_000, rel=REL)


def test_soft_constraint_is_reported_not_subtracted():
    zone = ll(utm_box(0, 0, 500, 1000))
    soft = RuleInput(9, "Pente indicative", SOFT, 0, (zone,))
    res = screen_site(site_1km(), ScreeningParams(), [soft])
    assert m(res, "surface_nette") == pytest.approx(1_000_000, rel=REL)
    assert m(res, "surface_contraintes_indicatives") == pytest.approx(500_000, rel=1e-8)


def test_soft_constraint_measured_inside_net_area_only():
    excl = ll(utm_box(0, 0, 500, 1000))
    zone = ll(utm_box(250, 0, 750, 1000))
    res = screen_site(
        site_1km(), ScreeningParams(), [hard(1, excl), RuleInput(2, "S", SOFT, 0, (zone,))]
    )
    assert m(res, "surface_contraintes_indicatives") == pytest.approx(250_000, rel=1e-8)


def test_strict_reproducibility():
    a = ll(utm_box(100, 100, 300, 300))
    road = ll(LineString([(X0 - 500, Y0 + 500), (X0 + 1500, Y0 + 520)]))
    args = (site_1km(), ScreeningParams(setback_m=30), [hard(1, a), hard(2, road, buffer=40)])
    r1, r2 = screen_site(*args), screen_site(*args)
    assert r1.as_dict() == r2.as_dict()
    assert [shapely.to_wkb(g) for *_, g, _ in r1.layers] == [shapely.to_wkb(g) for *_, g, _ in r2.layers]


def test_interval_requires_declared_accuracy():
    a = ll(utm_box(100, 100, 300, 300))
    res = screen_site(site_1km(), ScreeningParams(), [hard(1, a)])
    assert res.metrics["intervalle_surface_nette"]["nature"] == "inconnu"


def test_interval_brackets_nominal_value():
    a = ll(utm_box(100, 100, 300, 300))
    res = screen_site(site_1km(), ScreeningParams(setback_m=20, boundary_accuracy_m=5), [hard(1, a, acc=10)])
    iv = res.metrics["intervalle_surface_nette"]
    assert iv["nature"] == "calcule"
    assert iv["bas_m2"] < m(res, "surface_nette") < iv["haut_m2"]


def test_indicative_power_is_labelled_hypothetical():
    res = screen_site(site_1km(), ScreeningParams(density_mwp_dc_per_ha=0.8, density_justification="test"), [])
    p = res.metrics["puissance_indicative_mwp_dc"]
    assert p["nature"] == "hypothetique"
    assert p["valeur"] == pytest.approx(80.0, rel=REL)
    unknown = screen_site(site_1km(), ScreeningParams(), [])
    assert unknown.metrics["puissance_indicative_mwp_dc"]["valeur"] is None


def test_setback_consuming_site_gives_zero():
    res = screen_site(site_1km(), ScreeningParams(setback_m=600), [])
    assert m(res, "surface_nette") == 0
    assert any("totalité" in w for w in res.warnings)


@pytest.mark.parametrize(
    "lon,lat,epsg",
    [(28.0, -26.2, 32735), (-17.45, 14.7, 32628), (32.58, 0.35, 32636), (3.38, 6.52, 32631), (57.5, -20.2, 32740)],
)
def test_utm_zone_selection(lon, lat, epsg):
    assert utm_epsg_for(lon, lat) == epsg


def test_site_in_west_africa_uses_its_own_zone():
    # carré de 1 km défini en UTM 28N (Sénégal, ~14,5° N)
    sq = ll(Polygon([(400000, 1600000), (401000, 1600000), (401000, 1601000), (400000, 1601000)]), 32628)
    res = screen_site(sq, ScreeningParams(), [])
    assert res.crs_epsg == 32628
    assert m(res, "surface_brute") == pytest.approx(1_000_000, rel=1e-9)


def test_invalid_inputs_refused():
    bowtie = Polygon([(27, -26), (27.01, -26.01), (27.01, -26), (27, -26.01)])
    with pytest.raises(GeometryError):
        screen_site(LineString([(27, -26), (27.1, -26)]), ScreeningParams(), [])
    with pytest.raises(GeometryError):
        screen_site(site_1km(), ScreeningParams(setback_m=-1), [])
    with pytest.raises(GeometryError):
        screen_site(site_1km(), ScreeningParams(), [RuleInput(1, "x", "inconnu", 0, ())])
    with pytest.raises(GeometryError, match="invalide"):
        screen_site(bowtie, ScreeningParams(), [])
