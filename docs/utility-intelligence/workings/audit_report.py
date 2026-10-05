"""Build the step-1 document availability audit report (Markdown + JSON) from the workflow output."""
import json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(__file__)
OUT = sys.argv[1]
d = json.load(open(os.path.join(HERE, 'audit_raw.json')))
audits, spot = d['audits'], d['spot']

# Corrections from the independent spot-check (applied to the audit data)
FIX = {
    ('KETRACO', '2022/23'): {'audit_opinion': 'qualified', 'note': 'Spot-check: Auditor-General opinion is QUALIFIED ("Inaccuracies in the Financial Statements"); the auditing agent had not read it.'},
    ('Eko Electricity Distribution (EKEDC)', '2023'): {'audit_opinion': 'unmodified', 'note': 'Spot-check: opinion page (PDF p13) readable, PwC, unmodified.'},
    ('SONATREL', '2025'): {'audit_opinion': 'not_visible', 'note': 'Spot-check: KPMG Art. 715 report on DRAFT statements (22 June 2026) announcing a future unqualified opinion with an observation; not a final signed opinion.'},
}
for a in audits:
    for u in a['utilities']:
        for y in u['years']:
            for (name, fy), fx in FIX.items():
                if u['name'].startswith(name) and y['fiscal_year'].startswith(fy):
                    y['audit_opinion'] = fx['audit_opinion']
                    y['notes'] = (y['notes'] + ' ' + fx['note']).strip()

utils = [u for a in audits for u in a['utilities']]
AR = {'found_fetched': '●', 'found_link_not_fetched': '◐', 'referenced_only': '○', 'not_found': '·', 'not_checked': '?'}
FS = {'full_with_notes': '●', 'summary_or_extract': '◐', 'unaudited_only': 'u', 'not_found': '·', 'not_checked': '?'}
VIA = {'strong': 'fort', 'usable': 'utilisable', 'weak': 'faible', 'not_viable': 'non viable'}
SCOPE = {'integrated': 'intégrée', 'distribution': 'distribution', 'generation': 'production', 'transmission': 'transport', 'other': 'autre', 'single_buyer': 'acheteur unique', 'generation_transmission': 'prod.+transport', 'unknown': 'inconnu'}
ST = ['computable', 'partially_computable', 'reported_value_only', 'not_in_documents_read', 'not_applicable']
STFR = {'computable': 'calculable', 'partially_computable': 'partiel', 'reported_value_only': 'valeur publiée seule', 'not_in_documents_read': 'absent des docs lus', 'not_applicable': 'non applicable'}

agg = defaultdict(Counter)
for u in utils:
    for k in u['kpi_coverage']:
        agg[k['kpi_id']][k['status']] += 1
kpi_order = [k['kpi_id'] for k in utils[0]['kpi_coverage']]

via = Counter(u['mvp_viability'] for u in utils)
spot_c = Counter(c['verdict'] for c in spot['checks'])

L = []; w = L.append
w('# Étape 1 : audit de disponibilité des documents publics (v0.1)\n')
w(f'> Audit réalisé le 5 octobre 2026 par 8 agents de recherche (un par groupe de pays), suivi d’une contre-vérification indépendante. '
  f'Il couvre **{len(utils)} utilities dans 11 pays**, les exercices 2019 à 2025, et les 23 KPI du noyau MVP hors variables de contexte (voir `KPI_DICTIONARY.md`). '
  'Aucune valeur de KPI n’est relevée ici : l’audit dit seulement si les **données d’entrée** existent et où elles se trouvent.\n')

w('## Conclusions principales\n')
w(f'1. **Viabilité MVP** : {via["strong"]} fortes, {via["usable"]} utilisables, {via["weak"]} faibles, {via["not_viable"]} non viable. '
  'Les utilities cotées ou soumises à un auditeur public qui publie ses rapports (Kenya, Ghana pour GRIDCo, Afrique du Sud, Zambie) et Senelec forment le socle. '
  '**L’Afrique centrale francophone est le maillon faible** : E2C (Congo) ne publie rien en ligne ; SNEL (RDC) et SONABEL (Burkina) ne sont accessibles que via le régulateur ou les bailleurs.')
w('2. **Le biais de transparence est confirmé.** Les utilities les moins transparentes ne pourraient pas être notées sur la finance. Elles seraient donc soit absentes, soit pénalisées par la seule dimension Gouvernance. '
  'Il faut afficher un **taux de couverture** et ne pas publier de classement agrégé pour elles.')
