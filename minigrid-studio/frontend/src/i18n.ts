// Interface strings (FR/EN). Labels of assumptions, indicators, series and checks come
// from the API (/engine/labels), so the exports and the screens use the same words.

export type Lang = "fr" | "en";

const dict = {
  title: { fr: "Mini-Grid Financial Model Studio", en: "Mini-Grid Financial Model Studio" },
  disclaimer: {
    fr: "Outil d'analyse. Ni certification BAD, Banque mondiale ou CrossBoundary, ni avis juridique, fiscal ou d'investissement.",
    en: "Analysis tool. Not a certification by AfDB, the World Bank or CrossBoundary, nor legal, tax or investment advice.",
  },
  email: { fr: "E-mail", en: "E-mail" },
  password: { fr: "Mot de passe", en: "Password" },
  name: { fr: "Nom", en: "Name" },
  login: { fr: "Se connecter", en: "Sign in" },
  logout: { fr: "Se déconnecter", en: "Sign out" },
  language: { fr: "Langue", en: "Language" },
  projects: { fr: "Projets", en: "Projects" },
  project: { fr: "Projet", en: "Project" },
  compare: { fr: "Comparer", en: "Compare" },
  admin: { fr: "Administration", en: "Administration" },
  organisation: { fr: "Organisation", en: "Organisation" },
  role: { fr: "Rôle", en: "Role" },
  role_admin: { fr: "Administrateur", en: "Administrator" },
  role_analyst: { fr: "Analyste", en: "Analyst" },
  role_reviewer: { fr: "Réviseur", en: "Reviewer" },
  role_investor: { fr: "Investisseur", en: "Investor" },
  newProject: { fr: "Nouveau projet", en: "New project" },
  country: { fr: "Pays", en: "Country" },
  description: { fr: "Description", en: "Description" },
  restricted: { fr: "Accès restreint aux membres du projet", en: "Access restricted to project members" },
  archived: { fr: "Archivé (lecture seule)", en: "Archived (read-only)" },
  archive: { fr: "Archiver", en: "Archive" },
  unarchive: { fr: "Désarchiver", en: "Unarchive" },
  create: { fr: "Créer", en: "Create" },
  cancel: { fr: "Annuler", en: "Cancel" },
  save: { fr: "Enregistrer", en: "Save" },
  open: { fr: "Ouvrir", en: "Open" },
  back: { fr: "Retour", en: "Back" },
  noProjects: { fr: "Aucun projet visible.", en: "No visible project." },
  versions: { fr: "Versions de scénario", en: "Scenario versions" },
  scenario: { fr: "Scénario", en: "Scenario" },
  version: { fr: "Version", en: "Version" },
  status: { fr: "Statut", en: "Status" },
  createdAt: { fr: "Créée le", en: "Created on" },
  newVersion: { fr: "Nouvelle version", en: "New version" },
  fromTemplate: { fr: "À partir d'un gabarit", en: "From a template" },
  template: { fr: "Gabarit", en: "Template" },
  importWorkbook: { fr: "Importer un classeur (.xlsm, format CrossBoundary)", en: "Import a workbook (.xlsm, CrossBoundary format)" },
  importNote: {
    fr: "Le fichier est lu comme des données : formules non évaluées, macros jamais exécutées.",
    en: "The file is read as data: formulas are not evaluated and macros never run.",
  },
  import: { fr: "Importer", en: "Import" },
  st_draft: { fr: "Brouillon", en: "Draft" },
  st_submitted: { fr: "Soumise", en: "Submitted" },
  st_approved: { fr: "Approuvée", en: "Approved" },
  st_rejected: { fr: "Rejetée", en: "Rejected" },
  submit: { fr: "Soumettre à revue", en: "Submit for review" },
  approve: { fr: "Approuver", en: "Approve" },
  reject: { fr: "Rejeter", en: "Reject" },
  reviewComment: { fr: "Commentaire de revue", en: "Review comment" },
  fourEyes: {
    fr: "Règle des quatre yeux : ni l'auteur ni la personne qui soumet ne peuvent approuver.",
    en: "Four-eyes rule: neither the author nor the submitter can approve.",
  },
  assumptions: { fr: "Hypothèses", en: "Assumptions" },
  lots: { fr: "Sites et lots", en: "Sites and lots" },
  addLot: { fr: "Ajouter un lot", en: "Add a lot" },
  removeLot: { fr: "Retirer", en: "Remove" },
  lotsNote: {
    fr: "6 lots au plus (colonnes E à J du classeur). Champ vide : la valeur du portefeuille s'applique.",
    en: "At most 6 lots (workbook columns E to J). Empty field: the portfolio value applies.",
  },
  options: { fr: "Options d'amélioration", en: "Improvement options" },
  optionsNote: {
    fr: "Désactivées par défaut. En activer une marque le résultat « variante ».",
    en: "Off by default. Enabling one marks the result as a variant.",
  },
  solver: { fr: "Solveur", en: "Solver" },
  solver_excel_macros: { fr: "Rejeu des macros du classeur (fidèle)", en: "Replay of the workbook macros (faithful)" },
  solver_exact: { fr: "Point fixe exact (variante)", en: "Exact fixed point (variant)" },
  note: { fr: "Note de version", en: "Version note" },
  changes: { fr: "modification(s)", en: "change(s)" },
  saveAsNewVersion: { fr: "Enregistrer comme nouvelle version", en: "Save as a new version" },
  versionsImmutable: {
    fr: "Une version est immuable : chaque enregistrement crée une nouvelle version liée à la précédente.",
    en: "A version is immutable: each save creates a new version linked to the previous one.",
  },
  readOnly: { fr: "Lecture seule", en: "Read-only" },
  search: { fr: "Rechercher", en: "Search" },
  cell: { fr: "Cellule", en: "Cell" },
  unit: { fr: "Unité", en: "Unit" },
  value: { fr: "Valeur", en: "Value" },
  modified: { fr: "modifié", en: "changed" },
  calculate: { fr: "Calculer", en: "Calculate" },
  perLot: { fr: "Avec TRI par lot (expérimental, plus long)", en: "With per-lot IRR (experimental, slower)" },
  runs: { fr: "Calculs", en: "Runs" },
  noRuns: { fr: "Aucun calcul pour cette version.", en: "No run for this version." },
  results: { fr: "Résultats", en: "Results" },
  indicators: { fr: "Indicateurs", en: "Indicators" },
  source: { fr: "Source", en: "Source" },
  derived: { fr: "dérivé (sans équivalent Excel)", en: "derived (no Excel equivalent)" },
  experimental: { fr: "expérimental", en: "experimental" },
  alerts: { fr: "Alertes", en: "Alerts" },
  none: { fr: "Aucune", en: "None" },
  checks: { fr: "Contrôles du classeur", en: "Workbook checks" },
  ok: { fr: "OK", en: "OK" },
  failed: { fr: "Échec", en: "Failed" },
  status_reconciled: { fr: "Moteur rapproché du classeur", en: "Engine reconciled with the workbook" },
  status_variant: { fr: "Variante (écarts au classeur)", en: "Variant (departs from the workbook)" },
  status_failed: { fr: "Calcul en échec", en: "Calculation failed" },
  charts: { fr: "Graphiques", en: "Charts" },
  financials: { fr: "Tableaux financiers", en: "Financial tables" },
  tab_pl: { fr: "Compte de résultat", en: "Income statement" },
  tab_cash: { fr: "Trésorerie et dette", en: "Cash flow and debt" },
  tab_bs: { fr: "Bilan", en: "Balance sheet" },
  tab_ops: { fr: "Exploitation", en: "Operations" },
  allYears: { fr: "Toutes les années", en: "All years" },
  activeYears: { fr: "Années actives", en: "Active years" },
  chart_pl: { fr: "Recettes, charges et EBE", en: "Revenue, opex and EBITDA" },
  chart_ds: { fr: "CFADS et service de la dette", en: "CFADS and debt service" },
  chart_debt: { fr: "Encours de dette et réserves", en: "Debt outstanding and reserves" },
  chart_dscr: { fr: "DSCR annuel (dérivé)", en: "Annual DSCR (derived)" },
  target: { fr: "Cible", en: "Target" },
  showTable: { fr: "Voir les données", en: "Show data" },
  hideTable: { fr: "Masquer les données", en: "Hide data" },
  exports: { fr: "Exports", en: "Exports" },
  exportXlsx: { fr: "Classeur Studio (.xlsx, formules de contrôle)", en: "Studio workbook (.xlsx, audit formulas)" },
  exportPdf: { fr: "Rapport PDF", en: "PDF report" },
  exportCsv: { fr: "Séries annuelles (.csv)", en: "Annual series (.csv)" },
  exportCb: { fr: "Format CrossBoundary (votre classeur)", en: "CrossBoundary format (your workbook)" },
  exportCbNote: {
    fr: "Choisissez votre copie du classeur CrossBoundary : seules les cellules d'hypothèses et les 4 valeurs collées sont réécrites ; formules, graphiques et macros sont conservés, et Excel recalcule à l'ouverture. Le fichier n'est pas conservé sur le serveur. Réservé aux calculs fidèles.",
    en: "Choose your copy of the CrossBoundary workbook: only the input cells and the 4 pasted values are rewritten; formulas, charts and macros are kept, and Excel recalculates on opening. The file is not kept on the server. Faithful runs only.",
  },
  chooseFile: { fr: "Choisir le fichier", en: "Choose the file" },
  downloading: { fr: "Préparation…", en: "Preparing…" },
  compareTitle: { fr: "Comparaison de scénarios", en: "Scenario comparison" },
  compareHelp: {
    fr: "Choisissez de 2 à 4 calculs. Le premier sert de base ; les écarts sont calculés par rapport à lui.",
    en: "Choose 2 to 4 runs. The first is the base; differences are computed against it.",
  },
  addToCompare: { fr: "Ajouter à la comparaison", en: "Add to comparison" },
  inCompare: { fr: "Dans la comparaison", en: "In the comparison" },
  clear: { fr: "Vider", en: "Clear" },
  base: { fr: "Base", en: "Base" },
  delta: { fr: "Écart", en: "Difference" },
  assumptionDiffs: { fr: "Hypothèses qui diffèrent", en: "Differing assumptions" },
  noDiffs: { fr: "Aucune hypothèse ne diffère.", en: "No assumption differs." },
  members: { fr: "Membres", en: "Members" },
  invitations: { fr: "Invitations", en: "Invitations" },
  invite: { fr: "Inviter", en: "Invite" },
  inviteToken: {
    fr: "Jeton d'invitation, affiché une seule fois. Transmettez ce lien à la personne invitée par un canal sûr :",
    en: "Invitation token, shown once. Send this link to the invitee over a safe channel:",
  },
  copy: { fr: "Copier", en: "Copy" },
  expires: { fr: "Expire le", en: "Expires on" },
  accepted: { fr: "Acceptée", en: "Accepted" },
  pending: { fr: "En attente", en: "Pending" },
  remove: { fr: "Retirer", en: "Remove" },
  confirmRemove: { fr: "Retirer ce membre et révoquer ses sessions ?", en: "Remove this member and revoke their sessions?" },
  auditLog: { fr: "Journal d'audit", en: "Audit log" },
  action: { fr: "Action", en: "Action" },
  entity: { fr: "Objet", en: "Object" },
  date: { fr: "Date", en: "Date" },
  user: { fr: "Utilisateur", en: "User" },
  acceptInvitation: { fr: "Accepter l'invitation", en: "Accept the invitation" },
  inviteNewAccount: {
    fr: "Nouveau compte : choisissez votre nom et un mot de passe (12 caractères au moins).",
    en: "New account: choose your name and a password (12 characters at least).",
  },
  inviteExisting: {
    fr: "Vous avez déjà un compte : connectez-vous d'abord, puis rouvrez ce lien.",
    en: "You already have an account: sign in first, then open this link again.",
  },
  loading: { fr: "Chargement…", en: "Loading…" },
  error: { fr: "Erreur", en: "Error" },
  dismiss: { fr: "Fermer", en: "Dismiss" },
  sessionExpired: { fr: "Session expirée : reconnectez-vous.", en: "Session expired: please sign in again." },
  investorNote: {
    fr: "Profil investisseur : seules les versions approuvées sont visibles.",
    en: "Investor profile: only approved versions are visible.",
  },
  year: { fr: "Année", en: "Year" },
  total: { fr: "Total", en: "Total" },
  amountsNote: { fr: "Montants dans la devise du modèle.", en: "Amounts in the model currency." },
  latestRun: { fr: "Dernier calcul", en: "Latest run" },
  duration: { fr: "Durée", en: "Duration" },
  engineVersion: { fr: "Version du moteur", en: "Engine version" },
  provenance: { fr: "Origine", en: "Provenance" },
  parent: { fr: "Version parente", en: "Parent version" },
  demoTitle: { fr: "Démo dans le navigateur.", en: "In-browser demo." },
  demoNote: {
    fr: "Le moteur de calcul (le même que sur le serveur) tourne dans votre navigateur. Données fictives, enregistrées dans ce navigateur seulement ; pas de comptes, pas de revue à plusieurs, pas d'import de classeur ni d'export au format CrossBoundary. Le rapport PDF passe par l'impression du navigateur.",
    en: "The calculation engine (the same as on the server) runs in your browser. Fictitious data, saved in this browser only; no accounts, no multi-person review, no workbook import or CrossBoundary-format export. The PDF report uses the browser's print dialog.",
  },
  demoLoading: {
    fr: "Chargement du moteur de calcul dans le navigateur (environ 13 Mo à la première visite)…",
    en: "Loading the calculation engine in the browser (about 13 MB on the first visit)…",
  },
  demoReset: { fr: "Effacer les données de la démo", en: "Erase the demo data" },
  demoResetConfirm: { fr: "Effacer tous les projets et calculs de la démo dans ce navigateur ?", en: "Erase all demo projects and runs in this browser?" },
  printPdf: { fr: "Imprimer / enregistrer en PDF", en: "Print / save as PDF" },
  invalidNumber: { fr: "Nombre non reconnu", en: "Number not recognised" },
  invalidDate: { fr: "Date attendue au format AAAA-MM-JJ", en: "Date expected as YYYY-MM-DD" },
  vat: { fr: "TVA", en: "VAT" },
  lotIrr: { fr: "TRI projet du lot {n} seul (expérimental)", en: "Project IRR of lot {n} alone (experimental)" },
} as const;

