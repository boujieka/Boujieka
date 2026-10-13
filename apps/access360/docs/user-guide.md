# User guide (MVP)

## 1. Account and workspace

1. **Register.** Choose your organisation type. An "accredited organisation" stays *pending* until a platform administrator verifies it: registration alone gives no accredited status.
2. **Switch organisation.** If you belong to several organisations, use the organisation switcher at the top.
3. **Try the demo workspace.** Every figure there is synthetic and marked "Synthetic demo data".

## 2. A project, step by step

1. **Projects → New.** Enter the name, country and stage. The location is optional; you can type it or pick it on the map.
2. **Inputs.** Fill in each section. Units are shown in the labels; percentages are entered as percentages.
   * "Load demo inputs" fills the form with synthetic values. The project's provenance then becomes *illustrative*.
   * Enter **deliverable energy** from your engineering (hourly) design study. The platform does not size the system.
   * If you model grid arrival, cite the country rule you apply. Without it the model stays at *Incomplete inputs*.
3. **Results → Run model.** Read the status first:
   * **Validated:** every integrity check passed, no warning, and a named person has reviewed the assumptions (Inputs → Review).
   * **Warning:** checks passed, but warnings remain or the inputs are not reviewed.
   * **Failed checks** or **Incomplete inputs:** do not use the outputs.
4. **Sensitivity.** 18 cases plus the base, each a full rerun with its own checks, plus a tornado chart of project NPV.
5. **Subsidy.** The smallest capital grant that meets a minimum DSCR and/or equity IRR. If none does, the tool says so.
6. **Milestones.** Track feasibility, permits, tariff approval, financing, construction and commissioning.
7. **Exports.**
   * The Excel export is a live formula model: change a blue input on the Inputs sheet and the Model and Summary sheets recalculate. The `Run_` sheets keep the values of the run for audit.
   * The one-page teaser and the three-page project summary (project and financing; results and sensitivities; risks, readiness and sources) use only model outputs.
   * Both carry the run number, the engine version, the inputs hash and the date.

## 3. Portfolios and the Electrification Acceleration Score

* **Score and gates tab:** set the five mandatory gates (land rights, permits, technical feasibility, environmental and social risk, regulatory restrictions). The sixth gate, model checks, is read from the latest model run and cannot be set by hand. You can also enter months to first power and whether the area is underserved.
* **The score (0 to 100)** combines six criteria: access impact, financial and subsidy efficiency, readiness, speed, productive use and equity. Each criterion shows its points, its explanation and its source; missing data shows as "Data unavailable".
* **Gates override the score.** A failed gate excludes the project whatever its score; an unknown gate puts it under review.
* **Weights and scales** are initial design assumptions of the platform, not a validated standard. You can change them on the portfolio page.
* **Portfolio page:** group projects, rank them, and read the totals. Real and synthetic demo projects are totalled separately. A project whose latest run uses illustrative inputs counts as demo.
* **Site context** (Overview tab): country and region from Natural Earth, nearest Natural Earth places (a map selection, not a settlement inventory) and your own layers within 25 km.

## 3b. Optimizer

The optimizer compares options A to G for one settlement on annual energy and lifecycle cost.
* Options that fail a technical gate are listed with the reason and never ranked.
* It shows the least-cost option, the recommended option and the trade-offs behind the choice.
* It is a screening tool, not a least-cost electrification plan.

## 4. Explore Africa

* Upload GeoJSON or CSV layers with their source, licence and limitations.
* Nothing third party is bundled.
* "Data unavailable" means no layer covers that information yet.

## 5. What the platform does not do

It gives no investment, legal, tax or accounting advice.

This is an analytical modelling treatment and does not constitute a determination of the applicable accounting treatment under IFRS.
