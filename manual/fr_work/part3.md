### 6.9 Debt sizing (17_PROJECT_FINANCE, 18_DEBT)

**Funding base and uses.**

```
fund_base = u_capex+u_tx+u_devprem        (plant cost nominal, project transmission in construction, development premium)
uses      = fund_base+u_idc+u_fee+u_dsra
u_fee     = upfront_fee*(debt_c+debt_m)
```

Kasiri: 164.8 + 17.8 + 4.7 = funding base 187.3; IDC 17.4; fees 2.9; initial DSRA 7.3; total uses 215.0.

**Closed-form IDC factors.** Debt is drawn pro rata with the plant spending share, and interest accrues on the opening balance plus half the year's draw. The IDC per dollar of each tranche is therefore a constant:

```
idc_kc = str_rc*SUMPRODUCT(consflag,cumsh-0.5*share)
idc_km = rm_eff*SUMPRODUCT(consflag,cumsh-0.5*share)
rm_eff = str_rm+eff_rate_add*(1-hedge)
```

For Kasiri the sum is 1.5, so `idc_km` = 0.12.

**Lender-case CFADS and sculpting.** The lender case uses unlevered tax and depreciation without IDC and fees, which keeps the sizing free of circularity:

```
cfads_len = rev_len-opex-o_roy_len-IF(opyr>tax_hol,tax_rate*MAX(0,rev_len-opex-o_roy_len-dep_len),0)
inloan    = IF(AND(opyr>=1,opyr<=str_nm),1,0)
dfm       = IF(opyr>=1,1/(1+rm_eff)^opyr,0)
sculpt    = inloan*MAX(0,cfads_len/str_dscr-c_ds)
comm_cap  = SUMPRODUCT(sculpt,dfm)
```

Commercial debt service is sculpted to the target DSCR after concessional debt service, and capacity is its present value at the commercial rate, discounted to COD.

**Gearing cap.** Total senior debt may not exceed the cap times the funding base plus debt-funded IDC and fees. Solving for commercial debt gives a closed form:

```
gearing amount = MAX(0,(str_maxdebt*(fund_base+debt_c*(idc_kc+upfront_fee))-debt_c)/(1-str_maxdebt*(idc_km+upfront_fee)))
debt_c (sized) = MIN(str_conc,str_maxdebt)*fund_base
debt_m (sized) = MIN(comm_cap,gearing amount)
```

Kasiri: gearing amount 0.70 × 187.3 / (1 − 0.70 × 0.14) = 145.4, just below the sculpted capacity of 147.8, so the gearing cap binds. Gearing on total uses is 67.6%.

**Locked mode (`debt_mode` = 2).** Grant, government equity and concessional debt take the locked inputs `lock_grant`, `lock_goveq` and `lock_c`. Commercial debt is `MIN(lock_m,gearing amount)`, and its target debt service follows the locked principal schedule by operating year, scaled if the amount differs:

```
m_target = IF(inloan=1,IF(debt_mode=1,IF(comm_cap>0,sculpt*debt_m/comm_cap,0),
           IF(lock_m>0,INDEX(lock_ds,1,opyr)*debt_m/lock_m,0)+m_int),0)
m_prin   = IF(inloan=1,MAX(0,MIN(m_open,IF(opyr=str_nm,m_open,m_target-m_int))),0)
```

Interest floats only on the unhedged share through `rm_eff`. Equity absorbs any difference in uses.

**Tranches.**

```
c_draw = debt_c*share       c_int = str_rc*(c_open+0.5*c_draw*consflag)
c_prin = IF(AND(opyr>str_gc,opyr<=str_gc+str_nc),MIN(c_open,debt_c/str_nc),0)
m_draw = debt_m*share       m_int = rm_eff*(m_open+0.5*m_draw*consflag)
ds     = c_ds+m_ds          c_ds, m_ds = opflag*(interest+principal)
idc    = consflag*(c_int+m_int)
```