w('3. **Les régulateurs et les bailleurs sont des sources de premier rang**, pas des compléments : rapports trimestriels NERC (Nigeria, par DisCo), statistiques EPRA (Kenya), Energy Commission et SIGA (Ghana, états financiers audités abrégés d’ECG et de VRA), ARSE (Burkina), ARSEL (Cameroun), CRSE (Sénégal), ARE (RDC), ERB (Zambie), documents Banque mondiale (PAD/ISR).')
w('4. **KPI du noyau à reclasser** (voir le tableau ci-dessous) :')
w('   - `NET_saidi_hours` : **0 calculable sur 19**, 10 « valeur publiée seule », avec des définitions incompatibles (heures annuelles ou mensuelles, avec ou sans délestage, TMC ou SAIDI). À garder en **valeur publiée avec drapeau de définition**, sans classement inter-utilities au MVP.')
w('   - `GOV_audited_fs_publication_lag_months` : 1 seul calculable, car la date de mise en ligne est rarement déterminable et les re-téléversements faussent les dates de fichier. Utiliser la **date de signature du rapport d’audit** comme mesure principale.')
w('   - `FIN_government_transfer_dependency` : 2 calculables, 12 partiels. Le traitement comptable des transferts varie trop (voir conclusion 5).')
w('   - `NET_distribution_losses_pct` : surtout des valeurs publiées seules (6), rarement le bilan énergétique complet.')
w('   - Les KPI financiers « durs » sont les plus disponibles : capex / amortissements (11 calculables), marge d’EBITDA (10), recouvrement des coûts (9), liquidité (8), délai des créances (7).')
w('5. **Les compensations tarifaires sont comptabilisées de quatre façons** : dans le chiffre d’affaires (Senelec, « Écart sur RMA »), en subventions d’exploitation (ENEO), en autres produits (EKEDC, subvention FGN), ou en paiements directs de l’État aux producteurs (ECG, interrompus en FY2025). '
  'La règle d’extraction de `tariff_compensation_revenue_lcu_m` doit donc être documentée par utility. Sinon, l’EBITDA et le recouvrement des coûts ne sont pas comparables.')
w('6. **Les périmètres bougent pendant la fenêtre MVP** : concession CIE (2021, la CIE ne comptabilise plus que sa rémunération) ; création de NISO au Nigeria (2024) ; filiale NTCSA d’Eskom (2025) ; filiales DisCo sous régulation de l’État de Lagos (2025) ; nationalisation d’ENEO (2026, selon la presse, décret non consulté) ; affermage E2C suspendu. '
  'Le modèle de données doit **dater le périmètre de chaque entité** (`entity_scope` par exercice).')
w('7. **Extraction technique** : de nombreux PDF sont scannés (rapports ENEO 2020-2024, comptes EKEDC 2020-2023, états financiers ZESCO 2023 et 2025, pages d’audit kenyanes). Il faut de l’**OCR**, comme pour les rapports UMOA-Titres de Cartouche. '
  'Plusieurs sites bloquent les robots (ECG, E2C, SONABEL, Ikeja Electric). ANARE-CI exige une connexion SharePoint.')
w('8. **La publication s’accélère** chez plusieurs utilities : Eskom FY2026 publié en août 2026, ZESCO FY2025 en mars 2026, GRIDCo FY2025 signé six mois après la clôture. L’exercice 2025, voire 2026, est donc déjà exploitable pour une partie de l’échantillon.\n')

w('## Synthèse par utility\n')
w('Légende des exercices 2019 → 2025. Rapport annuel : ● ouvert, ◐ lien vu mais non ouvert, ○ cité ailleurs seulement, · non trouvé, ? non vérifié. '
  'États financiers audités : ● complets avec notes, ◐ résumé ou extrait, u non audités, · non trouvé.\n')
w('| Utility | Pays | Périmètre | Cadre | Rapport annuel | États fin. audités | KPI calculables / partiels / non applicables | Viabilité |')
w('|---|---|---|---|---|---|---|---|')
for u in utils:
    c = Counter(k['status'] for k in u['kpi_coverage'])
    ar = ''.join(AR[y['annual_report']] for y in u['years'])
    fs = ''.join(FS[y['audited_fs']] for y in u['years'])
    fw = u['reporting_currency_and_framework'].split(';')[0].split('(')[0].strip()[:28]
    w(f"| {u['name']} | {u['country']} | {SCOPE.get(u['entity_scope'], u['entity_scope'])} | {fw} | `{ar}` | `{fs}` | {c['computable']} / {c['partially_computable']} / {c['not_applicable']} | **{VIA[u['mvp_viability']]}** |")
w('')

w('## Couverture par KPI du noyau (19 utilities)\n')
w('| KPI | ' + ' | '.join(STFR[s] for s in ST) + ' |')
w('|---|' + '---|' * len(ST))
for k in kpi_order:
    w(f"| `{k}` | " + ' | '.join(str(agg[k][s]) for s in ST) + ' |')
w('\n« Absent des docs lus » ne signifie pas que la donnée n’existe pas : seuls 1 ou 2 documents par utility ont été lus en profondeur.\n')

