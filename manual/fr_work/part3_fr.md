### 6.9 Dimensionnement de la dette (17_PROJECT_FINANCE, 18_DEBT)

**Assiette de financement et emplois.**

```
fund_base = u_capex+u_tx+u_devprem        (coût de la centrale en nominal, transport du projet pendant la construction, prime de développement)
uses      = fund_base+u_idc+u_fee+u_dsra
u_fee     = upfront_fee*(debt_c+debt_m)
```

Kasiri : 164,8 + 17,8 + 4,7 = assiette de financement de 187,3 ; intérêts intercalaires (IDC) 17,4 ; commissions 2,9 ; dotation initiale du compte de réserve du service de la dette (DSRA) 7,3 ; total des emplois 215,0.

**Facteurs d'IDC sous forme fermée.** La dette est tirée au prorata de la part de dépenses de la centrale, et les intérêts courent sur le solde d'ouverture augmenté de la moitié du tirage de l'année. Les IDC par dollar de chaque tranche sont donc une constante :

```
idc_kc = str_rc*SUMPRODUCT(consflag,cumsh-0.5*share)
idc_km = rm_eff*SUMPRODUCT(consflag,cumsh-0.5*share)
rm_eff = str_rm+eff_rate_add*(1-hedge)
```

Pour Kasiri, la somme vaut 1,5, d'où `idc_km` = 0,12.

**Flux de trésorerie disponibles pour le service de la dette (CFADS) du cas prêteurs et sculptage.** Le cas prêteurs retient l'impôt et l'amortissement hors effet de levier, sans IDC ni commissions, ce qui évite toute circularité dans le dimensionnement :

```
cfads_len = rev_len-opex-o_roy_len-IF(opyr>tax_hol,tax_rate*MAX(0,rev_len-opex-o_roy_len-dep_len),0)
inloan    = IF(AND(opyr>=1,opyr<=str_nm),1,0)
dfm       = IF(opyr>=1,1/(1+rm_eff)^opyr,0)
sculpt    = inloan*MAX(0,cfads_len/str_dscr-c_ds)
comm_cap  = SUMPRODUCT(sculpt,dfm)
```

Le service de la dette commerciale est sculpté sur le ratio de couverture du service de la dette (DSCR) cible, après le service de la dette concessionnelle, et la capacité d'emprunt est sa valeur actualisée au taux commercial, ramenée à la date de mise en service commerciale (COD).

**Plafond du taux d'endettement (gearing).** La dette senior totale ne peut dépasser le plafond multiplié par l'assiette de financement augmentée des IDC et commissions financés par la dette. En résolvant pour la dette commerciale, on obtient une forme fermée :

```
gearing amount = MAX(0,(str_maxdebt*(fund_base+debt_c*(idc_kc+upfront_fee))-debt_c)/(1-str_maxdebt*(idc_km+upfront_fee)))
debt_c (sized) = MIN(str_conc,str_maxdebt)*fund_base
debt_m (sized) = MIN(comm_cap,gearing amount)
```

Kasiri : montant au plafond de gearing 0,70 × 187,3 / (1 − 0,70 × 0,14) = 145,4, juste sous la capacité sculptée de 147,8 ; c'est donc le plafond de gearing qui s'applique. Le taux d'endettement rapporté au total des emplois est de 67,6 %.

**Mode verrouillé (`debt_mode` = 2).** Les subventions, les fonds propres de l'État et la dette concessionnelle prennent les valeurs verrouillées `lock_grant`, `lock_goveq` et `lock_c`. La dette commerciale vaut `MIN(lock_m,gearing amount)`, et son service de la dette cible suit l'échéancier de principal verrouillé par année d'exploitation, mis à l'échelle si le montant diffère :

```
m_target = IF(inloan=1,IF(debt_mode=1,IF(comm_cap>0,sculpt*debt_m/comm_cap,0),
           IF(lock_m>0,INDEX(lock_ds,1,opyr)*debt_m/lock_m,0)+m_int),0)
m_prin   = IF(inloan=1,MAX(0,MIN(m_open,IF(opyr=str_nm,m_open,m_target-m_int))),0)
```

Le taux n'est variable que sur la part non couverte, via `rm_eff`. Les fonds propres absorbent tout écart sur les emplois.

**Tranches.**

