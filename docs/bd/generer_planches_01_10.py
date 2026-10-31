import html, re, sys
E=lambda s: html.escape(s, quote=True)
OUT = sys.argv[1] if len(sys.argv)>1 else 'out.html'
K='#1b1712'
def person(id, skin, top, bottom, head='', extra='', vb='0 0 100 170'):
    return f'''<symbol id="{id}" viewBox="{vb}">{head}
   <circle cx="50" cy="42" r="23" fill="{skin}" stroke="{K}" stroke-width="3"/>
   <circle cx="42" cy="42" r="3.4" fill="{K}"/><circle cx="58" cy="42" r="3.4" fill="{K}"/>
   <path d="M42 53 Q50 59 58 53" fill="none" stroke="{K}" stroke-width="3" stroke-linecap="round"/>
   <path d="M24 70 Q50 60 76 70 L80 128 L20 128 Z" fill="{top}" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>
   <path d="M26 126 L74 126 L72 156 L56 156 L50 138 L44 156 L28 156 Z" fill="{bottom}" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>
   <path d="M36 158 L28 166 L44 166 Z M64 158 L56 166 L72 166 Z" fill="#fff" stroke="{K}" stroke-width="2.5"/>{extra}</symbol>'''

SYMBOLS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
 <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{K}" opacity=".09"/></pattern>
 <symbol id="pepite" viewBox="0 0 120 100">
  <path d="M18 62 L10 40 L30 18 L58 10 L90 16 L110 40 L104 70 L80 90 L40 92 Z" fill="#f2b632" stroke="{K}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M30 30 L50 22 M78 26 L94 40" stroke="#fff3c4" stroke-width="5" stroke-linecap="round"/>
  <circle cx="46" cy="50" r="9" fill="#fff"/><circle cx="78" cy="50" r="9" fill="#fff"/>
  <circle cx="48" cy="52" r="4.5" fill="{K}"/><circle cx="80" cy="52" r="4.5" fill="{K}"/>
  <path d="M48 70 Q62 82 78 70" fill="none" stroke="{K}" stroke-width="4" stroke-linecap="round"/></symbol>
 {person('aicha','#7a4a2b','#e0672e','#2d4a7a',
   head=f'<circle cx="50" cy="16" r="14" fill="#2a1a12"/><circle cx="31" cy="32" r="9" fill="#2a1a12"/><circle cx="69" cy="32" r="9" fill="#2a1a12"/>',
   extra=f'<rect x="62" y="88" width="30" height="40" rx="4" fill="#3a3f4a" stroke="{K}" stroke-width="3"/><rect x="66" y="92" width="22" height="30" fill="#9fd4ea"/><path d="M68 112 L74 104 L80 108 L86 98" stroke="#c8402d" stroke-width="2" fill="none"/><path d="M30 162 q6 4 12 0 M58 162 q6 4 12 0" stroke="#b5532f" stroke-width="2.5" fill="none"/>')}
 {person('boris','#5b3620','#2f5fa8','#2f5fa8',
   head=f'<path d="M27 34 Q50 12 73 34" fill="{K}"/>',
   extra=f'<rect x="28" y="22" width="44" height="10" rx="5" fill="#333" stroke="{K}" stroke-width="2"/><circle cx="40" cy="27" r="6" fill="#4caf7a" stroke="{K}" stroke-width="2"/><circle cx="60" cy="27" r="6" fill="#4caf7a" stroke="{K}" stroke-width="2"/><rect x="40" y="80" width="20" height="16" fill="#244b85" stroke="{K}" stroke-width="2"/><path d="M14 80 L24 74 M86 80 L76 74" stroke="{K}" stroke-width="3"/>')}
 {person('fifi','#8a5636','#f2c94c','#6b3f8c',
   head=f'<path d="M26 38 Q24 14 50 14 Q76 14 74 38" fill="#2a1a12"/><path d="M28 40 L22 92 M34 44 L30 96 M72 40 L78 92 M66 44 L70 96" stroke="#2a1a12" stroke-width="5" stroke-linecap="round"/>',
   extra=f'<rect x="8" y="86" width="26" height="32" fill="#fff" stroke="{K}" stroke-width="3"/><path d="M8 90 h26 M8 96 h26" stroke="#2d5bb8" stroke-width="1.5"/><circle cx="12" cy="86" r="2.5" fill="none" stroke="{K}" stroke-width="1.5"/><circle cx="20" cy="86" r="2.5" fill="none" stroke="{K}" stroke-width="1.5"/><circle cx="28" cy="86" r="2.5" fill="none" stroke="{K}" stroke-width="1.5"/>')}
 {person('mballa','#4e2e1b','#8a5a1d','#3d3a34',
   head=f'<path d="M28 30 Q50 14 72 30" fill="#d8d4cc" stroke="{K}" stroke-width="2"/><path d="M34 56 Q50 72 66 56 L62 66 Q50 74 38 66Z" fill="#d8d4cc" stroke="{K}" stroke-width="2"/>',
   extra=f'<rect x="66" y="96" width="22" height="18" rx="3" fill="#f2b632" stroke="{K}" stroke-width="3"/><path d="M66 106 L40 106" stroke="#f2b632" stroke-width="5"/><path d="M44 103 v6 M50 103 v6 M56 103 v6" stroke="{K}" stroke-width="1"/>')}
 {person('chantal','#6a3f25','#c8402d','#c8402d',
   head=f'<path d="M24 34 Q22 0 50 4 Q80 0 76 34 Z" fill="#7b3f8c" stroke="{K}" stroke-width="3"/><path d="M70 8 L88 0 L84 18 Z" fill="#f2b632" stroke="{K}" stroke-width="2.5"/>',
   extra=f'<path d="M22 100 Q50 92 78 100 M22 116 Q50 108 78 116" stroke="#f2b632" stroke-width="4" fill="none"/><rect x="80" y="84" width="6" height="28" fill="#1f7a4d" stroke="{K}" stroke-width="2"/><path d="M80 84 h-8 M80 90 h-8 M80 96 h-8" stroke="{K}" stroke-width="2"/>')}
 {person('junior','#6a4026','#1f7a4d','#2d3e63',
   head=f'<path d="M26 32 Q50 12 74 32 Z" fill="#c8402d" stroke="{K}" stroke-width="3"/><path d="M26 32 L8 36 L10 28 Z" fill="#c8402d" stroke="{K}" stroke-width="2.5"/>',
   extra=f'<path d="M28 70 L70 120" stroke="{K}" stroke-width="3"/><rect x="62" y="112" width="24" height="16" rx="2" fill="#333" stroke="{K}" stroke-width="2"/><path d="M66 112 v-4 M80 112 v-4" stroke="#c8402d" stroke-width="3"/>')}
 {person('glacon','#4b2c19','#fff','#3d3a34',
   head=f'<ellipse cx="50" cy="22" rx="18" ry="6" fill="#4b2c19" opacity=".3"/>',
   extra=f'<path d="M30 80 L70 80 L74 128 L26 128 Z" fill="#9fd4ea" stroke="{K}" stroke-width="3"/><rect x="74" y="80" width="10" height="34" rx="3" fill="#1f7a4d" stroke="{K}" stroke-width="2"/>')}
 {person('inspecteur','#5b3620','#6b6458','#4a453d',
   head=f'<rect x="30" y="36" width="16" height="11" rx="3" fill="none" stroke="{K}" stroke-width="2.5"/><rect x="54" y="36" width="16" height="11" rx="3" fill="none" stroke="{K}" stroke-width="2.5"/><path d="M28 26 Q50 16 72 26" stroke="{K}" stroke-width="5" fill="none"/>',
   extra=f'<rect x="70" y="64" width="12" height="26" fill="#8a5a1d" stroke="{K}" stroke-width="2.5"/><rect x="62" y="88" width="28" height="12" fill="#c8402d" stroke="{K}" stroke-width="2.5"/>')}
 {person('passe','#7a4a2b','#5b2a7a','#2a1f33',
   head=f'<rect x="28" y="2" width="44" height="18" fill="{K}"/><rect x="18" y="18" width="64" height="5" fill="{K}"/>',
   extra=f'<path d="M50 66 L46 100 L50 106 L54 100 Z" fill="#f2b632"/><rect x="4" y="106" width="30" height="22" rx="3" fill="#1b1712"/><circle cx="12" cy="117" r="3" fill="#f2b632"/><circle cx="20" cy="117" r="3" fill="#f2b632"/><circle cx="28" cy="117" r="3" fill="#f2b632"/><rect x="70" y="40" width="10" height="18" rx="2" fill="#333"/>')}
 {person('sagefemme','#6a3f25','#7fc3c9','#7fc3c9',
   head=f'<path d="M26 32 Q50 10 74 32 Z" fill="#7fc3c9" stroke="{K}" stroke-width="3"/>',
   extra=f'<ellipse cx="50" cy="80" rx="22" ry="12" fill="#fff" stroke="{K}" stroke-width="2.5"/><circle cx="36" cy="76" r="9" fill="#8a5636" stroke="{K}" stroke-width="2"/>')}
 {person('pere','#4e2e1b','#1f7a4d','#3d3a34', head=f'<path d="M27 32 Q50 14 73 32" fill="{K}"/>')}
 <symbol id="congel" viewBox="0 0 150 110">
  <rect x="8" y="40" width="134" height="66" rx="8" fill="#eef4f7" stroke="{K}" stroke-width="4"/>
  <path d="M4 40 Q75 14 146 40 Z" fill="#dfeaf0" stroke="{K}" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="58" cy="32" r="5" fill="{K}"/><circle cx="92" cy="32" r="5" fill="{K}"/><path d="M50 22 L64 26 M100 22 L86 26" stroke="{K}" stroke-width="3" stroke-linecap="round"/>
  <path d="M60 66 Q75 58 90 66" fill="none" stroke="{K}" stroke-width="4" stroke-linecap="round"/>
  <rect x="62" y="80" width="26" height="8" rx="3" fill="#9aa"/><text x="75" y="102" text-anchor="middle" font-size="9" font-family="sans-serif" font-weight="700" fill="#6b6458">M. CONGÉLATEUR</text></symbol>
 <symbol id="congelouvert" viewBox="0 0 150 130">
  <rect x="8" y="60" width="134" height="66" rx="8" fill="#eef4f7" stroke="{K}" stroke-width="4"/>
  <path d="M10 60 L30 6 L140 6 L142 60" fill="#dfeaf0" stroke="{K}" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="64" cy="28" r="5" fill="{K}"/><circle cx="98" cy="28" r="5" fill="{K}"/><path d="M68 42 Q82 50 96 42" fill="none" stroke="{K}" stroke-width="4" stroke-linecap="round"/>
  <rect x="44" y="46" width="62" height="30" rx="3" fill="#f2b632" stroke="{K}" stroke-width="3" transform="rotate(-6 75 60)"/>
  <text x="75" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="800" fill="{K}" transform="rotate(-6 75 60)">PREUVES</text>
  <path d="M30 50 l-8 -10 M120 46 l8 -12 M75 2 v-0" stroke="#f2b632" stroke-width="4" stroke-linecap="round"/></symbol>
 <symbol id="camion" viewBox="0 0 220 110">
  <rect x="4" y="14" width="150" height="70" fill="#e6b47a" stroke="{K}" stroke-width="4"/><path d="M154 34 L196 34 L216 60 L216 84 L154 84 Z" fill="#c8402d" stroke="{K}" stroke-width="4" stroke-linejoin="round"/>
  <rect x="166" y="40" width="26" height="18" fill="#9fd4ea" stroke="{K}" stroke-width="2"/>
  <circle cx="40" cy="92" r="14" fill="#333" stroke="{K}" stroke-width="3"/><circle cx="120" cy="92" r="14" fill="#333" stroke="{K}" stroke-width="3"/><circle cx="188" cy="92" r="14" fill="#333" stroke="{K}" stroke-width="3"/>
  <text x="79" y="58" text-anchor="middle" font-size="22" font-family="sans-serif" font-weight="800" fill="{K}">10,9 t</text></symbol>
 <symbol id="balance4" viewBox="0 0 80 80">
  <path d="M40 10 L40 70 M24 72 L56 72 M14 26 L66 26" stroke="{K}" stroke-width="4" stroke-linecap="round"/>
  <path d="M6 44 Q14 54 22 44 Z" fill="#cfe0ff" stroke="{K}" stroke-width="2.5"/><path d="M58 44 Q66 54 74 44 Z" fill="#cfe0ff" stroke="{K}" stroke-width="2.5"/>
  <rect x="8" y="34" width="12" height="10" fill="#2d5bb8"/><text x="14" y="42" text-anchor="middle" font-size="7" fill="#fff" font-family="sans-serif" font-weight="700">4kg</text></symbol>
 <symbol id="ventilo" viewBox="0 0 60 90">
  <circle cx="30" cy="30" r="26" fill="#fff" stroke="{K}" stroke-width="3"/><path d="M30 30 L30 8 Q40 14 30 30 L52 34 Q46 44 30 30 L16 46 Q10 36 30 30" fill="#9fd4ea" stroke="{K}" stroke-width="2"/>
  <path d="M30 56 L30 80 M14 86 L46 86" stroke="{K}" stroke-width="5" stroke-linecap="round"/></symbol>
 <symbol id="ordi" viewBox="0 0 120 90">
  <rect x="10" y="4" width="100" height="62" rx="4" fill="#333" stroke="{K}" stroke-width="3"/><rect x="16" y="10" width="88" height="50" fill="#dfe9f5"/>
  <path d="M0 70 L120 70 L110 84 L10 84 Z" fill="#777" stroke="{K}" stroke-width="3"/><path d="M60 20 q10 6 0 14" stroke="#c8402d" stroke-width="2" fill="none"/></symbol>
 <symbol id="sac" viewBox="0 0 60 70">
  <path d="M12 14 Q30 4 48 14 L54 64 L6 64 Z" fill="#f4ecd0" stroke="{K}" stroke-width="3" stroke-linejoin="round"/><path d="M18 14 L42 14" stroke="{K}" stroke-width="3"/><text x="30" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="700" fill="#8a5a1d">RIZ</text></symbol>
 <symbol id="telephone" viewBox="0 0 40 70">
  <rect x="4" y="2" width="32" height="64" rx="6" fill="#222" stroke="{K}" stroke-width="3"/><rect x="8" y="10" width="24" height="44" fill="#e3eeff"/><path d="M11 18 h18 M11 26 h12 M11 34 h16" stroke="#2d5bb8" stroke-width="3"/></symbol>
 <symbol id="lampe" viewBox="0 0 50 70">
  <rect x="10" y="20" width="30" height="44" rx="4" fill="#f2b632" stroke="{K}" stroke-width="3"/><rect x="4" y="6" width="42" height="14" fill="#2d3e63" stroke="{K}" stroke-width="3"/><path d="M8 13 h34" stroke="#9fd4ea" stroke-width="2"/></symbol>
 <symbol id="projecteur" viewBox="0 0 80 50">
  <rect x="4" y="12" width="56" height="30" rx="5" fill="#ddd" stroke="{K}" stroke-width="3"/><circle cx="60" cy="27" r="11" fill="#9fd4ea" stroke="{K}" stroke-width="3"/><path d="M18 42 L12 50 M46 42 L52 50" stroke="{K}" stroke-width="3"/></symbol>
 <symbol id="calc" viewBox="0 0 90 120">
  <rect x="4" y="4" width="82" height="112" rx="8" fill="#3a3f4a" stroke="{K}" stroke-width="4"/><rect x="12" y="12" width="66" height="26" fill="#cfe8c0" stroke="{K}" stroke-width="2"/>
  <g fill="#ddd" stroke="{K}" stroke-width="2"><rect x="12" y="46" width="18" height="14"/><rect x="36" y="46" width="18" height="14"/><rect x="60" y="46" width="18" height="14"/><rect x="12" y="66" width="18" height="14"/><rect x="36" y="66" width="18" height="14"/><rect x="60" y="66" width="18" height="14" fill="#f2b632"/><rect x="12" y="86" width="18" height="14"/><rect x="36" y="86" width="18" height="14"/><rect x="60" y="86" width="18" height="14"/></g></symbol>
 <symbol id="ecole" viewBox="0 0 80 70">
  <path d="M6 30 L40 6 L74 30 Z" fill="#c8402d" stroke="{K}" stroke-width="3" stroke-linejoin="round"/><rect x="12" y="30" width="56" height="36" fill="#f4ecd0" stroke="{K}" stroke-width="3"/><rect x="34" y="44" width="12" height="22" fill="#8a5a1d"/><path d="M40 6 L40 -6 L52 -2 L40 2" fill="#1f7a4d" stroke="{K}" stroke-width="2"/></symbol>
 <symbol id="billet" viewBox="0 0 60 30">
  <rect x="2" y="2" width="56" height="26" rx="3" fill="#bfe3b0" stroke="{K}" stroke-width="2.5"/><circle cx="30" cy="15" r="7" fill="none" stroke="{K}" stroke-width="2"/><text x="30" y="19" text-anchor="middle" font-size="10" font-family="sans-serif" font-weight="700">$</text></symbol>
 <symbol id="carte" viewBox="0 0 40 26">
  <rect x="2" y="2" width="36" height="22" rx="3" fill="#fff" stroke="{K}" stroke-width="2.5"/><path d="M8 10 h24 M8 16 h16" stroke="#6b6458" stroke-width="2.5"/></symbol>
 <symbol id="acte" viewBox="0 0 60 76">
  <rect x="4" y="4" width="52" height="68" fill="#fffbe6" stroke="{K}" stroke-width="3"/><text x="30" y="22" text-anchor="middle" font-size="8" font-family="sans-serif" font-weight="800">ACTE DE</text><text x="30" y="31" text-anchor="middle" font-size="8" font-family="sans-serif" font-weight="800">NAISSANCE</text><text x="30" y="52" text-anchor="middle" font-size="14" font-family="sans-serif" font-weight="800" fill="#c8402d">2000</text><circle cx="44" cy="62" r="6" fill="none" stroke="#2d5bb8" stroke-width="2"/></symbol>
