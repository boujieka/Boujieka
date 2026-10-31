import html, re
E=lambda s: html.escape(s, quote=True)

SYMBOLS = '''
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
 <defs>
  <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#1b1712" opacity=".10"/></pattern>
  <symbol id="pepite" viewBox="0 0 120 100">
   <path d="M18 62 L10 40 L30 18 L58 10 L90 16 L110 40 L104 70 L80 90 L40 92 Z" fill="#f2b632" stroke="#1b1712" stroke-width="4" stroke-linejoin="round"/>
   <path d="M30 30 L50 22 M78 26 L94 40" stroke="#fff3c4" stroke-width="5" stroke-linecap="round"/>
   <circle cx="46" cy="50" r="9" fill="#fff"/><circle cx="78" cy="50" r="9" fill="#fff"/>
   <circle cx="48" cy="52" r="4.5" fill="#1b1712"/><circle cx="80" cy="52" r="4.5" fill="#1b1712"/>
   <path d="M48 70 Q62 82 78 70" fill="none" stroke="#1b1712" stroke-width="4" stroke-linecap="round"/>
  </symbol>
  <symbol id="abena" viewBox="0 0 100 170">
   <circle cx="34" cy="22" r="13" fill="#2a1a12"/><circle cx="66" cy="22" r="13" fill="#2a1a12"/>
   <circle cx="50" cy="42" r="24" fill="#7a4a2b" stroke="#1b1712" stroke-width="3"/>
   <circle cx="42" cy="42" r="3.5" fill="#1b1712"/><circle cx="58" cy="42" r="3.5" fill="#1b1712"/>
   <path d="M42 53 Q50 59 58 53" fill="none" stroke="#1b1712" stroke-width="3" stroke-linecap="round"/>
   <path d="M50 66 L18 150 L82 150 Z" fill="#1f7a4d" stroke="#1b1712" stroke-width="3" stroke-linejoin="round"/>
   <path d="M30 120 L70 120" stroke="#f2b632" stroke-width="5"/>
   <path d="M36 150 L36 166 M64 150 L64 166" stroke="#1b1712" stroke-width="5" stroke-linecap="round"/>
  </symbol>
  <symbol id="moussa" viewBox="0 0 100 170">
   <path d="M28 34 Q50 8 72 34" fill="#1b1712"/>
   <circle cx="50" cy="42" r="24" fill="#5b3620" stroke="#1b1712" stroke-width="3"/>
   <circle cx="42" cy="42" r="3.5" fill="#1b1712"/><circle cx="58" cy="42" r="3.5" fill="#1b1712"/>
   <path d="M42 54 Q50 58 58 54" fill="none" stroke="#1b1712" stroke-width="3" stroke-linecap="round"/>
   <rect x="24" y="68" width="52" height="58" rx="8" fill="#c8402d" stroke="#1b1712" stroke-width="3"/>
   <rect x="28" y="124" width="44" height="26" fill="#2d3e63" stroke="#1b1712" stroke-width="3"/>
   <path d="M38 150 L38 166 M62 150 L62 166" stroke="#1b1712" stroke-width="6" stroke-linecap="round"/>
  </symbol>
  <symbol id="mama" viewBox="0 0 110 170">
   <path d="M20 30 Q55 -4 90 30 L84 40 L26 40 Z" fill="#f2b632" stroke="#1b1712" stroke-width="3"/>
   <path d="M86 26 L104 18 L98 36 Z" fill="#c8402d" stroke="#1b1712" stroke-width="3"/>
   <circle cx="55" cy="50" r="24" fill="#6a3f25" stroke="#1b1712" stroke-width="3"/>
   <path d="M44 48 L50 48 M60 48 L66 48" stroke="#1b1712" stroke-width="3" stroke-linecap="round"/>
   <path d="M46 61 Q55 66 64 61" fill="none" stroke="#1b1712" stroke-width="3" stroke-linecap="round"/>
   <path d="M55 74 Q14 92 18 160 L92 160 Q96 92 55 74 Z" fill="#7b3f8c" stroke="#1b1712" stroke-width="3"/>
   <path d="M24 118 Q55 104 86 118" fill="none" stroke="#f2b632" stroke-width="4"/>
  </symbol>
  <symbol id="miroir" viewBox="0 0 110 170">
   <ellipse cx="55" cy="68" rx="44" ry="60" fill="#cfe8ef" stroke="#8a5a1d" stroke-width="9"/>
   <path d="M30 40 Q40 30 50 34" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
   <circle cx="42" cy="66" r="5" fill="#1b1712"/><circle cx="68" cy="66" r="5" fill="#1b1712"/>
   <path d="M38 52 L48 56 M72 52 L62 56" stroke="#1b1712" stroke-width="3" stroke-linecap="round"/>
   <path d="M42 90 Q55 98 68 90" fill="none" stroke="#1b1712" stroke-width="4" stroke-linecap="round"/>
   <path d="M55 128 L55 156 M34 160 L76 160" stroke="#8a5a1d" stroke-width="8" stroke-linecap="round"/>
  </symbol>
  <symbol id="avion" viewBox="0 0 160 70">
   <path d="M10 38 Q20 26 120 28 Q150 30 152 38 Q150 46 120 48 Q20 50 10 38 Z" fill="#fff" stroke="#1b1712" stroke-width="3"/>
   <path d="M70 30 L50 4 L66 4 L96 30 Z M70 46 L50 66 L66 66 L96 46 Z M20 34 L10 14 L22 14 L34 32 Z" fill="#c8402d" stroke="#1b1712" stroke-width="3" stroke-linejoin="round"/>
   <circle cx="104" cy="36" r="3" fill="#2d3e63"/><circle cx="116" cy="36" r="3" fill="#2d3e63"/><circle cx="128" cy="36" r="3" fill="#2d3e63"/>
  </symbol>
  <symbol id="balance" viewBox="0 0 200 120">
   <path d="M100 12 L100 108 M70 112 L130 112" stroke="#1b1712" stroke-width="6" stroke-linecap="round"/>
   <path d="M30 40 L170 18" stroke="#1b1712" stroke-width="6" stroke-linecap="round"/>
   <path d="M30 40 L14 74 L46 74 Z" fill="none" stroke="#1b1712" stroke-width="3"/><path d="M8 74 Q30 90 52 74 Z" fill="#cfe8ef" stroke="#1b1712" stroke-width="3"/>
   <path d="M170 18 L154 52 L186 52 Z" fill="none" stroke="#1b1712" stroke-width="3"/><path d="M148 52 Q170 68 192 52 Z" fill="#f2b632" stroke="#1b1712" stroke-width="3"/>
  </symbol>
  <symbol id="valise" viewBox="0 0 80 60">
   <rect x="6" y="14" width="68" height="42" rx="6" fill="#8a5a1d" stroke="#1b1712" stroke-width="3"/>
   <path d="M28 14 L28 6 L52 6 L52 14" fill="none" stroke="#1b1712" stroke-width="4"/>
   <text x="40" y="42" text-anchor="middle" font-size="14" font-family="sans-serif" font-weight="700" fill="#f2b632">DXB</text>
  </symbol>
  <symbol id="cartons" viewBox="0 0 120 80">
   <rect x="4" y="30" width="50" height="46" fill="#d9a066" stroke="#1b1712" stroke-width="3"/><rect x="58" y="12" width="56" height="64" fill="#e6b47a" stroke="#1b1712" stroke-width="3"/>
   <text x="86" y="50" text-anchor="middle" font-size="13" font-family="sans-serif" font-weight="700" fill="#1b1712">?? kg</text>
  </symbol>
 </defs>
</svg>'''

