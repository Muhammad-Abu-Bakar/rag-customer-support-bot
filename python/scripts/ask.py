"""Ask the support agent a question.

Run: python scripts/ask.py "how do I verify a webhook signature?"
"""

import sys

from rag_bot.agent import ask
from rag_bot.config import ConfigError, load_settings


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: python scripts/ask.py "your question here"')
        return 2

    question = " ".join(argv[1:])

    try:
        settings = load_settings()
    except ConfigError as exc:
        print(f"Config problem: {exc}")
        return 1

    print(f"Q: {question}")
    print()
    print(ask(question, settings))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
