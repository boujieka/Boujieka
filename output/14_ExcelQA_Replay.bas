Attribute VB_Name = "ExcelQA_Replay"
'==============================================================================
' ExcelQA_Replay: replays 79 red-team cases from 14 and 15_MODEL_REDTEAM_RERUN_v0.8 in
' Microsoft Excel and compares each result with the value LibreOffice 24.2
' produced. NOT RUN BY THE AUTHOR OF THIS MODULE: no Excel was available.
'
' How to use
'   1. Open AEF_SHS_PAYGo_Model_v0.8-dev.xlsx OR SolaraPay_Case_Model_v0.8-dev.xlsx
'      (work on a COPY; the macro restores every input it changes, but save a copy).
'   2. Alt+F11, File > Import File..., choose 14_ExcelQA_Replay.bas.
'   3. Run RunAll (Alt+F8). It runs the cases for the open workbook only
'      (detected from Inputs!C7: "LCY" = default model, "KVS" = SolaraPay case),
'      writes sheet QA_Replay and a CSV of every formula cell value next to the
'      workbook (<name>_formula_values_excel.csv).
'   4. Save the result as .xlsm or copy the QA_Replay sheet out; do not save the
'      tested model over the original.
'
' Value encoding in the case table: n:<number> (decimal point, Val parsing),
' s:<text>, b: (blank). Expected values are LibreOffice results on the rebuild
' of generator commit 813c3d5 (101,517 formulas; DSCR covenant basis at Inputs!C88).
'==============================================================================
Option Explicit

Private Const TOL_REL As Double = 0.000001

Private Function CaseData0() As String
    Dim s As String
    s = s & "Q001|D|1 Baseline: Baseline, no change||OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q002|C|1 Baseline: Baseline, no change||OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q003|D|2 Mode grid: scn=1 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:1.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|3.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q004|D|2 Mode grid: scn=2 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|2.0|n:-0.22905023088217163|44.0|0.0|0|10000000.000000007"
    s = s & vbLf
    s = s & "Q005|D|2 Mode grid: scn=3 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:3.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|2.0|s:n/a: no sign change|48.0|0.0|0|46602939.49451148"
    s = s & vbLf
    s = s & "Q006|C|2 Mode grid: scn=1 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:1.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|3.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q007|C|2 Mode grid: scn=2 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|2.0|s:n/a: no sign change|40.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q008|C|2 Mode grid: scn=3 struct=1 rbf=1 credit=1 dscr_basis=0|Inputs!C5~n:3.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|1.0|s:n/a: no sign change|45.0|0.0|0|41887142.88860103"
    s = s & vbLf
    s = s & "Q009|D|3 Sensitivity: Sens row 6: Base||OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q010|D|3 Sensitivity: Sens row 9: Base: default hazard x1.5|Scenarios!C6~n:1.5|OK|STOP|2.0|n:0.3612809809288786|40.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q011|D|3 Sensitivity: Sens row 12: Base: hardware cost +15%|Scenarios!C9~n:1.15|OK|STOP|2.0|n:0.29528045086580046|38.0|5.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q012|D|3 Sensitivity: Sens row 15: Base: RBF programme off|Inputs!C32~n:0.0|OK|STOP|2.0|n:0.44667965294468104|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q013|C|3 Sensitivity: Sens row 6: Base||OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q014|C|3 Sensitivity: Sens row 9: Base: default hazard x1.5|Scenarios!C6~n:1.5|OK|STOP|4.0|n:0.1121158021782405|39.0|5.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q015|C|3 Sensitivity: Sens row 12: Base: hardware cost +15%|Scenarios!C9~n:1.15|OK|STOP|4.0|n:0.002384271826892627|38.0|5.0|0|9000000.0"
    s = s & vbLf
    CaseData0 = s
End Function

Private Function CaseData1() As String
    Dim s As String
    s = s & "Q016|C|3 Sensitivity: Sens row 15: Base: RBF programme off|Inputs!C32~n:0.0|OK|STOP|4.0|n:0.26448503349872404|11.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q017|D|4 Invalid inputs: scenario = 0|Inputs!C5~n:0.0|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q018|D|4 Invalid inputs: financing structure = -1|Inputs!C60~n:-1.0|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q019|D|4 Invalid inputs: credit data mode = None|Credit_Assumptions!C5~b:|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q020|D|4 Invalid inputs: affordability reviewed switch = -1|Consumer_Risk!C5~n:-1.0|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q021|D|4 Invalid inputs: DSCR covenant basis = None|Inputs!C88~b:|ERROR|STOP|2.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q022|D|4 Invalid inputs: zero depreciation life|Inputs!C45~n:0.0|ERROR|STOP|1.0|s:n/a: no sign change|0|0|3399|0"
    s = s & vbLf
    s = s & "Q023|C|4 Invalid inputs: scenario = 0|Inputs!C5~n:0.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q024|C|4 Invalid inputs: financing structure = -1|Inputs!C60~n:-1.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q025|C|4 Invalid inputs: credit data mode = None|Credit_Assumptions!C5~b:|ERROR|STOP|1.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q026|C|4 Invalid inputs: affordability reviewed switch = -1|Consumer_Risk!C5~n:-1.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q027|C|4 Invalid inputs: DSCR covenant basis = None|Inputs!C88~b:|ERROR|STOP|4.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q028|C|4 Invalid inputs: zero depreciation life|Inputs!C45~n:0.0|ERROR|STOP|3.0|s:n/a: no sign change|0|0|3399|0"
    s = s & vbLf
    s = s & "Q029|D|4b Extended invalid inputs: EXT amortisation period 0|Inputs!C54~n:0.0|ERROR|STOP|1.0|n:0.46403452288193064|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q030|D|4b Extended invalid inputs: EXT facility first month 0|Inputs!C57~n:0.0|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    CaseData1 = s
End Function

