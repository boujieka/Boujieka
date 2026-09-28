"""VERSION A - DOCUMENTARY SHORT (9:16 vertical, under 3 min for Shorts/TikTok/LinkedIn).

Same method, compressed: promise -> four tests -> red team -> climax -> lesson.
Captions are burned in for sound-off viewing.
"""
from v2cards import *  # noqa: F401,F403

CHAPTERS = ["PROMISE", "TESTS", "RISKS", "DECISION"]

SHOTS = [
    panel(6, 0, [(K, "Today Kivona signs with SunRiver Power. One hundred megawatts of light for our people!")], music="bed"),
    panel(6, 1, [(M, "We are ready to build, Minister.")], cut=True),
    panel(7, 0, [(T, "An M-O-U is a good start, Emson. It is not financing.")], cut=True),
    big("Everything looks promising.", [(N, "Everything looks promising.")], hold=0.3),
    big("But is the project<br/>really ready?", [(N, "But is the project really ready?")], hold=1.2, music="silence"),
    title_card([(N, "Bankable is not enough.")]),

    act("TEST 1", "CAN THE UTILITY PAY?", [(N, "Test one. Can the utility pay?")], chapter=1),
    panel(12, 0, [(N, "For every one hundred billed, seventy are collected. Ninety-five are needed.")], music="tension"),
    panel(12, 1, [(B, "So if we miss a payment to SunRiver..."), (P, "...the State guarantee is called, and the bill goes to the Treasury.")]),

    act("TEST 2", "CAN THE GRID ABSORB IT?", [(N, "Test two. Can the grid absorb the power?")], chapter=1),
    panel(11, 0, [(N, "A one hundred megawatt plant. A grid that can absorb sixty. Forty megawatts: paid, never used.")], music="tension"),

    act("TEST 3", "WHO CARRIES THE RISK?", [(N, "Test three. Who carries the risk?")], chapter=2),
    big("Tariff: <b>10 US cents</b>/kWh", [(N, "The tariff: ten U.S. cents.")], code="fact", hold=0.2),
    big("Year 1: <b>60 KVF</b>/kWh", [(N, "Year one: sixty Kivona francs.")], code="fact", hold=0.2),
    big("Year 5: <b class='red'>80 KVF</b>/kWh", [(N, "Year five: eighty.")], code="fact", hold=0.3),
    big("Same dollar tariff.<br/>One third more<br/>in local money.", [(N, "Same dollar tariff. One third more in local money.")], hold=0.5, music="tension"),
    big("WHO CARRIES<br/>THE FX RISK?", [(N, "Who carries the currency risk?")], code="red", hold=1.5, sting="risk", music="silence"),

    act("TEST 4", "CAN THE PUBLIC SECTOR<br/>LIVE WITH IT?", [(N, "Test four. Can the public sector live with it?")], chapter=2),
    panel(16, 0, [(T, "Our loan is protected.")], cut=True),
    panel(16, 1, [(E, "Protected by whom?")], cut=True),
    panel(16, 2, [(T, "Well... by you.")], cut=True),
    big("A guarantee costs almost nothing<br/>on the day you sign.", [(E, "A guarantee needs almost no cash on the day we sign.")], hold=0.3, music="tension"),
    big("<span class='red'>That is exactly why<br/>it is dangerous.</span>", [(E, "That is exactly why it is dangerous.")], hold=0.8, music="tension"),

    redteam(("What could make this deal fail?", [(N, "Red team. What could make this deal fail?")]),
            [("The offtaker cannot pay", [(N, "The offtaker cannot pay.")]),
             ("The grid cannot absorb the power", [(N, "The grid cannot absorb the power.")]),
             ("Hidden State obligations", [(N, "The government carries hidden obligations.")])],
            ("Don't ask if it is attractive.<br/><b>Ask what could break it.</b>",
             [(N, "Don't ask whether the project is attractive. Ask what could break it.")])),

    act("THE DECISION", "SHOULD WE SIGN?", [(N, "Should we sign?")], chapter=3),
    ladder([("BANKABLE", "Lenders can finance it.", [(N, "Bankable.")], True),
            ("AFFORDABLE", "The system can carry the cost.", [(N, "Affordable.")], False),
            ("EXECUTABLE", "Grid and institutions can deliver.", [(N, "Executable.")], False),
            ("SUSTAINABLE", "Public obligations stay manageable.", [(N, "Sustainable.")], False)],
           ("BANKABLE &#8800; SUSTAINABLE", [(N, "Bankable is not the same as sustainable.")]),
           ("BANKABLE IS NOT ENOUGH.", [])),
    panel(22, 3, [(B, "Bankable is the start. Sustainable is the goal.")], music="theme"),
    lesson([(N, "Bankable is not enough.")], [(N, "Before you sign, test the deal.")], []),
    big("Episode 1: The Signing<br/><small>Full training video &amp; book</small>",
        [], hold=2.5, music="theme"),
]
