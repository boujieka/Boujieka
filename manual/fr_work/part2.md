## 6. Methodology and key formulas

Formulas are quoted from `model/build_model.py`, with template references replaced by the model's plain cell names. A name such as `p50` is the name used in `model/model_map.json`. "Row" in a time-series formula means the value in the same year.

### 6.1 Hydrology and P-values (03_HYDROLOGY)

Monthly long-term mean flows (Jan to Dec, m³/s): 24, 20, 28, 52, 70, 58, 40, 28, 22, 30, 46, 36. February has 28.25 days, so the year has 365.25. For each month:

```
usable flow = MIN(MAX(flow-eflow,0),q_design)
power (MW)  = MIN(rho*grav*usable*head*eta_t*eta_g/1000000,inst_mw)
energy gross= power*days*24/1000
energy net  = energy gross*avail
spill       = MAX(flow-eflow-q_design,0)
```

Annual statistics:

```
p50    = sum of monthly net energy
p75    = p50*(1-z75*cv)                 z75 = 0.6745
p90    = p50*(1-z90*cv)                 z90 = 1.2816 (one-year P90)
p90_10 = p50*(1-z90*cv*SQRT((1+rho1)/(1-rho1)/10))
cf     = p50/(inst_mw*8.76)
firm_mw= lowest monthly power*avail
```

The ten-year P90 is the P90 of the ten-year average energy. Year-to-year correlation `rho1` (default 0.3) represents the persistence of dry years: it inflates the variance of the average through the factor (1+ρ)/(1−ρ)/n. With CV 15% the Kasiri values are P50 292.5 GWh, P75 262.9, one-year P90 236.3 and ten-year P90 268.3 GWh; P90/P50 is 0.81 and the capacity factor 55.6%. The check row "theoretical power at design flow" (60.5 MW) should be at least the installed capacity.

The sheet notes that energy computed from long-term mean monthly flows overstates energy when flows exceed design flow in some years, and should be replaced by a simulation over the full record when one exists.

### 6.2 Energy (04_GENERATION)

```
p_sel     = CHOOSE(gen_case,p50,p75,p90)
p_len     = CHOOSE(lender_case,p50,p75,p90,p90_10)
drought   = IF(AND(st_drought=1,opyr>=p_drought_start,opyr<p_drought_start+p_drought_len),p_drought,1)
climate   = (1+eff_climate)^((year-base_year)/10)
rampf     = IF(opyr=1,ramp,1)
gen       = opflag*p_sel*eff_flow*drought*climate*rampf
gen_p50   = opflag*p50*eff_flow*climate*rampf
evacuable = gen*evac_ratio
delivered = MIN(evacuable,d_absorb)
gen_len   = opflag*p_len*eff_flow*climate*rampf
```

Installed, available, generated, evacuable, delivered and contracted energy are kept distinct. Curtailment for transmission or grid is `gen-evacuable`; curtailment for lack of demand is `evacuable-delivered`. Contracted energy is the P50 reference `gen_p50`. The lender-case generation `gen_len` does not include the drought factor: the drought is tested separately.

The evacuation ratio comes from *09_GRID*:

```
peak       = peak0*d_dom/base-year domestic demand
absorb_mw  = MAX(0,peak*minload-mustrun)+ic_mw
line_mw    = IF(tx_ready=1,tx_mw,tx_interim)
evac_mw    = MIN(line_mw,absorb_mw)
evac_ratio = MIN(1,evac_mw/inst_mw)
```

Demand on *10_DEMAND* grows by segment with the case growth rate, plus `eff_demg`, and is multiplied by `eff_dem` from COD. Absorbable project energy is the supply gap plus displaceable thermal generation plus contracted exports. Bankable demand is `opflag*MIN(contracted,absorbable*commercial/(domestic+exp_con))`; the worst ratio of bankable to contracted demand in operating years 1 to 5 feeds Gate 2.

### 6.3 Capital cost build-up (05_PLANT_CAPEX, 06_CONSTRUCTION, 08_TRANSMISSION)

Plant cost in real 2026 USD:

| Line | Kasiri (USDm) | Formula or source |
|---|---|---|
| Civil works | 68.0 | Input |
| Hydro-mechanical | 9.0 | Input |
| Electro-mechanical | 33.0 | Input |
| Environmental and social | 5.0 | Input |
| Engineering and supervision | 8.0 | Input |
| Owner's costs | 4.0 | Input |
| Development costs reimbursed at close | 9.0 | `cx_dev = dev_total` from *01A_DEVELOPMENT* |
| Contractor risk premium | 6.6 | `cx_epcprem = (cx_civil+cx_hm+cx_em)*epc_prem` |
| Subtotal | 142.6 | Sum |
| Physical contingency 10% | 14.3 | `capex_base = cx_sub*(1+cont)` |
| Base plant cost | 156.9 | USD 2,614/kW; 1.04x the benchmark of USD 2,515/kW |