Private Function CaseData2() As String
    Dim s As String
    s = s & "Q031|C|4b Extended invalid inputs: EXT amortisation period 0|Inputs!C54~n:0.0|ERROR|STOP|3.0|n:0.29018949366134034|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q032|C|4b Extended invalid inputs: EXT facility first month 0|Inputs!C57~n:0.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q033|D|5 Stress and direction: hazard x1.5|Scenarios!C6~n:1.5|OK|STOP|2.0|n:0.3612809809288786|40.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q034|D|5 Stress and direction: exit multiple 8x|Inputs!C84~n:8.0|OK|STOP|2.0|n:0.5564814283536318|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q035|D|5 Stress and direction: RBF per unit x2|Products!C30~n:10.0;Products!D30~n:30.0;Products!E30~n:50.0|OK|STOP|2.0|n:0.48011585725983064|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q036|D|5 Stress and direction: pre-money 16m|Inputs!C82~n:16000000.0|OK|STOP|2.0|n:0.3216246443571722|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q037|C|5 Stress and direction: hazard x1.5|Scenarios!C6~n:1.5|OK|STOP|4.0|n:0.1121158021782405|39.0|5.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q038|C|5 Stress and direction: exit multiple 8x|Inputs!C84~n:8.0|OK|STOP|4.0|n:0.37663447955964735|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q039|C|5 Stress and direction: RBF per unit x2|Products!C30~n:10.0;Products!D30~n:30.0;Products!E30~n:50.0|OK|STOP|4.0|n:0.31361737318403526|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q040|C|5 Stress and direction: pre-money 16m|Inputs!C82~n:16000000.0|OK|STOP|4.0|n:0.16472794988787431|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q041|D|6 Readiness: Baseline readiness||OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q042|D|6 Readiness: All 16 manual gates Met with where held and signed off|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readines"
    s = s & "s!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Inves"
    s = s & "tment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO|OK|STOP|18.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q043|D|6 Readiness: All manual Met, signed off but no where held|Investment_Readiness!D8~s:Met;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!J18~s:CFO;Investment_Readines"
    s = s & "s!D20~s:Met;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:Met;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!J29~s:CFO|OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q044|D|6 Readiness: All manual Met, where held but not signed off|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x"
    s = s & ";Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x|OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q045|D|6 Readiness: All manual In progress with evidence fields|Investment_Readiness!D8~s:In progress;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:In progress;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:In progress;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:In progress;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:In progress;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:In progress;Investment_Readiness!I13~s:Data room /x;Investment_Re"
    s = s & "adiness!J13~s:CFO;Investment_Readiness!D14~s:In progress;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:In progress;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:In progress;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:In progress;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:In progress;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:In progress;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D"
    s = s & "22~s:In progress;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:In progress;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:In progress;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:In progress;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO|OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    CaseData2 = s
End Function

Private Function CaseData3() As String
    Dim s As String
    s = s & "Q046|D|6 Readiness: All manual Met + DSCR basis 0 (no DSCR covenant)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~"
    s = s & "s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_"
    s = s & "Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0|OK|STOP|19.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q047|D|6 Readiness: All manual Met + DSCR basis 2 (cash basis)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;"
    s = s & "Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readin"
    s = s & "ess!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:2.0|OK|STOP|18.0|n:0.46378697449749107|0.0|2.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q048|D|6 Readiness: DSCR basis 2 only|Inputs!C88~n:2.0|OK|STOP|2.0|n:0.46378697449749107|0.0|2.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q049|C|6 Readiness: Baseline readiness||OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q050|C|6 Readiness: All manual Met, where held but not signed off|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x"
    s = s & ";Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q051|C|6 Readiness: All manual Met + DSCR basis 2 (cash basis)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;"
    s = s & "Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readin"
    s = s & "ess!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:2.0|OK|STOP|20.0|n:0.2900134763363904|0.0|3.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q052|C|6 Readiness: Manual + gate 10 + gate 20 evidence (gate 21 open)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D1"
    s = s & "4~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investmen"
    s = s & "t_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D4"
    s = s & "3~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0|OK|CONDITIONAL GO|22.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q053|C|6 Readiness: All 23 gates evidenced with DSCR basis 2|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;In"
    s = s & "vestment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readines"
    s = s & "s!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:2.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43~n:80.0;P"
    s = s & "ERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|STOP|22.0|n:0.2900134763363904|0.0|3.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q054|C|6 Readiness: GO state, covenant min CR 0.95 (monthly breaches)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14"
    s = s & "~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment"
    s = s & "_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43"
    s = s & "~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6;Inputs!C70~n:0.95|OK|STOP|22.0|n:0.2900134763363904|37.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q055|C|6 Readiness: GO state, statuses typed lower-case  met |Investment_Readiness!D8~s:met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:met;I"
    s = s & "nvestment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readine"
    s = s & "ss!D23~s:met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43~n:80.0;"
    s = s & "PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|GO|23.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q056|C|6 Readiness: GO state, ownership switch on but ownership data removed|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readin"
    s = s & "ess!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Inv"
    s = s & "estment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2"
    s = s & "026!D43~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~b:|OK|CONDITIONAL GO|22.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q057|C|7 Data checks: Vintage_Input cumulative collections fall (F9 < E9)|Vintage_Input!F9~n:400000.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q058|C|7 Data checks: Vintage_Input collections 10x instalments due (D9)|Vintage_Input!D9~n:3170937.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q059|C|7 Data checks: PERFORM_2026 RR@2x numerator above denominator|PERFORM_2026!C43~n:150.0;PERFORM_2026!J43~n:600.0;PERFORM_2026!K43~n:500.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q060|C|7 Data checks: PERFORM_2026 PvFin numerator 5x denominator|PERFORM_2026!C43~n:150.0;PERFORM_2026!F43~n:500.0;PERFORM_2026!G43~n:100.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    CaseData3 = s
End Function

