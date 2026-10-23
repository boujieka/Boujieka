/* ENERVIA vitrine — langue, menu mobile et assistant de diagnostic. */
(function () {
  "use strict";
  var PLATFORM = "https://enervia-energy-journey.lovable.app";

  // ---------------------------------------------------------------- langue
  var EN = window.ENERVIA_EN || {};
  function storeGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function storeSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* stockage indisponible */ } }
  var lang = storeGet("enervia-lang") === "en" ? "en" : "fr";

  function applyLang() {
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      if (el.dataset.fr === undefined) el.dataset.fr = el.innerHTML;
      var key = el.getAttribute("data-i18n");
      el.innerHTML = lang === "en" && EN[key] ? EN[key] : el.dataset.fr;
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      if (el.dataset.frPh === undefined) el.dataset.frPh = el.getAttribute("placeholder") || "";
      var key = el.getAttribute("data-i18n-ph");
      el.setAttribute("placeholder", lang === "en" && EN[key] ? EN[key] : el.dataset.frPh);
    });
    document.querySelectorAll(".lang").forEach(function (b) { b.textContent = lang === "en" ? "FR" : "EN"; b.setAttribute("aria-label", lang === "en" ? "Passer en français" : "Switch to English"); });
    if (typeof window.onLangChange === "function") window.onLangChange(lang);
  }
  document.querySelectorAll(".lang").forEach(function (b) {
    b.addEventListener("click", function () { lang = lang === "en" ? "fr" : "en"; storeSet("enervia-lang", lang); applyLang(); });
  });
  window.ENERVIA_LANG = function () { return lang; };

  // ---------------------------------------------------------------- menu mobile
  var menuBtn = document.querySelector(".menu-btn"), nav = document.querySelector(".nav");
  if (menuBtn && nav) menuBtn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.querySelectorAll("[data-platform]").forEach(function (a) { a.href = PLATFORM + a.getAttribute("data-platform"); });
  var y = document.getElementById("year"); if (y) y.textContent = String(new Date().getFullYear());

  applyLang();
})();
