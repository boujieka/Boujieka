/* ============================================================================
   FI-06 — Financement mixte et finance climatique pour l'accès à l'énergie
   Données du cours (contenu, études de cas, outils partenaires, quiz)
   Académie de la Transition Énergétique (ATE) · Aigle Group
   ==========================================================================*/

const COURSE = {
  code: "FI-06",
  title: "Financement mixte et finance climatique pour l'accès à l'énergie",
  subtitle: "Étude de cas par section · outils exploitables des partenaires",
  pole: "5 · Finance et investissements",
  domaine: "Finance et mobilisation des investissements",
  niveau: "Expert",
  duree: "5 jours (socle catalogue 3–5 j)",
  modalite: "Mixte — socle en ligne + clinique de structuration",
  publicPrioritaire: "MEH, unités de gestion de projet et FDSEL",
  publicAssocie: "Secteur privé et fonds de l'eau (FDSE)",
  prerequis: "Bases financières",
  lecture: "IRENA, Renewable Energy Finance ; SEforALL, Energizing Finance",
  version: "1.0 — 15 juillet 2026",
  concepteur: "Aigle Group (concepteur), en partenariat avec Africa Emergence Group et son réseau d'experts africains",
  auteur: "Emmanuel Boujieka Kamga, fondateur d'Aigle Group",
  seuil: 80,

  enjeu:
    "L'accès pour tous ne se financera pas au seul prix du marché. Combiner ressources concessionnelles, privées et fonds climat est la clé pour rendre les projets d'accès finançables. Pour un fonds sectoriel, c'est la compétence qui démultiplie ses ressources et attire des cofinancements.",

  objectifs: [
    "Combiner des ressources concessionnelles et privées dans un montage.",
    "Identifier les fonds climat pertinents et leurs critères d'accès.",
    "Structurer un rehaussement de crédit qui dé-risque l'investissement privé.",
    "Monter un dossier de financement mixte convaincant.",
    "Situer le montage dans les objectifs nationaux d'accès."
  ],

  // ---------------------------------------------------------------------------
  //  SECTIONS
  // ---------------------------------------------------------------------------
  sections: [
    {
      id: "s1",
      num: 1,
      title: "Pourquoi le marché seul ne suffit pas",
      resume:
        "Le déficit de financement de l'accès et la logique du financement mixte : mobiliser le privé plutôt que subventionner.",
      objectifs: [
        "Comprendre l'ampleur du déficit de financement de l'accès.",
        "Saisir la logique du financement mixte comme levier de mobilisation.",
        "Distinguer « maximiser la mobilisation privée » de « subventionner le projet »."
      ],
      contenu: [
        {
          type: "para",
          html:
            "L'investissement dans l'accès à l'énergie reste très en deçà des besoins, en particulier pour les <strong>ménages les plus difficiles à atteindre</strong>. Le prix du marché ne permet pas, à lui seul, de rendre ces projets finançables : les risques perçus sont trop élevés et les rendements attendus par le capital privé ne sont pas au rendez-vous."
        },
        {
          type: "para",
          html:
            "Le <strong>financement mixte (blended finance)</strong> est né précisément pour combler cet écart. Sa logique : utiliser des <strong>ressources concessionnelles</strong> (publiques, philanthropiques, climat) pour <strong>attirer le capital privé</strong> là où il ne viendrait pas seul."
        },
        {
          type: "key",
          title: "Idée-force",
          html:
            "L'objectif n'est pas de <em>subventionner</em> le projet, mais de <strong>maximiser la mobilisation privée par dollar public engagé</strong>. On mesure le succès à l'effet de levier obtenu, pas au montant de subvention distribué."
        }
      ],
      cas: {
        titre: "Le déficit de financement de l'accès en Afrique",
        html:
          "Les suivis des flux financiers montrent que l'investissement dans l'accès à l'énergie reste très en deçà des besoins, en particulier pour les ménages les plus difficiles à atteindre. Le financement mixte est né précisément pour combler cet écart en attirant le capital privé là où il ne viendrait pas seul.",
        source: "SEforALL, Energizing Finance ; IEA, Financing Clean Energy in Africa ; Banque mondiale."
      },
      outils: [
        { partenaire: "SEforALL", nom: "Energizing Finance", usage: "Données de suivi des flux de financement de l'accès, pour cadrer le déficit dans le cas national." },
        { partenaire: "IEA", nom: "Financing Clean Energy in Africa", usage: "Analyse des besoins et des flux d'investissement du continent." },
        { partenaire: "Convergence", nom: "Base de transactions de finance mixte", usage: "Exemples réels de structures pour illustrer la logique." }
      ],
      quiz: [
        {
          q: "Quel est l'objectif central du financement mixte pour un fonds sectoriel ?",
          choix: [
            "Subventionner le coût total du projet pour l'usager final",
            "Maximiser la mobilisation privée par dollar public engagé",
            "Remplacer intégralement le capital privé par des fonds publics",
            "Fixer le tarif de l'électricité en dessous du prix du marché"
          ],
          bonne: 1,
          explication:
            "Le financement mixte vise l'effet de levier : mobiliser un maximum de capital privé par dollar public, et non subventionner le projet."
        },
        {
          q: "Pourquoi le marché seul ne finance-t-il pas l'accès des ménages difficiles à atteindre ?",
          choix: [
            "Parce que la demande d'électricité est inexistante",
            "Parce que les risques perçus sont élevés et le capital privé ne vient pas seul",
            "Parce que les fonds climat interdisent l'investissement privé",
            "Parce que les tarifs sont plafonnés par les fonds climat"
          ],
          bonne: 1,
          explication:
            "Les risques élevés et les rendements insuffisants dissuadent le capital privé : c'est précisément l'écart que le financement mixte cherche à combler."
        },
        {
          q: "À quoi servent les données SEforALL « Energizing Finance » et IEA dans FI-06 ?",
          choix: [
            "À fixer les taux d'intérêt des prêts concessionnels",
            "À cadrer et chiffrer le déficit de financement dans le cas national",
            "À délivrer la certification finale du participant",
            "À garantir la liquidité des producteurs indépendants"
          ],
          bonne: 1,
          explication:
            "Ces séries de suivi des flux permettent d'objectiver l'ampleur du déficit de financement et de l'ancrer dans le contexte national."
        }
      ]
    },

    {
      id: "s2",
      num: 2,
      title: "Instruments concessionnels et rehaussement de crédit",
      resume:
        "Prêts concessionnels, garanties, tranches de première perte, subventions à la viabilité, AT — et le principe du rehaussement de crédit.",
      objectifs: [
        "Connaître la palette des instruments concessionnels.",
        "Comprendre le rehaussement de crédit : déplacer le risque plutôt que payer le projet.",
        "Identifier des instruments mobilisables pour un projet national."
      ],
      contenu: [
        {
          type: "para",
          html:
            "La boîte à outils concessionnelle comprend : <strong>prêts concessionnels</strong>, <strong>garanties partielles</strong> (de crédit ou de risque), <strong>tranches de première perte</strong>, <strong>subventions à la viabilité (viability gap funding)</strong> et <strong>assistance technique</strong>."
        },
        {
          type: "key",
          title: "Le principe du rehaussement de crédit",
          html:
            "Le rehaussement de crédit (<em>credit enhancement</em>) <strong>déplace ou réduit le risque</strong> supporté par l'investisseur privé — il ne paie pas le projet. En abaissant le risque perçu, il rend l'investissement bancable sans dépense publique directe équivalente au montant mobilisé."
        },
        {
          type: "para",
          html:
            "Une garantie de liquidité, par exemple, rassure les prêteurs sur le risque de retard de paiement de l'acheteur public, sans que l'argent public ne soit décaissé tant que l'événement couvert ne se produit pas."
        }
      ],
      cas: {
        titre: "ATIDI — RLSF, projet solaire de Golomoti (Malawi, 20 MW)",
        html:
          "La Facilité régionale de soutien à la liquidité (RLSF), portée par ATIDI avec l'appui allemand, fournit des garanties de liquidité couvrant le <strong>risque de retard de paiement de l'acheteur public</strong>. Elle a contribué à débloquer le financement de producteurs solaires indépendants, comme le projet de Golomoti au Malawi, en rassurant les prêteurs privés <strong>sans dépense publique directe</strong>.",
        source: "ATIDI (African Trade & Investment Development Insurance) ; GET.invest ; ESI-Africa."
      },
      outils: [
        { partenaire: "ATIDI", nom: "RLSF", usage: "Garantie de liquidité pour les IPP renouvelables ; instrument mobilisable pour les projets nationaux." },
        { partenaire: "PIDG", nom: "GuarantCo", usage: "Garanties de crédit pour les infrastructures en monnaie locale." },
        { partenaire: "AfDB", nom: "SEFA (Sustainable Energy Fund for Africa)", usage: "Dons de préparation et instruments concessionnels, notamment hors-réseau et États fragiles." },
        { partenaire: "Banque mondiale / MIGA", nom: "Garanties", usage: "Boîte à outils de garanties partielles de risque et de crédit." }
      ],
      quiz: [
        {
          q: "Que fait, par principe, un mécanisme de rehaussement de crédit ?",
          choix: [
            "Il paie directement le coût de construction du projet",
            "Il déplace ou réduit le risque supporté par l'investisseur privé",
            "Il fixe le rendement garanti des fonds propres privés",
            "Il remplace l'acheteur public défaillant"
          ],
          bonne: 1,
          explication:
            "Le rehaussement de crédit agit sur le risque, pas sur le prix du projet : il rend l'investissement bancable en dé-risquant."
        },
        {
          q: "Quel risque la RLSF d'ATIDI couvre-t-elle principalement ?",
          choix: [
            "Le risque de change à long terme",
            "Le risque de construction du projet",
            "Le risque de retard de paiement de l'acheteur public (risque de liquidité)",
            "Le risque de fluctuation du prix des modules solaires"
          ],
          bonne: 2,
          explication:
            "La RLSF fournit une garantie de liquidité couvrant les retards de paiement de l'off-taker public, ce qui rassure les prêteurs privés."
        },
        {
          q: "Parmi ces instruments, lequel est un don de préparation et instrument concessionnel adapté au hors-réseau et aux États fragiles ?",
          choix: [
            "GuarantCo de PIDG",
            "SEFA de l'AfDB",
            "Les garanties MIGA",
            "La base de transactions de Convergence"
          ],
          bonne: 1,
          explication:
            "Le SEFA (AfDB) fournit dons de préparation et instruments concessionnels, notamment pour le hors-réseau et les contextes fragiles."
        }
      ]
    },

    {
      id: "s3",
      num: 3,
      title: "La finance climatique",
      resume:
        "Fonds climat, instruments, critères d'accès, finance basée sur les résultats, marchés carbone (article 6) et exigence de MRV.",
      objectifs: [
        "Identifier les principaux fonds climat et leurs instruments.",
        "Maîtriser les critères d'accès : additionalité, entité accréditée, cofinancement.",
        "Comprendre la finance basée sur les résultats et le rôle du MRV."
      ],
      contenu: [
        {
          type: "para",
          html:
            "Les <strong>fonds climat</strong> — au premier rang desquels le <strong>Fonds vert pour le climat (GCF)</strong> et le <strong>GEF</strong> — offrent dons et ressources concessionnelles pour l'accès. Ils imposent des critères d'accès exigeants."
        },
        {
          type: "list",
          title: "Critères d'accès aux fonds climat",
          items: [
            "<strong>Additionalité</strong> : le fonds finance ce que le marché ne financerait pas.",
            "<strong>Entité accréditée</strong> : l'accès passe par une entité accréditée (banque de développement, ministère, etc.).",
            "<strong>Cofinancement</strong> : mobilisation de ressources complémentaires publiques et privées."
          ]
        },
        {
          type: "para",
          html:
            "S'y ajoutent la <strong>finance basée sur les résultats</strong> (paiement au résultat vérifié), les <strong>marchés carbone (article 6)</strong> et, transversalement, l'exigence de <strong>MRV — mesure, notification, vérification</strong>, indispensable pour attester l'impact climat."
        }
      ],
      cas: {
        titre: "GCF — Facilité de la BOAD pour le solaire en Afrique de l'Ouest francophone (FP105)",
        html:
          "Le Fonds vert pour le climat finance, via la <strong>Banque ouest-africaine de développement (BOAD) comme entité accréditée</strong>, une facilité qui mobilise l'investissement solaire dans les pays les moins avancés d'Afrique de l'Ouest francophone. Le montage — don et concessionnel du Fonds vert combinés à des ressources de la BOAD et du privé — est <strong>directement transposable au contexte francophone</strong>.",
        source: "Green Climate Fund, projet FP105."
      },
      outils: [
        { partenaire: "Green Climate Fund", nom: "Base de projets et propositions", usage: "Modèles de propositions, liste des entités accréditées, exemples francophones (FP105)." },
        { partenaire: "AfDB", nom: "SEFA, instrument climat off-grid", usage: "Finance climat concessionnelle pour le renouvelable décentralisé." },
        { partenaire: "GEF", nom: "Fonds pour l'environnement mondial", usage: "Cofinancement climat des projets d'accès." },
        { partenaire: "IRENA", nom: "Renewable Energy Finance", usage: "Données de coûts et analyses de la finance climat renouvelable." }
      ],
      quiz: [
        {
          q: "Quels sont les trois critères d'accès typiques d'un fonds climat comme le GCF ?",
          choix: [
            "Rentabilité, notation AAA et cotation en bourse",
            "Additionalité, entité accréditée et cofinancement",
            "Tarif plafonné, exclusivité et monnaie locale",
            "Garantie souveraine, assurance-crédit et prêt commercial"
          ],
          bonne: 1,
          explication:
            "Additionalité, passage par une entité accréditée et cofinancement sont les critères structurants de l'accès au financement climat."
        },
        {
          q: "Dans le projet FP105, quelle est l'entité accréditée qui canalise le financement du GCF ?",
          choix: [
            "L'IFC",
            "La MIGA",
            "La BOAD (Banque ouest-africaine de développement)",
            "GET.invest"
          ],
          bonne: 2,
          explication:
            "La BOAD agit comme entité accréditée du GCF pour la facilité solaire en Afrique de l'Ouest francophone (FP105)."
        },
        {
          q: "Que recouvre l'exigence de MRV dans la finance climatique ?",
          choix: [
            "Marché, revenus, valorisation",
            "Mesure, notification, vérification",
            "Mobilisation, rehaussement, viabilité",
            "Maturité, rendement, volatilité"
          ],
          bonne: 1,
          explication:
            "Le MRV (mesure, notification, vérification) atteste l'impact climat et conditionne notamment la finance basée sur les résultats."
        }
      ]
    },

    {
      id: "s4",
      num: 4,
      title: "Structurer un montage mixte",
      resume:
        "La pile de financement, le principe de subordination, le coût moyen et l'arbitrage sécurité publique / effet de levier privé.",
      objectifs: [
        "Décrire la pile de financement (don, concessionnel, dette privée, fonds propres).",
        "Appliquer le principe de subordination (le public prend le risque junior).",
        "Arbitrer entre sécurité publique et effet de levier privé."
      ],
      contenu: [
        {
          type: "para",
          html:
            "Un montage mixte s'organise en <strong>pile de financement (capital stack)</strong> : <strong>don</strong>, <strong>concessionnel</strong>, <strong>dette privée</strong> et <strong>fonds propres</strong>, chacun avec son coût et son rang de risque."
        },
        {
          type: "key",
          title: "Principe de subordination",
          html:
            "Le <strong>public prend le risque junior</strong> (première perte) : il est remboursé en dernier et absorbe les premières pertes. Cette subordination <strong>protège les tranches privées seniors</strong> et abaisse leur risque, ce qui les rend mobilisables."
        },
        {
          type: "para",
          html:
            "L'art du montage consiste à <strong>boucler le plan au meilleur coût moyen</strong> tout en maximisant l'effet de levier privé — un arbitrage permanent entre la <strong>sécurité apportée par le public</strong> et le <strong>levier privé</strong> obtenu."
        }
      ],
      cas: {
        titre: "IFC Scaling Solar — un montage mixte standardisé et reproductible",
        html:
          "Scaling Solar combine un <strong>appel d'offres standardisé</strong>, des <strong>contrats types</strong>, le financement de l'IFC et des garanties de la Banque mondiale et de la MIGA. Ce montage mixte a produit des <strong>tarifs solaires records</strong> — de l'ordre de 6 cents US/kWh en Zambie et 3,8 cents € /kWh au Sénégal — en dé-risquant l'investissement privé par un paquet reproductible.",
        source: "IFC ; Banque mondiale."
      },
      outils: [
        { partenaire: "IFC", nom: "Blended Finance", usage: "Principes de la finance concessionnelle mixte et structures types de dé-risquage." },
        { partenaire: "Banque mondiale", nom: "Boîte à outils garanties", usage: "Cadre d'emploi des garanties dans un montage de projet." },
        { partenaire: "Cours en ligne FI-06", nom: "Constructeur de montage mixte", usage: "Outil interactif de l'ATE pour tester la pile, le coût moyen et l'effet de levier." }
      ],
      quiz: [
        {
          q: "Selon le principe de subordination, quelle position occupe le capital public dans la pile ?",
          choix: [
            "Le rang senior, remboursé en premier",
            "Le rang junior (première perte), remboursé en dernier",
            "Un rang identique à la dette privée",
            "Aucun rang : il n'entre pas dans la pile"
          ],
          bonne: 1,
          explication:
            "Le public prend le risque junior : il absorbe les premières pertes, ce qui protège et mobilise les tranches privées seniors."
        },
        {
          q: "Comment Scaling Solar a-t-il obtenu des tarifs solaires records ?",
          choix: [
            "En subventionnant directement le prix payé par les ménages",
            "En dé-risquant l'investissement privé par un paquet standardisé et reproductible",
            "En interdisant la participation d'investisseurs privés",
            "En supprimant tout recours aux garanties"
          ],
          bonne: 1,
          explication:
            "Appel d'offres standardisé, contrats types, financement IFC et garanties Banque mondiale/MIGA : un paquet reproductible qui abaisse le risque et donc le tarif."
        },
        {
          q: "Quel est l'arbitrage central lorsqu'on boucle un montage mixte ?",
          choix: [
            "Entre le nombre de partenaires et la durée du projet",
            "Entre la sécurité apportée par le public et l'effet de levier privé, au meilleur coût moyen",
            "Entre le tarif et la puissance installée",
            "Entre l'additionalité et le MRV"
          ],
          bonne: 1,
          explication:
            "On cherche le meilleur coût moyen tout en maximisant le levier privé : plus de sécurité publique mobilise le privé mais coûte des ressources concessionnelles."
        }
      ]
    },

    {
      id: "s5",
      num: 5,
      title: "Monter le dossier et le défendre",
      resume:
        "Structurer le dossier, situer le montage dans les objectifs nationaux (Mission 300) et défendre additionalité, bancabilité et impact.",
      objectifs: [
        "Structurer un dossier de financement complet.",
        "Situer le montage dans les objectifs nationaux d'accès (Mission 300).",
        "Défendre additionalité, bancabilité et impact devant un panel."
      ],
      contenu: [
        {
          type: "list",
          title: "Structure d'un dossier de financement",
          items: [
            "<strong>Projet</strong> : description technique, marché, porteurs.",
            "<strong>Risques et allocation</strong> : matrice de risques et qui porte quoi.",
            "<strong>Plan de financement</strong> : pile de financement et sources.",
            "<strong>Impact</strong> : accès, emplois, genre, climat.",
            "<strong>MRV</strong> : dispositif de mesure, notification, vérification."
          ]
        },
        {
          type: "para",
          html:
            "Le dossier doit <strong>situer le montage dans les objectifs nationaux d'accès</strong> — plan national d'électrification, <strong>Mission 300</strong> — pour démontrer sa cohérence stratégique."
        },
        {
          type: "key",
          title: "Défendre devant un panel",
          html:
            "Face à un panel de financeurs, trois arguments se défendent : l'<strong>additionalité</strong> (pourquoi ce soutien est nécessaire), la <strong>bancabilité</strong> (pourquoi le montage tient) et l'<strong>impact</strong> (ce que le projet change concrètement)."
        }
      ],
      cas: {
        titre: "GET.invest — Finance Catalyst : de l'idée au bouclage",
        html:
          "Le Finance Catalyst de GET.invest, financé par l'Union européenne, accompagne <strong>gratuitement</strong> les porteurs de projets renouvelables d'Afrique subsaharienne dans la <strong>structuration</strong> et la <strong>mise en relation avec les financeurs</strong>. Il a contribué à mobiliser des financements pour de nombreux projets d'accès, en professionnalisant les dossiers présentés.",
        source: "GET.invest (Union européenne et partenaires)."
      },
      outils: [
        { partenaire: "GET.invest", nom: "Finance Catalyst", usage: "Appui gratuit à la structuration et à la mise en relation des projets renouvelables avec les financeurs." },
        { partenaire: "Green Climate Fund", nom: "Modèle de proposition de financement", usage: "Trame de dossier et critères attendus par un grand fonds climat." },
        { partenaire: "Cours en ligne FI-06", nom: "Modèle de note de structuration", usage: "Livrable emporté par le participant, base de son propre dossier." }
      ],
      quiz: [
        {
          q: "Quels éléments composent un dossier de financement mixte complet ?",
          choix: [
            "Uniquement le plan de financement et le tarif",
            "Projet, risques et allocation, plan de financement, impact et MRV",
            "Additionalité et cotation en bourse",
            "Contrat type et appel d'offres uniquement"
          ],
          bonne: 1,
          explication:
            "Un dossier structuré couvre le projet, l'allocation des risques, le plan de financement, l'impact et le dispositif MRV."
        },
        {
          q: "Dans quel cadre stratégique faut-il situer le montage pour convaincre ?",
          choix: [
            "Dans les objectifs nationaux d'accès (plan national, Mission 300)",
            "Dans le seul intérêt commercial de l'investisseur privé",
            "Dans la politique monétaire de la banque centrale",
            "Dans le budget de fonctionnement du ministère"
          ],
          bonne: 0,
          explication:
            "Situer le montage dans le plan national d'accès et la Mission 300 démontre sa cohérence stratégique et renforce le dossier."
        },
        {
          q: "Qu'apporte le Finance Catalyst de GET.invest aux porteurs de projets ?",
          choix: [
            "Un prêt commercial à taux de marché",
            "Une garantie de liquidité pour l'acheteur public",
            "Un appui gratuit à la structuration et à la mise en relation avec les financeurs",
            "Une accréditation automatique auprès du GCF"
          ],
          bonne: 2,
          explication:
            "Financé par l'UE, le Finance Catalyst accompagne gratuitement structuration et mise en relation, professionnalisant les dossiers."
        }
      ]
    }
  ],

  // ---------------------------------------------------------------------------
  //  RÉCAPITULATIF DES OUTILS PARTENAIRES
  // ---------------------------------------------------------------------------
  recap: [
    { partenaire: "SEforALL", outil: "Energizing Finance (série)", usage: "Cadrer le déficit de financement (section 1)" },
    { partenaire: "IEA", outil: "Financing Clean Energy in Africa", usage: "Données de besoins et de flux (section 1)" },
    { partenaire: "Convergence", outil: "Base de transactions de finance mixte", usage: "Exemples de structures (sections 1 et 4)" },
    { partenaire: "ATIDI", outil: "Regional Liquidity Support Facility (RLSF)", usage: "Garantie de liquidité IPP (section 2)" },
    { partenaire: "PIDG", outil: "GuarantCo", usage: "Garanties de crédit infrastructures (section 2)" },
    { partenaire: "AfDB", outil: "SEFA et instrument climat off-grid", usage: "Concessionnel et préparation (sections 2 et 3)" },
    { partenaire: "Banque mondiale / MIGA", outil: "Garanties et boîte à outils", usage: "Dé-risquage et structuration (sections 2 et 4)" },
    { partenaire: "Green Climate Fund", outil: "Projets, propositions, entités accréditées (FP105)", usage: "Finance climat et modèle de dossier (sections 3 et 5)" },
    { partenaire: "GEF", outil: "Cofinancement climat", usage: "Ressources climat (section 3)" },
    { partenaire: "IFC", outil: "Scaling Solar ; Blended Finance", usage: "Montage mixte reproductible (section 4)" },
    { partenaire: "GET.invest", outil: "Finance Catalyst", usage: "Structuration et mise en relation (section 5)" },
    { partenaire: "IRENA", outil: "Renewable Energy Finance", usage: "Données de coûts et de finance climat (sections 3 et 4)" }
  ],

  // ---------------------------------------------------------------------------
  //  DISPOSITIF & CERTIFICATION
  // ---------------------------------------------------------------------------
  dispositif: {
    approche: [
      "Socle théorique en ligne auto-rythmé (cours FI-06), avec constructeur de montage mixte interactif.",
      "Clinique de structuration animée à distance en cohorte, sur un cas réel du participant.",
      "Panel simulé de financeurs pour l'exercice de pitch.",
      "Étude des cas et outils partenaires listés dans chaque section."
    ],
    evaluation:
      "Contrôle des acquis (socle théorique en ligne, seuil de 80 %) et évaluation de la note de structuration financière sur grille, avec soutenance devant un panel. Certification délivrée par Aigle Group, validation technique par Africa Emergence Group (bloc Finance, niveau expert).",
    livrable:
      "Une note de structuration d'un financement mixte pour un projet d'accès : pile de financement, allocation des risques, effet de levier, impact et MRV, plan de mobilisation.",
    visites: [
      "Afrique du Sud — bureau des IPP / Trésor (REIPPPP). Observer un programme d'achat structuré et le dé-risquage de l'investissement privé.",
      "BOAD (Afrique de l'Ouest francophone) ou IFC Scaling Solar. Étudier une facilité de finance climat francophone (FP105) ou un montage standardisé bancable."
    ]
  },

  sources: [
    "SEforALL — Energizing Finance (série) ; ESMAP.",
    "IEA — Financing Clean Energy in Africa.",
    "ATIDI — Regional Liquidity Support Facility (RLSF) ; cas Golomoti Solar (Malawi).",
    "PIDG — GuarantCo.",
    "AfDB — Sustainable Energy Fund for Africa (SEFA).",
    "Green Climate Fund — projet FP105 (Facilité de la BOAD, Afrique de l'Ouest francophone).",
    "IFC / Banque mondiale — Scaling Solar ; Blended Finance ; garanties MIGA.",
    "GET.invest — Finance Catalyst (Union européenne).",
    "IRENA — Renewable Energy Finance."
  ]
};

// Examen final : tiré des quiz de section (banque de questions)
COURSE.examen = COURSE.sections.flatMap(s =>
  s.quiz.map(item => ({ ...item, section: s.num, sectionTitle: s.title }))
);
