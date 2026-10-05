## 6. Méthodologie et formules clés

Les formules sont reprises de `model/build_model.py`, en remplaçant les références du gabarit par les noms de cellules simples du modèle. Un nom tel que `p50` est celui utilisé dans `model/model_map.json`. Dans une formule de série chronologique, « ligne » désigne la valeur de la même année.

### 6.1 Hydrologie et valeurs P (03_HYDROLOGY)

Débits moyens mensuels de long terme (janvier à décembre, m³/s) : 24, 20, 28, 52, 70, 58, 40, 28, 22, 30, 46, 36. Février compte 28,25 jours, l'année compte donc 365,25 jours. Pour chaque mois :

```
usable flow = MIN(MAX(flow-eflow,0),q_design)
power (MW)  = MIN(rho*grav*usable*head*eta_t*eta_g/1000000,inst_mw)
energy gross= power*days*24/1000
energy net  = energy gross*avail
spill       = MAX(flow-eflow-q_design,0)
```

Statistiques annuelles :

```
p50    = sum of monthly net energy
p75    = p50*(1-z75*cv)                 z75 = 0.6745
p90    = p50*(1-z90*cv)                 z90 = 1.2816 (one-year P90)
p90_10 = p50*(1-z90*cv*SQRT((1+rho1)/(1-rho1)/10))
cf     = p50/(inst_mw*8.76)
firm_mw= lowest monthly power*avail
```

Le P90 à dix ans est le P90 de l'énergie moyenne sur dix ans. La corrélation d'une année sur l'autre `rho1` (0,3 par défaut) traduit la persistance des années sèches : elle augmente la variance de la moyenne par le facteur (1+ρ)/(1−ρ)/n. Avec un coefficient de variation de 15 %, les valeurs de Kasiri sont : P50 292,5 GWh, P75 262,9, P90 à un an 236,3 et P90 à dix ans 268,3 GWh ; le rapport P90/P50 est de 0,81 et le facteur de charge de 55,6 %. La ligne de contrôle « puissance théorique au débit d'équipement » (*« theoretical power at design flow »*, 60,5 MW) doit être au moins égale à la puissance installée.

La feuille signale que l'énergie calculée à partir des débits moyens mensuels de long terme surestime la production lorsque, certaines années, les débits dépassent le débit d'équipement ; il faut la remplacer par une simulation sur l'ensemble de la série de débits lorsqu'elle existe.

### 6.2 Énergie (04_GENERATION)

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

Le modèle distingue l'énergie installée, disponible, produite, évacuable, livrée et contractée. L'écrêtement dû au transport ou au réseau est `gen-evacuable` ; l'écrêtement dû à l'insuffisance de la demande est `evacuable-delivered`. L'énergie contractée est la référence P50 `gen_p50`. La production du cas prêteurs `gen_len` n'intègre pas le facteur de sécheresse : la sécheresse est testée à part.

Le ratio d'évacuation provient de *09_GRID* :

```
peak       = peak0*d_dom/base-year domestic demand
absorb_mw  = MAX(0,peak*minload-mustrun)+ic_mw
line_mw    = IF(tx_ready=1,tx_mw,tx_interim)
evac_mw    = MIN(line_mw,absorb_mw)
evac_ratio = MIN(1,evac_mw/inst_mw)
```

Sur *10_DEMAND*, la demande croît par segment au taux de croissance du cas, augmenté de `eff_demg`, et elle est multipliée par `eff_dem` à partir de la date de mise en service commerciale (COD). L'énergie du projet absorbable est égale au déficit d'offre, plus la production thermique substituable, plus les exportations contractées. La demande bancable est `opflag*MIN(contracted,absorbable*commercial/(domestic+exp_con))` ; le plus faible rapport entre demande bancable et demande contractée sur les années d'exploitation 1 à 5 alimente la porte 2.

### 6.3 Construction du coût d'investissement (05_PLANT_CAPEX, 06_CONSTRUCTION, 08_TRANSMISSION)

Coût de la centrale en USD constants de 2026 :

