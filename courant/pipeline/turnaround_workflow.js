export const meta = {
  name: 'courant-turnaround',
  description: 'Draft strategic turnaround orientations for one utility from its verified data and decision brief, challenge them with a sector critic, then revise (status stays draft until human review)',
  phases: [{ title: 'Draft' }, { title: 'Challenge' }, { title: 'Revise' }],
}
// args: { ud, utility, country, paged_dir }
const A = args
const RENDER = `python3 -I /home/user/Boujieka/courant/pipeline/render_turnaround.py ${A.ud} ${A.ud}/turnaround.html`
const FORMAT = `turnaround.json (French):
{ "title": "Redressement <Utility>", "utility": "<Utility>", "status": "draft",
  "headline": "one sentence: the turnaround thesis",
  "scope_note": "who this is for, what it covers, sources (cite [[V]]/[[S]])",
  "diagnosis": [ {"label": "short", "text": "finding with [[V<n>]] / [[S<n>]] chips"} ] (4-6),
  "causal_chain": ["step 1 with evidence", "→ step 2", ...] (4-7 steps, the vicious circle specific to this utility),
  "levers": [ {"horizon": "0-6|6-24|24-60", "title": "…", "why": "evidence-based rationale with chips", "owner": "institution(s) that must act", "kpi": "measurable indicator + baseline value with chip", "preconditions": "…", "risks": "…"} ] (8-12 levers across the three horizons),
  "avoid": ["common mistakes or tempting measures that the evidence argues against"],
  "limits": ["what the public documents cannot tell; what must be checked with management/regulator"] }
Markup: [[V<n>]] cites verified value n, [[S<n>]] verified signal n (ids from index.txt only); **bold**.`

const DRAFT = `You are a senior adviser who has led power-utility turnarounds in Sub-Saharan Africa (commercial recovery, loss reduction, arrears clearance, tariff reform, governance, financing). Draft strategic turnaround orientations in French for the decision-makers of ${A.utility} (${A.country}): ministers of finance and energy, the regulator, the board, lenders.
Inputs: ${A.ud}/index.txt (verified values V<n> and signals S<n>), ${A.ud}/verified.json, ${A.ud}/brief.json or ${A.ud}/brief.html (the fact-checked decision brief: build on it, do not contradict it), source texts in ${A.paged_dir}.
Rules: every diagnostic statement and every baseline must cite verified data. Levers must be specific to this utility's evidence, sequenced, with an owner and a measurable KPI; no generic consulting lists. Respect the utility's structure (distribution vs transmission vs generation vs integrated; private concession vs state-owned). State preconditions and risks honestly, including political and social ones. Do not invent costs, targets or benchmarks that are not in the data; when a target is a proposal, say it is a proposal to be calibrated.
Write ${A.ud}/turnaround.json in this format:
${FORMAT}
Then run: ${RENDER} and fix errors until it succeeds. Return a short summary.`

const SCHEMA = { type: 'object', properties: { issues: { type: 'array', items: { type: 'object', properties: {
  severity: { type: 'string', enum: ['blocking', 'important', 'minor'] }, where: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } },
  required: ['severity', 'where', 'problem', 'fix'] } } }, required: ['issues'] }

const CHALLENGE = `You are a skeptical reviewer for a development-finance institution, with utility-sector experience. Challenge the draft turnaround orientations for ${A.utility} (${A.country}) in ${A.ud}/turnaround.json (rendered ${A.ud}/turnaround.html), using ${A.ud}/verified.json, ${A.ud}/index.txt and sources in ${A.paged_dir}.
Look for: claims not supported by the cited data or misread; levers that do not fit the utility's structure or legal status; missing decision-critical levers (e.g. arrears, governance, tariff path, losses, liquidity, FX, procurement); sequencing errors (things that need prerequisites); unrealistic or invented targets/costs; political naivety; generic advice. Return issues with severity, location, problem and the concrete fix.`

const REVISE = (issues) => `Revise ${A.ud}/turnaround.json for ${A.utility} in light of the review below. Verify each point in the data before applying it; reject points that do not hold and say why. Keep "status": "draft". Run ${RENDER} until it succeeds. Return a change log.
REVIEW:
${JSON.stringify(issues, null, 1)}`

phase('Draft')
const d = await agent(DRAFT, { label: `draft:${A.utility}`, phase: 'Draft' })
phase('Challenge')
const c = await agent(CHALLENGE, { label: `challenge:${A.utility}`, phase: 'Challenge', schema: SCHEMA })
log(`${(c?.issues || []).length} review points`)
phase('Revise')
const r = await agent(REVISE(c?.issues || []), { label: `revise:${A.utility}`, phase: 'Revise' })
return { d, c, r }
