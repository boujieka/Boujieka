# Translation brief: "Bankable Is Not Enough" → French edition "Bancable ne suffit pas"

You are translating a published policy book on African power-sector finance (independent power projects,
public finance, project finance) from English into French for francophone African decision makers
(ministers, ministries of finance, regulators, utilities, lenders). Register: formal, precise, clear French
policy prose, as in World Bank / AfDB French publications. Translate meaning faithfully and completely:
**omit nothing, add nothing, summarise nothing**, no translator's notes, no comments.

## Files
- Input: `en_XX.md` (pandoc Markdown). Output: `fr_XX.md` with the same name number, same structure.
- Mandatory terminology: `glossary.md` (the author's own Appendix G). Use these terms everywhere.
- Check every output with: `python3 check_chunk.py en_XX.md fr_XX.md` → must print `OK`. Fix and re-run until it does.

## Markdown must be preserved exactly
- One paragraph per line, exactly as in the source; same blank-line structure; never wrap lines.
- Headings: keep the `#` level and the trailing attribute block `{#id .class}` byte-for-byte; translate only the text.
- Fenced div lines (`::: kicker`, `::: byline`, `::: titlepage`, `::: copyright`, `:::`) unchanged.
- Footnotes: keep every `[^n]` reference at the matching place and every `[^n]:` definition line (translate its text).
- Links: `[text](url)` → translate the text if it is prose, keep the URL; `<https://...>` unchanged.
- Pipe tables: same rows and columns, one row per line, keep the separator line (`|---|---|`) unchanged,
  keep `\|` escapes; translate cell text. Do not merge or split cells.
- Keep `**bold**`, `*italic*`, escaped characters (`\'`, `\$`, `\[`) valid Markdown.

## Terminology and abbreviations (in addition to glossary.md)
- MoU → « protocole d'accord » (plural « protocoles d'accord »); no French acronym.
- PPA → CAE (contrat d'achat d'électricité); IPP → PIE (producteur indépendant d'électricité).
- utility → société d'électricité; off-taker/buyer → acheteur; sponsor → promoteur; gate → étape de contrôle.
- Sustainable Financial Close → bouclage financier soutenable; lender's test → test du prêteur; state's test → test de l'État.
- IMF → FMI; World Bank → Banque mondiale; African Development Bank (AfDB) → Banque africaine de développement (BAD);
  GDP → PIB; development finance institution (DFI) → institution de financement du développement (IFD);
  SDG → ODD; PPP stays PPP (partenariat public-privé). Keep MW, GW, kWh, MWh, LCOE.
- Labels: Part → Partie; Chapter → Chapitre; Appendix → Annexe; Table → Tableau; Figure → Figure; Box → Encadré;
  "Source: author" → « Source : auteur »; "Note:" → « Note : »; "Implications for decision makers" → « Implications pour les décideurs »;
  "Key message" → « Message clé »; "References" → « Références »; "Two objections" → « Deux objections ».
- Test names: Need/Grid/Buyer/Sovereign/Sponsor and process/Contract/Financing and currency →
  Besoin/Réseau/Acheteur/Souverain/Promoteur et procédure/Contrat/Financement et devise.
  Chapter kicker example: "Chapter 4 · Test 1: Need" → "Chapitre 4 · Test 1 : Besoin".
- Question codes (N1, G3, B2, S4, P1, C5, F2 …), gate numbers, table/figure numbers: keep identical.

## Sources and citations: keep verbatim
- In-text citations in parentheses, e.g. "(World Bank 2024)", "(Eberhard et al. 2016)", "(IMF 2024b)": keep exactly as is,
  so they match the reference list. "n.d." stays.
- Reference-list entries (the paragraphs under « Références »): keep **verbatim in English**; translate only the heading.
- Titles of documents in running text may stay in English in italics. Proper names unchanged.
- Quotations from English sources: translate them into French inside « » (the book states that these are free translations).

## French conventions
- Quotation marks « » with non-breaking spaces inside; non-breaking space before : ; ? ! and before %.
- Numbers: decimal comma, space as thousands separator: 1 125 MW; 2,75; 2,2 %; 11,5 cents US.
- Money: "US$1.6 billion" → « 1,6 milliard de dollars US »; "US$150 million" → « 150 millions de dollars US »;
  in tables, short form « 150 M$ US », « 1,6 Md$ US ». Other currencies likewise (« 450 milliards de nairas »).
- Dates: "July 2016" → « juillet 2016 »; "2014 to 2017" → « de 2014 à 2017 ».

## Front matter (chunk 01 only) — use exactly these texts
- Title page: **BANCABLE NE SUFFIT PAS** / Boucler les contrats électriques de l'Afrique sans ouvrir de passifs publics /
  **Le cadre du bouclage financier soutenable** / 7 tests. 45 questions. 3 étapes de contrôle. 1 décision. / Emmanuel Boujieka Kamga
- Copyright block: first line « Copyright © 2026 Emmanuel Boujieka Kamga. Tous droits réservés. »; translate the other lines;
  « *Première édition, octobre 2026* ». Then **append one more paragraph line at the end of the copyright block, just before
  the closing `:::`**: « Traduit de l'anglais : *Bankable Is Not Enough*, 2026. Les citations de sources en anglais sont des traductions libres. »
  (This is the only addition allowed; the line-count check will report +1 for chunk 01 — that single difference is expected.)
- Hidden headings "Title Page" → "Page de titre", "Copyright" → "Droits d'auteur" (keep their attribute blocks).
- Abbreviations section: give the French expansion of each entry; use the French acronym where the French text uses one
  (CAE, PIE, FMI, BAD, PIB, IFD, ODD) and keep the English acronym in parentheses after the French expansion when useful;
  keep the same number of entries/lines.

## Appendix G (bilingual glossary)
Keep the English and French term columns exactly as they are; translate the third column (meaning) and the surrounding
prose; table header « Anglais | Français | Sens dans ce livre ».