Private Function CaseData4() As String
    Dim s As String
    s = s & "Q061|C|7 Data checks: Credit_Input negative gross receivables with matching negative bucket|Credit_Input!D8~n:-764500.0;Credit_Input!E8~n:-871530.0|ERROR|STOP|2.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q062|C|7 Data checks: FP: Credit_Input Tier 5 history cut to 24 months only (tier misalignment)|Credit_Input!B288~b:;Credit_Input!C288~b:;Credit_Input!D288~b:;Credit_Input!E288~b:;Credit_Input!F288~b:;Credit_Input!G288~b:;Credit_Input!H288~b:;Credit_Input!I288~b:;Credit_Input!J288~b:;Credit_Input!K288~b:;Credit_Input!L288~b:;Credit_Input!M288~b:;Credit_Input!N288~b:;Credit_Input!O288~b:;Credit_Input!P288~b:;Credit_Input!Q288~b:;Credit_Input!R288~b:;Credit_Input!S288~b:;Credit_Input!B289~b:;Credit_Input!C289~b:;Credit_Input!D289~b:;Credit_Input!E289~b:;Credit_Input!F289~b:;Credit_Input!G289~b:;Credit_Input!H289~b:;Credit_Input!I289~b:;Credit_Input!J289~b:;Credit_Input!K289~b:;Credit_Input!L28"
    s = s & "9~b:;Credit_Input!M289~b:;Credit_Input!N289~b:;Credit_Input!O289~b:;Credit_Input!P289~b:;Credit_Input!Q289~b:;Credit_Input!R289~b:;Credit_Input!S289~b:;Credit_Input!B290~b:;Credit_Input!C290~b:;Credit_Input!D290~b:;Credit_Input!E290~b:;Credit_Input!F290~b:;Credit_Input!G290~b:;Credit_Input!H290~b:;Credit_Input!I290~b:;Credit_Input!J290~b:;Credit_Input!K290~b:;Credit_Input!L290~b:;Credit_Input!M290~b:;Credit_Input!N290~b:;Credit_Input!O290~b:;Credit_Input!P290~b:;Credit_Input!Q290~b:;Credit_Input!R290~b:;Credit_Input!S290~b:;Credit_Input!B291~b:;Credit_Input!C291~b:;Credit_Input!D291~b:;Credit_Input!E291~b:;Credit_Input!F291~b:;Credit_Input!G291~b:;Credit_Input!H291~b:;Credit_Input!I291~b:;Cr"
    s = s & "edit_Input!J291~b:;Credit_Input!K291~b:;Credit_Input!L291~b:;Credit_Input!M291~b:;Credit_Input!N291~b:;Credit_Input!O291~b:;Credit_Input!P291~b:;Credit_Input!Q291~b:;Credit_Input!R291~b:;Credit_Input!S291~b:;Credit_Input!B292~b:;Credit_Input!C292~b:;Credit_Input!D292~b:;Credit_Input!E292~b:;Credit_Input!F292~b:;Credit_Input!G292~b:;Credit_Input!H292~b:;Credit_Input!I292~b:;Credit_Input!J292~b:;Credit_Input!K292~b:;Credit_Input!L292~b:;Credit_Input!M292~b:;Credit_Input!N292~b:;Credit_Input!O292~b:;Credit_Input!P292~b:;Credit_Input!Q292~b:;Credit_Input!R292~b:;Credit_Input!S292~b:;Credit_Input!B293~b:;Credit_Input!C293~b:;Credit_Input!D293~b:;Credit_Input!E293~b:;Credit_Input!F293~b:;Credit_In"
    s = s & "put!G293~b:;Credit_Input!H293~b:;Credit_Input!I293~b:;Credit_Input!J293~b:;Credit_Input!K293~b:;Credit_Input!L293~b:;Credit_Input!M293~b:;Credit_Input!N293~b:;Credit_Input!O293~b:;Credit_Input!P293~b:;Credit_Input!Q293~b:;Credit_Input!R293~b:;Credit_Input!S293~b:;Credit_Input!B294~b:;Credit_Input!C294~b:;Credit_Input!D294~b:;Credit_Input!E294~b:;Credit_Input!F294~b:;Credit_Input!G294~b:;Credit_Input!H294~b:;Credit_Input!I294~b:;Credit_Input!J294~b:;Credit_Input!K294~b:;Credit_Input!L294~b:;Credit_Input!M294~b:;Credit_Input!N294~b:;Credit_Input!O294~b:;Credit_Input!P294~b:;Credit_Input!Q294~b:;Credit_Input!R294~b:;Credit_Input!S294~b:;Credit_Input!B295~b:;Credit_Input!C295~b:;Credit_Input!D29"
    s = s & "5~b:;Credit_Input!E295~b:;Credit_Input!F295~b:;Credit_Input!G295~b:;Credit_Input!H295~b:;Credit_Input!I295~b:;Credit_Input!J295~b:;Credit_Input!K295~b:;Credit_Input!L295~b:;Credit_Input!M295~b:;Credit_Input!N295~b:;Credit_Input!O295~b:;Credit_Input!P295~b:;Credit_Input!Q295~b:;Credit_Input!R295~b:;Credit_Input!S295~b:;Credit_Input!B296~b:;Credit_Input!C296~b:;Credit_Input!D296~b:;Credit_Input!E296~b:;Credit_Input!F296~b:;Credit_Input!G296~b:;Credit_Input!H296~b:;Credit_Input!I296~b:;Credit_Input!J296~b:;Credit_Input!K296~b:;Credit_Input!L296~b:;Credit_Input!M296~b:;Credit_Input!N296~b:;Credit_Input!O296~b:;Credit_Input!P296~b:;Credit_Input!Q296~b:;Credit_Input!R296~b:;Credit_Input!S296~b:;Cr"
    s = s & "edit_Input!B297~b:;Credit_Input!C297~b:;Credit_Input!D297~b:;Credit_Input!E297~b:;Credit_Input!F297~b:;Credit_Input!G297~b:;Credit_Input!H297~b:;Credit_Input!I297~b:;Credit_Input!J297~b:;Credit_Input!K297~b:;Credit_Input!L297~b:;Credit_Input!M297~b:;Credit_Input!N297~b:;Credit_Input!O297~b:;Credit_Input!P297~b:;Credit_Input!Q297~b:;Credit_Input!R297~b:;Credit_Input!S297~b:;Credit_Input!B298~b:;Credit_Input!C298~b:;Credit_Input!D298~b:;Credit_Input!E298~b:;Credit_Input!F298~b:;Credit_Input!G298~b:;Credit_Input!H298~b:;Credit_Input!I298~b:;Credit_Input!J298~b:;Credit_Input!K298~b:;Credit_Input!L298~b:;Credit_Input!M298~b:;Credit_Input!N298~b:;Credit_Input!O298~b:;Credit_Input!P298~b:;Credit_In"
    s = s & "put!Q298~b:;Credit_Input!R298~b:;Credit_Input!S298~b:;Credit_Input!B299~b:;Credit_Input!C299~b:;Credit_Input!D299~b:;Credit_Input!E299~b:;Credit_Input!F299~b:;Credit_Input!G299~b:;Credit_Input!H299~b:;Credit_Input!I299~b:;Credit_Input!J299~b:;Credit_Input!K299~b:;Credit_Input!L299~b:;Credit_Input!M299~b:;Credit_Input!N299~b:;Credit_Input!O299~b:;Credit_Input!P299~b:;Credit_Input!Q299~b:;Credit_Input!R299~b:;Credit_Input!S299~b:;Credit_Input!B300~b:;Credit_Input!C300~b:;Credit_Input!D300~b:;Credit_Input!E300~b:;Credit_Input!F300~b:;Credit_Input!G300~b:;Credit_Input!H300~b:;Credit_Input!I300~b:;Credit_Input!J300~b:;Credit_Input!K300~b:;Credit_Input!L300~b:;Credit_Input!M300~b:;Credit_Input!N30"
    s = s & "0~b:;Credit_Input!O300~b:;Credit_Input!P300~b:;Credit_Input!Q300~b:;Credit_Input!R300~b:;Credit_Input!S300~b:;Credit_Input!B301~b:;Credit_Input!C301~b:;Credit_Input!D301~b:;Credit_Input!E301~b:;Credit_Input!F301~b:;Credit_Input!G301~b:;Credit_Input!H301~b:;Credit_Input!I301~b:;Credit_Input!J301~b:;Credit_Input!K301~b:;Credit_Input!L301~b:;Credit_Input!M301~b:;Credit_Input!N301~b:;Credit_Input!O301~b:;Credit_Input!P301~b:;Credit_Input!Q301~b:;Credit_Input!R301~b:;Credit_Input!S301~b:;Credit_Input!B302~b:;Credit_Input!C302~b:;Credit_Input!D302~b:;Credit_Input!E302~b:;Credit_Input!F302~b:;Credit_Input!G302~b:;Credit_Input!H302~b:;Credit_Input!I302~b:;Credit_Input!J302~b:;Credit_Input!K302~b:;Cr"
    s = s & "edit_Input!L302~b:;Credit_Input!M302~b:;Credit_Input!N302~b:;Credit_Input!O302~b:;Credit_Input!P302~b:;Credit_Input!Q302~b:;Credit_Input!R302~b:;Credit_Input!S302~b:;Credit_Input!B303~b:;Credit_Input!C303~b:;Credit_Input!D303~b:;Credit_Input!E303~b:;Credit_Input!F303~b:;Credit_Input!G303~b:;Credit_Input!H303~b:;Credit_Input!I303~b:;Credit_Input!J303~b:;Credit_Input!K303~b:;Credit_Input!L303~b:;Credit_Input!M303~b:;Credit_Input!N303~b:;Credit_Input!O303~b:;Credit_Input!P303~b:;Credit_Input!Q303~b:;Credit_Input!R303~b:;Credit_Input!S303~b:;Credit_Input!B304~b:;Credit_Input!C304~b:;Credit_Input!D304~b:;Credit_Input!E304~b:;Credit_Input!F304~b:;Credit_Input!G304~b:;Credit_Input!H304~b:;Credit_In"
    s = s & "put!I304~b:;Credit_Input!J304~b:;Credit_Input!K304~b:;Credit_Input!L304~b:;Credit_Input!M304~b:;Credit_Input!N304~b:;Credit_Input!O304~b:;Credit_Input!P304~b:;Credit_Input!Q304~b:;Credit_Input!R304~b:;Credit_Input!S304~b:;Credit_Input!B305~b:;Credit_Input!C305~b:;Credit_Input!D305~b:;Credit_Input!E305~b:;Credit_Input!F305~b:;Credit_Input!G305~b:;Credit_Input!H305~b:;Credit_Input!I305~b:;Credit_Input!J305~b:;Credit_Input!K305~b:;Credit_Input!L305~b:;Credit_Input!M305~b:;Credit_Input!N305~b:;Credit_Input!O305~b:;Credit_Input!P305~b:;Credit_Input!Q305~b:;Credit_Input!R305~b:;Credit_Input!S305~b:;Credit_Input!B306~b:;Credit_Input!C306~b:;Credit_Input!D306~b:;Credit_Input!E306~b:;Credit_Input!F30"
    s = s & "6~b:;Credit_Input!G306~b:;Credit_Input!H306~b:;Credit_Input!I306~b:;Credit_Input!J306~b:;Credit_Input!K306~b:;Credit_Input!L306~b:;Credit_Input!M306~b:;Credit_Input!N306~b:;Credit_Input!O306~b:;Credit_Input!P306~b:;Credit_Input!Q306~b:;Credit_Input!R306~b:;Credit_Input!S306~b:;Credit_Input!B307~b:;Credit_Input!C307~b:;Credit_Input!D307~b:;Credit_Input!E307~b:;Credit_Input!F307~b:;Credit_Input!G307~b:;Credit_Input!H307~b:;Credit_Input!I307~b:;Credit_Input!J307~b:;Credit_Input!K307~b:;Credit_Input!L307~b:;Credit_Input!M307~b:;Credit_Input!N307~b:;Credit_Input!O307~b:;Credit_Input!P307~b:;Credit_Input!Q307~b:;Credit_Input!R307~b:;Credit_Input!S307~b:;Credit_Input!B308~b:;Credit_Input!C308~b:;Cr"
    s = s & "edit_Input!D308~b:;Credit_Input!E308~b:;Credit_Input!F308~b:;Credit_Input!G308~b:;Credit_Input!H308~b:;Credit_Input!I308~b:;Credit_Input!J308~b:;Credit_Input!K308~b:;Credit_Input!L308~b:;Credit_Input!M308~b:;Credit_Input!N308~b:;Credit_Input!O308~b:;Credit_Input!P308~b:;Credit_Input!Q308~b:;Credit_Input!R308~b:;Credit_Input!S308~b:;Credit_Input!B309~b:;Credit_Input!C309~b:;Credit_Input!D309~b:;Credit_Input!E309~b:;Credit_Input!F309~b:;Credit_Input!G309~b:;Credit_Input!H309~b:;Credit_Input!I309~b:;Credit_Input!J309~b:;Credit_Input!K309~b:;Credit_Input!L309~b:;Credit_Input!M309~b:;Credit_Input!N309~b:;Credit_Input!O309~b:;Credit_Input!P309~b:;Credit_Input!Q309~b:;Credit_Input!R309~b:;Credit_In"
    s = s & "put!S309~b:;Credit_Input!B310~b:;Credit_Input!C310~b:;Credit_Input!D310~b:;Credit_Input!E310~b:;Credit_Input!F310~b:;Credit_Input!G310~b:;Credit_Input!H310~b:;Credit_Input!I310~b:;Credit_Input!J310~b:;Credit_Input!K310~b:;Credit_Input!L310~b:;Credit_Input!M310~b:;Credit_Input!N310~b:;Credit_Input!O310~b:;Credit_Input!P310~b:;Credit_Input!Q310~b:;Credit_Input!R310~b:;Credit_Input!S310~b:;Credit_Input!B311~b:;Credit_Input!C311~b:;Credit_Input!D311~b:;Credit_Input!E311~b:;Credit_Input!F311~b:;Credit_Input!G311~b:;Credit_Input!H311~b:;Credit_Input!I311~b:;Credit_Input!J311~b:;Credit_Input!K311~b:;Credit_Input!L311~b:;Credit_Input!M311~b:;Credit_Input!N311~b:;Credit_Input!O311~b:;Credit_Input!P31"
    s = s & "1~b:;Credit_Input!Q311~b:;Credit_Input!R311~b:;Credit_Input!S311~b:;Credit_Input!B312~b:;Credit_Input!C312~b:;Credit_Input!D312~b:;Credit_Input!E312~b:;Credit_Input!F312~b:;Credit_Input!G312~b:;Credit_Input!H312~b:;Credit_Input!I312~b:;Credit_Input!J312~b:;Credit_Input!K312~b:;Credit_Input!L312~b:;Credit_Input!M312~b:;Credit_Input!N312~b:;Credit_Input!O312~b:;Credit_Input!P312~b:;Credit_Input!Q312~b:;Credit_Input!R312~b:;Credit_Input!S312~b:;Credit_Input!B313~b:;Credit_Input!C313~b:;Credit_Input!D313~b:;Credit_Input!E313~b:;Credit_Input!F313~b:;Credit_Input!G313~b:;Credit_Input!H313~b:;Credit_Input!I313~b:;Credit_Input!J313~b:;Credit_Input!K313~b:;Credit_Input!L313~b:;Credit_Input!M313~b:;Cr"
    s = s & "edit_Input!N313~b:;Credit_Input!O313~b:;Credit_Input!P313~b:;Credit_Input!Q313~b:;Credit_Input!R313~b:;Credit_Input!S313~b:;Credit_Input!B314~b:;Credit_Input!C314~b:;Credit_Input!D314~b:;Credit_Input!E314~b:;Credit_Input!F314~b:;Credit_Input!G314~b:;Credit_Input!H314~b:;Credit_Input!I314~b:;Credit_Input!J314~b:;Credit_Input!K314~b:;Credit_Input!L314~b:;Credit_Input!M314~b:;Credit_Input!N314~b:;Credit_Input!O314~b:;Credit_Input!P314~b:;Credit_Input!Q314~b:;Credit_Input!R314~b:;Credit_Input!S314~b:;Credit_Input!B315~b:;Credit_Input!C315~b:;Credit_Input!D315~b:;Credit_Input!E315~b:;Credit_Input!F315~b:;Credit_Input!G315~b:;Credit_Input!H315~b:;Credit_Input!I315~b:;Credit_Input!J315~b:;Credit_In"
    s = s & "put!K315~b:;Credit_Input!L315~b:;Credit_Input!M315~b:;Credit_Input!N315~b:;Credit_Input!O315~b:;Credit_Input!P315~b:;Credit_Input!Q315~b:;Credit_Input!R315~b:;Credit_Input!S315~b:;Credit_Input!B316~b:;Credit_Input!C316~b:;Credit_Input!D316~b:;Credit_Input!E316~b:;Credit_Input!F316~b:;Credit_Input!G316~b:;Credit_Input!H316~b:;Credit_Input!I316~b:;Credit_Input!J316~b:;Credit_Input!K316~b:;Credit_Input!L316~b:;Credit_Input!M316~b:;Credit_Input!N316~b:;Credit_Input!O316~b:;Credit_Input!P316~b:;Credit_Input!Q316~b:;Credit_Input!R316~b:;Credit_Input!S316~b:;Credit_Input!B317~b:;Credit_Input!C317~b:;Credit_Input!D317~b:;Credit_Input!E317~b:;Credit_Input!F317~b:;Credit_Input!G317~b:;Credit_Input!H31"
    s = s & "7~b:;Credit_Input!I317~b:;Credit_Input!J317~b:;Credit_Input!K317~b:;Credit_Input!L317~b:;Credit_Input!M317~b:;Credit_Input!N317~b:;Credit_Input!O317~b:;Credit_Input!P317~b:;Credit_Input!Q317~b:;Credit_Input!R317~b:;Credit_Input!S317~b:;Credit_Input!B318~b:;Credit_Input!C318~b:;Credit_Input!D318~b:;Credit_Input!E318~b:;Credit_Input!F318~b:;Credit_Input!G318~b:;Credit_Input!H318~b:;Credit_Input!I318~b:;Credit_Input!J318~b:;Credit_Input!K318~b:;Credit_Input!L318~b:;Credit_Input!M318~b:;Credit_Input!N318~b:;Credit_Input!O318~b:;Credit_Input!P318~b:;Credit_Input!Q318~b:;Credit_Input!R318~b:;Credit_Input!S318~b:;Credit_Input!B319~b:;Credit_Input!C319~b:;Credit_Input!D319~b:;Credit_Input!E319~b:;Cr"
    s = s & "edit_Input!F319~b:;Credit_Input!G319~b:;Credit_Input!H319~b:;Credit_Input!I319~b:;Credit_Input!J319~b:;Credit_Input!K319~b:;Credit_Input!L319~b:;Credit_Input!M319~b:;Credit_Input!N319~b:;Credit_Input!O319~b:;Credit_Input!P319~b:;Credit_Input!Q319~b:;Credit_Input!R319~b:;Credit_Input!S319~b:;Credit_Input!B320~b:;Credit_Input!C320~b:;Credit_Input!D320~b:;Credit_Input!E320~b:;Credit_Input!F320~b:;Credit_Input!G320~b:;Credit_Input!H320~b:;Credit_Input!I320~b:;Credit_Input!J320~b:;Credit_Input!K320~b:;Credit_Input!L320~b:;Credit_Input!M320~b:;Credit_Input!N320~b:;Credit_Input!O320~b:;Credit_Input!P320~b:;Credit_Input!Q320~b:;Credit_Input!R320~b:;Credit_Input!S320~b:;Credit_Input!B321~b:;Credit_In"
    s = s & "put!C321~b:;Credit_Input!D321~b:;Credit_Input!E321~b:;Credit_Input!F321~b:;Credit_Input!G321~b:;Credit_Input!H321~b:;Credit_Input!I321~b:;Credit_Input!J321~b:;Credit_Input!K321~b:;Credit_Input!L321~b:;Credit_Input!M321~b:;Credit_Input!N321~b:;Credit_Input!O321~b:;Credit_Input!P321~b:;Credit_Input!Q321~b:;Credit_Input!R321~b:;Credit_Input!S321~b:;Credit_Input!B322~b:;Credit_Input!C322~b:;Credit_Input!D322~b:;Credit_Input!E322~b:;Credit_Input!F322~b:;Credit_Input!G322~b:;Credit_Input!H322~b:;Credit_Input!I322~b:;Credit_Input!J322~b:;Credit_Input!K322~b:;Credit_Input!L322~b:;Credit_Input!M322~b:;Credit_Input!N322~b:;Credit_Input!O322~b:;Credit_Input!P322~b:;Credit_Input!Q322~b:;Credit_Input!R32"
    s = s & "2~b:;Credit_Input!S322~b:;Credit_Input!B323~b:;Credit_Input!C323~b:;Credit_Input!D323~b:;Credit_Input!E323~b:;Credit_Input!F323~b:;Credit_Input!G323~b:;Credit_Input!H323~b:;Credit_Input!I323~b:;Credit_Input!J323~b:;Credit_Input!K323~b:;Credit_Input!L323~b:;Credit_Input!M323~b:;Credit_Input!N323~b:;Credit_Input!O323~b:;Credit_Input!P323~b:;Credit_Input!Q323~b:;Credit_Input!R323~b:;Credit_Input!S323~b:|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q063|D|2 Mode grid: scn=1 struct=2 rbf=4 credit=1 dscr_basis=0|Inputs!C5~n:1.0;Inputs!C60~n:2.0;Inputs!C34~n:4.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|3.0|n:0.46491198127783817|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q064|D|2 Mode grid: scn=2 struct=1 rbf=2 credit=2 dscr_basis=2|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:2.0;Credit_Assumptions!C5~n:2.0;Inputs!C88~n:2.0|OK|STOP|2.0|n:-0.236576729648254|44.0|5.0|0|10000000.000000004"
    s = s & vbLf
    s = s & "Q065|D|4 Invalid inputs: DSCR covenant basis = 3|Inputs!C88~n:3.0|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q066|D|4b Extended invalid inputs: EXT advance rate 150% T2|Products!D31~n:1.5|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q067|D|4b Extended invalid inputs: EXT negative daily rate T1|Products!C15~n:-25.0|ERROR|STOP|0.0|n:0.4180987412761874|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q068|C|2 Mode grid: scn=1 struct=2 rbf=4 credit=1 dscr_basis=0|Inputs!C5~n:1.0;Inputs!C60~n:2.0;Inputs!C34~n:4.0;Credit_Assumptions!C5~n:1.0;Inputs!C88~n:0.0|OK|STOP|3.0|n:0.29118638881020437|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q069|C|2 Mode grid: scn=2 struct=1 rbf=2 credit=2 dscr_basis=2|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:2.0;Credit_Assumptions!C5~n:2.0;Inputs!C88~n:2.0|OK|STOP|4.0|s:n/a: no sign change|40.0|5.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q070|C|4 Invalid inputs: DSCR covenant basis = 3|Inputs!C88~n:3.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q071|C|4b Extended invalid inputs: EXT advance rate 150% T2|Products!D31~n:1.5|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q072|C|4b Extended invalid inputs: EXT negative daily rate T1|Products!C15~n:-25.0|ERROR|STOP|2.0|n:0.2450820926399081|16.0|5.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q073|D|6 Readiness: DSCR basis 0 only|Inputs!C88~n:0.0|OK|STOP|3.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q074|C|6 Readiness: DSCR basis 2 only|Inputs!C88~n:2.0|OK|STOP|4.0|n:0.2900134763363904|0.0|3.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q075|C|6 Readiness: DSCR basis 0 only|Inputs!C88~n:0.0|OK|STOP|5.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    CaseData4 = s
