Attribute VB_Name = "ExcelQA_Replay"
'==============================================================================
' ExcelQA_Replay: replays 62 red-team cases from 14_MODEL_REDTEAM_QA_v0.8 in
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
' s:<text>, b: (blank). Expected values are LibreOffice results.
'==============================================================================
Option Explicit

Private Const TOL_REL As Double = 0.000001

Private Function CaseData0() As String
    Dim s As String
    s = s & "Q001|D|1 Baseline: Baseline, no change||OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q002|C|1 Baseline: Baseline, no change||OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q003|D|2 Mode grid: scn=1 struct=1 rbf=1 credit=1|Inputs!C5~n:1.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q004|D|2 Mode grid: scn=2 struct=1 rbf=1 credit=1|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|2.0|n:-0.22905023088217163|44.0|5.0|0|10000000.000000007"
    s = s & vbLf
    s = s & "Q005|D|2 Mode grid: scn=3 struct=1 rbf=1 credit=1|Inputs!C5~n:3.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|2.0|s:n/a: no sign change|48.0|5.0|0|46602939.49451148"
    s = s & vbLf
    s = s & "Q006|C|2 Mode grid: scn=1 struct=1 rbf=1 credit=1|Inputs!C5~n:1.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|2.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q007|C|2 Mode grid: scn=2 struct=1 rbf=1 credit=1|Inputs!C5~n:2.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|2.0|s:n/a: no sign change|40.0|5.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q008|C|2 Mode grid: scn=3 struct=1 rbf=1 credit=1|Inputs!C5~n:3.0;Inputs!C60~n:1.0;Inputs!C34~n:1.0;Credit_Assumptions!C5~n:1.0|OK|STOP|1.0|s:n/a: no sign change|45.0|5.0|0|41887142.88860103"
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
    s = s & "Q017|D|4 Invalid inputs: scenario = 0|Inputs!C5~n:0.0|ERROR|STOP|0.0|s:n/a: no sign change|0|0|77069|0"
    s = s & vbLf
    s = s & "Q018|D|4 Invalid inputs: financing structure = None|Inputs!C60~b:|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q019|D|4 Invalid inputs: credit data mode = 1.5|Credit_Assumptions!C5~n:1.5|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q020|D|4 Invalid inputs: ownership evidence switch = 0.5|Inputs!C39~n:0.5|ERROR|STOP|1.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q021|D|4 Invalid inputs: zero tenor tier C|Products!C16~n:0.0|ERROR|STOP|0.0|s:n/a: no sign change|0|0|7630|0"
    s = s & vbLf
    s = s & "Q022|D|4 Invalid inputs: zero depreciation life|Inputs!C45~n:0.0|ERROR|STOP|1.0|s:n/a: no sign change|0|0|3399|0"
    s = s & vbLf
    s = s & "Q023|C|4 Invalid inputs: scenario = 0|Inputs!C5~n:0.0|ERROR|STOP|2.0|s:n/a: no sign change|0|0|69056|0"
    s = s & vbLf
    s = s & "Q024|C|4 Invalid inputs: financing structure = None|Inputs!C60~b:|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q025|C|4 Invalid inputs: credit data mode = 1.5|Credit_Assumptions!C5~n:1.5|ERROR|STOP|1.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q026|C|4 Invalid inputs: ownership evidence switch = 0.5|Inputs!C39~n:0.5|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q027|C|4 Invalid inputs: zero tenor tier C|Products!C16~n:0.0|ERROR|STOP|2.0|s:n/a: no sign change|0|0|6250|0"
    s = s & vbLf
    s = s & "Q028|C|4 Invalid inputs: zero depreciation life|Inputs!C45~n:0.0|ERROR|STOP|3.0|s:n/a: no sign change|0|0|3399|0"
    s = s & vbLf
    s = s & "Q029|D|4b Extended invalid inputs: EXT amortisation period 0|Inputs!C54~n:0.0|OK|STOP|2.0|n:0.46403452288193064|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q030|D|4b Extended invalid inputs: EXT collection rate 120% T1|Products!C26~n:1.2|OK|STOP|2.0|n:0.46689406554034646|0.0|4.0|0|10000000.0"
    s = s & vbLf
    CaseData1 = s
End Function