**DSRA.** The target is `IF(OR(opflag=1,lastcons=1),dsra_m/12*next-year ds,0)`. The initial balance is funded at the end of construction from equity (it sits in uses).

**Ratios.**

```
kpi_min_dscr = IF(COUNT(dscr)=0,99,MIN(dscr))
kpi_avg_dscr = IF(COUNT(dscr)=0,99,AVERAGE(dscr))
kpi_llcr     = SUMPRODUCT(cfads,dfw,inloan_all)/(debt_c+debt_m)
kpi_plcr     = SUMPRODUCT(cfads,dfm)/(debt_c+debt_m)
```

`dfw` discounts at the weighted senior rate; `inloan_all` covers the longest tranche life. The value 99 means there is no debt service.

### 6.10 Waterfall (20_CASH_FLOW)

**Construction funding.** Uses each year are plant cost, project transmission, IDC, fees and premium at t = 1, and the initial DSRA. Grants and debt are drawn pro rata with the spending share; equity is the balance, split between government and private holders by their shares.

**Operations.**

```
ebitda     = rev_cash-opex-o_roy
cfads      = opflag*(ebitda-tax-tx_spend_prj)
dscr       = IF(ds>0.001,cfads/ds,"")
avail0     = cfads-ds+cash_bf
dsra_draw  = opflag*MIN(previous dsra_act,MAX(0,-avail0))
dsra_relx  = opflag*MAX(0,previous dsra_act-dsra_draw-dsra_tgt)
dsra_top   = opflag*MIN(MAX(0,dsra_tgt-previous dsra_act+dsra_draw),MAX(0,avail0))
cash_avail = cfads-ds+dsra_draw+dsra_relx-dsra_top
shortfall  = MAX(0,-(cash_avail+cash_bf))
lock_ok    = IF(opflag=1,IF(ds>0.001,IF(dscr>=lockup,1,0),1),0)
pool       = cash_avail+cash_bf+shortfall
grepay     = IF(OR(lock_ok=1,opyr=ops_years),MIN(previous gclaim,MAX(0,pool)),0)
dist       = IF(OR(lock_ok=1,opyr=ops_years),MAX(0,pool-grepay),0)
cash_cf    = pool-grepay-dist
```

The DSRA is drawn first in a shortfall, releases only its excess over target, and is topped up only from available cash. A remaining shortfall is funded by the sovereign guarantee (share `str_guar`) and by sponsors (the rest). The sovereign's claim is repaid from later cash ahead of distributions. Cash is trapped when the DSCR is below the lock-up and released in the final operating year.

### 6.11 Tax (21_TAX)

```
dep_base = fund_base+u_idc+u_fee-s_grant
dep      = IF(AND(opyr>=1,opyr<=dep_yrs),dep_base/dep_yrs,0)
taxable  = ebitda-dep-interest in operations
loss_use = IF(AND(taxable>0,opyr>tax_hol),MIN(taxable,loss_bf),0)
tax      = IF(opyr>tax_hol,tax_rate*MAX(0,taxable-loss_use),0)
tax_unlev= IF(opyr>tax_hol,tax_rate*MAX(0,ebitda-dep),0)
```

Losses are carried forward and not used during the holiday. Tax forgone through the holiday is reported (USD 8.6m nominal for Kasiri).

### 6.12 Returns (17_PROJECT_FINANCE, 19_EQUITY)

```
ucf      = -capex_nom-tx_spend_prj-premium at t=1+opflag*(ebitda-tax_unlev)
kpi_pirr = IFERROR(IRR(ucf,0.08),"n/a")
kpi_npv  = NPV(disc_rate,ucf)
kpi_eirr = IF(s_priv>0,IFERROR(IRR(eq_priv_cf,0.1),IFERROR(IRR(eq_priv_cf,-0.1),IFERROR(IRR(eq_priv_cf,-0.5),-1))),"n/a")
eq_priv_cf = -eq_priv_in+(dist-sf_eq)*(1-gov_eq_share)
lcoe     = NPV(disc_rate,lc_cost)/NPV(disc_rate,delivered+deemed)*1000
lcoe_sys = NPV(disc_rate,lc_cost_sys)/NPV(disc_rate,delivered*(1-tx_loss))*1000
```

