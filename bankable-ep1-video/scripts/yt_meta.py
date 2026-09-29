"""youtube.txt for each MoU Trap episode: title, description, chapters, tags.

usage: yt_meta.py <out_root> [en|fr]   (writes <lang>-16x9/episode-n/youtube/youtube.txt
                                        and <lang>-9x16/episode-n/youtube/youtube.txt)
Chapter times are the episode's shot starts (seconds), read from the built 16:9 project.
"""
import os
import re
import sys

SERIES = "The MoU Trap"
TITLES = ["Fourteen contracts, no power", "What an MoU really binds", "Why projects stall",
          "Who is in the room?", "When the deal closes anyway", "Closing the trap", "Before you sign"]

# (shot id or seconds, label). Only labels at least 10 s apart; the first is 0:00.
CHAPTERS = {
    1: [("s0", "Opening"), ("e:s1", "A signing ceremony"), ("s3", "Six seats at the table"),
        ("s4", "Fact, decision, red team"), ("s5", "Nigeria's 14 solar PPAs"), ("s13", "Where the deals stopped")],
    2: [("s0", "Opening"), ("s2", "What an MoU binds"), ("s4", "What it does in practice"),
        ("s6", "Three stages of commitment"), ("s7", "Where the trap lies"), ("s8", "Two tests: lender and state")],
    3: [("s0", "Opening"), ("s2", "How few projects close"), ("s4", "Private power investment, 1990-2014"),
        ("s5", "Qua Iboe, Nigeria"), ("s6", "The denominator problem"), ("s7", "Four layers"),
        ("s8", "Credible sponsors, still stalled")],
    4: [("s0", "Opening"), ("s2", "STOP: you are the minister"), ("e:s2", "Who is in the room"),
        ("s4", "Incentives at signature"), ("s5", "Why capable ministries sign"), ("s6", "Exit one: the project stalls"),
        ("s9", "Exit two: the project closes")],
    5: [("s0", "Opening"), ("s2", "Ghana: 43 non-competitive PPAs"), ("s6", "Lenders satisfied, state's test failed"),
        ("s7", "Questions asked too late"), ("s8", "When an MoU makes sense"), ("s10", "Cameroon's Nachtigal"),
        ("s11", "Exposed to a weak buyer")],
    6: [("s0", "Opening"), ("s2", "From trap to development tool"), ("s3", "The five costs"),
        ("s4", "Four measures"), ("s5", "Pricing the option is not enough"), ("s6", "The Sustainable Financial Close Test")],
    7: [("s0", "Opening"), ("e:s1", "The cabinet decides"), ("s3", "Red team"),
        ("s4", "Five questions before signing"), ("s5", "The lesson")],
}

SUMMARY = {
    1: "In July 2016, Nigeria's bulk electricity trader signed power purchase agreements with fourteen solar developers: "
       "some 1,125 MW at 11.5 US cents per kWh, fixed for 20 years. Three years later, none had reached financial close. "
       "Why a signed commitment is not yet a financeable one.",
    2: "A memorandum of understanding binds almost no one in law, yet it does a lot in practice: exclusivity, an "
       "indicative tariff that anchors every later negotiation, promises of state help, and a public political "
       "commitment. The two tests an MoU is signed before: the lender's test and the state's test.",
    3: "McKinsey estimated that fewer than ten percent of African infrastructure projects reach financial close (all "
       "sectors, so an order of magnitude). The Qua Iboe gas plant in Nigeria, the denominator problem, and four layers "
       "of explanation: sponsor, process, system and fiscal.",
    4: "Why does the trap persist when everyone can describe it? Look at who is in the room at signature, and who is "
       "not: the utility that must pay, the ministry of finance, the lenders. Then the two exits, both costly: the "
       "project stalls, or it closes under pressure.",
    5: "Ghana signed 43 PPAs through non-competitive processes during and after a supply crisis; in 2019 net sector "
       "arrears stood at US$2.75 billion. Then the fair case for MoUs, and Cameroon's Nachtigal hydropower plant: "
       "well structured, and still exposed to a weak buyer.",
    6: "The five costs of the trap, and four measures to close it: filter at entry against the least-cost plan, price "
       "the option, bring the utility and the ministry of finance in early, and publish a register of power MoUs. "
       "Plus the Sustainable Financial Close Test.",
    7: "A cabinet meeting that gets it right, the red-team summary, and five questions to ask before any power MoU "
       "is signed. The final episode of the series.",
}