End Function

Private Function CaseData5() As String
    Dim s As String
    s = s & "Q076|C|6 Readiness: All 23 gates evidenced (basis 0)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;Investment"
    s = s & "_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:"
    s = s & "Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:0.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43~n:80.0;PERFORM_2"
    s = s & "026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|GO|23.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q077|C|6 Readiness: All 23 gates evidenced but DSCR basis 1 (default)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14"
    s = s & "~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment"
    s = s & "_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C88~n:1.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43"
    s = s & "~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|STOP|22.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q078|C|7 Data checks: Vintage_Input negative units (C9 = -139)|Vintage_Input!C9~n:-139.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q079|C|7 Data checks: Credit_Input period-end dates out of order (B9 earlier than B8)|Credit_Input!B9~n:44957.0|ERROR|STOP|2.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    CaseData5 = s
End Function

Private Function AllCases() As String
    AllCases = CaseData0() & CaseData1() & CaseData2() & CaseData3() & CaseData4() & CaseData5()
End Function

Public Sub RunAll()
    Dim wbTag As String
    Select Case CStr(ThisWorkbookOrActive().Worksheets("Inputs").Range("C7").Value)
        Case "LCY": wbTag = "D"
        Case "KVS": wbTag = "C"
        Case Else
            MsgBox "Inputs!C7 is neither LCY nor KVS: open the default model or the SolaraPay case.", vbExclamation
            Exit Sub
    End Select
    RunCases wbTag
    ExportFormulaValuesCSV
    MsgBox "ExcelQA_Replay finished. See sheet QA_Replay and the CSV next to the workbook.", vbInformation