| Poste | Kasiri (M USD) | Formule ou source |
|---|---|---|
| Génie civil | 68,0 | Donnée d'entrée |
| Équipements hydromécaniques | 9,0 | Donnée d'entrée |
| Équipements électromécaniques | 33,0 | Donnée d'entrée |
| Environnement et social | 5,0 | Donnée d'entrée |
| Ingénierie et supervision | 8,0 | Donnée d'entrée |
| Coûts du maître d'ouvrage | 4,0 | Donnée d'entrée |
| Coûts de développement remboursés au bouclage | 9,0 | `cx_dev = dev_total` depuis *01A_DEVELOPMENT* |
| Prime de risque de l'entrepreneur | 6,6 | `cx_epcprem = (cx_civil+cx_hm+cx_em)*epc_prem` |
| Sous-total | 142,6 | Somme |
| Provision pour aléas physiques 10 % | 14,3 | `capex_base = cx_sub*(1+cont)` |
| Coût de base de la centrale | 156,9 | 2 614 USD/kW ; 1,04 fois la référence de 2 515 USD/kW |

Le coût effectif de la centrale applique le cas, le stress de dépassement de coûts, la part des dépassements et des coûts de retard supportée par le maître d'ouvrage, ainsi que l'ajustement (flex) :

```
eff_capex  = case_capex*(1+st_capex*p_overrun*epc_owner)*(1+fx_capex)
capex_real = capex_base*eff_capex*(1+delay_cost*eff_delay*epc_owner_d)
```

L'échelonnement suit une courbe en S sinusoïdale sur la durée effective de construction N, dont la somme vaut exactement un quel que soit N, avec une indexation au taux `capex_esc` :

```
share_t   = IF(consflag=1,SIN(PI()*(t-0.5)/N)*SIN(PI()/(2*N)),0)
capex_nom = capex_real*share*escidx       escidx = (1+capex_esc)^(year-base_year)
```

Le coût de transport est `(tx_km*tx_cost_km+tx_sub+tx_reinf)*eff_capex` (16,7 millions USD constants pour Kasiri), dépensé sur `tx_build` années avant la date prévue de mise en service de la ligne, avec une pénalité de retard `(1+delay_cost*eff_tdelay)` répartie sur `tx_build+eff_tdelay` années. `tx_party` = 1 met la dépense à la charge de l'État, 2 à la charge du projet. La date de mise en service de la ligne est `start_year+cons_years+tx_lag+eff_tdelay` ; l'écart de préparation est la date de mise en service de la ligne moins la COD de la centrale.

### 6.4 Contractualisation de la construction (05A_CONTRACTING)

`epc_struct` sélectionne une colonne de paramètres indicatifs :

| Paramètre | 1 EPC clés en main | 2 Lots séparés | 3 Multicontrats |
|---|---|---|---|
| Prime de l'entrepreneur sur le génie civil, l'hydromécanique et l'électromécanique (`epc_prem`) | 12 % | 6 % | 0 % |
| Part d'un dépassement de coûts supportée par le maître d'ouvrage (`epc_owner`) | 30 % | 55 % | 90 % |
| Part du coût de retard supportée par le maître d'ouvrage après pénalités forfaitaires (`epc_owner_d`) | 35 % | 60 % | 90 % |
| Risque d'interface (1 faible à 3 élevé) | 1 | 2 | 3 |

La prime entre dans le coût de base ; les parts du maître d'ouvrage modulent les stress de dépassement et de retard dans `eff_capex` et `capex_real`. Un contrat clés en main coûte donc plus cher dans le cas de base et moins cher en cas de dépassement. Les simulations figées (snapshot) *« EPC 1/2/3 base »* et *« EPC 1/2/3 overrun 96% »* comparent les trois structures, la dette étant redimensionnée pour chacune.

### 6.5 Coûts d'exploitation (07_OPEX)

Les données d'entrée en termes réels sont indexées sur l'indice des prix à la consommation américain (US CPI) :

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

La réserve pour gros entretien est comptée comme un coût d'exploitation, et non comme un compte de réserve distinct.