# scene backgrounds
BG = {
 'village': '<rect width="400" height="240" fill="#bfe3f0"/><circle cx="340" cy="44" r="24" fill="#f7d35c"/><path d="M0 170 Q100 120 200 160 T400 150 L400 240 L0 240Z" fill="#3f8f4f"/><rect y="200" width="400" height="40" fill="#b5532f"/><path d="M40 168 L70 140 L100 168 Z" fill="#8a5a1d"/><rect x="48" y="166" width="44" height="30" fill="#e8c78f" stroke="#1b1712" stroke-width="2"/>',
 'ville': '<rect width="400" height="240" fill="#f6e7c8"/><rect x="20" y="70" width="50" height="130" fill="#d9cdb5" stroke="#1b1712" stroke-width="2"/><rect x="80" y="40" width="60" height="160" fill="#e8dcc4" stroke="#1b1712" stroke-width="2"/><rect x="300" y="80" width="70" height="120" fill="#d9cdb5" stroke="#1b1712" stroke-width="2"/><rect y="200" width="400" height="40" fill="#8f8a80"/><path d="M0 220 L400 220" stroke="#fff" stroke-width="3" stroke-dasharray="18 14"/>',
 'sol': '<rect width="400" height="240" fill="#bfe3f0"/><rect y="70" width="400" height="170" fill="#b5532f"/><rect y="70" width="400" height="12" fill="#3f8f4f"/><path d="M0 140 Q120 120 200 150 T400 140" stroke="#8c3b20" stroke-width="3" fill="none"/>',
 'ciel': '<rect width="400" height="240" fill="#9fd4ea"/><path d="M40 70 q20 -20 40 0 q20 -14 36 4 q-38 10 -76 -4z" fill="#fff"/><path d="M280 120 q20 -20 40 0 q20 -14 36 4 q-38 10 -76 -4z" fill="#fff"/><rect y="210" width="400" height="30" fill="#e8d7a8"/>',
 'bureau': '<rect width="400" height="240" fill="#eef2e6"/><rect y="190" width="400" height="50" fill="#a07a50"/><rect x="250" y="40" width="120" height="80" fill="#fff" stroke="#1b1712" stroke-width="2"/><path d="M262 104 L290 80 L310 92 L350 56" stroke="#c8402d" stroke-width="4" fill="none"/>',
 'nuit': '<rect width="400" height="240" fill="#1d2a44"/><circle cx="330" cy="50" r="20" fill="#f4ecd0"/><circle cx="60" cy="40" r="2" fill="#fff"/><circle cx="140" cy="70" r="2" fill="#fff"/><circle cx="220" cy="30" r="2" fill="#fff"/><path d="M0 190 Q100 160 200 185 T400 180 L400 240 L0 240Z" fill="#2c3b2a"/>',
 'brouillard': '<rect width="400" height="240" fill="#d7dbe0"/><path d="M0 80 Q100 60 200 90 T400 80" stroke="#fff" stroke-width="18" fill="none" opacity=".8"/><path d="M0 150 Q100 130 200 160 T400 150" stroke="#fff" stroke-width="22" fill="none" opacity=".8"/><rect y="205" width="400" height="35" fill="#b9b3a5"/>',
 'aube': '<rect width="400" height="240" fill="#f9d9a0"/><circle cx="200" cy="200" r="70" fill="#f7b84a"/><path d="M0 200 L400 200 L400 240 L0 240Z" fill="#3f8f4f"/><path d="M0 214 L400 214" stroke="#c8402d" stroke-width="6"/><path d="M0 222 L400 222" stroke="#f2b632" stroke-width="6"/>',
}
def use(sym, x, y, w, h, flip=False):
    t = f' transform="translate({2*x+w} 0) scale(-1 1)"' if flip else ''
    return f'<use href="#{sym}" x="{x}" y="{y}" width="{w}" height="{h}"{t}/>'