End Sub

Private Function ThisWorkbookOrActive() As Workbook
    Set ThisWorkbookOrActive = ActiveWorkbook
End Function

Private Sub RunCases(ByVal wbTag As String)
    Dim wb As Workbook: Set wb = ThisWorkbookOrActive()
    Dim ws As Worksheet, lines() As String, f() As String, i As Long, r As Long
    Dim calcMode As Long, t As Double
    Application.DisplayAlerts = False
    On Error Resume Next
    wb.Worksheets("QA_Replay").Delete
    On Error GoTo 0
    Application.DisplayAlerts = True
    Set ws = wb.Worksheets.Add(After:=wb.Worksheets(wb.Worksheets.Count))
    ws.Name = "QA_Replay"
    ws.Range("A1:V1").Value = Array("Case", "Workbook", "Description", "Changes", _
        "Master (Excel)", "Master (LO)", "Decision (Excel)", "Decision (LO)", "Gates (Excel)", "Gates (LO)", _
        "IRR (Excel)", "IRR (LO)", "Breach months (Excel)", "Breach months (LO)", "DSCR years (Excel)", "DSCR years (LO)", _
        "Error cells (Excel)", "Error cells (LO)", "Peak equity USD (Excel)", "Peak equity USD (LO)", "Verdict", "Seconds")
    ws.Range("X1").Value = "Excel " & Application.Version & " build " & Application.Build & ", run " & Format(Now, "yyyy-mm-dd hh:nn")
    calcMode = Application.Calculation
    Application.Calculation = xlCalculationManual
    Application.CalculateFull
    lines = Split(AllCases(), vbLf)
    r = 2
    For i = LBound(lines) To UBound(lines)
        If Len(lines(i)) > 0 Then
            f = Split(lines(i), "|")
            If f(1) = wbTag Then
                t = Timer
                RunOne wb, ws, r, f
                ws.Cells(r, 22).Value = Round(Timer - t, 2)
                r = r + 1
            End If
        End If
    Next i
    ' circular references after the replay (should be none)
    Dim sh As Worksheet, circ As String
    On Error Resume Next
    For Each sh In wb.Worksheets
        If Not sh.CircularReference Is Nothing Then circ = circ & sh.Name & "!" & sh.CircularReference.Address & " "
    Next sh
    On Error GoTo 0
    ws.Range("X2").Value = "Circular references: " & IIf(circ = "", "none", circ)
    Application.Calculation = calcMode
    ws.Columns("A:V").AutoFit
