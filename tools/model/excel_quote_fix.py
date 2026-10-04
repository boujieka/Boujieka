"""Restore Excel-safe quoting of sheet names in a workbook saved by LibreOffice.

LibreOffice writes references such as 17_PROJECT_FINANCE!$C$31 without quotes. Excel requires sheet names that start
with a digit to be quoted ('17_PROJECT_FINANCE'!$C$31). This rewrites every formula, defined name, data validation and
conditional format in the package, keeping cached values untouched.

Run: python3 tools/model/excel_quote_fix.py model/Bankable_Hydro_Model.xlsx
"""
import re
import shutil
import sys
import tempfile
import zipfile

PAT = re.compile(r"(?<![\w'.])(\d[A-Za-z0-9_]*)!(?=\$?[A-Z])")


def fix_formula(s):
    return PAT.sub(lambda m: f"'{m.group(1)}'!", s)


def fix_xml(xml):
    n = 0

    def rep(m):
        nonlocal n
        new = fix_formula(m.group(2))
        n += new != m.group(2)
        return m.group(1) + new + m.group(3)
    xml = re.sub(r"(<(?:f|formula|formula1|formula2|definedName)\b[^>]*>)([^<]*)(</(?:f|formula|formula1|formula2|definedName)>)", rep, xml)
    return xml, n


def main(path):
    tmp = tempfile.mktemp(suffix=".xlsx")
    total = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml") and item.filename.startswith("xl/"):
                xml, n = fix_xml(data.decode("utf-8"))
                total += n
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)
    print(f"{path}: {total} formulas re-quoted")


if __name__ == "__main__":
    main(sys.argv[1])