def panel(bg, chars, caption, bubbles, wide=False, extra=''):
    lab = re.sub(r'<[^>]+>','', caption or bubbles[0][4]); lab = re.sub(r'\[\d+\]','',lab)
    svg = f'<svg viewBox="0 0 400 240" role="img" aria-label="{E(lab)}">{BG[bg]}{extra}{"".join(chars)}<rect width="400" height="240" fill="url(#dots)"/></svg>'
    b = ''.join(f'<p class="bulle {k}" style="left:{x}%;top:{y}%;max-width:{w}%">{t}</p>' for (k,x,y,w,t) in bubbles)
    cap = f'<p class="recit">{caption}</p>' if caption else ''
    return f'<figure class="case{" large" if wide else ""}">{cap}<div class="scene">{svg}{b}</div></figure>'

def sup(*n): return ''.join(f'<a class="ref" href="#src{i}">[{i}]</a>' for i in n)

PL = []
def planche(num, titre, cases):
    PL.append(f'<section class="planche" id="planche-{num}"><header class="ph"><span class="pn">Planche {num}</span><h2>{titre}</h2></header><div class="grille">{"".join(cases)}</div></section>')

# ---------------- PLANCHE 1
planche(1, "An 2000 : deux naissances", [
 panel('village', [use('mama',150,80,80,124), use('pepite',300,200,60,40)],
  "Bétaré-Oya, région de l’Est, an 2000. Une grand-mère tient un bébé tout neuf.",
  [('',4,6,48,"Elle s’appellera Abena. Elle aura un avenir en or !"), ('pense',62,58,36,"Hé ho… je suis juste là, sous vos pieds !")]),
 panel('ville', [use('moussa',170,96,70,120)],
  "Même année, à Garoua. Moussa pousse son premier cri.",
  [('',4,8,50,"Ouiiiin !"), ('',52,8,44,"(Papa) Mon fils, ce pays est riche !")]),
 panel('sol', [use('pepite',150,110,110,92)],
  "Moi, c’est Pépite. Je dors dans la latérite depuis des millions d’années.",
  [('',4,6,58,"En 2000, aucun pays au monde ne déclare avoir importé d’or « venant du Cameroun »."+sup(1))]),
 panel('nuit', [use('pepite',250,140,70,58), use('valise',180,170,50,38)],
  None,
  [('',4,8,60,"Tranquille, je dors… Mais j’entends déjà des pelles et des valises.")]),
])

