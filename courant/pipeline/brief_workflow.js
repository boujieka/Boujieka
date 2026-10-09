export const meta = {
  name: 'courant-brief',
  description: 'Write a sourced decision brief for one utility from verified data, adversarially fact-check it, then correct it',
  phases: [
    { title: 'Write', detail: 'brief writer produces brief.json and renders it' },
    { title: 'Check', detail: 'independent adversarial fact-checker' },
    { title: 'Fix', detail: 'apply verified corrections and re-render' },
  ],
}

// args: { ud, utility, country, decision, audience, paged_dir, example_html, lang }
const A = args
const RENDER = `python3 -I /home/user/Boujieka/courant/pipeline/render_brief.py ${A.ud} ${A.ud}/brief.html`

const SCHEMA_DOC = `
brief.json format (French text):
{
 "title": "Note <Utility> 2026"  (2-4 words, page name),
 "eyebrow": "Note de décision · <Utility> (<Pays>) · données <years> · octobre 2026",
 "headline": "one-sentence thesis: the most decision-relevant finding",
 "audience_and_sources": "Destinataires … Sources : … Chaque chiffre renvoie au document et à la page ; survolez une référence pour lire la citation exacte.",
 "decision_question": "the decision question",
 "computations": [ {"id": "loss_pt", "expr": "V12 / 100 * V40", "decimals": 1, "unit": "Mds KES", "scale": 0.001} ],
 "key_messages": [ {"figure": "21,2 %" or "[[C:id]]", "figure_label": "short label", "text": "… [[V12]] …", "tag": "fact|calc|interp"} ]  (4-6 items),
 "sections": [ {"heading": "…", "blocks": [
     {"type": "p", "text": "…", "tag": "fact|calc|interp|"},
     {"type": "list", "items": [{"text": "…", "tag": "…"}]},
     {"type": "chart", "kind": "grouped|stacked", "title": "…", "years": [2019,…], "series": [{"label": "…", "values": {"2019": "V12", "2020": "C:x"}}], "scale": 0.001, "decimals": 0, "unit_label": "Mds KES", "caption": "sources … [[V12]] …", "label_series": 0, "top_labels": {"2020": "C:cov20"}, "top_label_unit": " %"},
     {"type": "table", "columns": ["", "2022", "2023"], "rows": [{"label": "…", "cells": ["V1", "C:x", "texte"], "decimals": 1, "suffix": " %", "scale": 1}], "note": "…"}
 ]} ]  (4-6 sections),
 "options": [ {"title": "A. …", "text": "…"} ]  (3-5 options to investigate, not recommendations),
 "watch": ["indicator to monitor", …],
 "limits": ["specific limits of the sources/analysis", …],
 "footer_units": "units and fiscal-year convention"
}
Markup inside text: [[V<n>]] = source chip for verified value n; [[S<n>]] = chip for verified signal n; [[C:<id>]] = formatted computation result; **bold**.
Computations: expr is Python arithmetic over V<n> names and earlier computation ids; scale multiplies the result (e.g. 0.001 to turn millions into billions). Use computations for EVERY derived number (ratios, differences, growth, per-unit values). Never type a derived number by hand.
Charts/tables may reference V<n> or C:<id>. A chart's series must share one unit; use "scale" to convert.`

