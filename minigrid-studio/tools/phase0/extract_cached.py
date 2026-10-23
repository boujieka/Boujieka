"""Extract the values Excel cached in the published workbook (its last saved
calculation) for the outputs listed in outputs_spec.json.

For the published workbook these are genuine Excel results for scenario
S1_base: the file was saved by Microsoft Excel (docProps/app.xml) with the
debt/DSRA sizing checks at 0. For the other scenarios, run it on the workbook
saved by Excel after the procedure of docs/reference_scenarios.md.
Usage: python tools/phase0/extract_cached.py WORKBOOK OUT.json [SCENARIO_ID]
"""
import datetime
import hashlib
import json
import os
import sys

import openpyxl
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
EPOCH = datetime.datetime(1899, 12, 30)
TIMELINE = [get_column_letter(c) for c in range(10, 79)]  # J..BZ


def norm(v):
    if isinstance(v, datetime.datetime):
        return (v - EPOCH).total_seconds() / 86400
    if isinstance(v, bool):
        return float(v)
    return v


def main():
    src, out = sys.argv[1:3]
    scenario = sys.argv[3] if len(sys.argv) > 3 else "S1_base"
    spec = json.load(open(os.path.join(HERE, "outputs_spec.json")))
    wb = openpyxl.load_workbook(src, data_only=True)

    def get(ref):
        sh, addr = ref.split("!")
        return norm(wb[sh][addr].value)

    res = {
        "scenario": scenario,
        "engine": "Microsoft Excel (values cached in the saved workbook)",
        "source_sha256": hashlib.sha256(open(src, "rb").read()).hexdigest(),
        "inputs_changed": {},
        "scalars": {k: get(ref) for k, (ref, _l, _u) in spec["scalars"].items()},
        "pasted_values": {k: get(ref) for k, ref in spec["pasted_values"].items()},
        "series": {k: [get(f"{sh}!{c}{row}") for c in TIMELINE]
                   for k, (sh, row, _l) in spec["series"].items()},
    }
    json.dump(res, open(out, "w"), indent=1)
    print("written", out)


if __name__ == "__main__":
    main()
