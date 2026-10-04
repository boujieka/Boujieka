/* Tableau de bord pays de TasetyGrid.
   Deux familles de chiffres, toujours séparées à l'écran :
   - RÉELS : population estimée et comptes d'infrastructures issus de Natural Earth (données générales, non exhaustives) ;
   - FICTIFS : résultats par secteur et par produit recensé. Aucun recensement n'existe encore : ces valeurs
     sont tirées d'une graine déterminée par le pays et ne servent qu'à montrer le format du tableau de bord. */
(function (root) {
  "use strict";

  var T = {
    fr: {
      reel: "Données réelles · Natural Earth",
      reelNote: "Données générales à l'échelle 1:10 000 000, non exhaustives. Ce n'est pas un recensement.",
      pop: "Population estimée", airports: "Aéroports", ports: "Ports", rail: "Voies ferrées", roads: "Routes principales",
      cities: "Villes", sur: "dont %n sur la carte", km: "km", na: "n. d.",
      fictif: "Exemple fictif", fictifTitre: "Résultats du recensement (format de démonstration)",
      fictifNote: "Ces valeurs sont générées pour illustrer le format. Elles ne décrivent aucun pays réel.",
      parSecteur: "Par secteur", parProduit: "Par produit recensé",
      recenses: "éléments recensés", verifie: "vérifié", estime: "estimé", declare: "déclaré",
      deficit: "Déficit", faible: "faible", moyen: "moyen", fort: "fort",
      secteurs: ["Santé", "Éducation", "Eau", "Énergie", "Routes", "Télécoms", "Foncier", "Ressources"],
      produits: ["Écoles", "Centres de santé", "Forages et points d'eau", "Postes électriques", "Tronçons de piste", "Antennes télécoms", "Parcelles attestées", "Sites de ressources"],
      legende: "Barre : part vérifiée, estimée ou déclarée"
    },
    en: {
      reel: "Real data · Natural Earth",
      reelNote: "General data at 1:10,000,000 scale, not exhaustive. This is not a census.",
      pop: "Estimated population", airports: "Airports", ports: "Ports", rail: "Railways", roads: "Major roads",
      cities: "Cities", sur: "%n on the map", km: "km", na: "n/a",
      fictif: "Fictional example", fictifTitre: "Census results (demonstration format)",
      fictifNote: "These values are generated to illustrate the format. They do not describe any real country.",
      parSecteur: "By sector", parProduit: "By inventoried item",
      recenses: "items inventoried", verifie: "verified", estime: "estimated", declare: "declared",
      deficit: "Gap", faible: "low", moyen: "medium", fort: "high",
      secteurs: ["Health", "Education", "Water", "Energy", "Roads", "Telecoms", "Land", "Resources"],
      produits: ["Schools", "Health centres", "Boreholes and water points", "Substations", "Track sections", "Telecom masts", "Certified plots", "Resource sites"],
      legende: "Bar: verified, estimated or declared share"
    }
  };

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }

  // Générateur pseudo-aléatoire déterministe (mulberry32) à partir du code pays
  function graine(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return function () {
      h |= 0; h = (h + 0x6D2B79F5) | 0;
      var t = Math.imul(h ^ (h >>> 15), 1 | h);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function nombre(n, lang) {
    if (n == null || isNaN(n)) return null;
    return new Intl.NumberFormat(lang === "en" ? "en" : "fr").format(Math.round(n));
  }

  function fictives(iso3, pop, labels) {
    var r = graine(iso3 + "|tasety");
    var base = Math.max(40, Math.min(9000, Math.round(Math.sqrt(pop || 1e6) / 6)));
    return labels.map(function (nom) {
      var total = Math.max(5, Math.round(base * (0.25 + r() * 1.1)));
      var v = 0.25 + r() * 0.55, e = (1 - v) * (0.4 + r() * 0.3), d = 1 - v - e;
      var def = r();
      return { nom: nom, total: total, v: v, e: e, d: d, def: def < 0.34 ? "faible" : def < 0.7 ? "moyen" : "fort" };
    });
  }

  function mount(cont, opts) {
    var lang = (opts && opts.lang) === "en" ? "en" : "fr";
    var L = T[lang];
    var mode = "secteurs";
    var courant = null;

    var reel = el("section", "ad-bloc ad-reel");
    reel.setAttribute("aria-label", L.reel);
    var enteteR = el("div", "ad-entete");
    enteteR.appendChild(el("span", "ad-badge ad-badge-reel", L.reel));
    var kpi = el("dl", "ad-kpi");
    reel.appendChild(enteteR); reel.appendChild(kpi); reel.appendChild(el("p", "ad-note", L.reelNote));

    var fic = el("section", "ad-bloc ad-fictif");
    fic.setAttribute("aria-label", L.fictifTitre);
    var enteteF = el("div", "ad-entete");
    enteteF.appendChild(el("span", "ad-badge ad-badge-fictif", L.fictif));
    enteteF.appendChild(el("h3", "ad-titre", L.fictifTitre));
    var bascule = el("div", "ad-bascule"); bascule.setAttribute("role", "group");
    var b1 = el("button", null, L.parSecteur), b2 = el("button", null, L.parProduit);
    b1.type = b2.type = "button";
    bascule.appendChild(b1); bascule.appendChild(b2);
    enteteF.appendChild(bascule);
    var liste = el("ul", "ad-liste");
    fic.appendChild(enteteF); fic.appendChild(liste);
    fic.appendChild(el("p", "ad-note", L.fictifNote + " " + L.legende + "."));
    cont.appendChild(reel); cont.appendChild(fic);

    function bouton(b, actif) { b.setAttribute("aria-pressed", actif ? "true" : "false"); }
    function dessinerFictif() {
      bouton(b1, mode === "secteurs"); bouton(b2, mode === "produits");
      liste.textContent = "";
      if (!courant) return;
      var labels = mode === "secteurs" ? L.secteurs : L.produits;
      fictives(courant.iso3, courant.pop_est, labels).forEach(function (s) {
        var li = el("li", "ad-ligne");
        var tete = el("div", "ad-ligne-tete");
        tete.appendChild(el("b", null, s.nom));
        tete.appendChild(el("span", "ad-total", nombre(s.total, lang) + " " + L.recenses));
        var pastille = el("span", "ad-def", L.deficit + " " + L[s.def]);
        pastille.setAttribute("data-niveau", s.def);
        tete.appendChild(pastille);
        var barre = el("div", "ad-barre");
        barre.setAttribute("role", "img");
        var pv = Math.round(s.v * 100), pe = Math.round(s.e * 100), pd = Math.max(0, 100 - pv - pe);
        barre.setAttribute("aria-label", pv + " % " + L.verifie + ", " + pe + " % " + L.estime + ", " + pd + " % " + L.declare);
        [["v", pv], ["e", pe], ["d", pd]].forEach(function (x) {
          var i = el("i"); i.className = "ad-" + x[0]; i.style.width = x[1] + "%"; barre.appendChild(i);
        });
        var chiffres = el("div", "ad-chiffres");
        chiffres.textContent = "● " + pv + " %   ◐ " + pe + " %   ○ " + pd + " %";
        li.appendChild(tete); li.appendChild(barre); li.appendChild(chiffres);
        liste.appendChild(li);
      });
    }
    b1.addEventListener("click", function () { mode = "secteurs"; dessinerFictif(); });
    b2.addEventListener("click", function () { mode = "produits"; dessinerFictif(); });

    function update(data) {
      courant = data;
      kpi.textContent = "";
      var c = data.counts || {};
      var lignes = [
        [L.pop, nombre(data.pop_est, lang)],
        [L.airports, nombre(c.airports, lang)],
        [L.ports, nombre(c.ports, lang)],
        [L.rail, c.railways_km != null ? nombre(c.railways_km, lang) + " " + L.km : null],
        [L.roads, c.roads_km != null ? nombre(c.roads_km, lang) + " " + L.km : null],
        [L.cities, nombre(c.cities, lang)]
      ];
      var affichees = ((data.layers || {}).cities || []).length;
      if (c.cities != null && affichees < c.cities) lignes[5][2] = L.sur.replace("%n", nombre(affichees, lang));
      lignes.forEach(function (l) {
        var d = el("div", "ad-k");
        d.appendChild(el("dt", null, l[0]));
        d.appendChild(el("dd", null, l[1] == null ? L.na : l[1]));
        if (l[2]) d.appendChild(el("dt", "ad-sous", l[2]));
        kpi.appendChild(d);
      });
      dessinerFictif();
    }
    function clear() { courant = null; kpi.textContent = ""; liste.textContent = ""; }
    bouton(b1, true); bouton(b2, false);
    return { update: update, clear: clear };
  }

  root.AtlasDashboard = { mount: mount, _graine: graine };
})(typeof window !== "undefined" ? window : this);
