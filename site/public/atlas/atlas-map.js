/* AtlasMap : carte SIG légère en SVG, sans dépendance ni tuile (hors ligne / PWA).
   API : AtlasMap.mount(el, {lang, dataBase, onCountryLoaded, onError}) -> {setCountry, setLayerVisible, destroy}
   Les noms de lieux sont toujours insérés via textContent / setAttribute (jamais innerHTML). */
(function (global) {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var R = 6371.0088, RAD = Math.PI / 180;

  var T = {
    fr: {
      layers: 'Couches', borders: 'Frontières', regions: 'Régions', roads: 'Routes', rail: 'Rail', airports: 'Aéroports',
      ports: 'Ports', cities: 'Villes', lakes: 'Lacs', capital: 'Capitale', city: 'Ville', airport: 'Aéroport', port: 'Port',
      zoomIn: 'Zoomer', zoomOut: 'Dézoomer', recenter: 'Recentrer', recenterT: 'Recentrer', loading: 'Chargement de la carte…',
      error: 'Données indisponibles pour ce pays.', none: 'Choisissez un pays.', pop: 'hab.',
      help: 'Clavier : flèches pour déplacer, + / − pour zoomer, 0 pour recentrer, N / P pour parcourir les lieux visibles.',
      attrib: 'Natural Earth, domaine public. Données générales, non exhaustives.',
      alt: function (n, c) { return 'Carte de ' + n + (c ? ' : ' + c : '') + '.'; },
      ctrs: { airports: 'aéroports', ports: 'ports', cities: 'villes', railways_km: 'km de rail', roads_km: 'km de routes' },
      types: { large_airport: 'grand aéroport', medium_airport: 'aéroport moyen', small_airport: 'petit aéroport', international: 'aéroport international', major: 'aéroport majeur', mid: 'aéroport moyen', small: 'petit aéroport', military: 'militaire', heliport: 'héliport', seaplane_base: 'hydrobase' },
      found: function (i, n) { return i + ' sur ' + n; }, noPoints: 'Aucun lieu visible.'
    },
    en: {
      layers: 'Layers', borders: 'Borders', regions: 'Regions', roads: 'Roads', rail: 'Rail', airports: 'Airports',
      ports: 'Ports', cities: 'Cities', lakes: 'Lakes', capital: 'Capital', city: 'City', airport: 'Airport', port: 'Port',
      zoomIn: 'Zoom in', zoomOut: 'Zoom out', recenter: 'Reset view', recenterT: 'Reset view', loading: 'Loading map…',
      error: 'No data available for this country.', none: 'Choose a country.', pop: 'inh.',
      help: 'Keyboard: arrow keys to pan, + / − to zoom, 0 to reset, N / P to step through visible places.',
      attrib: 'Natural Earth, public domain. General data, not exhaustive.',
      alt: function (n, c) { return 'Map of ' + n + (c ? ': ' + c : '') + '.'; },
      ctrs: { airports: 'airports', ports: 'ports', cities: 'cities', railways_km: 'km of rail', roads_km: 'km of roads' },
      types: { large_airport: 'large airport', medium_airport: 'medium airport', small_airport: 'small airport', international: 'international airport', major: 'major airport', mid: 'medium airport', small: 'small airport', military: 'military', heliport: 'heliport', seaplane_base: 'seaplane base' },
      found: function (i, n) { return i + ' of ' + n; }, noPoints: 'No visible place.'
    }
  };

  // Symboles centrés sur (0,0), ~ 12 px
  var SYM = {
    airport: 'M0-6.5L1.6-1.5L6.5 1.8V3.4L1.4 2L1.2 5L3.2 6.6V7.6L0 6.8L-3.2 7.6V6.6L-1.2 5L-1.4 2L-6.5 3.4V1.8L-1.6-1.5Z',
    port: 'M-4.5-4.5H4.5V4.5H-4.5Z',
    city: 'M0-3.6A3.6 3.6 0 1 1 0 3.6A3.6 3.6 0 1 1 0-3.6Z',
    capital: 'M0-7L2-2.4L7-2.2L3.1 1L4.4 6L0 3.2L-4.4 6L-3.1 1L-7-2.2L-2-2.4Z'
  };
  var LAYERS = ['borders', 'regions', 'roads', 'rail', 'airports', 'ports', 'cities', 'lakes'];

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function h(tag, cls, parent, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function round1(v) { return Math.round(v * 10) / 10; }

  function mount(container, opts) {
    opts = opts || {};
    var lang = opts.lang === 'en' ? 'en' : 'fr';
    var L = T[lang];
    var dataBase = opts.dataBase || 'static/data/';
    if (dataBase.slice(-1) !== '/') dataBase += '/';
    var uid = 'am' + Math.random().toString(36).slice(2, 8);
    var nf = new Intl.NumberFormat(lang === 'fr' ? 'fr-FR' : 'en-GB');
    var reduce = global.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');

    // ---------- DOM ----------
    container.textContent = '';
    var root = h('div', 'am-root', container);
    var bar = h('div', 'am-bar', root);
    var title = h('h3', 'am-title', bar, L.none);
    var btns = h('div', 'am-btns', bar);
    function mkBtn(txt, label, fn) {
      var b = h('button', 'am-btn', btns, txt); b.type = 'button'; b.setAttribute('aria-label', label); b.title = label;
      b.addEventListener('click', fn); return b;
    }
    mkBtn('+', L.zoomIn, function () { zoomBy(1.6); });
    mkBtn('−', L.zoomOut, function () { zoomBy(1 / 1.6); });
    var recBtn = mkBtn(L.recenterT, L.recenter, function () { recenter(true); });
    recBtn.setAttribute('aria-label', L.recenter);

    var body = h('div', 'am-body', root);
    var stage = h('div', 'am-stage', body);
    var svg = el('svg', { 'class': 'am-svg', role: 'img', tabindex: '0', 'aria-labelledby': uid + 't ' + uid + 'd', 'aria-describedby': uid + 'h' }, stage);
    var svgTitle = el('title', { id: uid + 't' }, svg); svgTitle.textContent = L.none;
    var svgDesc = el('desc', { id: uid + 'd' }, svg); svgDesc.textContent = '';
    var world = el('g', { 'class': 'am-world' }, svg);
    var gLand = el('path', { 'class': 'am-land' }, world);
    var gLakes = el('path', { 'class': 'am-lakes' }, world);
    var gRegions = el('path', { 'class': 'am-regions' }, world);
    var gRoads = [1, 2, 3].map(function (t) { return el('path', { 'class': 'am-roads t' + t }, world); });
    var gRail = el('path', { 'class': 'am-rail' }, world);
    var gBorder = el('path', { 'class': 'am-border' }, world);
    var ptsRoot = el('g', { 'class': 'am-pts' }, svg);
    var layerGroups = { airports: el('g', null, ptsRoot), ports: el('g', null, ptsRoot), cities: el('g', null, ptsRoot) };
    var lblRoot = el('g', { 'class': 'am-labels' }, svg);

    var tip = h('div', 'am-tip', stage); tip.setAttribute('role', 'tooltip'); tip.id = uid + 'tip'; tip.hidden = true;
    var scaleBox = h('div', 'am-scale', stage); var scaleTxt = h('span', null, scaleBox); var scaleBar = h('i', null, scaleBox);
    var status = h('div', 'am-status', stage, L.none);
    var live = h('div', 'am-sr', root); live.setAttribute('aria-live', 'polite'); live.setAttribute('role', 'status');

    var fs = h('fieldset', 'am-layers', body);
    h('legend', null, fs, L.layers);
    var checks = {}, counts = {};
    var visible = {}; LAYERS.forEach(function (n) { visible[n] = true; });
    function legendIcon(name) {
      var s = el('svg', { width: 22, height: 16, viewBox: '-11 -8 22 16', 'aria-hidden': 'true', focusable: 'false' });
      var st = 'getComputedStyle';
      var styles = {
        borders: { k: 'line', c: 'var(--am-border)', w: 2.2 }, regions: { k: 'line', c: 'var(--am-region)', w: 1.2, d: '4 3' },
        roads: { k: 'line', c: 'var(--am-road)', w: 2 }, rail: { k: 'line', c: 'var(--am-rail)', w: 1.5, d: '7 3 1.5 3' },
        lakes: { k: 'rect' }, airports: { k: 'sym', s: 'airport' }, ports: { k: 'sym', s: 'port' }, cities: { k: 'sym', s: 'city' }
      }[name];
      if (styles.k === 'line') {
        el('path', { d: 'M-10 0H10', stroke: styles.c, 'stroke-width': styles.w, 'stroke-dasharray': styles.d || 'none', fill: 'none' }, s);
      } else if (styles.k === 'rect') {
        el('rect', { x: -9, y: -5, width: 18, height: 10, rx: 3, fill: 'var(--am-lake)', 'fill-opacity': .45, stroke: 'var(--am-lake)', 'stroke-width': 1 }, s);
      } else {
        el('path', { d: SYM[styles.s], fill: 'var(--am-' + (name === 'cities' ? 'city' : styles.s) + ')' }, s);
        if (name === 'cities') el('path', { d: SYM.capital, fill: 'var(--am-capital)', transform: 'translate(8 0) scale(.6)' }, s);
      }
      return s;
    }
    LAYERS.forEach(function (name) {
      var lab = h('label', null, fs);
      var cb = h('input', null, lab); cb.type = 'checkbox'; cb.checked = true; cb.setAttribute('data-layer', name);
      lab.appendChild(legendIcon(name));
      h('span', null, lab, L[name]);
      counts[name] = h('span', 'am-n', lab);
      checks[name] = cb;
      cb.addEventListener('change', function () { setLayerVisible(name, cb.checked); });
    });
    h('p', 'am-help', fs, L.help).id = uid + 'h';
    h('p', 'am-foot', root, L.attrib);

    // ---------- état ----------
    var data = null, lon0 = 0, lat0 = 0, cosL = 1;
    var geo = null;            // géométries projetées (km)
    var pts = [];              // points {x,y,kind,name,sub,pop,cap,g,rank}
    var W = 0, H = 0, s0 = 1;  // px par km à zoom 1
    var view = { cx: 0, cy: 0, k: 1 };
    var home = null, extent = null, bucket = -99, raf = 0, token = 0, active = -1, destroyed = false, anim = 0;
    var MAXK = 80;

    function proj(lon, lat) {
      var dl = lon - lon0; if (dl > 180) dl -= 360; else if (dl < -180) dl += 360;
      return [R * dl * RAD * cosL, -R * (lat - lat0) * RAD];
    }
    function projLine(coords) {
      var a = new Float64Array(coords.length * 2), n = 0;
      for (var i = 0; i < coords.length; i++) {
        var c = coords[i]; if (!c || c.length < 2 || !isFinite(c[0]) || !isFinite(c[1])) continue;
        var p = proj(c[0], c[1]); a[n++] = p[0]; a[n++] = p[1];
      }
      return a.subarray(0, n);
    }
    // Géométrie GeoJSON -> liste d'{closed, pts}
    function projGeom(g, out) {
      if (!g) return out;
      var t = g.type, c = g.coordinates, i, j;
      if (t === 'Polygon') { for (i = 0; i < c.length; i++) out.push({ closed: true, p: projLine(c[i]) }); }
      else if (t === 'MultiPolygon') { for (i = 0; i < c.length; i++) for (j = 0; j < c[i].length; j++) out.push({ closed: true, p: projLine(c[i][j]) }); }
      else if (t === 'LineString') out.push({ closed: false, p: projLine(c) });
      else if (t === 'MultiLineString') { for (i = 0; i < c.length; i++) out.push({ closed: false, p: projLine(c[i]) }); }
      else if (t === 'GeometryCollection') { for (i = 0; i < (g.geometries || []).length; i++) projGeom(g.geometries[i], out); }
      return out;
    }
    // Décimation par distance (O(n)), tolérance en km
    function pathOf(lines, tol) {
      var t2 = tol * tol, d = [];
      for (var i = 0; i < lines.length; i++) {
        var p = lines[i].p, n = p.length; if (n < 4) continue;
        var lx = p[0], ly = p[1], s = 'M' + round1(lx) + ' ' + round1(ly);
        for (var j = 2; j < n; j += 2) {
          var x = p[j], y = p[j + 1], last = j >= n - 2;
          var dx = x - lx, dy = y - ly;
          if (dx * dx + dy * dy >= t2 || last) { s += 'L' + round1(x) + ' ' + round1(y); lx = x; ly = y; }
        }
        d.push(s + (lines[i].closed ? 'Z' : ''));
      }
      return d.join('');
    }
    function roadTier(k) {
      if (typeof k === 'number') return k <= 1 ? 1 : k === 2 ? 2 : 3;
      k = String(k || '').toLowerCase();
      if (/^(1|a|motorway|trunk|primary|major|highway|national)/.test(k)) return 1;
      if (/^(2|b|secondary|regional)/.test(k)) return 2;
      return 3;
    }

    // ---------- chargement ----------
    function fetchJson(url) {
      return fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    }
    function setCountry(iso3) {
      var tk = ++token;
      iso3 = String(iso3 || '').trim();
      if (!/^[A-Za-z0-9_-]{2,8}$/.test(iso3)) { showStatus(L.error); return Promise.resolve(null); }
      showStatus(L.loading); hideTip();
      return fetchJson(dataBase + iso3.toUpperCase() + '.json').catch(function () { return fetchJson(dataBase + iso3.toLowerCase() + '.json'); })
        .then(function (d) {
          if (tk !== token || destroyed) return null;
          build(d);
          if (opts.onCountryLoaded) { try { opts.onCountryLoaded(d); } catch (e) { /* hôte */ } }
          return d;
        }, function () { if (tk === token) { clearAll(); showStatus(L.error); if (opts.onError) { try { opts.onError(iso3); } catch (e) { /* hôte */ } } } return null; });
    }
    function showStatus(msg) { status.textContent = msg; status.hidden = !msg; }
    function clearAll() {
      data = null; pts = []; geo = null; active = -1;
      [gLand, gLakes, gRegions, gBorder, gRail].concat(gRoads).forEach(function (p) { p.setAttribute('d', ''); });
      Object.keys(layerGroups).forEach(function (k) { layerGroups[k].textContent = ''; });
      lblRoot.textContent = ''; svgTitle.textContent = L.none; svgDesc.textContent = ''; title.textContent = L.none;
      LAYERS.forEach(function (n) { counts[n].textContent = ''; });
    }

    function build(d) {
      clearAll(); data = d || {};
      var bb = data.view || data.bbox || [-180, -90, 180, 90];
      lon0 = (bb[0] + bb[2]) / 2; if (bb[2] < bb[0]) lon0 = ((bb[0] + bb[2] + 360) / 2 + 180) % 360 - 180;
      lat0 = (bb[1] + bb[3]) / 2; cosL = Math.max(0.05, Math.cos(lat0 * RAD));
      var name = (lang === 'fr' ? data.name_fr : data.name_en) || data.name_en || data.name_fr || data.iso3 || '';
      title.textContent = name;
      var ly = data.layers || {};
      geo = {
        border: projGeom(data.border, []), regions: [], lakes: [], rail: [], roads: [[], [], []]
      };
      (data.admin1 || []).forEach(function (a) { projGeom(a && a.geometry, geo.regions); });
      (ly.lakes || []).forEach(function (g) { projGeom(g, geo.lakes); });
      (ly.railways || []).forEach(function (c) { geo.rail.push({ closed: false, p: projLine(c) }); });
      (ly.roads || []).forEach(function (r) { if (r && r.c) geo.roads[roadTier(r.k) - 1].push({ closed: false, p: projLine(r.c) }); });
      geo.nRoads = geo.roads[0].length + geo.roads[1].length + geo.roads[2].length;

      // étendue : frontière, à défaut bbox
      var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      if (data.view) { var va = proj(bb[0], bb[3]), vb = proj(bb[2], bb[1]); x0 = va[0]; y0 = va[1]; x1 = vb[0]; y1 = vb[1]; }
      else geo.border.forEach(function (l) { for (var i = 0; i < l.p.length; i += 2) { var x = l.p[i], y = l.p[i + 1]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } });
      if (!isFinite(x0)) { var a = proj(bb[0], bb[3]), b = proj(bb[2], bb[1]); x0 = a[0]; y0 = a[1]; x1 = b[0]; y1 = b[1]; }
      if (x1 - x0 < 1) { x0 -= 5; x1 += 5; } if (y1 - y0 < 1) { y0 -= 5; y1 += 5; }
      extent = [x0, y0, x1, y1];
      gLand.setAttribute('d', pathOf(geo.border, 0)); // sera redessiné au rendu

      // points
      pts = [];
      function addPts(kind, arr, mk) {
        var g = layerGroups[kind];
        (arr || []).forEach(function (r) {
          if (!r || !isFinite(r[0]) || !isFinite(r[1])) return;
          var p = proj(r[0], r[1]), o = mk(r);
          o.x = p[0]; o.y = p[1]; o.layer = kind; o.kind = o.cap ? 'capital' : kind === 'cities' ? 'city' : kind === 'airports' ? 'airport' : 'port';
          var ge = el('g', { 'class': 'am-pt ' + o.kind }, g);
          el('circle', { 'class': 'am-hit', r: 11 }, ge);
          var sc = o.kind === 'capital' ? 1.15 : o.kind === 'city' ? 0.9 + Math.min(0.5, Math.log10(Math.max(o.pop, 1000) / 1000) * 0.1) : o.kind === 'airport' ? 1 : 0.95;
          el('path', { 'class': 'am-sym', d: SYM[o.kind], transform: 'scale(' + sc.toFixed(2) + ')' }, ge);
          o.g = ge; o.idx = pts.length; ge.__pt = o.idx; pts.push(o);
        });
      }
      addPts('airports', ly.airports, function (r) { return { name: String(r[2] || ''), sub: String(r[3] || ''), pop: 0, rank: 3 }; });
      addPts('ports', ly.ports, function (r) { return { name: String(r[2] || ''), sub: '', pop: 0, rank: 4 }; });
      addPts('cities', ly.cities, function (r) { var pop = +r[3] || 0, cap = !!r[4]; return { name: String(r[2] || ''), sub: '', pop: pop, cap: cap, rank: cap ? 0 : 1 }; });

      var c = data.counts || {};
      ['airports', 'ports', 'cities'].forEach(function (n) { counts[n].textContent = nf.format(n === 'cities' ? (ly[n] || []).length : (c[n] != null ? c[n] : (ly[n] || []).length)); });
      counts.roads.textContent = c.roads_km != null ? nf.format(Math.round(c.roads_km)) + ' km' : '';
      counts.rail.textContent = c.railways_km != null ? nf.format(Math.round(c.railways_km)) + ' km' : '';
      counts.lakes.textContent = (ly.lakes || []).length ? nf.format(ly.lakes.length) : '';
      counts.regions.textContent = (data.admin1 || []).length ? nf.format(data.admin1.length) : '';
      var parts = [];
      ['airports', 'ports', 'cities', 'railways_km', 'roads_km'].forEach(function (k) { if (c[k] != null) parts.push(nf.format(Math.round(c[k])) + ' ' + L.ctrs[k]); });
      svgTitle.textContent = name;
      svgDesc.textContent = L.alt(name, parts.join(', '));

      showStatus('');
      measure(); recenter(false); applyVisibility();
      live.textContent = L.alt(name, parts.join(', '));
    }

    // ---------- vue ----------
    function measure() {
      var r = stage.getBoundingClientRect(); W = Math.max(50, r.width); H = Math.max(50, r.height);
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      if (extent) {
        var pad = Math.min(36, W * 0.06);
        s0 = Math.min((W - 2 * pad) / (extent[2] - extent[0]), (H - 2 * pad) / (extent[3] - extent[1]));
        home = { cx: (extent[0] + extent[2]) / 2, cy: (extent[1] + extent[3]) / 2, k: 1 };
      }
    }
    function limitView(v) {
      if (!extent) return v;
      v.k = clamp(v.k, 0.6, MAXK);
      var s = s0 * v.k, mx = (W / 2) / s, my = (H / 2) / s;
      v.cx = clamp(v.cx, extent[0] - mx * 0.5, extent[2] + mx * 0.5);
      v.cy = clamp(v.cy, extent[1] - my * 0.5, extent[3] + my * 0.5);
      return v;
    }
    function recenter(animate) { if (home) go({ cx: home.cx, cy: home.cy, k: 1 }, animate); }
    function go(target, animate) {
      limitView(target);
      cancelAnimationFrame(anim);
      if (!animate || (reduce && reduce.matches)) { view = target; schedule(); return; }
      var from = { cx: view.cx, cy: view.cy, k: view.k }, t0 = performance.now(), dur = 260;
      (function step(now) {
        var t = clamp((now - t0) / dur, 0, 1), e = t * (2 - t);
        view = { cx: from.cx + (target.cx - from.cx) * e, cy: from.cy + (target.cy - from.cy) * e, k: Math.exp(Math.log(from.k) + (Math.log(target.k) - Math.log(from.k)) * e) };
        schedule();
        if (t < 1) anim = requestAnimationFrame(step);
      })(t0);
    }
    function zoomAt(f, px, py, animate) {
      if (!data) return;
      var s = s0 * view.k, wx = view.cx + (px - W / 2) / s, wy = view.cy + (py - H / 2) / s;
      var k = clamp(view.k * f, 0.6, MAXK), s2 = s0 * k;
      go({ cx: wx - (px - W / 2) / s2, cy: wy - (py - H / 2) / s2, k: k }, animate);
    }
    function zoomBy(f) { zoomAt(f, W / 2, H / 2, true); }
    function panBy(dx, dy) { var s = s0 * view.k; go({ cx: view.cx + dx / s, cy: view.cy + dy / s, k: view.k }, false); }

    function schedule() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; render(); }); }

    function applyVisibility() {
      var v = visible;
      gBorder.style.display = gLand.style.display = v.borders ? '' : 'none';
      gRegions.style.display = v.regions ? '' : 'none';
      gRail.style.display = v.rail ? '' : 'none';
      gLakes.style.display = v.lakes ? '' : 'none';
      ['airports', 'ports', 'cities'].forEach(function (n) { layerGroups[n].style.display = v[n] ? '' : 'none'; });
      bucket = -99; schedule();
    }

    function render() {
      if (!geo || destroyed) return;
      var s = s0 * view.k;
      world.setAttribute('transform', 'translate(' + (W / 2 - view.cx * s) + ' ' + (H / 2 - view.cy * s) + ') scale(' + s + ')');
      var b = Math.round(Math.log(s / s0) / Math.LN2 * 3);
      if (b !== bucket) {
        bucket = b;
        var tol = 0.9 / s; // km correspondant à ~0,9 px
        if (visible.borders) { var dB = pathOf(geo.border, tol); gBorder.setAttribute('d', dB); gLand.setAttribute('d', dB); }
        if (visible.regions) gRegions.setAttribute('d', pathOf(geo.regions, tol * 1.5));
        if (visible.lakes) gLakes.setAttribute('d', pathOf(geo.lakes, tol));
        if (visible.rail) gRail.setAttribute('d', pathOf(geo.rail, tol * 1.3));
        var z = view.k, few = geo.nRoads <= 700;
        gRoads.forEach(function (p, i) {
          var show = visible.roads && (i === 0 || few || (i === 1 && z >= 1.6) || (i === 2 && z >= 3));
          p.setAttribute('d', show ? pathOf(geo.roads[i], tol * 1.3) : '');
        });
      }
      // points + libellés
      var x0 = -20, y0 = -20, x1 = W + 20, y1 = H + 20, i, p, sx, sy;
      for (i = 0; i < pts.length; i++) {
        p = pts[i]; sx = W / 2 + (p.x - view.cx) * s; sy = H / 2 + (p.y - view.cy) * s; p.sx = sx; p.sy = sy;
        p.on = sx >= x0 && sx <= x1 && sy >= y0 && sy <= y1;
        if (p.on) { p.g.setAttribute('transform', 'translate(' + sx.toFixed(1) + ' ' + sy.toFixed(1) + ')'); if (p.hid) { p.g.style.display = ''; p.hid = false; } }
        else if (!p.hid) { p.g.style.display = 'none'; p.hid = true; }
      }
      drawLabels();
      updateScale(s);
      if (tip.hidden === false && tipPt != null) placeTip(pts[tipPt]);
    }

    function drawLabels() {
      lblRoot.textContent = '';
      if (!visible.cities) return;
      var cands = [];
      for (var i = 0; i < pts.length; i++) if (pts[i].layer === 'cities' && pts[i].on && pts[i].name) cands.push(pts[i]);
      cands.sort(function (a, b) { return (a.rank - b.rank) || (b.pop - a.pop); });
      var max = Math.round(7 + 6 * Math.log2(Math.max(view.k, 1)) + (W > 700 ? 4 : 0)), placed = [], n = 0;
      for (var j = 0; j < cands.length && n < max; j++) {
        var p = cands[j], w = p.name.length * 6.6 + 4, hh = 13, sx = p.sx, sy = p.sy;
        var spots = [[sx + 8, sy - 6], [sx - 8 - w, sy - 6], [sx - w / 2, sy - 22], [sx - w / 2, sy + 9]];
        for (var q = 0; q < spots.length; q++) {
          var r = { x: spots[q][0], y: spots[q][1], w: w, h: hh };
          if (r.x < 2 || r.y < 2 || r.x + w > W - 2 || r.y + hh > H - 2) continue;
          var hit = false;
          for (var m = 0; m < placed.length; m++) { var o = placed[m]; if (r.x < o.x + o.w && r.x + r.w > o.x && r.y < o.y + o.h && r.y + r.h > o.y) { hit = true; break; } }
          if (hit) continue;
          placed.push(r); n++;
          var t = el('text', { 'class': 'am-lbl' + (p.cap ? ' cap' : ''), x: r.x, y: r.y + 10, 'aria-hidden': 'true' }, lblRoot);
          t.textContent = p.name; break;
        }
      }
    }

    function updateScale(s) {
      var target = 90 / s, pow = Math.pow(10, Math.floor(Math.log10(target))), best = pow;
      [1, 2, 5, 10].forEach(function (m) { if (pow * m <= target * 1.2) best = pow * m; });
      scaleBar.style.width = (best * s).toFixed(0) + 'px';
      scaleTxt.textContent = nf.format(best) + ' km';
    }

    // ---------- infobulle / points ----------
    var tipPt = null;
    function tipContent(p) {
      tip.textContent = '';
      h('b', null, tip, p.name || L[p.kind]);
      var sub = L[p.kind];
      if (p.kind === 'airport' && p.sub) sub = L.types[p.sub] || p.sub.replace(/_/g, ' ');
      if (p.layer === 'cities' && p.pop) sub += ' · ' + nf.format(p.pop) + ' ' + L.pop;
      h('span', null, tip, sub);
      return (p.name || L[p.kind]) + ', ' + sub;
    }
    function placeTip(p) {
      var demi = Math.min((tip.offsetWidth || 240) / 2 + 4, W / 2); tip.style.left = clamp(p.sx, demi, W - demi) + 'px';
      var top = p.sy; tip.style.top = Math.max(top, 44) + 'px';
    }
    function showTip(idx, announce) {
      var p = pts[idx]; if (!p || !p.on) return;
      tipPt = idx; var txt = tipContent(p); tip.hidden = false; placeTip(p);
      if (announce) live.textContent = txt;
    }
    function hideTip() {
      tipPt = null; tip.hidden = true;
      if (active >= 0 && pts[active]) pts[active].g.classList.remove('am-active');
      active = -1; svg.removeAttribute('aria-activedescendant');
    }
    function ptOf(t) { while (t && t !== svg) { if (t.__pt != null) return t.__pt; t = t.parentNode; } return null; }
    function setActive(idx, announce) {
      if (active >= 0 && pts[active]) pts[active].g.classList.remove('am-active');
      active = idx;
      if (idx < 0) { hideTip(); return; }
      var p = pts[idx];
      p.g.classList.add('am-active');
      if (!p.on || p.sx < 30 || p.sx > W - 30 || p.sy < 30 || p.sy > H - 30) { go({ cx: p.x, cy: p.y, k: view.k }, true); setTimeout(function () { showTip(idx, announce); }, reduce && reduce.matches ? 30 : 300); }
      else showTip(idx, announce);
    }
    function navigable() {
      var a = [];
      pts.forEach(function (p) { if (visible[p.layer] && p.on) a.push(p.idx); });
      a.sort(function (i, j) { var p = pts[i], q = pts[j]; return (p.rank - q.rank) || (q.pop - p.pop) || (p.name < q.name ? -1 : 1); });
      return a;
    }
    function step(dir) {
      var list = navigable(); if (!list.length) { live.textContent = L.noPoints; return; }
      var pos = list.indexOf(active); pos = pos < 0 ? (dir > 0 ? 0 : list.length - 1) : (pos + dir + list.length) % list.length;
      setActive(list[pos], true);
    }

    // ---------- interactions ----------
    var ptrs = new Map(), drag = null, pinch = null, moved = false;
    function local(e) { var r = svg.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
    function onDown(e) {
      if (!data) return;
      ptrs.set(e.pointerId, local(e)); moved = false;
      if (ptrs.size === 1) { drag = { x: e.clientX, y: e.clientY, cx: view.cx, cy: view.cy, id: e.pointerId, cap: false }; }
      else if (ptrs.size === 2) {
        var a = Array.from(ptrs.values()); drag = null;
        pinch = { d: Math.hypot(a[0][0] - a[1][0], a[0][1] - a[1][1]) || 1, k: view.k, mx: (a[0][0] + a[1][0]) / 2, my: (a[0][1] + a[1][1]) / 2 };
        try { svg.setPointerCapture(e.pointerId); } catch (x) { /* ok */ }
      }
    }
    function onMove(e) {
      if (ptrs.has(e.pointerId)) ptrs.set(e.pointerId, local(e));
      if (pinch && ptrs.size >= 2) {
        var a = Array.from(ptrs.values()), d = Math.hypot(a[0][0] - a[1][0], a[0][1] - a[1][1]) || 1;
        var mx = (a[0][0] + a[1][0]) / 2, my = (a[0][1] + a[1][1]) / 2;
        var k = clamp(pinch.k * d / pinch.d, 0.6, MAXK);
        // ancre : point monde sous le milieu initial reste sous le milieu courant
        var s = s0 * view.k, wx = view.cx + (pinch.mx - W / 2) / s, wy = view.cy + (pinch.my - H / 2) / s, s2 = s0 * k;
        view = limitView({ cx: wx - (mx - W / 2) / s2, cy: wy - (my - H / 2) / s2, k: k });
        pinch.mx = mx; pinch.my = my; pinch.d = d; pinch.k = k; moved = true; schedule(); return;
      }
      if (drag && e.pointerId === drag.id) {
        var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
        if (!moved && Math.hypot(dx, dy) < 5) return;
        if (!moved) { moved = true; hideTipSoft(); svg.classList.add('am-drag'); try { svg.setPointerCapture(e.pointerId); } catch (x) { /* ok */ } }
        var s2 = s0 * view.k; view = limitView({ cx: drag.cx - dx / s2, cy: drag.cy - dy / s2, k: view.k }); schedule();
      } else if (e.pointerType === 'mouse' && !ptrs.size) {
        var i = ptOf(e.target); if (i != null && pts[i] && pts[i].on) showTip(i, false); else if (tipPt != null && active < 0) { tipPt = null; tip.hidden = true; }
      }
    }
    function hideTipSoft() { tipPt = null; tip.hidden = true; }
    function onUp(e) {
      var wasDrag = drag && e.pointerId === drag.id;
      ptrs.delete(e.pointerId);
      if (ptrs.size < 2) pinch = null;
      if (!ptrs.size) {
        svg.classList.remove('am-drag');
        if (wasDrag && !moved && e.type === 'pointerup') { // tap : ouvrir l'infobulle
          var i = ptOf(e.target);
          if (i != null) { if (active >= 0 && pts[active]) pts[active].g.classList.remove('am-active'); active = i; pts[i].g.classList.add('am-active'); showTip(i, true); }
          else hideTip();
        }
        drag = null;
      } else if (ptrs.size === 1) { var id = ptrs.keys().next().value, pp = ptrs.get(id); drag = { x: pp[0] + svg.getBoundingClientRect().left, y: pp[1] + svg.getBoundingClientRect().top, cx: view.cx, cy: view.cy, id: id }; moved = true; }
    }
    function onWheel(e) {
      if (!data) return; e.preventDefault();
      var p = local(e), f = Math.exp(-e.deltaY * (e.deltaMode === 1 ? 0.05 : 0.0016) * (e.ctrlKey ? 2.5 : 1));
      zoomAt(f, p[0], p[1], false);
    }
    function onDbl(e) { if (!data) return; var p = local(e); zoomAt(2, p[0], p[1], true); }
    function onKey(e) {
      if (!data || e.altKey || e.ctrlKey || e.metaKey) return;
      var st = Math.min(W, H) * 0.2, handled = true;
      switch (e.key) {
        case 'ArrowLeft': panBy(-st, 0); break; case 'ArrowRight': panBy(st, 0); break;
        case 'ArrowUp': panBy(0, -st); break; case 'ArrowDown': panBy(0, st); break;
        case '+': case '=': zoomBy(1.6); break; case '-': case '_': zoomBy(1 / 1.6); break;
        case '0': recenter(true); break;
        case 'n': case 'N': step(e.shiftKey ? -1 : 1); break; case 'p': case 'P': step(-1); break;
        case 'Escape': hideTip(); break;
        default: handled = false;
      }
      if (handled) e.preventDefault();
    }
    svg.addEventListener('pointerdown', onDown);
    svg.addEventListener('pointermove', onMove);
    svg.addEventListener('pointerup', onUp);
    svg.addEventListener('pointercancel', onUp);
    svg.addEventListener('wheel', onWheel, { passive: false });
    svg.addEventListener('dblclick', onDbl);
    svg.addEventListener('keydown', onKey);
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && active < 0) hideTipSoft(); });
    svg.addEventListener('blur', function () { if (active >= 0) hideTip(); });

    var ro = global.ResizeObserver ? new ResizeObserver(function () { if (destroyed) return; var ow = W, oh = H; measure(); if (data && (Math.abs(ow - W) > 1 || Math.abs(oh - H) > 1)) { bucket = -99; view = limitView(view); schedule(); } }) : null;
    if (ro) ro.observe(stage);
    measure(); showStatus(L.none); updateScale(1);

    function setLayerVisible(name, on) {
      if (LAYERS.indexOf(name) < 0) return;
      visible[name] = !!on; if (checks[name]) checks[name].checked = !!on;
      if (!on && active >= 0 && pts[active] && pts[active].layer === name) hideTip();
      if (!on) { var m = { borders: [gBorder, gLand], regions: [gRegions], rail: [gRail], lakes: [gLakes], roads: gRoads }[name]; if (m) m.forEach(function (p) { p.setAttribute('d', ''); }); }
      applyVisibility();
    }
    function destroy() {
      destroyed = true; token++; cancelAnimationFrame(raf); cancelAnimationFrame(anim);
      if (ro) ro.disconnect(); container.textContent = '';
    }
    return { setCountry: setCountry, setLayerVisible: setLayerVisible, destroy: destroy };
  }

  global.AtlasMap = { mount: mount, version: '1.0.0' };
})(typeof window !== 'undefined' ? window : this);
