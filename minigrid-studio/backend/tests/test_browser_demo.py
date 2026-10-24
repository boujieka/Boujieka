"""The in-browser demo entry points (run here with CPython; Pyodide runs the same code)."""
import base64
import json

from app.demo import browser
from app.services.scenarios import load_template


def test_browser_entry_points_round_trip():
    meta = json.loads(browser.meta("fr"))
    assert meta["labels"]["groups"]["debt"] == "Dette senior" and meta["templates"][0]["name"] == "demo_fictitious"
    a = load_template("demo_fictitious")
    r = json.loads(browser.revise(json.dumps(a), json.dumps({"debt.target_dscr": 1.3})))
    assert r["ok"] and r["assumptions"]["debt"]["target_dscr"] == 1.3
    assert not json.loads(browser.revise(json.dumps(a), json.dumps({"__class__": 1})))["ok"]
    run1 = json.loads(browser.run(json.dumps(a), "{}", "excel_macros", False))
    run2 = json.loads(browser.run(json.dumps(r["assumptions"]), "{}", "excel_macros", False))
    assert run1["status"] == "reconciled-engine" and abs(run1["result"]["kpis"]["project_irr"]["value"] - 0.0810894) < 1e-6
    bad = json.loads(browser.run(json.dumps({**a, "lots": []}), "{}", "excel_macros", False))
    assert bad["status"] == "failed" and "lots" in bad["error"]
    items = [{"run": {"id": f"r{i}", **run}, "project": "P", "version": {"scenario": "s", "version": i, "status": "draft",
              "assumptions": asm}} for i, (run, asm) in enumerate(((run1, a), (run2, r["assumptions"])), 1)]
    c = json.loads(browser.compare(json.dumps(items), "fr"))
    assert [d["path"] for d in c["assumption_diffs"]] == ["debt.target_dscr"]
    xlsx = base64.b64decode(browser.studio_xlsx(json.dumps({"name": "P", "country": "F"}),
                                                json.dumps(items[0]["version"]), json.dumps(items[0]["run"]), "fr"))
    assert xlsx[:2] == b"PK"
