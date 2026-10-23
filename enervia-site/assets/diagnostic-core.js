/*
 * ENERVIA — Diagnostic express : calculs purs (aucun appel réseau).
 * Règles :
 *  - un champ vide reste « manquant » ; il n'est jamais remplacé par zéro en silence ;
 *  - une source d'énergie que l'utilisateur déclare ne pas utiliser vaut 0 (déclaré) ;
 *  - le rendement des groupes a une valeur type modifiable (3,5 kWh/L), toujours signalée « estimée » ;
 *  - facteur d'émission du gasoil : 2,68 kg CO2/L (combustion stationnaire, valeurs par défaut GIEC 2006).
 */
(function (root) {
  "use strict";

  var DIESEL_KG_CO2_PER_L = 2.68;
  var DEFAULT_KWH_PER_L = 3.5;

  /** Lit un nombre saisi en français ou en anglais : « 25 000 », « 25.000 », « 0,28 », « 1 234,5 ». */
  function parseNumber(raw) {
    if (raw === null || raw === undefined) return { state: "missing" };
    var s = String(raw).trim().replace(/[\s  ]/g, "");
    if (s === "") return { state: "missing" };
    var hasComma = s.indexOf(",") >= 0, hasDot = s.indexOf(".") >= 0;
    if (hasComma && hasDot) {
      // Le dernier séparateur est la décimale : « 1.234,5 » ou « 1,234.5 ».
      if (s.lastIndexOf(",") > s.lastIndexOf(".")) s = s.replace(/\./g, "").replace(",", ".");
      else s = s.replace(/,/g, "");
    } else if (hasComma || hasDot) {
      var sep = hasComma ? "," : ".";
      // Séparateur de milliers : groupes de 3 chiffres et partie entière ≠ 0 (« 25 000 », « 25.000 », « 1,250,000 »).
      var thousands = new RegExp("^[1-9]\\d{0,2}(\\" + sep + "\\d{3})+$");
      s = thousands.test(s) ? s.split(sep).join("") : s.replace(sep, ".");
    }
    if (!/^\d+(\.\d+)?$/.test(s)) return { state: "invalid" };
    var n = Number(s);
    if (!isFinite(n) || n < 0) return { state: "invalid" };
    return { state: "ok", value: n };
  }

  function annual(v, period) { return v == null ? null : (period === "month" ? v * 12 : v); }
  function num(raw) { var p = parseNumber(raw); return p.state === "ok" ? p.value : null; }

  /**
   * inputs = {
   *   supply: "grid" | "diesel" | "both",
   *   grid:   { mode: "amount" | "kwh", amount, kwh, tariff, period: "month" | "year" },
   *   diesel: { mode: "litres" | "spend", litres, spend, price, period, kwhPerL }
   * } — les valeurs sont des chaînes saisies.
   */
  function compute(inputs) {
    var errors = [], missing = [];
    var useGrid = inputs.supply === "grid" || inputs.supply === "both";
    var useDiesel = inputs.supply === "diesel" || inputs.supply === "both";
    if (!useGrid && !useDiesel) errors.push("supply");

    function field(key, raw) {
      var p = parseNumber(raw);
      if (p.state === "invalid") { errors.push(key); return null; }
      return p.state === "ok" ? p.value : null;
    }

    var gridCost = 0, gridKwh = 0, gridDeclaredZero = !useGrid;
    if (useGrid) {
      var g = inputs.grid || {};
      var gp = g.period === "month" ? "month" : "year";
      if (g.mode === "kwh") {
        var k = annual(field("grid_kwh", g.kwh), gp);
        var t = field("grid_tariff", g.tariff);
        if (k == null) missing.push("grid_kwh");
        if (t == null) missing.push("grid_tariff");
        gridKwh = k;
        gridCost = k != null && t != null ? k * t : null;
      } else {
        var a = annual(field("grid_amount", g.amount), gp);
        var k2 = annual(field("grid_kwh_optional", g.kwh), gp);
        if (a == null) missing.push("grid_amount");
        gridCost = a;
        gridKwh = k2; // facultatif : sans kWh, pas de coût par kWh
      }
    }

    var dieselCost = 0, dieselL = 0, dieselKwh = 0, kwhPerL = null, kwhPerLDefault = false;
    if (useDiesel) {
      var d = inputs.diesel || {};
      var dp = d.period === "month" ? "month" : "year";
      var price = field("diesel_price", d.price);
      kwhPerL = field("kwh_per_l", d.kwhPerL);
      if (kwhPerL == null) { kwhPerL = DEFAULT_KWH_PER_L; kwhPerLDefault = true; }
      if (kwhPerL <= 0) { errors.push("kwh_per_l"); kwhPerL = null; }
      if (d.mode === "spend") {
        var sp = annual(field("diesel_spend", d.spend), dp);
        if (sp == null) missing.push("diesel_spend");
        dieselCost = sp;
        dieselL = sp != null && price ? sp / price : null;
        if (price == null) missing.push("diesel_price_for_litres");
      } else {
        var L = annual(field("diesel_litres", d.litres), dp);
        if (L == null) missing.push("diesel_litres");
        if (price == null) missing.push("diesel_price");
        dieselL = L;
        dieselCost = L != null && price != null ? L * price : null;
      }
      dieselKwh = dieselL != null && kwhPerL ? dieselL * kwhPerL : null;
    }

    var totalCost = gridCost != null && dieselCost != null ? gridCost + dieselCost : null;
    var totalKwh = gridKwh != null && dieselKwh != null ? gridKwh + dieselKwh : null;
    var costPerKwh = totalCost != null && totalKwh ? totalCost / totalKwh : null;
    var dieselShareCost = totalCost ? (dieselCost || 0) / totalCost : null;
    var co2 = useDiesel ? (dieselL != null ? (dieselL * DIESEL_KG_CO2_PER_L) / 1000 : null) : 0;

    return {
      ok: errors.length === 0,
      errors: errors,
      missing: missing,
      useGrid: useGrid,
      useDiesel: useDiesel,
      gridDeclaredZero: gridDeclaredZero,
      gridCost: gridCost, gridKwh: gridKwh,
      dieselCost: dieselCost, dieselL: dieselL, dieselKwh: dieselKwh,
      kwhPerL: kwhPerL, kwhPerLDefault: kwhPerLDefault,
      totalCost: totalCost, totalKwh: totalKwh, costPerKwh: costPerKwh,
      dieselShareCost: dieselShareCost,
      dieselCo2T: co2,
      hasResult: totalCost != null && totalCost > 0
    };
  }

  var api = { parseNumber: parseNumber, compute: compute, DEFAULT_KWH_PER_L: DEFAULT_KWH_PER_L, DIESEL_KG_CO2_PER_L: DIESEL_KG_CO2_PER_L, num: num };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.EnerviaDiag = api;
})(this);
