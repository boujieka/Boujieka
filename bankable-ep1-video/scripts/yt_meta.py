"""youtube.txt for each MoU Trap episode: title, description, chapters, tags.

usage: yt_meta.py <out_root>   (English; writes en-16x9/episode-n/youtube/youtube.txt
                                and en-9x16/episode-n/youtube/youtube.txt)
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
    1: [("s0", "Opening"), (11, "A signing ceremony"), ("s3", "Six seats at the table"),
        ("s4", "Fact, decision, red team"), ("s5", "Nigeria's 14 solar PPAs"), ("s13", "Where the deals stopped")],
    2: [("s0", "Opening"), ("s2", "What an MoU binds"), ("s4", "What it does in practice"),
        ("s6", "Three stages of commitment"), ("s7", "Where the trap lies"), ("s8", "Two tests: lender and state")],
    3: [("s0", "Opening"), ("s2", "How few projects close"), ("s4", "Private power investment, 1990-2014"),
        ("s5", "Qua Iboe, Nigeria"), ("s6", "The denominator problem"), ("s7", "Four layers"),
        ("s8", "Credible sponsors, still stalled")],
    4: [("s0", "Opening"), ("s2", "STOP: you are the minister"), (38, "Who is in the room"),
        ("s4", "Incentives at signature"), ("s5", "Why capable ministries sign"), ("s6", "Exit one: the project stalls"),
        ("s9", "Exit two: the project closes")],
    5: [("s0", "Opening"), ("s2", "Ghana: 43 non-competitive PPAs"), ("s6", "Lenders satisfied, state's test failed"),
        ("s7", "Questions asked too late"), ("s8", "When an MoU makes sense"), ("s10", "Cameroon's Nachtigal"),
        ("s11", "Exposed to a weak buyer")],
    6: [("s0", "Opening"), ("s2", "From trap to development tool"), ("s3", "The five costs"),
        ("s4", "Four measures"), ("s5", "Pricing the option is not enough"), ("s6", "The Sustainable Financial Close Test")],
    7: [("s0", "Opening"), (10, "The cabinet decides"), ("s3", "Red team"),
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

TAGS = ["#MoUTrap", "#EnergyPolicy", "#Africa", "#PowerSector", "#InfrastructureFinance"]


def starts(project):
    h = open(os.path.join(project, "index.html")).read()
    return {a: float(b) for a, b in re.findall(r'id="(s\d+)"[^>]*?data-start="([\d.]+)"', h)}


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def main(out_root):
    for n in range(1, 8):
        h_proj = os.path.join(out_root, "en-16x9", f"episode-{n}")
        st = starts(h_proj)
        times = [(0 if i == 0 else (st[k] if isinstance(k, str) else k), lab) for i, (k, lab) in enumerate(CHAPTERS[n])]
        for i in range(1, len(times)):  # YouTube needs 10 s per chapter; nudge near-misses
            if times[i][0] - times[i - 1][0] < 10:
                assert times[i][0] - times[i - 1][0] >= 9, (n, times[i])
                times[i] = (times[i - 1][0] + 10, times[i][1])
        chap = "\n".join(f"{mmss(t)} {lab}" for t, lab in times)
        nxt = (f"Next: Episode {n + 1}/7 · {TITLES[n]}" if n < 7 else "This is the last episode of the series.")
        prev = f"Previous: Episode {n - 1}/7 · {TITLES[n - 2]}\n" if n > 1 else ""
        foot = ("Characters are fictional. Figures and cases are as reported in the public sources named in the "
                "narration; they are summarised, not independently verified here.\n"
                "Adapted from Chapter 1, \"The MoU Trap\". Produced by Courant Continental.")
        for fmt in ("16x9", "9x16"):
            short = fmt == "9x16"
            title = f"{SERIES} · Ep {n}/7: {TITLES[n - 1]}" + (" #Shorts" if short else "")
            assert len(title) <= 100, title
            body = [f"TITLE\n{title}\n", "DESCRIPTION", SUMMARY[n], "",
                    f"Episode {n} of 7 in \"{SERIES}\", a cartoon training series for ministers, cabinets, "
                    "regulators and other power-sector decision-makers.", "", prev + nxt, ""]
            if not short:
                body += ["CHAPTERS", chap, ""]
            body += [foot, "", " ".join(TAGS + (["#Shorts"] if short else [])), "",
                     "SETTINGS (suggested)",
                     "Playlist: " + SERIES + " (in order, episodes 1-7)",
                     "Category: Education · Language: English · Captions: " +
                     ("burned in" if short else "upload captions.srt from the project folder"),
                     "Thumbnail: " + ("cover.png (YouTube may only let you pick a frame for Shorts; use cover.png for posts and playlists)" if short else "thumbnail.png")]
            d = os.path.join(out_root, f"en-{fmt}", f"episode-{n}", "youtube")
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "youtube.txt"), "w").write("\n".join(body) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
