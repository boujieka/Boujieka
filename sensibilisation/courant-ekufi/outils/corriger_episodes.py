"""Corrige les épisodes 4 et 5 de « Courant Ekufi ! » avec les chiffres du Pacte national énergétique."""
import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '.')
from retouche import *  # noqa: F401,F403

# ---------------- ÉPISODE 4 : LE SEAU PERCÉ ----------------
ep4 = Image.open(D + '/../originaux/episode-04-original.png').convert('RGB')
O = 650
# Case 9 : 45 % (et non « environ 46 % ») ; on n'ajoute pas de chiffre calculé pour la part qui arrive
patch(ep4, (146, O + 132, 232, O + 226), [('45 %', 'bold', 32, WHITE), ('de pertes', 'bold', 14, WHITE), ('en 2022', 'bold', 13, WHITE)], at=(150, O + 200), radius=14)
patch(ep4, (240, O + 132, 340, O + 226), [('Le reste', 'bold', 19, WHITE), ('arrive aux', 'bold', 15, WHITE), ('usagers', 'bold', 15, WHITE)], at=(335, O + 200), radius=14)
patch(ep4, (24, O + 241, 346, O + 270), [('Source : Pacte national énergétique du Congo (PNE),', 'reg', 10, BLACK), ('pages imprimées 15 et 18.', 'reg', 10, BLACK)], fill=WHITE, align='left')
# Case 11 : ce que le Pacte prévoit vraiment
for (y0, y1, a, b) in [(144, 176, 'Pertes : – 3 % par an', '(p. 23).'), (178, 208, 'Moderniser transport', 'et distribution (p. 4).'),
                       (209, 233, 'Compteurs pour tous', ''), (234, 266, 'Régulariser les branche-', 'ments clandestins (p. 7).')]:
    patch(ep4, (950, O + y0, 1094, O + y1), [(a, 'reg', 13, BLACK)] + ([(b, 'reg', 13, BLACK)] if b else [('(p. 11).', 'reg', 13, BLACK)]) if b else [(a + ' (p. 11).', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=1, gap=0)
# « Le Pacte dit quoi ? »
patch(ep4, (118, O + 318, 268, O + 408), [('45 %', 'bold', 32, RED), ('de pertes en 2022,', 'bold', 13, NAVY), ('deux fois la moyenne', 'bold', 12, NAVY), ('africaine (22 %).', 'bold', 12, NAVY)], fill=WHITE)
patch(ep4, (393, O + 316, 660, O + 400), [('Objectif du Pacte :', 'bold', 16, NAVY), ('réduire les pertes de 3 % par an', 'bold', 14, NAVY), ('et encaisser 95 % des factures', 'bold', 14, NAVY), ('en 3 ans (73 % aujourd\'hui).', 'bold', 14, NAVY)], fill=WHITE, align='left')
patch(ep4, (12, O + 411, 640, O + 431), [('Source : Pacte national énergétique du Congo (PNE), pages imprimées 4, 7, 11, 15, 18 et 23.', 'reg', 11, BLACK)], fill=WHITE, align='left')
# « À retenir », 1re puce : un chiffre du Pacte au lieu d'une affirmation qu'il ne fait pas
patch(ep4, (700, O + 313, 1080, O + 333), [('45 % de l\'électricité perdue en 2022 (PNE p. 15).', 'reg', 15, BLACK)], at=(1060, O + 330), align='left', pad=2)
ep4.save(D + '/../episode-04-le-seau-perce-corrige.png')

# ---------------- ÉPISODE 5 : LES MILLIARDS INVISIBLES ----------------
ep5 = Image.open(D + '/../originaux/episode-05-original.png').convert('RGB')
T, M, B = 100, 440, 790
# Case 2 : le Pacte dit « d'ici 2030 », pas « sur cinq ans (2025-2030) »
patch(ep5, (612, T + 100, 838, T + 120), [('d\'ici 2030,', 'comic', 15, BLACK)], fill=WHITE)
patch(ep5, (640, T + 86, 832, T + 101), [('de 11,543 milliards USD', 'comic', 15, RED)], fill=WHITE, pad=1)
patch(ep5, (700, T + 188, 800, T + 205), [('D\'ICI 2030', 'cond', 15, NAVY)], at=(704, T + 202))
patch(ep5, (697, T + 268, 806, T + 302), [('2,31', 'bold', 26, RED)], at=(800, T + 296))
# Case 3 : on retire le chiffre calculé (1,653) et les « ≈ »
patch(ep5, (1050, T + 203, 1232, T + 252), [('Tableau 2 :', 'bold', 14, NAVY), ('sources privées', 'bold', 14, NAVY)], at=(1046, T + 250))
patch(ep5, (1288, T + 203, 1428, T + 252), [('655,2', 'bold', 22, GREEN), ('millions USD par an', 'bold', 11, GREEN)], at=(1290, T + 250))
patch(ep5, (1036, T + 266, 1430, T + 314), [('Total : 11,543 milliards USD d\'ici 2030', 'bold', 18, WHITE), ('soit 2,31 milliards USD par an', 'bold', 16, WHITE)], at=(1040, T + 270))
patch(ep5, (1095, T + 120, 1232, T + 196), [('8,267', 'bold', 26, NAVY), ('milliards USD', 'bold', 15, NAVY), ('d\'ici 2030', 'bold', 13, NAVY)], at=(1225, T + 125))
patch(ep5, (1325, T + 120, 1428, T + 196), [('3,276', 'bold', 22, GREEN), ('milliards USD', 'bold', 13, GREEN), ('d\'ici 2030', 'bold', 12, GREEN)], at=(1424, T + 125))
# Case 4 : 606 MILLIONS (et non milliards) ; pas de montants annuels calculés
for (x0, x1, big, unit, col) in [(22, 158, '7,691', 'milliards USD', NAVY), (162, 297, '986', 'millions USD', GREEN),
                                 (302, 437, '1,282', 'milliard USD', (225, 120, 20)), (442, 578, '606', 'millions USD', RED)]:
    patch(ep5, (x0, M + 174, x1, M + 268), [(big, 'bold', 24, col), (unit, 'bold', 14, col), ('d\'ici 2030', 'reg', 13, col)], at=(x0 + 6, M + 262))
patch(ep5, (160, M + 326, 584, M + 344), [('Source : Pacte national énergétique du Congo (PNE), tableau 2, p. 8.', 'reg', 11, BLACK)], fill=WHITE)
# Case 5 : remplace les quatre chiffres absents du Pacte par des objectifs du tableau 1
patch(ep5, (600, M + 128, 985, M + 330), [
    ('953 000 branchements supplémentaires', 'bold', 16, RED), ('874 000 en ville, 79 000 à la campagne (p. 4, 7)', 'reg', 13, BLACK), ('', 'reg', 6, BLACK),
    ('90 % en ville, 50 % à la campagne', 'bold', 16, RED), ('taux d\'accès visés en 2030 (p. 7)', 'reg', 13, BLACK), ('', 'reg', 6, BLACK),
    ('81,3 % de cuisson propre en 2030', 'bold', 16, RED), ('contre 39,6 % en 2023 (p. 7)', 'reg', 13, BLACK), ('', 'reg', 6, BLACK),
    ('45 % de pertes : – 3 % par an', 'bold', 16, RED), ('objectif de réduction (p. 15, 23)', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=10)
patch(ep5, (600, M + 330, 985, M + 346), [('Source : PNE, tableau 1, p. 7 ; p. 4, 15 et 23.', 'reg', 11, BLACK)], fill=WHITE)
# Case 6 : bulles sans chiffre calculé
patch(ep5, (1018, M + 42, 1214, M + 117), [('Le secteur privé doit apporter', 'comic', 14, BLACK), ('8,267 milliards USD', 'comic', 15, RED), ('d\'ici 2030 (71,6 % du total).', 'comic', 14, BLACK)], fill=WHITE, radius=12)
patch(ep5, (1224, M + 44, 1428, M + 128), radius=12, lines=[('Le secteur public devrait', 'comic', 13, BLACK), ('investir', 'comic', 13, BLACK), ('3,276 milliards USD', 'comic', 13, RED), ('d\'ici 2030, soit', 'comic', 13, BLACK), ('655,2 millions USD par an.', 'comic', 13, RED)], fill=WHITE)
# Case 8 : « 18,7 % » n'est pas un chiffre du Pacte
patch(ep5, (478, B + 38, 654, B + 120), radius=12, lines=[('S\'il n\'y a pas assez', 'comic', 13, BLACK), ('d\'investissements, beaucoup', 'comic', 13, BLACK), ('de ménages risquent de', 'comic', 13, BLACK), ('rester sans accès en 2030…', 'comic', 13, BLACK)], fill=WHITE)
# Case 9 : les vraies échéances du tableau 3
patch(ep5, (672, B + 122, 768, B + 240), [('Déc. 2025 :', 'bold', 12, BLACK), ('Stratégie', 'reg', 12, BLACK), ('d\'électrification', 'reg', 12, BLACK), ('(SEN), tarif', 'reg', 12, BLACK), ('social.', 'reg', 12, BLACK)], fill=WHITE)
patch(ep5, (772, B + 122, 882, B + 240), [('Déc. 2026 :', 'bold', 12, BLACK), ('PDEMC, cuisson', 'reg', 12, BLACK), ('propre, nouvelle', 'reg', 12, BLACK), ('grille tarifaire.', 'reg', 12, BLACK), ('Juin 2027 :', 'bold', 12, BLACK), ('comptes audités.', 'reg', 12, BLACK)], fill=WHITE)
patch(ep5, (886, B + 122, 990, B + 240), [('Juin 2028 :', 'bold', 12, BLACK), ('contrôle qualité', 'reg', 12, BLACK), ('des importations.', 'reg', 12, BLACK), ('Déc. 2028 : 1re', 'bold', 12, BLACK), ('mise à jour', 'reg', 12, BLACK), ('du PDEMC.', 'reg', 12, BLACK)], fill=WHITE)
patch(ep5, (672, B + 250, 1105, B + 268), [('Source : PNE, tableau 3, p. 9-11 ; tableau 1, p. 7.', 'reg', 11, BLACK)], fill=WHITE)
# Case 10 : « jusqu'en 2030 » plutôt que « pendant cinq ans »
patch(ep5, (1272, B + 26, 1436, B + 44), [('chaque année jusqu\'en 2030 !', 'comic', 15, BLACK)], fill=WHITE, pad=1)
ep5.save(D + '/../episode-05-les-milliards-invisibles-corrige.png')
print('ok')