The effective plant cost applies the case, the overrun stress, the owner's share of overruns and delay costs, and the flex:

```
eff_capex  = case_capex*(1+st_capex*p_overrun*epc_owner)*(1+fx_capex)
capex_real = capex_base*eff_capex*(1+delay_cost*eff_delay*epc_owner_d)
```

Phasing uses a sine S-curve over the effective construction period N that sums exactly to one for any N, and escalation at `capex_esc`:

```
share_t   = IF(consflag=1,SIN(PI()*(t-0.5)/N)*SIN(PI()/(2*N)),0)
capex_nom = capex_real*share*escidx       escidx = (1+capex_esc)^(year-base_year)
```

Transmission cost is `(tx_km*tx_cost_km+tx_sub+tx_reinf)*eff_capex` (USD 16.7m real for Kasiri), spent over `tx_build` years before the planned transmission COD, with a delay penalty `(1+delay_cost*eff_tdelay)` spread over `tx_build+eff_tdelay` years. `tx_party` = 1 puts the spend on government, 2 on the project. Transmission COD is `start_year+cons_years+tx_lag+eff_tdelay`; the readiness gap is transmission COD less plant COD.

### 6.4 Construction contracting (05A_CONTRACTING)

`epc_struct` selects a column of indicative parameters:

| Parameter | 1 Turnkey EPC | 2 Split packages | 3 Multi-contract |
|---|---|---|---|
| Contractor premium on civil, HM and E&M (`epc_prem`) | 12% | 6% | 0% |
| Owner's share of a cost overrun (`epc_owner`) | 30% | 55% | 90% |
| Owner's share of delay cost after LDs (`epc_owner_d`) | 35% | 60% | 90% |
| Interface risk (1 low to 3 high) | 1 | 2 | 3 |

The premium enters base cost; the owner's shares scale the overrun and delay stresses in `eff_capex` and `capex_real`. A turnkey contract therefore costs more in the base case and less under an overrun. The snapshot runs "EPC 1/2/3 base" and "EPC 1/2/3 overrun 96%" compare them with debt resized for each structure.

### 6.5 Operating costs (07_OPEX)

Real inputs are escalated by the US CPI index:

```
o_fix  = opflag*om_fix*eff_opex*uscpi
o_var  = gen*om_var*eff_opex*uscpi/1000
o_ins  = opflag*capex_real*ins*uscpi
o_mmr  = opflag*capex_real*mmr*uscpi
o_oth  = opflag*om_other*eff_opex*uscpi
o_txprj= IF(tx_party=2,tx_omc,0)+tx_wheelc
opex   = o_fix+o_var+o_ins+o_mmr+o_oth+o_txprj
o_roy  = delivered*royalty*uscpi/1000        (water royalty, paid to government)
```

The major maintenance reserve is carried as an operating cost, not as a separate reserve account.

### 6.6 PPA, tariff and revenue (14_PPA, 15_TARIFF, 16_REVENUE)

The Kasiri tariff is energy-only: capacity charge 0, energy charge USD 112/MWh (2026), half indexed to US CPI, fully in USD, with deemed energy payable for curtailment the seller did not cause.

```
fxfac   = (1-lc_share)+lc_share*lccpi/fxidx/uscpi
capc    = cap_chg*((1-cap_idx)+cap_idx*uscpi)*fxfac*eff_tariff
enc     = en_chg*((1-en_idx)+en_idx*uscpi)*fxfac*eff_tariff
deemed  = deemed flag*(curt_tx+curt_dem)
topshort= MAX(0,top*contracted-delivered-deemed)
epaid   = delivered+deemed+topshort
rev_cap = opflag*capc*inst_mw*12/1000*avail_ratio*rampf
rev_en  = enc*delivered/1000
rev_deem= enc*(deemed+topshort)/1000
rev_bill= rev_cap+rev_en+rev_deem
```

The utility shortfall is routed through three doors in order:

```
cov_backstop = IF(backstop=1,u_gap*bs_share,0)
ppag_lim     = str_ppag*ppag_months/12*rev_util
ppag_reimb   = opflag*MIN(previous ppag_out,MAX(0,u_maxppa-u_ppa))
cov_guar     = MIN(u_gap-cov_backstop,MAX(0,ppag_lim-previous ppag_out+ppag_reimb))
ppag_out     = previous ppag_out+cov_guar-ppag_reimb
unpaid       = u_gap-cov_backstop-cov_guar
rev_cash     = rev_bill-unpaid
```

