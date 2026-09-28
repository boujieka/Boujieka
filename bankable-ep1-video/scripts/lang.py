"""Language switch for the v2 builds: VIDEO_LANG=fr python scripts/build_v2.py <video>.

Holds on-screen interface strings and, for French, the voice recipes. Kokoro has
one native French voice (ff_siwis); character voices are blends of ff_siwis with
other Kokoro voices, which keeps French pronunciation while giving each
character a distinct pitch and timbre.
"""
import os

LANG = os.environ.get("VIDEO_LANG", "en")

UI = {
    "en": {"fact": "FACT", "decision": "DECISION", "red": "RED TEAM", "stop_spoken": "Stop.",
           "pause": "Pause the video and answer before continuing.", "q": "THE QUESTION", "ev": "THE EVIDENCE",
           "dec": "THE DECISION", "signals": "THREE SIGNALS", "source": "Source:", "ceremony": "MoU SIGNING CEREMONY",
           "cold_open": "Cold open", "title": "Title", "ladder": "Bankable vs sustainable", "checklist": "Before you sign",
           "redteam": "Red team", "lesson": "The lesson"},
    "fr": {"fact": "FAIT", "decision": "DÉCISION", "red": "RED TEAM", "stop_spoken": "Stop.",
           "pause": "Mettez la vidéo en pause et répondez avant de continuer.", "q": "LA QUESTION", "ev": "LES FAITS",
           "dec": "LA DÉCISION", "signals": "TROIS SIGNAUX", "source": "Source :", "ceremony": "SIGNATURE DU MoU",
           "cold_open": "Ouverture", "title": "Titre", "ladder": "Bancable ou durable", "checklist": "Avant de signer",
           "redteam": "Red team", "lesson": "La leçon"},
}


def ui(key):
    return UI.get(LANG, UI["en"])[key]


# French voices: narrator = ff_siwis (native, warm); characters = blends.
FR_VOICES = {
    "NARRATOR": ([("ff_siwis", 1.0)], 0.94),
    "BELPAU": ([("ff_siwis", 0.5), ("af_heart", 0.5)], 1.0),
    "ENILEC": ([("ff_siwis", 0.5), ("bf_emma", 0.5)], 0.97),
    "TIDIANIE": ([("ff_siwis", 0.5), ("af_nicole", 0.5)], 1.0),
    "KERBU": ([("ff_siwis", 0.5), ("am_fenrir", 0.5)], 0.97),
    "EMSON": ([("ff_siwis", 0.5), ("am_michael", 0.5)], 1.0),
    "PAUL": ([("ff_siwis", 0.5), ("bm_lewis", 0.5)], 0.95),
    "RESIDENT": ([("ff_siwis", 0.5), ("am_onyx", 0.5)], 1.0),
}