`lc_cost` is plant and project transmission spending, the premium, OPEX and royalty; `lc_cost_sys` adds public transmission spending and O&M. NPV follows the Excel convention (the first flow is discounted one period).

For termination, *19_EQUITY* computes the value of remaining private distributions at the target IRR by backward recursion, `e_pvfwd = (next e_out+next e_pvfwd)/(1+str_hurdle)`, and unrecovered private equity `e_unrec = MAX(0,-cumulative private equity cash flow)`.

The financing gap is the private equity required beyond what is available:

```
priv_avail = str_privmax*fund_base
fin_gap    = IF(str_resid=1,MAX(0,s_priv-priv_avail),0)
```

Kasiri: private equity 69.6 against 65.6 available, gap USD 4.1m (1.9% of uses).

### 6.13 Utility payment capacity and counterfactual (12_UTILITY)

The utility model tests whether the buyer can pay, rather than assuming it.

**Energy balance.** Utility demand is domestic demand less any mining load the project serves directly. The project supplies its utility share net of transmission losses; other supply is capped at the supply available (`d_sup`); demand above the cap is unserved.

**Cash and capacity.**

```
u_tar     = previous tariff*(1+lc_cpi*IF(AND(opyr>=1,opyr<=eff_freeze),0,ut_pt))
u_bill    = u_sales*u_tar/fx
u_collr   = MAX(0,MIN(1,ut_coll+IF(year>=cod_year,eff_coll_adj,0)))
u_subs    = ut_sub*IF(year>=cod_year,eff_sub,1)*lccpi/fxidx
u_opex    = -ut_opex*lccpi/fxidx*(0.5+0.5*u_sales/base-year demand)
u_supcost = -u_other*ut_supc*(ut_supusd*uscpi+(1-ut_supusd)*lccpi/fxidx)/1000
u_cash_pre= u_bill*u_collr+u_subs+u_opex+u_supcost-ut_ds
u_maxppa  = MAX(0,u_cash_pre)/ut_cov
u_gap     = opflag*MAX(0,u_ppa-u_maxppa)
u_ratio   = IF(u_ppa>0,u_maxppa/u_ppa,99)
```

`ut_ratio10` is the worst ratio in operating years 1 to 10 (5.96x for Kasiri). The FX rate is `fx0*(1+fx_dep)^(year-base_year)`, times `(1+eff_fxshock)` from COD.

**Counterfactual.** The model recomputes the utility's cash without the project (`u_cash_np`), buying from other supply up to its cap. The incremental cash of the state utility is:

```
f_soe = u_cash_post-u_cash_np-unpaid
```

so new arrears count as a cost to the public sector. This term carries the utility into the consolidated fiscal NPV.

### 6.14 Government support, guarantees and contingent liabilities (22 to 24)

**Direct support** (*22_GOVERNMENT_SUPPORT*): government equity, grants, public transmission capital and O&M, and the budget backstop of the PPA shortfall.

**Exposure by instrument** (*23_GUARANTEES*):

```
x_debt  = (1-str_onbud)*str_guar*debt_bal
x_ppa   = str_ppag*ppag_months/12*rev_util
x_term  = str_term*(opflag+consflag>0)*(debt_bal+MAX(e_unrec*(1+term_prem),e_pvfwd))
x_fx    = str_fxg*(ds+e_out)
x_mrg   = opflag*MAX(0,mrg*rev_cap/MAX(0.0001,rampf)-rev_cash)
x_onbud = str_onbud*debt_bal
```

**Maximum simultaneous exposure** (*24_CONTINGENT_LIABILITIES*) avoids adding the termination amount to the guarantees it would replace:

```
cl_max = MAX(x_term,x_debt+x_ppa+x_fx)
```

