import type { LocaleBundle } from "../types";

/**
 * Version française. Même structure et même minutage que la version anglaise :
 * une bande-son enregistrée sur le découpage EN reste valable en FR.
 * Les chiffres et leurs réserves sont ceux du chapitre.
 */
export const fr: LocaleBundle = {
  chrome: {
    series: "Bankable Is Not Enough",
    chapter: "Chapitre 1 — Le piège du MoU",
    author: "Emmanuel Boujieka Kamga",
    sourceLabel: "Source",
    testLender: "Le test du prêteur",
    testState: "Le test de l'État",
    continues: "suite",
    colSigned: "Ce qui est signé",
    colBinds: "Ce qui engage",
    colCommitted: "Ce que l'État a engagé",
    tableLabel: "Tableau",
    bearsRiskLabel: "Porte le risque",
    absentLabel: "Absent de la table",
  },

  films: {
    "MoUTrap-Core": {
      title: "Le piège du MoU",
      audience: "Toutes parties prenantes",
      copy: {
        "core.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough",
          title: "Le piège du MoU",
          subtitle:
            "Pourquoi des engagements signés ne deviennent pas de l'électricité — et ce qu'ils coûtent lorsqu'ils aboutissent",
          audience: "Module central",
          runtime: "Chapitre 1",
        },

        "core.nigeria": {
          kind: "cold-open",
          kicker: "Quatorze contrats, aucune électricité",
          place: "Nigeria",
          date: "Juillet 2016",
          headline:
            "L'acheteur public d'électricité en gros du Nigeria a signé des contrats d'achat d'électricité avec quatorze développeurs solaires.",
          stats: [
            { value: "14", label: "développeurs solaires signataires", tone: "signal" },
            { value: "1 125", unit: "MW", label: "à ajouter au réseau", tone: "signal" },
            { value: "11,5", unit: "cts US/kWh", label: "fixés pour vingt ans", tone: "trap" },
            { value: "18", unit: "mois", label: "objectif avant la première injection", tone: "trap" },
          ],
          cite: "Green Street s.d. ; pv magazine 2019 ; Offgrid Nigeria 2020",
        },

        "core.flip": {
          kind: "stat-flip",
          before: { value: "1 125", unit: "MW", label: "promis", tone: "signal" },
          after: { value: "0", label: "électron livré", tone: "liability" },
          verdict:
            "Trois ans plus tard, aucun des quatorze n'avait atteint le bouclage financier. Dix des mieux placés auraient déjà versé des cautions de développement.",
          cite: "Offgrid Nigeria 2020 — l'acheteur en gros n'a pas publié son propre relevé des garanties reçues",
        },

        "core.tests": {
          kind: "two-tests",
          title: "Deux tests. L'un des deux n'est presque jamais appliqué.",
          lender: {
            name: "Le test du prêteur",
            question: "Le projet peut-il rembourser sa dette ?",
            asker: "Posé par les banques et les IFD — des années après la signature",
          },
          state: {
            name: "Le test de l'État",
            question:
              "Le système électrique et les finances publiques peuvent-ils porter les obligations de ce projet pendant vingt ans ou plus ?",
            asker: "Posé par personne dans la salle au moment de la signature",
          },
          footnote:
            "Un MoU — et souvent le premier contrat qui le suit — est signé avant que l'un ou l'autre test n'ait été appliqué.",
        },

        "core.stages": {
          kind: "stage-ladder",
          title: "Trois étapes que le débat public confond",
          rows: [
            {
              stage: "MoU",
              signed: "Protocole d'accord",
              binds: "Peu de chose en droit ; souvent exclusivité et confidentialité",
              committed: "Un signal politique ; parfois un site ou une ressource",
            },
            {
              stage: "Contrat",
              signed: "CAE, convention de mise en œuvre et accords de soutien",
              binds: "Tarif, durée et obligations des deux parties, sous conditions",
              committed: "Des paiements futurs, conditionnés à la mise en service",
            },
            {
              stage: "Bouclage financier",
              signed: "Contrats de prêt signés, conditions levées, premier tirage effectué",
              binds: "Tout ce qui précède, désormais financé",
              committed: "Des obligations fermes pour toute la durée du contrat",
            },
          ],
          caption: "Le piège se situe entre la première ligne et la troisième. Tableau 1.1",
        },

        "core.denominator": {
          kind: "funnel",
          title: "Quelle distance entre l'annonce et le bouclage ?",
          steps: [
            { label: "MoU signés", note: "Non comptabilisés. Rarement publiés." },
            { label: "Faisabilité et plan d'affaires", note: "80 % échouent ici" },
            { label: "Bouclage financier", note: "Moins de 10 % des projets y parviennent" },
          ],
          stats: [
            { value: "<10 %", label: "des projets d'infrastructure africains atteignent le bouclage financier", tone: "liability" },
            { value: "30 Md$", label: "de coûts de développement immobilisés en phase de faisabilité, six plus grands marchés", tone: "trap" },
            { value: "8,7 Md$", label: "d'investissement PEI, Afrique subsaharienne hors Afrique du Sud, 1990-2013", tone: "signal" },
            { value: "40,8 Md$", unit: "par an", label: "besoin estimé du secteur électrique", tone: "liability" },
          ],
          unknown:
            "Le problème du dénominateur : les bases de données enregistrent les projets qui ont abouti. Personne ne compte les MoU restés sans suite, de sorte que le taux de réussite de la voie du MoU est inconnu.",
          cite: "McKinsey 2020 (toutes infrastructures, ordre de grandeur) ; Eberhard et al. 2016 via tralac — le besoin inclut le transport et la distribution",
        },

        "core.layers": {
          kind: "layers",
          title: "Quatre explications — à lire comme des couches, non comme des rivales",
          layers: [
            {
              id: "sponsor",
              name: "Promoteur",
              where: "Le développeur",
              policy: "Sélectionner les promoteurs ; limiter l'exclusivité ; imposer jalons et garanties",
            },
            {
              id: "process",
              name: "Procédure",
              where: "La manière dont le projet a été monté",
              policy: "Mettre en concurrence par défaut ; confronter les offres spontanées au plan",
            },
            {
              id: "system",
              name: "Système",
              where: "Le plan, le réseau et l'acheteur",
              policy: "Réparer le système avant d'ajouter des contrats",
            },
            {
              id: "fiscal",
              name: "Budgétaire",
              where: "La capacité de l'État à soutenir",
              policy: "Appliquer le test souverain et calibrer le soutien sur l'espace budgétaire",
            },
          ],
          closing:
            "Le programme solaire nigérian présente les quatre à la fois. La bonne question est de savoir quelle couche est contraignante en premier — la réponse indique à un gouvernement ce qu'il doit corriger. Tableau 1.2",
        },

        "core.quaiboe": {
          kind: "case-card",
          country: "Nigeria",
          project: "Qua Iboe — 533 MW au gaz",
          verdict: "Des promoteurs crédibles ne suffisent pas.",
          beats: [
            "2014 — la Banque mondiale approuve une garantie partielle de risque pouvant atteindre 150 M$",
            "2017 — le gouvernement fédéral approuve le CAE",
            "Mai 2018 — la dernière prorogation du délai de signature des accords de garantie expire, après deux prorogations exceptionnelles de douze mois",
            "2020 — projet signalé à l'arrêt ; classé abandonné début 2026",
            "Parmi les promoteurs : une major pétrolière internationale, une société d'infrastructures détenue par un grand fonds, l'un des plus grands groupes industriels nigérians et la compagnie pétrolière nationale",
          ],
          cite: "Banque mondiale 2014 ; TheCable 2020 ; Global Energy Monitor 2026 ; Templars s.d. ; Reuters 2018",
          tone: "trap",
        },

        "core.actors": {
          kind: "actor-table",
          title: "Pourquoi le piège persiste : qui gagne à la signature, qui paie ensuite",
          rows: [
            {
              actor: "Gouvernement",
              offers: "Une réponse visible aux pénuries d'électricité",
              costs: "Peu de chose ; les coûts, s'il y en a, viennent plus tard",
              incentive: "Signer volontiers",
              bearsRisk: false,
            },
            {
              actor: "Développeur",
              offers: "Une option sur un site, une ressource ou un marché — qui peut se revendre",
              costs: "Études préliminaires et temps d'équipe",
              incentive: "Accumuler des options",
              bearsRisk: false,
            },
            {
              actor: "Compagnie nationale",
              offers: "Souvent rien, car elle peut ne pas être partie",
              costs: "Rien encore ; les obligations viennent plus tard",
              incentive: "Rester passive",
              bearsRisk: true,
            },
            {
              actor: "Trésor",
              offers: "Ne figure même pas dans le tableau 1.3",
              costs: "Rien encore",
              incentive: "Découvre le projet quand les termes sont presque arrêtés",
              bearsRisk: true,
              absent: true,
            },
            {
              actor: "Prêteurs",
              offers: "Rien, car ils sont rarement impliqués à ce stade",
              costs: "Rien",
              incentive: "Aucun filtre précoce",
              bearsRisk: false,
            },
            {
              actor: "Partenaires au développement",
              offers: "La preuve d'un portefeuille de projets",
              costs: "Rien directement",
              incentive: "Compter ce qui est signé",
              bearsRisk: false,
            },
          ],
          closing:
            "Les parties qui porteront le risque — la compagnie nationale et le Trésor — sont absentes ou passives. Celles qui testent le plus durement, les prêteurs, arrivent des années plus tard. La capacité n'est pas l'explication : des ministères compétents signent aussi de mauvais MoU, parce qu'une signature est récompensée aujourd'hui et payée plus tard, par quelqu'un d'autre. Tableau 1.3",
        },

        "core.exits": {
          kind: "two-exits",
          title: "Deux sorties du piège. Toutes deux coûteuses.",
          stall: {
            name: "Le projet s'enlise",
            detail:
              "Des années de temps ministériel et de dépenses de développeur ne produisent aucune électricité. Les sites restent bloqués. Un tarif publié devient une référence contre laquelle les soumissionnaires suivants devront argumenter.",
            cost: "Le pays perd du temps, de l'argent et des options",
          },
          close: {
            name: "Le projet aboutit",
            detail:
              "Un projet annoncé au plus haut niveau ne s'éteint pas de lui-même. La pression monte pour accorder aux prêteurs ce qu'ils exigent : garantie de l'État, paiements de capacité fermes, tarif en devises.",
            cost: "Le pays hérite d'un engagement",
          },
          shared:
            "Les deux sorties partagent une même cause. Les questions qui décident de la soutenabilité d'un contrat ont été posées trop tard, ou par des personnes sans autorité pour dire non.",
        },

        "core.ghana": {
          kind: "case-card",
          country: "Ghana",
          project: "La sortie coûteuse",
          verdict: "Ces contrats ont satisfait leurs prêteurs. Ensemble, ils ont échoué au test de l'État.",
          beats: [
            "2014-2017 — trois producteurs d'urgence contractés sans mise en concurrence",
            "43 CAE signés par le distributeur national par des procédures non concurrentielles",
            "1 900 MW de surcapacité projetée à l'horizon 2019",
            "2,75 Md$ d'arriérés nets du secteur au lancement du Programme de redressement en 2019",
            "Plus de 500 M$ par an versés, selon la presse, pour une électricité non consommée",
          ],
          cite: "Banque mondiale 2018 ; ministère de l'Énergie du Ghana 2019 ; ESI Africa s.d. — le chiffre de 500 M$ provient de la presse spécialisée, non vérifié sur document gouvernemental",
          tone: "liability",
        },

        "core.nachtigal": {
          kind: "case-card",
          country: "Cameroun",
          project: "Nachtigal — l'argument en faveur du MoU, et son avertissement",
          verdict: "La manière dont un projet commence compte. Elle ne décide pas de la manière dont il finira.",
          beats: [
            "Développé dans le cadre d'un accord de développement conjoint entre l'État, EDF, l'IFC et la compagnie nationale — et non, autant que les sources publiques le montrent, par appel d'offres",
            "Bouclage financier atteint avec une tranche en monnaie locale d'une maturité sans précédent pour les banques locales concernées",
            "Quelques mois après la mise en service complète en 2025, la presse rapporte que la garantie de paiement était largement tirée",
            "Le ministère des Finances cherchait, selon la presse, une ligne bancaire pour sécuriser les paiements au projet",
            "Un projet bien structuré reste exposé à un acheteur fragile",
          ],
          cite: "Power Technology 2021 ; IFC 2019 ; Agence Ecofin 2025 — articles de presse ; aucune déclaration officielle trouvée à la date de rédaction",
          tone: "pass",
        },

        "core.costs": {
          kind: "cost-list",
          title: "Cinq coûts. En général, seul le premier est compté.",
          items: [
            { name: "L'électricité non livrée", detail: "Une capacité que le plan supposait et que les consommateurs n'ont jamais reçue" },
            { name: "Les meilleurs projets bloqués", detail: "Un droit exclusif détenu par un développeur incapable de financer le site le soustrait à celui qui le pourrait" },
            { name: "L'attention publique consommée", detail: "Des ministères peu dotés en spécialistes passent des années sur des projets qui n'aboutiront pas" },
            { name: "La crédibilité perdue", detail: "Quand des termes signés sont rouverts, les investisseurs relèvent la prime exigée de tout le pays" },
            { name: "Les engagements créés", detail: "Quand des projets piégés aboutissent, sous pression politique, à des conditions fixées lorsqu'ils étaient le moins testés" },
          ],
          note: "Seul le premier coût apparaît dans la plupart des comptes rendus. Les quatre autres se paient discrètement, pendant vingt ans.",
        },

        "core.remedies": {
          kind: "remedy-list",
          title: "Avancer le coût, et faire entrer les porteurs de risque dans la salle",
          items: [
            {
              n: "1",
              name: "Filtrer à l'entrée",
              detail: "Aucun MoU pour un projet hors du plan de moindre coût sans confrontation préalable à ce plan",
              chapter: "Chapitre 4",
            },
            {
              n: "2",
              name: "Donner un prix à l'option",
              detail: "Cautions de développement, jalons et clauses d'extinction, pour que détenir un site sans progresser coûte quelque chose",
              chapter: "Chapitre 8",
            },
            {
              n: "3",
              name: "Faire entrer les porteurs de risque tôt",
              detail: "La compagnie nationale et le ministère des Finances examinent tout MoU pouvant entraîner des paiements fermes ou un soutien de l'État",
              chapter: "Chapitres 7 et 12",
            },
            {
              n: "4",
              name: "Publier un registre",
              detail: "Un registre public des MoU électriques et de leur statut, pour que les options caduques deviennent visibles et que de meilleurs projets se présentent",
              chapter: "Chapitre 18",
            },
          ],
          closing:
            "Le Nigeria montre que donner un prix à l'option ne suffit pas à soi seul. Le piège doit être refermé à chaque point où un projet est testé — c'est l'objet du Test de bouclage financier soutenable : une opération n'aboutit que si les deux tests sont passés et que la réponse de l'État a été rendue publique. Chapitre 16",
        },

        "core.key": {
          kind: "key-message",
          label: "Message clé",
          text: "Un MoU ne coûte presque rien à signer et peut coûter très cher par la suite : soit sous la forme d'une électricité qui n'arrive jamais, soit sous celle d'un contrat que le système ne peut pas supporter. Le piège persiste parce que ceux qui en porteront le risque sont absents au moment où l'engagement est pris. Le refermer suppose d'amener les porteurs de risque, et les tests qu'ils appliqueraient, au début du processus.",
          source: "Bankable Is Not Enough — Chapitre 1, Le piège du MoU",
        },
      },
      narration: {
        "core.title": "Bankable is not enough. Chapitre premier : le piège du MoU.",
        "core.nigeria": "En juillet 2016, l'acheteur public d'électricité en gros du Nigeria a signé des contrats d'achat d'électricité avec quatorze développeurs solaires. Les centrales devaient aller de cinquante à cent mégawatts et ajouter ensemble quelque mille cent vingt-cinq mégawatts à un réseau reconnu pour son manque de fiabilité. Le tarif était de onze virgule cinq cents américains par kilowattheure, fixé pour vingt ans. La signature a été largement célébrée. L'objectif pour la première injection était de dix-huit mois.",
        "core.flip": "Trois ans plus tard, aucun des quatorze n'avait atteint le bouclage financier. Dix des mieux placés auraient déjà versé des cautions de développement. En 2020, une publication spécialisée résumait le programme en un titre : mille cent vingt-cinq mégawatts promis, pas un électron livré.",
        "core.tests": "Ce livre repose sur deux tests. Le premier est le test du prêteur : le projet peut-il rembourser sa dette ? Le second est le test de l'État : le système électrique et les finances publiques peuvent-ils porter les obligations de ce projet pendant vingt ans ou plus ? Un MoU, et souvent le premier contrat qui le suit, est signé avant que l'un ou l'autre test n'ait été appliqué.",
        "core.stages": "Le débat public confond trois étapes. Un MoU engage peu en droit, même s'il accorde souvent une exclusivité. Un contrat fixe le tarif, la durée et les obligations, sous réserve de la mise en service. Le bouclage financier finance l'ensemble, et les obligations deviennent fermes pour toute la durée du contrat. Le piège se situe entre la première étape et la troisième.",
        "core.denominator": "Personne ne sait combien de MoU électriques les gouvernements africains ont signés, ni quelle part atteint le bouclage financier. McKinsey estime que moins de dix pour cent des projets d'infrastructure africains y parviennent, et que quatre-vingts pour cent échouent au stade de la faisabilité. Hors Afrique du Sud, l'investissement privé dans la production électrique en Afrique subsaharienne entre 1990 et 2013 s'est élevé à huit virgule sept milliards de dollars, face à des besoins estimés à environ quarante virgule huit milliards par an. C'est le problème du dénominateur : les bases de données enregistrent les projets qui ont abouti. Personne ne compte ceux qui n'ont mené nulle part.",
        "core.layers": "Quatre explications circulent pour expliquer l'enlisement des projets. L'explication par le promoteur met en cause le développeur. L'explication par la procédure met en cause la manière dont le projet a été monté. L'explication par le système désigne le plan, le réseau et l'acheteur. L'explication budgétaire désigne la capacité de l'État à soutenir. On les présente d'ordinaire comme concurrentes. Il vaut mieux les lire comme des couches. La bonne question est de savoir laquelle est contraignante en premier.",
        "core.quaiboe": "Qua Iboe écarte l'explication la plus facile. Ses promoteurs étaient crédibles : une major pétrolière internationale, une société d'infrastructures détenue par un grand fonds, l'un des plus grands groupes industriels nigérians, et la compagnie pétrolière nationale. La Banque mondiale a approuvé en 2014 une garantie partielle de risque pouvant atteindre cent cinquante millions de dollars. Le projet s'est enlisé malgré tout, et le dossier public désigne l'acheteur et l'exposition de l'État, non les promoteurs.",
        "core.actors": "Le piège persiste à cause de qui gagne et qui paie au moment de la signature. Le gouvernement obtient une réponse visible aux pénuries, à un coût immédiat faible. Les développeurs obtiennent une option, qui peut se revendre. La compagnie nationale n'est souvent même pas partie. Les prêteurs ne sont pas encore là. Et les deux parties qui porteront le risque, la compagnie nationale et le Trésor, sont absentes ou passives. Le manque de capacité des ministères fait partie de l'histoire, mais il n'explique pas la persistance. Des pays dotés de ministères compétents signent aussi de mauvais MoU, parce qu'une signature est récompensée aujourd'hui et que son coût est payé plus tard, et par quelqu'un d'autre.",
        "core.exits": "Un engagement pris au piège en sort de deux manières. Il s'enlise, et le pays perd du temps, de l'argent et des options. Ou il aboutit à des conditions fixées lorsque le projet était le moins testé, et le pays hérite d'un engagement. Les deux sorties commencent par la même omission.",
        "core.ghana": "Le Ghana montre où mène la seconde sortie. Entre 2014 et 2017, trois producteurs d'urgence ont été contractés sans mise en concurrence, et le distributeur national a signé quarante-trois contrats d'achat d'électricité par des procédures non concurrentielles. Les centrales contractées devaient créer mille neuf cents mégawatts de surcapacité à l'horizon 2019. Au lancement du Programme de redressement du secteur de l'énergie, les arriérés nets du secteur atteignaient deux virgule sept cinq milliards de dollars. Ces contrats avaient satisfait leurs prêteurs. Ensemble, ils ont échoué au test de l'État.",
        "core.nachtigal": "L'argument en faveur des MoU n'est pas faible. Certains projets ne peuvent pas être mis en concurrence dès le départ, parce que personne n'en sait encore assez pour rédiger un appel d'offres. La centrale hydroélectrique de Nachtigal, au Cameroun, a été développée dans le cadre d'un accord de développement conjoint, et non par appel d'offres, et a atteint le bouclage financier avec une tranche en monnaie locale sans précédent pour les banques concernées. Mais Nachtigal porte un avertissement. Quelques mois après sa mise en service complète en 2025, la presse rapportait que sa garantie de paiement était largement tirée, et que le ministère des Finances cherchait une ligne bancaire pour sécuriser les paiements. Un projet bien structuré reste exposé à un acheteur fragile.",
        "core.costs": "Le piège du MoU a cinq coûts, et en général seul le premier est compté. L'électricité non livrée. Les meilleurs projets bloqués. L'attention publique consommée. La crédibilité perdue quand des termes signés sont rouverts. Et les engagements créés quand des projets piégés aboutissent, sous pression politique, à des conditions fixées lorsqu'ils étaient le moins testés.",
        "core.remedies": "Si le piège existe parce qu'un MoU ne coûte rien à la signature et que ses risques pèsent sur des parties qui ne sont pas dans la salle, le remède consiste à avancer à la fois le coût et ces parties. Filtrer à l'entrée. Donner un prix à l'option. Faire entrer les porteurs de risque tôt. Et publier un registre. Le Nigeria montre que donner un prix à l'option ne suffit pas à soi seul. Le piège doit être refermé à chaque point où un projet est testé, par l'institution la mieux placée pour le tester.",
        "core.key": "Un MoU ne coûte presque rien à signer et peut coûter très cher par la suite : soit sous la forme d'une électricité qui n'arrive jamais, soit sous celle d'un contrat que le système ne peut pas supporter. Le piège persiste parce que ceux qui en porteront le risque sont absents au moment où l'engagement est pris. Le refermer suppose d'amener les porteurs de risque, et les tests qu'ils appliqueraient, au début du processus.",
      },
    },

    "MoUTrap-Ministers": {
      title: "Avant de signer",
      audience: "Ministres et membres du gouvernement",
      copy: {
        "min.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module A",
          title: "Avant de signer",
          subtitle: "Ce à quoi un protocole d'accord vous engage réellement",
          audience: "Ministres et membres du gouvernement",
          runtime: "Chapitre 1",
        },
        "min.flip": {
          kind: "stat-flip",
          before: { value: "1 125", unit: "MW", label: "signés et célébrés, Nigeria 2016", tone: "signal" },
          after: { value: "0", label: "électron livré, quatre ans plus tard", tone: "liability" },
          verdict:
            "Ce n'étaient pas des MoU. C'étaient des contrats d'achat d'électricité signés, et la plupart des développeurs avaient engagé de l'argent. Ils se sont arrêtés là où s'arrêtent la plupart des engagements électriques africains.",
          cite: "Offgrid Nigeria 2020 ; pv magazine 2019",
        },
        "min.actors": {
          kind: "actor-table",
          title: "À la table de signature, et après",
          rows: [
            {
              actor: "Vous",
              offers: "Une réponse visible aux pénuries d'électricité",
              costs: "Peu de chose ; les coûts, s'il y en a, viennent plus tard",
              incentive: "Signer volontiers",
              bearsRisk: false,
            },
            {
              actor: "Développeur",
              offers: "Une option sur un site ou un marché — qui peut se revendre",
              costs: "Études préliminaires et temps d'équipe",
              incentive: "Accumuler des options",
              bearsRisk: false,
            },
            {
              actor: "Compagnie nationale",
              offers: "Souvent rien — elle peut ne même pas être partie",
              costs: "Rien encore ; les obligations viennent plus tard",
              incentive: "Rester passive",
              bearsRisk: true,
            },
            {
              actor: "Trésor",
              offers: "Rien. En général non consulté.",
              costs: "Rien encore",
              incentive: "Découvre le projet quand les termes sont presque arrêtés",
              bearsRisk: true,
              absent: true,
            },
            {
              actor: "Prêteurs",
              offers: "Rien — ils arrivent des années plus tard",
              costs: "Rien",
              incentive: "Aucun filtre précoce",
              bearsRisk: false,
            },
          ],
          closing:
            "Une signature publique, surtout en présence d'un chef d'État, crée un engagement politique plus difficile à retirer que n'importe quelle clause du document. Les deux parties qui le paieront ne sont pas dans la salle.",
        },
        "min.exits": {
          kind: "two-exits",
          title: "Ce entre quoi vous choisissez, sans le savoir",
          stall: {
            name: "Le projet s'enlise",
            detail:
              "Du temps ministériel et de l'argent de développeur ne produisent aucune électricité. Le site reste bloqué. Votre tarif publié devient la référence contre laquelle tout soumissionnaire ultérieur argumentera. Rouvrir des termes signés relève la prime de risque du pays.",
            cost: "Du temps, de l'argent et des options perdus",
          },
          close: {
            name: "Le projet aboutit",
            detail:
              "Annoncé au plus haut niveau, le projet ne peut pas simplement s'éteindre. La pression monte pour accorder aux prêteurs une garantie de l'État, des paiements de capacité fermes et un tarif en devises — à des conditions fixées quand le projet était le moins testé.",
            cost: "Un engagement de vingt ans hérité",
          },
          shared:
            "Les deux commencent par la même omission : personne n'a demandé si le réseau pouvait l'absorber, si l'acheteur pouvait payer, ou si l'État pouvait se porter garant.",
        },
        "min.ask": {
          kind: "ask-card",
          audience: "Ministres et membres du gouvernement",
          title: "Quatre exigences avant la prochaine signature",
          asks: [
            "Publier un registre des MoU électriques, avec leur statut et leur date d'expiration — et laisser les options caduques s'éteindre. Ce premier pas ne coûte presque rien.",
            "Exiger que tout MoU pour un projet hors du plan de moindre coût soit confronté à ce plan avant d'être signé.",
            "S'assurer que le ministère des Finances et la compagnie nationale ont vu tout MoU pouvant entraîner des paiements fermes ou un soutien de l'État — avant la signature, et non quand les prêteurs arrivent avec leurs term sheets.",
            "Assortir le MoU de jalons, d'une date d'extinction et, le cas échéant, de cautions de développement. Les développeurs sérieux n'ont pas grand-chose à craindre de ces exigences.",
          ],
          because:
            "Un MoU confronté au plan, assorti de jalons et d'une date d'extinction, examiné par les porteurs de risque et publié, n'est plus un piège. C'est un outil de développement.",
        },
        "min.key": {
          kind: "key-message",
          label: "Message clé",
          text: "Un MoU ne coûte presque rien à signer et peut coûter très cher par la suite : soit sous la forme d'une électricité qui n'arrive jamais, soit sous celle d'un contrat que le système ne peut pas supporter. Le piège persiste parce que ceux qui en porteront le risque sont absents au moment où l'engagement est pris.",
          source: "Bankable Is Not Enough — Chapitre 1, Le piège du MoU",
        },
      },
      narration: {
        "min.title": "Bankable is not enough. Module A, pour les ministres et les membres du gouvernement : avant de signer.",
        "min.flip": "En 2016, le Nigeria a signé des contrats d'achat d'électricité pour mille cent vingt-cinq mégawatts de solaire. Quatre ans plus tard, pas un électron n'avait été livré. Ce n'étaient pas des protocoles d'accord. C'étaient des contrats signés, et la plupart des développeurs avaient engagé de l'argent. Ils se sont arrêtés là où s'arrêtent la plupart des engagements électriques africains.",
        "min.actors": "Considérez qui est à la table quand vous signez, et qui ne l'est pas. Vous obtenez une réponse visible aux pénuries, à un coût immédiat faible. Le développeur obtient une option, qui peut se revendre. La compagnie nationale n'est souvent même pas partie. Le Trésor n'est en général pas consulté avant que les termes soient presque arrêtés. Et les prêteurs, qui testeront le projet le plus durement, arrivent des années plus tard. Les deux parties qui paieront réellement cet engagement ne sont pas dans la salle.",
        "min.exits": "Cette omission vous laisse deux issues, et vous ne choisissez pas laquelle. Le projet s'enlise, et le pays perd du temps, de l'argent et des options — et rouvrir des termes signés relève la prime de risque exigée de tout le pays. Ou le projet aboutit, sous pression politique, à des conditions fixées quand il était le moins testé, et le pays hérite d'un engagement de vingt ans.",
        "min.ask": "Quatre exigences avant la prochaine signature. Publier un registre des MoU électriques, avec leur statut et leur date d'expiration, et laisser les options caduques s'éteindre — ce premier pas ne coûte presque rien. Exiger que tout MoU hors du plan de moindre coût soit confronté à ce plan avant signature. S'assurer que le ministère des Finances et la compagnie nationale ont vu tout MoU pouvant créer des paiements fermes ou un soutien de l'État. Et assortir le MoU de jalons, d'une date d'extinction et, le cas échéant, de cautions de développement. Les développeurs sérieux n'ont pas grand-chose à craindre de ces exigences.",
        "min.key": "Un MoU ne coûte presque rien à signer et peut coûter très cher par la suite. Le piège persiste parce que ceux qui en porteront le risque sont absents au moment où l'engagement est pris.",
      },
    },

    "MoUTrap-Finance": {
      title: "Le test de l'État",
      audience: "Ministères des Finances et Trésor",
      copy: {
        "fin.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module B",
          title: "Le test de l'État",
          subtitle: "L'engagement commence à une signature qu'on ne vous a pas montrée",
          audience: "Ministères des Finances et Trésor",
          runtime: "Chapitre 1",
        },
        "fin.tests": {
          kind: "two-tests",
          title: "Le test que vous seuls pouvez appliquer",
          lender: {
            name: "Le test du prêteur",
            question: "Le projet peut-il rembourser sa dette ?",
            asker: "Appliqué rigoureusement — par les banques et les IFD, au bouclage financier",
          },
          state: {
            name: "Le test de l'État",
            question:
              "Le système électrique et les finances publiques peuvent-ils porter les obligations de ce projet pendant vingt ans ou plus ?",
            asker: "Appliqué par vous — en général bien trop tard, quand il l'est",
          },
          footnote:
            "Même lorsqu'une IFD codéveloppe dès le départ, le ministère des Finances ne découvre le projet que lorsque ses termes sont presque arrêtés. L'absence qui compte le plus est celle du test de l'État.",
        },
        "fin.ghana": {
          kind: "case-card",
          country: "Ghana",
          project: "Quand des contrats bancables cassent le budget",
          verdict: "Chacun de ces contrats a satisfait ses prêteurs. Ensemble, ils ont échoué au test de l'État.",
          beats: [
            "2014-2017 — trois producteurs d'urgence contractés sans mise en concurrence",
            "43 CAE signés par le distributeur national par des procédures non concurrentielles",
            "1 900 MW de surcapacité projetée à l'horizon 2019 — des paiements de capacité dus sur une électricité non nécessaire",
            "2,75 Md$ d'arriérés nets du secteur au lancement du Programme de redressement, 2019",
            "Plus de 500 M$ par an versés, selon la presse, pour une électricité non consommée",
          ],
          cite: "Banque mondiale 2018 ; ministère de l'Énergie du Ghana 2019 ; ESI Africa s.d. — le chiffre de 500 M$ provient de la presse spécialisée, non vérifié sur document gouvernemental",
          tone: "liability",
        },
        "fin.nachtigal": {
          kind: "case-card",
          country: "Cameroun",
          project: "Nachtigal — bonne structure, acheteur fragile",
          verdict: "Un projet bien structuré reste exposé à un acheteur fragile.",
          beats: [
            "Accord de développement conjoint entre l'État, EDF, l'IFC et la compagnie nationale",
            "Bouclage financier atteint avec une tranche en monnaie locale d'une maturité sans précédent pour les banques locales",
            "Quelques mois après la mise en service complète en 2025, la garantie de paiement était signalée largement tirée",
            "Le ministère des Finances cherchait, selon la presse, une ligne bancaire pour sécuriser les paiements au projet",
          ],
          cite: "Power Technology 2021 ; IFC 2019 ; Agence Ecofin 2025 — articles de presse ; aucune déclaration officielle trouvée à la date de rédaction",
          tone: "trap",
        },
        "fin.ask": {
          kind: "ask-card",
          audience: "Ministères des Finances et Trésor",
          title: "Ce qu'il faut exiger, et quand",
          asks: [
            "Exiger de voir tout MoU pouvant entraîner des paiements fermes ou un soutien de l'État — au stade du MoU, et non quand les prêteurs arrivent avec leurs term sheets.",
            "Calibrer le soutien de l'État sur l'espace budgétaire, et non sur ce qu'exige la term sheet. Garanties, paiements de capacité et tarifs en devises sont des engagements conditionnels, qu'ils soient comptabilisés comme tels ou non.",
            "Traiter une garantie de paiement tirée comme une défaillance du système, non comme un incident de trésorerie : Nachtigal était bien structuré et a pourtant exposé le Trésor quelques mois après la mise en service.",
            "Exiger que la réponse de l'État soit rendue publique au bouclage — le Test de bouclage financier soutenable demande que les deux tests soient passés et que la réponse de l'État soit publiée.",
          ],
          because:
            "Une signature est récompensée aujourd'hui ; son coût est payé plus tard, et par vous. Avancer le test de l'État est le seul moyen de changer cela.",
        },
        "fin.key": {
          kind: "key-message",
          label: "Message clé",
          text: "Beaucoup des engagements qui arrivent sur votre bureau ont commencé dans un MoU qu'on ne vous a jamais montré. Refermer le piège suppose d'amener les porteurs de risque, et les tests qu'ils appliqueraient, au début du processus.",
          source: "Bankable Is Not Enough — Chapitre 1, Le piège du MoU",
        },
      },
      narration: {
        "fin.title": "Bankable is not enough. Module B, pour les ministères des Finances et le Trésor : le test de l'État.",
        "fin.tests": "Deux tests décident de la survie d'un contrat électrique. Le test du prêteur demande si le projet peut rembourser sa dette. Ce test est appliqué rigoureusement, par les banques et les institutions de financement du développement, au bouclage financier. Le test de l'État demande autre chose : le système électrique et les finances publiques peuvent-ils porter les obligations de ce projet pendant vingt ans ou plus ? Vous seuls pouvez appliquer ce test. Même lorsqu'une institution de financement du développement codéveloppe dès le départ, le ministère des Finances ne découvre le projet que lorsque ses termes sont presque arrêtés. L'absence qui compte le plus est celle du test de l'État.",
        "fin.ghana": "Le Ghana montre ce qui arrive quand seul le test du prêteur est appliqué. Entre 2014 et 2017, trois producteurs d'urgence ont été contractés sans mise en concurrence, et le distributeur national a signé quarante-trois contrats d'achat d'électricité par des procédures non concurrentielles. Les centrales contractées devaient créer mille neuf cents mégawatts de surcapacité à l'horizon 2019. Au lancement du Programme de redressement du secteur de l'énergie, les arriérés nets atteignaient deux virgule sept cinq milliards de dollars, et le pays versait, selon la presse, plus de cinq cents millions de dollars par an pour une électricité qu'il ne consommait pas. Chacun de ces contrats avait satisfait ses prêteurs.",
        "fin.nachtigal": "Une bonne structure n'est pas non plus une défense à elle seule. La centrale camerounaise de Nachtigal a été développée dans le cadre d'un accord de développement conjoint avec EDF, l'IFC et la compagnie nationale, et a atteint le bouclage financier avec une tranche en monnaie locale d'une maturité sans précédent. Quelques mois après sa mise en service complète en 2025, la presse rapportait que sa garantie de paiement était largement tirée, et que le ministère des Finances cherchait une ligne bancaire pour sécuriser les paiements. Un projet bien structuré reste exposé à un acheteur fragile.",
        "fin.ask": "Donc : exigez de voir tout MoU pouvant entraîner des paiements fermes ou un soutien de l'État, au stade du MoU, et non quand les prêteurs arrivent avec leurs term sheets. Calibrez le soutien de l'État sur l'espace budgétaire, et non sur ce qu'exige la term sheet. Traitez une garantie de paiement tirée comme une défaillance du système, non comme un incident de trésorerie. Et exigez que la réponse de l'État soit rendue publique au bouclage.",
        "fin.key": "Beaucoup des engagements qui arrivent sur votre bureau ont commencé dans un MoU qu'on ne vous a jamais montré. Refermer le piège suppose d'amener les porteurs de risque, et les tests qu'ils appliqueraient, au début du processus.",
      },
    },

    "MoUTrap-Regulators": {
      title: "La référence dont vous héritez",
      audience: "Régulateurs et autorités de passation",
      copy: {
        "reg.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module C",
          title: "La référence dont vous héritez",
          subtitle: "Ce que coûte un tarif fixé administrativement quand le marché bouge",
          audience: "Régulateurs et autorités de passation",
          runtime: "Chapitre 1",
        },
        "reg.tariff": {
          kind: "cold-open",
          kicker: "Un tarif fixé avant toute mise en concurrence",
          place: "Nigeria",
          date: "2016 → 2019",
          headline:
            "Le tarif solaire nigérian a été fixé administrativement, avant toute découverte concurrentielle du prix. Quand les coûts du solaire ont baissé, le gouvernement a tenté de le rouvrir, et le programme s'est enlisé dans le différend.",
          stats: [
            { value: "11,5", unit: "cts US/kWh", label: "convenus en 2016, fixés pour 20 ans", tone: "signal" },
            { value: "7,5", unit: "cts US/kWh", label: "visés par le gouvernement en 2019", tone: "trap" },
            { value: "0", label: "projet au bouclage financier", tone: "liability" },
            { value: "7", unit: "ans et +", label: "des analystes proposaient encore des issues en 2023", tone: "liability" },
          ],
          cite: "pv magazine 2019 ; Energy for Growth Hub 2023",
        },
        "reg.layers": {
          kind: "layers",
          title: "Quelle couche est contraignante en premier ? La vôtre est en général la deuxième.",
          layers: [
            {
              id: "sponsor",
              name: "Promoteur",
              where: "Le développeur",
              policy: "Sélectionner les promoteurs ; limiter l'exclusivité ; imposer jalons et garanties",
            },
            {
              id: "process",
              name: "Procédure",
              where: "La manière dont le projet a été monté — en contournant la planification, la formation du prix et le contrôle",
              policy: "Mettre en concurrence par défaut ; confronter les offres spontanées au plan",
            },
            {
              id: "system",
              name: "Système",
              where: "Le plan, le réseau et l'acheteur",
              policy: "Réparer le système avant d'ajouter des contrats",
            },
            {
              id: "fiscal",
              name: "Budgétaire",
              where: "La capacité de l'État à soutenir",
              policy: "Appliquer le test souverain et calibrer le soutien sur l'espace budgétaire",
            },
          ],
          closing:
            "Une proposition apportée par un développeur et négociée de gré à gré contourne la planification, la formation du prix et le contrôle qu'un appel d'offres imposerait. C'est la couche qu'un régulateur est placé pour contraindre en premier. Tableau 1.2",
        },
        "reg.quote": {
          kind: "quote",
          text: "De tels projets rencontrent souvent des difficultés, notamment en détournant les ressources publiques des plans stratégiques du gouvernement.",
          attribution:
            "Banque mondiale et PPIAF, Policy Guidelines for Managing Unsolicited Proposals in Infrastructure Projects, 2017",
        },
        "reg.ask": {
          kind: "ask-card",
          audience: "Régulateurs et autorités de passation",
          title: "Quatre leviers qui relèvent de votre autorité",
          asks: [
            "Mettre en concurrence par défaut. Là où un appel d'offres est réellement impossible — grand site hydroélectrique, interconnexion transfrontalière, première installation d'une technologie nouvelle — le dire officiellement et l'expliquer.",
            "Confronter toute offre spontanée au plan de moindre coût avant qu'un tarif ne soit indiqué, quelle que soit la précaution avec laquelle il est qualifié de non contraignant.",
            "Traiter un tarif indicatif comme une référence publiée, car c'est ce qu'il devient. Tout soumissionnaire ultérieur argumentera contre lui, et le rouvrir coûte au pays sa crédibilité.",
            "Exiger jalons, dates d'extinction et cautions de développement dans les instruments que vous approuvez, pour que détenir un site sans progresser coûte quelque chose.",
          ],
          because:
            "Un tarif indicatif, quelle que soit son étiquette, devient la référence de toute négociation ultérieure. La formation du prix qui n'a pas lieu avant la signature a lieu après, sous forme de litige.",
        },
        "reg.key": {
          kind: "key-message",
          label: "Message clé",
          text: "Un tarif fixé avant toute mise en concurrence ne reste pas indicatif. Il devient la référence contre laquelle le pays devra argumenter pendant des années — et quand l'État le rouvre, les investisseurs relèvent la prime qu'ils exigent sur tout le reste.",
          source: "Bankable Is Not Enough — Chapitre 1, Le piège du MoU",
        },
      },
      narration: {
        "reg.title": "Bankable is not enough. Module C, pour les régulateurs et les autorités de passation : la référence dont vous héritez.",
        "reg.tariff": "Le tarif solaire nigérian a été fixé administrativement, avant toute découverte concurrentielle du prix : onze virgule cinq cents américains par kilowattheure, fixés pour vingt ans. Quand les coûts du solaire ont baissé, le gouvernement a cherché à le ramener à environ sept virgule cinq cents. Le programme s'est enlisé dans le différend. Aucun des quatorze projets n'a atteint le bouclage financier, et en 2023 encore, des analystes proposaient des issues au blocage.",
        "reg.layers": "Quatre explications circulent pour expliquer l'enlisement des projets : le promoteur, la procédure, le système, et la capacité budgétaire de l'État. Ce sont des couches, non des rivales, et la bonne question est de savoir laquelle est contraignante en premier. La vôtre est en général la deuxième. Une proposition apportée par un développeur et négociée de gré à gré contourne la planification, la formation du prix et le contrôle qu'un appel d'offres imposerait.",
        "reg.quote": "Les propres lignes directrices de la Banque mondiale sur les offres spontanées avertissent que de tels projets rencontrent souvent des difficultés, notamment en détournant les ressources publiques des plans stratégiques du gouvernement.",
        "reg.ask": "Quatre leviers qui relèvent de votre autorité. Mettre en concurrence par défaut, et là où un appel d'offres est réellement impossible, le dire officiellement et l'expliquer. Confronter toute offre spontanée au plan de moindre coût avant qu'un tarif ne soit indiqué. Traiter un tarif indicatif comme une référence publiée, car c'est ce qu'il devient. Et exiger jalons, dates d'extinction et cautions de développement dans les instruments que vous approuvez.",
        "reg.key": "Un tarif fixé avant toute mise en concurrence ne reste pas indicatif. Il devient la référence contre laquelle le pays devra argumenter pendant des années, et quand l'État le rouvre, les investisseurs relèvent la prime qu'ils exigent sur tout le reste.",
      },
    },

    "MoUTrap-Developers": {
      title: "Ce qui compte comme portefeuille",
      audience: "Développeurs et partenaires au développement",
      copy: {
        "dev.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module D",
          title: "Ce qui compte comme portefeuille",
          subtitle: "Les options sont peu coûteuses à détenir. C'est le problème, et l'occasion.",
          audience: "Développeurs et partenaires au développement",
          runtime: "Chapitre 1",
        },
        "dev.stages": {
          kind: "stage-ladder",
          title: "Ce que vous détenez réellement à chaque étape",
          rows: [
            {
              stage: "MoU",
              signed: "Protocole d'accord",
              binds: "Peu de chose en droit ; souvent exclusivité et confidentialité",
              committed: "Une option sur un site ou une ressource — peu coûteuse à détenir, et revendable",
            },
            {
              stage: "Contrat",
              signed: "CAE, convention de mise en œuvre et accords de soutien",
              binds: "Tarif, durée et obligations des deux parties, sous conditions",
              committed: "Des paiements futurs, conditionnés à la mise en service",
            },
            {
              stage: "Bouclage financier",
              signed: "Contrats de prêt signés, conditions levées, premier tirage effectué",
              binds: "Tout ce qui précède, désormais financé",
              committed: "La seule étape qui compte comme portefeuille",
            },
          ],
          caption: "Un MoU est peu coûteux à obtenir et précieux à détenir. Les options peuvent se revendre. Tableau 1.1",
        },
        "dev.denominator": {
          kind: "funnel",
          title: "Le dénominateur que personne ne publie",
          steps: [
            { label: "MoU signés", note: "Non comptabilisés. Les gouvernements les publient rarement ; les développeurs n'annoncent pas les caducités." },
            { label: "Faisabilité et plan d'affaires", note: "80 % échouent ici" },
            { label: "Bouclage financier", note: "Moins de 10 % des projets y parviennent" },
          ],
          stats: [
            { value: "<10 %", label: "des projets d'infrastructure africains atteignent le bouclage financier", tone: "liability" },
            { value: "30 Md$", label: "de coûts de développement immobilisés en phase de faisabilité, six plus grands marchés", tone: "trap" },
            { value: "8,7 Md$", label: "d'investissement PEI, Afrique subsaharienne hors Afrique du Sud, 1990-2013", tone: "signal" },
            { value: "40,8 Md$", unit: "par an", label: "besoin estimé du secteur électrique", tone: "liability" },
          ],
          unknown:
            "Les partenaires au développement comptent les MoU comme la preuve d'un portefeuille. Ils sont la preuve d'une intention. Le taux de réussite de la voie du MoU est inconnu, parce que personne ne compte ceux qui ne mènent nulle part.",
          cite: "McKinsey 2020 (toutes infrastructures, ordre de grandeur) ; Eberhard et al. 2016 via tralac",
        },
        "dev.nachtigal": {
          kind: "case-card",
          country: "Cameroun",
          project: "Nachtigal — la voie bilatérale bien menée",
          verdict: "Certains projets ne peuvent pas être mis en concurrence dès le départ. Ce livre ne plaide pas pour l'interdiction des MoU.",
          beats: [
            "Accord de développement conjoint entre l'État, EDF, l'IFC et la compagnie nationale — et non un appel d'offres",
            "Bouclage financier atteint avec une tranche en monnaie locale d'une maturité sans précédent pour les banques locales concernées",
            "Mais quelques mois après la mise en service en 2025, la garantie de paiement était signalée largement tirée",
            "La manière dont un projet commence compte. Elle ne décide pas de la manière dont il finira.",
          ],
          cite: "Power Technology 2021 ; IFC 2019 ; Agence Ecofin 2025 — articles de presse",
          tone: "pass",
        },
        "dev.ask": {
          kind: "ask-card",
          audience: "Développeurs et partenaires au développement",
          title: "Ce qu'il faut attendre, et ce qu'il faut mesurer",
          asks: [
            "Développeurs : attendez-vous à ce que les MoU comportent des jalons, des clauses d'extinction et, le cas échéant, des cautions de développement. Les développeurs sérieux n'ont pas grand-chose à en craindre.",
            "Développeurs : attendez-vous à une exclusivité limitée et bornée dans le temps. Un site détenu par un promoteur incapable de le financer le bloque pour celui qui le pourrait.",
            "Partenaires au développement : mesurez les portefeuilles au nombre de projets qui passent les deux tests — et non au nombre de MoU signés.",
            "Pour tous : un MoU publié, confronté au plan et examiné par la compagnie nationale et le ministère des Finances, n'est pas un obstacle. C'est ce qui rend l'option digne d'être détenue.",
          ],
          because:
            "Un MoU confronté au plan avant signature, assorti de jalons et d'une date d'extinction, examiné par les porteurs de risque et publié, n'est plus un piège. C'est un outil de développement.",
        },
        "dev.key": {
          kind: "key-message",
          label: "Message clé",
          text: "Un portefeuille ne se mesure pas au nombre de MoU signés. Il se mesure au nombre de projets capables de passer le test du prêteur et le test de l'État — et la discipline qui les y mène protège d'abord le développeur sérieux.",
          source: "Bankable Is Not Enough — Chapitre 1, Le piège du MoU",
        },
      },
      narration: {
        "dev.title": "Bankable is not enough. Module D, pour les développeurs et les partenaires au développement : ce qui compte comme portefeuille.",
        "dev.stages": "Considérez ce que vous détenez réellement à chaque étape. Un MoU engage peu en droit, mais il accorde souvent une exclusivité : c'est une option sur un site ou une ressource, peu coûteuse à obtenir, précieuse à détenir, et revendable. Un contrat fixe le tarif, la durée et les obligations, sous réserve de la mise en service. Seul le bouclage financier compte comme portefeuille.",
        "dev.denominator": "Et le dénominateur n'est jamais publié. Les gouvernements publient rarement les MoU qu'ils signent, et les développeurs n'ont aucune raison d'annoncer qu'un MoU est devenu caduc. McKinsey estime que moins de dix pour cent des projets d'infrastructure africains atteignent le bouclage financier, que quatre-vingts pour cent échouent au stade de la faisabilité, et qu'environ trente milliards de dollars de coûts de développement sont immobilisés à ce stade dans les six plus grands marchés. Les partenaires au développement comptent les MoU comme la preuve d'un portefeuille. Ils sont la preuve d'une intention.",
        "dev.nachtigal": "Ce n'est pas un plaidoyer pour l'interdiction des MoU. Certains projets ne peuvent pas être mis en concurrence dès le départ, parce que personne n'en sait encore assez pour rédiger un appel d'offres. La centrale camerounaise de Nachtigal a été développée dans le cadre d'un accord de développement conjoint avec EDF, l'IFC et la compagnie nationale, et a atteint le bouclage financier avec une tranche en monnaie locale d'une maturité sans précédent. Mais quelques mois après sa mise en service en 2025, sa garantie de paiement était signalée largement tirée. La manière dont un projet commence compte. Elle ne décide pas de la manière dont il finira.",
        "dev.ask": "Alors, ce qu'il faut attendre et ce qu'il faut mesurer. Développeurs : attendez-vous à ce que les MoU comportent des jalons, des clauses d'extinction et, le cas échéant, des cautions de développement. Les développeurs sérieux n'ont pas grand-chose à en craindre. Attendez-vous à une exclusivité limitée et bornée dans le temps, car un site détenu par un promoteur incapable de le financer le bloque pour celui qui le pourrait. Partenaires au développement : mesurez les portefeuilles au nombre de projets qui passent les deux tests, et non au nombre de MoU signés.",
        "dev.key": "Un portefeuille ne se mesure pas au nombre de MoU signés. Il se mesure au nombre de projets capables de passer le test du prêteur et le test de l'État — et la discipline qui les y mène protège d'abord le développeur sérieux.",
      },
    },
  },
};
