"""Retrieve chunks for a question and print them with citations.

Run: python scripts/query.py "how do I verify a webhook signature?"
"""

import sys

from rag_bot.config import ConfigError, load_settings
from rag_bot.retrieval import retrieve

PREVIEW_CHARS = 400


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: python scripts/query.py "your question here"')
        return 2

    question = " ".join(argv[1:])

    try:
        settings = load_settings()
    except ConfigError as exc:
        print(f"Config problem: {exc}")
        return 1

    print(f"Question: {question}")
    print(f"Retrieving top {settings.top_k} from {settings.pinecone_namespace}...")
    print()

    chunks = retrieve(settings, question)

    if not chunks:
        print("No chunks returned.")
        return 1

    for i, chunk in enumerate(chunks, start=1):
        preview = chunk.text[:PREVIEW_CHARS]
        if len(chunk.text) > PREVIEW_CHARS:
            preview += "..."

        print(f"--- {i}  score={chunk.score:.4f}  type={chunk.doc_type}")
        print(f"    {chunk.citation}")
        print()
        print(preview)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
