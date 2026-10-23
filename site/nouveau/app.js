/* Africa Bonds Monitor — Marchés and security pages of /nouveau/, rendered from data.json.
   Every value is copied from the verified dataset (FAIT). Ratios and totals are labelled CALCUL and are
   only computed when every input is published. XOF and XAF are never added together. No innerHTML
   with data: the DOM is built with text nodes. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  if (!app) return;

  var MONTHS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
  var KIND = { 'rendement': 'rendement · UMOA-Titres', 'prix': 'prix % du nominal · BEAC', 'précompté': 'taux précompté · BEAC', 'inconnu': 'nature non reconnue' };
  var FIELD_LABEL = { coupon: 'Coupon', maturity: 'Échéance', tenor: "Durée à l'émission", face: 'Valeur nominale', freq: 'Fréquence du coupon',
    issue: "Date d'émission", amort: 'Amortissement', listing: 'Cotation' };
  var STATUS_KEY = { coupon: 'coupon_rate', maturity: 'maturity_date', tenor: 'tenor_days', face: 'face_value', freq: 'coupon_frequency',
    issue: 'issue_date', amort: 'amortization', listing: 'listing_status' };
  var FREQ = { annual: 'annuelle', semiannual: 'semestrielle', semi_annual: 'semestrielle', quarterly: 'trimestrielle', monthly: 'mensuelle' };

  function h(tag, attrs) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    });
    for (var i = 2; i < arguments.length; i++) {
      var c = arguments[i];
      if (c === null || c === undefined || c === false) continue;
      if (Array.isArray(c)) c.forEach(function (x) { if (x) el.appendChild(typeof x === 'string' ? document.createTextNode(x) : x); });
      else el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    }
    return el;
  }
  function frNum(v, dp) {
    return v.toLocaleString('fr-FR', { minimumFractionDigits: dp, maximumFractionDigits: dp });
  }
  function frInt(v) { return Math.round(v).toLocaleString('fr-FR'); }
  function frDate(d, long) {
    var p = d.split('-');
    return long ? (parseInt(p[2], 10) + ' ' + MONTHS[parseInt(p[1], 10) - 1] + ' ' + p[0]) : (p[2] + '/' + p[1] + '/' + p[0]);
  }
  function md(v, cur) { return frNum(v / 1e9, 2) + ' Md ' + cur; }
  function full(v, cur) { return frInt(v) + ' ' + cur; }
  function badge(b) { return h('span', { class: 'badge ' + (b === 'FAIT' ? 'b-fact' : b === 'CALCUL' ? 'b-calc' : 'b-nd'), text: b }); }
  function srcShort(url) { return /umoatitres/.test(url) ? 'UMOA-Titres' : /beac\.int/.test(url) ? 'BEAC' : /bvm-ac/.test(url) ? 'BVMAC' : 'Source'; }
  function instrLabel(instr, zone) {
    if (instr !== 'treasury_bill' && instr !== 'treasury_bond') return 'Obligation cotée';
    var bill = instr === 'treasury_bill';
    return zone === 'CEMAC' ? (bill ? 'BTA (bon)' : 'OTA (obligation)') : (bill ? 'Bon du Trésor' : 'Obligation du Trésor');
  }
  function issuerLabel(issuer, country) { return /^Government of /.test(issuer) ? 'État (' + country + ')' : issuer; }
  function fact(label, value, b) { return h('div', { class: 'fact' }, h('span', { text: label }), h('span', null, h('span', { class: 'mono', text: value }), badge(b))); }

  function load() {
    return fetch('data.json', { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }
  function fail() {
    app.textContent = '';
    app.appendChild(h('div', { class: 'notice' }, 'Les données n’ont pas pu être chargées. ', h('a', { href: '../donnees/fr.html', text: 'Télécharger les fichiers CSV' }), ' ou réessayer plus tard.'));
  }

  function rowsOf(d) {
    return d.rows.map(function (r, i) {
      var s = d.secs[r[3]];
      var zone = d.countries[r[1]][1];
      return { i: i, date: r[0], iso: r[1], cur: r[2], isin: r[3], buyback: r[4] === 1, offered: r[5], submitted: r[6], allocated: r[7],
        value: r[8], kind: r[9], cutoff: r[10], bidders: r[11], url: d.urls[r[12]], zone: zone, sec: s,
        instr: s ? s[1] : null, maturity: s ? s[9] : null, coupon: s ? s[6] : null, name: d.countries[r[1]][0] };
    });
  }

  /* ---------------- Marchés ---------------- */
  function marches(d) {
    var all = rowsOf(d);
    var params = new URLSearchParams(location.search);
    var pre = params.get('pays');
    var st = { zone: 'all', country: 'all', instr: 'all', op: 'all', page: 0, sel: null };
    if (pre && d.countries[pre]) { st.country = pre; st.zone = d.countries[pre][1]; }
    var PER = 25;

    function filtered() {
      return all.filter(function (r) {
        return (st.zone === 'all' || r.zone === st.zone) && (st.country === 'all' || r.iso === st.country) &&
          (st.instr === 'all' || (st.instr === 'bill' ? r.instr === 'treasury_bill' : r.instr === 'treasury_bond')) &&
          (st.op === 'all' || (st.op === 'buyback' ? r.buyback : !r.buyback));
      });
    }
    function pills(label, opts, key, onPick) {
      return h('div', { class: 'frow' }, h('span', { class: 'flab', text: label }), opts.map(function (o) {
        return h('button', { type: 'button', class: 'pill', 'aria-pressed': String(st[key] === o[0]), text: o[1],
          onclick: function () { onPick(o[0]); render(); } });
      }));
    }
    function csv(rows) {
      var head = ['date', 'pays', 'zone', 'isin', 'operation', 'instrument', 'echeance', 'devise', 'montant_offert', 'montant_soumis', 'montant_retenu',
        'valeur_publiee', 'nature_valeur', 'taux_marginal', 'soumissionnaires', 'source', 'source_url'];
      var esc = function (v) { v = v === null || v === undefined ? '' : String(v); return /[",;\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
      var lines = [head.join(',')].concat(rows.map(function (r) {
        return [r.date, r.iso, r.zone, r.isin, r.buyback ? 'rachat' : 'emission', r.instr, r.maturity, r.cur, r.offered, r.submitted, r.allocated,
          r.value, r.kind, r.cutoff, r.bidders, srcShort(r.url), r.url].map(esc).join(',');
      }));
      var blob = new Blob(['﻿' + lines.join('\r\n') + '\r\n'], { type: 'text/csv;charset=utf-8' });
      var a = h('a', { href: URL.createObjectURL(blob), download: 'abm-adjudications-' + d.as_of + '.csv' });
      document.body.appendChild(a); a.click(); a.remove();
    }
    function detail(r) {
      if (!r) {
        return h('aside', { class: 'card side', 'aria-label': 'Détail de l’adjudication' }, h('h2', { text: 'Détail' }),
          h('p', { text: 'Sélectionnez une adjudication pour voir les montants publiés, les ratios calculés et le document officiel.' }),
          h('p', { class: 'small', text: 'Un champ non publié par la source est affiché « non publié » : il n’est jamais estimé.' }));
      }
      var kindWord = r.kind === 'prix' ? 'prix' : r.kind === 'précompté' ? 'taux précompté' : r.kind === 'rendement' ? 'rendement' : 'nature inconnue';
      var note = r.kind === 'prix' ? 'La BEAC publie un prix moyen pondéré en % du nominal. Ce n’est pas un rendement : il n’est pas converti sans les conditions complètes du titre.'
        : r.kind === 'précompté' ? 'Taux précompté publié par la BEAC : ce n’est pas un rendement actuariel.'
        : r.offered === null ? 'Le montant offert n’est pas publié pour cette adjudication : le taux de couverture n’est donc pas calculé.' : '';
      return h('aside', { class: 'card side', 'aria-label': 'Détail de l’adjudication', 'aria-live': 'polite' },
        h('p', { class: 'small', text: r.zone + ' · ' + r.cur + (r.buyback ? ' · opération de rachat' : '') }),
        h('h2', { text: r.name + ' — ' + instrLabel(r.instr, r.zone) }),
        h('p', { class: 'small mono', text: 'ISIN ' + r.isin }),
        h('div', { class: 'facts' },
          fact('Date', frDate(r.date), 'FAIT'),
          fact('Échéance', r.maturity ? frDate(r.maturity) : 'non publiée', r.maturity ? 'FAIT' : 'NON PUBLIÉ'),
          fact('Coupon', r.coupon === null ? (r.instr === 'treasury_bill' ? 'sans coupon' : 'non publié') : frNum(r.coupon, 2) + ' %', r.coupon === null && r.instr !== 'treasury_bill' ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Valeur publiée (' + kindWord + ')', r.value === null ? 'non publiée' : frNum(r.value, 2) + ' %', r.value === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Taux marginal', r.cutoff === null ? 'non publié' : frNum(r.cutoff, 2) + ' %', r.cutoff === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Montant offert', r.offered === null ? 'non publié' : full(r.offered, r.cur), r.offered === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Montant soumis', r.submitted === null ? 'non publié' : full(r.submitted, r.cur), r.submitted === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Montant retenu', r.allocated === null ? 'non publié' : full(r.allocated, r.cur), r.allocated === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Soumissionnaires', r.bidders === null ? 'non publié' : frInt(r.bidders), r.bidders === null ? 'NON PUBLIÉ' : 'FAIT'),
          fact('Taux de couverture (soumis / offert)', r.offered && r.submitted !== null ? frNum(r.submitted / r.offered, 2) + ' x' : 'indisponible', r.offered && r.submitted !== null ? 'CALCUL' : 'NON PUBLIÉ'),
          fact('Taux de service (retenu / soumis)', r.submitted > 0 && r.allocated !== null ? frNum(100 * r.allocated / r.submitted, 1) + ' %' : 'indisponible', r.submitted > 0 && r.allocated !== null ? 'CALCUL' : 'NON PUBLIÉ')),
        note ? h('p', { class: 'small', text: note }) : null,
        h('a', { href: r.url, text: 'Ouvrir le document officiel ' + srcShort(r.url) + ' →' }),
        h('a', { href: 'titre.html?isin=' + encodeURIComponent(r.isin), text: 'Fiche du titre →' }),
        h('a', { href: 'pays/' + r.iso + '.html', text: 'Page ' + r.name + ' →' }));
    }
    function render() {
      var list = filtered();
      var pages = Math.max(1, Math.ceil(list.length / PER));
      if (st.page >= pages) st.page = pages - 1;
      var shown = list.slice(st.page * PER, st.page * PER + PER);
      var selRow = st.sel === null ? null : all[st.sel];
      if (selRow && list.indexOf(selRow) < 0) selRow = null;
      var isos = [];
      all.forEach(function (r) { if ((st.zone === 'all' || r.zone === st.zone) && isos.indexOf(r.iso) < 0) isos.push(r.iso); });
      isos.sort(function (a, b) { return d.countries[a][0].localeCompare(d.countries[b][0], 'fr'); });
      var totals = ['XOF', 'XAF'].map(function (cur) {
        var rs = list.filter(function (r) { return r.cur === cur && !r.buyback && r.allocated !== null; });
        return rs.length ? h('div', { class: 'total' }, badge('CALCUL'), h('span', { text: 'Retenu en émission (' + cur + ', ' + frInt(rs.length) + ' adjudications filtrées) :' }),
          h('strong', { class: 'mono', text: md(rs.reduce(function (s, r) { return s + r.allocated; }, 0), cur) })) : null;
      });
      var tbody = h('tbody', null, shown.map(function (r) {
        var pick = function () { st.sel = r.i; render(); };
        return h('tr', { class: 'click' + (selRow === r ? ' sel' : ''), onclick: pick },
          h('td', { class: 'mono' }, h('button', { type: 'button', class: 'pill', style: 'min-height:28px;padding:3px 8px', 'aria-label': 'Détail : ' + r.name + ', ' + frDate(r.date), text: frDate(r.date),
            onclick: function (e) { e.stopPropagation(); pick(); } })),
          h('td', null, h('a', { href: 'pays/' + r.iso + '.html', text: r.name, onclick: function (e) { e.stopPropagation(); } })),
          h('td', { text: instrLabel(r.instr, r.zone) + (r.buyback ? ' · rachat' : '') }),
          h('td', { class: 'mono', text: r.maturity ? frDate(r.maturity) : '—' }),
          h('td', { class: 'num' }, r.value === null ? 'non publié' : frNum(r.value, 2) + ' %', h('br'), h('span', { class: 'kind', text: KIND[r.kind] })),
          h('td', { class: 'num', text: r.allocated === null ? 'non publié' : md(r.allocated, r.cur) }),
          h('td', null, h('a', { href: r.url, 'aria-label': srcShort(r.url) + ', adjudication ' + r.name + ' du ' + frDate(r.date) + ' (PDF)', text: srcShort(r.url).replace('UMOA-Titres', 'UMOA'),
            onclick: function (e) { e.stopPropagation(); } })));
      }));
      app.textContent = '';
      app.appendChild(h('div', null,
        h('p', { class: 'crumbs' }, h('a', { href: './', text: 'Accueil' }), ' / Marchés'),
        h('div', { class: 'row-head' },
          h('div', null, h('h1', { text: 'Adjudications vérifiées' }), h('p', { class: 'sub', text: 'Données au ' + frDate(d.as_of, true) + ' · ' + frInt(all.length) + ' adjudications, chacune reliée à son document officiel' })),
          h('div', { class: 'ctas' }, h('button', { type: 'button', class: 'btn btn-line', style: 'background:#fff;cursor:pointer', text: 'Exporter la sélection (CSV, avec sources)', onclick: function () { csv(list); } }),
            h('a', { class: 'btn btn-line', href: '../api/v1/index.json', text: 'API JSON' })))));
      app.appendChild(h('div', { class: 'filters' },
        pills('Zone', [['all', 'Toutes'], ['UEMOA', 'UEMOA (XOF)'], ['CEMAC', 'CEMAC (XAF)']], 'zone', function (v) { st.zone = v; st.country = 'all'; st.page = 0; st.sel = null; }),
        pills('Pays', [['all', 'Tous']].concat(isos.map(function (i) { return [i, d.countries[i][0]]; })), 'country', function (v) { st.country = v; st.page = 0; st.sel = null; }),
        pills('Instrument', [['all', 'Tous'], ['bill', 'Bons (BT / BTA)'], ['bond', 'Obligations (OAT / OTA)']], 'instr', function (v) { st.instr = v; st.page = 0; st.sel = null; }),
        pills('Opération', [['all', 'Toutes'], ['primary', 'Émissions'], ['buyback', 'Rachats']], 'op', function (v) { st.op = v; st.page = 0; st.sel = null; })));
      app.appendChild(h('div', { class: 'notice', role: 'note' }, 'La nature de la valeur publiée dépend de la source : ', h('strong', { text: 'rendement' }), ' (UMOA-Titres), ',
        h('strong', { text: 'prix en % du nominal' }), ' (OTA, BEAC) ou ', h('strong', { text: 'taux précompté' }), ' (BTA, BEAC). Elles ne sont jamais mélangées dans un même calcul, et XOF et XAF ne sont jamais additionnés.'));
      app.appendChild(h('div', { class: 'two' },
        h('div', { class: 'grow' },
          h('div', { class: 'row-head' }, h('span', { class: 'small', 'aria-live': 'polite', text: frInt(list.length) + (list.length > 1 ? ' adjudications' : ' adjudication') + ' · page ' + (st.page + 1) + ' / ' + pages }),
            h('span', { class: 'small', text: 'Cliquez sur une ligne pour le détail' })),
          h('div', { class: 'table-box' }, h('table', { class: 'dense' },
            h('thead', null, h('tr', null, ['Date', 'Pays', 'Instrument', 'Échéance', 'Valeur publiée', 'Retenu', 'Source'].map(function (t, k) {
              return h('th', { scope: 'col', class: k === 4 || k === 5 ? 'num' : null, text: t });
            }))), tbody)),
          h('div', { class: 'pager' },
            h('button', { type: 'button', text: '← Précédent', disabled: st.page === 0, onclick: function () { st.page--; render(); } }),
            h('button', { type: 'button', text: 'Suivant →', disabled: st.page >= pages - 1, onclick: function () { st.page++; render(); } })),
          h('div', { class: 'totals' }, totals)),
        detail(selRow)));
    }
    render();
  }

  /* ---------------- Titre ---------------- */
  function titre(d) {
    var isin = new URLSearchParams(location.search).get('isin') || '';
    var s = d.secs[isin];
    var bond = d.bvmac.filter(function (b) { return b.isin === isin; })[0];
    app.textContent = '';
    if (!s && !bond) {
      app.appendChild(h('div', { class: 'notice' }, 'Titre introuvable dans les données vérifiées. ', h('a', { href: 'marches.html', text: 'Retour aux marchés' })));
      return;
    }
    var iso = s ? s[2] : bond.country;
    var c = d.countries[iso] || [iso, '', '', ''];
    var zone = c[1], cur = s ? s[3] : 'XAF';
    var rows = rowsOf(d).filter(function (r) { return r.isin === isin; }).reverse();
    var nd = s ? s[13] : [];
    document.title = (s ? s[0] : bond.name) + ' — Africa Bonds Monitor';

    var terms = h('div', { class: 'facts' }, ['coupon', 'maturity', 'tenor', 'face', 'freq', 'issue', 'amort', 'listing'].map(function (k) {
      var v = null;
      if (s) v = { coupon: s[6], maturity: s[9], tenor: s[10], face: s[5], freq: s[7], issue: s[8], amort: s[11], listing: s[12] }[k];
      if (k === 'coupon' && v === null && bond && bond.coupon !== null) v = bond.coupon;
      if (v === null || v === undefined || v === '') {
        var undisclosed = nd.indexOf(STATUS_KEY[k]) >= 0;
        if (k === 'coupon' && s && s[1] === 'treasury_bill') return fact('Coupon', 'sans coupon (bon)', 'FAIT');
        return fact(FIELD_LABEL[k], undisclosed ? 'non publié' : 'non disponible', 'NON PUBLIÉ');
      }
      var txt = k === 'coupon' ? frNum(v, 2) + ' %' : k === 'maturity' || k === 'issue' ? frDate(v) : k === 'tenor' ? frInt(v) + ' jours'
        : k === 'face' ? frInt(v) + ' ' + cur : k === 'freq' ? (FREQ[v] || v) : k === 'amort' ? (v === 'CONSTANT' ? 'constant' : v) : k === 'listing' && /BVMAC/.test(v) ? 'BVMAC (bulletin officiel de la cote)' : String(v);
      return fact(FIELD_LABEL[k], txt, 'FAIT');
    }));
    var calcNote = (!s || !s[7] || !s[8])
      ? 'Sans fréquence de coupon et date d’émission publiées, la plateforme ne calcule ni rendement actuariel, ni duration, ni coupon couru pour ce titre : elle affiche les valeurs publiées.'
      : 'Valeurs affichées telles que publiées.';

    var primary = rows.filter(function (r) { return !r.buyback; });
    var buybacks = rows.length - primary.length;
    var sameCur = primary.filter(function (r) { return r.allocated !== null; });
    var vals = rows.filter(function (r) { return r.value !== null; });
    var kinds = vals.map(function (r) { return r.kind; }).filter(function (k, i, a) { return a.indexOf(k) === i; });
    var kpis = [];
    if (rows.length) {
      kpis.push([frInt(primary.length) + (buybacks ? ' + ' + frInt(buybacks) + ' rachat(s)' : ''), 'adjudications vérifiées (émission' + (buybacks ? ' et rachats' : '') + ')', 'FAIT']);
      if (sameCur.length) kpis.push([md(sameCur.reduce(function (a, r) { return a + r.allocated; }, 0), cur), 'retenu cumulé en émission — pas l’encours', 'CALCUL']);
      if (vals.length && kinds.length === 1) {
        var lo = Math.min.apply(null, vals.map(function (r) { return r.value; })), hi = Math.max.apply(null, vals.map(function (r) { return r.value; }));
        kpis.push([frNum(lo, 2) + ' – ' + frNum(hi, 2) + ' %', 'valeurs publiées (' + KIND[kinds[0]] + ')', 'FAIT']);
      }
    }
    if (bond && bond.trades.length) {
      kpis.push([frInt(bond.trades.length), 'jours avec transaction à la BVMAC', 'FAIT']);
      kpis.push([frNum(bond.trades[0][1], 2) + ' %', 'dernier cours de clôture (' + frDate(bond.trades[0][0]) + ')', 'FAIT']);
    }

    function chart(obs, label, unit) {
      if (obs.length < 2) return null;
      var ys = obs.map(function (o) { return o[1]; });
      var yMin = Math.floor(Math.min.apply(null, ys) - 0.5), yMax = Math.ceil(Math.max.apply(null, ys) + 0.5);
      if (yMax - yMin < 2) { yMin -= 1; yMax += 1; }
      var t0 = Date.parse(obs[0][0]), t1 = Date.parse(obs[obs.length - 1][0]), span = Math.max(1, t1 - t0);
      var box = h('div', { class: 'chart', role: 'img', 'aria-label': label });
      var step = yMax - yMin > 6 ? 2 : 1;
      for (var v = yMin; v <= yMax; v += step) {
        box.appendChild(h('div', { class: 'gy', style: 'bottom:' + (100 * (v - yMin) / (yMax - yMin)) + '%' }, h('span', { text: frNum(v, 0) + unit })));
      }
      box.appendChild(h('span', { class: 'gx', style: 'left:0%;transform:none', text: frDate(obs[0][0]) }));
      box.appendChild(h('span', { class: 'gx', style: 'left:auto;right:0;transform:none', text: frDate(obs[obs.length - 1][0]) }));
      obs.forEach(function (o) {
        box.appendChild(h('div', { class: 'pt', style: 'left:' + (100 * (Date.parse(o[0]) - t0) / span) + '%;bottom:' + (100 * (o[1] - yMin) / (yMax - yMin)) + '%' }, h('span', { class: 'dot' })));
      });
      return box;
    }

    var sections = [];
    if (rows.length) {
      var obs = kinds.length === 1 ? vals.map(function (r) { return [r.date, r.value]; }) : [];
      var ch = chart(obs, 'Valeurs publiées par adjudication, du ' + (obs.length ? frDate(obs[0][0]) : '') + ' au ' + (obs.length ? frDate(obs[obs.length - 1][0]) : ''), ' %');
      if (ch) sections.push(h('section', { class: 'card' }, h('div', { class: 'row-head' }, h('h2', { text: 'Valeur publiée par adjudication' }), h('span', { class: 'small', text: KIND[kinds[0]] + ' · points non reliés' })), ch));
      sections.push(h('section', null, h('h2', { text: 'Historique des adjudications' }),
        h('div', { class: 'table-box' }, h('table', null,
          h('thead', null, h('tr', null, ['Date', 'Opération', 'Offert', 'Soumis', 'Retenu', 'Valeur publiée', 'Source'].map(function (t, k) { return h('th', { scope: 'col', class: k >= 2 && k <= 5 ? 'num' : null, text: t }); }))),
          h('tbody', null, rows.slice().reverse().map(function (r) {
            return h('tr', null, h('td', { class: 'mono', text: frDate(r.date) }), h('td', { text: r.buyback ? 'Rachat' : 'Émission' }),
              h('td', { class: 'num', text: r.offered === null ? 'non publié' : full(r.offered, r.cur) }),
              h('td', { class: 'num', text: r.submitted === null ? 'non publié' : full(r.submitted, r.cur) }),
              h('td', { class: 'num', text: r.allocated === null ? 'non publié' : full(r.allocated, r.cur) }),
              h('td', { class: 'num' }, r.value === null ? 'non publié' : frNum(r.value, 2) + ' %', h('br'), h('span', { class: 'kind', text: KIND[r.kind] })),
              h('td', null, h('a', { href: r.url, 'aria-label': srcShort(r.url) + ', adjudication du ' + frDate(r.date) + ' (PDF)', text: srcShort(r.url) + ' (PDF)' })));
          })))),
        h('p', { class: 'small', text: 'Le cumul retenu n’est pas l’encours : les rachats et remboursements ne sont pas tous connus.' })));
    }
    if (bond) {
      var tr = bond.trades.slice().reverse();
      var chb = chart(tr.map(function (t) { return [t[0], t[1]]; }), 'Cours de clôture les jours de transaction', ' %');
      if (chb) sections.push(h('section', { class: 'card' }, h('div', { class: 'row-head' }, h('h2', { text: 'Cours de clôture (% du nominal)' }), h('span', { class: 'small', text: 'jours de transaction seulement' })), chb));
      sections.push(h('section', null, h('h2', { text: 'Transactions à la BVMAC' }),
        bond.trades.length ? h('div', { class: 'table-box' }, h('table', null,
          h('thead', null, h('tr', null, ['Date', 'Cours de clôture', 'Valeur transigée', 'Source'].map(function (t, k) { return h('th', { scope: 'col', class: k === 1 || k === 2 ? 'num' : null, text: t }); }))),
          h('tbody', null, bond.trades.map(function (t) {
            return h('tr', null, h('td', { class: 'mono', text: frDate(t[0]) }), h('td', { class: 'num', text: frNum(t[1], 2) + ' %' }), h('td', { class: 'num', text: full(t[2], 'XAF') }),
              h('td', null, h('a', { href: t[3], 'aria-label': 'BVMAC, bulletin officiel de la cote du ' + frDate(t[0]) + ' (PDF)', text: 'BVMAC (PDF)' })));
          })))) : h('p', { class: 'small', text: 'Aucune transaction relevée depuis le début de la collecte.' }),
        h('p', { class: 'small', text: 'Seuls les jours avec une transaction sont repris : un cours affiché sans échange (NC) n’est pas une transaction. Valeur transigée en francs CFA (XAF), coupon couru inclus, telle qu’imprimée. La BVMAC ne publie pas de rendement ; aucun n’est calculé.' })));
    }

    app.appendChild(h('p', { class: 'crumbs' }, h('a', { href: './', text: 'Accueil' }), ' / ', h('a', { href: 'marches.html', text: 'Marchés' }), ' / ',
      h('a', { href: 'pays/' + iso + '.html', text: c[0] }), ' / ' + isin));
    app.appendChild(h('div', { class: 'row-head' },
      h('div', null, h('p', { class: 'eyebrow', style: 'color:#4A5568', text: s ? instrLabel(s[1], zone) : 'Obligation cotée à la BVMAC' }),
        h('h1', { text: s ? s[0] : bond.name }),
        h('p', { class: 'sub' }, h('span', { class: 'mono', text: 'ISIN ' + isin }), ' · ' + issuerLabel((s && s[4]) || (bond && bond.issuer) || '', c[0]) + ' · ' + zone + ' · ' + cur))));
    var termsBox = h('section', { class: 'card side' }, h('h2', { text: 'Conditions du titre' }),
      h('p', { class: 'small', text: 'Telles que publiées par la source. Un champ absent n’est jamais estimé.' }), terms,
      h('p', { class: 'small', text: calcNote }),
      s ? h('a', { href: d.urls[s[14]], text: 'Document source des conditions (' + srcShort(d.urls[s[14]]) + ') →' }) : null);
    var right = h('div', { class: 'grow', style: 'display:flex;flex-direction:column;gap:20px' },
      kpis.length ? h('div', { class: 'kpis kpis-in' }, kpis.map(function (k) { return h('div', { class: 'kpi' }, h('span', { class: 'kv' }, k[0], badge(k[2])), h('span', { class: 'kl', text: k[1] })); })) : null,
      sections);
    app.appendChild(h('div', { class: 'two' }, termsBox, right));
  }

  load().then(function (d) {
    var page = app.getAttribute('data-page');
    if (page === 'marches') marches(d);
    else if (page === 'titre') titre(d);
  }).catch(fail);
})();
