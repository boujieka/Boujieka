/* ============================================================================
   FI-06 e-learning — Application (SPA vanilla JS)
   Routage · progression persistée · moteur de quiz · examen final
   ==========================================================================*/
(function () {
  "use strict";

  const STORAGE_KEY = "ate-fi06-progress-v1";
  const PASS = COURSE.seuil; // 80

  // ------------------------------------------------------------------ State
  const defaultState = () => ({
    name: "",
    sections: {},        // { s1: {passed:true, score, total} ... }
    exam: null,          // { passed, score, total, pct }
    visited: {}          // { route: true }
  });

  let state = load();

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return Object.assign(defaultState(), JSON.parse(raw));
    } catch (e) { /* ignore */ }
    return defaultState();
  }
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
  }

  // ------------------------------------------------------------------ Routes
  const routes = [
    { id: "accueil", label: "Accueil", sub: "Bienvenue", group: "Parcours", icon: "★" },
    { id: "presentation", label: "Présentation de la formation", sub: "Identité · objectifs", group: "Parcours", icon: "i" }
  ];
  COURSE.sections.forEach(s => routes.push({
    id: s.id, label: s.title, sub: "Section " + s.num, group: "Sections", icon: String(s.num), section: s
  }));
  routes.push({ id: "ressources", label: "Ressources partenaires", sub: "Récapitulatif", group: "Évaluation & ressources", icon: "◇" });
  routes.push({ id: "examen", label: "Examen final", sub: "Seuil " + PASS + " %", group: "Évaluation & ressources", icon: "✎" });
  routes.push({ id: "attestation", label: "Attestation", sub: "Fin de parcours", group: "Évaluation & ressources", icon: "✓" });

  const routeById = Object.fromEntries(routes.map(r => [r.id, r]));

  // ------------------------------------------------------------------ Helpers
  const $ = sel => document.querySelector(sel);
  const view = $("#view");
  const el = (tag, cls, html) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function sectionsDoneCount() {
    return COURSE.sections.filter(s => state.sections[s.id] && state.sections[s.id].passed).length;
  }
  function progressPct() {
    const totalSteps = COURSE.sections.length + 1; // sections + exam
    let done = sectionsDoneCount();
    if (state.exam && state.exam.passed) done += 1;
    return Math.round((done / totalSteps) * 100);
  }
  function allSectionsDone() { return sectionsDoneCount() === COURSE.sections.length; }

  // ------------------------------------------------------------------ Header progress
  function refreshHeaderProgress() {
    const pct = progressPct();
    $("#headerProgressFill").style.width = pct + "%";
    $("#headerProgressLabel").textContent = pct + " %";
  }

  // ------------------------------------------------------------------ Sidebar
  function renderNav() {
    const nav = $("#sideNav");
    nav.innerHTML = "";
    let currentGroup = null;
    routes.forEach(r => {
      if (r.group !== currentGroup) {
        currentGroup = r.group;
        nav.appendChild(el("div", "nav-group-label", r.group));
      }
      const item = el("a", "nav-item");
      item.href = "#" + r.id;
      const done = isRouteDone(r.id);
      if (done) item.classList.add("done");
      item.innerHTML =
        `<span class="nav-ico">${done ? "✓" : esc(r.icon)}</span>` +
        `<span class="nav-txt">${esc(r.label)}<small>${esc(r.sub)}</small></span>`;
      item.dataset.route = r.id;
      nav.appendChild(item);
    });
    highlightNav(current);
  }
  function isRouteDone(id) {
    if (id === "presentation") return !!state.visited.presentation;
    if (routeById[id] && routeById[id].section) return !!(state.sections[id] && state.sections[id].passed);
    if (id === "examen" || id === "attestation") return !!(state.exam && state.exam.passed);
    if (id === "ressources") return !!state.visited.ressources;
    return false;
  }
  function highlightNav(id) {
    document.querySelectorAll(".nav-item").forEach(n =>
      n.classList.toggle("active", n.dataset.route === id));
  }

  // ------------------------------------------------------------------ Router
  let current = "accueil";

  function go(id) {
    if (!routeById[id]) id = "accueil";
    current = id;
    state.visited[id] = true;
    save();
    window.scrollTo({ top: 0 });
    view.innerHTML = "";
    const inner = el("div", "view-inner");
    view.appendChild(inner);
    (renderers[id] || renderers._section)(inner, routeById[id]);
    highlightNav(id);
    renderNav();
    refreshHeaderProgress();
    view.focus();
    closeSidebar();
  }

  function pager(inner, prevId, nextId, nextLabel) {
    const p = el("div", "pager");
    if (prevId) {
      const b = el("a", "btn btn-ghost", "← Précédent");
      b.href = "#" + prevId;
      p.appendChild(b);
    } else { p.appendChild(el("span")); }
    p.appendChild(el("span", "spacer"));
    if (nextId) {
      const b = el("a", "btn btn-primary", (nextLabel || "Suivant") + " →");
      b.href = "#" + nextId;
      p.appendChild(b);
    }
    inner.appendChild(p);
  }
  function neighborIds(id) {
    const i = routes.findIndex(r => r.id === id);
    return { prev: i > 0 ? routes[i - 1].id : null, next: i < routes.length - 1 ? routes[i + 1].id : null };
  }

  // ------------------------------------------------------------------ Renderers
  const renderers = {};

  renderers.accueil = function (inner) {
    const pct = progressPct();
    const resume = pct > 0;
    const hero = el("div", "hero");
    hero.innerHTML =
      `<span class="eyebrow">${esc(COURSE.code)} · Pôle ${esc(COURSE.pole.split(" · ")[0])} · Niveau ${esc(COURSE.niveau)}</span>
       <h1>${esc(COURSE.title)}</h1>
       <p>${esc(COURSE.subtitle)}. Un cours en ligne auto-rythmé de l'Académie de la Transition Énergétique pour apprendre à combiner ressources concessionnelles, capital privé et finance climat au service de l'accès à l'énergie.</p>
       <div class="chips">
         <span class="chip">⏱ ${esc(COURSE.duree)}</span>
         <span class="chip">🎓 ${esc(COURSE.niveau)}</span>
         <span class="chip">📚 ${COURSE.sections.length} sections + examen</span>
         <span class="chip">✓ Certification au seuil de ${PASS} %</span>
       </div>
       <a class="btn btn-primary" href="#${resume ? resumeTarget() : "presentation"}">${resume ? "Reprendre le cours" : "Commencer le cours"} →</a>`;
    inner.appendChild(hero);

    inner.appendChild(el("h2", null, "Votre progression"));
    const prog = el("div", "card");
    prog.innerHTML =
      `<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
        <div style="flex:1;min-width:180px">
          <div class="header-progress-bar" style="width:100%;height:12px;background:var(--green-100)"><span style="width:${pct}%;background:linear-gradient(90deg,var(--green-500),var(--green-600))"></span></div>
          <p class="progress-note">${sectionsDoneCount()} / ${COURSE.sections.length} sections validées${state.exam && state.exam.passed ? " · examen final réussi" : ""}</p>
        </div>
        <div style="font-size:32px;font-weight:800;color:var(--green-700)">${pct} %</div>
       </div>`;
    inner.appendChild(prog);

    inner.appendChild(el("h2", null, "Comment se déroule le parcours"));
    const steps = el("div", "steps");
    [
      ["Étape 1", "Présentation", "Objectifs, enjeu et identité de la formation."],
      ["Étape 2", "5 sections", "Contenu, étude de cas réelle et outils partenaires."],
      ["Étape 3", "Quiz de section", "Un contrôle des acquis à valider à chaque section."],
      ["Étape 4", "Examen final", `${COURSE.examen.length} questions · seuil de ${PASS} %.`],
      ["Étape 5", "Attestation", "Attestation de réussite nominative."]
    ].forEach(([sn, t, p]) => {
      const s = el("div", "step");
      s.innerHTML = `<div class="sn">${esc(sn)}</div><h4>${esc(t)}</h4><p>${esc(p)}</p>`;
      steps.appendChild(s);
    });
    inner.appendChild(steps);

    const note = el("p", "progress-note", `Version ${esc(COURSE.version)} · ${esc(COURSE.concepteur)}. Votre progression est enregistrée automatiquement dans ce navigateur.`);
    inner.appendChild(note);

    pager(inner, null, "presentation", "Commencer");
  };

  function resumeTarget() {
    // premier item non terminé
    for (const s of COURSE.sections) {
      if (!(state.sections[s.id] && state.sections[s.id].passed)) return s.id;
    }
    if (!(state.exam && state.exam.passed)) return "examen";
    return "attestation";
  }

  renderers.presentation = function (inner) {
    inner.appendChild(el("span", "eyebrow", "Présentation"));
    inner.appendChild(el("h1", null, "Identité de la formation"));
    inner.appendChild(el("p", "lede", COURSE.title));

    const grid = el("div", "meta-grid");
    const cells = [
      ["Code", COURSE.code], ["Pôle", COURSE.pole], ["Domaine", COURSE.domaine],
      ["Niveau", COURSE.niveau], ["Durée", COURSE.duree], ["Modalité", COURSE.modalite],
      ["Public prioritaire", COURSE.publicPrioritaire], ["Public associé", COURSE.publicAssocie],
      ["Prérequis", COURSE.prerequis]
    ];
    cells.forEach(([k, v]) => {
      const c = el("div", "cell");
      c.innerHTML = `<div class="k">${esc(k)}</div><div class="v">${esc(v)}</div>`;
      grid.appendChild(c);
    });
    inner.appendChild(grid);

    inner.appendChild(el("h2", null, "L'enjeu"));
    const enjeu = el("div", "callout key");
    enjeu.innerHTML = `<div class="callout-title">⚡ Pourquoi cette compétence</div><p>${esc(COURSE.enjeu)}</p>`;
    inner.appendChild(enjeu);

    inner.appendChild(el("h2", null, "Objectifs — compétences visées"));
    const ol = el("ol", "obj-list");
    COURSE.objectifs.forEach((o, i) => {
      const li = el("li");
      li.innerHTML = `<span class="num">${i + 1}</span><span>${esc(o)}</span>`;
      ol.appendChild(li);
    });
    inner.appendChild(ol);

    inner.appendChild(el("h3", null, "Lecture de référence"));
    inner.appendChild(el("p", null, esc(COURSE.lecture)));

    pager(inner, "accueil", "s1", "Section 1");
  };

  renderers._section = function (inner, route) {
    const s = route.section;
    const { prev, next } = neighborIds(s.id);
    const done = state.sections[s.id] && state.sections[s.id].passed;

    const head = el("div");
    head.innerHTML = `<span class="eyebrow">Section ${s.num} / ${COURSE.sections.length}</span>`;
    inner.appendChild(head);
    inner.appendChild(el("h1", null, s.title));
    if (done) inner.appendChild(el("span", "badge-done", "✓ Section validée"));
    inner.appendChild(el("p", "lede", s.resume));

    // objectifs de section
    inner.appendChild(el("h3", null, "Ce que vous saurez faire"));
    const ul = el("ul", "pill-list");
    s.objectifs.forEach(o => ul.appendChild(el("li", null, o)));
    inner.appendChild(ul);

    // contenu
    inner.appendChild(el("h2", null, "Contenu"));
    const lead = el("div", "section-lead");
    s.contenu.forEach(block => lead.appendChild(renderBlock(block)));
    inner.appendChild(lead);

    // étude de cas
    inner.appendChild(el("h2", null, "Étude de cas"));
    const cas = el("div", "callout case");
    cas.innerHTML =
      `<div class="callout-title">🌍 ${esc(s.cas.titre)}</div>` +
      `<p>${s.cas.html}</p>` +
      `<div class="source">Source : ${esc(s.cas.source)}</div>`;
    inner.appendChild(cas);

    // outils partenaires
    inner.appendChild(el("h2", null, "Outils partenaires à exploiter"));
    const tools = el("div", "tools");
    s.outils.forEach(t => {
      const d = el("div", "tool");
      d.innerHTML = `<span class="tp">${esc(t.partenaire)}</span><span class="tn">${esc(t.nom)}</span><span class="tu">${esc(t.usage)}</span>`;
      tools.appendChild(d);
    });
    inner.appendChild(tools);

    // quiz de section
    inner.appendChild(el("h2", null, "Contrôle des acquis"));
    inner.appendChild(el("p", null, `Validez cette section en répondant correctement à au moins ${PASS} % des questions.`));
    const quizHost = el("div");
    inner.appendChild(quizHost);
    mountQuiz(quizHost, {
      questions: s.quiz,
      pass: PASS,
      storedScore: state.sections[s.id],
      onPass: (score, total, pct) => {
        state.sections[s.id] = { passed: true, score, total, pct };
        save();
        renderNav();
        refreshHeaderProgress();
        showSectionSuccess(quizHost, next);
      }
    });

    pager(inner, prev, next, next === "ressources" ? "Ressources" : (routeById[next] && routeById[next].section ? "Section " + routeById[next].section.num : "Suivant"));
  };

  function showSectionSuccess(host, next) {
    let banner = host.querySelector(".section-next");
    if (banner) return;
    banner = el("div", "callout case section-next");
    banner.style.marginTop = "18px";
    banner.innerHTML =
      `<div class="callout-title">✓ Section validée</div>
       <p>Bravo, vous pouvez passer à la suite.</p>
       <p style="margin-top:10px"><a class="btn btn-primary" href="#${next}">Continuer →</a></p>`;
    host.appendChild(banner);
  }

  function renderBlock(block) {
    if (block.type === "para") return el("p", null, block.html);
    if (block.type === "key") {
      const c = el("div", "callout key");
      c.innerHTML = `<div class="callout-title">💡 ${esc(block.title)}</div><p>${block.html}</p>`;
      return c;
    }
    if (block.type === "list") {
      const wrap = el("div");
      if (block.title) wrap.appendChild(el("h3", null, block.title));
      const ul = el("ul", "pill-list");
      block.items.forEach(it => { const li = el("li"); li.innerHTML = it; ul.appendChild(li); });
      wrap.appendChild(ul);
      return wrap;
    }
    return el("p", null, block.html || "");
  }

  // ------------------------------------------------------------------ Quiz engine
  function mountQuiz(host, opts) {
    const { questions, pass, onPass } = opts;
    host.innerHTML = "";
    const form = el("div", "quiz");
    const state_answered = new Array(questions.length).fill(null);
    let submitted = false;

    questions.forEach((item, qi) => {
      const q = el("div", "quiz-q");
      q.innerHTML = `<div class="qnum">Question ${qi + 1} / ${questions.length}</div><div class="qtext">${esc(item.q)}</div>`;
      const choices = el("div", "choices");
      item.choix.forEach((choice, ci) => {
        const lab = el("label", "choice");
        lab.innerHTML = `<input type="radio" name="q${qi}" value="${ci}"><span>${esc(choice)}</span><span class="mark"></span>`;
        lab.querySelector("input").addEventListener("change", () => {
          if (submitted) return;
          state_answered[qi] = ci;
          submitBtn.disabled = state_answered.includes(null);
        });
        choices.appendChild(lab);
      });
      q.appendChild(choices);
      q.appendChild(el("div", "explain"));
      form.appendChild(q);
    });

    const resultBox = el("div", "quiz-result");
    const actions = el("div");
    actions.style.cssText = "display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:8px";
    const submitBtn = el("button", "btn btn-primary", "Valider mes réponses");
    submitBtn.disabled = true;
    const retryBtn = el("button", "btn btn-ghost", "↺ Recommencer");
    retryBtn.style.display = "none";
    actions.appendChild(submitBtn);
    actions.appendChild(retryBtn);

    host.appendChild(form);
    host.appendChild(resultBox);
    host.appendChild(actions);

    submitBtn.addEventListener("click", () => {
      if (state_answered.includes(null)) return;
      submitted = true;
      let correct = 0;
      questions.forEach((item, qi) => {
        const qNode = form.children[qi];
        const labels = qNode.querySelectorAll(".choice");
        labels.forEach((lab, ci) => {
          lab.classList.add("locked");
          const input = lab.querySelector("input");
          input.disabled = true;
          if (ci === item.bonne) lab.classList.add("correct");
          else if (ci === state_answered[qi]) lab.classList.add("wrong");
        });
        const ok = state_answered[qi] === item.bonne;
        if (ok) correct++;
        const ex = qNode.querySelector(".explain");
        ex.classList.add("show");
        ex.classList.toggle("ko", !ok);
        ex.innerHTML = `<strong>${ok ? "Correct." : "À revoir."}</strong> ${esc(item.explication)}`;
      });
      const pct = Math.round((correct / questions.length) * 100);
      const passed = pct >= pass;
      resultBox.className = "quiz-result show " + (passed ? "pass" : "fail");
      const okMsg = opts.passMsg || "Félicitations, vous avez validé ce contrôle des acquis.";
      const koMsg = opts.failMsg || `Seuil de ${pass} % non atteint. Relisez la section et réessayez.`;
      resultBox.innerHTML =
        `<div class="score">${correct} / ${questions.length} — ${pct} %</div>` +
        `<p>${passed ? okMsg : koMsg}</p>`;
      submitBtn.style.display = "none";
      retryBtn.style.display = "inline-flex";
      resultBox.scrollIntoView({ behavior: "smooth", block: "center" });
      if (passed && typeof onPass === "function") onPass(correct, questions.length, pct);
      if (typeof opts.onSubmit === "function") opts.onSubmit(correct, questions.length, pct, passed);
    });

    retryBtn.addEventListener("click", () => mountQuiz(host, opts));

    if (opts.storedScore && opts.storedScore.passed) {
      const info = el("div", "quiz-result show pass");
      info.style.marginBottom = "0";
      info.innerHTML = `<div class="score">Déjà validé — ${opts.storedScore.score}/${opts.storedScore.total} (${opts.storedScore.pct} %)</div><p>Vous pouvez refaire ce contrôle pour vous entraîner.</p>`;
      host.insertBefore(info, form);
    }
  }

  // ------------------------------------------------------------------ Ressources
  renderers.ressources = function (inner) {
    inner.appendChild(el("span", "eyebrow", "Ressources"));
    inner.appendChild(el("h1", null, "Récapitulatif des outils et ressources partenaires"));
    inner.appendChild(el("p", "lede", "Vue d'ensemble des ressources ouvertes mobilisables pour produire et animer FI-06. La réutilisation suppose de vérifier les licences et de créditer les sources."));

    const wrap = el("div", "table-wrap");
    let rows = COURSE.recap.map(r =>
      `<tr><td>${esc(r.partenaire)}</td><td>${esc(r.outil)}</td><td>${esc(r.usage)}</td></tr>`).join("");
    wrap.innerHTML =
      `<table class="recap"><thead><tr><th>Partenaire</th><th>Outil / ressource</th><th>Usage dans FI-06</th></tr></thead><tbody>${rows}</tbody></table>`;
    inner.appendChild(wrap);

    inner.appendChild(el("h2", null, "Dispositif pédagogique et certification"));
    const approche = el("ul", "pill-list");
    COURSE.dispositif.approche.forEach(a => approche.appendChild(el("li", null, esc(a))));
    inner.appendChild(el("h3", null, "Approche pédagogique"));
    inner.appendChild(approche);

    inner.appendChild(el("h3", null, "Évaluation et certification"));
    inner.appendChild(el("p", null, esc(COURSE.dispositif.evaluation)));

    const liv = el("div", "callout key");
    liv.innerHTML = `<div class="callout-title">📦 Livrable emporté</div><p>${esc(COURSE.dispositif.livrable)}</p>`;
    inner.appendChild(liv);

    inner.appendChild(el("h3", null, "Visite d'échange Sud-Sud associée"));
    const vis = el("ul", "pill-list");
    COURSE.dispositif.visites.forEach(v => vis.appendChild(el("li", null, esc(v))));
    inner.appendChild(vis);

    inner.appendChild(el("h2", null, "Sources principales"));
    const src = el("ul", "pill-list");
    COURSE.sources.forEach(v => src.appendChild(el("li", null, esc(v))));
    inner.appendChild(src);

    pager(inner, "s5", "examen", "Examen final");
  };

  // ------------------------------------------------------------------ Examen final
  renderers.examen = function (inner) {
    inner.appendChild(el("span", "eyebrow", "Évaluation"));
    inner.appendChild(el("h1", null, "Examen final"));
    inner.appendChild(el("p", "lede", `${COURSE.examen.length} questions couvrant les cinq sections. Seuil de réussite : ${PASS} %.`));

    if (!allSectionsDone()) {
      const warn = el("div", "callout key");
      warn.innerHTML =
        `<div class="callout-title">ⓘ Avant de commencer</div>
         <p>Vous avez validé ${sectionsDoneCount()} / ${COURSE.sections.length} sections. Vous pouvez passer l'examen dès maintenant, mais nous vous recommandons de valider d'abord tous les contrôles des acquis de section.</p>`;
      inner.appendChild(warn);
    }
    if (state.exam && state.exam.passed) {
      const ok = el("div", "callout case");
      ok.innerHTML = `<div class="callout-title">✓ Examen déjà réussi</div><p>Score enregistré : ${state.exam.score}/${state.exam.total} (${state.exam.pct} %). <a href="#attestation">Voir mon attestation →</a></p><p style="margin-top:8px">Vous pouvez repasser l'examen ci-dessous si vous le souhaitez.</p>`;
      inner.appendChild(ok);
    }

    const host = el("div");
    inner.appendChild(host);
    mountQuiz(host, {
      questions: COURSE.examen,
      pass: PASS,
      passMsg: "Félicitations, vous avez réussi l'examen final et validé le cours FI-06 !",
      failMsg: `Seuil de ${PASS} % non atteint. Revoyez les sections concernées et repassez l'examen.`,
      onSubmit: (score, total, pct, passed) => {
        if (passed && (!state.exam || !state.exam.passed || pct > (state.exam.pct || 0))) {
          state.exam = { passed: true, score, total, pct };
          save(); renderNav(); refreshHeaderProgress();
        } else if (passed && state.exam && state.exam.passed) {
          state.exam = { passed: true, score, total, pct: Math.max(pct, state.exam.pct) };
          save();
        }
        if (passed) {
          const b = el("div", "callout case");
          b.style.marginTop = "14px";
          b.innerHTML = `<div class="callout-title">🎓 Cours réussi</div><p>Vous avez validé l'examen final. <a class="btn btn-primary" style="margin-top:8px" href="#attestation">Obtenir mon attestation →</a></p>`;
          host.appendChild(b);
        }
      }
    });

    pager(inner, "ressources", "attestation", "Attestation");
  };

  // ------------------------------------------------------------------ Attestation
  renderers.attestation = function (inner) {
    inner.appendChild(el("span", "eyebrow", "Fin de parcours"));
    inner.appendChild(el("h1", null, "Attestation de réussite"));

    const passed = state.exam && state.exam.passed;
    if (!passed) {
      const warn = el("div", "callout key");
      warn.innerHTML =
        `<div class="callout-title">Attestation verrouillée</div>
         <p>Réussissez l'examen final (seuil de ${PASS} %) pour débloquer votre attestation.</p>
         <p style="margin-top:10px"><a class="btn btn-primary" href="#examen">Passer l'examen final →</a></p>`;
      inner.appendChild(warn);
      pager(inner, "examen", null);
      return;
    }

    const cert = el("div", "cert");
    const today = new Date().toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" });
    cert.innerHTML =
      `<div class="cert-mark">🎓</div>
       <div class="eyebrow">Académie de la Transition Énergétique</div>
       <h2>Attestation de réussite</h2>
       <p>Ce document atteste que</p>
       <div class="cert-name" contenteditable="true" spellcheck="false">${state.name ? esc(state.name) : "Votre nom"}</div>
       <p>a suivi et validé avec succès le cours en ligne auto-rythmé</p>
       <p style="font-weight:700;color:var(--green-700);font-size:17px">${esc(COURSE.code)} — ${esc(COURSE.title)}</p>
       <p style="margin-top:10px">Score à l'examen final : <strong>${state.exam.pct} %</strong> (seuil requis : ${PASS} %)</p>
       <p class="progress-note" style="margin-top:16px">Délivrée le ${esc(today)} · Certification Aigle Group · validation technique Africa Emergence Group (bloc Finance, niveau expert).</p>`;
    inner.appendChild(cert);

    const nameField = cert.querySelector(".cert-name");
    nameField.addEventListener("blur", () => {
      const v = nameField.textContent.trim();
      if (v && v !== "Votre nom") { state.name = v; save(); }
    });
    nameField.addEventListener("focus", () => {
      if (nameField.textContent.trim() === "Votre nom") nameField.textContent = "";
    });

    const actions = el("div");
    actions.style.cssText = "display:flex;gap:12px;flex-wrap:wrap;justify-content:center";
    const printBtn = el("button", "btn btn-primary", "🖨 Imprimer / enregistrer en PDF");
    printBtn.addEventListener("click", () => {
      const v = nameField.textContent.trim();
      if (v && v !== "Votre nom") { state.name = v; save(); }
      window.print();
    });
    actions.appendChild(printBtn);
    inner.appendChild(actions);

    inner.appendChild(el("p", "progress-note", "Astuce : cliquez sur votre nom dans l'attestation pour le personnaliser avant d'imprimer."));

    inner.appendChild(el("h2", null, "Et après ?"));
    const after = el("div", "callout case");
    after.innerHTML =
      `<div class="callout-title">Prolonger la formation</div>
       <p>Le socle en ligne se poursuit par la <strong>clinique de structuration</strong> à distance en cohorte, sur un cas réel, et un <strong>panel simulé de financeurs</strong> pour l'exercice de pitch. Livrable : une <strong>note de structuration d'un financement mixte</strong> pour un projet d'accès.</p>`;
    inner.appendChild(after);

    pager(inner, "examen", null);
  };

  // ------------------------------------------------------------------ Sidebar toggle
  function openSidebar() { $("#sidebar").classList.add("open"); $("#sidebarScrim").hidden = false; $("#navToggle").setAttribute("aria-expanded", "true"); }
  function closeSidebar() { $("#sidebar").classList.remove("open"); $("#sidebarScrim").hidden = true; $("#navToggle").setAttribute("aria-expanded", "false"); }
  $("#navToggle").addEventListener("click", () => {
    $("#sidebar").classList.contains("open") ? closeSidebar() : openSidebar();
  });
  $("#sidebarScrim").addEventListener("click", closeSidebar);

  // ------------------------------------------------------------------ Reset
  $("#resetBtn").addEventListener("click", () => {
    if (confirm("Effacer votre progression enregistrée pour ce cours ?")) {
      localStorage.removeItem(STORAGE_KEY);
      state = defaultState();
      renderNav(); refreshHeaderProgress();
      go("accueil");
    }
  });

  // ------------------------------------------------------------------ Hash routing
  function fromHash() {
    const id = (location.hash || "#accueil").slice(1);
    go(routeById[id] ? id : "accueil");
  }
  window.addEventListener("hashchange", fromHash);

  // ------------------------------------------------------------------ Footer
  $("#footerMeta").textContent =
    `${COURSE.code} — ${COURSE.title} · Version ${COURSE.version} · Conçu par ${COURSE.auteur}. Académie de la Transition Énergétique (ATE).`;

  // ------------------------------------------------------------------ Init
  renderNav();
  refreshHeaderProgress();
  fromHash();
})();