# ---------------- PLANCHE 2
planche(2, "2009–2019 : l’or prend l’avion", [
 panel('ciel', [use('avion',90,90,220,96), use('pepite',140,110,50,42)],
  "2009. Abena a 9 ans. Pépite part en voyage.",
  [('',4,6,46,"Destination Dubaï !"), ('note',52,6,46,"Les Émirats arabes unis déclarent 1 364 kg d’or reçus du Cameroun."+sup(1))]),
 panel('ville', [use('moussa',60,96,70,120), use('cartons',230,140,110,74)],
  "2013. Moussa a 13 ans et adore les maths.",
  [('',4,6,46,"Les partenaires déclarent 11 490 kg d’or reçus du Cameroun : 507 M USD, ≈ 251 milliards FCFA."+sup(1,4)),
   ('',52,6,46,"Et le Cameroun déclare… 214 kg. Quatre sacs de ciment !"+sup(1))]),
 panel('village', [use('abena',60,84,74,126), use('pepite',300,175,62,52)],
  "2017. Un rapport d’INTERPOL compare les papiers.",
  [('note',4,4,56,"Cameroun → Émirats : 4 kg déclarés. Émirats ← Cameroun : 10 900 kg."+sup(2)),
   ('',50,46,48,"4 kilos ? C’est le poids de mon sac d’école !")]),
 panel('sol', [use('mama',40,72,80,124), use('pepite',260,150,60,50)],
  "2018. Record de la décennie : 11,7 tonnes déclarées par les Émirats, 415 M USD."+sup(1),
  [('',28,4,34,"Et notre village, il a eu quoi ?"), ('pense',64,4,34,"Bonne question. Garde-la pour la planche 6.")]),
])

# ---------------- PLANCHE 3
planche(3, "Monsieur Miroir explique la méthode", [
 panel('bureau', [use('miroir',40,60,96,150), use('moussa',290,96,70,120)],
  None,
  [('',30,6,52,"Je compare deux papiers : ce que le Cameroun dit avoir envoyé, et ce que les autres pays disent avoir reçu.")]),
 panel('bureau', [use('balance',100,80,200,120)],
  "Sur 2012–2022, même produit, mêmes années."+sup(1),
  [('note',2,8,40,"Le Cameroun déclare : 644 kg."), ('note',58,8,40,"Les partenaires déclarent : 96 275 kg."), ('',30,64,40,"149 fois plus !")]),
 panel('ciel', [use('avion',150,110,200,88), use('moussa',20,96,70,120)],
  "2023, vérifié dans la base WITS de la Banque mondiale."+sup(3),
  [('note',30,6,66,"Émirats : 14 048 kg reçus (879,7 M USD, ≈ 534 milliards FCFA). Cameroun : 20 kg envoyés."),
   ('',4,50,26,"702 fois !")]),
 panel('bureau', [use('miroir',40,60,96,150), use('abena',300,104,74,126)],
  None,
  [('',30,6,58,"Attention : un écart n’est pas une preuve de vol. Il dit que quelqu’un ne déclare pas, ou que de l’or d’ailleurs passe par chez nous."+sup(2))]),
])

