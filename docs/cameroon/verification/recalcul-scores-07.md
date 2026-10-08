# Recalcul indépendant des scores du module 07 (IOS)

> Provenance : rapport rédigé par l'agent de recalcul le 2026-10-08. La section 5 est reformulée en description (même contenu) au lieu des lignes de tableau exactes. L'outil lui a refusé l'écriture du
> fichier ; il a été enregistré par la session principale sur instruction explicite de
> l'utilisateur. Le script a été exécuté par l'agent ; la session principale a refait à la main les
> calculs du scénario A avant de l'appliquer au module 07.

Date : 2026-10-08. Objet : `docs/cameroon/07-investment-intelligence.md` (§3 méthode, §4 fiches, §5 synthèse), avec la règle de conversion du §9 de `06-market-trade.md` et le journal `verification/harmonisation.md`. **Aucun module n'a été modifié par l'agent** : ce rapport propose des remplacements (dernière section) sans les appliquer.

Règles reprises telles que publiées :
- **Poids et calcul** : G 15, R 20, I 20, M 10, Reg 10, E 15, K 10. IOS = Σ(note × poids) / 5 × 100, arrondi à l'unité (x,5 au supérieur). Test obligatoire à poids égaux ; un rang qui bouge de plus de 2 places rend le classement « fragile » (§3.4).
- **Données manquantes** : R et E sans donnée publique = 1 (ND) ; pour les autres critères, la note la plus prudente justifiable. Données de plus de 2 ans : note plafonnée à 3 et marquée ⚠. IC = nombre de critères notés sur des faits [F] de moins de 2 ans, sur 7 ; IC ≤ 2/7 = « non classable » (§3.5).
- **Conversion M06 → M** : note d'attractivité du 06 arrondie à l'entier, même note pour un même couple produit × marché. M ≤ 2 si la clause B = 1 a joué. Les produits non couverts par le 06 sont notés « hors module 06 » (§3.3 du 07 ; §9 du 06).

## 1. Script

Le script recalcule les attractivités du module 06 à partir de leurs barèmes (§7.2 à 7.6), applique la conversion, puis recalcule IOS, IOS à poids égaux, IC et rang. Il contrôle aussi le plafond, la règle ND et la conversion, et fait les tests de robustesse. Il calcule enfin les scénarios corrigés A et B (§3).

**Lecture stricte de l'IC.** Le module ne publie pas, critère par critère, ce qui compte dans l'IC. Le script compte un critère seulement si sa note repose sur au moins un fait [F] postérieur au 2024-10-08. Ne comptent pas : une note ND, une note ⚠, une note [?] ou [I] seule, ni une ressource « non conforme ». Cette dernière exclusion est déduite des IC publiés d'O4 et d'O9, que l'on ne retrouve qu'avec elle.

