import sys, re
src = open(sys.path[0] + '/generer_planches_01_10.py').read()
lines = src.split('\n')
prefix = '\n'.join(lines[:152])
css = src[src.index("CSS = '''"):src.index("COVER = ")]
exec(prefix)
exec(css)
OUT = sys.argv[1]

# ---- nouveaux personnages et accessoires
NEW = f'''
 {person('nora','#6a3f25','#fff','#7fc3c9',
   head=f'<path d="M28 30 Q50 12 72 30 L70 22 Q50 6 30 22 Z" fill="#2a1a12"/><rect x="36" y="12" width="28" height="10" rx="3" fill="#fff" stroke="{K}" stroke-width="2"/><path d="M50 13 v8 M46 17 h8" stroke="#c8402d" stroke-width="2.5"/>',
   extra=f'<path d="M36 70 Q34 100 50 104 Q66 100 64 70" fill="none" stroke="#333" stroke-width="3"/><circle cx="50" cy="106" r="5" fill="#9aa" stroke="{K}" stroke-width="2"/><path d="M58 84 v10 M53 89 h10" stroke="#c8402d" stroke-width="3"/>')}
 {person('grace','#7a4a2b','#e88a2e','#2d3e63',
   head=f'<path d="M24 34 Q24 8 50 8 Q76 8 76 34 Z" fill="#f2d65c" stroke="{K}" stroke-width="3"/><rect x="20" y="30" width="60" height="6" rx="3" fill="#f2d65c" stroke="{K}" stroke-width="2"/>',
   extra=f'<rect x="58" y="112" width="18" height="26" rx="3" fill="#f2b632" stroke="{K}" stroke-width="2.5"/><rect x="61" y="115" width="12" height="8" fill="#cfe8c0"/><path d="M64 138 v8 M70 138 v8" stroke="#c8402d" stroke-width="2"/>')}
 {person('reparation','#5b3620','#1f7a4d','#1f7a4d',
   head=f'<path d="M26 32 Q50 10 74 32 Z" fill="#c8402d" stroke="{K}" stroke-width="3"/>',
   extra=f'<path d="M78 70 L92 52" stroke="#777" stroke-width="7" stroke-linecap="round"/><circle cx="94" cy="49" r="7" fill="none" stroke="#777" stroke-width="4"/><rect x="2" y="112" width="30" height="22" fill="#c8402d" stroke="{K}" stroke-width="2.5"/><path d="M10 112 v-6 h14 v6" fill="none" stroke="{K}" stroke-width="2.5"/>')}
 <symbol id="enveloppe" viewBox="0 0 60 40"><rect x="2" y="2" width="56" height="36" fill="#fffbe6" stroke="{K}" stroke-width="2.5"/><path d="M2 2 L30 22 L58 2" fill="none" stroke="{K}" stroke-width="2.5"/></symbol>
 <symbol id="pompe" viewBox="0 0 60 100"><rect x="22" y="20" width="16" height="70" fill="#2d6f8a" stroke="{K}" stroke-width="3"/><path d="M38 30 L58 18" stroke="{K}" stroke-width="5" stroke-linecap="round"/><path d="M22 40 L6 44 L6 52" fill="none" stroke="#2d6f8a" stroke-width="6"/><rect x="10" y="88" width="40" height="10" fill="#9a8f80" stroke="{K}" stroke-width="2"/></symbol>
 <symbol id="pompecassee" viewBox="0 0 60 100"><rect x="22" y="20" width="16" height="70" fill="#8a7a6a" stroke="{K}" stroke-width="3"/><path d="M38 30 L50 44" stroke="{K}" stroke-width="5" stroke-linecap="round"/><path d="M22 40 L6 44 L6 52" fill="none" stroke="#8a7a6a" stroke-width="6"/><rect x="10" y="88" width="40" height="10" fill="#9a8f80" stroke="{K}" stroke-width="2"/><circle cx="30" cy="56" r="4" fill="#b5532f"/><circle cx="26" cy="70" r="3" fill="#b5532f"/></symbol>
 <symbol id="maquette" viewBox="0 0 140 90"><rect x="10" y="40" width="120" height="44" fill="#d9a066" stroke="{K}" stroke-width="3"/><path d="M4 42 L70 8 L136 42 Z" fill="#c9915a" stroke="{K}" stroke-width="3" stroke-linejoin="round"/><rect x="60" y="56" width="20" height="28" fill="#8a5a1d"/><rect x="22" y="52" width="22" height="16" fill="#f4ecd0" stroke="{K}" stroke-width="2"/><rect x="96" y="52" width="22" height="16" fill="#f4ecd0" stroke="{K}" stroke-width="2"/></symbol>
</defs>'''
SYMBOLS = SYMBOLS.replace('</defs>', NEW, 1)
P.update({'nora':(70,120),'grace':(72,122),'reparation':(74,124)})
SPK.update({'NORA':'#2d7f86','GRÂCE':'#c46a10','MADAME RÉPARATION':'#1f7a4d','INSPECTEUR DOUBLE-COPIE':'#4a453d'})
BG['conseil'] = '<rect width="400" height="240" fill="#e9dcc3"/><rect x="40" y="14" width="320" height="34" fill="#1f7a4d" stroke="#1b1712" stroke-width="3"/>' + T(200,37,14,'GRAND CONSEIL DE NKOAGNE','#fff') + '<rect y="196" width="400" height="44" fill="#a07a50"/><path d="M0 196 L400 196" stroke="#1b1712" stroke-width="3"/>'