# ---------------- PLANCHE 4
planche(4, "Combien ça fait ?", [
 panel('bureau', [use('abena',40,84,74,126)],
  "Abena sort la calculatrice. Période 2000–2025."+sup(1),
  [('',30,6,64,"138,5 tonnes d’or déclarées « venant du Cameroun » par ses partenaires.")]),
 panel('bureau', [use('moussa',300,96,70,120), use('pepite',30,150,60,50)],
  None,
  [('',4,6,64,"Valeur déclarée : 6,58 milliards de dollars, soit environ 3 744 milliards de FCFA."+sup(1,4)),
   ('pense',4,36,30,"Et j’en faisais partie…")]),
 panel('village', [use('mama',40,72,80,124), use('abena',280,84,74,126)],
  "2023 à elle seule : 18,3 tonnes, 1,15 milliard USD, ≈ 695 milliards FCFA."+sup(1),
  [('',26,6,46,"La Sonamines a collecté 10,48 milliards FCFA cette année-là."+sup(5)), ('',58,52,40,"Ça fait… 1,5 % !")]),
 panel('bureau', [use('moussa',40,96,70,120)],
  None,
  [('note',26,6,70,"Selon le gouvernement, 577,5 milliards FCFA de recettes fiscales et douanières n’ont pas été perçus sur 2021–2025."+sup(6)),
   ('',40,62,56,"Et ça, ce sont seulement les impôts, pas l’or lui-même !")]),
])

# ---------------- PLANCHE 5
planche(5, "Les prédateurs, d’ici et d’ailleurs", [
 panel('nuit', [use('cartons',40,130,120,80), use('pepite',250,150,60,50)],
  "D’ici et d’ailleurs : les exploitants sans papiers.",
  [('note',4,6,70,"Mai 2026 : le ministère des Mines identifie près de 200 sociétés artisanales illégales dans l’Est et l’Adamaoua, en majorité à capitaux étrangers."+sup(7))]),
 panel('ville', [use('pepite',300,150,70,58)],
  "D’ici : une règle qui fait fuir.",
  [('note',2,6,46,"Cameroun : environ 28,75 % prélevés sur l’or artisanal exporté."+sup(8)),
   ('note',52,6,46,"Ouganda : ≈ 0,25 %. Rwanda : 0,5 %."+sup(8)),
   ('',4,62,50,"Si le péage est cher d’un côté et presque gratuit de l’autre, devine par où je passe ?")]),
 panel('ciel', [use('avion',30,100,170,74), use('valise',250,150,70,52)],
  "D’ailleurs : les plaques tournantes.",
  [('note',2,6,52,"Émirats : 80 % des volumes recensés. Rwanda : 16 t, Ouganda : 7,7 t (2019–2025)."+sup(1)),
   ('note',56,6,42,"Entre 2012 et 2022, les Émirats ont importé 2 569 t d’or africain non déclaré."+sup(9))]),
 panel('brouillard', [use('abena',60,84,74,126), use('miroir',260,60,96,150)],
  "Le brouillard.",
  [('note',30,4,64,"Les chiffres 2024 des Émirats ont été publiés, puis retirés de la base de l’ONU « pour vérification »."+sup(9)),
   ('',4,40,30,"Même les chiffres jouent à cache-cache !")]),
])

# ---------------- PLANCHE 6
planche(6, "Ce qu’on ne sait pas (encore)", [
 panel('sol', [use('pepite',170,120,70,58)],
  None,
  [('',4,6,70,"L’or « venant du Cameroun » n’est pas forcément sorti de notre sol : il peut arriver de RCA ou du Tchad et transiter par ici."+sup(2))]),
 panel('brouillard', [use('cartons',150,120,120,80)],
  None,
  [('',4,6,70,"On ne sait pas encore qui a fait quoi, cargaison par cargaison. Il faudra des enquêtes douanières.")]),
 panel('bureau', [use('moussa',300,96,70,120), use('miroir',30,60,96,150)],
  None,
  [('note',28,6,46,"Gouvernement : 577,5 milliards. Page du ministère : 557 milliards. ITIE : 165 milliards (2023)."+sup(6,10)),
   ('',26,62,46,"Les chiffres officiels ne collent même pas entre eux !")]),
 panel('village', [use('mama',140,72,80,124), use('pepite',290,150,60,50)],
  None,
  [('',4,6,58,"Moralité : un bon enquêteur dit aussi ce qu’il ne sait pas."),
   ('pense',62,50,36,"Bon, et ma question sur le village ?")]),
])