**Deterministic calls** in the active scenario are PPA guarantee calls, debt guarantee calls (shortfall times guaranteed share) and minimum revenue guarantee calls.

**Expected loss** uses user-judgement probabilities and a loss given call:

```
el = (pr_debt*x_debt+pr_ppa*MAX(0,x_ppa-cov_guar)+pr_term*MAX(0,x_term-x_debt))*lgd
cl_pv_el = SUMPRODUCT(el,gdf)          gdf = 1/(1+gov_disc)^t
```

Kasiri: peak exposure USD 225.4m, mostly the termination amount; PV of expected loss USD 20.4m at the default probabilities (2%, 8%, 0.5% a year; LGD 60%).

### 6.15 Fiscal NPV, central and consolidated (25_FISCAL_IMPACT)

```
f_direct  = -g_direct
f_calls   = -call_tot
f_tax     = tax
f_roy     = o_roy
f_div     = e_g_out-sf_eq*gov_eq_share
f_grep    = grepay+ppag_reimb
f_net     = f_direct+f_calls+f_tax+f_roy+f_div+f_grep
f_net_cons= f_net+f_soe
fis_npv      = SUMPRODUCT(f_net,gdf)
fis_npv_cons = SUMPRODUCT(f_net_cons,gdf)
fis_npv_el   = fis_npv-cl_pv_el
```

Kasiri at 8%: central NPV USD +34.8m from taxes and royalties; consolidated NPV USD -27.6m, because the utility pays more for Kasiri's energy than it collects per MWh. The sheet also reports the peak annual cash need, the peak need as a share of government revenue, the deepest cumulative outlay and tax forgone.

### 6.16 Fiscal screen (26_DEBT_SUSTAINABILITY)

The screen asks whether this one project adds material fiscal pressure. It is not a debt sustainability analysis.

```
s_onbud = x_onbud/gdp          s_cl   = cl_max/gdp
s_cash  = f_need/gov_rev       s_cumout = MAX(0,-f_cum)/gdp
s_arr   = u_arrears/gdp        s_inc  = s_onbud+s_cumout+s_arr
sc_debt = MAX(s_inc)   sc_cl = MAX(s_cl)   sc_cash = MAX(s_cash)
sc_post = debt_gdp+sc_debt
sc_flags= (sc_debt>th_incr)+(sc_cl>th_cl)+(sc_cash>th_cash)+AND(sc_post>th_debt,debt_gdp<=th_debt)
```

Default thresholds: material increment 1% of GDP, material contingent exposure 2% of GDP, material cash need 1% of revenue, debt benchmark 55% of GDP. The result:

| Condition | Result |
|---|---|
| No flag and DSA rating 1 or 2 | LOW additional fiscal pressure |
| Three or more flags, or at least one flag with a DSA rating of 3 or 4 or public debt already above the benchmark | HIGH additional fiscal pressure, with an instruction to escalate to the finance ministry and DSA team |
| Otherwise | MODERATE additional fiscal pressure |

Kasiri: no flag, DSA rating 2, result LOW.

### 6.17 The 9-gate development screen (30_BANKABILITY)

Each test maps a metric to a score using three explicit, editable thresholds. Direction H means higher is better:

```
H: score = IF(metric>=READY,3,IF(metric>=COND,2,IF(metric>=DEV,1,0)))
L: score = IF(metric<=READY,3,IF(metric<=COND,2,IF(metric<=DEV,1,0)))
```

Scores map to READY (3), CONDITIONAL (2), DEVELOPMENT GAP (1) and CRITICAL GAP (0). A gate's score is the minimum of its tests: no averaging and no weights.