### 6.6 CAE, tarif et revenus (14_PPA, 15_TARIFF, 16_REVENUE)

Le tarif de Kasiri rémunère uniquement l'énergie : paiement de capacité nul, prix de l'énergie de 112 USD/MWh (2026), indexé pour moitié sur l'US CPI, entièrement libellé en USD, avec paiement de l'énergie réputée livrée en cas d'écrêtement non imputable au vendeur.

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

Le défaut de paiement de la compagnie d'électricité est couvert par trois mécanismes successifs :

```
cov_backstop = IF(backstop=1,u_gap*bs_share,0)
ppag_lim     = str_ppag*ppag_months/12*rev_util
ppag_reimb   = opflag*MIN(previous ppag_out,MAX(0,u_maxppa-u_ppa))
cov_guar     = MIN(u_gap-cov_backstop,MAX(0,ppag_lim-previous ppag_out+ppag_reimb))
ppag_out     = previous ppag_out+cov_guar-ppag_reimb
unpaid       = u_gap-cov_backstop-cov_guar
rev_cash     = rev_bill-unpaid
```

La garantie est plafonnée à `ppag_months` mois de facturation de la compagnie d'électricité (12 par défaut) et la compagnie la rembourse sur sa capacité de paiement excédentaire ; tout montant au-delà devient un arriéré envers le projet.

Les revenus du cas prêteurs utilisent le cas de production des prêteurs :

```
rev_len = rev_cap+enc*IF(deemed=1,gen_len,MIN(gen_len*evac_ratio,d_absorb))/1000
```

Indicateurs de qualité des revenus : part fixe des revenus facturés (`rev_fixed`, 0 % pour Kasiri), revenus à risque entre P50 et P90 la 2e année d'exploitation, part des revenus provenant de la compagnie d'électricité, et soutien nécessaire sur la durée de vie pour maintenir les paiements au titre du CAE. Sur *15_TARIFF*, la marge d'accessibilité tarifaire est égale aux revenus encaissés par la compagnie d'électricité par MWh injecté, moins le tarif moyen pondéré du CAE.

### 6.7 Module de développement (01A_DEVELOPMENT)

**Étapes.** Six étapes, chacune avec sa durée, son budget en termes réels et sa probabilité de succès jusqu'à l'étape suivante :

| Étape | Mois | Budget (M USD constants) | P(succès) |
|---|---|---|---|
| 1 Identification du site et reconnaissance | 6 | 0,10 | 60 % |
| 2 Préfaisabilité et début du jaugeage des débits | 12 | 0,60 | 60 % |
| 3 Étude de faisabilité, EIES, études géotechniques et de réseau | 18 | 4,50 | 70 % |
| 4 Licences, droits d'eau, foncier et permis | 12 | 0,80 | 85 % |
| 5 CAE, convention de mise en œuvre et approbation du tarif | 12 | 0,80 | 80 % |
| 6 Financement : conseillers, juristes, assurances, bouclage | 12 | 2,20 | 85 % |
| Total | 72 | 9,00 | 14,6 % |

```
dev_total = sum of budgets
dev_years = sum of months/12
dev_pfc   = PRODUCT(p1:p6)
dev_pct   = dev_total/capex_real
```

**Profil de dépenses.** Les étapes s'enchaînent sans interruption et s'achèvent au bouclage financier. Le budget de chaque étape est réparti uniformément sur ses mois et affecté aux dix colonnes d'années de développement précédant le bouclage (2017 à 2026), puis indexé par `(1+us_cpi)^(year-base_year)`. Pour Kasiri, les dépenses courent de 2021 à 2026 et totalisent 8,6 millions USD courants.

**P(en vie).** Pour chaque année de développement, la probabilité que le projet soit encore en vie au moment de la dépense est la moyenne, pondérée par les dépenses de chaque étape, de la probabilité d'atteindre cette étape, `PRODUCT(p1:pk)/pk`.

**VAN pondérée par le risque.** Avec r = `dev_rate` (25 %) et toutes les valeurs actuelles calculées au début du développement :

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