End Sub

Private Sub RunOne(wb As Workbook, ws As Worksheet, ByVal r As Long, f() As String)
    Dim chg() As String, kv() As String, refs() As String, olds() As String
    Dim j As Long, n As Long, rng As Range
    n = 0
    If Len(f(3)) > 0 Then
        chg = Split(f(3), ";")
        n = UBound(chg) - LBound(chg) + 1
    End If
    If n > 0 Then
        ReDim refs(1 To n): ReDim olds(1 To n)
        For j = 1 To n
            kv = Split(chg(LBound(chg) + j - 1), "~")
            refs(j) = kv(0)
            Set rng = RefToRange(wb, refs(j))
            olds(j) = rng.Formula
            SetEncoded rng, kv(1)
        Next j
    End If
    Application.CalculateFull
    Dim masterX As Variant, decX As Variant, gatesX As Variant, irrX As Variant, brX As Variant, dsX As Variant, peX As Variant
    Dim errX As Long
    masterX = CellText(wb, "Checks!C44")
    decX = CellText(wb, "Investment_Readiness!C35")
    gatesX = CellVal(wb, "Investment_Readiness!C4")
    irrX = CellVal(wb, "Valuation!C39")
    brX = CellVal(wb, "KPIs!C64")
    dsX = CellVal(wb, "KPIs!C65")
    peX = CellVal(wb, "KPIs!C57")
    errX = CountErrors(wb)
    ' restore
    If n > 0 Then
        For j = n To 1 Step -1
            RefToRange(wb, refs(j)).Formula = olds(j)
        Next j
    End If
    Application.CalculateFull
    ' write
    ws.Cells(r, 1).Value = f(0): ws.Cells(r, 2).Value = f(1): ws.Cells(r, 3).Value = f(2): ws.Cells(r, 4).Value = "'" & f(3)
    ws.Cells(r, 5).Value = masterX: ws.Cells(r, 6).Value = f(4)
    ws.Cells(r, 7).Value = decX: ws.Cells(r, 8).Value = f(5)
    ws.Cells(r, 9).Value = gatesX: ws.Cells(r, 10).Value = Val(f(6))
    ws.Cells(r, 11).Value = irrX: ws.Cells(r, 12).Value = DecodeShow(f(7))
    ws.Cells(r, 13).Value = brX: ws.Cells(r, 14).Value = Val(f(8))
    ws.Cells(r, 15).Value = dsX: ws.Cells(r, 16).Value = Val(f(9))
    ws.Cells(r, 17).Value = errX: ws.Cells(r, 18).Value = Val(f(10))
    ws.Cells(r, 19).Value = peX: ws.Cells(r, 20).Value = Val(f(11))
    Dim ok As Boolean
    ok = (CStr(masterX) = f(4)) And (CStr(decX) = f(5)) And SameNum(gatesX, Val(f(6))) _
        And SameEnc(irrX, f(7)) And SameNum(brX, Val(f(8))) And SameNum(dsX, Val(f(9))) _
        And (errX = CLng(Val(f(10)))) And SameNum(peX, Val(f(11)))
    ws.Cells(r, 21).Value = IIf(ok, "MATCH", "DIFFERENT")
    If Not ok Then ws.Rows(r).Interior.Color = RGB(255, 230, 230)