# ---------------- PLANCHE 7
planche(7, "Génération 2000, à vous de jouer", [
 panel('aube', [use('abena',100,70,74,126), use('moussa',220,80,70,120)],
  "2026. Abena et Moussa ont 26 ans.",
  [('',4,6,52,"Cet or, c’était aussi notre avenir."), ('',56,6,40,"Alors on apprend, et on demande des comptes.")]),
 panel('bureau', [use('moussa',30,96,70,120)],
  "Ce que font des pays producteurs d’or."+sup(8),
  [('note',28,6,68,"Ghana, Mali, Tanzanie : une petite taxe à l’export, un acheteur public pour l’or artisanal, et la traçabilité de chaque lingot.")]),
 panel('ville', [use('abena',30,84,74,126)],
  None,
  [('note',28,4,68,"1. Lire les rapports ITIE du Cameroun. 2. Demander les chiffres de la Sonamines. 3. Exiger la traçabilité de l’or. 4. Partager cette BD.")]),
 panel('aube', [use('mama',40,72,80,124), use('abena',150,84,74,126), use('moussa',240,96,70,120), use('pepite',320,170,56,46)],
  None,
  [('',4,4,56,"Le pays sous nos pieds… il est à nous tous."), ('pense',64,4,34,"Et moi, je préfère rester au pays !")]),
])

SOURCES = [
 (1, "UN Comtrade, code SH 7108 (or), importations déclarées « en provenance du Cameroun » par 254 pays et territoires, 2000–2025, extraction du 31/10/2026. Données : dépôt boujieka/Boujieka, docs/recherche-or-cameroun/donnees_miroir_or_tous_declarants.csv. Les années 2024–2025 sont partielles (pas de données des Émirats).", "https://comtradeplus.un.org/"),
 (2, "INTERPOL, Illegal Gold Mining in Central Africa, 2021 (séries Émirats 2008–2018, écart de 2017, hypothèse du transit d’or étranger).", "https://www.interpol.int/content/download/16493/file/2021%2007%2027%20ENGLISH%20PUBLIC%20VERSION_FINAL_Illegal%20gold%20mining%20in%20Central%20Africa.pdf"),
 (3, "WITS / UN Comtrade, or SH 7108, 2023 : importations des Émirats depuis le Cameroun et exportations déclarées par le Cameroun.", "https://wits.worldbank.org/trade/comtrade/en/country/All/year/2023/tradeflow/Imports/partner/CMR/product/7108"),
 (4, "Banque mondiale, taux de change officiel moyen annuel (PA.NUS.FCRF), utilisé pour convertir les dollars en FCFA année par année.", "https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=CM"),
 (5, "Rapport ITIE Cameroun 2023 : collectes de la Sonamines (impôt synthétique minier libératoire 9,11 milliards FCFA et droit de sortie 1,37 milliard FCFA), relayé par Sikafinance.", "https://www.sikafinance.com/marches/cameroun-la-contrebande-d-or-prive-le-tresor-public-de-577-milliards-fcfa-en-5-ans_63257"),
 (6, "Gouvernement du Cameroun, juillet 2026 : 577,51 milliards FCFA de recettes non perçues sur 2021–2025 (Business in Cameroon) ; la page du ministère des Mines du 24/07/2026 cite 557 milliards.", "https://www.businessincameroon.com/mining/2807-16535-cameroon-says-undeclared-gold-exports-cost-state-cfaf577-billion-in-five-years"),
 (7, "Ministère des Mines, mai 2026 : près de 200 sociétés artisanales illégales identifiées dans l’Est et l’Adamaoua (Business in Cameroon).", "https://www.businessincameroon.com/mining/1805-16183-cameroon-tightens-pressure-on-illegal-gold-miners-over-missing-export-revenue"),
 (8, "Régimes fiscaux : codes miniers du Cameroun (lois 2016/017 et 2023/014, loi de finances 2023) et de pays producteurs (Ghana, Mali, Tanzanie, Rwanda, Ouganda). Synthèse et sources par pays : docs/recherche-or-cameroun/FISCALITE_COMPAREE.md. Taux tirés d’extraits, à vérifier au Journal officiel.", "https://github.com/boujieka/Boujieka/blob/ccr-0e8cc9da-w57q8p/docs/recherche-or-cameroun/FISCALITE_COMPAREE.md"),
 (9, "SWISSAID : étude 2024 (2 569 t d’or africain non déclaré importées par les Émirats, 2012–2022) et communiqué du 04/11/2025 (données 2024 des Émirats retirées de UN Comtrade).", "https://www.swissaid.ch/en/media/united-arab-emirates-more-than-ever-a-hub-for-conflict-gold/"),
 (10, "ITIE (EITI), « Cameroon’s gold gap » : 22,3 kg exportés officiellement en 2023, ≈ 165 milliards FCFA de pertes potentielles.", "https://eiti.org/impact-story/cameroons-gold-gap-how-eiti-data-driving-reforms"),
]