# French: same chapter anchors as CHAPTERS, labels in the same order
FR = {
    "series": "Le piège du MoU",
    "titles": ["Quatorze contrats, aucun mégawatt", "Ce qu'engage vraiment un MoU", "Pourquoi les projets s'enlisent",
               "Qui est dans la salle ?", "Quand l'accord aboutit quand même", "Refermer le piège", "Avant de signer"],
    "chapters": {
        1: ["Ouverture", "Une cérémonie de signature", "Six sièges autour de la table", "Fait, décision, red team",
            "Nigeria : 14 contrats solaires", "Là où les projets se sont arrêtés"],
        2: ["Ouverture", "Ce qu'engage un MoU", "Ce qu'il fait en pratique", "Trois étapes d'engagement",
            "Où se situe le piège", "Deux tests : le prêteur et l'État"],
        3: ["Ouverture", "Si peu de projets bouclés", "Investissement privé, 1990-2014", "Qua Iboe, Nigeria",
            "Le problème du dénominateur", "Quatre couches", "Des promoteurs crédibles, et pourtant bloqué"],
        4: ["Ouverture", "STOP : vous êtes le ministre", "Qui est dans la salle", "Les incitations à la signature",
            "Pourquoi des ministères compétents signent", "Première issue : le projet s'enlise",
            "Deuxième issue : le projet aboutit"],
        5: ["Ouverture", "Ghana : 43 contrats sans concurrence", "Prêteurs satisfaits, test de l'État échoué",
            "Des questions posées trop tard", "Quand un MoU se justifie", "Nachtigal, Cameroun",
            "Exposé à un acheteur fragile"],
        6: ["Ouverture", "Du piège à l'outil de développement", "Les cinq coûts", "Quatre mesures",
            "Donner un prix à l'option ne suffit pas", "Le test du bouclage financier durable"],
        7: ["Ouverture", "Le conseil des ministres décide", "Red team", "Cinq questions avant de signer", "La leçon"],
    },
    "summary": {
        1: "En juillet 2016, l'acheteur d'électricité en gros du Nigeria signe des contrats d'achat avec quatorze "
           "développeurs solaires : quelque 1 125 MW à 11,5 cents de dollar le kWh, fixés pour 20 ans. Trois ans plus "
           "tard, aucun n'avait atteint le bouclage financier. Pourquoi un engagement signé n'est pas encore un "
           "engagement finançable.",
        2: "Un protocole d'accord n'engage presque personne en droit, mais il fait beaucoup en pratique : exclusivité, "
           "tarif indicatif qui devient la référence de toute négociation, promesses d'aide de l'État et engagement "
           "politique public. Les deux tests que l'on n'applique pas avant de signer : celui du prêteur et celui de "
           "l'État.",
        3: "McKinsey estimait que moins de dix pour cent des projets d'infrastructure africains atteignent le "
           "bouclage financier (tous secteurs : un ordre de grandeur). La centrale au gaz de Qua Iboe au Nigeria, le "
           "problème du dénominateur, et quatre couches d'explication : promoteur, procédure, système et budget.",
        4: "Pourquoi le piège persiste-t-il alors que tout le monde sait le décrire ? Regardez qui est dans la salle "
           "au moment de la signature, et qui n'y est pas : la compagnie qui doit payer, le ministère des Finances, "
           "les prêteurs. Puis les deux issues, toutes deux coûteuses : le projet s'enlise, ou il aboutit sous la "
           "pression.",
        5: "Pendant et après une crise d'approvisionnement, le Ghana signe 43 contrats d'achat sans mise en "
           "concurrence ; en 2019, les arriérés nets du secteur atteignent 2,75 milliards de dollars. Puis la défense "
           "honnête des protocoles d'accord, et la centrale hydroélectrique de Nachtigal au Cameroun : bien "
           "structurée, et pourtant exposée à un acheteur fragile.",
        6: "Les cinq coûts du piège, et quatre mesures pour le refermer : filtrer à l'entrée selon le plan de moindre "
           "coût, donner un prix à l'option, associer tôt la compagnie d'électricité et le ministère des Finances, et "
           "publier un registre des protocoles d'accord. Et le test du bouclage financier durable.",
        7: "Un conseil des ministres qui fait les choses dans l'ordre, la synthèse red team, et cinq questions à "
           "poser avant de signer tout protocole d'accord énergétique. Le dernier épisode de la série.",
    },
    "tags": ["#PiègeDuMoU", "#Énergie", "#Afrique", "#Électricité", "#FinancementDesInfrastructures"],
}