```python
# Recalcul indépendant de l'IOS du module 07 (édition Cameroun), version du 2026-10-08.
from decimal import Decimal, ROUND_HALF_UP
import copy

CRIT = ["G", "R", "I", "M", "Reg", "E", "K"]
W = {"G": 15, "R": 20, "I": 20, "M": 10, "Reg": 10, "E": 15, "K": 10}   # §3.4

def rnd(x):  # arrondi à l'unité, x,5 au supérieur
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def att(notes):  # module 06 §7.1 règle 1 : ND exclus, poids renormalisés
    return sum(n * p for n, p in notes) / sum(p for _, p in notes)
M06 = {
    "bauxite>Chine":   (att([(5, 30), (2, 20), (1, 15)]), False),           # 3,15
    "fer>Chine":       (att([(5, 30), (1, 20), (1, 15)]), False),           # 2,85
    "alu>UE":          (att([(5, 30), (4, 20), (4, 20), (3, 15)]), False),  # 4,18
    "ciment>Cameroun": (att([(3, 30), (5, 20), (3, 15), (5, 15)]), False),  # 3,88
    "or>EAU":          (att([(5, 30), (5, 20), (4, 20)]), False),           # 4,71
}
def m_conv(key):
    v, elim = M06[key]; m = rnd(v)
    return min(m, 2) if elim else m

# statut : ok = fait [F] < 2 ans ; ND ; old = données > 2 ans (plafond 3, ⚠) ; ? = [?]/[I] seul ; nc = non conforme
PUB = {
 "O1":  dict(n=[4,5,3,3,3,3,2], m06="bauxite>Chine", ios=69, eq=66, ic=6, rank="1",
             st=dict(G="ok",R="ok",I="ok",M="ok",Reg="old",E="ok",K="ok")),
 "O8":  dict(n=[4,3,2,5,3,3,3], m06="or>EAU", ios=63, eq=66, ic=6, rank="2",
             st=dict(G="ok",R="ok",I="?",M="ok",Reg="ok",E="ok",K="ok")),
 "O9":  dict(n=[3,2,3,5,4,2,2], m06="or>EAU", ios=57, eq=60, ic=4, rank="3",
             st=dict(G="ok",R="nc",I="?",M="ok",Reg="ok",E="ND",K="ok")),
 "O4":  dict(n=[3,2,3,3,3,2,2], m06="fer>Chine", ios=51, eq=51, ic=5, rank="4=",
             st=dict(G="ok",R="nc",I="ok",M="ok",Reg="old",E="ok",K="ok")),
 "O5":  dict(n=[3,2,3,3,3,2,2], m06="fer>Chine", ios=51, eq=51, ic=5, rank="4=",
             st=dict(G="ok",R="nc",I="ok",M="ok",Reg="ok",E="ok",K="ok")),
 "O6":  dict(n=[3,3,2,3,2,2,2], m06=None, ios=49, eq=49, ic=4, rank="6",
             st=dict(G="old",R="old",I="?",M="ok",Reg="ok",E="old",K="ok")),
 "O10": dict(n=[3,1,2,4,3,1,3], m06="ciment>Cameroun", ios=44, eq=49, ic=3, rank="7",
             st=dict(G="ok",R="ND",I="?",M="ok",Reg="?",E="ND",K="ok")),
 "O7":  dict(n=[2,1,3,4,3,1,2], m06=None, ios=43, eq=46, ic=3, rank="8",
             st=dict(G="old",R="ND",I="?",M="?",Reg="ok",E="old",K="ok")),
 "O3":  dict(n=[3,3,1,3,2,1,1], m06="fer>Chine", ios=40, eq=40, ic=4, rank="9",
             st=dict(G="old",R="old",I="ok",M="ok",Reg="ok",E="ND",K="ok")),
}
O2 = dict(n=dict(I=3, M=4, Reg=3, E=2, K=2), m06="alu>UE", ios=55, ic=4)

def ios(notes, w=W):
    tot = sum(w[c] for c in notes)
    return sum(notes[c] * w[c] for c in notes) / (5 * tot) * 100

def ranks(scores):  # ex aequo = même rang
    s = sorted(scores.items(), key=lambda kv: -kv[1]); out = {}
    for k, v in s:
        r = 1 + sum(1 for _, v2 in s if v2 > v)
        out[k] = f"{r}=" if sum(1 for _, v2 in s if v2 == v) > 1 else str(r)
    return out

def checks(d):
    notes = dict(zip(CRIT, d["n"])); msgs = []
    for c in CRIT:
        st = d["st"][c]
        if st == "old" and notes[c] > 3: msgs.append(f"{c}={notes[c]} > plafond 3")
        if st == "ND" and c in ("R", "E") and notes[c] != 1: msgs.append(f"{c}={notes[c]} alors que ND -> 1")
    if d["m06"] and notes["M"] != m_conv(d["m06"]): msgs.append(f"M ≠ conversion 06 ({m_conv(d['m06'])})")
    return msgs

def ic(d): return sum(1 for c in CRIT if d["st"][c] == "ok")

def table(data, w=W):
    sc = {k: ios(dict(zip(CRIT, d["n"])), w) for k, d in data.items()}
    return sc, ranks({k: rnd(v) for k, v in sc.items()})

if __name__ == "__main__":
    print("Conversion 06 -> M :", {k: (round(v, 3), m_conv(k)) for k, (v, _) in M06.items()})
    eqw = {c: 1 for c in CRIT}
    sc, rk = table(PUB); sce, rke = table(PUB, eqw)
    for k, d in PUB.items():
        print(f"{k:4} IOS pub {d['ios']:3} calc {sc[k]:6.2f}->{rnd(sc[k]):3} | égaux pub {d['eq']:3} calc {sce[k]:6.2f}->{rnd(sce[k]):3}"
              f" | IC pub {d['ic']} strict {ic(d)} | rang pub {d['rank']:3} calc {rk[k]:3} égaux {rke[k]:3} | {checks(d) or 'règles OK'}")
    print(f"O2 IOS calc {ios(O2['n']):.2f} | égaux {ios(O2['n'], eqw):.2f} | M conv {m_conv('alu>UE')}")
    base = {k: int(r.rstrip('=')) for k, r in rk.items()}
    for c in CRIT:
        w2 = {x: W[x] for x in CRIT if x != c}
        s2 = {k: rnd(ios({x: dict(zip(CRIT, d['n']))[x] for x in w2}, w2)) for k, d in PUB.items()}
        r2 = ranks(s2)
        print(f"sans {c:3}: écart max {max(abs(int(r2[k].rstrip('='))-base[k]) for k in PUB)} | "
              + " ".join(f"{k}:{s2[k]}({r2[k]})" for k in sorted(PUB, key=lambda k: -s2[k])))
    print("poids égaux : écart max", max(abs(int(rke[k].rstrip('=')) - base[k]) for k in PUB))
    def scen(changes, extra_st=None):
        D = copy.deepcopy(PUB)
        for (k, c), v in changes.items(): D[k]["n"][CRIT.index(c)] = v
        for (k, c), v in (extra_st or {}).items(): D[k]["st"][c] = v
        return D
    A = {("O9","E"):1, ("O5","E"):1, ("O7","M"):2, ("O7","I"):2, ("O9","I"):2, ("O9","Reg"):3}
    B = {**A, ("O8","Reg"):2, ("O7","Reg"):2, ("O5","I"):2, ("O1","E"):4}
    for nm, ch in (("A", A), ("B", B)):
        D = scen(ch, {("O5","E"):"ND"}); s, r = table(D); se, re_ = table(D, eqw)
        print(f"== Scénario {nm} ==")
        for k in sorted(D, key=lambda k: -s[k]):
            print(f"{k:4} IOS {rnd(s[k]):3} rang {r[k]:3} | égaux {rnd(se[k]):3} rang {re_[k]:3} | IC strict {ic(D[k])}"
                  + ("  NON CLASSABLE" if ic(D[k]) <= 2 else ""))
        bA = {k: int(v.rstrip('=')) for k, v in r.items()}
        print("écart max poids égaux :", max(abs(int(re_[k].rstrip('=')) - bA[k]) for k in D))
        for c in CRIT:
            w2 = {x: W[x] for x in CRIT if x != c}
            r2 = ranks({k: rnd(ios({x: dict(zip(CRIT, d['n']))[x] for x in w2}, w2)) for k, d in D.items()})
            print(f"  sans {c}: écart max {max(abs(int(r2[k].rstrip('=')) - bA[k]) for k in D)}")
```

