/* Old links to the platform (/#marche, /#compte, /?next=…, sign-in returns /#access_token=…) keep working
   now that / is the redesigned home: they live on /plateforme.html. Same rule as the classic home. */
(function () {
  var h = location.hash.slice(1), q = location.search;
  var platform = /^(carte|marche|radar|acheteurs|comparer|acces|bvmac|abonnements|parcours|strategie|brief|rapports|offres|compte|glossaire|methode|veille|sources|feuille|dealers-sub|access_token=|error_description=|[a-z]{3}$)/;
  if ((h && platform.test(h)) || /[?&]next=/.test(q)) location.replace('/plateforme.html' + q + location.hash);
})();