The guarantee is capped at `ppag_months` of utility billing (12 by default) and is reimbursed by the utility from spare payment capacity; anything beyond becomes arrears to the project.

Lender-case revenue uses the lender generation case:

```
rev_len = rev_cap+enc*IF(deemed=1,gen_len,MIN(gen_len*evac_ratio,d_absorb))/1000
```

Revenue quality measures: fixed share of billed revenue (`rev_fixed`, 0% for Kasiri), revenue at risk between P50 and P90 in operating year 2, utility share of revenue, and lifetime support needed to sustain PPA payments. On *15_TARIFF*, affordability headroom is collected utility revenue per MWh sent out less the blended PPA tariff.

### 6.7 Development module (01A_DEVELOPMENT)

**Stages.** Six stages with duration, real budget and probability of success to the next stage:

| Stage | Months | Budget (USDm real) | P(success) |
|---|---|---|---|
| 1 Site identification and reconnaissance | 6 | 0.10 | 60% |
| 2 Pre-feasibility and start of flow gauging | 12 | 0.60 | 60% |
| 3 Feasibility study, ESIA, geotechnical and grid studies | 18 | 4.50 | 70% |
| 4 Licences, water rights, land and permits | 12 | 0.80 | 85% |
| 5 PPA, implementation agreement and tariff approval | 12 | 0.80 | 80% |
| 6 Financing: advisers, legal, insurance, close | 12 | 2.20 | 85% |
| Total | 72 | 9.00 | 14.6% |

```
dev_total = sum of budgets
dev_years = sum of months/12
dev_pfc   = PRODUCT(p1:p6)
dev_pct   = dev_total/capex_real
```

**Spend profile.** Stages run back to back and end at financial close. Each stage's budget is spread evenly over its months and allocated to the ten development-year columns before close (2017 to 2026), then escalated by `(1+us_cpi)^(year-base_year)`. For Kasiri, spend runs from 2021 to 2026 and totals USD 8.6m nominal.

**P(alive).** For each development year, the probability that the project is still alive when the money is spent is the spend-weighted average over stages of the probability of reaching that stage, `PRODUCT(p1:pk)/pk`.

**Risk-weighted NPV.** With r = `dev_rate` (25%) and all PVs taken at the start of development:

```
dev_reimb        = total nominal development spend
dev_prem         = dev_prem_pct*capex_real
dev_eq_npv_fc    = dev_stake*NPV(r_fc,eq_priv_cf)
dev_success_value= dev_reimb+dev_prem+dev_eq_npv_fc
dev_pv_cost_unw  = NPV(r,spend)*(1+r)^(10-dev_months/12)
dev_pv_cost_rw   = SUMPRODUCT(spend,P(alive),1/(1+r)^column)*(1+r)^(10-dev_months/12)
dev_pv_success   = dev_success_value/(1+r)^(dev_months/12)
dev_npv_success  = dev_pv_success-dev_pv_cost_unw
dev_enpv         = dev_pfc*dev_pv_success-dev_pv_cost_rw
```

Kasiri: value at close on the success path USD 11.27m; success-path NPV USD -1.00m; risk-weighted NPV USD -0.95m.

**Break-even premium and probability.**

```
dev_be_prem = MAX(0,dev_prem-dev_enpv*(1+r)^(dev_months/12)/dev_pfc)
dev_be_p    = IF(dev_npv_success<=0,"n/a: negative on the success path",dev_pv_cost_rw/dev_pv_success)
```

Kasiri needs a premium of USD 29.7m (18.9% of plant cost) for a zero risk-weighted NPV, and has no break-even probability because the success path itself loses value at 25%.

**Value by stage (section D2).** For the stage k about to start, with real budgets c and durations d, and start month s:

```
B (P close from here) = PRODUCT(pk:p6)
C (PV value at close) = B*dev_success_value/(1+r)^((dev_months-s_k)/12)
D (PV remaining spend)= sum over j>=k of c_j*PRODUCT(pk:p(j-1))/(1+r)^((s_j-s_k+0.5*d_j)/12)
E (position value)    = C-D
```

| Stage about to start | P(close) | Value at close | Remaining spend | Position value |
|---|---|---|---|---|
| 1 | 14.6% | 0.43 | 1.63 | -1.20 |
| 2 | 24.3% | 0.80 | 2.86 | -2.06 |
| 3 | 40.5% | 1.67 | 4.84 | -3.17 |
| 4 | 57.8% | 3.34 | 2.06 | 1.28 |
| 5 | 68.0% | 4.91 | 1.98 | 2.93 |
| 6 | 85.0% | 7.67 | 1.97 | 5.70 |