## 2. Publié vs recalculé (notes publiées)

| Opp. | G-R-I-M-Reg-E-K | IOS pub. | IOS recalc. | Égaux pub. | Égaux recalc. | IC pub. | IC strict | Rang pub. / recalc. / égaux |
|---|---|---|---|---|---|---|---|---|
| O1 | 4-5-3-3-3⚠-3-2 | 69 | 69,00 | 66 | 65,71 → 66 | 6 | 6 | 1 / 1 / 1= |
| O8 | 4-3-2-5-3-3-3 | 63 | 63,00 | 66 | 65,71 → 66 | 6 | 6 | 2 / 2 / 1= |
| O9 | 3-2-3-5-4-2-2 | 57 | 57,00 | 60 | 60,00 | 4 | 4 | 3 / 3 / 3 |
| O4 | 3-2-3-3-3-2-2 | 51 | 51,00 | 51 | 51,43 → 51 | 5 | 5 | 4= / 4= / 4= |
| O5 | 3-2-3-3-3-2-2 | 51 | 51,00 | 51 | 51,43 → 51 | 5 | **6** | 4= / 4= / 4= |
| O6 | 3⚠-3-2-3-2-2⚠-2 | 49 | 49,00 | 49 | 48,57 → 49 | 4 | **3** | 6 / 6 / 6= |
| O10 | 3-1-2-4-3-1-3 | 44 | 44,00 | 49 | 48,57 → 49 | 3 | 3 | 7 / 7 / 6= |
| O7 | 2-1-3-4-3-1-2 | 43 | 43,00 | 46 | 45,71 → 46 | 3 | **2** | 8 / 8 / 8 |
| O3 | 3⚠-3⚠-1-3-2-1-1 | 40 | 40,00 | 40 | 40,00 | 4 | 4 | 9 / 9 / 9 |
| O2 (à part) | I-M-Reg-E-K 3-4-3-2-2 | 55 | 180/325 = 55,38 → 55 | — | 56,00 | 4 | — | à part |

