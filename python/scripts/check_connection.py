"""Verify Pinecone connectivity and report what's actually in the index.

Run: python scripts/check_connection.py
Requires: PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_NAMESPACE
Does NOT require OpenAI or Anthropic keys.
"""

import sys

from pinecone import Pinecone

from rag_bot.config import ConfigError, load_settings


def main() -> int:
    try:
        settings = load_settings()
    except ConfigError as exc:
        print(f"Config problem: {exc}")
        return 1

    print(f"Index:     {settings.pinecone_index_name}")
    print(f"Namespace: {settings.pinecone_namespace}")
    print()

    pc = Pinecone(api_key=settings.pinecone_api_key)

    existing = [i["name"] for i in pc.list_indexes()]
    if settings.pinecone_index_name not in existing:
        print(f"Index not found. Available: {existing or '(none)'}")
        return 1

    index = pc.Index(settings.pinecone_index_name)
    stats = index.describe_index_stats()

    print(f"Dimension:      {stats.get('dimension')}")
    print(f"Total vectors:  {stats.get('total_vector_count')}")
    print()

    namespaces = stats.get("namespaces", {}) or {}
    print("Namespaces:")
    for name, info in sorted(namespaces.items()):
        marker = "  <- configured" if name == settings.pinecone_namespace else ""
        print(f"  {name}: {info.get('vector_count')} vectors{marker}")

    if settings.pinecone_namespace not in namespaces:
        print()
        print(f"Configured namespace {settings.pinecone_namespace!r} not found above.")
        return 1

    print()
    print("Connection OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