</defs></svg>'''

T = lambda x,y,s,txt,fill=K,anchor='middle',w='700',fam='IBM Plex Sans Condensed, Arial Narrow, sans-serif',extra='': f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{s}" font-family="{fam}" font-weight="{w}" fill="{fill}" {extra}>{E(txt)}</text>'

BAR_WALL = '<rect width="400" height="240" fill="#f3c98b"/><rect y="0" width="400" height="16" fill="#c8402d"/><rect x="250" y="34" width="130" height="10" fill="#8a5a1d"/><g>' + ''.join(f'<rect x="{258+i*16}" y="12" width="9" height="22" rx="3" fill="{c}" stroke="#1b1712" stroke-width="1.5"/>' for i,c in enumerate(['#1f7a4d','#8a5a1d','#1f7a4d','#c8402d','#8a5a1d','#1f7a4d','#2d3e63'])) + '</g><rect y="196" width="400" height="44" fill="#8a5a1d"/><path d="M0 196 L400 196" stroke="#1b1712" stroke-width="3"/>'
BG = {
 'collines': '<rect width="400" height="240" fill="#fbe2b0"/><circle cx="330" cy="54" r="26" fill="#f7b84a"/><path d="M0 150 Q70 90 150 140 T300 120 T400 130 L400 240 L0 240Z" fill="#5c9e5a"/><path d="M0 175 Q100 150 200 178 T400 170 L400 240 L0 240Z" fill="#3f7f45"/><path d="M200 240 Q240 200 300 196 T400 186" stroke="#7fc3e0" stroke-width="12" fill="none"/>',
 'coupe': '<rect width="400" height="240" fill="#bfe3f0"/><rect y="44" width="400" height="196" fill="#b5532f"/><rect y="44" width="400" height="12" fill="#3f8f4f"/><path d="M0 110 Q120 96 200 120 T400 110" stroke="#8c3b20" stroke-width="3" fill="none"/><path d="M0 170 Q120 156 200 180 T400 170" stroke="#8c3b20" stroke-width="3" fill="none"/>',
 'chambre': '<rect width="400" height="240" fill="#e7dccb"/><rect x="250" y="30" width="110" height="70" fill="#bfe3f0" stroke="#1b1712" stroke-width="3"/><path d="M305 30 v70 M250 65 h110" stroke="#1b1712" stroke-width="3"/><rect y="176" width="400" height="64" fill="#a07a50"/><rect x="120" y="150" width="200" height="12" fill="#6e4b2a" stroke="#1b1712" stroke-width="2"/>',
 'ecran': '<rect width="400" height="240" fill="#2a2f3a"/><rect x="18" y="14" width="364" height="212" rx="10" fill="#f4f7fb" stroke="#1b1712" stroke-width="4"/><rect x="18" y="14" width="364" height="22" rx="10" fill="#cfd8e3"/><circle cx="34" cy="25" r="4" fill="#c8402d"/><circle cx="48" cy="25" r="4" fill="#f2b632"/><circle cx="62" cy="25" r="4" fill="#4caf7a"/>',
 'bar': BAR_WALL,
 'barenseigne': BAR_WALL + '<rect x="60" y="30" width="140" height="34" rx="6" fill="#1b1712"/>' + T(130,54,20,'LA FRAÎCHE',fill='#9fd4ea',fam='Bowlby One SC, Arial Black, sans-serif',w='400'),
 'tableau': BAR_WALL + '<rect x="20" y="22" width="360" height="150" fill="#24493a" stroke="#6e4b2a" stroke-width="8"/>',
 'rue': '<rect width="400" height="240" fill="#e88a4a"/><rect width="400" height="110" fill="#f6b46a"/><rect x="0" y="40" width="150" height="150" fill="#f3c98b" stroke="#1b1712" stroke-width="3"/><rect x="20" y="60" width="110" height="26" fill="#1b1712"/>' + T(75,79,15,'LA FRAÎCHE',fill='#9fd4ea',fam='Bowlby One SC, Arial Black, sans-serif',w='400') + '<rect x="50" y="110" width="50" height="80" fill="#8a5a1d" stroke="#1b1712" stroke-width="3"/><rect y="190" width="400" height="50" fill="#9a8f80"/><path d="M300 190 L300 70 L330 70" stroke="#1b1712" stroke-width="5" fill="none"/><circle cx="334" cy="74" r="8" fill="#fff3c4" stroke="#1b1712" stroke-width="2"/>',
 'aerien': '<rect width="400" height="240" fill="#2f6b3a"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x,y,r,c in [(30,30,24,'#3f8f4f'),(90,60,30,'#2a5e33'),(160,24,26,'#3f8f4f'),(240,70,32,'#2a5e33'),(330,30,28,'#3f8f4f'),(380,110,30,'#2a5e33'),(40,170,30,'#2a5e33'),(130,200,28,'#3f8f4f'),(300,200,34,'#2a5e33'),(220,150,22,'#3f8f4f')]) + '<path d="M0 230 Q80 180 150 150 T260 100 T400 40" stroke="#b5532f" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M150 150 Q170 190 230 230" stroke="#b5532f" stroke-width="8" fill="none"/><g fill="#e8c78f" stroke="#1b1712" stroke-width="2"><rect x="10" y="200" width="16" height="12"/><rect x="30" y="208" width="14" height="10"/></g>',
 'titre': '<rect width="400" height="240" fill="#f7b84a"/><rect y="120" width="400" height="120" fill="#b5532f"/><rect y="120" width="400" height="12" fill="#3f8f4f"/><path d="M0 190 Q120 176 200 196 T400 186" stroke="#8c3b20" stroke-width="3" fill="none"/>',
 'ciel': '<rect width="400" height="240" fill="#cfe7f5"/><path d="M40 70 q20 -20 40 0 q20 -14 36 4 q-38 10 -76 -4z" fill="#fff"/><path d="M280 40 q20 -20 40 0 q20 -14 36 4 q-38 10 -76 -4z" fill="#fff"/><rect y="200" width="400" height="40" fill="#e8d7a8"/>',
 'carte': '<rect width="400" height="240" fill="#f4ecd0"/><path d="M0 0 L400 0 L400 240 L0 240Z" fill="url(#dots)"/><rect x="10" y="10" width="380" height="220" fill="none" stroke="#8a5a1d" stroke-width="3" stroke-dasharray="8 6"/>',
 'route': '<rect width="400" height="240" fill="#c9a77a"/><rect width="400" height="110" fill="#d9c4a6"/><path d="M0 120 Q70 100 130 120 T260 110 T400 118 L400 240 L0 240Z" fill="#4f7a4a"/><path d="M180 240 Q200 170 240 140 T300 112" stroke="#b5532f" stroke-width="26" fill="none"/><rect x="268" y="70" width="114" height="26" fill="#fff" stroke="#1b1712" stroke-width="3"/><path d="M325 96 L325 130" stroke="#1b1712" stroke-width="4"/>' + T(325,88,12,'BÉTARÉ-OYA →'),
}
def use(sym, x, y, w, h, flip=False):
    t = f' transform="translate({2*x+w} 0) scale(-1 1)"' if flip else ''
    return f'<use href="#{sym}" x="{x}" y="{y}" width="{w}" height="{h}"{t}/>'
P = {  # personnages : (symbole, largeur, hauteur)
 'aicha':(70,120),'boris':(76,124),'fifi':(70,118),'mballa':(72,122),'chantal':(72,126),'junior':(66,112),
 'glacon':(72,122),'inspecteur':(70,120),'passe':(72,128),'sagefemme':(72,122),'pere':(70,120)}
def ch(name, x, flip=False, y=None, s=1.0):
    w,h = P[name]; w*=s; h*=s
    if y is None: y = 236-h
    return use(name, x, y, w, h, flip)

SPK = {'AÏCHA':'#e0672e','BORIS':'#2f5fa8','FIFI':'#7b3f8c','TONTON MBALLA':'#8a5a1d','MAMI CHANTAL':'#c8402d','JUNIOR':'#1f7a4d',
       'PATER GLAÇON':'#2d6f8a','INSPECTEUR DOUBLE-COPIE':'#4a453d','M. PASSE-PARTOUT':'#5b2a7a','M. CONGÉLATEUR':'#2d6f8a','SAGE-FEMME':'#2d7f86','PÈRE':'#1f7a4d','NARRATEUR':'#6b6458'}
def q(who, txt): return f'<b class="qui" style="color:{SPK[who]}">{E(who)}</b> {txt}'
def sup(*n): return ''.join(f'<a class="ref" href="#src{i}">[{i}]</a>' for i in n)

def panel(bg, art, caption, bubbles, wide=False):
    lab = re.sub(r'<[^>]+>','', caption or bubbles[0][4]); lab = re.sub(r'\[\d+\]','',lab)
    svg = f'<svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{E(lab)}">{BG[bg]}{"".join(art)}<rect width="400" height="240" fill="url(#dots)"/></svg>'
    b = ''.join(f'<p class="bulle {k}" style="left:{x}%;top:{y}%;max-width:{w}%">{t}</p>' for (k,x,y,w,t) in bubbles)
    cap = f'<p class="recit">{caption}</p>' if caption else ''
    return f'<figure class="case{" large" if wide else ""}">{cap}<div class="scene">{svg}{b}</div></figure>'

PL = []
def section(titre, sous):
    PL.append(f'<div class="partie"><span>{E(sous)}</span><h2>{E(titre)}</h2></div>')
def planche(num, titre, cases, transition, source=None, tag=None):
    t = f'<span class="tag">{E(tag)}</span>' if tag else ''
    src = f'<p class="bandeau"><b>Source :</b> {source}</p>' if source else ''
    PL.append(f'<section class="planche" id="planche-{num:02d}"><header class="ph"><span class="pn">Planche {num:02d}</span><h3>{E(titre)}</h3>{t}</header><div class="grille">{"".join(cases)}</div>{src}<p class="transition">{E(transition)}</p></section>')
def fiche(titre, fait, doute, question):
    PL.append(f'<aside class="fiche"><h3>Fiche vérité · {E(titre)}</h3><dl><div class="f1"><dt>Le fait</dt><dd>{fait}</dd></div><div class="f2"><dt>Le doute</dt><dd>{doute}</dd></div><div class="f3"><dt>La question</dt><dd>{question}</dd></div></dl></aside>')

# ====================== PROLOGUE
section("Ceux de l’an 2000", "Prologue · planches 01 à 06")

planche(1, "2000 : un certificat de naissance", [
 panel('collines', [ch('sagefemme',120), ch('pere',230,flip=True)], "An 2000. Quelque part au Cameroun, un matin.",
  [('',3,5,46,q('SAGE-FEMME',"Bienvenue au monde, petite Aïcha !")), ('',56,5,40,q('PÈRE',"Son avenir sera en or !"))]),
 panel('coupe', [use('pepite',150,120,100,84), T(388,232,10,'* Illustration symbolique','#fff3c4','end','600')], q('NARRATEUR',"Le pays n’est pas seulement au-dessus de nos têtes."), []),
 panel('chambre', [use('ordi',150,88,120,90), use('ventilo',300,120,50,76), ch('aicha',40), T(325,116,10,'(ne tourne pas)','#6b6458')], "2026. Aïcha a 26 ans.",
  [('',3,5,60,q('AÏCHA',"En 2000, on m’a promis l’or. En 2026, j’ai surtout la facture du courant."))]),
 panel('ecran', ['<rect x="34" y="46" width="160" height="20" rx="10" fill="#fff" stroke="#2d5bb8" stroke-width="2"/>', T(42,60,11,'Cameroun exportations or','#2d5bb8','start','600'),
   '<rect x="206" y="46" width="164" height="20" rx="10" fill="#fff" stroke="#b8860b" stroke-width="2"/>', T(214,60,11,'EAU importations or Cameroun','#8a6400','start','600'),
   '<rect x="40" y="80" width="150" height="120" fill="#e3eeff" stroke="#2d5bb8" stroke-width="2"/><rect x="210" y="80" width="150" height="120" fill="#fff3d0" stroke="#b8860b" stroke-width="2"/>',
   T(115,100,12,'DÉCLARÉ PAR LE CAMEROUN','#2d5bb8'), T(285,100,12,'DÉCLARÉ PAR LES EAU','#8a6400'), T(115,150,30,'…','#2d5bb8'), T(285,150,30,'…','#8a6400')], None,
  [('',22,74,56,q('AÏCHA',"Tiens… pourquoi ces deux colonnes ne se parlent-elles pas ?"))]),
], "Un mystère, deux livres de comptes.")

planche(2, "LA FRAÎCHE : le bar où les chiffres se disputent", [
 panel('barenseigne', [ch('glacon',60), use('congel',230,130,150,110)], "Nkoagne, fin d’après-midi.",
  [('',52,4,45,q('PATER GLAÇON',"Chez moi, même la bière a obtenu son indépendance thermique.")), ('pense',58,38,34,"(M. Congélateur boude.)")]),
 panel('bar', [ch('boris',70), use('ventilo',170,150,50,76), '<rect x="160" y="210" width="34" height="22" rx="3" fill="#333" stroke="#1b1712" stroke-width="2"/>', ch('junior',290,flip=True)], None,
  [('',46,4,50,q('JUNIOR',"Tu répares le ventilateur ou tu le présentes aux élections ?")), ('',3,4,40,q('BORIS',"Je lui cherche un mandat de cinq ans renouvelable."))]),
 panel('bar', [ch('aicha',40), '<rect x="96" y="150" width="34" height="44" fill="#fff" stroke="#1b1712" stroke-width="2" transform="rotate(-8 113 172)"/>', ch('chantal',220,flip=True), ch('mballa',305,flip=True)], None,
  [('',3,4,62,q('AÏCHA',"J’ai trouvé un mystère : un pays déclare des kilos ; un autre, des tonnes."))]),
 panel('bar', [ch('mballa',150), '<rect x="40" y="150" width="70" height="56" fill="#fff" stroke="#1b1712" stroke-width="2"/><path d="M110 200 L210 200" stroke="#f2b632" stroke-width="6"/>'], None,
  [('',3,4,66,q('TONTON MBALLA',"Attendez ! Avant de crier au scandale, on mesure la longueur des tonnes."))]),
], "Première question : qui a raison, la feuille ou le mètre ?")

planche(3, "Le tableau qui n’osait pas se regarder", [
 panel('tableau', ['<path d="M200 40 L200 160" stroke="#fff" stroke-width="3"/>', T(110,62,13,'EXPORTÉ PAR','#9cc4ff'), T(110,80,13,'LE CAMEROUN','#9cc4ff'), T(290,62,13,'IMPORTÉ PAR','#ffd770'), T(290,80,13,'LES EAU','#ffd770'), ch('aicha',300,s=.9)], None,
  [('',3,64,60,q('AÏCHA',"Une même marchandise laisse normalement des traces dans les deux pays."))]),
 panel('tableau', ['<path d="M200 40 L200 160" stroke="#fff" stroke-width="3"/>', use('sac',90,120,28,34), use('sac',230,60,110,126), ch('boris',10,s=.9)], None,
  [('',30,4,64,q('BORIS',"Quand ma mère dit « un sachet » et ma tante « un camion », je vérifie le magasin."))]),
 panel('tableau', [T(200,112,26,'VOL','#fff','middle','700',extra='text-decoration="line-through"'), '<path d="M160 104 L240 104" stroke="#c8402d" stroke-width="5"/>', T(200,146,20,'ÉCART STATISTIQUE','#ffd770'), ch('fifi',300,flip=True,s=.9)], None,
  [('',3,4,56,q('FIFI',"On n’a pas encore prouvé le vol. On a prouvé qu’il faut poser une question."))]),
 panel('bar', [use('congelouvert',120,96,170,140)], None,
  [('',3,4,62,q('M. CONGÉLATEUR',"Pour une fois, mettez les faits au frais. Les rumeurs, elles, tournent trop vite."))]),
], "Un écart, c’est une question. Pas encore une réponse.")

planche(4, "2017 : quatre kilos, dix tonnes", [
 panel('bar', ['<rect x="30" y="70" width="230" height="120" fill="#fff" stroke="#1b1712" stroke-width="3"/>', T(145,92,11,'INTERPOL · Illegal Gold Mining in Central Africa (2021)','#6b6458'), ch('fifi',300,flip=True)], None,
  [('note cm',9,40,52,"Cameroun → EAU : <b>4 kg</b> déclarés (2017)"+sup(1)), ('note imp',9,60,52,"EAU ← Cameroun : <b>10,9 t</b> déclarées (2017)"+sup(1,3)),
   ('',3,4,74,q('FIFI',"Ça, c’est dans un rapport publié par INTERPOL, pas dans la conversation du quartier."))]),
 panel('bar', [use('balance4',30,150,80,80), use('camion',150,120,250,124), ch('boris',90,s=.8)], None,
  [('',3,4,66,q('BORIS',"Donc le camion n’a pas lu la même déclaration que la balance !"))]),
 panel('bar', [ch('inspecteur',60), '<g transform="rotate(-10 260 150)"><rect x="170" y="110" width="200" height="70" fill="none" stroke="#c8402d" stroke-width="5"/></g>', T(268,140,16,'DOSSIER À','#c8402d',extra='transform="rotate(-10 260 150)"'), T(268,164,16,'RÉCONCILIER','#c8402d',extra='transform="rotate(-10 260 150)"'), '<rect x="190" y="196" width="150" height="24" fill="#fff" stroke="#c8402d" stroke-width="3" transform="rotate(4 265 208)"/>', T(265,213,12,'VU, MAIS PAS VÉRIFIÉ','#c8402d',extra='transform="rotate(4 265 208)"')], None,
  [('',3,4,64,q('INSPECTEUR DOUBLE-COPIE',"Moi, quand deux chiffres se battent, je convoque le papier carbone !"))]),
 panel('carte', ['<path d="M60 200 Q150 150 300 80" stroke="#2d5bb8" stroke-width="4" stroke-dasharray="8 6" fill="none"/><path d="M370 210 Q260 190 300 80" stroke="#7b3f8c" stroke-width="4" stroke-dasharray="8 6" fill="none"/>', '<circle cx="60" cy="200" r="7" fill="#2d5bb8"/><circle cx="370" cy="210" r="7" fill="#7b3f8c"/><circle cx="300" cy="80" r="9" fill="#f2b632" stroke="#1b1712" stroke-width="2"/>', T(60,224,11,'mine au Cameroun','#2d5bb8'), T(340,232,11,'pays voisin ?','#7b3f8c'), T(300,66,11,'frontière','#8a6400'), ch('fifi',150,s=.75)], None,
  [('',3,4,62,q('FIFI',"Attention : « en provenance du Cameroun » ne prouve pas que tout cet or a été extrait au Cameroun.")),
   ('note hyp',52,40,44,"Hypothèse examinée par INTERPOL : de l’or de pays voisins transiterait par le Cameroun. Non démontré cargaison par cargaison."+sup(1))]),
], "Deux colonnes, deux pays… et peut-être plus de deux routes.",
 source="INTERPOL, <i>Illegal Gold Mining in Central Africa</i> (2021), série 2008–2018 "+sup(1)+" ; UN Comtrade : 10 907 kg déclarés par les EAU en 2017 "+sup(3)+".", tag="Avant-goût du chapitre 2")

planche(5, "La génération qui veut le reçu", [
 panel('tableau', [use('acte',40,40,60,76), '<path d="M120 80 L330 80" stroke="#fff" stroke-width="4"/><path d="M330 80 l-12 -8 v16 z" fill="#fff"/>', T(130,104,18,'2000','#ffd770'), T(320,104,18,'2026','#ffd770'), ch('aicha',170,s=.85)], None,
  [('',30,6,66,q('AÏCHA',"J’ai 26 ans. On ne peut pas nous demander de patienter encore vingt-six ans pour comprendre nos comptes."))]),
 panel('bar', [ch('junior',60), use('telephone',140,130,26,46), ch('fifi',270,flip=True)], None,
  [('',3,4,46,q('JUNIOR',"Je peux chercher les données moi-même ?")), ('',52,4,46,q('FIFI',"Oui. Et noter le code, l’année, la source et les unités."))]),
 panel('bar', ['<rect x="150" y="64" width="232" height="70" fill="#d9a066" stroke="#1b1712" stroke-width="4"/><path d="M266 134 L266 200" stroke="#1b1712" stroke-width="7"/>', T(266,94,15,'QUESTION = CITATION','#1f5f3a'), T(266,118,15,'+ DATE + PÉRIMÈTRE','#1f5f3a'), ch('chantal',40)], None,
  [('note civ',30,4,66,q('MAMI CHANTAL',"La vérité ne doit pas avoir besoin d’un parrain. Elle a besoin d’une référence."))]),
 panel('bar', [ch('aicha',20,s=.85), ch('boris',90,s=.85), '<rect x="170" y="166" width="60" height="44" fill="#f2b632" stroke="#1b1712" stroke-width="3"/>', ch('fifi',240,s=.85,flip=True), ch('mballa',310,s=.85,flip=True)], None,
  [('',30,4,66,q('TONTON MBALLA',"Mais je garde mon mètre. On ne sait jamais : le mensonge est peut-être très long."))]),
], "Règle du bar : pas de chiffre sans sa carte d’identité.")

planche(6, "Le pays sous nos pieds", [
 panel('aerien', [], q('NARRATEUR',"Ils ne partent pas chercher un coupable. Ils partent chercher la route d’un chiffre."), [], wide=True),
 panel('rue', [ch('passe',200), use('carte',290,150,40,26), use('carte',300,164,40,26)], None,
  [('note hyp',62,86,30,"(Personnage fictif)"), ('',44,4,54,q('M. PASSE-PARTOUT',"Ils ont découvert les colonnes ? Évitez qu’ils découvrent les factures…"))]),
 panel('bar', [ch('aicha',10,s=.85), ch('fifi',90,s=.85), ch('boris',190,s=.85), use('lampe',255,180,30,42), ch('junior',300,s=.85,flip=True)], None,
  [('',2,4,36,q('AÏCHA',"Première étape : les registres. Ensuite, le terrain.")), ('',39,4,28,q('JUNIOR',"Et tes lunettes, Boris ?")), ('',69,4,29,q('BORIS',"Sur le front. La sécurité d’abord !"))]),
 panel('titre', [use('pepite',90,140,80,66), T(200,78,40,'LE PAYS SOUS','#1b1712',fam='Bowlby One SC, Arial Black, sans-serif',w='400'), T(200,116,40,'NOS PIEDS','#1b1712',fam='Bowlby One SC, Arial Black, sans-serif',w='400')], None,
  [('',50,62,40,q('M. CONGÉLATEUR',"(voix off) Si l’or change de pays, qu’on nous montre son passeport !"))], wide=True),
], "Fin du prologue.")

fiche("Prologue",
 "En 2017, les Émirats arabes unis déclarent avoir importé <b>10 907 kg</b> d’or (SH 7108) « en provenance du Cameroun », pour 382 M USD "+sup(3)+". INTERPOL relève <b>4 kg</b> déclarés côté camerounais "+sup(1)+".",
 "« Provenance » ne veut pas dire « origine » : une partie de cet or a pu être extraite dans des pays voisins puis transiter. Aucun chiffre ne dit, à lui seul, qui a fraudé.",
 "Quelles exportations d’or le Cameroun a-t-il enregistrées en 2017, et vers quels pays ? Cherchez « Cameroon, 7108, 2017, Exports » sur WITS ou UN Comtrade.")

# ====================== CHAPITRE 1
section("Le comptoir des deux colonnes", "Chapitre 1 · planches 07 à 10 (suite : planche 11)")

planche(7, "Mode d’emploi d’un chiffre", [
 panel('bar', ['<rect x="150" y="30" width="230" height="110" fill="#fff" stroke="#1b1712" stroke-width="3"/>', T(265,98,40,'SH 7108','#8a6400',fam='Bowlby One SC, Arial Black, sans-serif',w='400'), use('projecteur',150,170,80,50), ch('fifi',40)], None,
  [('',30,62,66,q('FIFI',"Dans les douanes du monde entier, l’or brut, en barres, en poudre ou mi-ouvré porte un code : <b>7108</b>."))]),
 panel('bar', [ch('boris',60), '<rect x="160" y="110" width="60" height="80" fill="#f2d65c" stroke="#1b1712" stroke-width="3" transform="rotate(8 190 150)"/>', T(190,150,11,'CODE DE','#1b1712',extra='transform="rotate(8 190 150)"'), T(190,164,11,'LA ROUTE','#1b1712',extra='transform="rotate(8 190 150)"')], None,
  [('',40,4,56,q('BORIS',"Moi aussi j’ai un code. Avec lui, mes motos ne franchissent même pas le carrefour."))]),
 panel('tableau', [T(40,58,14,'REPORTER = le pays qui déclare','#fff','start'), T(40,84,14,'PARTNER = le pays associé','#fff','start'), T(40,110,14,'FLOW = Import / Export','#fff','start'), T(40,136,14,'YEAR = l’année','#fff','start'), ch('fifi',310,s=.8,flip=True)], None,
  [('',3,74,70,q('FIFI',"Si vous inversez « qui parle » et « de qui on parle », vous fabriquez une révélation avec une faute de tableur."))]),
 panel('bar', [use('projecteur',220,150,110,68), '<rect x="250" y="130" width="60" height="22" fill="#1f7a4d" stroke="#1b1712" stroke-width="2" transform="rotate(-6 280 141)"/>', T(280,146,12,'SOURCE','#fff',extra='transform="rotate(-6 280 141)"'), ch('chantal',60)], None,
  [('',30,4,66,q('MAMI CHANTAL',"Chez nous, même le projecteur n’a pas le droit de parler sans justificatif."))]),
], "Maintenant qu’on sait lire le tableau, on peut l’ouvrir.")

planche(8, "Les chiffres de 2023 entrent au bar", [
 panel('ecran', [T(200,58,12,'WITS / UN Comtrade · SH 7108 · 2023','#6b6458')], None,
  [('note cm',8,30,84,"Cameroun → EAU (export déclaré) : <b>20 kg</b>"+sup(2)), ('note imp',8,46,84,"EAU ← Cameroun (import déclaré) : <b>14 048 kg</b>"+sup(2)),
   ('',8,66,84,q('AÏCHA',"Même produit, même année, mêmes pays : 20 kilos d’un côté, 14 048 de l’autre."))]),
 panel('bar', [ch('mballa',150), '<path d="M220 160 L300 160" stroke="#f2b632" stroke-width="6"/>'], None,
  [('',3,4,66,q('TONTON MBALLA',"D’accord. Pour les kilogrammes, j’ai compris. Le mètre est innocent."))]),
 panel('bar', [use('calc',40,80,110,146), '<rect x="160" y="88" width="230" height="56" fill="#cfe8c0" stroke="#1b1712" stroke-width="3"/>', T(275,125,24,'14 048 ÷ 20 = 702,4','#1b1712'), ch('junior',322,s=.75,flip=True)], None,
  [('',33,62,44,q('JUNIOR',"Sept cent deux fois ? Le chiffre a pris l’avion en classe affaires ?"))]),
 panel('tableau', ['<rect x="40" y="40" width="150" height="40" fill="none" stroke="#ffd770" stroke-width="3"/>', T(115,67,18,'BILATÉRAL','#ffd770'), ch('fifi',310,s=.85,flip=True)], None,
  [('',3,40,70,q('FIFI',"C’est un écart de déclarations, pas 702 crimes prouvés.")),
   ('note imp',3,62,74,"Tous pays déclarants, 2023 : EAU 14 048 kg, Rwanda 3 060 kg, Ouganda 1 145 kg"+sup(3)+". Les « ≈ 15 t » de l’ITIE "+sup(4)+" correspondent à EAU + Ouganda.")]),
], "Et ces kilos, combien valent-ils ?",
 source="WITS / UN Comtrade 2023, SH 7108, importations des EAU depuis le Cameroun et exportations du Cameroun vers les EAU "+sup(2)+" ; UN Comtrade, tous déclarants "+sup(3)+" ; ITIE (2026) "+sup(4)+".", tag="Avant-goût du chapitre 3")

planche(9, "Le milliard qui n’était pas un budget", [
 panel('ecran', [T(200,58,12,'EAU ← Cameroun · SH 7108 · 2023 · valeur CIF','#6b6458'), T(200,120,38,'879,72 M USD','#8a6400',fam='Bowlby One SC, Arial Black, sans-serif',w='400'), T(200,150,14,'≈ 534 milliards FCFA au taux moyen 2023','#6b6458','middle','600')], None,
  [('',8,70,84,q('AÏCHA',"La valeur commerciale déclarée par les Émirats approche 880 millions de dollars."+sup(2,5)))]),
 panel('ciel', [use('ecole',150,120,70,62), use('ecole',220,100,60,54), use('ecole',280,128,56,48), use('billet',150,60,50,26), use('billet',250,50,50,26), use('billet',320,72,50,26), ch('boris',30)], "Fantaisie de Boris, pas calcul budgétaire.",
  [('pense',40,4,56,q('BORIS',"Avec ça, je construis douze universités et trois autoroutes !"))]),
 panel('tableau', ['<g fill="none" stroke="#fff" stroke-width="3"><rect x="34" y="70" width="100" height="56"/><rect x="150" y="70" width="100" height="56"/><rect x="266" y="70" width="100" height="56"/></g><path d="M134 98 h16 M250 98 h16" stroke="#fff" stroke-width="3"/>', T(84,94,12,'Valeur de la','#fff'), T(84,110,12,'marchandise','#fff'), T(200,94,12,'Taxes','#fff'), T(200,110,12,'dues','#fff'), T(316,94,12,'Recettes','#fff'), T(316,110,12,'versées','#fff')], None,
  [('',3,4,94,q('FIFI',"Stop. La valeur vendue n’est pas la recette fiscale perdue. Il faut les contrats, les taxes, les origines et les paiements.")),
   ('note',3,66,94,"CIF : valeur à l’arrivée, assurance et fret compris. Le Cameroun déclare ses exportations en FOB, valeur au départ.")]),
 panel('bar', [ch('chantal',40), ch('boris',290,flip=True,s=.9)], None,
  [('',28,4,60,q('MAMI CHANTAL',"Quand tu confonds chiffre d’affaires et salaire, même ton comptable démissionne."))]),
], "Une valeur n’est pas une recette. Reste à savoir d’où vient l’or.",
 source="WITS / UN Comtrade 2023, valeur CIF des importations des EAU depuis le Cameroun : 879 721,73 milliers USD "+sup(2)+" ; conversion au taux annuel moyen de la Banque mondiale "+sup(5)+".", tag="Avant-goût du chapitre 3")

steps = [('mine ?',50,'#2d5bb8'),('acheteur ?',125,'#7b3f8c'),('transit ?',200,'#7b3f8c'),('raffinerie ?',275,'#7b3f8c'),('pays déclarant',350,'#8a6400')]
chain = ''.join(f'<circle cx="{x}" cy="150" r="22" fill="#fff" stroke="{c}" stroke-width="4"/>'+T(x,190,11,lbl,c) for lbl,x,c in steps) + ''.join(f'<path d="M{x+24} 150 L{x+51} 150" stroke="#1b1712" stroke-width="3"/><path d="M{x+51} 150 l-8 -5 v10z" fill="#1b1712"/>' for _,x,_ in steps[:-1])
planche(10, "Qui a rempli le formulaire ?", [
 panel('carte', [chain], None,
  [('',3,6,90,q('AÏCHA',"Le registre est notre point de départ. Maintenant, il faut reconstruire la chaîne réelle."))]),
 panel('rue', [ch('passe',160), '<g transform="rotate(-10 270 140)"><rect x="236" y="120" width="80" height="40" rx="4" fill="#fff" stroke="#1b1712" stroke-width="3"/></g>', T(276,146,11,'Pays d’origine','#2d5bb8',extra='transform="rotate(-10 270 140)"'), '<g transform="rotate(8 330 190)"><rect x="278" y="172" width="118" height="40" rx="4" fill="#fff" stroke="#1b1712" stroke-width="3"/></g>', T(339,198,11,'Pays de provenance','#8a6400',extra='transform="rotate(8 330 190)"')], None,
  [('',3,4,60,q('M. PASSE-PARTOUT',"Avec moi, chaque pays a sa carte… surtout quand personne ne demande laquelle."))]),
 panel('bar', [ch('fifi',40), '<rect x="120" y="150" width="136" height="64" fill="#fff" stroke="#1b1712" stroke-width="3"/>', T(188,178,12,'NE PAS CONCLURE','#c8402d'), T(188,198,12,'SANS PREUVE','#c8402d')], None,
  [('',30,4,66,q('FIFI',"Une quantité peut voyager par plusieurs pays. Ne mélangeons pas extraction et passage de frontière.")),
   ('note imp',66,42,32,"2023 : le Rwanda et l’Ouganda déclarent aussi 4,2 t reçues du Cameroun"+sup(3)+".")]),
 panel('route', [ch('aicha',90)], "Le ton change.",
  [('',3,4,62,q('AÏCHA',"Il existe un autre registre à vérifier : celui des enfants qui quittent l’école. Direction l’Est."+sup(6)))]),
], "À suivre : planche 11, puis le chapitre 2.")

fiche("Chapitre 1 (ouverture)",
 "En 2023, les EAU déclarent <b>14 048 kg</b> d’or importés du Cameroun, pour <b>879,72 M USD</b> (valeur CIF) ; le Cameroun déclare <b>20 kg</b> exportés vers les EAU "+sup(2)+". D’autres pays déclarent aussi de l’or reçu du Cameroun : Rwanda 3 060 kg, Ouganda 1 145 kg "+sup(3)+".",
 "L’ITIE parle de « plus de 15 t » "+sup(4)+" : ce total correspond à EAU + Ouganda, sans le Rwanda. C’est une question de périmètre, à préciser à chaque fois. La valeur commerciale n’est pas une perte fiscale.",
 "Quel taux de taxe le Cameroun aurait-il dû appliquer à cet or, s’il était camerounais ? Et combien a réellement été collecté en 2023 ? (Réponse au chapitre 6.)")

SOURCES = [
 (1, "INTERPOL, Project ENACT, Illegal Gold Mining in Central Africa (2021) : figure sur les importations d’or des EAU en provenance du Cameroun (2008–2018) et discussion du cas de 2017.", "https://www.interpol.int/content/download/16493/file/2021%2007%2027%20ENGLISH%20PUBLIC%20VERSION_FINAL_Illegal%20gold%20mining%20in%20Central%20Africa.pdf"),
 (2, "WITS / UN Comtrade, SH 7108, 2023 : importations des EAU depuis le Cameroun (14 048 kg ; 879 721,73 milliers USD) et exportations du Cameroun vers les EAU (20 kg ; 631,23 milliers USD).", "https://wits.worldbank.org/trade/comtrade/en/country/All/year/2023/tradeflow/Imports/partner/CMR/product/7108"),
 (3, "UN Comtrade, SH 7108, partenaire Cameroun, tous pays déclarants (extraction du 31/10/2026) : 2017, EAU 10 907 kg ; 2023, EAU 14 048,4 kg, Rwanda 3 060 kg, Ouganda 1 144,73 kg. Fichier : docs/recherche-or-cameroun/donnees_miroir_or_tous_declarants.csv (dépôt boujieka/Boujieka).", "https://comtradeplus.un.org/"),
 (4, "ITIE internationale, « Écarts dans le secteur aurifère du Cameroun » (avril 2026) : ≈ 15,2 t déclarées par les partenaires en 2023, dont plus de 90 % par les EAU. Le rapprochement avec EAU + Ouganda est une inférence des auteurs.", "https://eiti.org/fr/impact-story/ecarts-dans-le-secteur-aurifere-du-cameroun-la-contribution-des-donnees-itie-la"),
 (5, "Banque mondiale, taux de change officiel moyen annuel (PA.NUS.FCRF) : conversion des USD en FCFA.", "https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=CM"),
 (6, "UNICEF Cameroun, « Quand la ruée vers l’or vole les rêves des enfants » (12/01/2026), Mbal, commune de Bétaré-Oya : l’exploitation aurifère menace les progrès scolaires.", "https://www.unicef.org/cameroon/fr/recits/quand-la-ru%C3%A9e-vers-lor-vole-les-r%C3%AAves-des-enfants"),
]
src_html = ''.join(f'<li id="src{n}"><span class="sn">[{n}]</span> {E(t)} <a href="{u}" target="_blank" rel="noopener">{E(u.split("//")[1].split("/")[0])}</a></li>' for n,t,u in SOURCES)

CSS = '''
:root{
 --papier:#fffdf6; --encre:#1b1712; --or:#f2b632; --laterite:#b5532f; --foret:#1f7a4d; --gris:#6b6458;
 --cm:#2d5bb8; --cm-bg:#e3eeff; --imp:#b8860b; --imp-bg:#fff3d0; --hyp:#7b3f8c; --hyp-bg:#f3e8fa; --civ:#1f7a4d; --civ-bg:#e4f4ea;
 --f-titre:"Bowlby One SC", "Arial Black", sans-serif;
 --f-bulle:"Patrick Hand", "Comic Sans MS", cursive;
 --f-note:"IBM Plex Sans Condensed", "Arial Narrow", sans-serif;
 color-scheme: light;
}
*{box-sizing:border-box}
body{background:var(--papier);color:var(--encre);font-family:var(--f-note);margin:0}
.wrap{max-width:1080px;margin:0 auto;padding-block:24px 48px;padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));display:flex;flex-direction:column;gap:36px;}
.couv{border:5px solid var(--encre);background:var(--laterite);color:var(--papier);position:relative;overflow:hidden;display:grid;grid-template-columns:1.15fr .85fr;gap:16px;padding:28px;box-shadow:8px 8px 0 var(--encre);}
.couv::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 1px 1px, rgba(0,0,0,.18) 1.2px, transparent 1.4px) 0 0/9px 9px;pointer-events:none;}
.couv > div{position:relative;z-index:1;min-width:0}
.serie{font-family:var(--f-titre);font-size:15px;letter-spacing:.12em;margin:0 0 8px;color:#ffe9b0}
.hs{display:inline-block;background:var(--or);color:var(--encre);font-family:var(--f-titre);font-size:14px;letter-spacing:.08em;padding:4px 10px;border:3px solid var(--encre);transform:rotate(-2deg);}
.couv h1{font-family:var(--f-titre);font-size:clamp(34px,6.5vw,68px);line-height:.95;margin:14px 0 12px;text-wrap:balance;text-shadow:4px 4px 0 var(--encre);color:var(--or);}
.accroche{font-family:var(--f-bulle);font-size:clamp(19px,2.4vw,26px);margin:0 0 14px;line-height:1.2}
.pour{font-size:15px;max-width:54ch;line-height:1.5;margin:0;}
.couv svg{width:100%;height:auto;display:block;border:3px solid var(--encre)}
.legende{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.legende span{font-size:13px;font-weight:600;padding:3px 8px;border:2px solid var(--encre);color:var(--encre)}
.lg-cm{background:var(--cm-bg)} .lg-imp{background:var(--imp-bg)} .lg-hyp{background:var(--hyp-bg);border-style:dashed!important} .lg-civ{background:var(--civ-bg)}
.partie{border-top:6px double var(--encre);padding-top:14px}
.partie span{font-family:var(--f-note);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:13px;color:var(--laterite)}
.partie h2{font-family:var(--f-titre);font-weight:400;font-size:clamp(26px,4vw,42px);margin:4px 0 0;line-height:1}
.planche{display:flex;flex-direction:column;gap:12px;}
.ph{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:4px solid var(--encre);padding-bottom:6px;}
.pn{font-family:var(--f-titre);font-size:13px;letter-spacing:.1em;background:var(--encre);color:var(--or);padding:3px 8px;}
.ph h3{font-family:var(--f-titre);font-weight:400;font-size:clamp(20px,3vw,30px);margin:0;text-wrap:balance;}
.tag{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:2px solid var(--encre);padding:2px 6px;background:#fff}
.grille{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.case{margin:0;border:4px solid var(--encre);background:#fff;display:flex;flex-direction:column;min-width:0;box-shadow:5px 5px 0 var(--encre);}
.case.large{grid-column:1 / -1}
.case.large .scene{aspect-ratio:400/180;}
.recit{margin:0;background:var(--or);border-bottom:3px solid var(--encre);padding:7px 10px;font-weight:600;font-size:15px;line-height:1.35;}
.scene{position:relative;container-type:inline-size;aspect-ratio:400/240;max-width:100%;flex:1 0 auto;}
.scene svg{display:block;width:100%;height:100%;}
.bulle{position:absolute;margin:0;background:#fff;border:2.5px solid var(--encre);border-radius:16px;padding:.4em .65em;font-family:var(--f-bulle);font-size:clamp(12.5px,3.5cqw,21px);line-height:1.15;box-shadow:2px 2px 0 var(--encre);}
.qui{font-family:var(--f-note);font-size:.68em;letter-spacing:.06em;display:block;margin-bottom:1px}
.bulle.pense{border-style:dashed;border-radius:26px;background:#fffbe6;}
.bulle.note{border-radius:4px;background:#f6f6f2;font-family:var(--f-note);font-size:clamp(11.5px,3cqw,18px);font-weight:500;}
.bulle.cm{background:var(--cm-bg);border-color:var(--cm)} .bulle.imp{background:var(--imp-bg);border-color:var(--imp)}
.bulle.hyp{background:var(--hyp-bg);border-color:var(--hyp);border-style:dashed} .bulle.civ{background:var(--civ-bg);border-color:var(--civ)}
.ref{font-family:var(--f-note);font-size:.72em;font-weight:700;color:var(--laterite);text-decoration:none;margin-left:2px;vertical-align:super;}
.ref:hover,.ref:focus-visible{text-decoration:underline;}
a:focus-visible{outline:3px solid var(--foret);outline-offset:2px;}
.bandeau{margin:0;font-size:13px;line-height:1.45;color:var(--gris);border-left:4px solid var(--gris);padding:2px 10px;max-width:95ch}
.transition{margin:0;font-family:var(--f-bulle);font-size:19px;text-align:right;color:var(--laterite)}
.fiche{border:4px solid var(--encre);background:#fff;padding:16px 18px;box-shadow:5px 5px 0 var(--encre)}
.fiche h3{font-family:var(--f-titre);font-weight:400;font-size:20px;margin:0 0 10px}
.fiche dl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0}
.fiche dl > div{padding:10px 12px;border:2px solid var(--encre)}
.fiche dt{font-family:var(--f-titre);font-size:14px;letter-spacing:.05em;margin-bottom:4px}
.fiche dd{margin:0;font-size:14.5px;line-height:1.5}
.f1{background:var(--imp-bg)} .f2{background:var(--hyp-bg)} .f3{background:var(--civ-bg)}
.avert{border:3px dashed var(--encre);padding:14px 18px;background:#fff;font-size:15px;line-height:1.55;max-width:85ch;}
.avert strong{font-family:var(--f-titre);font-weight:400;letter-spacing:.04em;}
.sources h2{font-family:var(--f-titre);font-weight:400;font-size:clamp(20px,3vw,28px);margin:0 0 10px;}
.sources ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px;}
.sources li{font-size:14px;line-height:1.5;max-width:95ch;}
.sources .sn{font-weight:700;color:var(--laterite);margin-right:4px;}
.sources a{color:var(--foret);word-break:break-word;}
@media (max-width:720px){
 .grille{grid-template-columns:1fr;}
 .couv{grid-template-columns:1fr;padding:20px;}
 .fiche dl{grid-template-columns:1fr}
 .bulle{font-size:max(12px,3.4cqw);}
}
'''

COVER = f'<svg viewBox="0 0 400 300" role="img" aria-label="Aïcha, Boris, Fifi, Tonton Mballa, Mami Chantal et Junior autour d’une pépite d’or">{BG["titre"].replace("240","300")}{use("aicha",20,150,74,128)}{use("boris",90,150,78,128)}{use("fifi",160,156,70,120)}{use("mballa",222,152,74,126)}{use("chantal",284,146,74,130)}{use("pepite",160,60,90,74)}{use("junior",340,170,56,100)}</svg>'

page = f'''<title>Le pays sous nos pieds</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bowlby+One+SC&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&family=Patrick+Hand&display=swap">
<style>{CSS}</style>
{SYMBOLS}
<main class="wrap">
 <header class="couv">
  <div>
   <p class="serie">COURANT CONTINENTAL</p>
   <span class="hs">HORS-SÉRIE</span>
   <h1>Le pays sous nos pieds</h1>
   <p class="accroche">« L’or circule. Les chiffres se contredisent. Qui tient le registre de notre avenir ? »</p>
   <p class="pour">Planches 01 à 10 : le prologue et l’ouverture du chapitre 1. Comédie d’enquête citoyenne pour la génération née en 2000. Personnages inventés ; chaque chiffre renvoie à sa source, numérotée entre crochets.</p>
   <div class="legende" aria-label="Code couleur des encadrés"><span class="lg-cm">Bleu : déclaré par le Cameroun</span><span class="lg-imp">Or : déclaré par le pays importateur</span><span class="lg-hyp">Violet : hypothèse non vérifiée</span><span class="lg-civ">Vert : action citoyenne</span></div>
  </div>
  <div>{COVER}</div>
 </header>
 {"".join(PL)}
 <aside class="avert"><strong>Avertissement.</strong> Fiction documentée. Aïcha, Boris, Fifi, Tonton Mballa, Mami Chantal, Junior, Pater Glaçon, l’Inspecteur Double-Copie, M. Passe-Partout et M. Congélateur sont des personnages inventés ; aucun ne représente une personne ou une institution réelle. Les statistiques « miroir » montrent un écart entre les déclarations au départ et à l’arrivée. Elles ne prouvent ni l’origine de chaque gramme, ni la responsabilité d’une personne. Les données 2024 des EAU ont été retirées d’UN Comtrade pour vérification (SWISSAID, 04/11/2025) : elles ne sont pas utilisées ici. Données arrêtées au 31 octobre 2026.</aside>
 <section class="sources" id="sources"><h2>Sources</h2><ol>{src_html}</ol></section>
</main>'''
open(OUT,'w').write(page)
print(len(page))
