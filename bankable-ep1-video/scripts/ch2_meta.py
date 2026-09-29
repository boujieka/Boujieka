"""youtube.txt for the Chapter 2 long-form videos (EN and FR).

usage: ch2_meta.py <out_root> [en|fr]   reads <out_root>/<lang>/chapters.txt, writes <lang>/youtube/youtube.txt
"""
import os
import re
import sys

LABELS = {
    "en": {"Cold open": "The day the deal closes", "Title": "Two tests, one framework", "The lesson": "The key message"},
    "fr": {"Ouverture": "Le jour du bouclage", "Titre": "Deux tests, un cadre", "La leçon": "Le message clé"},
}

TXT = {
    "en": {
        "title": "Two Tests, One Framework: why a bankable power deal is not enough | Bankable Is Not Enough, Ch. 2",
        "summary": ("A power project that lenders will finance has passed only half of its examination. This chapter of "
                    "Bankable Is Not Enough sets out the lender's test and the missing state's test, the two-test matrix "
                    "(sustainable financial close, the liability trap, the reform gap and the MoU graveyard), diagonal "
                    "risk, and a framework of seven dimensions and two questions for African power deals."),
        "audience": ("A cartoon training video for ministers, ministries of finance, regulators, utilities, lenders and "
                     "development partners."),
        "sources_h": "Main sources cited on screen (full references in the chapter):",
        "foot": ("The 120 MW plant is a composite case, not a single transaction. Characters are fictional. Figures and "
                 "quotations are as reported in the sources named on screen; they are summarised here, not independently "
                 "verified.\nBased on Chapter 2 of Bankable Is Not Enough, by Emmanuel Boujieka Kamga. "
                 "Produced by Courant Continental."),
        "prev": "Previous: Chapter 1, The MoU Trap (full module and 7-episode series on this channel).",
        "tags": ["#EnergyPolicy", "#Africa", "#PowerSector", "#ProjectFinance", "#PublicFinance", "#Mission300"],
        "lang": "English",
    },
    "fr": {
        "title": "Deux tests, un cadre : pourquoi un projet électrique bancable ne suffit pas | Bancable ne suffit pas, ch. 2",
        "summary": ("Un projet électrique que les prêteurs acceptent de financer n'a réussi que la moitié de son examen. "
                    "Ce chapitre présente le test du prêteur et le test manquant de l'État, la matrice des deux tests "
                    "(bouclage durable, piège du passif, fossé des réformes, cimetière des MoU), le risque diagonal, et un "
                    "cadre de sept dimensions et deux questions pour les projets électriques africains."),
        "audience": ("Une vidéo de formation en dessin animé pour les ministres, les ministères des Finances, les "
                     "régulateurs, les compagnies d'électricité, les prêteurs et les partenaires au développement."),
        "sources_h": "Principales sources citées à l'écran (références complètes dans le chapitre) :",
        "foot": ("La centrale de 120 MW est un cas composite, pas une transaction réelle. Les personnages sont fictifs. "
                 "Les chiffres et citations sont ceux des sources indiquées à l'écran ; les citations sont traduites "
                 "librement de l'anglais. Ils sont résumés ici, sans vérification indépendante.\n"
                 "D'après le chapitre 2 de Bankable Is Not Enough, d'Emmanuel Boujieka Kamga. "
                 "Une production Courant Continental."),
        "prev": "Précédent : chapitre 1, Le piège du MoU (module complet et série en 7 épisodes sur cette chaîne).",
        "tags": ["#Énergie", "#Afrique", "#Électricité", "#FinancementDeProjets", "#FinancesPubliques", "#Mission300"],
        "lang": "French",
    },
}

SOURCES = ["CLDP and ALSF 2024 (Power Africa, Understanding Power Project Financing)",
           "Eberhard and Gratwick 2011; Eberhard et al. 2016, 2017", "Kojima and Trimble 2016; Trimble et al. 2016",
           "Foster and Rana 2020", "IRENA 2026; ESMAP 2026", "Polackova 1999",
           "IMF 2023, 2024a, 2024b (Ghana)", "World Bank 2025 and n.d. (Mission 300)"]


def main(out_root, lang="en"):
    t = TXT[lang]
    assert len(t["title"]) <= 100, len(t["title"])
    chap = []
    for line in open(os.path.join(out_root, lang, "chapters.txt")).read().splitlines():
        m = re.match(r"(\d\d):(\d\d) (.*)", line)
        if not m:
            continue
        mm, ss, label = int(m.group(1)), m.group(2), m.group(3)
        if label in LABELS[lang]:
            label = LABELS[lang][label]
        else:  # "02 - What Earlier Research" -> "2 · What earlier research"
            label = re.sub(r"^0(\d) - ", r"\1 · ", label)
            head, _, rest = label.partition(" · ")
            rest = rest[:1] + rest[1:].lower().replace("mou", "MoU")
            label = f"{head} · {rest}"
        chap.append(f"{mm}:{ss} {label}")
    body = [f"TITLE\n{t['title']}\n", "DESCRIPTION", t["summary"], "", t["audience"], "", t["prev"], "",
            "CHAPTERS", "\n".join(chap), "", t["sources_h"]] + [f"- {s}" for s in SOURCES] + \
           ["", t["foot"], "", " ".join(t["tags"]), "", "SETTINGS (suggested)",
            f"Category: Education · Language: {t['lang']} · Captions: upload captions.srt from the project folder",
            "Thumbnail: thumbnail.png"]
    d = os.path.join(out_root, lang, "youtube")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "youtube.txt"), "w").write("\n".join(body) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])