Private Function CaseData2() As String
    Dim s As String
    s = s & "Q031|C|4b Extended invalid inputs: EXT amortisation period 0|Inputs!C54~n:0.0|OK|STOP|4.0|n:0.29018949366134034|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q032|C|4b Extended invalid inputs: EXT collection rate 120% T1|Products!C26~n:1.2|OK|STOP|4.0|n:0.2937684796906917|0.0|4.0|0|9000000.0"
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
    s = s & "Q046|D|6 Readiness: All manual Met + DSCR minimum removed (gate 10 can pass)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readin"
    s = s & "ess!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Inv"
    s = s & "estment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C73~n:-1000000000.0|OK|STOP|19.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q047|D|6 Readiness: Gate 10 only: monthly breaches 0 but DSCR years >0 (default) vs min DSCR removed|Inputs!C73~n:-1000000000.0|OK|STOP|3.0|n:0.46378697449749107|0.0|0.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q048|D|6 Readiness: Default: credit data mode 2 with empty Credit_Input|Credit_Assumptions!C5~n:2.0|OK|STOP|2.0|n:0.46378697449749107|0.0|4.0|0|10000000.0"
    s = s & vbLf
    s = s & "Q049|C|6 Readiness: Baseline readiness||OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q050|C|6 Readiness: All manual Met, signed off but no where held|Investment_Readiness!D8~s:Met;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!J18~s:CFO;Investment_Readines"
    s = s & "s!D20~s:Met;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:Met;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!J29~s:CFO|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q051|C|6 Readiness: All manual In progress with evidence fields|Investment_Readiness!D8~s:In progress;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:In progress;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:In progress;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:In progress;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:In progress;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:In progress;Investment_Readiness!I13~s:Data room /x;Investment_Re"
    s = s & "adiness!J13~s:CFO;Investment_Readiness!D14~s:In progress;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:In progress;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:In progress;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:In progress;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:In progress;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:In progress;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D"
    s = s & "22~s:In progress;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:In progress;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:In progress;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:In progress;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q052|C|6 Readiness: Gate 10 only: monthly breaches 0 but DSCR years >0 (default) vs min DSCR removed|Inputs!C73~n:-1000000000.0|OK|STOP|5.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q053|C|6 Readiness: All 23 gates evidenced|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:Met;Investment_Readiness"
    s = s & "!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readiness!D23~s:Met;Invest"
    s = s & "ment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C73~n:-1000000000.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D43~n:80.0;PERFORM_2"
    s = s & "026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|GO|23.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q054|C|6 Readiness: GO state, Tier 1 hardware USD 200 (negative lifetime contribution)|Investment_Readiness!D8~s:Met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investm"
    s = s & "ent_Readiness!D14~s:Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22"
    s = s & "~s:CFO;Investment_Readiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C73~n:-1000000000.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C"
    s = s & "43~n:150.0;PERFORM_2026!D43~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6;Products!C18~n:200.0|OK|STOP|21.0|n:0.1347081363951482|35.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q055|C|6 Readiness: GO state, gate 2 (critical) Not started|Investment_Readiness!D8~s:Not started;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:Met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:Met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:Met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:Met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:Met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s"
    s = s & ":Met;Investment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:Met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:Met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:Met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:Met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:Met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:Met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_R"
    s = s & "eadiness!D23~s:Met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:Met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:Met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C73~n:-1000000000.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_"
    s = s & "2026!D43~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|STOP|22.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q056|C|6 Readiness: GO state, statuses typed lower-case  met |Investment_Readiness!D8~s:met;Investment_Readiness!I8~s:Data room /x;Investment_Readiness!J8~s:CFO;Investment_Readiness!D9~s:met;Investment_Readiness!I9~s:Data room /x;Investment_Readiness!J9~s:CFO;Investment_Readiness!D10~s:met;Investment_Readiness!I10~s:Data room /x;Investment_Readiness!J10~s:CFO;Investment_Readiness!D11~s:met;Investment_Readiness!I11~s:Data room /x;Investment_Readiness!J11~s:CFO;Investment_Readiness!D12~s:met;Investment_Readiness!I12~s:Data room /x;Investment_Readiness!J12~s:CFO;Investment_Readiness!D13~s:met;Investment_Readiness!I13~s:Data room /x;Investment_Readiness!J13~s:CFO;Investment_Readiness!D14~s:met;I"
    s = s & "nvestment_Readiness!I14~s:Data room /x;Investment_Readiness!J14~s:CFO;Investment_Readiness!D15~s:met;Investment_Readiness!I15~s:Data room /x;Investment_Readiness!J15~s:CFO;Investment_Readiness!D17~s:met;Investment_Readiness!I17~s:Data room /x;Investment_Readiness!J17~s:CFO;Investment_Readiness!D18~s:met;Investment_Readiness!I18~s:Data room /x;Investment_Readiness!J18~s:CFO;Investment_Readiness!D20~s:met;Investment_Readiness!I20~s:Data room /x;Investment_Readiness!J20~s:CFO;Investment_Readiness!D21~s:met;Investment_Readiness!I21~s:Data room /x;Investment_Readiness!J21~s:CFO;Investment_Readiness!D22~s:met;Investment_Readiness!I22~s:Data room /x;Investment_Readiness!J22~s:CFO;Investment_Readine"
    s = s & "ss!D23~s:met;Investment_Readiness!I23~s:Data room /x;Investment_Readiness!J23~s:CFO;Investment_Readiness!D25~s:met;Investment_Readiness!I25~s:Data room /x;Investment_Readiness!J25~s:CFO;Investment_Readiness!D29~s:met;Investment_Readiness!I29~s:Data room /x;Investment_Readiness!J29~s:CFO;Inputs!C73~n:-1000000000.0;Consumer_Risk!C5~n:1.0;Consumer_Risk!C4~n:1.0;Consumer_Risk!C14~s:Validated;Consumer_Risk!C15~s:Validated;Consumer_Risk!D14~s:Validated;Consumer_Risk!D15~s:Validated;Consumer_Risk!E14~s:Validated;Consumer_Risk!E15~s:Validated;Consumer_Risk!F14~s:Validated;Consumer_Risk!F15~s:Validated;Consumer_Risk!G14~s:Validated;Consumer_Risk!G15~s:Validated;PERFORM_2026!C43~n:150.0;PERFORM_2026!D"
    s = s & "43~n:80.0;PERFORM_2026!E43~n:100.0;PERFORM_2026!C108~n:150.0;PERFORM_2026!D108~n:80.0;PERFORM_2026!E108~n:100.0;PERFORM_2026!C173~n:150.0;PERFORM_2026!D173~n:80.0;PERFORM_2026!E173~n:100.0;PERFORM_2026!C238~n:150.0;PERFORM_2026!D238~n:80.0;PERFORM_2026!E238~n:100.0;PERFORM_2026!C303~n:150.0;PERFORM_2026!D303~n:80.0;PERFORM_2026!E303~n:100.0;Inputs!C39~n:1.0;Vintage_Input!BH9~n:0.6|OK|GO|23.0|n:0.2900134763363904|0.0|0.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q057|C|7 Data checks: Vintage_Input cumulative collections fall (F9 < E9)|Vintage_Input!F9~n:400000.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q058|C|7 Data checks: Vintage_Input mode 3 in B9|Vintage_Input!B9~n:3.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q059|C|7 Data checks: PERFORM_2026 RR PvP numerator above denominator|PERFORM_2026!C43~n:150.0;PERFORM_2026!D43~n:120.0;PERFORM_2026!E43~n:100.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q060|C|7 Data checks: PERFORM_2026 OR@2x owners above contracts reaching 2x|PERFORM_2026!C43~n:150.0;PERFORM_2026!L43~n:140.0;PERFORM_2026!M43~n:120.0|ERROR|STOP|3.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    CaseData3 = s
End Function

Private Function CaseData4() As String
    Dim s As String
    s = s & "Q061|C|7 Data checks: PERFORM_2026 PvFin numerator 5x denominator|PERFORM_2026!C43~n:150.0;PERFORM_2026!F43~n:500.0;PERFORM_2026!G43~n:100.0|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    s = s & "Q062|C|7 Data checks: Credit_Input bucket gap of 0.4 (below rounding)|Credit_Input!E8~n:657470.4|OK|STOP|4.0|n:0.2900134763363904|0.0|4.0|0|9000000.0"
    s = s & vbLf
    CaseData4 = s
End Function

Private Function AllCases() As String
    AllCases = CaseData0() & CaseData1() & CaseData2() & CaseData3() & CaseData4()
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