| Gate | Test | Dir. | READY | COND. | DEV. GAP | Kasiri |
|---|---|---|---|---|---|---|
| 1 Resource | Reliable flow record (years) | H | 25 | 15 | 8 | 12 |
| | P90/P50 energy ratio | H | 0.85 | 0.78 | 0.70 | 0.81 |
| | Hydrology study maturity (1 to 3) | H | 3 | 2 | 1 | 2 |
| 2 Demand | Bankable/contracted demand, worst of years 1 to 5 | H | 1.0 | 0.9 | 0.7 | 1.0 |
| | Share of system peak at COD | L | 15% | 25% | 35% | 3.3% |
| 3 Configuration | Unit cost / benchmark | L | 1.00 | 1.25 | 1.50 | 1.04 |
| | Capacity factor (P50) | H | 45% | 35% | 25% | 55.6% |
| | Feasibility maturity (1 to 3) | H | 3 | 2 | 1 | 2 |
| 4 Transmission | Evacuation at COD / installed | H | 1.0 | 0.8 | 0.5 | 2.0 |
| | Transmission lag (years) | L | 0 | 1 | 2 | 0 |
| | Transmission financing secured | H | 1 | 1 | 0 | 1 |
| 5 Offtaker | Payment capacity / PPA, worst of years 1 to 10 | H | 1.2 | 1.0 | 0.8 | 5.96 |
| | Collection rate | H | 95% | 90% | 80% | 88% |
| | Payment security (months) | H | 6 | 3 | 1 | 3 |
| 6 Regulation/PPA | Items at CRITICAL GAP | L | 0 | 0 | 0 | 0 |
| | Items at GAP | L | 1 | 3 | 5 | 4 |
| | Fixed (capacity) share of revenue | H | 60% | 40% | 20% | 0% |
| 7 Financing | Minimum DSCR, actual case | H | `str_dscr` | `lockup` | 1.0 | 1.53 |
| | Financing gap / uses | L | 0% | 5% | 15% | 1.9% |
| | Private equity IRR vs target | H | hurdle | hurdle −2pp | hurdle −5pp | 13.8% |
| 8 Public finance | Peak cash need / revenue | L | 0.5% | 1% | 2% | 0% |
| | Peak contingent exposure / GDP | L | 1% | 2% | 4% | 0.56% |
| | Peak on-budget increment / GDP | L | 0.5% | 1% | 2% | 0% |
| | Consolidated fiscal NPV / GDP | H | 0% | −0.5% | −2% | −0.08% |
| | DSA risk rating (1 to 4) | L | 1 | 2 | 3 | 2 |
| 9 E&S | ESIA and lender-standard compliance | H | 3 | 2 | 1 | 2 |
| | Resettlement plan status | H | 3 | 2 | 1 | 2 |
| | Transboundary issues | H | 3 | 2 | 1 | 3 |

The equity IRR test uses `IF(ISNUMBER(kpi_eirr),kpi_eirr,IF(s_priv>0,-1,str_hurdle))`, so a structure without private equity passes it. The overall verdict:

| Condition | Verdict |
|---|---|
| Any gate at CRITICAL GAP | NOT BANKABLE (critical gap(s) must be closed) |
| Otherwise any DEVELOPMENT GAP | NOT YET BANKABLE (development gaps remain) |
| Otherwise lowest score 2 | BANKABLE SUBJECT TO CONDITIONS |
| All gates READY | READY FOR FINANCIAL CLOSE |

Each gate carries a pre-written action: a gap action when the score is 0 or 1, a conditional action when it is 2. The dashboard ranks gates by a key equal to the score plus the gate number divided by 100, so ties are broken in gate order, and lists the five lowest with their actions.

Reading note for Kasiri: Gate 6 is at CRITICAL GAP only because the tariff is energy-only, so the fixed share of revenue is 0%, below the 20% development-gap threshold. The threshold is illustrative; an energy-only tariff can be bankable if hydrology risk is otherwise covered, and the user should calibrate this test to the lenders' view.

### 6.18 The 23-gate close readiness and the decision ladder (30A_CLOSE_READINESS)

Each gate has an area, a critical flag and either an automatic model test or an evidence status entered by the user (MET, PARTIAL, NOT MET or NO EVIDENCE). Automatic tests return MET or NOT MET.

