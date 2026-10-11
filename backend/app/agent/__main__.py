"""Ask the ABM agent from the command line:  python -m app.agent "Quel est le dernier taux 5 ans du Sénégal ?"

Needs Anthropic credentials (ANTHROPIC_API_KEY or an `ant auth login` profile) and reads the feed from
ABM_FEED (a directory or an https URL), else site/dist/api/v1, else the public site.
"""

import sys

from app.agent.core import BondAgent


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    agent = BondAgent()
    history: list[dict] = []
    question = " ".join(sys.argv[1:])
    while question:
        r = agent.ask(question, history)
        history = r.messages
        print(r.answer)
        if r.sources:
            print("\nSources:\n" + "\n".join(f"- {u}" for u in r.sources))
        print(f"\n[{len(r.tool_calls)} tool calls · {r.usage}]")
        if not sys.stdin.isatty():
            break
        try:
            question = input("\n> ").strip()
        except EOFError:
            break


if __name__ == "__main__":
    main()