def fiche4(titre, fait, ignore, cout, question):
    PL.append(f'<aside class="fiche"><h3>Fiche vérité · {E(titre)}</h3><dl class="d4"><div class="f1"><dt>Le fait</dt><dd>{fait}</dd></div><div class="f2"><dt>Ce qu’on ignore</dt><dd>{ignore}</dd></div><div class="f4"><dt>Le coût possible</dt><dd>{cout}</dd></div><div class="f3"><dt>La question à poser</dt><dd>{question}</dd></div></dl></aside>')

def board(lines, x=36, y0=46, dy=18, size=12.5):
    out=[]
    for i,(l,r,col) in enumerate(lines):
        yy=y0+i*dy
        out.append(T(x,yy,size,l,col,'start','600'))
        out.append(T(364,yy,size,r,col,'end','700'))
    return ''.join(out)

PL.clear()
section("Le grand conseil des trente milliards", "Épisode 16 · planches 082 à 086 · Mouvement III, Reconstruire des choix")

envs = ''.join(use('enveloppe',14+i*48,150+(i%2)*14,42,28) for i in range(6)) + ''.join(T(35+i*48,206+(i%2)*14,9,t) for i,t in enumerate(['Écoles','Santé','Forages','Eau solaire','Électricité','Entretien']))
planche(82, "Un budget sans trésor", [
 panel('conseil', ['<rect x="150" y="66" width="230" height="56" fill="#fff" stroke="#1b1712" stroke-width="3" transform="rotate(-3 265 94)"/>', T(265,92,16,'30 Md FCFA','#1f7a4d',extra='transform="rotate(-3 265 94)"'), T(265,112,13,'EXERCICE FICTIF','#c8402d',extra='transform="rotate(-3 265 94)"'), ch('aicha',40)], "Nkoagne, salle polyvalente. Le Grand Conseil des trente milliards se réunit.",
  [('',30,62,40,q('AÏCHA',"On s’entraîne à choisir, comme si on avait 30 milliards."))]),
 panel('conseil', [ch('junior',160)], None,
  [('',3,24,52,q('JUNIOR',"Attends… l’or nous a payé ça ?"))]),
 panel('conseil', [ch('fifi',40)], None,
  [('',30,22,40,q('FIFI',"Non. C’est une hypothèse pour apprendre à choisir.")),
   ('note civ',30,56,66,"Trente milliards, c’est notre budget d’exercice. Ce n’est ni l’argent retrouvé ni le prix d’une promesse.")]),
 panel('conseil', [envs, ch('boris',318,s=.85)], None,
  [('',3,20,74,q('BORIS',"Livraison ! Six enveloppes… zéro billet dedans.")),
   ('note hyp',3,38,74,"Ordre de grandeur : 30 Md ≈ 5,4 % des 557 Md estimés sur le site du MINMIDT, à condition qu’ils soient confirmés, recouvrés et affectés."+sup(4))]),
], "Six enveloppes, six camps.")

