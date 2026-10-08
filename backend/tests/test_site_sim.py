"""Site simulators: published-rate points (site/build.py yield_points), the shared arithmetic
(site/simcalc.js, run with node when available) and the public-key guard of auth_config."""

import base64
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[2] / "site"
sys.path.insert(0, str(SITE))
spec = importlib.util.spec_from_file_location("site_build", SITE / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
import report  # noqa: E402

AS_OF = date(2026, 10, 8)


def row(d, res, y="7.0", alloc="1000", typ="primary_auction", isin="X", country="SEN",
        url="https://www.umoatitres.org/x.pdf", cur="XOF", instr="treasury_bill"):
    return {"country": country, "date": d, "type": typ, "isin": isin, "name": isin, "instr": instr, "maturity": None,
            "residual_years": res, "alloc": None if alloc is None else Decimal(alloc), "sub": None,
            "yld": None if y is None else Decimal(y), "url": url, "currency": cur}


@pytest.fixture
def rows(monkeypatch):
    box = []
    monkeypatch.setattr(report, "load_rows", lambda *a, **k: box)
    return box


def test_empty_data_gives_no_points(rows):
    assert build.yield_points(AS_OF) == {}


def test_window_is_last_12_months_inclusive_of_as_of(rows):
    rows += [row(date(2025, 10, 8), 3.0, isin="OLD"), row(AS_OF, 3.0, isin="TODAY"), row(date(2026, 10, 9), 3.0, isin="FUTURE")]
    assert build.yield_points(AS_OF)["SEN"]["3"]["isin"] == "TODAY"


def test_held_or_non_issuance_rows_are_skipped(rows):
    rows += [row(AS_OF, 3.0, y=None, isin="NOY"), row(AS_OF, 3.0, alloc="0", isin="NOALLOC"), row(AS_OF, 3.0, alloc=None, isin="NONE"),
             row(AS_OF, 3.0, typ="buyback", isin="BB"), row(AS_OF, None, isin="NORES")]
    assert build.yield_points(AS_OF) == {}


def test_latest_then_largest_allotment_wins(rows):
    rows += [row(date(2026, 9, 1), 5.0, isin="A", alloc="9999"), row(date(2026, 9, 2), 5.0, isin="B", alloc="1"),
             row(date(2026, 9, 2), 5.0, isin="C", alloc="2")]
    assert build.yield_points(AS_OF)["SEN"]["5"]["isin"] == "C"


@pytest.mark.parametrize("res,h", [(1.0, "1"), (1.0021, "1"), (3.0, "3"), (4.0, "3"), (6.0, "5"), (8.5, "7"), (15.0, "10")])
def test_horizon_windows(rows, res, h):
    rows.append(row(AS_OF, res))  # 12-month bills run 364 to 366 days: both are "1 year"
    assert list(build.yield_points(AS_OF)["SEN"]) == [h]


@pytest.mark.parametrize("res", [0.25, 0.5, 1.5, 2.0])
def test_short_bills_and_two_year_paper_are_not_stretched_to_a_horizon(rows, res):
    rows.append(row(AS_OF, res))
    assert build.yield_points(AS_OF) == {}


def test_bond_without_known_coupon_gives_no_point(rows):
    rows.append(row(AS_OF, 5.0, isin="NOT-IN-SECURITIES", instr="treasury_bond"))
    assert build.yield_points(AS_OF) == {}


def test_source_label_from_url(rows):
    rows += [row(AS_OF, 3.0, url="https://www.beac.int/x.pdf", country="CMR", cur="XAF"),
             row(AS_OF, 3.0, url="https://example.org/x.pdf", country="CIV")]
    yp = build.yield_points(AS_OF)
    assert yp["CMR"]["3"]["src"] == "BEAC" and yp["CIV"]["3"]["src"] == "example.org"


def test_real_data_points_are_finite_and_sourced():
    for pts in build.yield_points(AS_OF).values():
        for p in pts.values():
            assert 0 < p["y"] < 100 and p["d"] <= AS_OF.isoformat() and p["url"].startswith("https://")
            assert p["src"] in ("UMOA-Titres", "BEAC") and (p["instr"] == "treasury_bill" or p["coupon"] is not None)


def test_embedded_json_cannot_close_the_script_block():
    s = build._embed({"t": "</script><!--<script>"})
    assert "<" not in s and json.loads(s)["t"] == "</script><!--<script>"
    with pytest.raises(ValueError):
        build._embed({"x": float("nan")})


def _jwt(role):
    enc = lambda o: base64.urlsafe_b64encode(json.dumps(o).encode()).decode().rstrip("=")  # noqa: E731
    return f"{enc({'alg': 'HS256'})}.{enc({'role': role})}.sig"


@pytest.mark.parametrize("url,key,ok", [
    ("https://abc.supabase.co", _jwt("anon"), True),
    ("https://abc.supabase.co", "sb_publishable_x", True),
    ("https://abc.supabase.co", _jwt("service_role"), False),
    ("https://abc.supabase.co", "sb_secret_x", False),
    ("https://abc.supabase.co;report-uri", "sb_publishable_x", False),
    ("http://abc.supabase.co", "sb_publishable_x", False),
    ("https://abc.supabase.co/path", "sb_publishable_x", False),
])
def test_auth_config_accepts_only_the_public_key_and_a_bare_https_host(monkeypatch, url, key, ok):
    monkeypatch.setenv("SUPABASE_URL", url)
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", key)
    if ok:
        assert build.auth_config() == {"url": url, "key": key}
    else:
        with pytest.raises(SystemExit):
            build.auth_config()


def test_auth_config_off_without_key(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_PUBLISHABLE_KEY", raising=False)
    monkeypatch.delenv("SUPABASE_ANON_KEY", raising=False)
    assert build.auth_config() is None


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_simcalc_js():
    r = subprocess.run(["node", "--test", str(SITE / "tests" / "simcalc.test.js")], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]


def test_prerender_fills_markup_but_never_scripts():
    html = ('<h1 data-ih="a"></h1><p data-i="b"></p><span data-i="missing"></span><b data-country="SEN"></b>'
            '<script>const x = `<p data-i="b"></p>`;</script>')
    out = build.prerender(html, {"a": "<em>A</em>", "b": "x < y", "b.real": "réel"}, real=True, names={"SEN": "Sénégal"})
    assert '<h1 data-ih="a"><em>A</em></h1>' in out and '<p data-i="b">réel</p>' in out
    assert '<span data-i="missing"></span>' in out and '<b data-country="SEN">Sénégal</b>' in out
    assert out.endswith('<script>const x = `<p data-i="b"></p>`;</script>')  # script body untouched
    assert "x &lt; y" in build.prerender('<p data-i="b"></p>', {"b": "x < y"})


def test_csp_hashes_cover_inline_scripts_only(tmp_path, monkeypatch):
    import base64
    import hashlib

    monkeypatch.setattr(build, "DIST", tmp_path)
    (tmp_path / "a.html").write_text('<script>run()</script><script src="/x.js"></script><script type="application/json">{}</script>')
    want = "'sha256-" + base64.b64encode(hashlib.sha256(b"run()").digest()).decode() + "'"
    assert build.inline_script_hashes() == [want]
