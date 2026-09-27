"""Shot list for "Bankable Is Not Enough, Episode 1: The Signing".

Each shot frames one panel of a book page (panel boxes come from
scripts/panels.json, detected by scripts/detect_panels.py) and lists the lines
spoken over it as (voice_key, text). Text follows the book's wording; spellings
such as "M-O-U" only guide pronunciation. The on-screen art is never altered.

Shot forms:
  ("panel", page, panel_index, lines)            frame one detected panel
  ("pan",   page, rect_from, rect_to, lines)     slow move between two rects
  ("group", page, [panel_indexes], lines)        frame the union of panels
  ("card",  kind, data, lines)                   HTML title/chapter/credit card
"""

# Voice casting (Kokoro-82M voices).
VOICES = {
    "NARRATOR": "bm_george",
    "BELPAU": "af_heart",
    "ENILEC": "bf_emma",
    "TIDIANIE": "af_bella",
    "KERBU": "am_fenrir",
    "EMSON": "am_michael",
    "PAUL": "bm_lewis",
    "RESIDENT": "am_puck",
}

N, B, E, T, K, M, P = "NARRATOR", "BELPAU", "ENILEC", "TIDIANIE", "KERBU", "EMSON", "PAUL"


def red(q):
    return [(N, "Red team question."), (N, q)]


def note(t):
    return [(N, "Decision note."), (N, t)]


