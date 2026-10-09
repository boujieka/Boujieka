"""Corrige les épisodes 1, 2 et 3 de « Courant Ekufi ! » avec les chiffres du Pacte national énergétique."""
import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '.')
from retouche import *  # noqa: F401,F403

YELLOW_TXT = (190, 20, 30)

# ---------------- ÉPISODE 1 : ENCORE UNE COUPURE ! ----------------
ep1 = Image.open(D + '/../originaux/episode-01-original.png').convert('RGB')
# Encadré final : « 18,7 % restants » est un calcul (100 – 81,3), pas un chiffre du Pacte
patch(ep1, (1486, 905, 1666, 930), [('Qui sera dans les 81,3 % ?', 'bold', 13, NAVY)], at=(1660, 925), pad=2)
# Encadré « Le Pacte dit quoi ? » : on nomme l'autre indicateur cité par le Pacte
patch(ep1, (1370, 770, 1660, 861), [
    ('Les 31,66 % comptent les ménages clients', 'reg', 13, BLACK),
    ('réguliers d\'E2C (p. 7). Le suivi international', 'reg', 13, BLACK),
    ('ODD 7, cité par le Pacte, donne 47,5 % (p. 14).', 'reg', 13, BLACK),
    ('Source : Pacte national énergétique du Congo', 'reg', 12, BLACK), ('(PNE), pages imprimées 4, 7 et 14.', 'reg', 12, BLACK)], fill=WHITE, align='left', pad=2, gap=2)
ep1.save(D + '/../episode-01-encore-une-coupure-corrige.png')

# ---------------- ÉPISODE 2 : LA PROMESSE DE 2030 ----------------
ep2 = Image.open(D + '/../originaux/episode-02-original.png').convert('RGB')
Y = 380
# Case 6 : titre et bulle sans le calcul « 18,7 % »
patch(ep2, (438, 388, 638, 410), [('Qui restera sans courant ?', 'bold', 16, BLACK)], at=(436, 393), pad=1)
patch(ep2, (436, 427, 598, 501), radius=14, lines=[
    ('Soki ezali 81,3 %…', 'bold', 15, BLACK), ('nani akotikala ?', 'bold', 15, BLACK),
    ('Si c\'est 81,3 %…', 'reg', 12, BLACK), ('qui restera sans courant ?', 'reg', 12, BLACK)], fill=WHITE, pad=2, gap=1)
# Case 10 : carnet de Fifi
patch(ep2, (492, 806, 662, 842), [('1. Qui restera hors', 'bold', 15, NAVY), ('des 81,3 % ?', 'bold', 15, NAVY)], at=(666, 832), align='left', pad=2, gap=1)
# « Le Pacte dit quoi ? » : remplace « 18,7 % reste à électrifier » par les cibles ville / campagne du tableau 1
patch(ep2, (508, 968, 710, 1054), [
    ('90 % / 50 %', 'bold', 26, RED), ('Objectifs 2030 en ville /', 'reg', 13, BLACK),
    ('à la campagne (38,67 % /', 'reg', 13, BLACK), ('1,01 % aujourd\'hui), p. 7', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=4, gap=1)
ep2.save(D + '/../episode-02-la-promesse-de-2030-corrige.png')

# ---------------- ÉPISODE 3 : LE VILLAGE DE MBUTA ----------------
ep3 = Image.open(D + '/../originaux/episode-03-original.png').convert('RGB')
Z = 690
# Case 10 : ce que le Pacte dit vraiment pour les zones rurales (p. 7)
patch(ep3, (502, 727, 698, 812), [
    ('Pour les nouveaux accès ruraux,', 'reg', 13, BLACK), ('le Pacte suppose :', 'reg', 13, BLACK),
    ('• 90 % de systèmes solaires autonomes ;', 'reg', 13, BLACK), ('• 10 % de mini-réseaux ;', 'reg', 13, BLACK),
    ('à confirmer par la SEN (p. 7).', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=4, gap=1)
patch(ep3, (540, 817, 692, 919), [
    ('Mokano : 50 % na', 'bold', 15, BLACK), ('mboka na 2030 !', 'bold', 15, BLACK),
    ('Objectif : 50 % des ménages', 'reg', 12, BLACK), ('ruraux raccordés en 2030', 'reg', 12, BLACK), ('(1,01 % aujourd\'hui, p. 7).', 'reg', 12, BLACK)],
    at=(548, 909), pad=3, gap=1)
# « Le Pacte dit quoi ? »
patch(ep3, (18, 1006, 172, 1058), [('Hypothèse rurale', 'bold', 13, BLACK), ('Kits solaires 90 %,', 'reg', 13, BLACK), ('mini-réseaux 10 % (p. 7)', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=2, gap=1)
patch(ep3, (216, 994, 314, 1010), [('Objectif rural', 'bold', 13, BLACK)], fill=WHITE, align='left', pad=1)
patch(ep3, (180, 1011, 314, 1058), [('50 % des ménages', 'reg', 13, BLACK), ('en 2030 (1,01 %', 'reg', 13, BLACK), ('aujourd\'hui), p. 7', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=2, gap=1)
patch(ep3, (362, 994, 526, 1010), [('Localités prioritaires', 'bold', 13, BLACK)], fill=WHITE, align='left', pad=1)
patch(ep3, (322, 1011, 526, 1058), [('Celles de plus de', 'reg', 13, BLACK), ('1 000 habitants (p. 4)', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=2, gap=1)
patch(ep3, (582, 984, 722, 1003), [('Branchements ruraux', 'bold', 13, BLACK)], fill=WHITE, align='left', pad=1)
patch(ep3, (582, 1004, 722, 1050), [('79 000 d\'ici 2030', 'reg', 13, BLACK), ('(p. 4 et 7)', 'reg', 13, BLACK)], fill=WHITE, align='left', pad=2, gap=1)
patch(ep3, (14, 1063, 505, 1082), [('Source : Pacte national énergétique du Congo (PNE), pages imprimées 4 et 7.', 'reg', 11, BLACK)], fill=WHITE, align='left', pad=2)
# « À retenir »
patch(ep3, (754, 978, 1110, 993), [('•  Le Pacte suppose surtout des kits solaires (90 %) et des mini-réseaux (10 %).', 'reg', 13, BLACK)], at=(1104, 985), align='left', pad=1)
patch(ep3, (754, 1035, 1110, 1062), [('•  Objectif rural 2030 : 50 % des ménages (1,01 % aujourd\'hui),', 'reg', 13, BLACK), ('    79 000 branchements (PNE p. 4 et 7).', 'reg', 13, BLACK)], at=(1104, 1040), align='left', pad=1, gap=0)
ep3.save(D + '/../episode-03-le-village-de-mbuta-corrige.png')
print('ok')
