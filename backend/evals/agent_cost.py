"""Measure what one question to the ABM agent costs (spends API credits; run by hand).

    cd backend && python -m evals.agent_cost            # the 8 typical questions below

Prints tokens and dollars per question from the API's own usage counts. Prices are Claude Opus 5.5
list prices per million tokens (input $4, output $20 - thinking is billed as output, cache read
$0.20, 5-minute cache write $5); update PRICES if the model or the prices change.
"""

from app.agent.core import MODEL, BondAgent

PRICES = {"claude-opus-5-5": {"input": 4.0, "output": 20.0, "cache_read": 0.20, "cache_write": 5.0}}

QUESTIONS = [
    "Quel est le dernier rendement publié à 5 ans pour le Sénégal ?",
    "Combien rapporteraient 1 000 000 FCFA placés au Bénin sur 3 ans ?",
    "Compare le Sénégal, le Togo et le Mali à 5 ans pour 2 millions de FCFA.",
    "Quelles ont été les 10 dernières adjudications de la Côte d'Ivoire ?",
    "Comment un particulier de la diaspora peut-il acheter des bons du Trésor du Sénégal ?",
    "Quelles banques sont SVT en Côte d'Ivoire ?",
    "Quel est le dernier cours de l'obligation ECMR à la BVMAC ?",
    "Résume les résultats d'adjudication de la semaine.",
]


def cost(usage: dict, model: str = MODEL) -> float:
    p = PRICES[model]
    return (usage["input_tokens"] * p["input"] + usage["output_tokens"] * p["output"]
            + usage["cache_read_input_tokens"] * p["cache_read"] + usage["cache_creation_input_tokens"] * p["cache_write"]) / 1e6


def main() -> None:
    agent = BondAgent()
    total = 0.0
    for q in QUESTIONS:
        r = agent.ask(q)
        c = cost(r.usage)
        total += c
        print(f"${c:.4f}  {len(r.tool_calls)} tools  {r.usage}  {q}")
    print(f"\naverage ${total / len(QUESTIONS):.4f} per question over {len(QUESTIONS)} questions")


if __name__ == "__main__":
    main()
