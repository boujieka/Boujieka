import type { LocaleBundle } from "../types";

/**
 * English copy. Every figure here is traceable to Chapter 1 of
 * "Bankable Is Not Enough" by Emmanuel Boujieka Kamga, and carries the same
 * caveats the chapter attaches to it. Where the chapter footnotes a number as
 * press-sourced or unverified, the on-screen citation says so.
 */
export const en: LocaleBundle = {
  chrome: {
    series: "Bankable Is Not Enough",
    chapter: "Chapter 1 — The MoU Trap",
    author: "Emmanuel Boujieka Kamga",
    sourceLabel: "Source",
    testLender: "The lender's test",
    testState: "The state's test",
    continues: "continues",
    colSigned: "What is signed",
    colBinds: "What binds",
    colCommitted: "What the state has committed",
    tableLabel: "Table",
    bearsRiskLabel: "Carries the risk",
    absentLabel: "Not at the table",
  },

  films: {
    "MoUTrap-Core": {
      title: "The MoU Trap",
      audience: "All stakeholders",
      copy: {
        "core.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough",
          title: "The MoU Trap",
          subtitle: "Why signed commitments fail to become power — and what it costs when they succeed",
          audience: "Core briefing",
          runtime: "Chapter 1",
        },

        "core.nigeria": {
          kind: "cold-open",
          kicker: "Fourteen contracts, no power",
          place: "Nigeria",
          date: "July 2016",
          headline:
            "Nigeria's bulk electricity trader signed power purchase agreements with fourteen solar developers.",
          stats: [
            { value: "14", label: "solar developers signed", tone: "signal" },
            { value: "1,125", unit: "MW", label: "to be added to the grid", tone: "signal" },
            { value: "11.5", unit: "US¢/kWh", label: "fixed for twenty years", tone: "trap" },
            { value: "18", unit: "months", label: "target to first power", tone: "trap" },
          ],
          cite: "Green Street n.d.; pv magazine 2019; Offgrid Nigeria 2020",
        },

        "core.flip": {
          kind: "stat-flip",
          before: { value: "1,125", unit: "MW", label: "promised", tone: "signal" },
          after: { value: "0", label: "electrons delivered", tone: "liability" },
          verdict:
            "Three years on, none of the fourteen had reached financial close. Ten of the front-runners had reportedly already posted development security bonds.",
          cite: "Offgrid Nigeria 2020 — the bulk buyer has not published its own record of securities received",
        },

        "core.tests": {
          kind: "two-tests",
          title: "Two tests. One of them is almost never applied.",
          lender: {
            name: "The lender's test",
            question: "Can the project repay its debt?",
            asker: "Asked by banks and DFIs — years after signature",
          },
          state: {
            name: "The state's test",
            question:
              "Can the power system and the public finances carry this project's obligations for twenty years or more?",
            asker: "Asked by nobody in the room at signature",
          },
          footnote:
            "An MoU — and often the first contract after it — is signed before either test has been applied.",
        },

        "core.stages": {
          kind: "stage-ladder",
          title: "Three stages public debate runs together",
          rows: [
            {
              stage: "MoU",
              signed: "Memorandum of understanding",
              binds: "Little in law; often exclusivity and confidentiality",
              committed: "A political signal; sometimes a site or a resource",
            },
            {
              stage: "Contract",
              signed: "PPA, implementation and support agreements",
              binds: "Tariff, term and obligations of both parties, subject to conditions",
              committed: "Future payments, conditional on the plant reaching operation",
            },
            {
              stage: "Financial close",
              signed: "Loan agreements signed, conditions satisfied, first drawdown made",
              binds: "All of the above, now funded",
              committed: "Fixed obligations for the life of the contract",
            },
          ],
          caption: "The trap lies between the first row and the third. Table 1.1",
        },

        "core.denominator": {
          kind: "funnel",
          title: "How far is announcement from close?",
          steps: [
            { label: "MoUs signed", note: "Not counted. Rarely published." },
            { label: "Feasibility and business plan", note: "80% fail here" },
            { label: "Financial close", note: "Fewer than 10% of projects arrive" },
          ],
          stats: [
            { value: "<10%", label: "of African infrastructure projects reach financial close", tone: "liability" },
            { value: "US$30bn", label: "of development costs sitting in the feasibility phase, six largest markets", tone: "trap" },
            { value: "US$8.7bn", label: "IPP investment, Sub-Saharan Africa excl. South Africa, 1990–2013", tone: "signal" },
            { value: "US$40.8bn", unit: "per year", label: "estimated power sector need", tone: "liability" },
          ],
          unknown:
            "The denominator problem: databases record the projects that closed. Nobody counts the MoUs that went nowhere, so the success rate of the MoU route is unknown.",
          cite: "McKinsey 2020 (all infrastructure, order of magnitude); Eberhard et al. 2016 via tralac — needs figure includes transmission and distribution",
        },

        "core.layers": {
          kind: "layers",
          title: "Four explanations — read as layers, not rivals",
          layers: [
            {
              id: "sponsor",
              name: "Sponsor",
              where: "The developer",
              policy: "Screen sponsors; limit exclusivity; attach milestones and securities",
            },
            {
              id: "process",
              name: "Process",
              where: "How the project was originated",
              policy: "Compete by default; test unsolicited proposals against the plan",
            },
            {
              id: "system",
              name: "System",
              where: "The plan, the grid and the buyer",
              policy: "Fix the system before adding contracts",
            },
            {
              id: "fiscal",
              name: "Fiscal",
              where: "The state's capacity to support",
              policy: "Apply the sovereign test and size support to fiscal space",
            },
          ],
          closing:
            "Nigeria's solar programme displays all four at once. The useful question is which layer binds first — the answer tells a government what to fix. Table 1.2",
        },

        "core.quaiboe": {
          kind: "case-card",
          country: "Nigeria",
          project: "Qua Iboe — 533 MW gas-fired",
          verdict: "Credible sponsors are not enough.",
          beats: [
            "2014 — World Bank approves a partial risk guarantee of up to US$150 million",
            "2017 — the federal government approves the PPA",
            "May 2018 — the final extension for signing the guarantee agreements expires, after two exceptional twelve-month extensions",
            "2020 — reported stalled; listed as shelved in early 2026",
            "Sponsors included an international oil major, a private-equity-owned infrastructure company, one of Nigeria's biggest industrial groups and the national oil company",
          ],
          cite: "World Bank 2014; TheCable 2020; Global Energy Monitor 2026; Templars n.d.; Reuters 2018",
          tone: "trap",
        },

        "core.actors": {
          kind: "actor-table",
          title: "Why the trap persists: who gains at signature, who pays later",
          rows: [
            {
              actor: "Government",
              offers: "A visible response to power shortages",
              costs: "Little; costs, if any, come later",
              incentive: "Sign readily",
              bearsRisk: false,
            },
            {
              actor: "Developer",
              offers: "An option on a site, a resource or a market — which can be sold",
              costs: "Early studies and staff time",
              incentive: "Collect options",
              bearsRisk: false,
            },
            {
              actor: "Utility",
              offers: "Often nothing, since it may not be a party",
              costs: "Nothing yet; the obligations come later",
              incentive: "Stay passive",
              bearsRisk: true,
            },
            {
              actor: "Treasury",
              offers: "Not a row in Table 1.3 at all",
              costs: "Nothing yet",
              incentive: "Sees the project when terms are nearly settled",
              bearsRisk: true,
              absent: true,
            },
            {
              actor: "Lenders",
              offers: "Nothing, since they are rarely involved yet",
              costs: "Nothing",
              incentive: "No early filter",
              bearsRisk: false,
            },
            {
              actor: "Development partners",
              offers: "Evidence of a pipeline",
              costs: "Nothing directly",
              incentive: "Count what is signed",
              bearsRisk: false,
            },
          ],
          closing:
            "The parties that will carry the risk — the utility and the treasury — are absent or passive. The parties that test hardest, the lenders, arrive years later. Capacity is not the explanation: capable ministries sign weak MoUs too, because a signature is rewarded today and paid for later, by someone else. Table 1.3",
        },

        "core.exits": {
          kind: "two-exits",
          title: "Two exits from the trap. Both are costly.",
          stall: {
            name: "It stalls",
            detail:
              "Years of ministry time and developer spending produce no power. Sites stay locked up. A published tariff becomes a benchmark later bidders must argue against.",
            cost: "The country loses time, money and options",
          },
          close: {
            name: "It closes",
            detail:
              "A project announced at the highest level does not simply lapse. Pressure builds to give lenders whatever they require: a state guarantee, fixed capacity payments, a hard currency tariff.",
            cost: "The country inherits a liability",
          },
          shared:
            "Both exits share a cause. The questions that decide whether a contract is sustainable were asked too late, or by people with no authority to say no.",
        },

        "core.ghana": {
          kind: "case-card",
          country: "Ghana",
          project: "The expensive exit",
          verdict: "These contracts satisfied their lenders. Together, they failed the state's test.",
          beats: [
            "2014–2017 — three emergency power producers contracted without a competitive process",
            "43 PPAs signed by the national distribution utility through noncompetitive processes",
            "1,900 MW of projected excess capacity by 2019",
            "US$2.75 billion in net sector arrears when the Energy Sector Recovery Programme launched in 2019",
            "More than US$500 million a year reportedly paid for electricity not used",
          ],
          cite: "World Bank 2018; Ministry of Energy, Ghana 2019; ESI Africa n.d. — the US$500m figure is trade press, not checked against a primary government document",
          tone: "liability",
        },

        "core.nachtigal": {
          kind: "case-card",
          country: "Cameroon",
          project: "Nachtigal — the case for the MoU, and its warning",
          verdict: "How a project begins matters. It does not settle how it will end.",
          beats: [
            "Developed under a joint development agreement between the state, EDF, IFC and the national utility — not, as far as public sources show, through a competitive tender",
            "Reached financial close with a local currency tranche whose tenor was without precedent for the local banks involved",
            "Within months of full commissioning in 2025, the press reported the payment guarantee was largely drawn",
            "The ministry of finance was reported to be seeking a bank facility to secure payments to the project",
            "A well structured project remains exposed to a weak buyer",
          ],
          cite: "Power Technology 2021; IFC 2019; Ecofin Agency 2025 — press reports; no official statement found at the time of writing",
          tone: "pass",
        },

        "core.costs": {
          kind: "cost-list",
          title: "Five costs. Usually only the first is counted.",
          items: [
            { name: "Power not delivered", detail: "Capacity a plan assumed and consumers never received" },
            { name: "Better projects blocked", detail: "An exclusive right held by a developer who cannot finance the site keeps it from one who could" },
            { name: "Public attention consumed", detail: "Ministries with few specialists spend years on projects that will not close" },
            { name: "Credibility lost", detail: "When signed terms are reopened, investors raise the premium they charge the whole country" },
            { name: "Liabilities created", detail: "When trapped projects do close, under political pressure, on terms set when they were least tested" },
          ],
          note: "Only the first cost appears in most reporting. The other four are paid quietly, for twenty years.",
        },

        "core.remedies": {
          kind: "remedy-list",
          title: "Bring the cost forward, and bring the risk bearers into the room",
          items: [
            {
              n: "1",
              name: "Filter at entry",
              detail: "No MoU for a project outside the least-cost plan unless it has first been tested against the plan",
              chapter: "Chapter 4",
            },
            {
              n: "2",
              name: "Put a price on the option",
              detail: "Development securities, milestones and sunset clauses, so holding a site without progress costs something",
              chapter: "Chapter 8",
            },
            {
              n: "3",
              name: "Bring the risk bearers in early",
              detail: "The utility and the ministry of finance review any MoU that could lead to fixed payments or state support",
              chapter: "Chapters 7 and 12",
            },
            {
              n: "4",
              name: "Publish a register",
              detail: "A public register of power MoUs and their status, so lapsed options become visible and better projects can come forward",
              chapter: "Chapter 18",
            },
          ],
          closing:
            "Nigeria shows that pricing the option is not enough on its own. The trap has to be closed at every point where a project is tested — which is the purpose of the Sustainable Financial Close Test: a deal closes only when both tests have been passed, and the state's answer has been made public. Chapter 16",
        },

        "core.key": {
          kind: "key-message",
          label: "Key message",
          text: "An MoU costs almost nothing to sign and can cost a great deal later, either as power that never arrives or as a contract the system cannot carry. The trap persists because those who will bear the risk are absent when the commitment is made. Closing it means bringing the risk bearers, and the tests they would apply, to the start of the process.",
          source: "Bankable Is Not Enough — Chapter 1, The MoU Trap",
        },
      },
      narration: {
        "core.title": "Bankable is not enough. Chapter one: the MoU trap.",
        "core.nigeria": "In July 2016, Nigeria's bulk electricity trader signed power purchase agreements with fourteen solar developers. The plants were to range from fifty to a hundred megawatts, and together add some one thousand one hundred and twenty-five megawatts to a grid known for its unreliability. The tariff was eleven and a half US cents per kilowatt hour, fixed for twenty years. The signing was widely celebrated. The target for first power was eighteen months.",
        "core.flip": "Three years later, none of the fourteen had reached financial close. Ten of the front-runners had reportedly already paid development security bonds. In 2020, a specialist publication summed the programme up in a headline: one thousand one hundred and twenty-five megawatts promised, not one electron delivered.",
        "core.tests": "This book is built on two tests. The first is the lender's test: can the project repay its debt? The second is the state's test: can the power system and the public finances carry this project's obligations for twenty years or more? An MoU, and often the first contract that follows it, is signed before either test has been applied.",
        "core.stages": "Public debate runs three stages together. An MoU binds little in law, though it often grants exclusivity. A contract fixes tariff, term and obligations, conditional on the plant reaching operation. Financial close funds all of it, and the obligations become fixed for the life of the contract. The trap lies between the first stage and the third.",
        "core.denominator": "No one knows how many power MoUs African governments have signed, or what share reach financial close. McKinsey estimated that fewer than ten percent of African infrastructure projects reach close, and that eighty percent fail at the feasibility stage. Excluding South Africa, private power investment in sub-Saharan Africa between 1990 and 2013 came to eight point seven billion dollars, against needs of roughly forty point eight billion a year. This is the denominator problem: databases record the projects that closed. Nobody counts the ones that went nowhere.",
        "core.layers": "Four explanations circulate for why projects stall. The sponsor explanation blames the developer. The process explanation blames how the project was originated. The system explanation points to the plan, the grid and the buyer. The fiscal explanation points to the state's capacity to support. These are usually presented as competitors. They are better read as layers. The useful question is which layer binds first.",
        "core.quaiboe": "Qua Iboe removes the easiest explanation. Its sponsors were credible: an international oil major, a private-equity-owned infrastructure company, one of Nigeria's biggest industrial groups, and the national oil company. The World Bank approved a partial risk guarantee of up to a hundred and fifty million dollars in 2014. The project stalled all the same, and the public record points to the buyer and to the state's exposure, not to the sponsors.",
        "core.actors": "The trap persists because of who gains and who pays at the moment of signature. Government gets a visible response to power shortages, at little immediate cost. Developers get an option, which can be sold. The utility is often not even a party. The lenders are not there yet. And the two parties that will carry the risk — the utility and the treasury — are absent or passive. A shortage of ministry capacity is part of the story, but it does not account for persistence. Countries with capable ministries sign weak MoUs too, because a signature is rewarded today and its cost is paid later, and by someone else.",
        "core.exits": "A commitment caught in the trap leaves it in one of two ways. It stalls, and the country loses time, money and options. Or it closes on terms fixed when the project was least tested, and the country inherits a liability. Both exits begin with the same omission.",
        "core.ghana": "Ghana shows where the second exit leads. Between 2014 and 2017, three emergency power producers were contracted without a competitive process, and the national distribution utility signed forty-three power purchase agreements through noncompetitive processes. Contracted plants were projected to create one thousand nine hundred megawatts of excess capacity by 2019. When Ghana launched its Energy Sector Recovery Programme, net sector arrears stood at two point seven five billion dollars. These contracts had satisfied their lenders. Taken together, they failed the state's test.",
        "core.nachtigal": "The case for MoUs is not a weak one. Some projects cannot be tendered at the outset, because nobody yet knows enough to write a tender. Cameroon's Nachtigal hydropower plant was developed under a joint development agreement, not a competitive tender, and reached financial close with a local currency tranche without precedent for the banks involved. But Nachtigal carries a warning. Within months of full commissioning in 2025, the press reported that its payment guarantee was largely drawn, and that the ministry of finance was seeking a bank facility to secure payments. A well structured project remains exposed to a weak buyer.",
        "core.costs": "The MoU trap has five costs, and usually only the first is counted. The power not delivered. The better projects blocked. The public attention consumed. The credibility lost when signed terms are reopened. And the liabilities created when trapped projects do close, under political pressure, on terms set when they were least tested.",
        "core.remedies": "If the trap exists because an MoU costs nothing at signature, and its risks fall on parties who are not in the room, the remedy is to bring both the cost and those parties forward. Filter at entry. Put a price on the option. Bring the risk bearers in early. And publish a register. Nigeria shows that pricing the option is not enough on its own. The trap has to be closed at every point where a project is tested, by the institution best placed to test it.",
        "core.key": "An MoU costs almost nothing to sign, and can cost a great deal later — either as power that never arrives, or as a contract the system cannot carry. The trap persists because those who will bear the risk are absent when the commitment is made. Closing it means bringing the risk bearers, and the tests they would apply, to the start of the process.",
      },
    },

    "MoUTrap-Ministers": {
      title: "Before You Sign",
      audience: "Ministers and Cabinet",
      copy: {
        "min.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module A",
          title: "Before You Sign",
          subtitle: "What a memorandum of understanding actually commits you to",
          audience: "Ministers and Cabinet",
          runtime: "Chapter 1",
        },
        "min.flip": {
          kind: "stat-flip",
          before: { value: "1,125", unit: "MW", label: "signed and celebrated, Nigeria 2016", tone: "signal" },
          after: { value: "0", label: "electrons delivered, four years on", tone: "liability" },
          verdict:
            "These were not MoUs. They were signed power purchase agreements, and most developers had put money down. They stopped where most African power commitments stop.",
          cite: "Offgrid Nigeria 2020; pv magazine 2019",
        },
        "min.actors": {
          kind: "actor-table",
          title: "At the signing table, and after it",
          rows: [
            {
              actor: "You",
              offers: "A visible response to power shortages",
              costs: "Little; costs, if any, come later",
              incentive: "Sign readily",
              bearsRisk: false,
            },
            {
              actor: "Developer",
              offers: "An option on a site or a market — which can be sold",
              costs: "Early studies and staff time",
              incentive: "Collect options",
              bearsRisk: false,
            },
            {
              actor: "Utility",
              offers: "Often nothing — it may not even be a party",
              costs: "Nothing yet; the obligations come later",
              incentive: "Stay passive",
              bearsRisk: true,
            },
            {
              actor: "Treasury",
              offers: "Nothing. Usually not consulted.",
              costs: "Nothing yet",
              incentive: "Sees the project when terms are nearly settled",
              bearsRisk: true,
              absent: true,
            },
            {
              actor: "Lenders",
              offers: "Nothing — they arrive years later",
              costs: "Nothing",
              incentive: "No early filter",
              bearsRisk: false,
            },
          ],
          closing:
            "A public signing, particularly one attended by a head of state, creates a political commitment harder to withdraw than any clause in the document. The two parties who will pay for it are not in the room.",
        },
        "min.exits": {
          kind: "two-exits",
          title: "What you are choosing between, without knowing it",
          stall: {
            name: "It stalls",
            detail:
              "Ministry time and developer money produce no power. The site stays locked. Your published tariff becomes the benchmark every later bidder argues against. Reopening signed terms raises the country's risk premium.",
            cost: "Time, money and options lost",
          },
          close: {
            name: "It closes",
            detail:
              "Announced at the highest level, the project cannot simply lapse. Pressure builds to give lenders a state guarantee, fixed capacity payments and a hard currency tariff — on terms set when the project was least tested.",
            cost: "A twenty-year liability inherited",
          },
          shared:
            "Both begin with the same omission: nobody asked whether the grid could carry it, whether the buyer could pay, or whether the state could stand behind them.",
        },
        "min.ask": {
          kind: "ask-card",
          audience: "Ministers and Cabinet",
          title: "Four things to require before the next signature",
          asks: [
            "Publish a register of power MoUs, with status and expiry dates — and let lapsed options expire. This first step costs almost nothing.",
            "Require any MoU for a project outside the least-cost plan to be tested against the plan before it is signed.",
            "Ensure the ministry of finance and the utility have seen any MoU that could lead to fixed payments or state support — before signature, not when lenders arrive with term sheets.",
            "Attach milestones, a sunset date and, where appropriate, development securities. Serious developers have little to fear from any of these.",
          ],
          because:
            "An MoU checked against the plan, carrying milestones and a sunset date, reviewed by the risk bearers and published, is no longer a trap. It is a development tool.",
        },
        "min.key": {
          kind: "key-message",
          label: "Key message",
          text: "An MoU costs almost nothing to sign and can cost a great deal later, either as power that never arrives or as a contract the system cannot carry. The trap persists because those who will bear the risk are absent when the commitment is made.",
          source: "Bankable Is Not Enough — Chapter 1, The MoU Trap",
        },
      },
      narration: {
        "min.title": "Bankable is not enough. Module A, for ministers and cabinet: before you sign.",
        "min.flip": "In 2016 Nigeria signed power purchase agreements for one thousand one hundred and twenty-five megawatts of solar. Four years later, not one electron had been delivered. These were not memoranda of understanding. They were signed contracts, and most of the developers had put money down. They stopped where most African power commitments stop.",
        "min.actors": "Consider who is at the table when you sign, and who is not. You get a visible response to power shortages, at little immediate cost. The developer gets an option, which can be sold. The utility is often not even a party. The treasury is usually not consulted until the terms are nearly settled. And the lenders, who will test the project hardest, arrive years later. The two parties who will actually pay for this commitment are not in the room.",
        "min.exits": "That omission leaves you with two outcomes, and you do not get to choose which. The project stalls, and the country loses time, money and options — and reopening signed terms raises the risk premium investors charge the whole country. Or the project closes, under political pressure, on terms fixed when it was least tested, and the country inherits a twenty-year liability.",
        "min.ask": "Four things to require before the next signature. Publish a register of power MoUs, with status and expiry dates, and let lapsed options expire — this first step costs almost nothing. Require any MoU outside the least-cost plan to be tested against the plan before signature. Ensure the ministry of finance and the utility have seen any MoU that could create fixed payments or state support. And attach milestones, a sunset date, and where appropriate, development securities. Serious developers have little to fear from any of these.",
        "min.key": "An MoU costs almost nothing to sign and can cost a great deal later. The trap persists because those who will bear the risk are absent when the commitment is made.",
      },
    },

    "MoUTrap-Finance": {
      title: "The State's Test",
      audience: "Ministries of Finance and Treasury",
      copy: {
        "fin.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module B",
          title: "The State's Test",
          subtitle: "The liability begins at a signature you were not shown",
          audience: "Ministries of Finance and Treasury",
          runtime: "Chapter 1",
        },
        "fin.tests": {
          kind: "two-tests",
          title: "The test only you can apply",
          lender: {
            name: "The lender's test",
            question: "Can the project repay its debt?",
            asker: "Applied rigorously — by banks and DFIs, at financial close",
          },
          state: {
            name: "The state's test",
            question:
              "Can the power system and the public finances carry this project's obligations for twenty years or more?",
            asker: "Applied by you — usually far too late, if at all",
          },
          footnote:
            "Even where a DFI co-develops from the start, the ministry of finance tends to see the project only when its terms are nearly settled. The absence that matters most is the absence of the state's test.",
        },
        "fin.ghana": {
          kind: "case-card",
          country: "Ghana",
          project: "When bankable contracts break the budget",
          verdict: "Every one of these contracts satisfied its lenders. Together they failed the state's test.",
          beats: [
            "2014–2017 — three emergency power producers contracted without a competitive process",
            "43 PPAs signed by the national distribution utility through noncompetitive processes",
            "1,900 MW of projected excess capacity by 2019 — capacity payments owed on power not needed",
            "US$2.75 billion in net sector arrears at the launch of the Energy Sector Recovery Programme, 2019",
            "More than US$500 million a year reportedly paid for electricity not used",
          ],
          cite: "World Bank 2018; Ministry of Energy, Ghana 2019; ESI Africa n.d. — the US$500m figure is trade press, not verified against a primary government document",
          tone: "liability",
        },
        "fin.nachtigal": {
          kind: "case-card",
          country: "Cameroon",
          project: "Nachtigal — good structure, weak buyer",
          verdict: "A well structured project remains exposed to a weak buyer.",
          beats: [
            "Joint development agreement between the state, EDF, IFC and the national utility",
            "Financial close achieved with a local currency tranche of unprecedented tenor for the local banks",
            "Within months of full commissioning in 2025, the payment guarantee was reported largely drawn",
            "The ministry of finance was reported to be seeking a bank facility to secure payments to the project",
          ],
          cite: "Power Technology 2021; IFC 2019; Ecofin Agency 2025 — press reports; no official statement found at the time of writing",
          tone: "trap",
        },
        "fin.ask": {
          kind: "ask-card",
          audience: "Ministries of Finance and Treasury",
          title: "What to claim, and when",
          asks: [
            "Claim sight of every MoU that could lead to fixed payments or state support — at MoU stage, not when lenders arrive with term sheets.",
            "Size state support to fiscal space, not to what the lender's term sheet requires. Guarantees, capacity payments and hard-currency tariffs are contingent liabilities whether or not they are recorded as such.",
            "Treat a drawn payment guarantee as a systems failure, not a cash-flow event: Nachtigal was well structured and still exposed the treasury within months of commissioning.",
            "Insist the state's answer is made public at close — the Sustainable Financial Close Test asks that both tests pass, and that the state's answer be published.",
          ],
          because:
            "A signature is rewarded today; its cost is paid later, and by you. Bringing the state's test forward is the only way that changes.",
        },
        "fin.key": {
          kind: "key-message",
          label: "Key message",
          text: "Many of the liabilities that arrive on your desk began in an MoU you were never shown. Closing the trap means bringing the risk bearers, and the tests they would apply, to the start of the process.",
          source: "Bankable Is Not Enough — Chapter 1, The MoU Trap",
        },
      },
      narration: {
        "fin.title": "Bankable is not enough. Module B, for ministries of finance and treasury: the state's test.",
        "fin.tests": "Two tests decide whether a power contract survives. The lender's test asks whether the project can repay its debt. That test is applied rigorously, by banks and development finance institutions, at financial close. The state's test asks something different: can the power system and the public finances carry this project's obligations for twenty years or more? Only you can apply that test. Even where a development finance institution co-develops from the start, the ministry of finance tends to see the project only when its terms are nearly settled. The absence that matters most is the absence of the state's test.",
        "fin.ghana": "Ghana shows what happens when only the lender's test is applied. Between 2014 and 2017, three emergency power producers were contracted without competition, and the national distribution utility signed forty-three power purchase agreements through noncompetitive processes. Contracted plants were projected to create one thousand nine hundred megawatts of excess capacity by 2019. When the Energy Sector Recovery Programme launched, net sector arrears stood at two point seven five billion dollars, and the country was reported to be paying more than five hundred million dollars a year for electricity it did not use. Every one of these contracts satisfied its lenders.",
        "fin.nachtigal": "Nor is good structure a defence on its own. Cameroon's Nachtigal plant was developed under a joint development agreement with EDF, the IFC and the national utility, and reached financial close with a local currency tranche of unprecedented tenor. Within months of full commissioning in 2025, the press reported its payment guarantee was largely drawn, and that the ministry of finance was seeking a bank facility to secure payments. A well structured project remains exposed to a weak buyer.",
        "fin.ask": "So: claim sight of every MoU that could lead to fixed payments or state support, at MoU stage, not when lenders arrive with term sheets. Size state support to fiscal space, not to what the term sheet requires. Treat a drawn payment guarantee as a systems failure, not a cash-flow event. And insist that the state's answer is made public at close.",
        "fin.key": "Many of the liabilities that arrive on your desk began in an MoU you were never shown. Closing the trap means bringing the risk bearers, and the tests they would apply, to the start of the process.",
      },
    },

    "MoUTrap-Regulators": {
      title: "Price Discovery and the Benchmark You Inherit",
      audience: "Regulators and procurement authorities",
      copy: {
        "reg.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module C",
          title: "The Benchmark You Inherit",
          subtitle: "What an administratively set tariff costs when the market moves",
          audience: "Regulators and procurement authorities",
          runtime: "Chapter 1",
        },
        "reg.tariff": {
          kind: "cold-open",
          kicker: "A tariff set before any price discovery",
          place: "Nigeria",
          date: "2016 → 2019",
          headline:
            "Nigeria's solar tariff was set administratively, before any competitive price discovery. When solar costs fell, the government tried to reopen it, and the programme stalled over the dispute.",
          stats: [
            { value: "11.5", unit: "US¢/kWh", label: "agreed 2016, fixed for 20 years", tone: "signal" },
            { value: "7.5", unit: "US¢/kWh", label: "sought by government in 2019", tone: "trap" },
            { value: "0", label: "projects at financial close", tone: "liability" },
            { value: "7", unit: "years+", label: "analysts still proposing ways out in 2023", tone: "liability" },
          ],
          cite: "pv magazine 2019; Energy for Growth Hub 2023",
        },
        "reg.layers": {
          kind: "layers",
          title: "Which layer binds first? Yours is usually the second.",
          layers: [
            {
              id: "sponsor",
              name: "Sponsor",
              where: "The developer",
              policy: "Screen sponsors; limit exclusivity; attach milestones and securities",
            },
            {
              id: "process",
              name: "Process",
              where: "How the project was originated — bypassing planning, price discovery and scrutiny",
              policy: "Compete by default; test unsolicited proposals against the plan",
            },
            {
              id: "system",
              name: "System",
              where: "The plan, the grid and the buyer",
              policy: "Fix the system before adding contracts",
            },
            {
              id: "fiscal",
              name: "Fiscal",
              where: "The state's capacity to support",
              policy: "Apply the sovereign test and size support to fiscal space",
            },
          ],
          closing:
            "A proposal brought by a developer and negotiated directly bypasses the planning, price discovery and scrutiny a tender would impose. That is the layer a regulator is placed to bind first. Table 1.2",
        },
        "reg.quote": {
          kind: "quote",
          text: "Such projects often run into trouble, among other things by diverting public resources away from the strategic plans of the government.",
          attribution: "World Bank and PPIAF, Policy Guidelines for Managing Unsolicited Proposals in Infrastructure Projects, 2017",
        },
        "reg.ask": {
          kind: "ask-card",
          audience: "Regulators and procurement authorities",
          title: "Four things within your authority",
          asks: [
            "Compete by default. Where a tender is genuinely impossible — a large hydropower site, a cross-border interconnector, a first project in a new technology — say so on the record and explain why.",
            "Test every unsolicited proposal against the least-cost plan before any tariff is indicated, however carefully it is labelled non-binding.",
            "Treat an indicative tariff as a published benchmark, because it becomes one. Every later bidder will argue against it, and reopening it costs the country credibility.",
            "Require milestones, sunset dates and development securities in the instruments you approve, so that holding a site without progress costs something.",
          ],
          because:
            "An indicative tariff, however labelled, becomes the reference point for every later negotiation. Price discovery that does not happen before signature happens afterwards, as a dispute.",
        },
        "reg.key": {
          kind: "key-message",
          label: "Key message",
          text: "A tariff set before price discovery does not stay indicative. It becomes the benchmark the country must argue against for years — and when the state reopens it, investors raise the premium they charge on everything else.",
          source: "Bankable Is Not Enough — Chapter 1, The MoU Trap",
        },
      },
      narration: {
        "reg.title": "Bankable is not enough. Module C, for regulators and procurement authorities: the benchmark you inherit.",
        "reg.tariff": "Nigeria's solar tariff was set administratively, before any competitive price discovery: eleven and a half US cents per kilowatt hour, fixed for twenty years. When solar costs fell, the government sought to cut it to around seven and a half cents. The programme stalled over the dispute. Not one of the fourteen projects reached financial close, and as late as 2023, analysts were still proposing ways out of the deadlock.",
        "reg.layers": "Four explanations circulate for why projects stall — the sponsor, the process, the system, and the state's fiscal capacity. They are layers, not rivals, and the useful question is which binds first. Yours is usually the second. A proposal brought by a developer and negotiated directly bypasses the planning, the price discovery and the scrutiny that a tender would impose.",
        "reg.quote": "The World Bank's own guidelines on unsolicited proposals warn that such projects often run into trouble, among other things by diverting public resources away from the strategic plans of the government.",
        "reg.ask": "Four things within your authority. Compete by default, and where a tender is genuinely impossible, say so on the record and explain why. Test every unsolicited proposal against the least-cost plan before any tariff is indicated. Treat an indicative tariff as a published benchmark, because that is what it becomes. And require milestones, sunset dates and development securities in the instruments you approve.",
        "reg.key": "A tariff set before price discovery does not stay indicative. It becomes the benchmark the country must argue against for years, and when the state reopens it, investors raise the premium they charge on everything else.",
      },
    },

    "MoUTrap-Developers": {
      title: "What Counts as a Pipeline",
      audience: "Developers and development partners",
      copy: {
        "dev.title": {
          kind: "title-card",
          series: "Bankable Is Not Enough — Module D",
          title: "What Counts as a Pipeline",
          subtitle: "Options are cheap to hold. That is the problem, and the opportunity.",
          audience: "Developers and development partners",
          runtime: "Chapter 1",
        },
        "dev.stages": {
          kind: "stage-ladder",
          title: "What you actually hold at each stage",
          rows: [
            {
              stage: "MoU",
              signed: "Memorandum of understanding",
              binds: "Little in law; often exclusivity and confidentiality",
              committed: "An option on a site or a resource — cheap to hold, and saleable",
            },
            {
              stage: "Contract",
              signed: "PPA, implementation and support agreements",
              binds: "Tariff, term and obligations of both parties, subject to conditions",
              committed: "Future payments, conditional on the plant reaching operation",
            },
            {
              stage: "Financial close",
              signed: "Loan agreements signed, conditions satisfied, first drawdown made",
              binds: "All of the above, now funded",
              committed: "The only stage that counts as a pipeline",
            },
          ],
          caption: "An MoU is cheap to obtain and valuable to hold. Options can be sold. Table 1.1",
        },
        "dev.denominator": {
          kind: "funnel",
          title: "The denominator nobody publishes",
          steps: [
            { label: "MoUs signed", note: "Not counted. Governments rarely publish them; developers do not announce lapses." },
            { label: "Feasibility and business plan", note: "80% fail here" },
            { label: "Financial close", note: "Fewer than 10% of projects arrive" },
          ],
          stats: [
            { value: "<10%", label: "of African infrastructure projects reach financial close", tone: "liability" },
            { value: "US$30bn", label: "of development costs sitting in the feasibility phase, six largest markets", tone: "trap" },
            { value: "US$8.7bn", label: "IPP investment, Sub-Saharan Africa excl. South Africa, 1990–2013", tone: "signal" },
            { value: "US$40.8bn", unit: "per year", label: "estimated power sector need", tone: "liability" },
          ],
          unknown:
            "Development partners count MoUs as evidence of a pipeline. They are evidence of intent. The success rate of the MoU route is unknown, because nobody counts the ones that go nowhere.",
          cite: "McKinsey 2020 (all infrastructure, order of magnitude); Eberhard et al. 2016 via tralac",
        },
        "dev.nachtigal": {
          kind: "case-card",
          country: "Cameroon",
          project: "Nachtigal — the bilateral route done well",
          verdict: "Some projects cannot be tendered at the outset. This book does not argue for banning MoUs.",
          beats: [
            "Joint development agreement between the state, EDF, IFC and the national utility — not a competitive tender",
            "Reached financial close with a local currency tranche whose tenor was without precedent for the local banks involved",
            "But within months of commissioning in 2025, the payment guarantee was reported largely drawn",
            "How a project begins matters. It does not settle how it will end.",
          ],
          cite: "Power Technology 2021; IFC 2019; Ecofin Agency 2025 — press reports",
          tone: "pass",
        },
        "dev.ask": {
          kind: "ask-card",
          audience: "Developers and development partners",
          title: "What to expect, and what to measure",
          asks: [
            "Developers: expect MoUs to carry milestones, sunset clauses and, where appropriate, development securities. Serious developers have little to fear from any of these.",
            "Developers: expect exclusivity to be limited and time-boxed. A site held by a sponsor who cannot finance it blocks one who could.",
            "Development partners: measure pipelines by the number of projects that pass both tests — not by the number of MoUs signed.",
            "Everyone: a published MoU, checked against the plan and reviewed by the utility and the ministry of finance, is not an obstacle. It is what makes the option worth holding.",
          ],
          because:
            "An MoU that has been checked against the plan before signature, that carries milestones and a sunset date, that the risk bearers have reviewed, and that has been published, is no longer a trap. It is a development tool.",
        },
        "dev.key": {
          kind: "key-message",
          label: "Key message",
          text: "A pipeline is not the number of MoUs signed. It is the number of projects that can pass the lender's test and the state's test — and the discipline that gets them there protects the serious developer most.",
          source: "Bankable Is Not Enough — Chapter 1, The MoU Trap",
        },
      },
      narration: {
        "dev.title": "Bankable is not enough. Module D, for developers and development partners: what counts as a pipeline.",
        "dev.stages": "Consider what you actually hold at each stage. An MoU binds little in law, but it often grants exclusivity — it is an option on a site or a resource, cheap to obtain, valuable to hold, and saleable. A contract fixes tariff, term and obligations, conditional on the plant reaching operation. Only financial close counts as a pipeline.",
        "dev.denominator": "And the denominator is never published. Governments rarely publish the MoUs they sign, and developers have no reason to announce when one lapses. McKinsey estimated that fewer than ten percent of African infrastructure projects reach financial close, with eighty percent failing at the feasibility stage, and about thirty billion dollars of development costs sitting in that phase across the six largest markets. Development partners count MoUs as evidence of a pipeline. They are evidence of intent.",
        "dev.nachtigal": "This is not an argument for banning MoUs. Some projects cannot be tendered at the outset, because nobody yet knows enough to write a tender. Cameroon's Nachtigal plant was developed under a joint development agreement with EDF, the IFC and the national utility, and reached financial close with a local currency tranche of unprecedented tenor. But within months of commissioning in 2025, its payment guarantee was reported largely drawn. How a project begins matters. It does not settle how it will end.",
        "dev.ask": "So, what to expect and what to measure. Developers: expect MoUs to carry milestones, sunset clauses and, where appropriate, development securities. Serious developers have little to fear from any of these. Expect exclusivity to be limited and time-boxed, because a site held by a sponsor who cannot finance it blocks one who could. Development partners: measure pipelines by the number of projects that pass both tests, not by the number of MoUs signed.",
        "dev.key": "A pipeline is not the number of MoUs signed. It is the number of projects that can pass the lender's test and the state's test — and the discipline that gets them there protects the serious developer most.",
      },
    },
  },
};