planche(83, "La guerre des priorités", [
 panel('conseil', [ch('mballa',40), '<rect x="20" y="96" width="72" height="20" fill="#fff" stroke="#1b1712" stroke-width="2"/>', T(56,111,11,'ÉCOLES')], None,
  [('',30,24,50,q('TONTON MBALLA',"Je vote ciment ! Des murs, des toits, des bancs !"))]),
 panel('conseil', [ch('nora',290,flip=True), '<rect x="282" y="96" width="76" height="20" fill="#fff" stroke="#1b1712" stroke-width="2"/>', T(320,111,11,'SANTÉ')], None,
  [('',3,24,60,q('NORA',"Le ciment sans soins ne guérit pas. Il faut des infirmières, des médicaments, une chaîne du froid."))]),
 panel('conseil', [ch('grace',40), '<rect x="28" y="96" width="80" height="20" fill="#fff" stroke="#1b1712" stroke-width="2"/>', T(68,111,11,'RÉSEAU')], None,
  [('',30,24,64,q('GRÂCE',"Et sans courant, ni ton école ni son centre n’ont de lumière le soir. Ni de frigo pour les vaccins."))]),
 panel('conseil', [ch('chantal',300,flip=True)], None,
  [('',3,8,70,q('MAMI CHANTAL',"Et qui entretient tout ça, après la photo d’inauguration ?")),
   ('note',3,56,66,"Arbitrer entre secteurs, c’est le rôle d’un budget public. La BD n’impose aucun ordre de priorité.")]),
], "La question de Mami reste sur la table.")

LIG = [
 ('300 blocs de 2 salles × 22 M','6,600','#fff'),
 ('80 centres de santé (bâtiments) × 50 M','4,000','#fff'),
 ('350 forages équipés × 10 M *','3,500','#d9b8ff'),
 ('40 réseaux d’eau solaires × 48,1 M','1,924','#fff'),
 ('Électricité : enveloppe non dimensionnée **','10,000','#d9b8ff'),
 ('Personnel, entretien : provision','3,976','#fff'),
 ('TOTAL (Md FCFA)','30,000','#ffd770'),
]
planche(84, "Le budget à six lignes", [
 panel('tableau', [board(LIG), '<path d="M36 141 L364 141" stroke="#fff" stroke-width="2"/>'], None,
  [('',3,74,60,q('AÏCHA',"Toutes les additions doivent tomber juste. Et elles tombent juste."+sup(1,2,3,5)))]),
 panel('conseil', [ch('boris',60), '<rect x="190" y="80" width="190" height="90" fill="#24493a" stroke="#6e4b2a" stroke-width="5"/>', T(285,112,13,'6,6 + 4 + 3,5','#fff'), T(285,132,13,'+ 1,924 + 10 + 3,976','#fff'), T(285,156,15,'= 30 Md','#ffd770')], None,
  [('',3,6,64,q('BORIS',"Même mes soudures n’alignent pas autant de chiffres !"))]),
 panel('conseil', [ch('fifi',300,flip=True)], None,
  [('note hyp',3,8,70,"* Correction v2.1 : l’avis S8 parle-t-il de 10 M <b>par forage</b> ou <b>par lot de deux</b> ? Dans le second cas, la ligne passe de 3,5 à 1,75 Md."+sup(3)),
   ('',3,56,64,q('FIFI',"Une ligne entière dépend d’un seul mot : « lot ». On relit l’avis avant de dessiner les forages."))]),
 panel('conseil', [ch('grace',40), ch('junior',310,flip=True,s=.85)], None,
  [('note hyp',28,4,70,"** Pour 200 localités solaires, un document cite environ 96 Md FCFA ; un prêt Afreximbank finance une phase pour 34,7 Md (53 M€)."+sup(6,7)),
   ('',28,46,46,q('JUNIOR',"Alors 10 milliards, ça électrifie combien de villages ?")),
   ('',28,72,46,q('GRÂCE',"Personne ne peut le dire sans étude. Un prêt partiel n’est pas le coût d’un programme."))]),
], "Un citoyen lève la main : « Où est le projet détaillé ? »",
 source="Coûts d’appels d’offres ARMP (S6 à S9) et Compact énergie (S10), cités d’après la bible v2.1 "+sup(1,2,3,5,6)+" ; prêt Afreximbank "+sup(7)+".")