src_html = ''.join(f'<li id="src{n}"><span class="sn">[{n}]</span> {E(t)} <a href="{u}" target="_blank" rel="noopener">{E(u.split("//")[1].split("/")[0])}</a></li>' for n,t,u in SOURCES)

CSS = '''
:root{
 /* Planches de BD sur papier journal : cases encrées, récitatifs jaunes, bulles blanches */
 --papier:#fffdf6; --encre:#1b1712; --or:#f2b632; --laterite:#b5532f; --foret:#1f7a4d; --ciel:#9fd4ea; --gris:#6b6458;
 --f-titre:"Bowlby One SC", "Arial Black", sans-serif;
 --f-bulle:"Patrick Hand", "Comic Sans MS", cursive;
 --f-note:"IBM Plex Sans Condensed", "Arial Narrow", sans-serif;
 color-scheme: light;
}
body{background:var(--papier);color:var(--encre);font-family:var(--f-note);}
.wrap{max-width:1080px;margin:0 auto;padding-block:24px 48px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));display:flex;flex-direction:column;gap:40px;}
.couv{border:5px solid var(--encre);background:var(--laterite);color:var(--papier);position:relative;overflow:hidden;display:grid;grid-template-columns:1.2fr .8fr;gap:16px;padding:28px;box-shadow:8px 8px 0 var(--encre);}
.couv::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 1px 1px, rgba(0,0,0,.18) 1.2px, transparent 1.4px) 0 0/9px 9px;pointer-events:none;}
.hs{display:inline-block;background:var(--or);color:var(--encre);font-family:var(--f-titre);font-size:14px;letter-spacing:.08em;padding:4px 10px;border:3px solid var(--encre);transform:rotate(-2deg);}
.couv h1{font-family:var(--f-titre);font-size:clamp(34px,6.5vw,70px);line-height:.95;margin:14px 0 10px;text-wrap:balance;text-shadow:4px 4px 0 var(--encre);color:var(--or);}
.couv .sous{font-family:var(--f-bulle);font-size:clamp(20px,2.6vw,28px);margin:0 0 14px;}
.couv .pour{font-size:15px;max-width:52ch;line-height:1.5;margin:0;}
.couv svg{width:100%;height:auto;position:relative;z-index:1}
.couv > div{position:relative;z-index:1;min-width:0}
.planche{display:flex;flex-direction:column;gap:14px;}
.ph{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;border-bottom:4px solid var(--encre);padding-bottom:6px;}
.pn{font-family:var(--f-titre);font-size:13px;letter-spacing:.1em;background:var(--encre);color:var(--or);padding:3px 8px;}
.ph h2{font-family:var(--f-titre);font-size:clamp(22px,3.2vw,34px);margin:0;text-wrap:balance;}
.grille{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.case{margin:0;border:4px solid var(--encre);background:#fff;display:flex;flex-direction:column;min-width:0;box-shadow:5px 5px 0 var(--encre);}
.recit{margin:0;background:var(--or);border-bottom:3px solid var(--encre);padding:8px 10px;font-family:var(--f-note);font-weight:600;font-size:15px;line-height:1.35;}
.scene{position:relative;container-type:inline-size;aspect-ratio:400/240;max-width:100%;}
.scene svg{display:block;width:100%;height:100%;}
.bulle{position:absolute;margin:0;background:#fff;border:2.5px solid var(--encre);border-radius:18px;padding:.45em .7em;font-family:var(--f-bulle);font-size:max(13px,3.55cqw);line-height:1.15;box-shadow:2px 2px 0 var(--encre);}
.bulle.pense{border-style:dashed;border-radius:28px;background:#fffbe6;}
.bulle.note{border-radius:4px;background:#f3f7ff;font-family:var(--f-note);font-size:max(12px,3.1cqw);font-weight:500;}
.ref{font-family:var(--f-note);font-size:.72em;font-weight:700;color:var(--laterite);text-decoration:none;margin-left:2px;vertical-align:super;}
.ref:hover,.ref:focus-visible{text-decoration:underline;}
a:focus-visible{outline:3px solid var(--foret);outline-offset:2px;}
.avert{border:3px dashed var(--encre);padding:14px 18px;background:#fff;font-size:15px;line-height:1.55;max-width:80ch;}
.avert strong{font-family:var(--f-titre);font-weight:400;letter-spacing:.04em;}
.sources h2{font-family:var(--f-titre);font-size:clamp(20px,3vw,28px);margin:0 0 10px;}
.sources ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;}
.sources li{font-size:14px;line-height:1.5;max-width:95ch;}
.sources .sn{font-weight:700;color:var(--laterite);margin-right:4px;}
.sources a{color:var(--foret);word-break:break-word;}
.fin{font-family:var(--f-bulle);font-size:22px;text-align:center;margin:0;}
@media (max-width:720px){
 .grille{grid-template-columns:1fr;}
 .couv{grid-template-columns:1fr;padding:20px;}
 .bulle{font-size:max(12px,3.4cqw);}
}
@media (prefers-reduced-motion:no-preference){ .hs{transition:transform .2s} .couv:hover .hs{transform:rotate(2deg)} }
'''