```
c_draw = debt_c*share       c_int = str_rc*(c_open+0.5*c_draw*consflag)
c_prin = IF(AND(opyr>str_gc,opyr<=str_gc+str_nc),MIN(c_open,debt_c/str_nc),0)
m_draw = debt_m*share       m_int = rm_eff*(m_open+0.5*m_draw*consflag)
ds     = c_ds+m_ds          c_ds, m_ds = opflag*(interest+principal)
idc    = consflag*(c_int+m_int)
```

**DSRA.** La cible est `IF(OR(opflag=1,lastcons=1),dsra_m/12*next-year ds,0)`. Le solde initial est financé à la fin de la construction par les fonds propres (il figure dans les emplois).

**Ratios.**

```
kpi_min_dscr = IF(COUNT(dscr)=0,99,MIN(dscr))
kpi_avg_dscr = IF(COUNT(dscr)=0,99,AVERAGE(dscr))
kpi_llcr     = SUMPRODUCT(cfads,dfw,inloan_all)/(debt_c+debt_m)
kpi_plcr     = SUMPRODUCT(cfads,dfm)/(debt_c+debt_m)
```

`dfw` actualise au taux senior pondéré ; `inloan_all` couvre la durée de la tranche la plus longue. La valeur 99 signifie qu'il n'y a pas de service de la dette.

### 6.10 Cascade des flux (20_CASH_FLOW)

**Financement de la construction.** Les emplois de chaque année sont le coût de la centrale, le transport du projet, les IDC, les commissions et la prime à t = 1, ainsi que la dotation initiale du DSRA. Les subventions et la dette sont tirées au prorata de la part de dépenses ; les fonds propres constituent le solde, réparti entre l'État et les actionnaires privés selon leurs parts.

**Exploitation.**

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

En cas d'insuffisance, le DSRA est mobilisé en premier ; il ne libère que son excédent au-delà de la cible et n'est reconstitué qu'à partir de la trésorerie disponible. L'insuffisance restante est couverte par la garantie souveraine (part `str_guar`) et par les promoteurs (le reste). La créance de l'État est remboursée sur la trésorerie ultérieure, avant les distributions. La trésorerie est bloquée quand le DSCR est inférieur au seuil de blocage (lock-up), puis libérée lors de la dernière année d'exploitation.

### 6.11 Impôt (21_TAX)

```
dep_base = fund_base+u_idc+u_fee-s_grant
dep      = IF(AND(opyr>=1,opyr<=dep_yrs),dep_base/dep_yrs,0)
taxable  = ebitda-dep-interest in operations
loss_use = IF(AND(taxable>0,opyr>tax_hol),MIN(taxable,loss_bf),0)
tax      = IF(opyr>tax_hol,tax_rate*MAX(0,taxable-loss_use),0)
tax_unlev= IF(opyr>tax_hol,tax_rate*MAX(0,ebitda-dep),0)
```

Les pertes sont reportées et ne sont pas imputées pendant l'exonération fiscale. L'impôt auquel l'État renonce du fait de l'exonération est indiqué (8,6 millions USD en nominal pour Kasiri).

### 6.12 Rentabilité (17_PROJECT_FINANCE, 19_EQUITY)

```
ucf      = -capex_nom-tx_spend_prj-premium at t=1+opflag*(ebitda-tax_unlev)
kpi_pirr = IFERROR(IRR(ucf,0.08),"n/a")
kpi_npv  = NPV(disc_rate,ucf)
kpi_eirr = IF(s_priv>0,IFERROR(IRR(eq_priv_cf,0.1),IFERROR(IRR(eq_priv_cf,-0.1),IFERROR(IRR(eq_priv_cf,-0.5),-1))),"n/a")
eq_priv_cf = -eq_priv_in+(dist-sf_eq)*(1-gov_eq_share)
lcoe     = NPV(disc_rate,lc_cost)/NPV(disc_rate,delivered+deemed)*1000
lcoe_sys = NPV(disc_rate,lc_cost_sys)/NPV(disc_rate,delivered*(1-tx_loss))*1000
```