- **Arithmétique** : exacte partout.
- **Conversion M06 → M** : exacte. Bauxite → Chine 3,154 → 3 ; fer → Chine 2,846 → 3 ; aluminium → UE 4,176 → 4 ; ciment → Cameroun 3,875 → 4 ; or → EAU 4,714 → 5. Aucune clause B = 1.
- **Plafond de 3** : respecté.
- **IC**, trois écarts dus à la lecture de la règle :
  - **O5** : l'écart disparaît si E est noté ND (anomalie A6).
  - **O6** : R repose sur la BFS de 2011 ; les chiffres 2026 de la Sonamines sont sans code.
  - **O7** : G, E et une partie de K reposent sur les conclusions d'Eramet d'octobre 2023. En lecture stricte, IC = 2/7, donc O7 serait « non classable » (règle 3.5 n° 3).

## 3. Anomalies

### 3.1 Violations de règle (scénario A)

| # | Opp. | Critère | Publié → conforme | Motif (faits de la fiche → règle) |
|---|---|---|---|---|
| A1 | O9 | E | 2 → **1 (ND)** | La fiche indique « Non publié ; seul un chiffre d'affaires cible de 60 M$/an ». Un chiffre d'affaires n'est pas un indicateur E (§3.2), et le descripteur 2 exige un capex déclaré. Règle 3.5 n° 1 |
| A2 | O7 | M | 4 → **2** | Hors module 06, sans fait ; la fiche dit « marché étroit mais à forte valeur [I] ». Le descripteur 2 correspond à « marché étroit ou volatil » ; le 4 suppose un « marché profond ». Règle de la note la plus prudente |
| A3 | O7 | I | 3 → **2** | « Proximité de Yaoundé [I] ; non vérifié [?] ». Le 3 suppose un maillon manquant financé. Les autres infrastructures [?] sont notées 2 (O6, O8, O10) |
| A4 | O9 | I | 3 → **2** | « Besoin limité [I] ; non documentée [?] ». Même motif que A3 |
| A5 | O9 | Reg | 4 → **3** | Mborguéné : mise en exploitation exigée sous 2 ans, sous peine de retrait. Colomine : acte de 2022 ⚠, 16,7 kg produits contre 500 kg/an. Le descripteur 3 correspond à un « titre délivré, conditions » |
| A6 | O5 | E | 2 → **1 (ND)** | Aucun capex de projet. Les 41,2 Md FCFA sont un financement, exclu de E (→ module 08, §3.2). Les 570 Md FCFA de l'annexe ne sont pas un capex (C3). La valorisation est rejetée |
| A7 | O4, O6, O7 | marquage | ⚠ manquant | Reg d'O4 (actes de 2022), R d'O6 (2011), G et E d'O7 (Eramet 2023) : les fiches marquent ⚠, pas le tableau (règle 3.5 n° 5) |

Effet sur l'IOS : O9 passe de 57 à **48**, O5 de 51 à **48**, O7 de 43 à **35**. Nouveau classement : O1 69 (1), O8 63 (2), O4 51 (3), O6 49 (4), O9 et O5 48 (5=), O10 44 (7), O3 40 (8), O7 35 (9).

### 3.2 Lectures de descripteur à arbitrer (scénario B = A + B1 à B4)