End Sub

Private Function RefToRange(wb As Workbook, ByVal ref As String) As Range
    Dim p As Long: p = InStrRev(ref, "!")
    Set RefToRange = wb.Worksheets(Left(ref, p - 1)).Range(Mid(ref, p + 1))
End Function

Private Sub SetEncoded(rng As Range, ByVal enc As String)
    Select Case Left(enc, 2)
        Case "n:": rng.Value = Val(Mid(enc, 3))
        Case "s:"
            If IsNumeric(Mid(enc, 3)) Then rng.Value = "'" & Mid(enc, 3) Else rng.Value = CStr(Mid(enc, 3))
        Case Else: rng.ClearContents
    End Select
End Sub

Private Function DecodeShow(ByVal enc As String) As Variant
    If Left(enc, 2) = "n:" Then DecodeShow = Val(Mid(enc, 3)) Else DecodeShow = Mid(enc, 3)
End Function

Private Function CellVal(wb As Workbook, ByVal ref As String) As Variant
    Dim v As Variant: v = RefToRange(wb, ref).Value2
    If IsError(v) Then CellVal = "ERR:" & CStr(RefToRange(wb, ref).Text) Else CellVal = v
End Function

Private Function CellText(wb As Workbook, ByVal ref As String) As String
    Dim v As Variant: v = RefToRange(wb, ref).Value2
    If IsError(v) Then CellText = "ERR:" & RefToRange(wb, ref).Text Else CellText = CStr(v)
