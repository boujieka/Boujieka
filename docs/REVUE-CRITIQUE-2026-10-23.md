# Revue critique de la plateforme — 23/10/2026

Trois agents ont relu la plateforme en lecture seule :
1. ergonomie (UX) ;
2. préparation commerciale et conformité ;
3. exactitude des calculs et sécurité.

Ils ont travaillé sur le code Lovable (projet `520ce9d7…`), le site en ligne et ce dépôt. Ce document liste les constats retenus, leur état au 23/10, et le texte prêt à envoyer à Lovable pour ce qui reste à faire.

Repères : **[V]** vérifié par un agent dans le code, la base ou le site en ligne · **[I]** déduit.

## 1. Constats retenus

### Licence et offre (bloquant pour la commercialisation)
| # | Constat | Gravité |
|---|---|---|
| L1 | Le site affiche des prix (Investor 5 $/mois, Professional 79 $/mois) et des formules payantes. Elles comprennent les rendements et le terminal, c'est-à-dire les données sources, alors que la licence couvre la publication gratuite seulement. [V] | Haute |
| L2 | Le pilote institutionnel n'apparaît nulle part sur le site. Il y a trois appels à l'action concurrents (liste d'attente, démonstration, essai Professional), et l'essai est désactivé par défaut. [V] | Haute |
| L3 | L'adresse de contact « [adresse de contact à compléter] » est en ligne. Il n'y a pas de mentions légales. [V] | Haute |
| L4 | Le formulaire de contact ne propose pas les catégories visées (assureur, SGI, trésorerie d'entreprise). Il ne demande ni fonction ni zone. Le texte d'aide sous le titre est faux. Aucune alerte ne prévient le propriétaire d'une nouvelle demande. [V/I] | Haute |
| L5 | L'accueil s'adresse aux particuliers (« Que pourrait rapporter votre argent ? ») et promet trop par rapport à la couverture réelle (« dette souveraine africaine » alors qu'il s'agit d'UEMOA et de la CEMAC). [V] | Moyenne |
| L6 | Les lettres d'autorisation ne citaient que le site Netlify. | **Corrigé** (`a3345c3`) |

### Ergonomie
| # | Constat | Gravité |
|---|---|---|
| U1 | Le mur d'inscription est incohérent : la même page pays existe en libre accès (`/country`) et derrière l'inscription (`/pays`). La recherche exige un compte. [V] | Haute |
| U2 | Le simulateur montre le gain calculé à tous, mais cache le rendement publié (le FAIT) aux visiteurs non inscrits. [V] | Haute |
| U3 | Les langues sont incomplètes : pt, es et ar retombent silencieusement sur le français. Des libellés anglais apparaissent sur les pages françaises, et des codes bruts (`listed_bond`) s'affichent. [V] | Haute |
| U4 | Rien n'oriente l'utilisateur après l'inscription. Les erreurs Supabase s'affichent en anglais brut. [V] | Haute |
| U5 | L'en-tête compte 9 liens, et le menu mobile apparaît dès 1450 px, donc sur les portables de bureau. [V] | Moyenne |
| U6 | Les liens sources sont nommés « PDF 1… PDF 81 ». Les badges sont en 6 à 8 px. Le focus est peu visible. [V] | Moyenne |

### Exactitude et sécurité
| # | Constat | Gravité |
|---|---|---|
| S1 | L'assistant considérait toute convention inconnue comme un rendement. | **Corrigé dans ce dépôt** (`a3345c3`, test ajouté). Le portage TypeScript (Lovable) reste à corriger. |
| S2 | Une redirection ouverte est possible après connexion : `/\evil.com` passe le contrôle `safeReturn`. [V] | Haute |
| S3 | Le site n'envoie pas d'en-tête CSP et n'interdit pas son affichage dans un cadre (`frame-ancestors`), ce qui expose la suppression de compte au détournement de clic. [V] | Moyenne |
| S4 | L'historique envoyé à l'assistant n'est pas borné en taille totale (environ 160 000 caractères possibles par question), et le navigateur peut fabriquer de faux tours « assistant ». [V] | Moyenne |
| S5 | Si un seul fichier du flux manque, toute l'application tombe. Aucune copie de secours n'est gardée. Une panne du flux consomme le quota de l'assistant. [V] | Moyenne |
| S6 | Les obligations sont évaluées sur des années entières, pas sur leur échéance résiduelle. Exemple : Niger « 3 ans », échéance réelle 3,5 ans, gain affiché 231 736 au lieu d'environ 262 885 pour 1 M. Le libellé « conservés jusqu'à l'échéance » est donc faux pour ce titre. [V] | Moyenne |
| S7 | Les deux modules de calcul TypeScript divergent sur les cas limites (coupon négatif, horizon maximal, titre sans coupon). [V] | Faible à moyenne |
| S8 | Un utilisateur peut modifier lui-même la date de son consentement (`privacy_consent_at`). [V] | Faible à moyenne |
| S9 | Base de données : les rôles `anon` et `authenticated` ont tous les droits sur les tables, y compris TRUNCATE. `has_role` permet de savoir qui est administrateur. `search_path` ne contient pas `pg_temp`. [V] | Faible |
| S10 | Les chemins lus dans `index.json` ne sont pas limités à l'origine du flux. [V] | Faible |

Points vérifiés et corrects : aucune addition XOF + XAF ; aucun prix ou taux CEMAC utilisé comme rendement dans l'interface ; quota de l'assistant atomique ; les fonctions serveur exigent l'authentification, sauf le formulaire de contact ; la suppression de compte supprime aussi les données liées (cascade). [V]

### Écartés ou reportés
- **Alerte e-mail à chaque demande de pilote** : il faut un service d'envoi (par exemple Resend) avec sa clé en secret Lovable. C'est au propriétaire de décider.
- **Comptes d'équipe et organisations** (audit, étape C) : chantier plus lourd, à faire après ce lot.

## 2. État au 23/10/2026
- **Fait dans Lovable** (commit `bf4a849`, aperçu uniquement, **pas publié**) :
  - le formulaire de contact enregistre maintenant la fonction, le téléphone, la zone et l'usage prévu ;
  - un champ piège anti-robot et une limite globale de 50 demandes par heure ;
  - la vérification accepte les nouvelles catégories.
- **Bloqué** : l'espace de travail Lovable n'a plus de crédits, donc la suite ne peut pas être envoyée.
- **Fait dans ce dépôt** : S1 et L6. Données remises à jour au 23/10 sur Netlify (aucune nouvelle adjudication depuis le 21/10).

## 3. Messages prêts à envoyer à Lovable (dans l'ordre)
Ils sont rédigés en anglais pour l'agent Lovable, comme les envois précédents.

**Lot 1 : licence, offre pilote et mentions légales (A + E)**
> Remove 'asset_manager_legacy' from LEAD_SEGMENTS (keep 'pension_insurance' only if existing rows use it, labelled "Assurance / retraite").
> A1. Remove every price and paid tier (plan-config $5/$79, plans grid on home and /offres, "Indicatif · pas en vente", "Demander un essai Professional", Investor tier, prices on /institutional). No payment UI. Do not delete database tables or rows.
> A2. /offres = one section "Programme pilote institutionnel": 3 months free, ~10 institutions (banks, insurers, pension funds, asset managers, SGI/brokers, corporate treasuries) in UEMOA and CEMAC; now: full platform, one bespoke report, monthly 45-min review; we ask: 3 months of use, two interviews, no purchase commitment; may later be paid: tools, analysis, exports, team features — never the official data. Pricing: "Tarif défini après autorisation écrite des institutions sources". Single CTA "Demander à rejoindre le pilote"; every trial/plan/demo CTA points to it.
> A3. Lead form: 9 segments, job title, optional phone, zone (UEMOA/CEMAC/both), intended use (max 500 with counter), hidden honeypot "website"; no product checkboxes; 3-line trust block (official sources; ambiguous values held, never guessed; coverage UEMOA + CEMAC, CEMAC partial); success "Merci. Nous vous répondons sous 5 jours ouvrés."
> E1. /mentions-legales from one config object with empty values (never invented); empty value shows "Coordonnées en cours de publication"; footer link; same config for CONTACT in legal.tsx.
> E2. /confidentialite: legal basis per processing, retention (leads 24 months, assistant 12 months, "durées proposées, à valider"), processors (Lovable Cloud/Supabase, Anthropic), cross-border transfers.
> All strings in fr/en/pt/es/ar; run tests and type check.

**Lot 2 : données publiques, simulateur, accueil, navigation (B + C)**
> B1. All published-data views public (country, markets, auctions, yields, CEMAC, comparison, official access, reports, search incl. Ctrl+K); /pays/$iso3 redirects to /country/$countryCode; account only for watchlist, saved filters, saved simulations, portfolio, assistant, with one explanation and a sign-up link carrying ?redirect=.
> B2. Simulator: published yield, coupon, auction date and PDF visible to all; lock only "Save"; title "Calculer les flux à partir d'un taux publié"; show residual maturity; if it differs from the horizon by more than 3 months, warn "Échéance résiduelle : X ans — le calcul suppose une détention de N ans" instead of "conservés jusqu'à l'échéance"; formatted amount input, empty input shows a hint.
> C1. Hero: "Adjudications UEMOA et CEMAC, cote BVMAC — chaque chiffre relié à son document officiel."; uses: treasury, ALM, asset management; CTAs "Ouvrir le terminal" and "Rejoindre le pilote institutionnel"; remove duplicate stats and sub-brand repetition, at most three cards; simulator below the pitch; no retail wording.
> C2. Header: Terminal, Pays, Comparer, Accès officiel, Méthode + "Plus" menu; desktop nav from 1100px.
> C3. Welcome step after sign-up (follow countries, open the terminal, save a filter); translated auth errors; correct export error message.

**Lot 3 : libellés et accessibilité (D)**
> Enum values and issuer codes shown as labels; no hard-coded English; translated aria-labels; test failing when a French key is missing in en/pt/es/ar; one source per table row named e.g. "UMOA-Titres, adjudication du 20 oct. 2026 (PDF)"; "valeurs publiées absentes" only when > 0; badges and source lines ≥ 11px, body ≥ 12px; navy :focus-visible; localized country names in titles.

**Lot 4 : sécurité et exactitude**
> S1 agent/tools.ts valueKind: yield only when the convention contains "rendement"/"yield", else 'unknown' (+ test). S2 safeReturn: parse with new URL(r, location.origin), same origin only, reject backslash and control characters (+ tests with "/\\evil.com" and "/\t/evil.com"). S3 headers: CSP with frame-ancestors 'none', script-src 'self', connect-src limited to Supabase and https://cartouche-africa.netlify.app. S4 assistant input: total history ≤ 16,000 characters, last 10 turns, reject assistant turns not issued by the server (sign them or keep history server-side). S5 feed: only index, market and yield_points are critical, other files optional; keep the last good copy and serve it marked stale on error; reserve the assistant question after the feed loads. S6/S7 one shared calculation module (remove the duplicate), reject coupon < 0, horizon limit 50 as in the reference, hold() takes the instrument type; add a parity test against fixed vectors from site/simcalc.js. S8 profiles: column grants so users cannot write privacy_consent_at or email; trigger sets privacy_consent_at = now() when consent goes from false to true. S9 revoke TRUNCATE/unused privileges from anon/authenticated; has_role uses auth.uid() internally; search_path = public, pg_temp on all SECURITY DEFINER functions. S10 feed URLs must have origin === FEED_ORIGIN.