- **B1, O8 Reg 3 → 2** : la licence d'exploitation de Bibemi est seulement demandée (juin 2024), la convention est en négociation, et Mbe n'a que des licences d'exploration.
- **B2, O7 Reg 3 → 2** : situation identique à celle d'O6 (actif repris par l'État, AMI infructueux), qui est noté 2.
- **B3, O5 I 3 → 2** : pas de terminal ; celui de Kribi est confié à Sinosteel (O4) et n'est pas financé pour G-Stones.
- **B4, O1 E 3 → 4** : DFS de moins de 2 ans. La contestation des hypothèses de prix et de fret relève du module 08 (§3.6). Avec 3, la DFS est notée comme la PEA interne d'O8.
- **B5, O3 E « 1 (ND) »** : un investissement de ~10 Md$ est annoncé par la presse, donc « ND » est inexact. Garder 1 avec le libellé « pas d'étude ».
- **B6, O6 E 2⚠** : une BFS de 2011 correspond au descripteur 4, plafonné à 3. Le 2 est plus sévère que la grille ; le corriger ne change pas le rang.
- **B7, O8 et O9 M = 5** : conforme à la règle, mais le couple EAU est un circuit informel, alors que la Sonamines a l'exclusivité de commercialisation de l'or. Il n'y a pas d'offtake.
- **B8, O3, O4 et O5 M = 3** : conforme à la règle, mais le couple fer → Chine est « Faible » dans le 06 (2,85). La règle ne plafonne à 2 que les cas où la clause B = 1 a joué.
- **B9, O2** : le « meilleur couple » de l'aluminium est la Turquie (4,29, 3 critères), pas l'UE (4,18). M = 4 dans les deux cas.

Classement en scénario B : O1 72 ; O8 61 ; O4 51 ; O6 49 ; O9 48 ; O5 et O10 44 (6=) ; O3 40 ; O7 33.

## 4. Robustesse

**Notes publiées**
- À poids égaux, l'écart maximal est de **1 place** : O1 et O8 sont à 1= (65,71), O6 et O10 à 6=. Le classement n'est pas fragile.
- En retirant chaque critère à tour de rôle, l'écart maximal est de 2 places :
  - sans R : O8 passe 1ᵉʳ, O1 et O9 à 2= ;
  - sans I : O6 monte de 6 à 4, O3 de 9 à 7= ;
  - sans Reg : O6 à 4= ;
  - sans G, M, E ou K : 0 ou 1 place.

**Scénario A**
- À poids égaux, l'écart maximal est de 2 places (O9 de 5= à 3= ; O10 de 7 à 5=).
- En retirant R, l'écart atteint **3 places** : O10 monte de 7 à 4=, car sa note R = 1 (ND) disparaît. Son rang dépend donc surtout de la règle ND.

**Scénario B** : 2 places au plus dans tous les tests.

**Conclusion** : la tête (O1, O8) et la queue (O3, O7) sont robustes. Le milieu (O4, O5, O6, O9, O10, de 44 à 51) est serré. La 3ᵉ place d'O9 ne résiste pas à l'application stricte des règles.

## 5. Remplacements proposés (scénario A et marquage ⚠ ; les points B sont à arbitrer)

| Texte actuel exact | Texte proposé |
|---|---|
| Ligne O9 du tableau §5.1 (rang 3, notes 3-2-3-5-4-2-2, IOS 57, égaux 60, IC 4) | Rang 5=, notes 3-2-2-5-3-1 (ND)-2, IOS **48**, égaux 51, IC 4 (après O6) |
| Ligne O4 (rang 4=, Reg 3) | Rang 3, Reg « 3 ⚠ », IOS 51 inchangé |
| Ligne O5 (rang 4=, E 2, IOS 51, égaux 51) | Rang 5=, E « 1 (ND) », IOS **48**, égaux 49, IC 5 (après O9) |
| Ligne O6 (rang 6, R 3) | Rang 4, R « 3 ⚠ », IOS 49 inchangé (IC 3 en lecture stricte : à arbitrer) |
| Ligne O7 (rang 8, G 2, I 3, M 4, E 1, IOS 43, égaux 46) | Rang 9, G « 2 ⚠ », I 2, M 2, E « 1 ⚠ », IOS **35**, égaux 37 (en lecture stricte, IC 2 et « non classable » : à arbitrer) |
| Ligne O3 (rang 9) | Rang 8 |
| Phrase de robustesse du §5.3 | Ajouter : O9 remonte de 5= à 3= et O10 de 7 à 5= à poids égaux ; le milieu (44 à 51) reste serré ; sans R, O10 passe de 7 à 4= |
| Fiche O9, ligne « Capex public » | Préciser : pas un indicateur E au sens du §3.2 : E = 1 (ND) |
| Fiche O5, ligne « Capex public » | Préciser : aucun capex de projet publié ; le financement de 41,2 Md FCFA relève du module 08 (§3.2 ; E = 1 (ND)) |

Ordre du tableau §5.1 après remplacement : O1, O8, O4, O6, O9, O5, O10, O3, O7.