| # | Gate | Critical | Test or default evidence | Question |
|---|---|---|---|---|
| 1 | Flow record of at least 15 years and independent hydrology review | Y | `AND(rec_years>=15,hyd_study=3)` | Q1 |
| 2 | P90 energy confirmed by the lenders' technical adviser | Y | PARTIAL | Q1 |
| 3 | Bankable feasibility study signed off by the lenders' technical adviser | Y | `fs_level=3` | Q1 |
| 4 | Geotechnical investigation sufficient for a baseline report | Y | PARTIAL | Q1 |
| 5 | ESIA approved and compliant with lender standards | Y | `es_level=3` | Q2 |
| 6 | Resettlement action plan approved and funded | Y | `rap_level>=2` | Q2 |
| 7 | Generation licence and water-use permit granted | Y | PARTIAL | Q2 |
| 8 | Land rights secured for all project areas | Y | NOT MET | Q2 |
| 9 | PPA signed and approved by the regulator | Y | PARTIAL | Q2 |
| 10 | Implementation or concession agreement signed | Y | PARTIAL | Q2 |
| 11 | Grid connection agreement signed and transmission financed | Y | `tx_fin=1` | Q3 |
| 12 | Transmission in service no later than plant COD | N | `tx_gap_yrs<=0` | Q3 |
| 13 | EPC contract(s) signed with fixed price, completion date and LDs | Y | PARTIAL | Q6 |
| 14 | O&M arrangements and owner's team in place | N | PARTIAL | Q6 |
| 15 | Payment security of at least 6 months in place | Y | `lc_months>=6` | Q7 |
| 16 | Offtaker payment capacity at least 1.2x the PPA bill (worst of first 10 years) | Y | `ut_ratio10>=1.2` | Q7 |
| 17 | Financing plan fully committed (no financing gap) | Y | `fin_gap<=0.5` | Q5 |
| 18 | Minimum DSCR at or above the sizing target in the selected case | Y | `AND(debt_m+debt_c>0,kpi_min_dscr>=str_dscr)` | Q5 |
| 19 | Equity commitments signed and equity IRR at or above target | Y | `IF(ISNUMBER(kpi_eirr),kpi_eirr>=str_hurdle,s_priv<=0)` | Q4 |
| 20 | Political risk cover or guarantees signed | N | NO EVIDENCE | Q5 |
| 21 | Government support approved by the finance ministry; fiscal screen not HIGH | Y | `LEFT(sc_result,4)<>"HIGH"` | Q7 |
| 22 | Insurance programme placed (construction all risks, DSU) | N | PARTIAL | Q6 |
| 23 | Independent model audit completed | N | NO EVIDENCE | Q5 |

Gate 17 allows a financing gap of up to USD 0.5m. Gate 18 requires debt to exist, so a structure without senior debt does not pass it on the placeholder DSCR of 99. Gate 18 reads the selected case, so it moves with stresses.

**Decision ladder**, evaluated in this order:

```
IF fc_crit_fail>0     "STOP: a critical gate is not met"
ELSE IF fc_crit_noev>0 "STOP: critical evidence missing"
ELSE IF fc_crit_part>0 "NOT READY: critical gates partly met"
ELSE IF fc_met=fc_n    "GO: evidence complete for a close decision"
ELSE                   "CONDITIONAL GO: all critical gates met"
```

A GO says the evidence file is complete for lenders and sponsors to decide; it is not an investment recommendation. Kasiri: 6 of 23 met, 7 critical not met, 6 critical partly met, decision STOP.

The summary at the foot of the sheet counts, for each question, the gates, those met and the critical gates not met or without evidence. Q8 is the total. For Kasiri: Q1 0 of 4 met (2 critical open), Q2 1 of 6 (2), Q3 2 of 2 (0), Q4 0 of 1 (1), Q5 1 of 4 (1), Q6 0 of 3 (0), Q7 2 of 3 (1), Q8 6 of 23 (7).

---