w('## Recommandation d’échantillon MVP\n')
w('Le périmètre doit rester un filtre strict pour les comparaisons. Les groupes proposés :\n')
w('- **Intégrées** : Senelec (fort), Eskom (fort), ZESCO (utilisable), ENEO/SOCADEL (utilisable). SONABEL (via ARSE) et SNEL (via ARE et la Banque mondiale) peuvent être affichées en mode « valeurs publiées », sans score financier.')
w('- **Distribution** : Kenya Power (fort), EKEDC (fort, avec les données opérationnelles NERC), Ikeja Electric (utilisable via NERC ; comptes audités introuvables), ECG (utilisable via SIGA, l’Energy Commission et le PURC). Pour la Côte d’Ivoire, le **secteur CIE + CI-ENERGIES** doit être traité comme une seule unité d’analyse.')
w('- **Transport** : GRIDCo (fort), KETRACO (utilisable), SONATREL (faible, comptes FY2025 seulement), TCN (faible, comptes jusqu’en FY2020).')
w('- **Production** : KenGen (fort), VRA (faible, via SIGA seulement).')
w('- **Hors MVP pour l’instant** : E2C (Congo). Aucune donnée primaire n’existe en ligne. Elle pourrait figurer sur une page « transparence » avec un score de divulgation proche de zéro, mais il faut d’abord décider si c’est souhaitable (risque politique).\n')
w('**Conséquence** : un groupe de pairs ne dépasse pas 4 à 6 utilities. Le score « ajusté aux pairs » ne sera statistiquement fragile qu’au MVP (comparaison descriptive plutôt que régression). Pour l’étoffer, il faut ajouter des utilities du même type : DisCos nigérianes via NERC, NEDCo (Ghana), ou d’autres utilities d’Afrique australe et de l’Est.\n')

w('## Régulateurs et sources secondaires\n')
w('| Pays | Organisme | Ce qui est publié (selon l’agent) | Consulté |')
w('|---|---|---|---|')
for a in audits:
    for r in a['regulators']:
        w(f"| {r['country']} | {r['name']} | {r['publishes'].replace('|', '/')} | {'oui' if r['url_fetched'] else 'non'} |")
w('')

w('## Contre-vérification indépendante\n')
w(f"{d['claims_total']} documents déclarés « ouverts » ont été échantillonnés, et 30 ont été rouverts par un agent indépendant : "
  f"**{spot_c['confirmed']} confirmés, {spot_c['partially_confirmed']} partiellement confirmés, {spot_c.get('contradicted', 0)} contredits, {spot_c.get('unreachable', 0)} inaccessibles**. "
  'Les écarts concernaient des opinions d’audit mal lues : KETRACO 2022/23 est en réalité **qualifiée**, EKEDC 2023 est non modifiée, et SONATREL 2025 n’a qu’un rapport sur projet d’états financiers. '
  'Ils ont été corrigés dans les données. Les deux documents Eskom FY2024 et FY2025 n’ont pas été rouverts.\n')
w('**Limite connue** : le contrôle de sécurité automatique n’a pas pu relire le travail de l’agent Kenya (délai dépassé). Ses affirmations sur KPLC et KETRACO ont été partiellement recoupées par la contre-vérification, mais pas celles sur KenGen FY2026.\n')

w('## Faits inattendus signalés par les agents\n')
w('Ce sont des affirmations des agents, sourcées dans `audit_matrix.json`. Elles n’ont pas toutes été recoupées : à vérifier avant toute publication.\n')
for a in audits:
    for s in a['surprises']:
        w(f'- **{a["cluster"]}** : {s}')
w('')

w('## Détail par utility\n')
for u in utils:
    w(f"### {u['name']} ({u['country']})\n")
    w(f"- **Nom légal confirmé** : {u['legal_name_confirmed']}")
    w(f"- **Actionnariat** : {u['ownership']}")
    w(f"- **Cadre comptable** : {u['reporting_currency_and_framework']} · clôture : {u['fiscal_year_end']}")
    w(f"- **Site** : {u['website']} ({u['website_status']})")
    w(f"- **Évaluation** : {u['overall_assessment']}")
    if u['access_issues']:
        w(f"- **Accès** : {u['access_issues']}")
    w('\n| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |')
    w('|---|---|---|---|---|---|')
    for y in u['years']:
        url = f"<{y['best_url']}>" if y['best_url'] else ''
        w(f"| {y['fiscal_year']} | {y['annual_report']} | {y['audited_fs']} | {y['audit_opinion']} | {y['publication_date'].replace('|', '/')} | {url} |")
    w('\n<details><summary>Couverture des KPI (preuves)</summary>\n')
    for k in u['kpi_coverage']:
        w(f"- `{k['kpi_id']}` : **{STFR.get(k['status'], k['status'])}**. {k['evidence']}")
    w('\n</details>\n')

open(os.path.join(OUT, 'AUDIT_STEP1_DOCUMENTS.md'), 'w').write('\n'.join(L))
json.dump({'as_of': '2026-10-05', 'audits': audits, 'spot_check': spot, 'kpi_coverage_counts': {k: dict(v) for k, v in agg.items()}},
          open(os.path.join(OUT, 'audit_matrix.json'), 'w'), ensure_ascii=False, indent=1)
print(len(utils), dict(via), dict(spot_c))