`lc_cost` regroupe les dépenses de la centrale et du transport du projet, la prime, les charges d'exploitation (OPEX) et la redevance ; `lc_cost_sys` y ajoute les dépenses de transport public et leur exploitation et maintenance (O&M). La valeur actuelle nette (VAN) suit la convention d'Excel (le premier flux est actualisé d'une période).

Pour la résiliation, *19_EQUITY* calcule par récurrence à rebours la valeur des distributions privées restantes au taux de rendement interne (TRI) cible, `e_pvfwd = (next e_out+next e_pvfwd)/(1+str_hurdle)`, ainsi que les fonds propres privés non récupérés, `e_unrec = MAX(0,-cumulative private equity cash flow)`.

Le besoin de financement non couvert (écart de financement) correspond aux fonds propres privés requis au-delà de ceux qui sont disponibles :

```
priv_avail = str_privmax*fund_base
fin_gap    = IF(str_resid=1,MAX(0,s_priv-priv_avail),0)
```

Kasiri : fonds propres privés de 69,6 pour 65,6 disponibles, soit un écart de 4,1 millions USD (1,9 % des emplois).

### 6.13 Capacité de paiement de la compagnie d'électricité et scénario contrefactuel (12_UTILITY)

Le modèle de la compagnie d'électricité vérifie que l'acheteur peut payer, au lieu de le supposer.

**Bilan énergétique.** La demande adressée à la compagnie d'électricité est la demande intérieure, diminuée de la charge minière éventuellement desservie directement par le projet. Le projet fournit sa part destinée à la compagnie, nette des pertes de transport ; les autres approvisionnements sont plafonnés à l'offre disponible (`d_sup`) ; la demande au-delà de ce plafond n'est pas servie.

**Trésorerie et capacité.**

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

`ut_ratio10` est le ratio le plus défavorable des années d'exploitation 1 à 10 (5,96 x pour Kasiri). Le taux de change vaut `fx0*(1+fx_dep)^(year-base_year)`, multiplié par `(1+eff_fxshock)` à partir de la COD.

**Scénario contrefactuel.** Le modèle recalcule la trésorerie de la compagnie d'électricité sans le projet (`u_cash_np`), celle-ci achetant alors aux autres sources dans la limite de leur plafond. La trésorerie supplémentaire de la compagnie publique est :

```
f_soe = u_cash_post-u_cash_np-unpaid
```

de sorte que les nouveaux arriérés sont comptés comme un coût pour le secteur public. Ce terme intègre la compagnie d'électricité dans la VAN budgétaire consolidée.

### 6.14 Soutien de l'État, garanties et passifs éventuels (22 à 24)

**Soutien direct** (*22_GOVERNMENT_SUPPORT*) : fonds propres de l'État, subventions, investissement et O&M du transport public, et garantie budgétaire couvrant l'insuffisance de paiement au titre du contrat d'achat d'électricité (CAE, PPA).

**Exposition par instrument** (*23_GUARANTEES*) :

```
x_debt  = (1-str_onbud)*str_guar*debt_bal
x_ppa   = str_ppag*ppag_months/12*rev_util
x_term  = str_term*(opflag+consflag>0)*(debt_bal+MAX(e_unrec*(1+term_prem),e_pvfwd))
x_fx    = str_fxg*(ds+e_out)
x_mrg   = opflag*MAX(0,mrg*rev_cap/MAX(0.0001,rampf)-rev_cash)
x_onbud = str_onbud*debt_bal
```

**L'exposition simultanée maximale** (*24_CONTINGENT_LIABILITIES*) évite d'additionner l'indemnité de résiliation et les garanties qu'elle remplacerait :

```
cl_max = MAX(x_term,x_debt+x_ppa+x_fx)
```

**Les appels déterministes** du scénario actif sont les appels de la garantie du CAE, les appels de la garantie de la dette (insuffisance multipliée par la part garantie) et les appels de la garantie de revenu minimum.

**La perte attendue** repose sur des probabilités fixées à dire d'expert par l'utilisateur et sur une perte en cas d'appel :

```
el = (pr_debt*x_debt+pr_ppa*MAX(0,x_ppa-cov_guar)+pr_term*MAX(0,x_term-x_debt))*lgd
cl_pv_el = SUMPRODUCT(el,gdf)          gdf = 1/(1+gov_disc)^t
```

Kasiri : exposition maximale de 225,4 millions USD, constituée pour l'essentiel de l'indemnité de résiliation ; valeur actualisée de la perte attendue de 20,4 millions USD avec les probabilités par défaut (2 %, 8 % et 0,5 % par an ; perte en cas d'appel (LGD) de 60 %).

### 6.15 VAN budgétaire, centrale et consolidée (25_FISCAL_IMPACT)

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

Kasiri à 8 % : VAN de l'administration centrale de +34,8 millions USD, grâce aux impôts et aux redevances ; VAN consolidée de −27,6 millions USD, car la compagnie d'électricité paie l'énergie de Kasiri plus cher qu'elle n'encaisse par MWh. La feuille indique aussi le besoin de trésorerie annuel maximal, ce besoin maximal en part des recettes publiques, la sortie de fonds cumulée la plus profonde et l'impôt auquel l'État renonce.

### 6.16 Filtre budgétaire (26_DEBT_SUSTAINABILITY)

Le filtre cherche à savoir si ce seul projet crée une pression budgétaire supplémentaire significative. Il ne s'agit pas d'une analyse de soutenabilité de la dette (DSA).

```
s_onbud = x_onbud/gdp          s_cl   = cl_max/gdp
s_cash  = f_need/gov_rev       s_cumout = MAX(0,-f_cum)/gdp
s_arr   = u_arrears/gdp        s_inc  = s_onbud+s_cumout+s_arr
sc_debt = MAX(s_inc)   sc_cl = MAX(s_cl)   sc_cash = MAX(s_cash)
sc_post = debt_gdp+sc_debt
sc_flags= (sc_debt>th_incr)+(sc_cl>th_cl)+(sc_cash>th_cash)+AND(sc_post>th_debt,debt_gdp<=th_debt)
```

Seuils par défaut : augmentation significative à 1 % du PIB, exposition éventuelle significative à 2 % du PIB, besoin de trésorerie significatif à 1 % des recettes, référence d'endettement à 55 % du PIB. Le résultat :

| Condition | Résultat |
|---|---|
| Aucune alerte et note DSA de 1 ou 2 | *LOW additional fiscal pressure* (pression budgétaire supplémentaire faible) |
| Trois alertes ou plus, ou au moins une alerte avec une note DSA de 3 ou 4 ou une dette publique déjà supérieure à la référence | *HIGH additional fiscal pressure* (pression budgétaire supplémentaire élevée), avec l'instruction de saisir le ministère des Finances et l'équipe DSA |
| Autres cas | *MODERATE additional fiscal pressure* (pression budgétaire supplémentaire modérée) |

Kasiri : aucune alerte, note DSA de 2, résultat LOW.

### 6.17 Le filtre de développement à neuf portes (30_BANKABILITY)

Chaque test associe un indicateur à une note au moyen de trois seuils explicites et modifiables. Le sens H signifie que plus la valeur est élevée, mieux c'est :

```
H: score = IF(metric>=READY,3,IF(metric>=COND,2,IF(metric>=DEV,1,0)))
L: score = IF(metric<=READY,3,IF(metric<=COND,2,IF(metric<=DEV,1,0)))
```

Les notes correspondent à READY (prêt, 3), CONDITIONAL (sous conditions, 2), DEVELOPMENT GAP (lacune de développement, 1) et CRITICAL GAP (lacune critique, 0). La note d'une porte est le minimum de ses tests : ni moyenne, ni pondération.

| Porte | Test | Sens | READY | COND. | DEV. GAP | Kasiri |
|---|---|---|---|---|---|---|
| 1 Ressource | Série de débits fiable (années) | H | 25 | 15 | 8 | 12 |
| | Ratio d'énergie P90/P50 | H | 0,85 | 0,78 | 0,70 | 0,81 |
| | Maturité de l'étude hydrologique (1 à 3) | H | 3 | 2 | 1 | 2 |
| 2 Demande | Demande bancable ou contractée, pire des années 1 à 5 | H | 1,0 | 0,9 | 0,7 | 1,0 |
| | Part de la pointe du système à la COD | L | 15 % | 25 % | 35 % | 3,3 % |
| 3 Configuration | Coût unitaire / référence | L | 1,00 | 1,25 | 1,50 | 1,04 |
| | Facteur de charge (P50) | H | 45 % | 35 % | 25 % | 55,6 % |
| | Maturité de la faisabilité (1 à 3) | H | 3 | 2 | 1 | 2 |
| 4 Transport | Capacité d'évacuation à la COD / puissance installée | H | 1,0 | 0,8 | 0,5 | 2,0 |
| | Retard du transport (années) | L | 0 | 1 | 2 | 0 |
| | Financement du transport acquis | H | 1 | 1 | 0 | 1 |
| 5 Acheteur | Capacité de paiement / CAE, pire des années 1 à 10 | H | 1,2 | 1,0 | 0,8 | 5,96 |
| | Taux de recouvrement | H | 95 % | 90 % | 80 % | 88 % |
| | Garantie de paiement (mois) | H | 6 | 3 | 1 | 3 |
| 6 Réglementation/CAE | Éléments en CRITICAL GAP | L | 0 | 0 | 0 | 0 |
| | Éléments en GAP | L | 1 | 3 | 5 | 4 |
| | Part fixe (capacité) du chiffre d'affaires | H | 60 % | 40 % | 20 % | 0 % |
| 7 Financement | DSCR minimum, cas réel | H | `str_dscr` | `lockup` | 1,0 | 1,53 |
| | Écart de financement / emplois | L | 0 % | 5 % | 15 % | 1,9 % |
| | TRI des fonds propres privés par rapport à la cible | H | cible | cible −2 pts | cible −5 pts | 13,8 % |
| 8 Finances publiques | Besoin de trésorerie maximal / recettes | L | 0,5 % | 1 % | 2 % | 0 % |
| | Exposition éventuelle maximale / PIB | L | 1 % | 2 % | 4 % | 0,56 % |
| | Augmentation budgétaire maximale / PIB | L | 0,5 % | 1 % | 2 % | 0 % |
| | VAN budgétaire consolidée / PIB | H | 0 % | −0,5 % | −2 % | −0,08 % |
| | Note de risque DSA (1 à 4) | L | 1 | 2 | 3 | 2 |
| 9 E&S | EIES et conformité aux normes des prêteurs | H | 3 | 2 | 1 | 2 |
| | État du plan de réinstallation | H | 3 | 2 | 1 | 2 |
| | Questions transfrontalières | H | 3 | 2 | 1 | 3 |

Le test du TRI des fonds propres utilise `IF(ISNUMBER(kpi_eirr),kpi_eirr,IF(s_priv>0,-1,str_hurdle))`, de sorte qu'une structure sans fonds propres privés le réussit. Le verdict global :

| Condition | Verdict |
|---|---|
| Une porte au moins en CRITICAL GAP | NOT BANKABLE (non bancable : la ou les lacunes critiques doivent être comblées) |
| Sinon, au moins une DEVELOPMENT GAP | NOT YET BANKABLE (pas encore bancable : des lacunes de développement subsistent) |
| Sinon, note la plus basse égale à 2 | BANKABLE SUBJECT TO CONDITIONS (bancable sous conditions) |
| Toutes les portes READY | READY FOR FINANCIAL CLOSE (prêt pour le bouclage financier) |

Chaque porte comporte une action prérédigée : une action corrective quand la note vaut 0 ou 1, une action conditionnelle quand elle vaut 2. Le tableau de bord classe les portes selon une clé égale à la note augmentée du numéro de la porte divisé par 100, de sorte que les égalités sont départagées dans l'ordre des portes, et affiche les cinq portes les moins bien notées avec leurs actions.

Note de lecture pour Kasiri : la porte 6 est en CRITICAL GAP uniquement parce que le tarif rémunère uniquement l'énergie ; la part fixe du chiffre d'affaires est donc de 0 %, sous le seuil de lacune de développement de 20 %. Ce seuil est illustratif : un tarif rémunérant uniquement l'énergie peut être bancable si le risque hydrologique est couvert par ailleurs, et l'utilisateur doit calibrer ce test selon l'appréciation des prêteurs.

### 6.18 Les 23 portes de maturité pour le bouclage et l'échelle de décision (30A_CLOSE_READINESS)

Chaque porte comporte un domaine, un indicateur de porte critique et soit un test automatique du modèle, soit un statut de preuve saisi par l'utilisateur (MET (franchie), PARTIAL (partielle), NOT MET (non franchie) ou NO EVIDENCE (sans preuve)). Les tests automatiques renvoient MET ou NOT MET.

| N° | Porte | Critique | Test ou preuve par défaut | Question |
|---|---|---|---|---|
| 1 | Série de débits d'au moins 15 ans et revue hydrologique indépendante | Oui | `AND(rec_years>=15,hyd_study=3)` | Q1 |
| 2 | Énergie P90 confirmée par le conseiller technique des prêteurs | Oui | PARTIAL | Q1 |
| 3 | Étude de faisabilité bancable validée par le conseiller technique des prêteurs | Oui | `fs_level=3` | Q1 |
| 4 | Reconnaissances géotechniques suffisantes pour un rapport de référence | Oui | PARTIAL | Q1 |
| 5 | EIES approuvée et conforme aux normes des prêteurs | Oui | `es_level=3` | Q2 |
| 6 | Plan d'action de réinstallation (PAR) approuvé et financé | Oui | `rap_level>=2` | Q2 |
| 7 | Licence de production et permis d'utilisation de l'eau accordés | Oui | PARTIAL | Q2 |
| 8 | Droits fonciers acquis pour toutes les emprises du projet | Oui | NOT MET | Q2 |
| 9 | CAE signé et approuvé par le régulateur | Oui | PARTIAL | Q2 |
| 10 | Convention de mise en œuvre ou de concession signée | Oui | PARTIAL | Q2 |
| 11 | Contrat de raccordement au réseau signé et transport financé | Oui | `tx_fin=1` | Q3 |
| 12 | Transport en service au plus tard à la COD de la centrale | Non | `tx_gap_yrs<=0` | Q3 |
| 13 | Contrat(s) EPC signé(s) avec prix ferme, date d'achèvement et pénalités forfaitaires | Oui | PARTIAL | Q6 |
| 14 | Dispositif d'O&M et équipe du maître d'ouvrage en place | Non | PARTIAL | Q6 |
| 15 | Garantie de paiement d'au moins 6 mois en place | Oui | `lc_months>=6` | Q7 |
| 16 | Capacité de paiement de l'acheteur au moins égale à 1,2 x la facture du CAE (pire des 10 premières années) | Oui | `ut_ratio10>=1.2` | Q7 |
| 17 | Plan de financement entièrement engagé (aucun écart de financement) | Oui | `fin_gap<=0.5` | Q5 |
| 18 | DSCR minimum égal ou supérieur à la cible de dimensionnement dans le cas sélectionné | Oui | `AND(debt_m+debt_c>0,kpi_min_dscr>=str_dscr)` | Q5 |
| 19 | Engagements en fonds propres signés et TRI des fonds propres égal ou supérieur à la cible | Oui | `IF(ISNUMBER(kpi_eirr),kpi_eirr>=str_hurdle,s_priv<=0)` | Q4 |
| 20 | Assurance contre le risque politique ou garanties signées | Non | NO EVIDENCE | Q5 |
| 21 | Soutien de l'État approuvé par le ministère des Finances ; filtre budgétaire autre que HIGH | Oui | `LEFT(sc_result,4)<>"HIGH"` | Q7 |
| 22 | Programme d'assurances placé (tous risques chantier, pertes d'exploitation anticipées (DSU)) | Non | PARTIAL | Q6 |
| 23 | Audit indépendant du modèle réalisé | Non | NO EVIDENCE | Q5 |

La porte 17 tolère un écart de financement allant jusqu'à 0,5 million USD. La porte 18 exige l'existence d'une dette, de sorte qu'une structure sans dette senior ne la franchit pas grâce au DSCR de substitution de 99. La porte 18 lit le cas sélectionné ; elle évolue donc avec les tests de résistance.

**Échelle de décision**, évaluée dans cet ordre :

```
IF fc_crit_fail>0     "STOP: a critical gate is not met"
ELSE IF fc_crit_noev>0 "STOP: critical evidence missing"
ELSE IF fc_crit_part>0 "NOT READY: critical gates partly met"
ELSE IF fc_met=fc_n    "GO: evidence complete for a close decision"
ELSE                   "CONDITIONAL GO: all critical gates met"
```

Dans l'ordre, ces libellés signifient : STOP (arrêt), une porte critique n'est pas franchie ; STOP, une preuve critique manque ; NOT READY (non prêt), des portes critiques sont partiellement franchies ; GO (feu vert), le dossier de preuves est complet pour une décision de bouclage ; CONDITIONAL GO (feu vert sous conditions), toutes les portes critiques sont franchies. Un GO indique que le dossier de preuves est complet pour que les prêteurs et les promoteurs décident ; ce n'est pas une recommandation d'investissement. Kasiri : 6 portes franchies sur 23, 7 portes critiques non franchies, 6 portes critiques partiellement franchies, décision STOP.

Le récapitulatif au bas de la feuille compte, pour chaque question, les portes, les portes franchies et les portes critiques non franchies ou sans preuve. Q8 correspond au total. Pour Kasiri : Q1 0 sur 4 franchie (2 critiques ouvertes), Q2 1 sur 6 (2), Q3 2 sur 2 (0), Q4 0 sur 1 (1), Q5 1 sur 4 (1), Q6 0 sur 3 (0), Q7 2 sur 3 (1), Q8 6 sur 23 (7).

---
