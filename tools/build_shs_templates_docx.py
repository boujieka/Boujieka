"""Word templates of the Book 2 Templates Pack: investment memo (T01), customer credit policy (T03), business model canvas (T08).

Called from build_shs_templates.py. Each document carries a contents field (Word refreshes it on opening), a running
header, and "Page x of y" in the footer. Text in square brackets is to be replaced; grey italic paragraphs are guidance
to delete before issue.
"""
import re
import shutil
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AUTHOR = "Emmanuel Boujieka Kamga"
HOUSE = "Africa Energy Finance"
GREEN = RGBColor(0x0B, 0x30, 0x20)
GOLD = RGBColor(0xB0, 0x7C, 0x0F)
GREY = RGBColor(0x66, 0x66, 0x66)
BANNED = ["—", "–", " - ", " -- "]
BANNED_WORDS = re.compile(r"investment.grade|bankab|definitive|\bbest\b|Volume 2|version 1\.0", re.I)


# ------------------------------------------------------------------ helpers
def base_doc(code, title, landscape=False):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    st.paragraph_format.space_after = Pt(4)
    for name, size, color in (("Heading 1", 15, GREEN), ("Heading 2", 12, GREEN), ("Heading 3", 10.5, GOLD)):
        h = doc.styles[name]
        h.font.name, h.font.size, h.font.color.rgb, h.font.bold = "Arial", Pt(size), color, True
        rf = h.element.rPr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            h.element.rPr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), "Arial")
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        h.paragraph_format.space_before = Pt(12 if name != "Heading 3" else 8)
        h.paragraph_format.space_after = Pt(4)
    sec = doc.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    else:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    for m in ("left_margin", "right_margin"):
        setattr(sec, m, Cm(2.0 if not landscape else 1.5))
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(1.8)
    hp = sec.header.paragraphs[0]
    hp.text = ""
    r = hp.add_run(f"{HOUSE.upper()}  |  BOOK 2  |  TEMPLATE {code}")
    r.font.size, r.font.bold, r.font.color.rgb = Pt(7.5), True, GREEN
    r2 = hp.add_run(f"\t\t{title}")
    r2.font.size, r2.font.color.rgb = Pt(7.5), GREY
    fp = sec.footer.paragraphs[0]
    fp.text = ""
    r = fp.add_run(f"{HOUSE} | Book 2 Template {code} | Version 0.9 (pre-release)\t\tPage ")
    r.font.size, r.font.color.rgb = Pt(7.5), GREY
    _field(fp, "PAGE", 7.5)
    r = fp.add_run(" of ")
    r.font.size, r.font.color.rgb = Pt(7.5), GREY
    _field(fp, "NUMPAGES", 7.5)
    # right aligned tab stop at the text width
    width = sec.page_width - sec.left_margin - sec.right_margin
    for p in (hp, fp):
        p.paragraph_format.tab_stops.add_tab_stop(width, alignment=2)
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)
    cp = doc.core_properties
    cp.author = cp.last_modified_by = AUTHOR
    cp.title = f"AEF Book 2 Template {code}: {title}"
    cp.subject = "Africa Energy Finance, Book 2 Templates Pack"
    cp.keywords = "Africa Energy Finance; Book 2; PAYGo Solar Finance; template"
    cp.comments = "Decision support material; not investment, legal, tax or accounting advice."
    from datetime import datetime
    cp.created = cp.modified = datetime.now().replace(microsecond=0)
    cp.revision = 1
    return doc


def _field(par, instr, size=10):
    def fc(t):
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), t)
        return e
    r = par.add_run()
    r.font.size = Pt(size)
    r._r.append(fc("begin"))
    r = par.add_run()
    r.font.size = Pt(size)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    r._r.append(it)
    r = par.add_run()
    r._r.append(fc("separate"))
    r = par.add_run("1")
    r.font.size = Pt(size)
    r = par.add_run()
    r._r.append(fc("end"))


def shade(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_)
    tcPr.append(sh)


def cover(doc, kicker, title, subtitle, fields):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0, 0)
    shade(c, "0B3020")
    p = c.paragraphs[0]
    r = p.add_run(kicker)
    r.font.size, r.font.bold, r.font.color.rgb = Pt(9), True, RGBColor(0xE3, 0xC2, 0x7A)
    p = c.add_paragraph()
    r = p.add_run(title)
    r.font.size, r.font.bold, r.font.color.rgb = Pt(22), True, RGBColor(0xFF, 0xFF, 0xFF)
    p = c.add_paragraph()
    r = p.add_run(subtitle)
    r.font.size, r.font.color.rgb = Pt(12), RGBColor(0xE8, 0xE8, 0xE8)
    p = c.add_paragraph()
    r = p.add_run("AUTHOR & IDEATION   ")
    r.font.size, r.font.bold, r.font.color.rgb = Pt(8), True, RGBColor(0xE3, 0xC2, 0x7A)
    r = p.add_run(AUTHOR)
    r.font.size, r.font.bold, r.font.color.rgb = Pt(10), True, RGBColor(0xFF, 0xFF, 0xFF)
    doc.add_paragraph()
    if fields:
        table(doc, ["Item", "Entry"], fields, widths=(5.5, 11.0), first_bold=True)
    doc.add_paragraph()
    guide(doc, "Text in square brackets is to be replaced. Grey italic paragraphs are guidance and should be deleted before the "
               "document is issued. The contents list and page numbers refresh when the document is opened in Word; if they do "
               "not, select the contents and press F9.")