COVER_SVG = f'<svg viewBox="0 0 400 300" role="img" aria-label="Pépite, la pépite d’or, entourée d’Abena, Moussa et Mama Ngo">{BG["aube"].replace("240","300")}{use("mama",20,120,90,140)}{use("abena",120,140,80,136)}{use("moussa",210,146,74,128)}{use("pepite",280,190,100,84)}{use("avion",230,30,150,64)}</svg>'

page = f'''<title>Le pays sous nos pieds</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bowlby+One+SC&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&family=Patrick+Hand&display=swap">
<style>{CSS}</style>
{SYMBOLS}
<main class="wrap">
 <header class="couv">
  <div>
   <span class="hs">HORS-SÉRIE</span>
   <h1>Le pays sous nos pieds</h1>
   <p class="sous">L’or des enfants de l’an 2000</p>
   <p class="pour">Pour toutes les filles et tous les fils du Cameroun nés en 2000. Une BD comique, mais avec des chiffres vrais : chaque nombre renvoie à sa source, numérotée entre crochets et listée à la fin.</p>
  </div>
  <div>{COVER_SVG}</div>
 </header>
 {"".join(PL)}
 <aside class="avert"><strong>Avertissement des auteurs.</strong> Les personnages (Abena, Moussa, Mama Ngo, Pépite, Monsieur Miroir) sont fictifs. Les chiffres viennent des statistiques douanières internationales (comparaison « miroir ») et de sources officielles. Ces statistiques montrent un écart entre ce qui est déclaré au départ et à l’arrivée ; elles ne prouvent ni l’origine exacte de chaque gramme, ni la responsabilité d’une personne ou d’une entreprise précise. Données arrêtées au 31 octobre 2026.</aside>
 <section class="sources" id="sources"><h2>Sources</h2><ol>{src_html}</ol></section>
 <p class="fin">— Fin du hors-série. Partagez-le avec un ami né en 2000. —</p>
</main>'''
open('/home/user/Boujieka/docs/bd/le-pays-sous-nos-pieds.html','w').write(page)
print(len(page))