TAGS = ["#MoUTrap", "#EnergyPolicy", "#Africa", "#PowerSector", "#InfrastructureFinance"]


def starts(project):
    """shot id -> start; "e:<id>" -> end of that shot (start of the unlisted scene after it)."""
    h = open(os.path.join(project, "index.html")).read()
    out = {}
    for a, b, d in re.findall(r'id="(s\d+)"[^>]*?data-start="([\d.]+)" data-duration="([\d.]+)"', h):
        out[a], out["e:" + a] = float(b), float(b) + float(d) - 0.3
    return out


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def main(out_root, lang="en"):
    fr = lang == "fr"
    series = FR["series"] if fr else SERIES
    titles = FR["titles"] if fr else TITLES
    for n in range(1, 8):
        st = starts(os.path.join(out_root, f"{lang}-16x9", f"episode-{n}"))
        labels = FR["chapters"][n] if fr else [lab for _, lab in CHAPTERS[n]]
        assert len(labels) == len(CHAPTERS[n]), n
        times = [(0 if i == 0 else (st[k] if isinstance(k, str) else k), lab)
                 for i, ((k, _), lab) in enumerate(zip(CHAPTERS[n], labels))]
        i = 1
        while i < len(times):  # YouTube needs 10 s per chapter: nudge near-misses, drop a too-short one
            gap = times[i][0] - times[i - 1][0]
            if gap < 9 and i > 1:
                del times[i - 1]
                continue
            if gap < 10:
                times[i] = (times[i - 1][0] + 10, times[i][1])
            i += 1
        chap = "\n".join(f"{mmss(t)} {lab}" for t, lab in times)
        if fr:
            nxt = (f"Épisode suivant : {n + 1}/7 · {titles[n]}" if n < 7 else "C'est le dernier épisode de la série.")
            prev = f"Épisode précédent : {n - 1}/7 · {titles[n - 2]}\n" if n > 1 else ""
            foot = ("Les personnages sont fictifs. Les chiffres et les cas sont ceux rapportés par les sources publiques "
                    "citées dans la narration ; ils sont résumés ici, sans vérification indépendante.\n"
                    "Adapté du chapitre 1, « Le piège du MoU ». Une production Courant Continental.")
            intro = (f"Épisode {n} sur 7 de « {series} », une série de formation en dessin animé pour les ministres, "
                     "les cabinets, les régulateurs et les autres décideurs du secteur électrique.")
        else:
            nxt = (f"Next: Episode {n + 1}/7 · {titles[n]}" if n < 7 else "This is the last episode of the series.")
            prev = f"Previous: Episode {n - 1}/7 · {titles[n - 2]}\n" if n > 1 else ""
            foot = ("Characters are fictional. Figures and cases are as reported in the public sources named in the "
                    "narration; they are summarised, not independently verified here.\n"
                    "Adapted from Chapter 1, \"The MoU Trap\". Produced by Courant Continental.")
            intro = (f"Episode {n} of 7 in \"{series}\", a cartoon training series for ministers, cabinets, "
                     "regulators and other power-sector decision-makers.")
        tags = FR["tags"] if fr else TAGS
        for fmt in ("16x9", "9x16"):
            short = fmt == "9x16"
            title = (f"{series} · Ép. {n}/7 : {titles[n - 1]}" if fr else f"{series} · Ep {n}/7: {titles[n - 1]}")
            title += " #Shorts" if short else ""
            assert len(title) <= 100, title
            body = [f"TITLE\n{title}\n", "DESCRIPTION", (FR["summary"] if fr else SUMMARY)[n], "", intro, "",
                    prev + nxt, ""]
            if not short:
                body += ["CHAPTERS", chap, ""]
            body += [foot, "", " ".join(tags + (["#Shorts"] if short else [])), "",
                     "SETTINGS (suggested)",
                     "Playlist: " + series + " (in order, episodes 1-7)",
                     f"Category: Education · Language: {'French' if fr else 'English'} · Captions: " +
                     ("burned in" if short else "upload captions.srt from the project folder"),
                     "Thumbnail: " + ("cover.png (YouTube may only let you pick a frame for Shorts; use cover.png "
                                      "for posts and playlists)" if short else "thumbnail.png")]
            d = os.path.join(out_root, f"{lang}-{fmt}", f"episode-{n}", "youtube")
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "youtube.txt"), "w").write("\n".join(body) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])
