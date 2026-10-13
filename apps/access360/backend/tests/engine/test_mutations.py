"""Mutation tests: plant plausible formula errors in a copy of the engine and require that at least one check
fails for each. Adapted from the independent review (finding F06)."""
from __future__ import annotations

import importlib
import os
import shutil
import sys

import pytest

from app.engine.demo import demo_inputs

SRC = os.path.join(os.path.dirname(__file__), "..", "..", "app", "engine")

MUTANTS = {
    "interest on closing balance x1.5": ("interest = open_ccy * r", "interest = (open_ccy + d_ccy) * r * 1.5"),
    "tax charged twice": ("tax = tax_with_losses(taxable, m.tax_rate)", "tax = 2 * tax_with_losses(taxable, m.tax_rate)"),
    "tariff support double counted": ("tariff_support = np.where(ts_active, billed_kwh * sub.tariff_support_per_kwh, 0.0)",
                                      "tariff_support = np.where(ts_active, 2 * billed_kwh * sub.tariff_support_per_kwh, 0.0)"),
    "unlevered tax ignored in project CF": ("pre_sub = base_cf - unlev_tax_pre", "pre_sub = base_cf"),
    "replacements omitted from project CF": ("cash_collected + fee_rev - cash_opex - repl, 0.0)", "cash_collected + fee_rev - cash_opex, 0.0)"),
    "grant released in one quarter": ("rel = base / remaining_q", "rel = base"),
    "collection forced to 100%": ("collected = billed * p.opex.collection_efficiency", "collected = billed * 1.0"),
    "fuel cost x10": ("fuel = generated * tech.diesel_share", "fuel = 10 * generated * tech.diesel_share"),
    "depreciation life halved": ("n = max(int(round(life * 4)), 1)\n        for i in np.nonzero(spend > 0)[0]:\n            start = max(i + 1, C)  # assets",
                                 "n = max(int(round(life * 2)), 1)\n        for i in np.nonzero(spend > 0)[0]:\n            start = max(i + 1, C)  # assets"),
    "CFADS excludes tax": ("cfads = cash_ops - tax - repl", "cfads = cash_ops - repl"),
    "annuity sized on 110% of balance": ("pay = annuity_payment(open_ccy, r, n_amort)", "pay = annuity_payment(open_ccy * 1.1, r, n_amort)"),
    "DSRA sized on 1 quarter": ("dsra_target[i] = sched_ds[i + 1:i + 1 + nq].sum()", "dsra_target[i] = sched_ds[i + 1:i + 2].sum()"),
    "lock-up never applied": ("d = 0.0 if ((lock or reserve_short) and i < T - 1)", "d = 0.0 if ((reserve_short) and i < T - 1)"),
}


@pytest.mark.parametrize("label", sorted(MUTANTS))
def test_mutant_is_caught(label, tmp_path):
    old, new = MUTANTS[label]
    pkg = tmp_path / "mut"
    shutil.copytree(SRC, pkg / "engine", ignore=shutil.ignore_patterns("__pycache__"))
    (pkg / "__init__.py").write_text("")
    f = pkg / "engine" / "model.py"
    src = f.read_text()
    assert old in src, f"mutation pattern no longer matches the engine: {label}"
    f.write_text(src.replace(old, new, 1))
    sys.path.insert(0, str(tmp_path))
    try:
        for k in [k for k in sys.modules if k == "mut" or k.startswith("mut.")]:
            del sys.modules[k]
        mm = importlib.import_module("mut.engine.model")
        mc = importlib.import_module("mut.engine.checks")
    finally:
        sys.path.pop(0)
    p = demo_inputs()
    p.subsidies.tariff_support_per_kwh = 100
    p.subsidies.tariff_support_years = 5
    p.financing.lockup_dscr = 1.5  # makes lock-up bind in the demo
    p = mm.ProjectInputs.model_validate(p.model_dump())
    r = mm.run_model(p)
    failed = [c.code for c in mc.integrity_checks(r) if not c.passed]
    assert failed, f"mutant passes every check: {label}"