Kasiri : valeur au bouclage sur le scénario de succès de 11,27 millions USD ; VAN sur le scénario de succès de -1,00 million USD ; VAN pondérée par le risque de -0,95 million USD.

**Prime et probabilité de point mort.**

```
dev_be_prem = MAX(0,dev_prem-dev_enpv*(1+r)^(dev_months/12)/dev_pfc)
dev_be_p    = IF(dev_npv_success<=0,"n/a: negative on the success path",dev_pv_cost_rw/dev_pv_success)
```

Kasiri a besoin d'une prime de 29,7 millions USD (18,9 % du coût de la centrale) pour obtenir une VAN pondérée par le risque nulle, et n'a pas de probabilité de point mort, car le scénario de succès lui-même détruit de la valeur à 25 %.

**Valeur par étape (section D2).** Pour l'étape k sur le point de commencer, avec des budgets réels c, des durées d et un mois de début s :

```
B (P close from here) = PRODUCT(pk:p6)
C (PV value at close) = B*dev_success_value/(1+r)^((dev_months-s_k)/12)
D (PV remaining spend)= sum over j>=k of c_j*PRODUCT(pk:p(j-1))/(1+r)^((s_j-s_k+0.5*d_j)/12)
E (position value)    = C-D
```

| Étape sur le point de commencer | P(bouclage) | Valeur au bouclage | Dépenses restantes | Valeur de la position |
|---|---|---|---|---|
| 1 | 14,6 % | 0,43 | 1,63 | -1,20 |
| 2 | 24,3 % | 0,80 | 2,86 | -2,06 |
| 3 | 40,5 % | 1,67 | 4,84 | -3,17 |
| 4 | 57,8 % | 3,34 | 2,06 | 1,28 |
| 5 | 68,0 % | 4,91 | 1,98 | 2,93 |
| 6 | 85,0 % | 7,67 | 1,97 | 5,70 |

La VAN de la section D (dépenses courantes, année par année) et la valeur à l'étape 1 de la section D2 (budgets réels en milieu d'étape) répondent à la même question par deux voies différentes ; le Livre 7 utilise la première pour la décision de lancer le projet et la seconde pour fixer le prix d'entrée.

**Revalorisations (section E), fonds propres privés à 100 %.**

```
val_fc       = NPV(r_fc,eq_priv_cf)+NPV(r_fc,eq_priv_in)
val_step_fc  = NPV(r_fc,eq_priv_cf)
val_cod      = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))/(1+r_fc)^cons_eff
val_step_cod = val_cod-SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_fc)^t)
```

Kasiri : valeur créée au bouclage de -5,1 millions USD (le TRI des fonds propres est inférieur au taux de 15 % retenu au stade du bouclage) ; revalorisation liée à la réduction des risques entre le bouclage et la COD de 18,3 millions USD.

**Cession partielle (section F).**

```
v_cod_nom     = SUMPRODUCT(opflag,eq_priv_cf,1/(1+r_cod)^(t-cons_eff))
sell_proceeds = sell_pct*dev_stake*v_cod_nom
```

Le flux de trésorerie du développeur s'étend sur 50 colonnes (dix années de développement et les 40 années du modèle) : les dépenses de développement en négatif ; à t = 1, le remboursement plus la prime ; chaque année du modèle, `dev_stake` fois le flux de trésorerie des fonds propres privés, réduit de `(1-sell_pct)` pendant les années d'exploitation ; et le produit de cession la dernière année de construction. Kasiri : produit de cession de 19,5 millions USD, multiple de trésorerie de 4,97x, pic de trésorerie cumulée à risque de 10,2 millions USD.

**TRI du développeur avec trois valeurs de départ.**

```
dev_irr = IF(ISNUMBER(IRR(cf,0.15)),IF(ABS(IRR(cf,0.15))<1,IRR(cf,0.15),-1),
          IF(ISNUMBER(IRR(cf,0.05)),IF(ABS(IRR(cf,0.05))<1,IRR(cf,0.05),-1),
          IF(ISNUMBER(IRR(cf,-0.05)),IF(ABS(IRR(cf,-0.05))<1,IRR(cf,-0.05),-1),-1)))
```