def toc(doc):
    t_ = doc.add_paragraph()
    r_ = t_.add_run("Contents")
    r_.bold, r_.font.size, r_.font.color.rgb = True, Pt(15), GREEN
    p = doc.add_paragraph()
    def fc(t):
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), t)
        return e
    r = p.add_run()
    r._r.append(fc("begin"))
    r = p.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = ' TOC \\o "1-2" \\h \\z \\u '
    r._r.append(it)
    r = p.add_run()
    r._r.append(fc("separate"))
    r = p.add_run("Word builds the contents list with page numbers when the document is opened.")
    r.italic = True
    r = p.add_run()
    r._r.append(fc("end"))
    page_break(doc)


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def guide(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic, r.font.size, r.font.color.rgb = True, Pt(9), GREY
    return p


def para(doc, text, bold_lead=None):
    p = doc.add_paragraph()
    if bold_lead:
        r = p.add_run(bold_lead + " ")
        r.bold = True
    p.add_run(text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def bullets(doc, items, style="List Number"):
    for it in items:
        doc.add_paragraph(it, style=style)


def table(doc, headers, rows, widths=None, first_bold=False, font=9):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = t.cell(0, j)
        shade(c, "0B3020")
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold, r.font.size, r.font.color.rgb = True, Pt(font), RGBColor(0xFF, 0xFF, 0xFF)
    for i, row in enumerate(rows, start=1):
        for j, v in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
            r = c.paragraphs[0].add_run("" if v is None else str(v))
            r.font.size = Pt(font)
            if first_bold and j == 0:
                r.bold = True
            if isinstance(v, str) and v.startswith("[") and v.endswith("]"):
                r.font.color.rgb = RGBColor(0x00, 0x00, 0xFF)
    # repeat header row on each page
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    if widths:
        for row in t.rows:
            for j, w in enumerate(widths):
                row.cells[j].width = Cm(w)
    doc.add_paragraph()
    return t


def blank(n, k):
    return [["" for _ in range(k)] for _ in range(n)]


def save(doc, path):
    for p in _all_paragraph_text(doc):
        for b in BANNED:
            if b in p:
                raise SystemExit(f"dash in {path.name}: {p[:80]}")
        if BANNED_WORDS.search(p):
            raise SystemExit(f"banned wording in {path.name}: {p[:80]}")
    doc.save(path)
    tmp = Path(tempfile.mkstemp(suffix=".docx")[1])
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>.*?</Application>", b"<Application>Africa Energy Finance</Application>", data)
                data = re.sub(rb"<Company>.*?</Company>", b"<Company>Africa Energy Finance</Company>", data)
            zout.writestr(item, data)
    shutil.move(tmp, path)
    path.chmod(0o644)
    print(path.name)


def _all_paragraph_text(doc):
    for p in doc.paragraphs:
        yield p.text
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    yield p.text
    for s in doc.sections:
        for p in s.header.paragraphs + s.footer.paragraphs:
            yield p.text


# ================================================================== T01 Investment memo
def build_t01(out):
    doc = base_doc("T01", "Investment committee memorandum")
    cover(doc, "BOOK 2  |  TEMPLATE T01", "Investment committee memorandum",
          "PAYGo solar company: equity or debt investment",
          [("Company", "[Company name, country]"), ("Transaction", "[Instrument, amount, currency]"),
           ("Valuation and stake", "[Pre money valuation; stake]"), ("Investment committee date", "[Date]"),
           ("Deal team", "[Names]"), ("Recommendation", "[Go / Conditional Go / Stop]"),
           ("Model and version", "[MODEL 2, PAYGo Company Financial and Investment Model: version, file name]"),
           ("Investment readiness", "[x of 23 gates met, y of 13 critical; workbook decision GO / CONDITIONAL GO / STOP]")])
    table(doc, ["Version", "Date", "Author", "Reviewer", "Changes"], [["[0.1]", "[date]", "[name]", "[name]", "[first draft]"]] + blank(2, 5))
    page_break(doc)
    toc(doc)

    S = []
    doc.add_paragraph("1. Recommendation and conditions", style="Heading 1")
    guide(doc, "State the recommendation in one sentence, then the conditions. Every later section is evidence for or against "
               "them. Write each condition as a condition precedent, a covenant or a structural feature, never as a hope.")
    para(doc, "[The deal team recommends a Go / Conditional Go / Stop on an investment of USD x in Company, subject to the "
              "conditions below.]")
    doc.add_paragraph("Conditions", style="Heading 2")
    table(doc, ["No.", "Condition", "Type", "Evidence required", "Linked gate or risk", "Owner"],
          [["1", "[Pricing policy: indexation of new contract prices]", "[Condition precedent]", "[Board resolution]", "[Risk R2]", "[Name]"]] + blank(6, 6),
          widths=(1.0, 5.0, 2.6, 3.4, 2.6, 2.0))
    doc.add_paragraph("Key figures", style="Heading 2")
    table(doc, ["Metric", "Base", "Downside", "Source in the model"],
          [["Revenue, Year 1 and Year 5 (USD)", "", "", "KPIs; Investment_Summary"],
           ["EBITDA margin, Year 5", "", "", "KPIs"],
           ["Peak equity requirement (USD)", "", "", "Investment_Summary"],
           ["Investor IRR and multiple (USD)", "", "", "Valuation"],
           ["Lowest trailing 3 month operational collection rate against covenant", "", "", "Covenants"],
           ["Observed operational collection rate, last 12 months of history", "", "", "Credit_Portfolio (history summary)"],
           ["PAYGo PERFORM 2026 KPIs, company reported (RR PvP, OR @2x)", "", "", "PERFORM_2026"],
           ["Readiness gates met (critical gates met) and workbook decision", "", "", "Investment_Readiness"]], widths=(7.0, 2.5, 2.5, 4.5), first_bold=True)

    doc.add_paragraph("2. Company, market and product range", style="Heading 1")
    guide(doc, "Describe the company as three businesses: retailer, service provider and consumer lender. Who are the customers "
               "by tier, what do they pay, and what alternatives do they have?")
    table(doc, ["Tier", "Product", "Cash price", "Deposit", "Daily rate", "Tenor", "Implied APR", "Planned mix"],
          [[f"{i}", "", "", "", "", "", "", ""] for i in range(1, 6)], font=8.5)
    para(doc, "[Market, competition, distribution footprint, management team.]")

    doc.add_paragraph("3. Unit economics by tier", style="Heading 1")
    guide(doc, "Use the calibrated curves, not the management plan. Read LTV to CAC with payback and unit IRR, and state which "
               "tiers rest on proxy credit assumptions without history.")
    table(doc, ["Tier", "Expected loss", "Lifetime contribution", "LTV to CAC", "Cash payback", "Unit IRR", "Credit evidence"],
          [[f"{i}", "", "", "", "", "", "[Observed / proxy]"] for i in range(1, 6)], font=8.5)

    doc.add_paragraph("4. Portfolio quality and data", style="Heading 1")
    guide(doc, "Load the company history before any projection. Compare cohort repayment with plan at the same age; state "
               "whether the DPD buckets reconcile to the ledger and how DPD is measured. Report the five PAYGo PERFORM 2026 KPIs "
               "only as computed by the company on contract data (GOGLA Technical Guide, June 2026), with their numerators and "
               "denominators; write \"not provided\" otherwise. The collection rate is an operational metric, not a PERFORM KPI, "
               "and never stands in for the repayment rate.")
    table(doc, ["Tier", "Cohort repayment ratio at M12, observed", "Plan", "Gap (points)", "Calibrated hazard", "Plan hazard"],
          [[f"{i}", "", "", "", "", ""] for i in range(1, 6)], font=8.5)
    table(doc, ["Portfolio KPI (latest month)", "Value", "Twelve months earlier", "Comment"],
          [["Operational collection rate (trailing 3 months)", "", "", ""], ["PAR30", "", "", ""], ["PAR90", "", "", ""],
           ["Write off ratio (trailing 12 months)", "", "", ""], ["Recovery rate", "", "", ""]], first_bold=True)
    para(doc, "[Data quality statement: period covered, reconciliation, definitions, independent review.]")

    doc.add_paragraph("5. Financial projections and funding requirement", style="Heading 1")
    guide(doc, "Present the calibrated case. Explain why EBITDA turns positive before operating cash flow does, and show the "
               "funding requirement by source.")
    guide(doc, "State the provenance of the inputs behind the case, as counted on the Start sheet of the model: model "
               "assumptions, company data, external evidence, calibrated assumptions and unverified inputs. Where revenue or "
               "credit losses are discussed, add: \"This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.\"")
    table(doc, ["Input provenance", "Number of inputs", "Main items"],
          [["MODEL ASSUMPTION", "", ""], ["COMPANY DATA", "", ""], ["EXTERNAL EVIDENCE", "", ""],
           ["CALIBRATED ASSUMPTION", "", ""], ["UNVERIFIED", "", ""]], first_bold=True, font=8.5)
    table(doc, ["Calibrated Base", "Y1", "Y2", "Y3", "Y4", "Y5"],
          [["Revenue", "", "", "", "", ""], ["Gross margin", "", "", "", "", ""], ["EBITDA margin", "", "", "", "", ""],
           ["Net income", "", "", "", "", ""], ["Net credit losses to revenue", "", "", "", "", ""],
           ["Operational collection rate", "", "", "", "", ""], ["30+ DPD to gross receivables", "", "", "", "", ""],
           ["Debt to book equity (year end)", "", "", "", "", ""], ["Cash flow from operations", "", "", "", "", ""]],
          first_bold=True, font=8.5)

    doc.add_paragraph("6. Scenarios and stress tests", style="Heading 1")
    guide(doc, "Run Base, Downside and Severe, then targeted cases: pricing response, untested tiers, funding drought. Read "
               "the multiple, peak equity and breach months together; IRR alone misleads in the tails.")
    table(doc, ["Case", "Peak equity", "Y5 EBITDA margin", "Y5 operational collection rate", "Investor IRR", "Multiple", "Breach months"],
          [["Management plan, Base", "", "", "", "", "", ""], ["Calibrated, Base", "", "", "", "", "", ""],
           ["Calibrated, Downside", "", "", "", "", "", ""], ["Calibrated, Severe", "", "", "", "", "", ""],
           ["[Targeted case]", "", "", "", "", "", ""], ["[Targeted case]", "", "", "", "", "", ""]], font=8.5)
    para(doc, "[Reverse stress: the change in collections or default hazard that breaches the collection covenant, and the "
              "fall in EBITDA that eliminates exit equity.]")

    doc.add_paragraph("7. Financing structure, borrowing base and covenants", style="Heading 1")
    guide(doc, "Match each funding layer to the asset it finances by size, tenor and currency. Set covenants at levels the "
               "company's own history supports, with cure periods.")
    table(doc, ["Covenant", "Threshold", "Projected worst", "Headroom", "Latest actual", "Comment"],
          [["Trailing 3 month operational collection rate", "", "", "", "", ""], ["Receivables at risk", "", "", "", "", ""],
           ["30+ DPD", "", "", "", "", ""], ["90+ DPD", "", "", "", "", ""], ["Borrowing base headroom", "", "", "", "", ""],
           ["Debt to book equity", "", "", "", "", ""]], first_bold=True, font=8.5)

    doc.add_paragraph("8. Valuation and returns", style="Heading 1")
    guide(doc, "Present the DCF and the exit based value side by side and explain the gap. State the exit multiple and the "
               "credit performance the entry price assumes, and the effect of currency depreciation on USD returns.")
    table(doc, ["Metric", "Value", "Comment"],
          [["DCF enterprise value at entry (discount rate)", "", ""], ["Exit equity value, 100%, end of Year 5", "", ""],
           ["Stake", "", ""], ["Investor IRR and multiple (USD)", "", ""], ["Value retained in USD after 5 years of depreciation", "", ""]],
          first_bold=True)

    doc.add_paragraph("9. Benchmarking and calibration", style="Heading 1")
    guide(doc, "Use a reference as a test only when its source status is VERIFIED or VERIFIED (HISTORICAL). Show the grade "
               "(A to D) and the status separately, with the period and the definition, and say whether the reference is "
               "comparable with the company's figure. Pending, unverified or conflicting figures are context only; a sector "
               "collection rate is not a PERFORM repayment rate. Ranges built on one or two peers are anecdotal.")
    table(doc, ["Ratio", "Company", "Reference, period and definition", "Grade", "Status", "Comparable?", "Reading"], blank(4, 7), font=8.5)

    doc.add_paragraph("10. Consumer protection and impact", style="Heading 1")
    guide(doc, "Payment burden by tier on surveyed incomes, implied APR and its disclosure, collection conduct, complaints, "
               "and evidence of ownership at the end of the plan.")
    table(doc, ["Tier", "Payment burden", "Implied APR", "Evidence status", "Action"],
          [[f"{i}", "", "", "", ""] for i in range(1, 6)], font=8.5)

    doc.add_paragraph("11. Readiness gates and outstanding diligence", style="Heading 1")
    guide(doc, "Report the workbook's decision as the Investment_Readiness sheet computes it, on evidence only: STOP when a "
               "test fails (master check, covenant breach, negative contribution); GO when all 23 gates are met; CONDITIONAL GO "
               "when all 13 critical gates are met; otherwise STOP, evidence incomplete. A manual gate counts only when the sheet "
               "records where the evidence is held and who signed it off. The decision measures whether the evidence is complete; "
               "the recommendation in section 1 is the deal team's judgement. Where the two differ, say why, and write the "
               "conditions so that disbursement waits until the critical gates they address are evidenced.")
    table(doc, ["Gates met (of 23)", "Critical gates met (of 13)", "Failed tests", "Workbook decision", "Deal team recommendation"],
          blank(1, 5), font=8.5)
    guide(doc, "Translate every open gate into a condition precedent, a covenant or an accepted risk. Copy open items from "
               "the diligence checklist (Template T02).")
    table(doc, ["Gate or diligence item", "Critical", "Status", "Evidence held at", "Signed off by", "Treatment"], blank(8, 6), font=8.5)

    doc.add_paragraph("12. Risks and mitigants", style="Heading 1")
    guide(doc, "Rate likelihood and impact as High, Medium or Low before and after mitigation. Keep the list to the risks "
               "that could change the decision.")
    risks = ["Credit deterioration in existing tiers", "Untested credit on new tiers", "Currency depreciation and pricing power",
             "Funding drought or facility delay", "Regulatory change on lockout, APR or data", "Fraud and ghost sales",
             "Platform or payment channel failure", "Key person and governance"]
    table(doc, ["No.", "Risk", "Likelihood", "Impact", "Mitigant", "Residual", "Owner"],
          [[f"R{i + 1}", r, "", "", "", "", ""] for i, r in enumerate(risks)], widths=(1.0, 4.6, 1.8, 1.6, 4.2, 1.8, 1.6), font=8.5)

    doc.add_paragraph("Annex A. Sources and verification status", style="Heading 1")
    guide(doc, "List every external figure quoted in the memo with its source, the page read, its grade (A to D) and its status "
               "(VERIFIED, VERIFIED (HISTORICAL), PENDING PRIMARY DOCUMENT, UNVERIFIED, CONFLICTING SOURCES, NOT USED).")
    table(doc, ["Ref.", "Figure as used", "Source and page", "Grade", "Status"], blank(5, 5))
    doc.add_paragraph("Annex B. Approvals", style="Heading 1")
    table(doc, ["Role", "Name", "Decision", "Date", "Signature"],
          [["Investment committee chair", "", "", "", ""], ["Member", "", "", "", ""], ["Member", "", "", "", ""],
           ["Risk", "", "", "", ""]], first_bold=True)
    guide(doc, "Decision support template from the Africa Energy Finance Book 2 Templates Pack. It does not constitute investment, "
               "legal, tax or accounting advice.")
    save(doc, out / "AEF_V2_T01_Investment_Memo.docx")


# ================================================================== T03 Customer credit policy
def build_t03(out):
    doc = base_doc("T03", "Customer credit policy")
    cover(doc, "BOOK 2  |  TEMPLATE T03", "Customer credit policy", "PAYGo solar home systems",
          [("Company", "[Company name]"), ("Countries covered", "[Country or countries]"), ("Policy owner", "[Chief Risk Officer or CFO]"),
           ("Approved by", "[Credit Committee / Board], [date]"), ("Effective date", "[Date]"), ("Next review", "[Date, at least annually]")])
    table(doc, ["Version", "Date", "Changes", "Approved by"], [["[0.1]", "[date]", "[First issue]", "[Credit Committee]"]] + blank(2, 4))
    page_break(doc)
    toc(doc)

    doc.add_paragraph("1. Scope and governance", style="Heading 1")
    para(doc, "This policy applies to every PAYGo contract originated, serviced or collected by [Company] in [countries], "
              "whatever the sales channel. It sets the rules for eligibility, affordability, approval, pricing, servicing, "
              "collections, default, repossession and write off, and the monitoring that tells management whether the rules work.")
    para(doc, "The Credit Committee, chaired by [title], approves this policy and every change to it. Its members are [titles]. "
              "Sales management may attend but does not vote on credit matters. The Committee meets at least [monthly] and "
              "reviews the KPIs in Section 9 at each meeting.")
    para(doc, "Any exception to this policy is approved by [title] and recorded in the exceptions log with the reason, the "
              "account and the approver. The log is reported to the Credit Committee every month. Exceptions above "
              "[x]% of monthly originations trigger a review of the policy.")
    para(doc, "The policy is reviewed at least once a year, and earlier when cohort repayment at month 6 or month 12 deviates "
              "from plan by more than [5] percentage points for two consecutive cohorts.")

    doc.add_paragraph("2. Eligibility", style="Heading 1")
    table(doc, ["Criterion", "Rule", "Evidence"],
          [["Identification", "[National ID or accepted alternative]", "[Copy or reference number verified]"],
           ["Age", "[18 years or older]", "[ID]"],
           ["Location", "[Within an active service area]", "[GPS tag at installation]"],
           ["Payment channel", "[Active mobile money account in the customer's name]", "[Wallet number verified]"],
           ["Existing PAYGo contracts", "[No account with the company more than 30 DPD]", "[Platform check]"],
           ["Prohibited segments", "[List]", ""]], widths=(4.0, 7.0, 5.5), first_bold=True)

    doc.add_paragraph("3. Affordability assessment", style="Heading 1")
    para(doc, "The monthly instalment must not exceed the maximum payment burden for the tier, measured on the household's "
              "income in a lean month where seasonality applies. The maximum is a policy choice approved by the Credit "
              "Committee and is reviewed against repayment outcomes.")
    table(doc, ["Tier", "Target segment", "Maximum payment burden", "Minimum deposit", "Maximum tenor"],
          [["1", "[Rural, first time customers]", "[10%]", "[x% of cash price]", "[12 months]"],
           ["2", "", "[10%]", "", "[24 months]"], ["3", "", "[10%]", "", "[30 months]"],
           ["4", "", "[10%]", "", "[36 months]"], ["5", "", "[10%]", "", "[48 months]"]], font=8.5)
    para(doc, "Income evidence accepted: [mobile money inflows over at least three months; employer letter; agent assessment "
              "verified by a call centre interview]. Outstanding PAYGo or digital loan instalments are deducted from income "
              "before the burden is computed.")

    doc.add_paragraph("4. Scoring and approval", style="Heading 1")
    table(doc, ["Score band", "Decision", "Highest tier available", "Conditions"],
          [["[A]", "[Approve]", "[Tier 5]", ""], ["[B]", "[Approve]", "[Tier 3]", "[Higher deposit for Tier 3]"],
           ["[C]", "[Refer to credit desk]", "[Tier 2]", ""], ["[D]", "[Decline]", "", ""]], first_bold=True)
    para(doc, "Manual review is required when [identity or location data do not match; the applicant has a restructured "
              "account; the agent has a flagged cohort quality ranking]. Agents cannot override a decline. Referred "
              "applications are decided by the credit desk within [two] working days.")

    doc.add_paragraph("5. Pricing and disclosure", style="Heading 1")
    table(doc, ["Tier", "Cash price", "Deposit", "Daily rate", "Tenor", "Total contract value", "Nominal APR", "Effective annual rate"],
          [[f"{i}", "", "", "", "", "", "", ""] for i in range(1, 6)], font=8)
    para(doc, "Before activation the customer receives, in [language], the cash price, the deposit, the daily rate, the "
              "number of days, the total amount payable, the implied annual rate on the basis required by [applicable rule], "
              "the lockout rules and the complaints channel. Early repayment of the full balance is allowed at any time "
              "[without penalty].")

    doc.add_paragraph("6. Servicing and lockout", style="Heading 1")
    table(doc, ["Event", "Action", "Channel", "Timing"],
          [["Credit about to expire", "[Reminder]", "[SMS]", "[2 days before]"],
           ["Credit expired", "[Device locks]", "[Automatic]", "[Day 0, after a grace of x days]"],
           ["Payment received", "[Device unlocks for the days paid]", "[Automatic]", "[Within minutes]"],
           ["Final payment", "[Permanent unlock and ownership notice]", "[Automatic and SMS]", "[On receipt]"]], first_bold=True)
    para(doc, "Days past due are measured as the shortfall against the payment schedule, expressed in days of the daily "
              "rate. Days without credit are recorded separately. The same definition is used for collections, provisioning "
              "and lender reporting.")

    doc.add_paragraph("7. Collections", style="Heading 1")
    table(doc, ["DPD bucket", "Action", "Channel", "Responsible", "Escalation"],
          [["1 to 7", "[Reminder]", "[SMS, call]", "[Call centre]", ""],
           ["8 to 30", "[Call; payment plan offer]", "[Call]", "[Call centre]", "[Agent visit if no contact]"],
           ["31 to 60", "[Visit]", "[Field]", "[Collections agent]", "[Supervisor]"],
           ["61 to 90", "[Final notice; repossession assessment]", "[Field]", "[Supervisor]", "[Credit desk]"],
           ["91 to 180", "[Repossession where criteria are met]", "[Field]", "[Repossession team]", "[Credit Committee report]"],
           ["Over 180", "[Default; write off review]", "", "[Credit desk]", ""]], font=8.5)
    para(doc, "Collectors identify themselves, contact customers only between [hours], do not contact third parties about "
              "the debt, and never use threats or public shaming. Collection incentives are paid on cured accounts, not on "
              "repossessions.")
    para(doc, "A contract may be restructured at most [once] in its life, only after a hardship assessment and with the "
              "approval of [title]. Restructured accounts keep their days past due history; they are reported separately "
              "and are not eligible for the borrowing base until they have made [three] consecutive payments.")

    doc.add_paragraph("8. Default, repossession and write off", style="Heading 1")
    para(doc, "An account is in default at [180] days past due. The default definition, the write off trigger and the "
              "repossession trigger are aligned and are disclosed to lenders; any change is approved by the Credit Committee "
              "and history is restated.")
    table(doc, ["Tier", "Repossess when", "Minimum expected net resale value", "Refurbishment standard"],
          [[f"{i}", "", "", ""] for i in range(1, 6)], font=8.5)
    para(doc, "Balances are written off when there is no reasonable expectation of recovery and no later than [x] days past "
              "due, with approval by [title] above [amount]. Recoveries after write off are recorded against the original "
              "account.")

    doc.add_paragraph("9. Monitoring and early warning", style="Heading 1")
    table(doc, ["Indicator", "Early warning level", "Action when breached", "Frequency"],
          [["Operational collection rate, trailing 3 months", "[below x%]", "[Collections review; tighten approvals]", "[Monthly]"],
           ["RR PvP at 90 days by monthly cohort (PAYGo PERFORM 2026)", "[below x%]", "[Review origination channel and agents]", "[Monthly]"],
           ["PAR30", "[above x%]", "[Credit Committee review]", "[Monthly]"],
           ["Cohort repayment at M3 against plan", "[gap above x points]", "[Review origination channel and agents]", "[Monthly]"],
           ["Deposit only accounts", "[above x% of sales]", "[Fraud review]", "[Monthly]"],
           ["Exceptions to policy", "[above x% of sales]", "[Policy review]", "[Monthly]"]], first_bold=True, font=8.5)

    doc.add_paragraph("10. Data and model governance", style="Heading 1")
    para(doc, "Customer and payment data are kept for [x] years in line with [applicable data protection rules]. The servicing "
              "platform is reconciled to the general ledger every month for gross receivables, collections and write offs. "
              "Scorecards and provisioning parameters are validated at least once a year against cohort outcomes, and every "
              "change is recorded with its rationale and approval.")

    doc.add_paragraph("Annex. Definitions", style="Heading 1")
    table(doc, ["Term", "Definition"],
          [["Operational collection rate", "Instalments collected ÷ instalments due, both excluding deposits; an operational metric, not a PERFORM KPI"],
           ["Repayment rate (RR PvP, PAYGo PERFORM 2026)", "Payments applied to due instalments to date ÷ instalments due to date, on contract data; deposits, prepayments, penalties, fees and subsidies excluded (GOGLA Technical Guide, June 2026)"],
           ["Days past due", "Schedule shortfall expressed in days of the daily rate"],
           ["Default", "Account at or beyond the default threshold in Section 8"],
           ["Payment burden", "Monthly instalment ÷ monthly household income"],
           ["PAR30", "Gross receivables of accounts more than 30 days past due ÷ gross receivables"],
           ["Restructuring", "Any change to the payment schedule agreed with a customer in arrears"]], widths=(4.0, 12.5), first_bold=True)
    guide(doc, "Template from the Africa Energy Finance Book 2 Templates Pack. Confirm every rule against the law of each country "
               "of operation with local counsel before adoption.")
    save(doc, out / "AEF_V2_T03_Customer_Credit_Policy.docx")


# ================================================================== T08 Business model canvas
CANVAS_Q = {
    "Key partners": "Hardware suppliers, mobile money operators, lenders, RBF programmes, retail partners. Which partner could stop the business?",
    "Key activities": "Underwriting, logistics, installation, servicing, collections, repossession, data and reporting.",
    "Key resources": "Lockout platform, customer data, agent network, receivables book, funding lines.",
    "Value proposition": "What the household gets per day of payment compared with kerosene, batteries and phone charging; ownership at the end.",
    "Customer relationships": "Daily payments, lockout, reminders, service visits, upgrades after ownership.",
    "Channels": "Direct agents, retail partners, installers. Who selects the customer, and how are they paid?",
    "Customer segments": "Segments by tier and income type; seasonality; first time or repeat customers.",
    "Cost structure": "Landed hardware, installation, warranty, CAC (narrow and fully loaded), servicing, central costs, funding cost.",
    "Credit engine": "Default hazard and collection rate by tier, observed or proxy; DPD definition; recoveries.",
    "Revenue streams": "Hardware at cash price, financing income over the tenor, RBF, add on services.",
    "Funding stack": "Equity, hard currency term debt, local currency receivables facility, securitisation; currency match.",
    "Impact and consumer protection": "Payment burden, APR and disclosure, complaints, ownership evidence.",
    "Key metrics": "PAYGo PERFORM 2026 KPIs (company reported); operational collection rate; PAR30; cohort repayment against plan; LTV to CAC; payback; peak equity.",
}
CANVAS_EX = {
    "Key partners": "USD hardware suppliers; two mobile money operators; local bank (proposed KVS 4.5bn facility); USD 3.0m term lender; impact fund.",
    "Key activities": "Agent sales and installation; collections through lockout; repossession not yet operating (observed LGD proxy about 99%).",
    "Key resources": "Lockout platform; 24 months of portfolio history; agent network; receivables book.",
    "Value proposition": "Light, TV and refrigeration paid by the day; ownership after 12 to 48 months.",
    "Customer relationships": "Daily mobile money payments; reminders; lockout on expiry; permanent unlock at the end of the plan.",
    "Channels": "Direct agents paid by commission; installers for Tiers 3 to 5.",
    "Customer segments": "Rural first time buyers (Tier 1), rural and peri urban households (Tiers 2 and 3), urban households and small businesses on a weak grid (Tiers 4 and 5, new).",
    "Cost structure": "USD hardware; installation; warranty; commission and marketing; central costs; facility at 16% and term debt at 10%.",
    "Credit engine": "Calibrated hazards 4.55%, 3.38% and 2.47% a month for Tiers 1 to 3; Tiers 4 and 5 on proxy values without history.",
    "Revenue streams": "Hardware revenue at cash price; PAYGo financing income; sales based RBF.",
    "Funding stack": "USD 9.0m equity; USD 3.0m term loan; KVS 4.5bn local currency facility (proposed).",
    "Impact and consumer protection": "Payment burden above the model's 10% policy threshold for Tiers 2 to 4; Tier 1 implied APR 106%; no ownership evidence yet.",
    "Key metrics": "Operational collection rate 69.3% over the last twelve months (not a PERFORM KPI); PAR30 17.0%; calibrated investor IRR 29.0%; readiness 5 of 23 gates, workbook decision STOP (8 of 13 critical gates open).",
}


def _canvas(doc, content, example):
    t = doc.add_table(rows=4, cols=5)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    a = t.cell(0, 0).merge(t.cell(1, 0))
    v = t.cell(0, 2).merge(t.cell(1, 2))
    s = t.cell(0, 4).merge(t.cell(1, 4))
    cs = t.cell(2, 0).merge(t.cell(2, 1))
    rv = t.cell(2, 3).merge(t.cell(2, 4))
    fs = t.cell(3, 0).merge(t.cell(3, 1))
    km = t.cell(3, 3).merge(t.cell(3, 4))
    cells = {"Key partners": a, "Key activities": t.cell(0, 1), "Key resources": t.cell(1, 1), "Value proposition": v,
             "Customer relationships": t.cell(0, 3), "Channels": t.cell(1, 3), "Customer segments": s, "Cost structure": cs,
             "Credit engine": t.cell(2, 2), "Revenue streams": rv, "Funding stack": fs,
             "Impact and consumer protection": t.cell(3, 2), "Key metrics": km}
    for k, c in cells.items():
        c.text = ""
        p = c.paragraphs[0]
        r = p.add_run(k.upper())
        r.bold, r.font.size, r.font.color.rgb = True, Pt(8), GREEN
        p2 = c.add_paragraph()
        r = p2.add_run(content[k])
        r.font.size = Pt(8.5)
        if not example:
            r.italic, r.font.color.rgb = True, GREY
        if k in ("Credit engine", "Funding stack", "Impact and consumer protection", "Key metrics"):
            shade(c, "F2EEE3")
    for i, row in enumerate(t.rows):
        row.height = Cm(4.2 if i < 2 else 3.0)
    return t


def build_t08(out):
    doc = base_doc("T08", "PAYGo business model canvas", landscape=True)
    p = doc.add_paragraph()
    r = p.add_run("PAYGo business model canvas")
    r.font.size, r.bold, r.font.color.rgb = Pt(18), True, GREEN
    guide(doc, "Nine classic blocks plus four PAYGo blocks (shaded): the credit engine, the funding stack, impact and consumer "
               "protection, and the metrics that tell management whether the model works. Replace the grey questions with the "
               "company's answers; keep each block to a few lines.")
    para(doc, "[Company name]  |  [Date]  |  Prepared by [name]")
    _canvas(doc, CANVAS_Q, example=False)
    page_break(doc)
    p = doc.add_paragraph()
    r = p.add_run("Worked example: SolaraPay Ltd (fictional)")
    r.font.size, r.bold, r.font.color.rgb = Pt(16), True, GREEN
    guide(doc, "Filled from CASE 2, the SolaraPay case study of Book 2. SolaraPay and the Republic of Kivara are fictional; figures come from the case workbook.")
    _canvas(doc, CANVAS_EX, example=True)
    page_break(doc)
    doc.add_paragraph("Three tests before the canvas is final", style="Heading 1")
    bullets(doc, ["Cash test: does the cost structure, read with the funding stack, show where the cash for the receivables book comes from in each of the next three years?",
                  "Credit test: is every number in the credit engine block observed in company data, and if not, is it labelled as a proxy?",
                  "Customer test: does the value proposition hold at the payment burden shown in the impact block, in a lean month?"])
    save(doc, out / "AEF_V2_T08_Business_Model_Canvas.docx")


def build_all(out):
    build_t01(out)
    build_t03(out)
    build_t08(out)