End Function

Private Function SameNum(ByVal a As Variant, ByVal b As Double) As Boolean
    If IsNumeric(a) And Not IsEmpty(a) Then
        SameNum = Abs(CDbl(a) - b) <= TOL_REL * Application.WorksheetFunction.Max(1, Abs(b))
    ElseIf IsEmpty(a) Then
        SameNum = (b = 0)
    Else
        SameNum = False
    End If
End Function

Private Function SameEnc(ByVal a As Variant, ByVal enc As String) As Boolean
    If Left(enc, 2) = "n:" Then
        SameEnc = SameNum(a, Val(Mid(enc, 3)))
    Else
        SameEnc = (CStr(a) = Mid(enc, 3))
    End If
End Function

Private Function CountErrors(wb As Workbook) As Long
    Dim sh As Worksheet, rng As Range, n As Long
    For Each sh In wb.Worksheets
        If sh.Name <> "QA_Replay" Then
            Set rng = Nothing
            On Error Resume Next
            Set rng = sh.UsedRange.SpecialCells(xlCellTypeFormulas, xlErrors)
            On Error GoTo 0
            If Not rng Is Nothing Then n = n + rng.Cells.Count
        End If
    Next sh
    CountErrors = n
End Function

Public Sub ExportFormulaValuesCSV()
    ' Writes sheet, cell, value of every formula cell (numbers with a decimal point,
    ' errors as their text, e.g. #DIV/0!) for comparison with the LibreOffice values.
    Dim wb As Workbook: Set wb = ThisWorkbookOrActive()
    Dim sh As Worksheet, c As Range, fr As Range, fn As Integer, path As String, v As Variant, s As String
    Application.CalculateFull
    path = wb.Path & Application.PathSeparator & Replace(wb.Name, ".xlsx", "") & "_formula_values_excel.csv"
    fn = FreeFile
    Open path For Output As #fn
    Print #fn, "sheet,cell,value"
    For Each sh In wb.Worksheets
        If sh.Name <> "QA_Replay" Then
            Set fr = Nothing
            On Error Resume Next
            Set fr = sh.UsedRange.SpecialCells(xlCellTypeFormulas)
            On Error GoTo 0
            If Not fr Is Nothing Then
                For Each c In fr.Cells
                    v = c.Value2
                    If IsError(v) Then
                        s = c.Text
                    ElseIf IsEmpty(v) Then
                        s = ""
                    ElseIf VarType(v) = vbString Then
                        s = """" & Replace(CStr(v), """", """""") & """"
                    ElseIf VarType(v) = vbBoolean Then
                        s = IIf(v, "TRUE", "FALSE")
                    Else
                        s = Trim(Str(v))
                    End If
                    Print #fn, sh.Name & "," & c.Address(False, False) & "," & s
                Next c
            End If
        End If
    Next sh
    Close #fn
End Sub
