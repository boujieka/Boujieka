"""Compare two output files produced by extract_cached.py / lo_scenarios.py.
Tolerances follow docs/reference_scenarios.md: 0.1 % relative for amounts,
1e-4 absolute for ratios/rates; flags must match exactly.
Usage: python tools/phase0/compare_outputs.py REFERENCE.json CANDIDATE.json
"""
import json
import sys

REL_AMOUNT = 1e-3
ABS_RATIO = 1e-4
ABS_FLOOR = 1.0   # amounts below one currency unit are compared absolutely


def close(key, a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if key.startswith("check_") or key == "bs_check":
            return a == b
        if "irr" in key or key in ("avg_tariff_time_weighted",):
            return abs(a - b) <= ABS_RATIO
        return abs(a - b) <= max(REL_AMOUNT * abs(a), ABS_FLOOR * REL_AMOUNT)
    return a == b


def main():
    ref, cand = (json.load(open(p)) for p in sys.argv[1:3])
    fails, worst = [], 0.0
    for k, a in ref["scalars"].items():
        b = cand["scalars"].get(k)
        if not close(k, a, b):
            fails.append((k, a, b))
    for k, row in ref["series"].items():
        for i, (a, b) in enumerate(zip(row, cand["series"][k])):
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a) > 1:
                worst = max(worst, abs(a - b) / abs(a))
            if not close(k, a, b):
                fails.append((f"{k}[{i}]", a, b))
    print(f"scalars compared: {len(ref['scalars'])}, series: {len(ref['series'])}")
    print(f"max relative gap on series amounts > 1: {worst:.3e}")
    print("result:", "PASS" if not fails else f"FAIL ({len(fails)})")
    for f in fails[:30]:
        print("  ", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