The NPV in section D (nominal spend, year by year) and the value at stage 1 in D2 (real budgets at mid-stage) answer the same question by different routes; Book 7 uses the first for the decision to start and the second for pricing entry.

**Step-ups (section E), private equity at 100%.**

```
val_fc       = NPV(r_fc,eq_priv_cf)+NPV(r_fc,eq_priv_in)
val_step_fc  = NPV(r_fc,eq_priv_cf)
val_cod      = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))/(1+r_fc)^cons_eff
val_step_cod = val_cod-SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_fc)^t)
```

Kasiri: value created at close USD -5.1m (the equity IRR is below the 15% close-stage rate); de-risking step-up from close to COD USD 18.3m.

**Sell-down (section F).**

```
v_cod_nom     = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))
sell_proceeds = sell_pct*dev_stake*v_cod_nom
```

The developer's cash flow runs over 50 columns (ten development years and the 40 model years): minus development spend; at t = 1 the reimbursement plus the premium; in every model year `dev_stake` times the private equity cash flow, reduced by `(1-sell_pct)` in operating years; and the sale proceeds in the last construction year. Kasiri: sale proceeds USD 19.5m, cash multiple 4.97x, peak cumulative cash at risk USD 10.2m.

**Developer IRR with three starting values.**

```
dev_irr = IF(ISNUMBER(IRR(cf,0.15)),IF(ABS(IRR(cf,0.15))<1,IRR(cf,0.15),-1),
          IF(ISNUMBER(IRR(cf,0.05)),IF(ABS(IRR(cf,0.05))<1,IRR(cf,0.05),-1),
          IF(ISNUMBER(IRR(cf,-0.05)),IF(ABS(IRR(cf,-0.05))<1,IRR(cf,-0.05),-1),-1)))
```

The developer cash flow changes sign several times, so the starting value matters. The formula tries 15%, then 5%, then -5%, moving to the next only when the previous one returns an error; a result of absolute value 1 or more is treated as spurious and reported as -1 (-100%). Kasiri: 16.0%. Promotes and carried interest are not modelled.

### 6.8 Financing structures (17A_STRUCTURES)

Column C reads the selected structure from columns E to I with `INDEX(E:I,structure)`.

| Parameter | 1 Public | 2 IPP | 3 PPP | 4 Hybrid | 5 Blended |
|---|---|---|---|---|---|
| Government equity | 15% | 0% | 10% | 0% | 5% |
| Grants, VGF, public capital | 0% | 0% | 5% | 35% | 8% |
| Concessional debt | 55% | 0% | 30% | 25% | 35% |
| Gearing cap (total senior debt) | 85% | 70% | 75% | 55% | 72% |
| Maximum private equity | 0% | 35% | 20% | 25% | 25% |
| Residual equity provider | Government | Private | Private | Private | Private |
| Senior debt guaranteed by sovereign | 100% | 0% | 40% | 20% | 15% |
| Senior debt recorded as public debt | 100% | 0% | 0% | 0% | 0% |
| Sovereign PPA guarantee | No | Yes | Yes | Yes | Yes |
| Termination payment obligation | No | Yes | Yes | Yes | Yes |
| FX convertibility cover | 0% | 100% | 100% | 100% | 50% |
| Concessional rate / grace / term | 2.0% / 5 / 20 | 3.0% / 5 / 20 | 3.0% / 5 / 20 | 3.0% / 5 / 20 | 2.5% / 5 / 20 |
| Commercial rate / tenor | 7.5% / 15 | 8.0% / 16 | 7.5% / 16 | 7.5% / 16 | 7.2% / 18 |
| Sizing DSCR | 1.20 | 1.35 | 1.30 | 1.30 | 1.30 |
| Private equity target IRR | 10% | 15% | 14% | 14% | 13% |

Percentages are of the funding base. Common terms: lock-up DSCR 1.10x, upfront and commitment fees 2% of senior debt, DSRA six months of next-year debt service. A structure check confirms that grants, government equity, maximum debt and maximum private equity can cover 100%.

The live closed-form comparison is a screen, not a substitute for the full engine:

```
WACC     = (goveq+govx)*gov_disc+conc*rc+comm*rm+priv*hurdle/(1-tax_rate)
WACC_ex  = WACC/(1-grant)
CRF      = WACC_ex/(1-(1+WACC_ex)^-ops_years)
tariff   = (fund_base*(1+maxdebt*(idc_km+upfront_fee))*(1-grant)*CRF+opex_y2)/p50*1000
exposure = public capital+on-budget debt+MAX(guaranteed debt+PPA guarantee,termination)
```

where commercial debt is assumed at the gearing cap less concessional debt. The full-engine snapshot on the same sheet, and the required tariff solved by the runner for structures 2 to 5, are the figures to quote.
