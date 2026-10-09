// Courant platform client: Supabase magic-link sign-in, tier display, gated downloads.
// Config (public values only) comes from /assets/config.js: window.COURANT = { supabaseUrl, supabaseAnonKey }.
(function () {
  var cfg = window.COURANT || {};
  var sb = (window.supabase && cfg.supabaseUrl && cfg.supabaseAnonKey) ? window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseAnonKey) : null;
  var TIER_LABEL = { public: 'Public', registered: 'Inscrit', institutional: 'Institutionnel' };

  async function session() { if (!sb) return null; var r = await sb.auth.getSession(); return r.data.session; }
  async function tierOf(s) {
    if (!s) return 'public';
    var r = await sb.from('profiles').select('tier').eq('id', s.user.id).maybeSingle();
    return (r.data && r.data.tier) || 'registered';
  }
  var RANK = { public: 0, registered: 1, institutional: 2 };

  async function paintAccount() {
    var el = document.getElementById('acct');
    var s = await session();
    var t = await tierOf(s);
    if (el) el.textContent = s ? ('Compte · ' + TIER_LABEL[t]) : 'Se connecter';
    document.querySelectorAll('[data-need]').forEach(function (b) {
      var need = b.getAttribute('data-need');
      var ok = RANK[t] >= RANK[need];
      var msg = b.closest('.dl') && b.closest('.dl').querySelector('.msg');
      b.disabled = !ok && need !== 'public';
      if (msg) msg.textContent = ok ? '' : (s ? 'Réservé au niveau ' + TIER_LABEL[need] + '. Demandez l’accès depuis votre compte.' : 'Connectez-vous pour télécharger.');
    });
    return { s: s, t: t };
  }

  async function download(path, name, btn) {
    var s = await session();
    var msg = btn.closest('.dl').querySelector('.msg');
    if (!s) { msg.textContent = 'Connectez-vous pour télécharger.'; return; }
    msg.textContent = 'Préparation du fichier…';
    try {
      var r = await fetch('/.netlify/functions/download?path=' + encodeURIComponent(path), { headers: { Authorization: 'Bearer ' + s.access_token } });
      if (r.status === 403) { msg.textContent = 'Votre niveau d’accès ne permet pas ce téléchargement.'; return; }
      if (!r.ok) { msg.textContent = 'Le téléchargement a échoué (' + r.status + '). Réessayez plus tard.'; return; }
      var blob = await r.blob();
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 5000);
      msg.textContent = 'Téléchargé.';
    } catch (e) { msg.textContent = 'Le téléchargement a échoué. Vérifiez votre connexion.'; }
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-path]');
    if (b) { e.preventDefault(); download(b.getAttribute('data-path'), b.getAttribute('data-name'), b); }
  });

  // account page
  var form = document.getElementById('login-form');
  if (form) {
    var st = document.getElementById('login-status');
    if (!sb) { st.hidden = false; st.textContent = 'La connexion n’est pas encore configurée sur ce site.'; form.querySelector('button').disabled = true; }
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var email = document.getElementById('email').value.trim();
      var org = document.getElementById('org').value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { st.hidden = false; st.textContent = 'Cette adresse e-mail ne semble pas valide.'; return; }
      var r = await sb.auth.signInWithOtp({ email: email, options: { emailRedirectTo: location.origin + '/compte.html', data: { organisation: org } } });
      st.hidden = false;
      st.textContent = r.error ? ('Envoi impossible : ' + r.error.message) : 'Lien de connexion envoyé à ' + email + '. Ouvrez-le depuis cette même machine.';
    });
  }
  var out = document.getElementById('logout');
  if (out) out.addEventListener('click', async function () { await sb.auth.signOut(); location.reload(); });

  paintAccount().then(function (x) {
    var who = document.getElementById('who');
    if (who) {
      document.getElementById('signed-in').hidden = !x.s;
      document.getElementById('signed-out').hidden = !!x.s;
      if (x.s) who.textContent = x.s.user.email + ' · niveau ' + TIER_LABEL[x.t];
    }
  });
  if (sb) sb.auth.onAuthStateChange(function () { paintAccount(); });
})();
