"""Optional print-area hook used to render listing screenshots.

When the PRINT_AREAS environment variable holds a JSON object {sheet title: "A1:F30"}, the builders
set those print areas (one page per sheet) before saving. Without the variable nothing changes, so the
workbooks sold to customers are unaffected.
"""
import json
import os


def apply(wb):
    spec = os.environ.get("PRINT_AREAS")
    if not spec:
        return
    for title, rng in json.loads(spec).items():
        if title not in wb.sheetnames:
            raise KeyError(f"PRINT_AREAS: no sheet named {title!r}")
        ws = wb[title]
        ws.print_area = rng
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 1
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_options.gridLines = False
    # screenshots: keep the author in the footer, drop the page counter
    for ws in wb.worksheets:
        ws.oddFooter.right.text = None
        ws.evenFooter.right.text = None
