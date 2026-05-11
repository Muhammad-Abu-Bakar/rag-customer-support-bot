# rag-customer-support-bot
# AI Customer Support Bot with RAG

Retrieval-augmented Telegram bot that answers questions about a SaaS product's
documentation, with citations back to source. Built end-to-end in n8n.

**Stack:** n8n · Pinecone · OpenAI (text-embedding-3-small + GPT-4o-mini) ·
Telegram Bot API

## Status
## Status
   ✓ Ingestion working (171 chunks across 7 Stripe webhook docs)
   ✓ Bot live on Telegram — try [@abubakar_rag_bot](https://t.me/abubakar_rag_bot)

## Demo
_(Coming in Step 7 — 30-second video + live bot link)_

## How it works
1. **Ingestion:** Upload docs → chunk (800 tok / 100 overlap) → embed with
   `text-embedding-3-small` → store in Pinecone with metadata.
2. **Retrieval:** User question → embed → top-k similarity search in Pinecone →
   pass chunks + question to GPT-4o-mini via the n8n AI Agent node.
3. **Response:** Grounded answer with inline citations to source docs.

## Repo structure
- `workflows/` — exported n8n workflow JSON
- `docs/` — setup, architecture, demo notes
- `samples/` — info about the demo dataset
- `screenshots/` — workflow canvas + demo screenshots

## Setup
See [`docs/SETUP.md`](docs/SETUP.md).

## Architecture
See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

Built by [Muhammad Abubakar](https://github.com/Muhammad-Abu-Bakar) — n8n /
AI Automation Engineer based in Lahore.
