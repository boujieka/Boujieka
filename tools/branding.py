"""Author branding shared by the workbook builders.

apply(wb, T) writes the author line on the first sheet (row 4, the blank line under the subtitle)
and sets a print footer on every sheet: author on the left, page number on the right.
"""
from openpyxl.styles import Font

AUTHOR = "Emmanuel Boujieka Kamga"


def apply(wb, T):
    first = wb.worksheets[0]
    c = first["B4"]
    if c.value in (None, ""):
        c.value = f"By {AUTHOR}"  # the i18n cell hook translates it in French builds
        c.font = Font(name="Arial", size=10, bold=True, color="1B7F79")
    for ws in wb.worksheets:
        ws.oddFooter.left.text = AUTHOR
        ws.oddFooter.left.size = 8
        ws.oddFooter.right.text = "&P / &N"
        ws.oddFooter.right.size = 8
        ws.evenFooter.left.text = AUTHOR
        ws.evenFooter.right.text = "&P / &N"
