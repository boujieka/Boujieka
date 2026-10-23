/* ENERVIA — Diagnostic express : interface en 3 étapes. Tout est calculé dans le navigateur. */
(function () {
  "use strict";
  var D = window.EnerviaDiag, EN = window.ENERVIA_EN || {};
  var $ = function (id) { return document.getElementById(id); };
  var step = 1, last = null;
  var state = { gridMode: "amount", gridPeriod: "month", dieselMode: "litres", dieselPeriod: "month" };

  function L() { return window.ENERVIA_LANG ? window.ENERVIA_LANG() : "fr"; }
  // Texte FR depuis l'élément porteur data-i18n, ou EN depuis le dictionnaire.
  function t(key, fr) { return L() === "en" && EN[key] ? EN[key] : fr; }
  function currency() { return $("currency").value || "XAF"; }
  function fmt(n, digits) {
    if (n == null || !isFinite(n)) return null;
    return new Intl.NumberFormat(L() === "en" ? "en-GB" : "fr-FR", { maximumFractionDigits: digits == null ? 0 : digits }).format(n);
  }
  function money(n) { var s = fmt(n, currency() === "XAF" ? 0 : 2); return s == null ? null : s + " " + currency(); }
  function compact(n) {
    if (n == null || !isFinite(n)) return null;
    if (n >= 1e9) return fmt(n / 1e9, 2) + (L() === "en" ? " bn " : " Md ") + currency();
    if (n >= 1e6) return fmt(n / 1e6, 1) + " M " + currency();
    return money(n);
  }

  function inputs() {
    var supply = (document.querySelector("input[name=supply]:checked") || {}).value || "";
    return {
      supply: supply,
      grid: { mode: state.gridMode, period: state.gridPeriod, amount: $("grid_amount").value, kwh: state.gridMode === "kwh" ? $("grid_kwh").value : $("grid_kwh_opt").value, tariff: $("grid_tariff").value },
      diesel: { mode: state.dieselMode, period: state.dieselPeriod, litres: $("diesel_litres").value, spend: $("diesel_spend").value, price: $("diesel_price").value, kwhPerL: $("kwh_per_l").value }
    };
  }

  // ------------------------------------------------------------ segmented controls
  document.querySelectorAll(".seg").forEach(function (seg) {
    seg.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      seg.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      state[seg.dataset.key] = b.dataset.val;
      syncVisibility(); render();
    });
  });
  function syncVisibility() {
    var s = inputs().supply;
    $("grid-block").classList.toggle("hidden", !(s === "grid" || s === "both"));
    $("diesel-block").classList.toggle("hidden", !(s === "diesel" || s === "both"));
    $("prov-field").classList.toggle("hidden", !s);
    $("grid-amount-fields").classList.toggle("hidden", state.gridMode !== "amount");
    $("grid-kwh-fields").classList.toggle("hidden", state.gridMode !== "kwh");
    $("diesel-litres-fields").classList.toggle("hidden", state.dieselMode !== "litres");
    $("diesel-spend-fields").classList.toggle("hidden", state.dieselMode !== "spend");
    $("price-label").innerHTML = state.dieselMode === "spend" ? t("d.priceOpt", "Prix livré par litre (facultatif, pour estimer les litres et le CO₂)") : t("d.price", "Prix livré par litre");
    document.querySelectorAll("[data-unit=cur]").forEach(function (el) { el.textContent = currency(); });
    document.querySelectorAll("[data-unit=curkwh]").forEach(function (el) { el.textContent = currency() + "/kWh"; });
    document.querySelectorAll("[data-unit=curl]").forEach(function (el) { el.textContent = currency() + "/L"; });
  }

  // ------------------------------------------------------------ result
  function row(label, value, hint) {
    return "<li><span>" + label + "</span><span>" + (value != null ? value : '<em class="muted">' + (hint || t("d.na", "non disponible")) + "</em>") + "</span></li>";
  }
  function render() {
    var r = D.compute(inputs()); last = r;
    var box = $("result-body"), bar = $("mobile-total");
    if (!r.hasResult) {
      box.innerHTML = '<p class="muted">' + t("d.rEmpty", "Saisissez votre consommation pour voir votre résultat.") + "</p>";
      bar.textContent = "—"; return r;
    }
    var h = '<p class="muted">' + t("d.rTotal", "Coût de l'énergie par an") + '</p><p class="big">' + compact(r.totalCost) + "</p><ul class=\"rlist\">";
    if (r.useGrid) h += row(t("d.rGrid", "Électricité réseau"), money(r.gridCost));
    if (r.useDiesel) h += row(t("d.rDiesel", "Gasoil"), money(r.dieselCost));
    if (r.useDiesel) h += row(t("d.rLitres", "Litres de gasoil par an"), r.dieselL != null ? fmt(r.dieselL) + " L" : null, t("d.needPrice", "ajoutez le prix"));
    h += row(t("d.rKwh", "Énergie consommée"), r.totalKwh ? fmt(r.totalKwh) + " kWh" : null, t("d.needKwh", "ajoutez les kWh"));
    h += row(t("d.rPerKwh", "Coût moyen par kWh"), r.costPerKwh != null ? fmt(r.costPerKwh, currency() === "XAF" ? 0 : 3) + " " + currency() + "/kWh" : null, t("d.needKwh", "ajoutez les kWh"));
    if (r.useGrid && r.useDiesel && r.dieselShareCost != null) h += row(t("d.rShare", "Part du gasoil dans le coût"), fmt(r.dieselShareCost * 100) + " %");
    if (r.useDiesel) h += row(t("d.rCo2", "Émissions CO₂ du gasoil"), r.dieselCo2T != null ? fmt(r.dieselCo2T) + " t/an" : null, t("d.needPrice", "ajoutez le prix"));
    h += "</ul>";
    var prov = (document.querySelector("input[name=prov]:checked") || {}).value;
    var trust = prov === "yes" ? t("d.trustBills", "Basé sur vos factures — diagnostic préliminaire") : prov === "part" ? t("d.trustPart", "Basé en partie sur vos factures — diagnostic préliminaire") : t("d.trustDecl", "Estimation basée sur vos chiffres");
    h += '<div class="trust">' + trust + (r.useDiesel && r.kwhPerLDefault ? "<br>" + t("d.effNote", "Rendement des groupes : valeur type 3,5 kWh/L utilisée.") : "") + "</div>";
    box.innerHTML = h;
    bar.textContent = compact(r.totalCost);
    return r;
  }

  // ------------------------------------------------------------ steps
  function showStep(n) {
    step = n;
    [1, 2, 3].forEach(function (i) { $("step" + i).classList.toggle("hidden", i !== n); });
    document.querySelectorAll(".progress span").forEach(function (s, i) { s.classList.toggle("on", i < n); });
    $("step-no").textContent = String(n);
    if (n === 3) { $("lead-summary").value = summary(); }
    var top = document.querySelector(".wizard-main"); if (top && top.scrollIntoView && window.scrollY > 200) top.scrollIntoView({ behavior: "smooth" });
  }
  function clearMarks() { document.querySelectorAll("[aria-invalid=true]").forEach(function (el) { el.removeAttribute("aria-invalid"); el.style.borderColor = ""; }); }
  function mark(id) { var el = $(id); if (el) { el.setAttribute("aria-invalid", "true"); el.style.borderColor = "var(--danger)"; } }

  $("next1").addEventListener("click", function () {
    clearMarks(); var ok = true;
    ["sector", "country"].forEach(function (id) { if (!$(id).value) { mark(id); ok = false; } });
    $("err1").textContent = ok ? "" : t("d.err.required", "Merci de compléter les champs signalés.");
    if (ok) showStep(2);
  });
  $("back2").addEventListener("click", function () { showStep(1); });
  $("back3").addEventListener("click", function () { showStep(2); });
  $("next2").addEventListener("click", function () {
    clearMarks();
    var r = render(), msg = "";
    var idmap = { grid_kwh_optional: "grid_kwh_opt", diesel_price_for_litres: null, kwh_per_l: "kwh_per_l" };
    if (r.errors.indexOf("supply") >= 0) msg = t("d.err.supply", "Choisissez comment votre site est alimenté.");
    else if (r.errors.length) { r.errors.forEach(function (k) { mark(idmap[k] !== undefined ? idmap[k] : k); }); msg = t("d.err.invalid", "Certaines valeurs ne sont pas des nombres valides (chiffres, espaces pour les milliers)."); }
    else if (!r.hasResult) {
      r.missing.forEach(function (k) { if (idmap[k] !== null) mark(idmap[k] || k); });
      msg = t("d.err.required", "Merci de compléter les champs signalés.");
    }
    $("err2").textContent = msg;
    if (!msg) showStep(3);
  });

  // ------------------------------------------------------------ résumé (formulaire et impression)
  function summary() {
    var i = inputs(), r = last || D.compute(i);
    var sel = function (id) { var s = $(id); return s.options[s.selectedIndex] ? s.options[s.selectedIndex].text : ""; };
    var lines = [
      "Secteur: " + sel("sector"), "Pays: " + sel("country") + ($("city").value ? " / " + $("city").value : ""), "Devise: " + currency(),
      "Alimentation: " + i.supply,
      "Réseau (" + i.grid.mode + ", " + i.grid.period + "): montant=" + (i.grid.amount || "-") + " kWh=" + (i.grid.kwh || "-") + " tarif=" + (i.grid.tariff || "-"),
      "Gasoil (" + i.diesel.mode + ", " + i.diesel.period + "): litres=" + (i.diesel.litres || "-") + " dépense=" + (i.diesel.spend || "-") + " prix=" + (i.diesel.price || "-") + " kWh/L=" + (i.diesel.kwhPerL || "3.5 (valeur type)"),
      "Provenance: " + ((document.querySelector("input[name=prov]:checked") || {}).value || "-"),
      "RÉSULTAT coût/an=" + (r.totalCost != null ? Math.round(r.totalCost) : "-") + " kWh/an=" + (r.totalKwh ? Math.round(r.totalKwh) : "-") +
        " coût/kWh=" + (r.costPerKwh != null ? r.costPerKwh.toFixed(2) : "-") + " litres/an=" + (r.dieselL != null ? Math.round(r.dieselL) : "-") + " CO2 t/an=" + (r.dieselCo2T != null ? r.dieselCo2T.toFixed(1) : "-")
    ];
    return lines.join("\n");
  }

  // ------------------------------------------------------------ envoi Netlify Forms
  $("lead-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var f = e.target; $("lead-summary").value = summary();
    if (!f.reportValidity()) return;
    var btn = f.querySelector("button[type=submit]"); btn.disabled = true;
    var body = new URLSearchParams(new FormData(f)).toString();
    fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body })
      .then(function (res) { if (!res.ok) throw new Error(String(res.status)); f.classList.add("hidden"); $("lead-ok").classList.remove("hidden"); })
      .catch(function () { $("lead-err").textContent = t("d.sendErr", "L'envoi a échoué. Réessayez ou utilisez la page contact."); btn.disabled = false; });
  });
  $("print-btn").addEventListener("click", function () {
    $("print-date").textContent = new Date().toLocaleDateString(L() === "en" ? "en-GB" : "fr-FR");
    window.print();
  });

  ["input", "change"].forEach(function (ev) {
    document.querySelector(".wizard-main").addEventListener(ev, function () { syncVisibility(); render(); });
  });
  window.onLangChange = function () { syncVisibility(); render(); };
  syncVisibility(); render();
})();