export type Key = keyof typeof dict;

export function t(key: Key, lang: Lang): string {
  return dict[key][lang];
}

export function allKeysTranslated(): boolean {
  return Object.values(dict).every((v) => v.fr.length > 0 && v.en.length > 0);
}

const locale = (lang: Lang) => (lang === "fr" ? "fr-FR" : "en-GB");

/** Parse a number typed in French or English ("1 600,5", "1,600.5", "0.45"); NaN if not a number. */
export function parseNumber(raw: string): number {
  let s = raw.trim().replace(/[\s\u00a0\u202f]/g, "");
  if (s === "") return NaN;
  if (s.includes(",") && s.includes(".")) s = s.lastIndexOf(",") > s.lastIndexOf(".") ? s.replace(/\./g, "").replace(",", ".") : s.replace(/,/g, "");
  else s = s.replace(",", ".");
  return /^[+-]?(\d+\.?\d*|\.\d+)(e[+-]?\d+)?$/i.test(s) ? Number(s) : NaN;
}

export function formatValue(value: number | null | undefined, unit: string, lang: Lang): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "n/a";
  if (Math.abs(value) < 0.005 && !unit.startsWith("%") && unit !== "x") value = 0;   // no "-0,00"
  if (unit.startsWith("%")) return new Intl.NumberFormat(locale(lang), { style: "percent", maximumFractionDigits: 2 }).format(value);
  if (unit === "x") return `${new Intl.NumberFormat(locale(lang), { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value)} x`;
  if (unit === "year") return String(value);
  const digits = Math.abs(value) >= 100 ? 0 : 2;
  return new Intl.NumberFormat(locale(lang), { maximumFractionDigits: digits }).format(value);
}

export function formatShort(value: number, lang: Lang): string {
  return new Intl.NumberFormat(locale(lang), { notation: "compact", maximumFractionDigits: 2 }).format(value);
}

export function formatDate(iso: string, lang: Lang): string {
  return new Intl.DateTimeFormat(locale(lang), { dateStyle: "medium", timeStyle: "short" }).format(new Date(iso));
}

/** French form of an engine message, from the server's rules (Python regex; groups written \1). */
export function translateMessage(text: string, rules: [string, string][]): string {
  if (!rules.length || !text) return text;
  return text.split("; ").map((part) => {
    for (const [pattern, replacement] of rules) {
      const re = new RegExp(pattern);
      if (re.test(part)) return part.replace(re, replacement.replace(/\\(\d)/g, "$$$1"));
    }
    return part;
  }).join("; ");
}

export function statusKey(status: string): Key {
  return (`st_${status}` in dict ? `st_${status}` : "st_draft") as Key;
}