Le flux de trésorerie du développeur change plusieurs fois de signe ; la valeur de départ a donc une importance. La formule essaie 15 %, puis 5 %, puis -5 %, et ne passe à la valeur suivante que si la précédente renvoie une erreur ; un résultat de valeur absolue supérieure ou égale à 1 est considéré comme aberrant et affiché à -1 (-100 %). Kasiri : 16,0 %. Les intéressements des promoteurs (promote) et le carried interest ne sont pas modélisés.

### 6.8 Structures de financement (17A_STRUCTURES)

La colonne C lit la structure sélectionnée dans les colonnes E à I avec `INDEX(E:I,structure)`.

| Paramètre | 1 Public | 2 PIE | 3 PPP | 4 Hybride | 5 Mixte |
|---|---|---|---|---|---|
| Fonds propres de l'État | 15 % | 0 % | 10 % | 0 % | 5 % |
| Subventions, financement de l'écart de viabilité (VGF), capital public | 0 % | 0 % | 5 % | 35 % | 8 % |
| Dette concessionnelle | 55 % | 0 % | 30 % | 25 % | 35 % |
| Plafond d'endettement (dette senior totale) | 85 % | 70 % | 75 % | 55 % | 72 % |
| Fonds propres privés maximum | 0 % | 35 % | 20 % | 25 % | 25 % |
| Apporteur des fonds propres résiduels | État | Privé | Privé | Privé | Privé |
| Dette senior garantie par l'État | 100 % | 0 % | 40 % | 20 % | 15 % |
| Dette senior comptabilisée en dette publique | 100 % | 0 % | 0 % | 0 % | 0 % |
| Garantie souveraine du CAE | Non | Oui | Oui | Oui | Oui |
| Obligation d'indemnité de résiliation | Non | Oui | Oui | Oui | Oui |
| Couverture du risque de convertibilité des devises | 0 % | 100 % | 100 % | 100 % | 50 % |
| Taux concessionnel / différé / durée | 2,0 % / 5 / 20 | 3,0 % / 5 / 20 | 3,0 % / 5 / 20 | 3,0 % / 5 / 20 | 2,5 % / 5 / 20 |
| Taux commercial / maturité | 7,5 % / 15 | 8,0 % / 16 | 7,5 % / 16 | 7,5 % / 16 | 7,2 % / 18 |
| DSCR de dimensionnement | 1,20 | 1,35 | 1,30 | 1,30 | 1,30 |
| TRI cible des fonds propres privés | 10 % | 15 % | 14 % | 14 % | 13 % |

Les pourcentages s'entendent en proportion de la base de financement. Conditions communes : DSCR de blocage des distributions (lock-up) de 1,10x, commissions de mise en place et d'engagement de 2 % de la dette senior, DSRA égal à six mois du service de la dette de l'année suivante. Un contrôle de structure vérifie que les subventions, les fonds propres de l'État, la dette maximale et les fonds propres privés maximum peuvent couvrir 100 % du besoin.

La comparaison analytique en temps réel est un filtre, elle ne remplace pas le moteur de calcul complet :

```
WACC     = (goveq+govx)*gov_disc+conc*rc+comm*rm+priv*hurdle/(1-tax_rate)
WACC_ex  = WACC/(1-grant)
CRF      = WACC_ex/(1-(1+WACC_ex)^-ops_years)
tariff   = (fund_base*(1+maxdebt*(idc_km+upfront_fee))*(1-grant)*CRF+opex_y2)/p50*1000
exposure = public capital+on-budget debt+MAX(guaranteed debt+PPA guarantee,termination)
```

où la dette commerciale est supposée égale au plafond d'endettement moins la dette concessionnelle. Les chiffres à citer sont ceux de la simulation figée du moteur complet sur la même feuille et du tarif requis calculé par le programme d'exécution pour les structures 2 à 5.
