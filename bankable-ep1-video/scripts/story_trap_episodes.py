"""THE MoU TRAP as a YouTube series: the core module cut into 7 episodes of 3 minutes or less.

Each episode = logo opening -> episode card -> a contiguous run of core-module
shots (nothing dropped except the long-form title and pause instruction, which
the episode cards replace) -> end card announcing the next episode.
VIDEO_LANG=fr uses the French core module and French cards.
"""
import copy

from trap_common import *  # noqa: F401,F403
from trap_common import part, screen, esc
from lang import LANG

if LANG == "fr":
    import story_trap_core_fr as core
    SERIES, EP, NEXT, LAST = "LE PIÈGE DU MoU", "ÉPISODE", "Prochain épisode", "Fin de la série"
    TITLES = ["Quatorze contrats, aucun mégawatt", "Ce qu'engage vraiment un MoU", "Pourquoi les projets s'enlisent",
              "Qui est dans la salle ?", "Quand l'accord aboutit quand même", "Refermer le piège", "Avant de signer"]
    SPOKEN_SERIES = "Le piège du protocole d'accord"
else:
    import story_trap_core as core
    SERIES, EP, NEXT, LAST = "THE MoU TRAP", "EPISODE", "Next episode", "End of the series"
    TITLES = ["Fourteen contracts, no power", "What an MoU really binds", "Why projects stall",
              "Who is in the room?", "When the deal closes anyway", "Closing the trap", "Before you sign"]
    SPOKEN_SERIES = "The M-O-U trap"

# core-module shot indices per episode (see scripts/story_trap_core.py order)
CUTS = [[1, 3, 4] + list(range(6, 15)), list(range(15, 22)), list(range(22, 29)), list(range(29, 37)),
        list(range(37, 47)), list(range(47, 52)), list(range(52, 57))]
N_EP = len(CUTS)


def _spoken_title(t):
    return t.replace("MoU", "M-O-U" if LANG != "fr" else "protocole d'accord")


def ep_card(n):
    t = TITLES[n - 1]
    say = (f"{SPOKEN_SERIES}. Épisode {n}. {_spoken_title(t)}" if LANG == "fr"
           else f"{SPOKEN_SERIES}. Episode {n}. {_spoken_title(t)}")
    return screen("act", [part(f'<div class="act-label">{SERIES} · {EP} {n}/{N_EP}</div>'),
                          part(f'<div class="act-title">{esc(t.upper()).replace("MOU", "MoU")}</div>', [(N, say)], 0.8)],
                  None, "theme", "act", 0)


def end_card(n):
    if n < N_EP:
        nxt = TITLES[n]
        head = f'{NEXT} · {EP} {n + 1}/{N_EP}'
        say = (f"Prochain épisode : {_spoken_title(nxt)}." if LANG == "fr" else f"Next episode: {_spoken_title(nxt)}.")
        body = esc(nxt)
    else:
        head, nxt = LAST, ""
        say = ("Merci d'avoir suivi la série. Retrouvez le module complet et les briefings sur Courant Continental."
               if LANG == "fr" else "Thank you for watching the series. Find the full module and the role briefings on Courant Continental.")
        body = "Courant Continental"
    follow = "Abonnez-vous à Courant Continental" if LANG == "fr" else "Subscribe to Courant Continental"
    return screen("lesson", [part(f'<div class="ls2">{esc(head)}</div>'),
                             part(f'<div class="ls1">{body}</div>', [(N, say)], 0.8),
                             part(f'<div class="ls3">{follow}</div>', [], 1.6)], None, "theme", "act")


def build_episode(n):
    shots = [logo_intro(hold=2.8), ep_card(n)]
    for i in CUTS[n - 1]:
        sh = copy.deepcopy(core.SHOTS[i])
        sh["chapter"] = None
        shots.append(sh)
    shots.append(end_card(n))
    return shots


EPISODES = {n: build_episode(n) for n in range(1, N_EP + 1)}
for _n in range(1, N_EP + 1):
    globals()[f"EP{_n}"] = EPISODES[_n]
    globals()[f"EP{_n}_CHAPTERS"] = [f"{EP} {_n}/{N_EP} · {TITLES[_n - 1].upper()}".replace("MOU", "MoU")]
CHAPTERS = [""]