const WRITER = `You are a senior power-sector analyst (utility finance, regulation, Sub-Saharan Africa) writing a decision brief in French for ${A.audience}.
Utility: ${A.utility} (${A.country}). Decision question to answer: ${A.decision}

Inputs:
- ${A.ud}/index.txt : every VERIFIED value (V<n>) and signal (S<n>) extracted from official documents, with item, fiscal year, value, unit, document, page and definition notes. ONLY these may be cited.
- ${A.ud}/verified.json : same data with exact quotes (values[n], signals[n]).
- ${A.ud}/docs.json : document labels.
- ${A.paged_dir} : full source texts with "=== PAGE n ===" markers, to understand context and definitions (do not cite pages that are not in index.txt).
- Quality and style reference (a finished brief on another utility, already fact-checked): ${A.example_html}. Match its rigour: definitions stated, scope changes flagged, inferences tagged "interp", options framed as things to investigate.

Method:
1. Explore the index; pick the 4-6 findings that matter most for the decision. Prefer analyses a dashboard would not show: decomposition of the financial gap, cross-source contradictions, trends hidden by definition changes (e.g. exports, pass-through revenue, FX), government arrears, audit findings, liquidity.
2. Check scopes before comparing numbers (same definition across years? restated? company vs group? pass-through included?). When two sources disagree, say so.
3. Write ${A.ud}/brief.json following this format:
${SCHEMA_DOC}
4. Tag every paragraph/list item: "fact" (directly sourced), "calc" (computed), "interp" (your judgement). Every fact needs at least one [[V]] or [[S]] chip next to it.
5. Run: ${RENDER}
   Fix any RENDER ERRORS and re-run until it succeeds.
6. Return a short summary of the brief's main messages and any data problems you met.`

const CHECK_SCHEMA = {
  type: 'object',
  properties: {
    issues: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['blocking', 'important', 'minor'] },
      where: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' },
    }, required: ['severity', 'where', 'problem', 'evidence', 'fix'] } },
    checked_ok: { type: 'array', items: { type: 'string' } },
  },
  required: ['issues', 'checked_ok'],
}

const CHECKER = `You are an adversarial fact-checker. A decision brief on ${A.utility} (${A.country}) will go to ministers and lenders. Find errors before it does. Do not praise. No web.
Files: brief source ${A.ud}/brief.json, rendered ${A.ud}/brief.html; verified data ${A.ud}/verified.json (values[n] = V<n>, signals[n] = S<n>, with doc, found_page, quote, definition_note); index ${A.ud}/index.txt; source texts ${A.paged_dir} (=== PAGE n === markers; doc key = file name).
Check: (1) does each cited page support the sentence next to it (open the page)? (2) are computations right and do they mix scopes (pass-through vs base revenue, company vs group, restated figures, fiscal-year labels, units KShs '000 vs millions vs billions, annual average vs end-period)? (3) are hand-typed numbers in text consistent with the data? (4) are interpretations overstated or presented as facts? (5) does anything in the sources contradict a main message, or is something decision-critical missing (e.g. a going-concern uncertainty, a qualification, a large government arrear)?
Return issues with severity, exact location, problem, evidence (file + page + quote) and the corrected wording, plus a short list of what you checked and found correct.`

const FIXER = (issues) => `You maintain the decision brief ${A.ud}/brief.json on ${A.utility}. An independent fact-checker raised the issues below. For each: verify it yourself in ${A.ud}/verified.json / ${A.ud}/index.txt / ${A.paged_dir}. If it holds, correct brief.json (wording, computations, citations; add citations only to V/S ids that exist in index.txt). If it does not hold, leave the text and explain why. Then run ${RENDER} until it succeeds.
Return a change log: one line per issue (applied / rejected + reason).
ISSUES:
${JSON.stringify(issues, null, 1)}`

phase('Write')
const written = await agent(WRITER, { label: `write:${A.utility}`, phase: 'Write' })
phase('Check')
const check = await agent(CHECKER, { label: `check:${A.utility}`, phase: 'Check', schema: CHECK_SCHEMA })
const toFix = (check?.issues || []).filter(i => i.severity !== 'minor' || true)
log(`${toFix.length} issues raised (${toFix.filter(i => i.severity === 'blocking').length} blocking, ${toFix.filter(i => i.severity === 'important').length} important)`)
phase('Fix')
const fixed = toFix.length ? await agent(FIXER(toFix), { label: `fix:${A.utility}`, phase: 'Fix' }) : 'no issues'
return { written, check, fixed }