planche(85, "Un devis n’est pas un chantier", [
 panel('conseil', [use('maquette',170,110,150,96), '<path d="M150 150 L340 150" stroke="#c8402d" stroke-width="6"/>', ch('inspecteur',50), T(300,104,10,'carton','#6b6458')], None,
  [('',40,4,56,q('MAMI CHANTAL',"(hors champ) Tu inaugures le budget… ou les toilettes ?"))]),
 panel('conseil', [ch('inspecteur',150), '<path d="M230 160 l30 -12 M230 160 l30 12" stroke="#777" stroke-width="5" stroke-linecap="round"/>', '<path d="M260 150 q20 20 40 0" stroke="#c8402d" stroke-width="5" fill="none"/>'], None,
  [('',3,6,60,q('INSPECTEUR DOUBLE-COPIE',"J’ai coupé le ruban avant l’appel d’offres… c’est grave ?"))]),
 panel('tableau', [T(200,58,14,'ÉTUDES  →  APPEL D’OFFRES  →  CONTRÔLE','#b8f0c8'), T(200,84,14,'→  RÉCEPTION  →  ENTRETIEN','#b8f0c8'), ch('mballa',300,s=.85,flip=True)], None,
  [('',3,66,64,q('TONTON MBALLA',"Chez moi, on mesure deux fois et on coupe une fois. Le ruban, c’est la dernière étape."))]),
 panel('conseil', [ch('fifi',40), ch('reparation',320,flip=True,s=.85)], "Au fond de la salle, une silhouette arrive avec une caisse à outils.",
  [('note',28,6,50,"22 M, 50 M, 10 M, 48,1 M : des montants d’appels d’offres pour un site donné. Ce ne sont ni des factures d’ouvrages achevés ni des prix nationaux."+sup(1,2,3,5))]),
], "Madame Réparation a une question.")

planche(86, "La décennie de maintenance", [
 panel('collines', [use('pompe',180,110,70,118), T(215,104,14,'ANNÉE 1','#1b1712'), ch('reparation',40)], None,
  [('',3,4,62,q('MADAME RÉPARATION',"Le vrai trésor, ce n’est pas l’inauguration. C’est dix ans de service."))]),
 panel('collines', [use('pompecassee',180,110,70,118), T(215,104,14,'ANNÉE 5','#1b1712'), ch('reparation',260,flip=True)], None,
  [('note',3,4,58,"Pièces d’usure (cuir de pompe, batteries, onduleurs), formation d’un réparateur local : un coût récurrent à chiffrer pour chaque ouvrage.")]),
 panel('conseil', [ch('aicha',40), ch('nora',300,flip=True)], None,
  [('',28,6,46,q('AÏCHA',"Notre provision de 3,976 milliards n’est pas encore un plan d’exploitation.")),
   ('',28,52,46,q('NORA',"Et les salaires des infirmières, ils sont dans quelle enveloppe ?"))]),
 panel('conseil', [ch('junior',40), '<rect x="140" y="96" width="140" height="110" fill="#fff" stroke="#1b1712" stroke-width="3"/>', T(210,118,10,'DEMANDE À LA COMMUNE','#1f7a4d'), T(150,140,9,'1. Avis d’appel d’offres','#1b1712','start'), T(150,158,9,'2. PV de réception','#1b1712','start'), T(150,176,9,'3. Budget d’entretien sur 10 ans','#1b1712','start'), ch('chantal',300,flip=True,s=.9)], None,
  [('note civ',3,4,58,q('MAMI CHANTAL',"Pas de reçu, pas de ruban."))]),
], "À suivre : épisode 17, « La brigade des marchés publics ».")

fiche4("Épisode 16",
 "Coûts repris d’appels d’offres ARMP (S6 à S9) : 22 M FCFA pour un bloc de deux salles (Yagoua, 2024) ; 50 M pour un centre de santé (Ndogmbé II, 2026) ; 10 M pour des forages (2026) ; 48 110 654 FCFA pour un réseau d’eau solaire (2026). L’addition donne exactement 30,000 Md.",
 "Si le prix des forages est de 10 M par forage ou par lot de deux. Le coût réel de l’électrification (environ 96 Md pour 200 localités selon un document, 34,7 Md pour une phase financée par prêt). Les charges récurrentes sur 10 ans.",
 "30 Md : un <b>exercice fictif</b>, environ 5,4 % des 557 Md (ou 5,2 % des 577,5 Md) d’estimations publiées, <i>à condition qu’ils soient</i> confirmés, recouvrés et affectés.",
 "Pour chaque ouvrage de ma commune : quel avis d’appel d’offres, quel procès-verbal de réception, quel budget d’entretien ?")