SHOTS = [
    ("card", "title", {}, [(N, "Bankable is not enough. Episode one: The Signing.")]),

    # ---------------- Meet the cast (book page 4) ----------------
    ("card", "section", {"title": "MEET THE CAST"}, [(N, "Meet the cast.")]),
    ("panel", 3, 0, [(N, "Belpau. Analyst at KivoElec, the national utility. Curious and stubborn. Reads every clause, even at midnight.")]),
    ("panel", 3, 1, [(N, "Enilec Mok. Director of Public Debt at the Ministry of Finance. Guards the public purse. For her, a guarantee is a debt with a delay.")]),
    ("panel", 3, 2, [(N, "Minister Kerbu. Minister of Energy. Wants power for his people, and fast. Under pressure every day.")]),
    ("panel", 3, 3, [(N, "Emson Anahct. C.E.O. of SunRiver Power. Serious and ambitious. Needs contracts that banks will finance.")]),
    ("panel", 3, 4, [(N, "Tidianie Eugom. Investment officer at a development finance institution. Lends to private projects. Honest about who really carries the risk.")]),
    ("panel", 3, 5, [(N, "Paul Ahmak. Managing Director of KivoElec. Runs a utility short of cash. Knows the grid better than anyone.")]),

    # ---------------- 1. The Promise (pages 6-8) ----------------
    ("card", "chapter", {"n": "1", "title": "THE PROMISE"}, [(N, "Chapter one. The promise.")]),
    ("panel", 5, 0, [(N, "Kivona. Another night without power."), ("RESIDENT", "Again?! The third time this week!")]),
    ("panel", 5, 1, [(N, "Belpau studies by the light of her phone. One day, she thinks, this country will have power every night.")]),
    ("panel", 5, 2, [(N, "Clinics and shops run on diesel generators: expensive, noisy and polluting.")]),
    ("panel", 5, 3, [(N, "Then, the good news."), (N, "The Kivona Herald. Minister promises one hundred megawatts of solar power.")]),
    ("panel", 6, 0, [(K, "Today Kivona signs with SunRiver Power. One hundred megawatts of light for our people!")]),
    ("panel", 6, 1, [(M, "We are ready to build, Minister.")]),
    ("panel", 6, 2, [(N, "An M-O-U is a promise. Financial close is where the promise gets paid for.")]),
    ("panel", 6, 3, note("Across Africa, many power M-O-Us never reach financial close. Those that do are only as strong as the contracts behind them.")),
    ("panel", 7, 0, [(M, "Signed! Now we can raise the money."), (T, "An M-O-U is a good start, Emson. It is not financing.")]),
    ("panel", 7, 1, [(T, "What our credit committee will check. Can the buyer pay? The utility's finances. Is the P-P-A solid and fair? Can the grid take the power? Land, permits and environmental impact. And who carries the currency risk?")]),
    ("panel", 7, 2, [(M, "Then Kivona must give us strong guarantees."), (T, "Or build strong institutions. Guarantees are never free, Emson.")]),
    ("panel", 7, 3, red("What commitment did we just create, and what does it cost to walk away from it?")),

    # ---------------- 2. What Lenders Need (pages 9-10) ----------------
    ("card", "chapter", {"n": "2", "title": "WHAT LENDERS NEED"}, [(N, "Chapter two. What lenders need.")]),
    ("panel", 8, 0, [(M, "Minister, lenders will need a bankable revenue contract and adequate protection against risks that could interrupt debt service. For this project, three things.")]),
    ("panel", 8, 1, [(M, "One: a long-term P-P-A. Twenty years or more of guaranteed purchase. Two: a dollar tariff, so the lenders carry no currency risk. Three: a State guarantee, in case the utility cannot pay."),
                     (N, "I-P-Ps bring private capital, speed and skills. The question is not whether to do the deal, but how.")]),
    ("panel", 8, 2, [(K, "Give him what he needs. Our people want light now!")]),
    ("panel", 8, 3, note("I-P-Ps are part of the solution; the goal is balanced deals, not fewer deals. Lenders need an adequate revenue and credit support structure; the instruments depend on the project's risk profile. What Emson lists are common forms, not universal requirements.")),
    ("panel", 9, 0, [(M, "I am not asking for favours. Without these, no bank will lend.")]),
    ("panel", 9, 1, [(K, "Paul? The P-P-A must be approved by Friday.")]),
    ("panel", 9, 2, [(P, "Friday? Minister, we have not even seen the grid study.")]),
    ("panel", 9, 3, [(N, "Political calendars move faster than contracts. Rushed negotiations are where hidden costs are born.")]),
    ("panel", 9, 4, red("What must be true before Friday, and who has actually checked it?")),

    # ---------------- 3. The Fine Print (pages 11-13) ----------------
    ("card", "chapter", {"n": "3", "title": "THE FINE PRINT"}, [(N, "Chapter three. The fine print.")]),
    ("panel", 10, 0, [(P, "Belpau, the Ministry wants our comments by Friday."), (B, "Friday?! It is three hundred pages!")]),
    ("panel", 10, 1, [(B, "We pay for what the plant can produce... even when our grid cannot take it?")]),
    ("panel", 10, 2, [(N, "Clause seven point two. Capacity payment. The Offtaker shall pay for the Available Capacity, whether or not the energy is dispatched.")]),
    ("panel", 10, 3, [(B, "Questions for Monday. One: take or pay. We pay even if we cannot use the power. Two: a tariff in U.S. dollars. Three: a State guarantee with no ceiling. Four: who pays if the grid is late?")]),
    ("panel", 10, 4, red("What exactly are we paying for: capacity, energy, availability or dispatch?")),
    ("panel", 11, 0, [(N, "Take or pay: the utility pays for available capacity. A one hundred megawatt solar plant. A grid that can absorb sixty. Forty megawatts: paid, never used.")]),
    ("panel", 11, 1, [(B, "Our grid can absorb sixty megawatts today. We would pay for forty megawatts we cannot use.")]),
    ("panel", 11, 2, [(P, "And the line upgrade we need for the full one hundred megawatts is not financed yet.")]),
    ("panel", 11, 3, note("Take or pay is common and protects lenders; it is not bad in itself. Its risk depends on what is paid for, what triggers payment, the caps and exceptions, and who controls the underlying risk. Signing it before the grid, the demand and the utility's cash flow are ready is where it bites.")),
    ("panel", 12, 0, [(N, "KivoElec. For every one hundred billed, seventy are collected, and ninety-five are needed to pay costs and I-P-Ps.")]),
    ("panel", 12, 1, [(P, "We already pay some of our suppliers late."), (B, "So if we miss a payment to SunRiver..."), (P, "...the State guarantee is called, and the bill goes to the Treasury.")]),
    ("panel", 12, 2, note("The strongest guarantee is a utility that can pay. Fixing collection and cash flow reduces the need for State support.")),

    # ---------------- 4. The Hidden Bill (pages 14-16) ----------------
    ("card", "chapter", {"n": "4", "title": "THE HIDDEN BILL"}, [(N, "Chapter four. The hidden bill.")]),
    ("panel", 13, 0, [(E, "A State guarantee? That is not in our budget."), (B, "Not yet. It is a contingent liability.")]),
    ("panel", 13, 1, [(E, "A guarantee needs almost no cash on the day we sign. But the contingent exposure starts when the guarantee is issued, and it can carry fees. That is exactly why it is dangerous."),
                      (N, "On the books: public debt, salaries, schools and roads. Off the books, for now: State guarantees, take or pay commitments, and currency risk.")]),
    ("panel", 13, 2, red("If the guarantee is called next year, where does the money come from, and what else goes unpaid?")),
    ("pan", 14, [221, 411, 2090, 1176], [221, 1596, 2090, 1176],
     [(N, "What the signing ceremony shows: a bankable project."), (N, "What the Treasury may pay later: currency risk. Take or pay. The State guarantee. Utility arrears.")]),
    ("panel", 14, 1, note("A contingent liability is a potential obligation whose timing or amount depends on an uncertain future event. It may not be recorded as debt today, but it must be identified, measured and disclosed before signing, not after.")),
    ("panel", 15, 0, [(E, "Tariff in dollars, revenue in local currency. If our currency falls, who pays the difference?"), (B, "The Treasury.")]),
    ("panel", 15, 1, [(N, "Year one: one dollar buys six hundred Kivona francs. A tariff of ten U.S. cents per kilowatt-hour costs sixty francs. Year five: one dollar buys eight hundred francs, and the same tariff costs eighty. Same tariff in dollars. One third more in local money.")]),
    ("panel", 15, 2, [(E, "Belpau, write it all down. I want to meet their lender."), (B, "Already done.")]),
    ("panel", 15, 3, red("What does this contract cost the utility after a forty percent depreciation? Who has run that number?")),

    # ---------------- 5. Bankable for Whom? (pages 17-18) ----------------
    ("card", "chapter", {"n": "5", "title": "BANKABLE FOR WHOM?"}, [(N, "Chapter five. Bankable, for whom?")]),
    ("panel", 16, 0, [(T, "From our side, the project is bankable. Our loan is protected.")]),
    ("panel", 16, 1, [(E, "Protected by whom?")]),
    ("panel", 16, 2, [(T, "Well... by you.")]),
    ("panel", 16, 3, [(T, "Lenders price risk. When the State carries it, the deal looks cheap. The cost is simply hidden elsewhere."), (E, "Then let us put that cost on the table.")]),
    ("panel", 17, 0, [(N, "A deal can be bankable for the project, and still unsustainable for the country.")]),
    ("panel", 17, 1, [(E, "Around this table, who defends the country's balance sheet?")]),
    ("panel", 17, 2, [(B, "To be frank, nobody trained us for this.")]),
    ("panel", 17, 3, note("Bankability asks: will the lenders be repaid? Sustainability asks: can the country keep paying? Negotiators need to answer both.")),

    # ---------------- 6. Around the Same Table (pages 19-22) ----------------
    ("card", "chapter", {"n": "6", "title": "AROUND THE SAME TABLE"}, [(N, "Chapter six. Around the same table.")]),
    ("panel", 18, 0, [(K, "Are you trying to kill my project?!"), (E, "No, Minister. We are trying to save it.")]),
    ("panel", 18, 1, [(B, "Three risks in this P-P-A. One: take or pay before the grid is ready. Two: full exposure to the dollar. Three: a State guarantee with no ceiling.")]),
    ("panel", 18, 2, [(K, "Call everyone: developer, lender, utility, Finance. Same table, next week.")]),
    ("panel", 18, 3, red("What happens to this deal if demand does not materialise, or if the cheaper hydro plant is dispatched first?")),
    ("panel", 19, 0, [(N, "Instead of fighting the deal, they fixed it."), (K, "Let us fix this deal together.")]),
    ("panel", 19, 1, [(P, "First, we fix our cash flow: meters, collection, and a payment reserve.")]),
    ("panel", 19, 2, [(B, "We phase the plant with the grid upgrade. No paying for power we cannot use.")]),
    ("panel", 19, 3, [(T, "We can add a partial risk guarantee and a local currency loan. Less risk stays with the State.")]),
    ("panel", 19, 4, [(E, "And every guarantee goes into a register, with a ceiling and a yearly risk report.")]),
    ("panel", 20, 0, [(M, "A deal that breaks my client breaks me too. Count me in."), (K, "Then we have a deal.")]),
    ("panel", 20, 1, [(N, "The new deal. Capacity: sixty megawatts now, forty when the grid is ready. Currency: a local currency loan for part of the debt. Guarantee: a capped guarantee, plus a partial risk guarantee from the lender. Utility: a payment reserve and a collection plan. Finance: every commitment in a risk register."),
                      (N, "Same plant. Same developer. Same lenders. A different deal.")]),
    ("panel", 20, 2, red("If this contract terminates in year three, what does the State owe, and where is that number written?")),
    ("panel", 21, 0, [(P, "A joint team: Finance, utility, regulator."), (E, "Next time, we will be ready before the M-O-U is signed."), (B, "And training for all of us.")]),
    ("panel", 21, 1, [(N, "Before the next M-O-U: one team for the public side. The regulator, the Ministry of Energy, the utility and the Ministry of Finance, working as one joint deal team.")]),
    ("panel", 21, 2, note("The tools exist: phasing, liquidity reserves, partial risk guarantees, local currency finance and fiscal risk registers. Using them well requires trained people on the public side, and for large deals, an independent technical, financial, legal, and environmental and social review.")),

    # ---------------- 7. Financial Close (page 23) ----------------
    ("card", "chapter", {"n": "7", "title": "FINANCIAL CLOSE"}, [(N, "Chapter seven. Financial close.")]),
    ("panel", 22, 0, [(N, "Months later. Financial close: Kivona Solar."), (K, "This time, we sign a deal we can keep.")]),
    ("panel", 22, 1, [(N, "Construction begins.")]),
    ("panel", 22, 2, [(E, "Every guarantee: recorded and capped.")]),
    ("panel", 22, 4, red("If the plant's debt service coverage ratio falls below the covenant in year five, who moves first: the lender, the utility, or the Treasury?")),
    ("panel", 22, 3, [(B, "Bankable is the start. Sustainable is the goal."), (N, "The end of episode one.")]),

    # ---------------- Ten questions (page 24) ----------------
    ("card", "section", {"title": "TEN QUESTIONS EVERY NEGOTIATOR MUST ANSWER"}, [(N, "Ten questions every negotiator must answer.")]),
    ("group", 23, [0, 1, 2], [(N, "One. What exactly are we committing to when we sign an M-O-U? Two. Is there a real project behind the promise? Three. Who will buy the electricity, and how much do they need?")]),
    ("group", 23, [3, 4, 5], [(N, "Four. Can the utility actually pay? Five. What exactly does the P-P-A require us to pay? Six. Can the grid absorb the contracted electricity?")]),
    ("group", 23, [6, 7], [(N, "Seven. Who carries currency, demand, grid and political risk? Eight. What is the maximum and the expected fiscal exposure?")]),
    ("group", 23, [8, 9], [(N, "Nine. What happens if the project fails, or the contract terminates? And ten. What must be true before the government signs?")]),

    ("card", "end", {}, [(N, "Bankable is the start. Sustainable is the goal.")]),
    ("card", "credits", {}, []),
]