SOURCES = [
 (1, "S6 · ARMP Cameroun (2024), bloc de deux salles de classe, 22 M FCFA, Yagoua. Cité d’après la bible v2.1, avis non relu par nous.", "https://www.armp.cm/details?id_publication=45339&type_publication=AO"),
 (2, "S7 · ARMP Cameroun (12/05/2026), centre de santé intégré de Ndogmbé II, 50 M FCFA. Cité d’après la bible v2.1, non relu.", "https://new.armp.cm/details?id_publication=62784&type_publication=AO"),
 (3, "S8 · ARMP Cameroun (02/03/2026), forages équipés, « 10 M FCFA / lot ». À trancher : par forage ou par lot de deux ? Cité d’après la bible v2.1, non relu.", "https://www.armp.cm/details?id_publication=60732&type_publication=AO"),
 (4, "S4 · MINMIDT (24/07/2026), Tableau sommaire des exploitations d’or 2021–2025 : 557 Md FCFA de pertes estimées ; d’autres reprises citent 577,5 Md.", "https://www.minmidt.cm/tableau-sommaire-des-exploitations-dor-sur-les-cinq-dernieres-annees-2021-a-2025/"),
 (5, "S9 · ARMP Cameroun (2026), réseau d’adduction d’eau solaire, 48 110 654 FCFA. Le libellé (Conseil régional de l’Est ou Offices régionaux) est à harmoniser. Non relu.", "https://armp.cm/details?id_publication=65053&type_publication=AO"),
 (6, "S10 · Compact énergétique national du Cameroun (Mission 300). Le chiffre « ≈ 96 Md FCFA pour 200 localités » n’a pas été retrouvé : à vérifier dans l’annexe I.", "https://www.afdb.org/sites/default/files/documents/publications/cameroon_compact_m300.pdf"),
 (7, "S17 · MINEPAT (09/03/2023) : prêt Afreximbank de 53 M€ (≈ 34,7 Md FCFA) pour l’électrification solaire de 200 localités (troisième phase).", "https://minepat.gov.cm/en/2023/03/09/cameroon-afreximbank-fcfa-34-7-billion-to-bring-electricity-to-200-localities-in-cameroon/"),
]
src_html = ''.join(f'<li id="src{n}"><span class="sn">[{n}]</span> {E(t)} <a href="{u}" target="_blank" rel="noopener">{E(u.split("//")[1].split("/")[0])}</a></li>' for n,t,u in SOURCES)
CSS += '''
.fiche dl.d4{grid-template-columns:repeat(4,1fr)} .f4{background:#ffe7d1}
@media (max-width:900px){ .fiche dl.d4{grid-template-columns:1fr 1fr} }
@media (max-width:720px){ .fiche dl.d4{grid-template-columns:1fr} }
'''
COVER = f'<svg viewBox="0 0 400 300" role="img" aria-label="Le Grand Conseil : Aïcha, Tonton Mballa, Nora, Grâce et Mami Chantal autour de six enveloppes">{BG["conseil"].replace("240","300")}{use("mballa",14,160,70,120)}{use("nora",84,162,68,118)}{use("aicha",156,160,70,120)}{use("grace",226,158,70,122)}{use("chantal",300,154,72,126)}' + ''.join(use('enveloppe',40+i*56,80,46,30) for i in range(6)) + '</svg>'
page = f'''<title>Le Grand Conseil</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bowlby+One+SC&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&family=Patrick+Hand&display=swap">
<style>{CSS}</style>
{SYMBOLS}
<main class="wrap">
 <header class="couv">
  <div>
   <p class="serie">COURANT CONTINENTAL · LE PAYS SOUS NOS PIEDS</p>
   <span class="hs">ÉPISODE 16</span>
   <h1>Le Grand Conseil des trente milliards</h1>
   <p class="accroche">« Trente milliards, c’est notre budget d’exercice. Ce n’est ni l’argent retrouvé ni le prix d’une promesse. »</p>
   <p class="pour">Planches 082 à 086 de la bible v2.1. Un exercice de pédagogie budgétaire : comment choisir, chiffrer et entretenir des écoles, des centres de santé, des forages, des réseaux d’eau et l’électricité, sans confondre devis et chantier. Les corrections de la relecture v2.1 sont intégrées.</p>
   <div class="legende" aria-label="Code couleur des encadrés"><span class="lg-cm">Bleu : déclaré par le Cameroun</span><span class="lg-imp">Or : déclaré par le partenaire</span><span class="lg-hyp">Violet : hypothèse, à vérifier</span><span class="lg-civ">Vert : option citoyenne, budget fictif</span></div>
  </div>
  <div>{COVER}</div>
 </header>
 {"".join(PL)}
 <aside class="avert"><strong>Avertissement.</strong> Fiction documentée. Le portefeuille de 30 Md FCFA est un exercice fictif : ce n’est pas une mesure du manque à gagner, ni de l’argent retrouvé, ni un devis réalisable en l’état. Les coûts unitaires viennent d’appels d’offres publiés pour des sites précis ; ils ne valent pas prix national et ne prouvent pas qu’un ouvrage a été réalisé. Personnages inventés ; aucune institution réelle n’est caricaturée.</aside>
 <section class="sources" id="sources"><h2>Sources</h2><ol>{src_html}</ol></section>
</main>'''
open(OUT,'w').write(page)
print(len(page))
